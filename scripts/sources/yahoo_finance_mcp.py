"""Yahoo Finance MCP connector for Reach.

Invokes yahoo-finance-mcp via stdio JSON-RPC to get comprehensive financial data
from Yahoo Finance. No API key required.

MCP server: yahoo-finance-mcp (GitHub)
Install:   uvx --from git+https://github.com/Alex2Yang97/yahoo-finance-mcp yahoo-finance-mcp
"""
from __future__ import annotations

import json
import subprocess
import threading
from typing import Any, Dict, Optional


class _MCPClient:
    """Minimal stdio JSON-RPC client for MCP servers."""

    def __init__(self, cmd: list[str], env: Optional[dict] = None):
        self._proc: Optional[subprocess.Popen] = None
        self._cmd = cmd
        self._env = env
        self._lock = threading.Lock()
        self._id_counter = 0

    def start(self):
        import os
        env = os.environ.copy()
        if self._env:
            env.update(self._env)
        self._proc = subprocess.Popen(
            self._cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
            text=True,
            bufsize=1,
        )
        self._initialize()

    def _initialize(self):
        req = {
            "jsonrpc": "2.0",
            "id": self._next_id(),
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "ocas-reach", "version": "3.4.0"},
            },
        }
        resp = self._send(req)
        if "error" in resp:
            raise RuntimeError(f"MCP init failed: {resp['error']}")
        self._send_notification("notifications/initialized")

    def call_tool(self, tool_name: str, arguments: dict) -> dict:
        self._ensure_running()
        req = {
            "jsonrpc": "2.0",
            "id": self._next_id(),
            "method": "tools/call",
            "params": {"name": "tools/call", "arguments": {"name": tool_name, "arguments": arguments}},
        }
        resp = self._send(req)
        if "error" in resp:
            return {"error": resp["error"].get("message", str(resp["error"])), "raw": resp["error"]}
        result = resp.get("result", {})
        content = result.get("content", [])
        if not content:
            return result
        texts = []
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                texts.append(block.get("text", ""))
        combined = "\n".join(texts).strip()
        if combined.startswith("{") or combined.startswith("["):
            try:
                return json.loads(combined)
            except json.JSONDecodeError:
                pass
        return {"text": combined}

    def _send(self, req: dict) -> dict:
        self._ensure_running()
        assert self._proc is not None
        payload = json.dumps(req) + "\n"
        self._proc.stdin.write(payload)  # type: ignore[union-attr]
        self._proc.stdin.flush()  # type: ignore[union-attr]
        line = self._proc.stdout.readline()  # type: ignore[union-attr]
        if not line:
            raise RuntimeError("MCP server closed stdout")
        return json.loads(line)

    def _send_notification(self, method: str, params: dict = None):
        self._ensure_running()
        assert self._proc is not None
        req: dict[str, Any] = {"jsonrpc": "2.0", "method": method}
        if params:
            req["params"] = params
        payload = json.dumps(req) + "\n"
        self._proc.stdin.write(payload)  # type: ignore[union-attr]
        self._proc.stdin.flush()  # type: ignore[union-attr]

    def _next_id(self) -> int:
        self._id_counter += 1
        return self._id_counter

    def _ensure_running(self):
        if self._proc is None:
            self.start()
        elif self._proc.poll() is not None:
            raise RuntimeError("MCP server process has exited")

    def close(self):
        proc = self._proc
        self._proc = None
        if proc is not None and proc.poll() is None:
            try:
                proc.stdin.close()  # type: ignore[union-attr]
            except Exception:
                pass
            proc.wait(timeout=5)


# ── Module-level client cache ──────────────────────────────────────────────
_client: Optional[_MCPClient] = None


def _get_client(auth: dict) -> _MCPClient:
    global _client
    if _client is None or _client._proc is None or _client._proc.poll() is not None:
        _client = _MCPClient([
            "uvx", "--from",
            "git+https://github.com/Alex2Yang97/yahoo-finance-mcp",
            "yahoo-finance-mcp"
        ])
        _client.start()
    return _client


def _close_client():
    global _client
    if _client:
        _client.close()
        _client = None


# ── Reach query interface ──────────────────────────────────────────────────

def query(action: str, params: dict, auth: dict) -> dict:
    """
    Reach-facing query entry point.

    Actions:
      historical_prices — Get OHLCV data. Params: symbol, period, interval
      stock_info        — Get comprehensive metrics. Params: symbol
      news              — Get news. Params: symbol, count
      financial_statement — Get financials. Params: symbol, statement_type, period
      holder_info       — Get holder data. Params: symbol, holder_type
      recommendations   — Get analyst recs. Params: symbol
      options_chain     — Get options. Params: symbol, expiration, option_type
      stock_actions     — Get dividends/splits. Params: symbol
    """
    client = _get_client(auth)

    try:
        symbol = params.get("symbol", "").upper()
        if not symbol and action != "recommendations":
            return {"error": f"{action} requires 'symbol'"}

        action_map = {
            "historical_prices": ("get_historical_stock_prices", _args_historical),
            "stock_info": ("get_stock_info", _args_symbol),
            "news": ("get_yahoo_finance_news", _args_news),
            "financial_statement": ("get_financial_statement", _args_financial),
            "holder_info": ("get_holder_info", _args_holder),
            "recommendations": ("get_recommendations", _args_symbol),
            "options_chain": ("get_option_chain", _args_options),
            "stock_actions": ("get_stock_actions", _args_symbol),
        }

        entry = action_map.get(action)
        if entry is None:
            return {"error": f"Unknown action: {action}", "valid_actions": list(action_map.keys())}

        tool_name, args_fn = entry
        args = args_fn(symbol, params)
        if isinstance(args, dict) and "error" in args:
            return args

        return client.call_tool(tool_name, args)
    except Exception as e:
        _close_client()
        return {"error": str(e), "action": action}


def _args_symbol(symbol: str, params: dict) -> dict:
    return {"symbol": symbol}


def _args_historical(symbol: str, params: dict) -> dict:
    args = {"symbol": symbol}
    if params.get("period"):
        args["period"] = params["period"]
    if params.get("interval"):
        args["interval"] = params["interval"]
    return args


def _args_news(symbol: str, params: dict) -> dict:
    args = {"symbol": symbol}
    if params.get("count"):
        args["count"] = int(params["count"])
    return args


def _args_financial(symbol: str, params: dict) -> dict:
    args = {"symbol": symbol}
    if params.get("statement_type"):
        args["statement_type"] = params["statement_type"]
    if params.get("period"):
        args["period"] = params["period"]
    return args


def _args_holder(symbol: str, params: dict) -> dict:
    args = {"symbol": symbol}
    if params.get("holder_type"):
        args["holder_type"] = params["holder_type"]
    return args


def _args_options(symbol: str, params: dict) -> dict:
    args = {"symbol": symbol}
    if params.get("expiration"):
        args["expiration"] = params["expiration"]
    if params.get("option_type"):
        args["option_type"] = params["option_type"]
    return args
