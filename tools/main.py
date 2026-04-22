from __future__ import annotations

import random
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

try:
    from tools.roxy_client import RoxyClient, RoxyAPIError, RoxyClientError
except ModuleNotFoundError:
    # 兼容在 tools 目录下直接执行：python main.py <token>
    from roxy_client import RoxyClient, RoxyAPIError, RoxyClientError

TOKEN = "af28a5799bd369b50cdae3dcf085ddfa"
PORT = 50000
TARGET_URLS = [
    "https://vids.st/v/23931",
]
PROXY_RAWS = [
    "proxy.veproxy.com:10000:res_4_lp_842_w65f:ef7ed145-a545-ad83-472e-97662e09db12",
    "proxy.veproxy.com:10001:res_4_lp_842_w65f:ef7ed145-a545-ad83-472e-97662e09db12",
    "proxy.veproxy.com:10002:res_4_lp_842_w65f:ef7ed145-a545-ad83-472e-97662e09db12",
    "proxy.veproxy.com:10003:res_4_lp_842_w65f:ef7ed145-a545-ad83-472e-97662e09db12",
    "proxy.veproxy.com:10004:res_4_lp_842_w65f:ef7ed145-a545-ad83-472e-97662e09db12",
]
# 窗口槽位数量：槽位少会自动多轮执行，直到所有 URL+代理 组合都跑完。
WINDOW_COUNT = 5
WORKSPACE_NAME = None
PROJECT_NAME = None
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400
SCREEN_WIDTH_OVERRIDE = None
WINDOW_NAME_PREFIX = "Auto-Visit-"
# 是否启用无头模式打开浏览器窗口（通过 browser_open 的 args 注入）。
HEADLESS_MODE = False
# 是否仅使用已有窗口（不创建新窗口）。
USE_EXISTING_WINDOWS_ONLY = False
# 指纹中的时区是否跟随 IP 自动匹配（文档字段: fingerInfo.isTimeZone）。
TIMEZONE_FOLLOW_IP = True
# 每个任务完成后是否立即关闭窗口。
AUTO_CLOSE_AFTER_TASK = True
# 打开窗口后的随机等待区间（秒）。
WAIT_AFTER_OPEN_RANGE = (3.0, 6.0)
# 点击页面后的随机等待区间（秒）。
WAIT_AFTER_CLICK_RANGE = (20.0, 40.0)
# 页面加载超时时间（毫秒）。
PAGE_LOAD_TIMEOUT_MS = 45000
# 页面加载失败后的最大重载次数（不含首次加载）。
PAGE_RELOAD_MAX_RETRIES = 2
# 每次重载前的随机等待区间（秒）。
PAGE_RELOAD_DELAY_RANGE = (1.0, 2.0)
# 每一轮目标总时长区间（秒），默认约 3 分钟。
# 规则：从一轮开始计时，若本轮执行时长小于目标时长则补等待；超过则直接下一轮。
CYCLE_TARGET_DURATION_RANGE = (60.0, 70.0)
# 点击时优先使用页面中心，避免点到无效区域。
CLICK_RATIO_X = 0.3
CLICK_RATIO_Y = 0.4
# 每轮打开前是否清理本地缓存，尽量避免同一窗口残留多个历史标签页。
CLEAR_LOCAL_CACHE_BEFORE_OPEN = True
# 每轮打开前是否清理服务器缓存，进一步避免历史标签页回灌。
CLEAR_SERVER_CACHE_BEFORE_OPEN = True
# Playwright 页面操作是否放到子进程执行，避免主进程因底层崩溃退出。
PLAYWRIGHT_IN_SUBPROCESS = True
# 子进程页面操作超时时间（秒）。
PLAYWRIGHT_ACTION_TIMEOUT_SEC = 120
# 发生未知异常后的兜底等待区间（秒），避免异常风暴打满 CPU。
FATAL_BACKOFF_RANGE = (3.0, 8.0)
# 是否忽略 Ctrl+C，忽略后程序不会退出，会继续下一轮。
IGNORE_KEYBOARD_INTERRUPT = True


