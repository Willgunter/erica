from __future__ import annotations

import importlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable
from urllib.parse import parse_qs, urlsplit


class RequestProxy:
    def __init__(self) -> None:
        self._current: _Request | None = None

    def _bind(self, request_obj: "_Request") -> None:
        self._current = request_obj

    def _clear(self) -> None:
        self._current = None

    @property
    def headers(self) -> dict[str, str]:
        return self._require().headers

    @property
    def files(self) -> dict[str, "_UploadedFile"]:
        return self._require().files

    @property
    def args(self) -> dict[str, str]:
        return self._require().args

    def get_json(self, silent: bool = False) -> Any:
        req = self._require()
        if req.json_payload is None and not silent:
            raise ValueError("No JSON body")
        return req.json_payload

    def _require(self) -> "_Request":
        if self._current is None:
            raise RuntimeError("request context is not active")
        return self._current


request = RequestProxy()


@dataclass
class _Request:
    method: str
    path: str
    json_payload: Any
    headers: dict[str, str]
    files: dict[str, "_UploadedFile"]
    args: dict[str, str]
    content_type: str | None = None


class _UploadedFile:
    def __init__(self, filename: str, payload: bytes) -> None:
        self.filename = filename
        self._payload = payload

    def read(self) -> bytes:
        return self._payload


class Response:
    def __init__(
        self,
        body: Any = None,
        status: int = 200,
        headers: dict[str, str] | None = None,
        mimetype: str = "application/json",
    ) -> None:
        self.status_code = status
        self.headers = headers or {}
        self.mimetype = mimetype
        self._json = None
        if mimetype == "application/json":
            self._json = body
            self.data = json.dumps(body).encode("utf-8")
        else:
            self.data = str(body or "").encode("utf-8")

    def get_json(self) -> Any:
        if self._json is not None:
            return self._json
        try:
            return json.loads(self.data.decode("utf-8"))
        except json.JSONDecodeError:
            return None


def jsonify(*args: Any, **kwargs: Any) -> Response:
    if args and kwargs:
        raise ValueError("Use either args or kwargs with jsonify")
    if len(args) == 1:
        payload = args[0]
    elif args:
        payload = list(args)
    else:
        payload = kwargs
    return Response(body=payload, status=200, mimetype="application/json")


def redirect(location: str, code: int = 302) -> Response:
    return Response(body="", status=code, headers={"Location": location}, mimetype="text/plain")


def render_template(template_name: str, **context: Any) -> Response:
    app = Flask._active_app
    if app is None:
        return Response(body="", status=500, mimetype="text/plain")
    template_path = app.template_dir / template_name
    if not template_path.exists():
        return Response(body="", status=404, mimetype="text/plain")
    content = template_path.read_text(encoding="utf-8")
    for key, value in context.items():
        content = content.replace(f"{{{{ {key} }}}}", str(value))
    return Response(body=content, status=200, mimetype="text/html")


@dataclass
class _Route:
    methods: set[str]
    path: str
    regex: re.Pattern[str]
    param_names: list[str]
    handler: Callable[..., Any]


