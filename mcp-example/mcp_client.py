import asyncio
import sys
from llama_index.tools.mcp import BasicMCPClient, McpToolSpec
from llama_index.core.agent.workflow import ReActAgent
from llama_index.llms.ollama import Ollama
from prompt_template import FINANCE_PROMPT
import os

# Configuration variables
MCP_URL = os.environ.get("MCP_URL", "http://127.0.0.1:3001/sse")
MODEL_NAME = os.environ.get("LLM_MODEL", "qwen3:4b")
TEMPERATURE = float(os.environ.get("LLM_TEMPERATURE", "0.7"))

async def setup_agent():
    """Setup and return the finance assistant agent"""
    try:
        # Connect to MCP server
        print(f"Connecting to MCP server at {MCP_URL}")
        mcp_client = BasicMCPClient(MCP_URL)
        
        # Get tools list
        print("Fetching available tools...")
        tools = await McpToolSpec(client=mcp_client).to_tool_list_async()
        print(f"Found {len(tools)} tools")
        
        # Initialize Ollama LLM
        print(f"Initializing Ollama with model {MODEL_NAME}...")
        llm = Ollama(model=MODEL_NAME, temperature=TEMPERATURE)
        
        # Create agent with finance search prompt
        system_prompt = FINANCE_PROMPT.template.replace("{tools}", "").replace("{tool_names}", "").replace("{input}", "")
        agent = ReActAgent(
            name="FinanceAgent", 
            llm=llm, 
            tools=tools,
            system_prompt=system_prompt,
            temperature=TEMPERATURE
        )
        
        return agent
    except Exception as e:
        print(f"Error setting up agent: {str(e)}")
        raise

async def main():
    """Main function to run the application"""
    print("\n Natural Language Financial Assistant ")
    print("-" * 50)
    print("Ask me anything about stock price and description using natural language!")
    print("\nType 'exit' or 'quit' to end the session.")
    print("-" * 50)  
    print("Make sure the agent server is running with:")

    
    try:
        # Set up the agent
        agent = await setup_agent()
        # Start conversation loop
        while True:
            user_query = input("\n🔍 Your financial query: ")
            
            if user_query.lower() in ['exit', 'quit', 'q']:
                print("\nThank you for using the Financial Assistant. Goodbye!")
                break
            
            if user_query.strip():
                print("Processing...")
                try:
                    response = await agent.run(user_query)
                    print(f"\n{response}")
                except Exception as e:
                    print(f"Error processing query: {e}")
                
    except Exception as e:
        print(f"Error: {e}")
        print(f"Make sure the server is running at {MCP_URL}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(asyncio.run(main())) 