# 输出统一中文状态日志，便于观察任务进度。
def log_status(stage: str, message: str) -> None:
    now = time.strftime("%H:%M:%S")
    print(f"[{now}][{stage}] {message}")


# 解析命令行参数：支持 token 与子进程动作参数。
def parse_cli_args(argv: list[str]) -> tuple[str | None, str | None, str | None, str | None]:
    token: str | None = None
    worker_action: str | None = None
    worker_http: str | None = None
    worker_url: str | None = None
    idx = 1
    while idx < len(argv):
        arg = argv[idx]
        if arg == "--worker-action" and idx + 1 < len(argv):
            worker_action = argv[idx + 1]
            idx += 2
            continue
        if arg == "--worker-http" and idx + 1 < len(argv):
            worker_http = argv[idx + 1]
            idx += 2
            continue
        if arg == "--worker-url" and idx + 1 < len(argv):
            worker_url = argv[idx + 1]
            idx += 2
            continue
        if not arg.startswith("--") and token is None:
            token = arg.strip()
            idx += 1
            continue
        idx += 1
    return token, worker_action, worker_http, worker_url


# 生成 open 接口参数，按开关启用无头模式。
def build_open_args() -> list[str]:
    args: list[str] = []
    if HEADLESS_MODE:
        args.append("--headless=new")
    return args


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


# 构建基础指纹配置，避免多个接口修改窗口时字段不一致。
def build_finger_info_base() -> dict:
    return {
        "syncTab": False,
        "isTimeZone": TIMEZONE_FOLLOW_IP,
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
        tasks.append(
            {
                "url_index": idx,
                "proxy_index": idx,
                "url": target_urls[idx],
                "proxy_raw": proxy_raws[idx],
            }
        )

    # 第二阶段：补齐剩余组合，保证每个 URL+代理 组合最多只访问一次。
    for url_idx, url in enumerate(target_urls):
        for proxy_idx, proxy_raw in enumerate(proxy_raws):
            key = (url_idx, proxy_idx)
            if key in used:
                continue
            used.add(key)
            tasks.append(
                {
                    "url_index": url_idx,
                    "proxy_index": proxy_idx,
                    "url": url,
                    "proxy_raw": proxy_raw,
                }
            )

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
    resp = client.browser_list_v3(
        {
            "workspaceId": workspace_id,
            "page_index": 1,
            "page_size": 500,
        }
    )
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


# 提取窗口列表中的 dirId 队列。
def extract_window_ids(rows: list[dict]) -> list[str]:
    ids: list[str] = []
    for row in rows:
        dir_id = row.get("dirId")
        if isinstance(dir_id, str) and dir_id:
            ids.append(dir_id)
    return ids


# 规范化 http 调试地址。
def normalize_http_endpoint(http_value: Any) -> str | None:
    if not isinstance(http_value, str) or not http_value.strip():
        return None
    http_value = http_value.strip()
    if http_value.startswith("http://") or http_value.startswith("https://"):
        return http_value
    return f"http://{http_value}"


# 在子进程执行页面动作，避免主进程受 Playwright 崩溃影响。
def run_playwright_action_in_subprocess(action: str, http_endpoint: str, target_url: str) -> bool:
    cmd = [
        sys.executable,
        "-u",
        str(Path(__file__).resolve()),
        "--worker-action",
        action,
        "--worker-http",
        http_endpoint,
        "--worker-url",
        target_url,
    ]
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=PLAYWRIGHT_ACTION_TIMEOUT_SEC,
        )
    except subprocess.TimeoutExpired:
        log_status("子进程超时", f"{action} 超时 {PLAYWRIGHT_ACTION_TIMEOUT_SEC}s，判定失败")
        return False
    except Exception as exc:
        log_status("子进程失败", f"{action} 启动异常: {exc}")
        return False

    if result.returncode == 0:
        return True

    output = (result.stdout or "").strip()
    error = (result.stderr or "").strip()
    if output:
        log_status("子进程输出", output[-300:])
    if error:
        log_status("子进程错误", error[-300:])
    log_status("子进程退出", f"{action} returncode={result.returncode}")
    return False


