from __future__ import annotations

import json
import random
import shutil
import subprocess
import sys
import threading
import time
import unicodedata
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

try:
    from tools.roxy_client import RoxyClient, RoxyAPIError, RoxyClientError
except ModuleNotFoundError:
    # 兼容在 tools 目录下直接执行：python main.py <token>
    from roxy_client import RoxyClient, RoxyAPIError, RoxyClientError

DEFAULT_CONFIG: dict[str, Any] = {
    "token": "",
    "port": 50000,
    "target_urls": [],
    "proxy_raws": [],
    "window_count": 5,
    "urls_per_window_per_round": None,
    "workspace_name": None,
    "project_name": None,
    "window_width": 600,
    "window_height": 400,
    "screen_width_override": None,
    "window_name_prefix": "Auto-Visit-",
    "headless_mode": True,
    "use_existing_windows_only": False,
    "timezone_follow_ip": True,
    "auto_close_after_task": False,
    "wait_after_open_range": [3.0, 6.0],
    "wait_after_click_range": [20.0, 40.0],
    "page_load_timeout_ms": 45000,
    "page_reload_max_retries": 2,
    "page_reload_delay_range": [1.0, 2.0],
    "cycle_target_duration_range": [60.0, 70.0],
    "click_ratio_x": 0.3,
    "click_ratio_y": 0.4,
    "clear_local_cache_before_open": True,
    "clear_server_cache_before_open": True,
    "playwright_in_subprocess": True,
    "playwright_action_timeout_sec": 120,
    "fatal_backoff_range": [3.0, 8.0],
    "ignore_keyboard_interrupt": True,
}

CONFIG_PATH = Path(__file__).resolve().parent / "runtime_config.json"
CONFIG_EXAMPLE_PATH = Path(__file__).resolve().parent / "runtime_config.example.json"


# 读取 JSON 配置并与默认配置合并，保证每次启动都从配置文件加载。
def load_runtime_config() -> dict[str, Any]:
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(
            f"未找到配置文件: {CONFIG_PATH}。请基于 {CONFIG_EXAMPLE_PATH} 创建 runtime_config.json"
        )
    try:
        raw = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"配置文件 JSON 格式错误: {exc}") from exc
    if not isinstance(raw, dict):
        raise ValueError("配置文件顶层必须为 JSON 对象")

    merged = dict(DEFAULT_CONFIG)
    merged.update(raw)
    return merged


# 将配置值标准化为两元素浮点区间，统一用于随机等待与节奏控制。
def normalize_range(value: Any, key: str) -> tuple[float, float]:
    if not isinstance(value, (list, tuple)) or len(value) != 2:
        raise ValueError(f"配置项 {key} 必须是长度为 2 的数组")
    start = float(value[0])
    end = float(value[1])
    if start < 0 or end < 0 or end < start:
        raise ValueError(f"配置项 {key} 区间非法: {value}")
    return start, end


def normalize_bool(value: Any, key: str, default: bool) -> bool:
    """将配置项解析为布尔值，避免字符串 \"false\" 被误判为 True。"""
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    if isinstance(value, str):
        text = value.strip().lower()
        if text in {"1", "true", "yes", "y", "on"}:
            return True
        if text in {"0", "false", "no", "n", "off"}:
            return False
    raise ValueError(f"配置项 {key} 不是合法布尔值: {value!r}")


