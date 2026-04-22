from __future__ import annotations

from tools.roxy_client import RoxyClient, RoxyAPIError, RoxyClientError

TOKEN = "af28a5799bd369b50cdae3dcf085ddfa"
PORT = 50000
TARGET_URLS = [
    "https://vids.st/v/23672",
    "https://vids.st/v/23803",
    "https://vids.st/v/23812"
]
PROXY_RAWS = [
    "165.154.173.254:4733:G8g3TKqdi7fX:7G6nUjZB1w",
    "165.154.173.254:5103:gGfVV1TbhVqN:8MP7QPbRF9bY"
]
WINDOW_COUNT = 3
WORKSPACE_NAME = None
PROJECT_NAME = None
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 400
SCREEN_WIDTH_OVERRIDE = None
WINDOW_NAME_PREFIX = "Auto-Visit-"


# 解析 host:port:username:password 形式的代理字符串。
def parse_proxy_raw(proxy_raw: str) -> tuple[str, str, str, str]:
    parts = proxy_raw.split(":", 3)
    if len(parts) != 4:
        raise ValueError("代理格式错误，必须为 host:port:username:password")
    host, port, username, password = parts
    if not host or not port:
        raise ValueError("代理格式错误，host 和 port 不能为空")
    return host, port, username, password


# 构建代理配置对象，供 create/mdf 接口复用。
def build_proxy_info(proxy_raw: str) -> dict:
    host, port, username, password = parse_proxy_raw(proxy_raw)
    return {
        "proxyMethod": "custom",
        "proxyCategory": "HTTP",  # 或 HTTPS/SOCKS5
        "ipType": "IPV4",
        "host": host,
        "port": port,
        "proxyUserName": username,
        "proxyPassword": password,
        "checkChannel": "IPRust.io",
    }


# 从创建接口响应中提取窗口 dirId。
def extract_dir_id(resp: dict) -> str:
    data = resp.get("data", {})
    if isinstance(data, dict) and "dirId" in data:
        return data["dirId"]
    if isinstance(data, dict) and isinstance(data.get("rows"), list) and data["rows"]:
        return data["rows"][0]["dirId"]
    raise ValueError(f"未找到 dirId: {resp}")


# 生成 URL+代理 的唯一任务列表：先按同索引配对，再补齐剩余笛卡尔组合。
def build_visit_tasks(target_urls: list[str], proxy_raws: list[str]) -> list[dict]:
    if not target_urls:
        raise ValueError("TARGET_URLS 不能为空")
    if not proxy_raws:
        raise ValueError("PROXY_RAWS 不能为空")

    tasks: list[dict] = []
    used: set[tuple[int, int]] = set()

    # 第一阶段：优先满足你给的顺序语义，如 url1-proxy1, url2-proxy2。
    for idx in range(min(len(target_urls), len(proxy_raws))):
        key = (idx, idx)
        used.add(key)
        tasks.append({
            "url_index": idx,
            "proxy_index": idx,
            "url": target_urls[idx],
            "proxy_raw": proxy_raws[idx],
        })

    # 第二阶段：补齐剩余组合，保证每个 URL+代理 组合最多只访问一次。
    for url_idx, url in enumerate(target_urls):
        for proxy_idx, proxy_raw in enumerate(proxy_raws):
            key = (url_idx, proxy_idx)
            if key in used:
                continue
            used.add(key)
            tasks.append({
                "url_index": url_idx,
                "proxy_index": proxy_idx,
                "url": url,
                "proxy_raw": proxy_raw,
            })

    return tasks


# 自动从空间列表中解析 workspaceId 和 projectId。
def resolve_workspace_project_id(
        workspace_resp: dict,
        workspace_name: str | None = None,
        project_name: str | None = None,
) -> tuple[int, int]:
    rows = workspace_resp.get("data", {}).get("rows", [])
    if not isinstance(rows, list) or not rows:
        raise ValueError(f"未获取到可用空间列表: {workspace_resp}")

    # 优先按空间名称匹配，否则默认选择第一个空间。
    chosen_workspace = None
    if workspace_name:
        for row in rows:
            if isinstance(row, dict) and row.get("workspaceName") == workspace_name:
                chosen_workspace = row
                break
    if chosen_workspace is None:
        chosen_workspace = rows[0]

    workspace_id = chosen_workspace.get("id")
    if not isinstance(workspace_id, int):
        raise ValueError(f"空间ID无效: {chosen_workspace}")

    project_details = chosen_workspace.get("project_details", [])
    if not isinstance(project_details, list) or not project_details:
        raise ValueError(f"空间下没有可用项目: {chosen_workspace}")

    # 优先按项目名称匹配，否则默认选择第一个项目。
    chosen_project = None
    if project_name:
        for item in project_details:
            if isinstance(item, dict) and item.get("projectName") == project_name:
                chosen_project = item
                break
    if chosen_project is None:
        chosen_project = project_details[0]

    project_id = chosen_project.get("projectId")
    if not isinstance(project_id, int):
        raise ValueError(f"项目ID无效: {chosen_project}")

    return workspace_id, project_id