# 在当前进程中等待目标页面加载完成（domcontentloaded + load）。
def wait_page_loaded_local(http_endpoint: str, target_url: str) -> bool:
    try:
        from playwright.sync_api import sync_playwright
    except Exception as exc:
        log_status("加载跳过", f"Playwright 不可用: {exc}")
        return False

    try:
        with sync_playwright() as pw:
            browser = pw.chromium.connect_over_cdp(http_endpoint)
            context = browser.contexts[0] if browser.contexts else browser.new_context()

            page = None
            for _ in range(30):
                for p in context.pages:
                    if target_url in (p.url or ""):
                        page = p
                        break
                if page:
                    break
                time.sleep(0.5)

            if page is None and context.pages:
                page = context.pages[0]
            if page is None:
                page = context.new_page()
                page.goto(target_url, wait_until="domcontentloaded", timeout=PAGE_LOAD_TIMEOUT_MS)

            max_attempts = PAGE_RELOAD_MAX_RETRIES + 1
            for attempt in range(max_attempts):
                attempt_no = attempt + 1
                try:
                    page.bring_to_front()
                    page.wait_for_load_state("domcontentloaded", timeout=PAGE_LOAD_TIMEOUT_MS)
                    page.wait_for_load_state("load", timeout=PAGE_LOAD_TIMEOUT_MS)
                    browser.close()
                    return True
                except Exception as exc:
                    log_status("加载重试", f"第 {attempt_no}/{max_attempts} 次失败: {exc}")
                    if attempt_no >= max_attempts:
                        break
                    delay = random.uniform(*PAGE_RELOAD_DELAY_RANGE)
                    log_status("加载重试", f"重载前等待 {delay:.2f}s")
                    time.sleep(delay)
                    try:
                        page.reload(wait_until="domcontentloaded", timeout=PAGE_LOAD_TIMEOUT_MS)
                    except Exception as reload_exc:
                        log_status("加载重试", f"重载失败: {reload_exc}")

            browser.close()
            return False
    except Exception as exc:
        log_status("加载失败", str(exc))
        return False


# 在当前进程中执行一次点击。
def click_page_once_local(http_endpoint: str, target_url: str) -> bool:
    try:
        from playwright.sync_api import sync_playwright
    except Exception as exc:
        log_status("点击跳过", f"Playwright 不可用: {exc}")
        return False

    try:
        with sync_playwright() as pw:
            browser = pw.chromium.connect_over_cdp(http_endpoint)
            context = browser.contexts[0] if browser.contexts else browser.new_context()

            # 优先定位目标 URL 页面，找不到则用当前页或新开页。
            page = None
            for p in context.pages:
                if target_url in (p.url or ""):
                    page = p
                    break
            if page is None and context.pages:
                page = context.pages[0]
            if page is None:
                page = context.new_page()
                page.goto(target_url, wait_until="domcontentloaded", timeout=60000)

            page.bring_to_front()
            viewport = page.viewport_size or {"width": WINDOW_WIDTH, "height": WINDOW_HEIGHT}
            click_x = max(1, int(viewport["width"] * CLICK_RATIO_X))
            click_y = max(1, int(viewport["height"] * CLICK_RATIO_Y))
            page.mouse.click(click_x, click_y)

            # 仅断开控制连接，不主动关闭真实浏览器窗口。
            browser.close()
            return True
    except Exception as exc:
        log_status("点击失败", str(exc))
        return False


# 等待目标页面加载完成（可选子进程隔离）。
def wait_page_loaded(http_endpoint: str, target_url: str) -> bool:
    if PLAYWRIGHT_IN_SUBPROCESS:
        return run_playwright_action_in_subprocess("wait_loaded", http_endpoint, target_url)
    return wait_page_loaded_local(http_endpoint, target_url)