RUNTIME_CONFIG = load_runtime_config()
TOKEN = str(RUNTIME_CONFIG.get("token", "")).strip()
PORT = int(RUNTIME_CONFIG.get("port", 50000))
TARGET_URLS = [str(x).strip() for x in RUNTIME_CONFIG.get("target_urls", []) if str(x).strip()]
PROXY_RAWS = [str(x).strip() for x in RUNTIME_CONFIG.get("proxy_raws", []) if str(x).strip()]
WINDOW_COUNT = int(RUNTIME_CONFIG.get("window_count", 5))
URLS_PER_WINDOW_PER_ROUND = RUNTIME_CONFIG.get("urls_per_window_per_round")
WORKSPACE_NAME = RUNTIME_CONFIG.get("workspace_name")
PROJECT_NAME = RUNTIME_CONFIG.get("project_name")
WINDOW_WIDTH = int(RUNTIME_CONFIG.get("window_width", 600))
WINDOW_HEIGHT = int(RUNTIME_CONFIG.get("window_height", 400))
SCREEN_WIDTH_OVERRIDE = RUNTIME_CONFIG.get("screen_width_override")
WINDOW_NAME_PREFIX = str(RUNTIME_CONFIG.get("window_name_prefix", "Auto-Visit-"))
HEADLESS_MODE = bool(RUNTIME_CONFIG.get("headless_mode", True))
USE_EXISTING_WINDOWS_ONLY = bool(RUNTIME_CONFIG.get("use_existing_windows_only", False))
TIMEZONE_FOLLOW_IP = bool(RUNTIME_CONFIG.get("timezone_follow_ip", True))
AUTO_CLOSE_AFTER_TASK = normalize_bool(
    RUNTIME_CONFIG.get("auto_close_after_task"),
    "auto_close_after_task",
    default=False,
)
WAIT_AFTER_OPEN_RANGE = normalize_range(RUNTIME_CONFIG.get("wait_after_open_range"), "wait_after_open_range")
WAIT_AFTER_CLICK_RANGE = normalize_range(
    RUNTIME_CONFIG.get("wait_after_click_range"), "wait_after_click_range"
)
PAGE_LOAD_TIMEOUT_MS = int(RUNTIME_CONFIG.get("page_load_timeout_ms", 45000))
PAGE_RELOAD_MAX_RETRIES = int(RUNTIME_CONFIG.get("page_reload_max_retries", 2))
PAGE_RELOAD_DELAY_RANGE = normalize_range(
    RUNTIME_CONFIG.get("page_reload_delay_range"), "page_reload_delay_range"
)
CYCLE_TARGET_DURATION_RANGE = normalize_range(
    RUNTIME_CONFIG.get("cycle_target_duration_range"), "cycle_target_duration_range"
)
CLICK_RATIO_X = float(RUNTIME_CONFIG.get("click_ratio_x", 0.3))
CLICK_RATIO_Y = float(RUNTIME_CONFIG.get("click_ratio_y", 0.4))
CLEAR_LOCAL_CACHE_BEFORE_OPEN = bool(RUNTIME_CONFIG.get("clear_local_cache_before_open", True))
CLEAR_SERVER_CACHE_BEFORE_OPEN = bool(RUNTIME_CONFIG.get("clear_server_cache_before_open", True))
PLAYWRIGHT_IN_SUBPROCESS = bool(RUNTIME_CONFIG.get("playwright_in_subprocess", True))
PLAYWRIGHT_ACTION_TIMEOUT_SEC = int(RUNTIME_CONFIG.get("playwright_action_timeout_sec", 120))
FATAL_BACKOFF_RANGE = normalize_range(RUNTIME_CONFIG.get("fatal_backoff_range"), "fatal_backoff_range")
IGNORE_KEYBOARD_INTERRUPT = bool(RUNTIME_CONFIG.get("ignore_keyboard_interrupt", True))


# 计算每个窗口每轮应处理的 URL 数量：
# - 配置 urls_per_window_per_round 时，固定使用该值（不超过 URL 总数）
# - 未配置时，保持历史策略（URL>=4 随机 3/4 个，否则全量）
def resolve_selected_url_count(url_total: int) -> int:
    if url_total <= 0:
        raise ValueError("url_total 必须大于 0")

    configured = URLS_PER_WINDOW_PER_ROUND
    if configured is not None:
        configured_int = int(configured)
        if configured_int <= 0:
            raise ValueError("urls_per_window_per_round 必须大于 0")
        return min(configured_int, url_total)

    if url_total >= 4:
        return random.randint(3, 4)
    return url_total


# 输出统一中文状态日志，便于观察任务进度。
def log_status(stage: str, message: str) -> None:
    now = time.strftime("%H:%M:%S")
    print(f"[{now}][{stage}] {message}")