# 自动获取主屏幕宽度，可通过参数覆盖。
def get_screen_width(override_width: int | None = None) -> int:
    if isinstance(override_width, int) and override_width > 0:
        return override_width
    try:
        import tkinter as tk

        root = tk.Tk()
        root.withdraw()
        width = int(root.winfo_screenwidth())
        root.destroy()
        return width if width > 0 else 1920
    except Exception:
        return 1920


# 获取 workspace 中现有窗口列表。
def list_existing_windows(client: RoxyClient, workspace_id: int) -> list[dict]:
    resp = client.browser_list_v3({
        "workspaceId": workspace_id,
        "page_index": 1,
        "page_size": 500,
    })
    rows = resp.get("data", {}).get("rows", [])
    if isinstance(rows, list):
        return [row for row in rows if isinstance(row, dict)]
    return []


# 生成窗口名到 dirId 的映射，便于复用已有窗口。
def build_window_name_map(rows: list[dict]) -> dict[str, str]:
    name_map: dict[str, str] = {}
    for row in rows:
        name = row.get("windowName")
        dir_id = row.get("dirId")
        if isinstance(name, str) and isinstance(dir_id, str) and name:
            name_map[name] = dir_id
    return name_map


client = RoxyClient(token=TOKEN, port=PORT, timeout=120)

try:
    tasks = build_visit_tasks(TARGET_URLS, PROXY_RAWS)
    max_windows = len(tasks)
    if WINDOW_COUNT <= 0:
        raise ValueError("WINDOW_COUNT 必须大于 0")
    if WINDOW_COUNT > max_windows:
        raise ValueError(
            f"窗口数量超过可分配组合上限：WINDOW_COUNT={WINDOW_COUNT}, 上限={max_windows}"
        )

    # 本次需要处理的任务（每个 URL+代理 组合只会出现一次）。
    selected_tasks = tasks[:WINDOW_COUNT]

    workspace_resp = client.browser_workspace({"page_index": 1, "page_size": 100})
    workspace_id, project_id = resolve_workspace_project_id(
        workspace_resp,
        workspace_name=WORKSPACE_NAME,
        project_name=PROJECT_NAME,
    )
    print("workspace_id:", workspace_id, "project_id:", project_id)

    screen_width = get_screen_width(SCREEN_WIDTH_OVERRIDE)
    print("screen_width:", screen_width)

    existing_rows = list_existing_windows(client, workspace_id)
    window_name_map = build_window_name_map(existing_rows)

    for slot_index, task in enumerate(selected_tasks):
        window_name = f"{WINDOW_NAME_PREFIX}{slot_index + 1}"
        proxy_info = build_proxy_info(task["proxy_raw"])
        dir_id = window_name_map.get(window_name)

        if dir_id:
            # 窗口已存在：更新该窗口的代理和目标 URL。
            mdf_resp = client.browser_mdf({
                "workspaceId": workspace_id,
                "projectId": project_id,
                "dirId": dir_id,
                "windowName": window_name,
                "defaultOpenUrl": [task["url"]],
                "proxyInfo": proxy_info,
            })
            print(f"[{window_name}] mdf_resp:", mdf_resp)
        else:
            # 窗口不存在：创建新窗口。
            create_resp = client.browser_create({
                "workspaceId": workspace_id,
                "projectId": project_id,
                "windowName": window_name,
                "defaultOpenUrl": [task["url"]],
                "proxyInfo": proxy_info,
            })
            dir_id = extract_dir_id(create_resp)
            print(f"[{window_name}] create_resp:", create_resp)

        # 每次打开前都先随机指纹。
        random_env_resp = client.browser_random_env({
            "workspaceId": workspace_id,
            "dirId": dir_id,
        })
        print(f"[{window_name}] random_env_resp:", random_env_resp)

        # 自动按屏幕宽度平铺窗口位置与大小。
        layout_resp = client.browser_auto_tile_window_layout(
            workspace_id=workspace_id,
            dir_id=dir_id,
            slot_index=slot_index,
            screen_width=screen_width,
            width=WINDOW_WIDTH,
            height=WINDOW_HEIGHT,
        )
        print(f"[{window_name}] layout_resp:", layout_resp)

        # 打开窗口。
        open_resp = client.browser_open({
            "workspaceId": workspace_id,
            "dirId": dir_id,
        })
        print(f"[{window_name}] open_resp:", open_resp)

except (RoxyAPIError, RoxyClientError, ValueError) as e:
    print("调用失败:", e)
finally:
    client.close()
