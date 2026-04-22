from tools.roxy_client import RoxyClient, RoxyAPIError, RoxyClientError

TOKEN = "af28a5799bd369b50cdae3dcf085ddfa"
PORT = 50000
TARGET_URL = "https://vids.st/v/23670"
PROXY_RAW = "165.154.173.254:4733:G8g3TKqdi7fX:7G6nUjZB1w"
WORKSPACE_NAME = None
PROJECT_NAME = None


# 解析 host:port:username:password 形式的代理字符串。
def parse_proxy_raw(proxy_raw: str) -> tuple[str, str, str, str]:
    parts = proxy_raw.split(":", 3)
    if len(parts) != 4:
        raise ValueError("代理格式错误，必须为 host:port:username:password")
    host, port, username, password = parts
    if not host or not port:
        raise ValueError("代理格式错误，host 和 port 不能为空")
    return host, port, username, password


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


PROXY_HOST, PROXY_PORT, PROXY_USERNAME, PROXY_PASSWORD = parse_proxy_raw(PROXY_RAW)

client = RoxyClient(token=TOKEN, port=PORT, timeout=120)

try:
    workspace_resp = client.browser_workspace({"page_index": 1, "page_size": 100})
    workspace_id, project_id = resolve_workspace_project_id(
        workspace_resp,
        workspace_name=WORKSPACE_NAME,
        project_name=PROJECT_NAME,
    )
    print("workspace_id:", workspace_id, "project_id:", project_id)

    create_resp = client.browser_create({
        "workspaceId": workspace_id,
        "projectId": project_id,
        "windowName": "Demo-Window",
        "defaultOpenUrl": [TARGET_URL],
        "proxyInfo": {
            "proxyMethod": "custom",
            "proxyCategory": "HTTP",  # 或 HTTPS/SOCKS5
            "ipType": "IPV4",
            "host": PROXY_HOST,
            "port": PROXY_PORT,
            "proxyUserName": PROXY_USERNAME,
            "proxyPassword": PROXY_PASSWORD,
            "checkChannel": "IPRust.io",
        },
    })
    print("create_resp:", create_resp)

    # 兼容提取 dirId
    data = create_resp.get("data", {})
    if isinstance(data, dict) and "dirId" in data:
        dir_id = data["dirId"]
    elif isinstance(data, dict) and isinstance(data.get("rows"), list) and data["rows"]:
        dir_id = data["rows"][0]["dirId"]
    else:
        raise ValueError(f"未找到 dirId: {create_resp}")

    random_env_resp = client.browser_random_env({
        "workspaceId": workspace_id,
        "dirId": dir_id,
    })
    print("random_env_resp:", random_env_resp)

    open_resp = client.browser_open({
        "workspaceId": workspace_id,
        "dirId": dir_id,
    })
    print("open_resp:", open_resp)

except (RoxyAPIError, RoxyClientError, ValueError) as e:
    print("调用失败:", e)
finally:
    client.close()