class ConsoleProgressBoard:
    """按窗口实时刷新固定行进度，避免控制台刷屏。"""

    def __init__(
        self,
        window_names: list[str],
        total_by_slot: list[int],
        window_round_by_slot: list[int],
    ) -> None:
        self._window_names = window_names
        self._total_by_slot = total_by_slot
        self._window_round_by_slot = window_round_by_slot
        self._lock = threading.Lock()
        self._is_tty = sys.stdout.isatty()
        self._line_count = len(window_names)
        self._rendered = False
        self._lines: list[str] = []
        for slot_index, window_name in enumerate(window_names):
            total = self._safe_total(slot_index)
            self._lines.append(self._format_line(slot_index, window_name, 0, total, "待开始"))

    def _safe_total(self, slot_index: int) -> int:
        if 0 <= slot_index < len(self._total_by_slot):
            total = self._total_by_slot[slot_index]
            return total if total > 0 else 1
        return 1

    def _format_line(
        self, slot_index: int, window_name: str, current: int, total: int, status: str
    ) -> str:
        current_norm = max(0, min(current, total))
        window_round = (
            self._window_round_by_slot[slot_index]
            if 0 <= slot_index < len(self._window_round_by_slot)
            else 0
        )
        return (
            f"{slot_index + 1}. {window_name} "
            f"[窗轮{window_round}] "
            f"{current_norm}/{total} {status}"
        )

    # 估算字符在终端中的显示宽度，避免中文字符导致光标回退行数不准。
    def _display_width(self, text: str) -> int:
        width = 0
        for ch in text:
            width += 2 if unicodedata.east_asian_width(ch) in ("W", "F") else 1
        return width

    # 将文本裁剪到终端可视宽度内，防止自动换行产生重复残影。
    def _fit_terminal_width(self, text: str) -> str:
        cols = shutil.get_terminal_size(fallback=(120, 20)).columns
        max_cols = max(20, cols - 1)
        if self._display_width(text) <= max_cols:
            return text

        suffix = "..."
        suffix_width = self._display_width(suffix)
        if max_cols <= suffix_width:
            return suffix[:max_cols]

        keep_width = max_cols - suffix_width
        output_chars: list[str] = []
        used = 0
        for ch in text:
            ch_width = 2 if unicodedata.east_asian_width(ch) in ("W", "F") else 1
            if used + ch_width > keep_width:
                break
            output_chars.append(ch)
            used += ch_width
        return "".join(output_chars) + suffix

    def _render_locked(self) -> None:
        if not self._lines:
            return
        fitted_lines = [self._fit_terminal_width(line) for line in self._lines]
        if not self._is_tty:
            if not self._rendered:
                print("\n".join(fitted_lines), flush=True)
                self._rendered = True
            return
        if not self._rendered:
            print("\n".join(fitted_lines), flush=True)
            self._rendered = True
            return

        sys.stdout.write(f"\x1b[{self._line_count}F")
        for idx, line in enumerate(fitted_lines):
            sys.stdout.write("\r\x1b[2K")
            sys.stdout.write(line)
            if idx < self._line_count - 1:
                sys.stdout.write("\n")
        # 重绘后补一个换行，把光标稳定放到进度面板下方，避免下一次回退基准漂移。
        sys.stdout.write("\n")
        sys.stdout.flush()

    def update(self, slot_index: int, current: int, status: str) -> None:
        with self._lock:
            if slot_index < 0 or slot_index >= len(self._lines):
                return
            total = self._safe_total(slot_index)
            window_name = self._window_names[slot_index]
            self._lines[slot_index] = self._format_line(
                slot_index=slot_index,
                window_name=window_name,
                current=current,
                total=total,
                status=status,
            )
            self._render_locked()

    def begin_round(
        self,
        slot_index: int,
        total: int,
        window_round: int,
        status: str = "待开始",
    ) -> None:
        with self._lock:
            if slot_index < 0 or slot_index >= len(self._lines):
                return
            safe_total = total if total > 0 else 1
            self._total_by_slot[slot_index] = safe_total
            self._window_round_by_slot[slot_index] = window_round
            window_name = self._window_names[slot_index]
            self._lines[slot_index] = self._format_line(
                slot_index=slot_index,
                window_name=window_name,
                current=0,
                total=safe_total,
                status=status,
            )
            self._render_locked()


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


