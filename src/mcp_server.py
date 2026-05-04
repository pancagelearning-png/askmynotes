import sys
import json
import os

sys.path.insert(0, os.path.dirname(__file__))
from chain import answer

SERVER_NAME = "askmynotes"
SERVER_VERSION = "1.0.0"

TOOLS = [
    {
        "name": "search_my_notes",
        "description": "Search personal notes and PDFs to answer questions",
        "inputSchema": {
            "type": "object",
            "properties": {
                "question": {
                    "type": "string",
                    "description": "The question to search for in the notes",
                }
            },
            "required": ["question"],
        },
    }
]


def send(obj):
    line = json.dumps(obj)
    sys.stdout.write(line + "\n")
    sys.stdout.flush()


def handle(req):
    method = req.get("method")
    req_id = req.get("id")

    if method == "initialize":
        send({
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "serverInfo": {"name": SERVER_NAME, "version": SERVER_VERSION},
                "capabilities": {"tools": {}},
            },
        })

    elif method == "notifications/initialized":
        pass  # no response needed for notifications

    elif method == "tools/list":
        send({
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {"tools": TOOLS},
        })

    elif method == "tools/call":
        tool_name = req.get("params", {}).get("name")
        arguments = req.get("params", {}).get("arguments", {})

        if tool_name == "search_my_notes":
            question = arguments.get("question", "")
            result = answer(question)
            send({
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [{"type": "text", "text": result}],
                    "isError": False,
                },
            })
        else:
            send({
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32601, "message": f"Unknown tool: {tool_name}"},
            })

    else:
        if req_id is not None:
            send({
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32601, "message": f"Method not found: {method}"},
            })


def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            handle(req)
        except json.JSONDecodeError:
            send({
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32700, "message": "Parse error"},
            })


if __name__ == "__main__":
    main()