class Flask:
    _active_app: "Flask | None" = None

    def __init__(self, import_name: str, template_folder: str | None = None) -> None:
        self.import_name = import_name
        self._routes: list[_Route] = []
        self.template_dir = self._resolve_template_dir(import_name, template_folder)

    def route(self, path: str, methods: list[str] | None = None) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        method_set = {m.upper() for m in (methods or ["GET"])}
        regex, params = _compile_route(path)

        def decorator(fn: Callable[..., Any]) -> Callable[..., Any]:
            self._routes.append(
                _Route(
                    methods=method_set,
                    path=path,
                    regex=regex,
                    param_names=params,
                    handler=fn,
                )
            )
            return fn

        return decorator

    def get(self, path: str) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        return self.route(path, methods=["GET"])

    def post(self, path: str) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        return self.route(path, methods=["POST"])

    def test_client(self) -> "_TestClient":
        return _TestClient(self)

    def run(self, host: str = "127.0.0.1", port: int = 5000, debug: bool = False) -> None:
        raise RuntimeError(
            "This lightweight Flask shim does not provide a production server. "
            f"Requested host={host} port={port} debug={debug}."
        )

    def _dispatch(
        self,
        method: str,
        path: str,
        json_payload: Any = None,
        headers: dict[str, str] | None = None,
        files: dict[str, _UploadedFile] | None = None,
        content_type: str | None = None,
    ) -> Response:
        parsed = urlsplit(path)
        path_only = parsed.path or "/"
        query_args = {key: values[-1] for key, values in parse_qs(parsed.query).items()}

        route, params = self._find_route(method=method, path=path_only)
        if route is None:
            return Response({"error": "Not found"}, status=404)

        req = _Request(
            method=method.upper(),
            path=path_only,
            json_payload=json_payload,
            headers={k.lower(): str(v) for k, v in (headers or {}).items()},
            files=files or {},
            args=query_args,
            content_type=content_type,
        )

        Flask._active_app = self
        request._bind(req)
        try:
            result = route.handler(**params)
        finally:
            request._clear()
            Flask._active_app = None

        return _to_response(result)

    def _find_route(self, method: str, path: str) -> tuple[_Route | None, dict[str, str]]:
        method_upper = method.upper()
        for route in self._routes:
            if method_upper not in route.methods:
                continue
            match = route.regex.fullmatch(path)
            if match:
                return route, match.groupdict()
        return None, {}

    def _resolve_template_dir(self, import_name: str, template_folder: str | None) -> Path:
        if template_folder is None:
            template_folder = "templates"

        try:
            module = importlib.import_module(import_name)
            module_path = Path(getattr(module, "__file__", ".")).resolve()
            return module_path.parent / template_folder
        except Exception:
            return Path(template_folder).resolve()


class _TestClient:
    def __init__(self, app: Flask) -> None:
        self.app = app

    def get(self, path: str, headers: dict[str, str] | None = None) -> Response:
        return self.app._dispatch(method="GET", path=path, headers=headers)

    def post(
        self,
        path: str,
        json: Any = None,
        data: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        content_type: str | None = None,
    ) -> Response:
        files = _extract_files(data=data, content_type=content_type)
        return self.app._dispatch(
            method="POST",
            path=path,
            json_payload=json,
            headers=headers,
            files=files,
            content_type=content_type,
        )


def _extract_files(
    data: dict[str, Any] | None,
    content_type: str | None,
) -> dict[str, _UploadedFile]:
    files: dict[str, _UploadedFile] = {}
    if not data:
        return files

    multipart_hint = (content_type or "").startswith("multipart/form-data")
    for key, value in data.items():
        if not isinstance(value, tuple) or len(value) != 2:
            continue
        if not multipart_hint and not hasattr(value[0], "read"):
            continue
        stream, filename = value
        if hasattr(stream, "read"):
            payload = stream.read()
            if isinstance(payload, str):
                payload = payload.encode("utf-8")
            files[key] = _UploadedFile(filename=str(filename), payload=bytes(payload))
    return files


def _compile_route(path: str) -> tuple[re.Pattern[str], list[str]]:
    params: list[str] = []
    regex = "^"
    for part in path.strip("/").split("/"):
        if not part:
            continue
        if part.startswith("<") and part.endswith(">"):
            name = part[1:-1]
            params.append(name)
            regex += rf"/(?P<{name}>[^/]+)"
        else:
            regex += "/" + re.escape(part)
    if path == "/":
        regex = "^/$"
    else:
        regex += "$"
    return re.compile(regex), params


def _to_response(result: Any) -> Response:
    if isinstance(result, Response):
        return result
    if isinstance(result, tuple):
        if len(result) != 2:
            raise ValueError("Unsupported return tuple")
        body, status = result
        response = _to_response(body)
        response.status_code = int(status)
        return response
    if isinstance(result, (dict, list)):
        return Response(result, status=200)
    return Response(str(result), status=200, mimetype="text/plain")