# 生成每个窗口要执行的任务列表：
# - 配置 urls_per_window_per_round 时：每个窗口每轮固定处理该数量
# - 未配置时：沿用历史策略（URL>=4 随机 3/4 个，否则全量）
def build_window_visit_tasks(
    target_urls: list[str], proxy_raws: list[str], window_count: int
) -> list[list[dict[str, Any]]]:
    if not target_urls:
        raise ValueError("TARGET_URLS 不能为空")
    if not proxy_raws:
        raise ValueError("PROXY_RAWS 不能为空")
    if window_count <= 0:
        raise ValueError("window_count 必须大于 0")

    url_total = len(target_urls)
    slot_tasks: list[list[dict[str, Any]]] = []
    all_url_indices = list(range(url_total))

    for slot_index in range(window_count):
        selected_count = resolve_selected_url_count(url_total)
        selected_indices = random.sample(all_url_indices, k=selected_count)
        random.shuffle(selected_indices)

        proxy_index = slot_index % len(proxy_raws)
        proxy_raw = proxy_raws[proxy_index]
        tasks_for_slot: list[dict[str, Any]] = []
        for url_index in selected_indices:
            tasks_for_slot.append(
                {
                    "slot_index": slot_index,
                    "url_index": url_index,
                    "proxy_index": proxy_index,
                    "url": target_urls[url_index],
                    "proxy_raw": proxy_raw,
                }
            )
        slot_tasks.append(tasks_for_slot)

    return slot_tasks


def build_slot_visit_tasks(
    target_urls: list[str],
    proxy_raws: list[str],
    slot_index: int,
) -> list[dict[str, Any]]:
    if not target_urls:
        raise ValueError("TARGET_URLS 不能为空")
    if not proxy_raws:
        raise ValueError("PROXY_RAWS 不能为空")
    if slot_index < 0:
        raise ValueError("slot_index 不能小于 0")

    url_total = len(target_urls)
    all_url_indices = list(range(url_total))
    selected_count = resolve_selected_url_count(url_total)
    selected_indices = random.sample(all_url_indices, k=selected_count)
    random.shuffle(selected_indices)

    proxy_index = slot_index % len(proxy_raws)
    proxy_raw = proxy_raws[proxy_index]
    tasks_for_slot: list[dict[str, Any]] = []
    for url_index in selected_indices:
        tasks_for_slot.append(
            {
                "slot_index": slot_index,
                "url_index": url_index,
                "proxy_index": proxy_index,
                "url": target_urls[url_index],
                "proxy_raw": proxy_raw,
            }
        )
    return tasks_for_slot


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


# 从接口 data 中尽量提取可用的 http 调试地址。
def extract_http_endpoint_from_data(data: Any) -> str | None:
    if isinstance(data, str):
        return normalize_http_endpoint(data)

    if isinstance(data, dict):
        preferred_keys = [
            "http",
            "debugHttp",
            "debug_http",
            "httpUrl",
            "http_url",
            "debugAddress",
            "debug_address",
        ]
        for key in preferred_keys:
            endpoint = normalize_http_endpoint(data.get(key))
            if endpoint:
                return endpoint

        for value in data.values():
            endpoint = extract_http_endpoint_from_data(value)
            if endpoint:
                return endpoint

    if isinstance(data, list):
        for item in data:
            endpoint = extract_http_endpoint_from_data(item)
            if endpoint:
                return endpoint

    return None


