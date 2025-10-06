# server.py
from fastmcp import FastMCP  # konsistent: fastmcp
mcp = FastMCP("Demo")

@mcp.tool
def add(a: int, b: int) -> int:
    "Addiert zwei Zahlen."
    return a + b

# MCP-Tool, das das Geheimnis 42 zurückgibt
@mcp.tool
def get_secret() -> int:
    "Gibt das Geheimnis zurück."
    return 45

if __name__ == "__main__":
    mcp.run()               # STDIO ist Default (entspricht transport="stdio")
    # oder: mcp.run(transport="stdio")
