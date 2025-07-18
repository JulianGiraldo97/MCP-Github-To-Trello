"""
Example MCP Client

This script demonstrates how to interact with the MCP server programmatically.
"""

import asyncio
import json
import subprocess
import sys
from typing import Dict, Any


class MCPClient:
    def __init__(self, server_command: str):
        """Initialize the MCP client."""
        self.server_command = server_command
        self.process = None
        self.request_id = 0
    
    async def start_server(self):
        """Start the MCP server process."""
        self.process = await asyncio.create_subprocess_exec(
            *self.server_command.split(),
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
    
    async def send_request(self, method: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Send a request to the MCP server."""
        if not self.process:
            raise RuntimeError("Server not started")
        
        self.request_id += 1
        request = {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": method,
            "params": params or {}
        }
        
        # Send request
        request_str = json.dumps(request) + "\n"
        self.process.stdin.write(request_str.encode())
        await self.process.stdin.drain()
        
        # Read response
        response_line = await self.process.stdout.readline()
        if not response_line:
            raise RuntimeError("No response from server")
        
        try:
            response = json.loads(response_line.decode().strip())
            return response
        except json.JSONDecodeError as e:
            # Try to read more lines to get the full response
            full_response = response_line.decode()
            while True:
                try:
                    line = await asyncio.wait_for(self.process.stdout.readline(), timeout=1.0)
                    if not line:
                        break
                    full_response += line.decode()
                    try:
                        response = json.loads(full_response.strip())
                        return response
                    except json.JSONDecodeError:
                        continue
                except asyncio.TimeoutError:
                    break
            
            raise RuntimeError(f"Failed to parse server response: {full_response}")
    
    async def list_tools(self) -> Dict[str, Any]:
        """List available tools."""
        return await self.send_request("tools/list")
    
    async def call_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Call a tool."""
        return await self.send_request("tools/call", {
            "name": name,
            "arguments": arguments
        })
    
    async def stop_server(self):
        """Stop the MCP server process."""
        if self.process:
            self.process.terminate()
            await self.process.wait()


async def main():
    """Main function demonstrating MCP client usage."""
    print("🔌 MCP Client Example")
    print("=" * 30)
    
    # Initialize client
    client = MCPClient("python mcp_server.py")
    
    try:
        # Start server
        print("🚀 Starting MCP server...")
        await client.start_server()
        print("✅ Server started")
        
        # Wait a moment for server to initialize
        await asyncio.sleep(1)
        
        # Initialize the server
        print("\n📋 Initializing server...")
        try:
            init_response = await client.send_request("initialize", {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {
                    "name": "example-client",
                    "version": "1.0.0"
                }
            })
            print(f"✅ Server initialized: {init_response.get('result', {}).get('serverInfo', {}).get('name', 'Unknown')}")
        except Exception as e:
            print(f"⚠️  Initialization warning: {e}")
            print("Continuing anyway...")
        
        # List available tools
        print("\n🔧 Listing available tools...")
        try:
            tools_response = await client.list_tools()
            tools = tools_response.get("result", {}).get("tools", [])
            
            print(f"✅ Found {len(tools)} tools:")
            for tool in tools:
                print(f"  - {tool['name']}: {tool['description']}")
        except Exception as e:
            print(f"❌ Error listing tools: {e}")
            return
        
        # Example: Get repository info
        if tools:
            print("\n📊 Getting repository information...")
            try:
                repo_response = await client.call_tool("get_repository_info", {
                    "repository_url": "microsoft/vscode"
                })
                
                result = repo_response.get("result", {})
                if "content" in result and result["content"]:
                    content = result["content"][0]
                    if content.get("type") == "text":
                        print("✅ Repository information retrieved:")
                        print(content["text"][:500] + "..." if len(content["text"]) > 500 else content["text"])
            except Exception as e:
                print(f"❌ Error getting repository info: {e}")
        
        # Example: List repositories
        print("\n📋 Listing repositories...")
        try:
            repos_response = await client.call_tool("list_repositories", {
                "username": "microsoft"
            })
            
            result = repos_response.get("result", {})
            if "content" in result and result["content"]:
                content = result["content"][0]
                if content.get("type") == "text":
                    print("✅ Repositories listed:")
                    print(content["text"][:300] + "..." if len(content["text"]) > 300 else content["text"])
        except Exception as e:
            print(f"❌ Error listing repositories: {e}")
        
        print("\n✨ Example completed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    finally:
        # Stop server
        print("\n🛑 Stopping server...")
        await client.stop_server()
        print("✅ Server stopped")


if __name__ == "__main__":
    asyncio.run(main()) 