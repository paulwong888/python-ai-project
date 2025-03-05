import os, yfinance as yf
from typing import List, Dict
from datetime import datetime
from serpapi import GoogleSearch

async def get_stock_data(symbol: str) -> Dict[str, any]:
    """
    Get real stock market data for a given symbol with improved error handling
    Args:
        symbol: Stock ticker symbol (e.g. 'TSLA')
    Returns:
        Dict containing price, volume, PE ratio and market cap
    """
    try:
        # 创建股票对象
        stock = yf.Ticker(symbol)

        # 获取实时价格数据
        price_info = stock.history(period='1d')
        if not price_info.empty:
            current_price = price_info['Close'].iloc[-1]
        else:
            current_price = None

        # 获取其他信息
        info = stock.info

        return {
            "price": current_price,
            "volume": info.get("regularMarketVolume"),
            "pe_ratio": info.get("forwardPE"),
            "market_cap": info.get("marketCap"),
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    except Exception as e:
        print(f"Error fetching stock data for {symbol}: {str(e)}")
        return {
            "price": None,
            "volume": None,
            "pe_ratio": None,
            "market_cap": None,
            "error": str(e)
        }

async def get_news(query: str) -> List[Dict[str, str]]:
    """Get recent news articles about a company"""
    params = {
        "engine": "google_news",
        "q": query,
        "gl": "us",
        "hl": "en",
        "api_key": os.getenv("SERPAPI_API_KEY"),
        "num": 3  # 限制结果数量
    }

    try:
        search = GoogleSearch(params)
        results = search.get_dict()

        news_items = []
        for article in results.get("news_results", []):
            # 获取更多文章细节
            title = article.get("title", "").strip()
            source = article.get("source", {})
            source_name = source.get("name", "")
            authors = source.get("authors", [])
            author_text = f"By {', '.join(authors)}" if authors else ""

            # 提取或构建摘要
            snippet = article.get("snippet", "")
            description = article.get("description", "")
            link_text = article.get("link_text", "")

            # 选择最长的非空内容作为摘要
            summary_candidates = [s for s in [snippet, description, link_text] if s]
            summary = max(summary_candidates, key=len) if summary_candidates else title

            # 格式化日期
            date_str = article.get("date", "")
            try:
                if date_str:
                    date_obj = datetime.strptime(date_str.split(",")[0], "%m/%d/%Y")
                    formatted_date = date_obj.strftime("%Y-%m-%d")
                else:
                    formatted_date = datetime.now().strftime("%Y-%m-%d")
            except:
                formatted_date = date_str

            news_items.append({
                "title": title,
                "date": formatted_date,
                "summary": f"{summary} {author_text}".strip(),
                "source": source_name
            })

        return news_items

    except Exception as e:
        print(f"Error fetching news: {str(e)}")
        return []