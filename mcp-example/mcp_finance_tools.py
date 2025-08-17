
from mcp.server.fastmcp import FastMCP
import yfinance as yf

mcp = FastMCP("Finance",port=3001)

@mcp.tool()
def get_stock_price(stock_symbol):
    """Fetch stock price of given symbol e.g. AAPL """
    try:
        stock = yf.Ticker(stock_symbol)
        price = stock.history(period="1d")["Close"][0]
        return f"The current price of the stock {stock_symbol} is {price:.2f}"
    except Exception as e:
        return f"Count not retrive the stock price for symbol {stock_symbol}, Error {e}"

@mcp.tool()       
def get_stock_info(stock_symbol):
    """Fetch stock information of given symbol e.g. AAPL """
    try:
        stock = yf.Ticker(stock_symbol)
        info = stock.info
        print(info["longBusinessSummary"])
        return info["longBusinessSummary"]
    except Exception as e:
        return f"Count not retrive the stock info for symbol {stock_symbol}, Error {e}"    

if __name__ == "__main__":
    mcp.run(transport="sse")