# 计算页面 URL 与目标 URL 的匹配分值，分值越高代表越可能是目标标签页。
def calculate_url_match_score(page_url: str, target_url: str) -> int:
    page = (page_url or "").strip()
    target = (target_url or "").strip()
    if not page or not target:
        return 0
    if page == target:
        return 4
    if target in page or page in target:
        return 3
    try:
        parsed_page = urlparse(page)
        parsed_target = urlparse(target)
    except Exception:
        return 0

    if parsed_page.netloc and parsed_page.netloc == parsed_target.netloc:
        if parsed_page.path and parsed_page.path == parsed_target.path:
            return 2
        return 1
    return 0


# 在当前上下文中选择最可能的目标标签页；同分时优先最新打开的标签页。
def select_best_page(context: Any, target_url: str, require_match: bool = False) -> Any | None:
    pages = list(getattr(context, "pages", []) or [])
    if not pages:
        return None

    best_page = None
    best_score = -1
    best_idx = -1
    for idx, page in enumerate(pages):
        score = calculate_url_match_score(getattr(page, "url", ""), target_url)
        # 同分时优先索引更大的标签页（通常是后打开的页）。
        if score > best_score or (score == best_score and idx > best_idx):
            best_score = score
            best_page = page
            best_idx = idx

    if require_match and best_score <= 0:
        return None
    if best_page is not None:
        return best_page
    return pages[-1]


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


# 在当前进程中导航到目标 URL 并等待页面加载完成。
def navigate_page_to_url_local(http_endpoint: str, target_url: str) -> bool:
    try:
        from playwright.sync_api import sync_playwright
    except Exception as exc:
        log_status("导航跳过", f"Playwright 不可用: {exc}")
        return False

    try:
        with sync_playwright() as pw:
            browser = pw.chromium.connect_over_cdp(http_endpoint)
            context = browser.contexts[0] if browser.contexts else browser.new_context()
            page = select_best_page(context, target_url, require_match=False)
            if page is None:
                page = context.new_page()

            max_attempts = PAGE_RELOAD_MAX_RETRIES + 1
            for attempt in range(max_attempts):
                attempt_no = attempt + 1
                try:
                    page.bring_to_front()
                    page.goto(target_url, wait_until="domcontentloaded", timeout=PAGE_LOAD_TIMEOUT_MS)
                    page.wait_for_load_state("load", timeout=PAGE_LOAD_TIMEOUT_MS)
                    return True
                except Exception as exc:
                    log_status("导航重试", f"第 {attempt_no}/{max_attempts} 次失败: {exc}")
                    if attempt_no >= max_attempts:
                        break
                    delay = random.uniform(*PAGE_RELOAD_DELAY_RANGE)
                    log_status("导航重试", f"重试前等待 {delay:.2f}s")
                    time.sleep(delay)
            return False
    except Exception as exc:
        log_status("导航失败", str(exc))
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
                page = select_best_page(context, target_url, require_match=True)
                if page:
                    break
                time.sleep(0.5)

            if page is None:
                page = select_best_page(context, target_url, require_match=False)
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
            page = select_best_page(context, target_url, require_match=False)
            if page is None:
                page = context.new_page()
                page.goto(target_url, wait_until="domcontentloaded", timeout=60000)

            page.bring_to_front()
            viewport = page.viewport_size or {"width": WINDOW_WIDTH, "height": WINDOW_HEIGHT}
            click_x = max(1, int(viewport["width"] * CLICK_RATIO_X))
            click_y = max(1, int(viewport["height"] * CLICK_RATIO_Y))
            page.mouse.click(click_x, click_y)

            # 这里不主动调用 browser.close()，避免误关闭真实浏览器窗口。
            # with sync_playwright() 退出时会回收控制连接。
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


# 在已打开窗口内导航到指定 URL（可选子进程隔离）。
def navigate_page_to_url(http_endpoint: str, target_url: str) -> bool:
    if PLAYWRIGHT_IN_SUBPROCESS:
        return run_playwright_action_in_subprocess("navigate_url", http_endpoint, target_url)
    return navigate_page_to_url_local(http_endpoint, target_url)


