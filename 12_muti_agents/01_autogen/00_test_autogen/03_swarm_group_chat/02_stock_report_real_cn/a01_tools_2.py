from typing import List, Dict

async def get_stock_data(symbol: str) -> Dict[str, any]:
    """Get stock market data for a given symbol"""
    return {"price": 180.25, "volume": 1000000, "pe_ratio": 65.4, "market_cap": "700B"}

async def get_news(query: str) -> List[Dict[str, str]]:
    """Get recent news articles about a company"""
    return [
        {
            "title": "Tesla Expands Cybertruck Production",
            "date": "2024-03-20",
            "summary": "Tesla ramps up Cybertruck manufacturing capacity at Gigafactory Texas, aiming to meet strong demand.",
        },
        {
            "title": "Tesla FSD Beta Shows Promise",
            "date": "2024-03-19",
            "summary": "Latest Full Self-Driving beta demonstrates significant improvements in urban navigation and safety features.",
        },
        {
            "title": "Model Y Dominates Global EV Sales",
            "date": "2024-03-18",
            "summary": "Tesla's Model Y becomes best-selling electric vehicle worldwide, capturing significant market share.",
        },
    ]