# config.py (配置文件)
import os
from dotenv import load_dotenv

class Config:
    load_dotenv("/home/paul/config/.env-deepseek")
    # 数据库配置
    DB_PATH = os.path.join(os.path.dirname(__file__), 'football_data.db')
    
    # API密钥（示例）
    FOOTBALL_API_KEY = os.getenv("FOOTBALL_DATA_KEY")
    
    # 请求头
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Accept-Encoding': 'gzip, deflate',
        'X-Auth-Token': '2440631ab75741c8b3af49d9b34e3fda',
    }

    # 代理设置（可选）
    PROXIES = None

    API_URL = "https://api.football-data.org/v4/"