# 在已打开页面中心执行一次点击（可选子进程隔离）。
def click_page_once(http_endpoint: str, target_url: str) -> bool:
    if PLAYWRIGHT_IN_SUBPROCESS:
        return run_playwright_action_in_subprocess("click_once", http_endpoint, target_url)
    return click_page_once_local(http_endpoint, target_url)


# 在区间内随机等待。
def sleep_random(wait_range: tuple[float, float], label: str) -> float:
    start, end = wait_range
    if start < 0 or end < 0 or end < start:
        raise ValueError(f"等待区间配置错误: {wait_range}")
    duration = random.uniform(start, end)
    print(f"{label}: sleep {duration:.2f}s")
    time.sleep(duration)
    return duration


# 子进程入口：执行单个 Playwright 动作并返回退出码。
def run_worker_action(action: str, http_endpoint: str, target_url: str) -> int:
    if not http_endpoint or not target_url:
        log_status("子进程参数错误", "缺少 http_endpoint 或 target_url")
        return 2
    if action == "wait_loaded":
        return 0 if wait_page_loaded_local(http_endpoint, target_url) else 3
    if action == "click_once":
        return 0 if click_page_once_local(http_endpoint, target_url) else 4
    log_status("子进程参数错误", f"未知动作: {action}")
    return 2


