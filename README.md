# MCP Finance Assistant Example

This project demonstrates a simple Model Context Protocol (MCP) server and a ReAct-based client for answering stock questions with LLM tooling.

## Components
- `mcp-example/mcp_finance_tools.py` – FastMCP server exposing `get_stock_price` and `get_stock_info` using `yfinance`.
- `mcp-example/mcp_client.py` – Connects to the MCP server via `BasicMCPClient` and an Ollama LLM (e.g., `qwen3:4b`).
- `mcp-example/prompt_template.py` – Prompt template guiding the agent’s reasoning.

## Requirements
- Python 3.10+
- Packages: `fastmcp`, `llama-index`, `langchain`, `yfinance`, `ollama` (client-side model runtime).

## Running the MCP server
```bash
python mcp-example/mcp_finance_tools.py
```

## Running the client
```bash
MCP_URL=http://127.0.0.1:3001/sse python mcp-example/mcp_client.py
```

## Environment variables
| Variable        | Default                      | Description                     |
|-----------------|------------------------------|---------------------------------|
| `MCP_URL`       | `http://127.0.0.1:3001/sse`   | MCP server endpoint             |
| `LLM_MODEL`     | `qwen3:4b`                    | Ollama model used by the client |
| `LLM_TEMPERATURE` | `0.7`                      | Generation temperature          |

