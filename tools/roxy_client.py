"""Roxy Browser 本地 API 客户端封装。"""

from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


class RoxyClientError(Exception):
    """Roxy 客户端基础异常。"""


@dataclass(slots=True)
class RoxyHTTPError(RoxyClientError):
    """HTTP 请求失败异常。"""

    status_code: int
    message: str
    response_text: str = ""

    # 返回便于排查的 HTTP 异常描述。
    def __str__(self) -> str:
        return f"HTTP {self.status_code}: {self.message}"


@dataclass(slots=True)
class RoxyAPIError(RoxyClientError):
    """业务接口返回失败异常。"""

    code: int
    message: str
    payload: Any = None

    # 返回便于排查的业务异常描述。
    def __str__(self) -> str:
        return f"API code={self.code}, message={self.message}"


class RoxyClient:
    """Roxy Browser API 客户端。"""

    # 初始化客户端配置，包括本地服务地址、鉴权 token 和超时策略。
    def __init__(
        self,
        token: str,
        port: int = 50000,
        host: str = "127.0.0.1",
        timeout: float = 30.0,
        raise_for_api_error: bool = True,
    ) -> None:
        self.host = host
        self.port = port
        self.token = token
        self.timeout = timeout
        self.raise_for_api_error = raise_for_api_error
        self.base_url = f"http://{self.host}:{self.port}"

    # 关闭客户端资源，当前为短连接实现，仅保留统一调用入口。
    def close(self) -> None:
        # 当前实现使用标准库短连接，无需额外释放资源。
        return None

    # 支持 with 语法进入上下文时返回客户端实例。
    def __enter__(self) -> "RoxyClient":
        return self

    # 支持 with 语法退出上下文时自动执行关闭逻辑。
    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.close()

    # 构建统一请求头，包含 JSON 类型和 token 鉴权信息。
    def _build_headers(self) -> dict[str, str]:
        return {
            "Content-Type": "application/json",
            "token": self.token,
        }

    # 发送底层 HTTP 请求并统一处理编码、异常和业务返回码。
    def _request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        url = f"{self.base_url}{path}"
        if params:
            url = f"{url}?{urlencode(params, doseq=True)}"

        body: bytes | None = None
        if data is not None:
            body = json.dumps(data, ensure_ascii=False).encode("utf-8")

        request = Request(
            url=url,
            data=body,
            headers=self._build_headers(),
            method=method,
        )

        try:
            with urlopen(request, timeout=self.timeout) as response:
                status_code = response.status
                response_text = response.read().decode("utf-8", errors="replace")
        except HTTPError as exc:
            response_text = exc.read().decode("utf-8", errors="replace")
            raise RoxyHTTPError(
                status_code=exc.code,
                message="HTTP 请求失败",
                response_text=response_text,
            ) from exc
        except URLError as exc:
            raise RoxyClientError(f"请求失败: {exc}") from exc
        except TimeoutError as exc:
            raise RoxyClientError(f"请求失败: {exc}") from exc

        if status_code < 200 or status_code >= 300:
            raise RoxyHTTPError(
                status_code=status_code,
                message="HTTP 请求失败",
                response_text=response_text,
            )

        try:
            payload = json.loads(response_text)
        except json.JSONDecodeError as exc:
            raise RoxyClientError(f"响应不是合法 JSON: {response_text}") from exc

        if not isinstance(payload, dict):
            raise RoxyClientError(f"响应结构不是对象: {payload!r}")

        code = payload.get("code")
        msg = payload.get("msg", "")
        if self.raise_for_api_error and isinstance(code, int) and code != 0:
            raise RoxyAPIError(code=code, message=str(msg), payload=payload)

        return payload

    # 统一发送 GET 请求。
    def _get(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        return self._request("GET", path, params=params)

    # 统一发送 POST 请求。
    def _post(self, path: str, data: dict[str, Any] | None = None) -> dict[str, Any]:
        return self._request("POST", path, data=data)

    # 健康检查
    # 检查 Roxy 本地服务是否可用，对应 GET /health。
    def health(self) -> dict[str, Any]:
        return self._get("/health")

    # 空间项目接口
    # 获取空间和项目列表，对应 GET /browser/workspace。
    def browser_workspace(self, params: dict[str, Any] | None = None) -> dict[str, Any]:
        return self._get("/browser/workspace", params=params)

    # 获取账号库列表，对应 GET /browser/account。
    def browser_account(self, params: dict[str, Any] | None = None) -> dict[str, Any]:
        return self._get("/browser/account", params=params)

    # 获取标签列表，对应 GET /browser/label。
    def browser_label(self, params: dict[str, Any] | None = None) -> dict[str, Any]:
        return self._get("/browser/label", params=params)

    # 浏览器窗口接口
    # 获取浏览器窗口列表，对应 GET /browser/list_v3。
    def browser_list_v3(self, params: dict[str, Any] | None = None) -> dict[str, Any]:
        return self._get("/browser/list_v3", params=params)

    # 获取浏览器窗口详情，对应 GET /browser/detail。
    def browser_detail(self, params: dict[str, Any] | None = None) -> dict[str, Any]:
        return self._get("/browser/detail", params=params)

    # 创建浏览器窗口，对应 POST /browser/create。
    def browser_create(self, data: dict[str, Any]) -> dict[str, Any]:
        return self._post("/browser/create", data=data)

    # 修改浏览器窗口配置，对应 POST /browser/mdf。
    def browser_mdf(self, data: dict[str, Any]) -> dict[str, Any]:
        return self._post("/browser/mdf", data=data)

    # 按指定尺寸和比例坐标修改窗口布局，并写入窗口配置。
    def browser_set_window_layout(
        self,
        workspace_id: int,
        dir_id: str,
        *,
        width: int = 1000,
        height: int = 1000,
        position_x: float = 0.0,
        position_y: float = 0.0,
        position_switch: bool = True,
        extra_payload: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        payload: dict[str, Any] = dict(extra_payload or {})
        payload["workspaceId"] = workspace_id
        payload["dirId"] = dir_id

        # 保留外部传入的 fingerInfo 其他字段，只覆盖窗口布局相关项。
        finger_info_raw = payload.get("fingerInfo", {})
        finger_info = dict(finger_info_raw) if isinstance(finger_info_raw, dict) else {}
        finger_info.update(
            {
                "openWidth": str(width),
                "openHeight": str(height),
                "positionSwitch": position_switch,
                "windowRatioPosition": f"{position_x:.6g},{position_y:.6g}",
            }
        )
        payload["fingerInfo"] = finger_info
        return self.browser_mdf(payload)

    # 按网格索引自动计算平铺坐标并修改窗口布局。
    def browser_tile_window_layout(
        self,
        workspace_id: int,
        dir_id: str,
        *,
        slot_index: int,
        columns: int = 2,
        rows: int = 2,
        width: int = 1000,
        height: int = 1000,
        start_x: float = 0.0,
        start_y: float = 0.0,
        extra_payload: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        if columns <= 0 or rows <= 0:
            raise ValueError("平铺参数错误，columns 和 rows 必须大于 0")
        if slot_index < 0 or slot_index >= columns * rows:
            raise ValueError("平铺参数错误，slot_index 超出网格范围")

        col_idx = slot_index % columns
        row_idx = slot_index // columns
        x_step = 1.0 / columns
        y_step = 1.0 / rows
        position_x = start_x + col_idx * x_step
        position_y = start_y + row_idx * y_step

        return self.browser_set_window_layout(
            workspace_id=workspace_id,
            dir_id=dir_id,
            width=width,
            height=height,
            position_x=position_x,
            position_y=position_y,
            position_switch=True,
            extra_payload=extra_payload,
        )

    # 根据屏幕宽度自动计算列数并进行平铺布局。
    def browser_auto_tile_window_layout(
        self,
        workspace_id: int,
        dir_id: str,
        *,
        slot_index: int,
        screen_width: int,
        width: int = 1000,
        height: int = 1000,
        start_x: float = 0.0,
        start_y: float = 0.0,
        extra_payload: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        if screen_width <= 0:
            raise ValueError("自动平铺参数错误，screen_width 必须大于 0")
        if width <= 0 or height <= 0:
            raise ValueError("自动平铺参数错误，width 和 height 必须大于 0")

        # 至少一列，并按屏幕宽度自动容纳窗口数量。
        columns = max(1, screen_width // width)
        return self.browser_tile_window_layout(
            workspace_id=workspace_id,
            dir_id=dir_id,
            slot_index=slot_index,
            columns=columns,
            rows=max(1, slot_index // columns + 1),
            width=width,
            height=height,
            start_x=start_x,
            start_y=start_y,
            extra_payload=extra_payload,
        )

    # 删除浏览器窗口，对应 POST /browser/delete。
    def browser_delete(self, data: dict[str, Any]) -> dict[str, Any]:
        return self._post("/browser/delete", data=data)

    # 打开浏览器窗口，对应 POST /browser/open。
    def browser_open(self, data: dict[str, Any]) -> dict[str, Any]:
        return self._post("/browser/open", data=data)

    # 关闭浏览器窗口，对应 POST /browser/close。
    def browser_close(self, data: dict[str, Any]) -> dict[str, Any]:
        return self._post("/browser/close", data=data)

    # 获取浏览器连接信息（调试地址等），对应 GET /browser/connection_info。
    def browser_connection_info(self, params: dict[str, Any] | None = None) -> dict[str, Any]:
        return self._get("/browser/connection_info", params=params)

    # 清理本地缓存，对应 POST /browser/clear_local_cache。
    def browser_clear_local_cache(self, data: dict[str, Any]) -> dict[str, Any]:
        return self._post("/browser/clear_local_cache", data=data)

    # 清理云端缓存，对应 POST /browser/clear_server_cache。
    def browser_clear_server_cache(self, data: dict[str, Any]) -> dict[str, Any]:
        return self._post("/browser/clear_server_cache", data=data)

    # 随机生成或刷新环境参数，对应 POST /browser/random_env。
    def browser_random_env(self, data: dict[str, Any]) -> dict[str, Any]:
        return self._post("/browser/random_env", data=data)

    # 账号接口
    # 获取平台账号列表，对应 GET /account/list。
    def account_list(self, params: dict[str, Any] | None = None) -> dict[str, Any]:
        return self._get("/account/list", params=params)

    # 新增平台账号，对应 POST /account/create。
    def account_create(self, data: dict[str, Any]) -> dict[str, Any]:
        return self._post("/account/create", data=data)

    # 批量新增平台账号，对应 POST /account/batch_create。
    def account_batch_create(self, data: dict[str, Any]) -> dict[str, Any]:
        return self._post("/account/batch_create", data=data)

    # 修改平台账号信息，对应 POST /account/modify。
    def account_modify(self, data: dict[str, Any]) -> dict[str, Any]:
        return self._post("/account/modify", data=data)

    # 删除平台账号，对应 POST /account/delete。
    def account_delete(self, data: dict[str, Any]) -> dict[str, Any]:
        return self._post("/account/delete", data=data)

    # 代理接口
    # 获取代理列表，对应 GET /proxy/list。
    def proxy_list(self, params: dict[str, Any] | None = None) -> dict[str, Any]:
        return self._get("/proxy/list", params=params)

    # 获取已购买代理列表，对应 GET /proxy/bought_list。
    def proxy_bought_list(self, params: dict[str, Any] | None = None) -> dict[str, Any]:
        return self._get("/proxy/bought_list", params=params)

    # 新增代理配置，对应 POST /proxy/create。
    def proxy_create(self, data: dict[str, Any]) -> dict[str, Any]:
        return self._post("/proxy/create", data=data)

    # 批量新增代理配置，对应 POST /proxy/batch_create。
    def proxy_batch_create(self, data: dict[str, Any]) -> dict[str, Any]:
        return self._post("/proxy/batch_create", data=data)

    # 修改代理配置，对应 POST /proxy/modify。
    def proxy_modify(self, data: dict[str, Any]) -> dict[str, Any]:
        return self._post("/proxy/modify", data=data)

    # 删除代理配置，对应 POST /proxy/delete。
    def proxy_delete(self, data: dict[str, Any]) -> dict[str, Any]:
        return self._post("/proxy/delete", data=data)

    # 触发代理连通性检测，对应 POST /proxy/detect。
    def proxy_detect(self, data: dict[str, Any]) -> dict[str, Any]:
        return self._post("/proxy/detect", data=data)

    # 获取可用的代理检测渠道，对应 GET /proxy/detect_channel。
    def proxy_detect_channel(self, params: dict[str, Any] | None = None) -> dict[str, Any]:
        return self._get("/proxy/detect_channel", params=params)