def run_one_cycle(client: RoxyClient, cycle_no: int) -> None:
    log_status("轮次开始", f"第 {cycle_no} 轮开始执行")
    tasks = build_visit_tasks(TARGET_URLS, PROXY_RAWS)
    max_windows = len(tasks)
    if WINDOW_COUNT <= 0:
        raise ValueError("WINDOW_COUNT 必须大于 0")
    if WINDOW_COUNT > max_windows:
        raise ValueError(
            f"窗口数量超过可分配组合上限：WINDOW_COUNT={WINDOW_COUNT}, 上限={max_windows}"
        )
    effective_window_count = min(WINDOW_COUNT, len(tasks))
    if effective_window_count < WINDOW_COUNT:
        log_status(
            "窗口提示",
            f"组合任务数仅 {len(tasks)}，本轮最多使用 {effective_window_count} 个窗口槽位",
        )

    workspace_resp = client.browser_workspace({"page_index": 1, "page_size": 100})
    workspace_id, project_id = resolve_workspace_project_id(
        workspace_resp,
        workspace_name=WORKSPACE_NAME,
        project_name=PROJECT_NAME,
    )
    log_status("空间信息", f"workspace_id={workspace_id}, project_id={project_id}")

    screen_width = get_screen_width(SCREEN_WIDTH_OVERRIDE)
    log_status("屏幕信息", f"screen_width={screen_width}, 无头模式={'开启' if HEADLESS_MODE else '关闭'}")

    existing_rows = list_existing_windows(client, workspace_id)
    window_name_map = build_window_name_map(existing_rows)
    existing_ids = extract_window_ids(existing_rows)

    # 初始化窗口槽位：优先绑定同名窗口，其次复用其他已有窗口，最后才尝试创建。
    slots: list[dict[str, Any]] = []
    assigned_ids: set[str] = set()
    for slot_index in range(effective_window_count):
        window_name = f"{WINDOW_NAME_PREFIX}{slot_index + 1}"
        dir_id = window_name_map.get(window_name)
        if isinstance(dir_id, str) and dir_id:
            assigned_ids.add(dir_id)
        slots.append({"window_name": window_name, "dir_id": dir_id})

    reusable_existing_ids = [x for x in existing_ids if x not in assigned_ids]
    for slot in slots:
        if slot["dir_id"]:
            continue
        if reusable_existing_ids:
            slot["dir_id"] = reusable_existing_ids.pop(0)
            assigned_ids.add(slot["dir_id"])

    # 按轮执行：每轮先把所有槽位窗口都打开，再做后续等待/点击/关闭。
    for round_start in range(0, len(tasks), effective_window_count):
        round_tasks = tasks[round_start : round_start + effective_window_count]
        round_index = round_start // effective_window_count + 1
        opened_windows: list[dict[str, Any]] = []

        # 第一阶段：准备并打开本轮所有窗口（实现“同时打开”的效果）。
        for offset, task in enumerate(round_tasks):
            task_idx = round_start + offset
            slot_index = offset
            slot = slots[slot_index]
            window_name = slot["window_name"]
            try:
                proxy_info = build_proxy_info(task["proxy_raw"])
                dir_id = slot["dir_id"]

                log_status(
                    "任务开始",
                    f"task[{task_idx + 1}/{len(tasks)}] round={round_index} slot={slot_index + 1} "
                    f"url_idx={task['url_index'] + 1} proxy_idx={task['proxy_index'] + 1}",
                )

                if dir_id:
                    # 窗口已存在：更新该窗口的代理和目标 URL。
                    mdf_resp = client.browser_mdf(
                        {
                            "workspaceId": workspace_id,
                            "projectId": project_id,
                            "dirId": dir_id,
                            "windowName": window_name,
                            "defaultOpenUrl": [task["url"]],
                            "proxyInfo": proxy_info,
                            "fingerInfo": build_finger_info_base(),
                        }
                    )
                    print(f"[{window_name}] mdf_resp:", mdf_resp)
                else:
                    # 槽位无可用窗口时尝试创建；若额度不足则降级复用剩余已有窗口。
                    if USE_EXISTING_WINDOWS_ONLY:
                        raise ValueError(f"[{window_name}] 未找到可复用窗口，且已禁用创建新窗口")
                    try:
                        create_resp = client.browser_create(
                            {
                                "workspaceId": workspace_id,
                                "projectId": project_id,
                                "windowName": window_name,
                                "defaultOpenUrl": [task["url"]],
                                "proxyInfo": proxy_info,
                                "fingerInfo": build_finger_info_base(),
                            }
                        )
                        dir_id = extract_dir_id(create_resp)
                        slot["dir_id"] = dir_id
                        window_name_map[window_name] = dir_id
                        print(f"[{window_name}] create_resp:", create_resp)
                    except RoxyAPIError as exc:
                        if exc.code != 409:
                            raise
                        if reusable_existing_ids:
                            dir_id = reusable_existing_ids.pop(0)
                            slot["dir_id"] = dir_id
                            print(f"[{window_name}] create_skip_409: 额度不足，改用现有窗口 {dir_id}")
                        else:
                            raise ValueError("窗口额度不足，且没有可复用的现有窗口")

                # 每次打开前都先随机指纹。
                random_env_resp = client.browser_random_env(
                    {
                        "workspaceId": workspace_id,
                        "dirId": dir_id,
                    }
                )
                print(f"[{window_name}] random_env_resp:", random_env_resp)

                # 自动按屏幕宽度平铺窗口位置与大小。
                layout_resp = client.browser_auto_tile_window_layout(
                    workspace_id=workspace_id,
                    dir_id=dir_id,
                    slot_index=slot_index,
                    screen_width=screen_width,
                    width=WINDOW_WIDTH,
                    height=WINDOW_HEIGHT,
                    extra_payload={"fingerInfo": build_finger_info_base()},
                )
                print(f"[{window_name}] layout_resp:", layout_resp)

                if CLEAR_LOCAL_CACHE_BEFORE_OPEN:
                    clear_local_resp = client.browser_clear_local_cache({"dirIds": [dir_id]})
                    print(f"[{window_name}] clear_local_resp:", clear_local_resp)
                if CLEAR_SERVER_CACHE_BEFORE_OPEN:
                    clear_server_resp = client.browser_clear_server_cache(
                        {"workspaceId": workspace_id, "dirIds": [dir_id]}
                    )
                    print(f"[{window_name}] clear_server_resp:", clear_server_resp)

                open_payload = {
                    "workspaceId": workspace_id,
                    "dirId": dir_id,
                    "args": build_open_args(),
                }
                open_resp = client.browser_open(open_payload)
                print(f"[{window_name}] open_resp:", open_resp)
                opened_windows.append(
                    {
                        "window_name": window_name,
                        "dir_id": dir_id,
                        "url": task["url"],
                        "open_resp": open_resp,
                    }
                )
            except Exception as exc:
                log_status("任务失败", f"{window_name} 准备/开窗失败，已跳过: {exc}")
                continue

        # 第二阶段：对本轮已打开的窗口执行加载等待、点击、关窗。
        for item in opened_windows:
            window_name = item["window_name"]
            dir_id = item["dir_id"]
            target_url = item["url"]
            open_resp = item["open_resp"]

            try:
                open_data = open_resp.get("data", {}) if isinstance(open_resp, dict) else {}
                http_endpoint = normalize_http_endpoint(open_data.get("http") if isinstance(open_data, dict) else None)
                loaded = False
                if http_endpoint:
                    loaded = wait_page_loaded(http_endpoint=http_endpoint, target_url=target_url)
                    print(f"[{window_name}] page_loaded:", loaded)
                else:
                    print(f"[{window_name}] page_loaded: False (缺少 http 调试地址)")

                if loaded:
                    sleep_random(WAIT_AFTER_OPEN_RANGE, f"[{window_name}] wait_after_open")
                    clicked = click_page_once(http_endpoint=http_endpoint, target_url=target_url)
                    print(f"[{window_name}] clicked:", clicked)
                    sleep_random(WAIT_AFTER_CLICK_RANGE, f"[{window_name}] wait_after_click")
                else:
                    print(f"[{window_name}] 跳过等待与点击：页面未确认加载完成")
            except Exception as exc:
                log_status("任务失败", f"{window_name} 页面操作失败，已跳过: {exc}")
            finally:
                if AUTO_CLOSE_AFTER_TASK:
                    try:
                        close_resp = client.browser_close(
                            {
                                "workspaceId": workspace_id,
                                "dirId": dir_id,
                            }
                        )
                        print(f"[{window_name}] close_resp:", close_resp)
                    except Exception as exc:
                        log_status("关窗失败", f"{window_name} 关闭失败，将在下一轮继续复用: {exc}")
    log_status("轮次结束", f"第 {cycle_no} 轮执行完成")


