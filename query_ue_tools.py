import asyncio
from mcp import ClientSession
from mcp.client.sse import sse_client

async def main():
    url = "http://127.0.0.1:8000/sse" # Standard SSE endpoint often ends in /sse or /mcp/sse
    try:
        async with sse_client(url) as streams:
            async with ClientSession(streams[0], streams[1]) as session:
                await session.initialize()
                tools = await session.list_tools()
                for tool in tools.tools:
                    print(f"Tool: {tool.name}")
                    print(f"Schema: {tool.inputSchema}")
                    print("-" * 40)
    except Exception as e:
        print(f"Error with /sse: {e}")
        
        # fallback to /mcp
        url2 = "http://127.0.0.1:8000/mcp"
        try:
            async with sse_client(url2) as streams:
                async with ClientSession(streams[0], streams[1]) as session:
                    await session.initialize()
                    tools = await session.list_tools()
                    for tool in tools.tools:
                        print(f"Tool: {tool.name}")
                        print(f"Schema: {tool.inputSchema}")
                        print("-" * 40)
        except Exception as e2:
            print(f"Error with /mcp: {e2}")

if __name__ == "__main__":
    asyncio.run(main())
