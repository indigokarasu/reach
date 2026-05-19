"""Paper Search MCP connector for Reach.

Invokes paper-search-mcp (pip package) via stdio JSON-RPC to search and download
academic papers from 20+ sources (arXiv, PubMed, bioRxiv, Semantic Scholar, etc.).

MCP server: paper-search-mcp (pip/PyPI)
Install:   pip install paper-search-mcp
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
            "params": {"name": tool_name, "arguments": arguments},
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
        env = {}
        for key in ("PAPER_SEARCH_MCP_SEMANTIC_SCHOLAR_KEY", "PAPER_SEARCH_MCP_CORE_KEY",
                     "PAPER_SEARCH_MCP_UNPAYWALL_EMAIL", "PAPER_SEARCH_MCP_GOOGLE_SCHOLAR_PROXY_URL"):
            val = auth.get(key) or auth.get(key.lower())
            if val:
                env[key] = val
        _client = _MCPClient(["python3", "-m", "paper_search_mcp.server"], env=env if env else None)
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
      search       — Search arXiv (default multi-source entry point). Params: query, limit
      arxiv        — Search arXiv specifically. Params: query, limit
      pubmed       — Search PubMed. Params: query, limit
      biorxiv      — Search bioRxiv. Params: query, limit
      medrxiv      — Search medRxiv. Params: query, limit
      google_scholar — Search Google Scholar. Params: query, limit
      download     — Download a paper PDF. Params: paper_id, source
    """
    client = _get_client(auth)

    try:
        if action == "search" or action == "arxiv":
            return _action_search_source(client, "search_arxiv", params)
        elif action == "pubmed":
            return _action_search_source(client, "search_pubmed", params)
        elif action == "biorxiv":
            return _action_search_source(client, "search_biorxiv", params)
        elif action == "medrxiv":
            return _action_search_source(client, "search_medrxiv", params)
        elif action == "google_scholar":
            return _action_search_source(client, "search_google_scholar", params)
        elif action == "download":
            return _action_download(client, params)
        else:
            return {"error": f"Unknown action: {action}",
                    "valid_actions": ["search", "arxiv", "pubmed", "biorxiv", "medrxiv", "google_scholar", "download"]}
    except Exception as e:
        _close_client()
        return {"error": str(e), "action": action}


def _action_search_source(client: _MCPClient, tool_name: str, params: dict) -> dict:
    args = {
        "query": params.get("query", ""),
        "limit": int(params.get("limit", 10)),
    }
    return client.call_tool(tool_name, args)


def _action_download(client: _MCPClient, params: dict) -> dict:
    source = params.get("source", "arxiv")
    paper_id = params.get("paper_id", "")
    if not paper_id:
        return {"error": "download requires 'paper_id'"}
    tool_map = {
        "arxiv": "download_arxiv",
        "pubmed": "download_pubmed",
        "biorxiv": "download_biorxiv",
        "medrxiv": "download_medrxiv",
    }
    tool_name = tool_map.get(source)
    if not tool_name:
        return {"error": f"Unknown download source: {source}", "valid_sources": list(tool_map.keys())}
    return client.call_tool(tool_name, {"paper_id": paper_id})