# 在区间内随机等待。
def sleep_random(wait_range: tuple[float, float], _label: str) -> float:
    start, end = wait_range
    if start < 0 or end < 0 or end < start:
        raise ValueError(f"等待区间配置错误: {wait_range}")
    duration = random.uniform(start, end)
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
    if action == "navigate_url":
        return 0 if navigate_page_to_url_local(http_endpoint, target_url) else 5
    log_status("子进程参数错误", f"未知动作: {action}")
    return 2


def run_one_cycle(client: RoxyClient) -> None:
    log_status("运行模式", "已启用窗口独立轮次模式：窗口完成后立即进入下一轮")
    log_status(
        "关窗策略",
        "每轮结束将主动关窗" if AUTO_CLOSE_AFTER_TASK else "每轮结束仅刷新指纹并保留窗口",
    )
    max_windows = max(1, len(PROXY_RAWS))
    if WINDOW_COUNT <= 0:
        raise ValueError("WINDOW_COUNT 必须大于 0")
    if WINDOW_COUNT > max_windows:
        raise ValueError(
            f"窗口数量超过可分配组合上限：WINDOW_COUNT={WINDOW_COUNT}, 上限={max_windows}"
        )
    effective_window_count = min(WINDOW_COUNT, max_windows)
    if effective_window_count < WINDOW_COUNT:
        log_status(
            "窗口提示",
            f"代理槽位数仅 {max_windows}，本轮最多使用 {effective_window_count} 个窗口槽位",
        )
    if not TARGET_URLS:
        raise ValueError("TARGET_URLS 不能为空")

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

    progress_board = ConsoleProgressBoard(
        window_names=[str(slot["window_name"]) for slot in slots],
        total_by_slot=[1 for _ in range(effective_window_count)],
        window_round_by_slot=[0 for _ in range(effective_window_count)],
    )

    # 独立窗口并发执行：每个槽位持续自循环，完成即进入下一轮，不等待其他窗口。
    shared_lock = threading.Lock()

    # 针对共享状态（窗口ID池/映射）加锁，避免并发读写冲突。
    def acquire_reusable_dir_id() -> str | None:
        with shared_lock:
            if reusable_existing_ids:
                return reusable_existing_ids.pop(0)
            return None

    def update_slot_dir_id(slot_ref: dict[str, Any], window_name_ref: str, dir_id_ref: str) -> None:
        with shared_lock:
            slot_ref["dir_id"] = dir_id_ref
            window_name_map[window_name_ref] = dir_id_ref

    def run_slot_tasks(slot_index: int) -> None:
        slot = slots[slot_index]
        window_name = slot["window_name"]
        window_round = 0
        while True:
            round_start_at = time.monotonic()
            window_round += 1
            tasks_for_slot = build_slot_visit_tasks(TARGET_URLS, PROXY_RAWS, slot_index)
            progress_board.begin_round(
                slot_index=slot_index,
                total=len(tasks_for_slot),
                window_round=window_round,
                status="本轮开始",
            )

            opened_this_round = False
            last_http_endpoint: str | None = None
            for task_order, task in enumerate(tasks_for_slot):
                dir_id: str | None = slot.get("dir_id")
                try:
                    proxy_info = build_proxy_info(task["proxy_raw"])
                    progress_board.update(slot_index, task_order + 1, "准备中")
                    just_opened_now = False

                    if not opened_this_round:
                        if dir_id:
                            # 仅在本轮首次任务更新窗口配置，后续 URL 走同窗导航。
                            client.browser_mdf(
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
                            progress_board.update(slot_index, task_order + 1, "更新窗口配置")
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
                                update_slot_dir_id(slot, window_name, dir_id)
                                progress_board.update(slot_index, task_order + 1, "创建窗口成功")
                            except RoxyAPIError as exc:
                                if exc.code != 409:
                                    raise
                                reusable_dir_id = acquire_reusable_dir_id()
                                if reusable_dir_id:
                                    dir_id = reusable_dir_id
                                    update_slot_dir_id(slot, window_name, dir_id)
                                    progress_board.update(slot_index, task_order + 1, "额度不足，已复用现有窗口")
                                else:
                                    raise ValueError("窗口额度不足，且没有可复用的现有窗口")

                    if not isinstance(dir_id, str) or not dir_id:
                        raise ValueError(f"[{window_name}] 无有效 dirId，无法继续执行")

                    # 自动按屏幕宽度平铺窗口位置与大小。
                    client.browser_auto_tile_window_layout(
                        workspace_id=workspace_id,
                        dir_id=dir_id,
                        slot_index=slot_index,
                        screen_width=screen_width,
                        width=WINDOW_WIDTH,
                        height=WINDOW_HEIGHT,
                        extra_payload={"fingerInfo": build_finger_info_base()},
                    )
                    progress_board.update(slot_index, task_order + 1, "调整窗口布局")

                    if not opened_this_round:
                        # 每个窗口每轮仅执行一次随机指纹，放在本轮首次任务开始前。
                        client.browser_random_env(
                            {
                                "workspaceId": workspace_id,
                                "dirId": dir_id,
                            }
                        )
                        progress_board.update(slot_index, task_order + 1, "刷新指纹")

                        if CLEAR_LOCAL_CACHE_BEFORE_OPEN:
                            client.browser_clear_local_cache({"dirIds": [dir_id]})
                            progress_board.update(slot_index, task_order + 1, "清理本地缓存")
                        if CLEAR_SERVER_CACHE_BEFORE_OPEN:
                            client.browser_clear_server_cache(
                                {"workspaceId": workspace_id, "dirIds": [dir_id]}
                            )
                            progress_board.update(slot_index, task_order + 1, "清理服务端缓存")

                        open_payload = {
                            "workspaceId": workspace_id,
                            "dirId": dir_id,
                            "args": build_open_args(),
                        }
                        open_resp = client.browser_open(open_payload)
                        progress_board.update(slot_index, task_order + 1, "窗口已打开")
                        open_data = open_resp.get("data", {}) if isinstance(open_resp, dict) else None
                        last_http_endpoint = extract_http_endpoint_from_data(open_data)
                        if not last_http_endpoint:
                            try:
                                conn_resp = client.browser_connection_info(
                                    {
                                        "workspaceId": workspace_id,
                                        "dirId": dir_id,
                                    }
                                )
                                conn_data = conn_resp.get("data", {}) if isinstance(conn_resp, dict) else None
                                last_http_endpoint = extract_http_endpoint_from_data(conn_data)
                            except Exception as conn_exc:
                                log_status("调试地址", f"{window_name} connection_info 获取失败: {conn_exc}")
                        if last_http_endpoint:
                            progress_board.update(slot_index, task_order + 1, "调试地址就绪")
                        else:
                            progress_board.update(slot_index, task_order + 1, "调试地址缺失")
                        opened_this_round = True
                        just_opened_now = True

                    loaded = False
                    if last_http_endpoint:
                        if just_opened_now:
                            progress_board.update(slot_index, task_order + 1, "等待首个页面加载")
                            loaded = wait_page_loaded(
                                http_endpoint=last_http_endpoint,
                                target_url=task["url"],
                            )
                            if not loaded:
                                progress_board.update(slot_index, task_order + 1, "首个加载失败，尝试同窗导航")
                                loaded = navigate_page_to_url(
                                    http_endpoint=last_http_endpoint,
                                    target_url=task["url"],
                                )
                        else:
                            progress_board.update(slot_index, task_order + 1, "同窗导航并等待加载")
                            loaded = navigate_page_to_url(
                                http_endpoint=last_http_endpoint,
                                target_url=task["url"],
                            )
                    else:
                        progress_board.update(slot_index, task_order + 1, "缺少调试地址，加载失败")

                    if loaded:
                        progress_board.update(slot_index, task_order + 1, "页面已加载")
                        sleep_random(WAIT_AFTER_OPEN_RANGE, f"[{window_name}] wait_after_open")
                        progress_board.update(slot_index, task_order + 1, "执行点击")
                        clicked = click_page_once(http_endpoint=last_http_endpoint, target_url=task["url"])
                        progress_board.update(
                            slot_index,
                            task_order + 1,
                            "点击完成" if clicked else "点击失败",
                        )
                        sleep_random(WAIT_AFTER_CLICK_RANGE, f"[{window_name}] wait_after_click")
                    else:
                        progress_board.update(slot_index, task_order + 1, "页面未确认加载，跳过点击")
                except Exception as exc:
                    progress_board.update(slot_index, task_order + 1, f"失败: {type(exc).__name__}")
                    log_status("任务失败", f"{window_name} 执行失败，已跳过: {exc}")

            if AUTO_CLOSE_AFTER_TASK:
                final_dir_id = slot.get("dir_id")
                if isinstance(final_dir_id, str) and final_dir_id:
                    try:
                        client.browser_close(
                            {
                                "workspaceId": workspace_id,
                                "dirId": final_dir_id,
                            }
                        )
                        progress_board.update(slot_index, len(tasks_for_slot), "本轮完成，已关闭")
                    except Exception as exc:
                        progress_board.update(slot_index, len(tasks_for_slot), "本轮完成，关窗失败")
                        log_status("关窗失败", f"{window_name} 本轮结束关闭失败: {exc}")
                else:
                    progress_board.update(slot_index, len(tasks_for_slot), "本轮完成，无可关闭窗口")
            else:
                final_dir_id = slot.get("dir_id")
                if isinstance(final_dir_id, str) and final_dir_id:
                    try:
                        client.browser_random_env(
                            {
                                "workspaceId": workspace_id,
                                "dirId": final_dir_id,
                            }
                        )
                        progress_board.update(slot_index, len(tasks_for_slot), "本轮完成，已刷新指纹")
                    except Exception as exc:
                        progress_board.update(slot_index, len(tasks_for_slot), "本轮完成，刷新指纹失败")
                        log_status("刷新指纹失败", f"{window_name} 本轮结束刷新指纹失败: {exc}")
                else:
                    progress_board.update(slot_index, len(tasks_for_slot), "本轮完成，窗口保留")

            # 窗口独立轮次：本窗口完成即进入下一轮，不等待其他窗口。
            round_elapsed = time.monotonic() - round_start_at
            target_round_duration = random.uniform(*CYCLE_TARGET_DURATION_RANGE)
            if round_elapsed < target_round_duration:
                wait_duration = target_round_duration - round_elapsed
                progress_board.update(
                    slot_index,
                    len(tasks_for_slot),
                    f"本轮完成，节奏等待 {wait_duration:.1f}s",
                )
                time.sleep(wait_duration)
                round_elapsed = time.monotonic() - round_start_at

            log_status(
                "窗口轮次",
                f"{window_name} 第 {window_round} 轮完成，用时 {round_elapsed:.2f}s，目标 {target_round_duration:.2f}s",
            )

    workers: list[threading.Thread] = []
    for slot_index in range(effective_window_count):
        worker = threading.Thread(target=run_slot_tasks, args=(slot_index,), daemon=False)
        worker.start()
        workers.append(worker)

    for worker in workers:
        worker.join()


def main() -> None:
    token_arg, worker_action, worker_http, worker_url = parse_cli_args(sys.argv)
    if worker_action:
        exit_code = run_worker_action(worker_action, worker_http or "", worker_url or "")
        raise SystemExit(exit_code)

    runtime_token = token_arg or TOKEN
    token_source = "命令行参数" if token_arg else "默认配置"
    log_status("启动配置", f"token 来源: {token_source}")
    client = RoxyClient(token=runtime_token, port=PORT, timeout=120)
    try:
        run_one_cycle(client)
    except KeyboardInterrupt:
        if IGNORE_KEYBOARD_INTERRUPT:
            log_status("中断提示", "收到 Ctrl+C，当前模式不重启线程，已退出")
        raise
    except Exception as exc:
        log_status("运行失败", f"窗口独立轮次模式异常: {exc}")
        backoff = random.uniform(*FATAL_BACKOFF_RANGE)
        log_status("异常退避", f"等待 {backoff:.2f}s 后退出")
        time.sleep(backoff)
    finally:
        client.close()


if __name__ == "__main__":
    main()