def main() -> None:
    token_arg, worker_action, worker_http, worker_url = parse_cli_args(sys.argv)
    if worker_action:
        exit_code = run_worker_action(worker_action, worker_http or "", worker_url or "")
        raise SystemExit(exit_code)

    runtime_token = token_arg or TOKEN
    token_source = "命令行参数" if token_arg else "默认配置"
    log_status("启动配置", f"token 来源: {token_source}")
    client = RoxyClient(token=runtime_token, port=PORT, timeout=120)
    cycle_no = 1
    try:
        while True:
            cycle_start_at = time.monotonic()
            cycle_target = random.uniform(*CYCLE_TARGET_DURATION_RANGE)
            try:
                run_one_cycle(client, cycle_no)
            except KeyboardInterrupt:
                if IGNORE_KEYBOARD_INTERRUPT:
                    log_status("中断忽略", "收到 Ctrl+C，按配置忽略并继续循环")
                else:
                    raise
            except Exception as exc:
                log_status("轮次失败", f"cycle {cycle_no} 异常: {exc}")
                backoff = random.uniform(*FATAL_BACKOFF_RANGE)
                log_status("异常退避", f"等待 {backoff:.2f}s 后继续下一轮")
                time.sleep(backoff)

            cycle_elapsed = time.monotonic() - cycle_start_at
            remain = cycle_target - cycle_elapsed
            if remain > 0:
                log_status(
                    "节奏控制",
                    f"cycle {cycle_no}: 已运行 {cycle_elapsed:.2f}s, "
                    f"目标 {cycle_target:.2f}s, 补等待 {remain:.2f}s",
                )
                time.sleep(remain)
            else:
                log_status(
                    "节奏控制",
                    f"cycle {cycle_no}: 已运行 {cycle_elapsed:.2f}s, "
                    f"超过目标 {cycle_target:.2f}s, 直接开始下一轮",
                )
            cycle_no += 1
    finally:
        client.close()


if __name__ == "__main__":
    main()
