import requests
import time
import random
from bs4 import BeautifulSoup
from a01_config import Config
from database.connector import Database

# （基础爬虫类）
class BaseCrawler:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(Config.HEADERS)
        self.db = Database()
        self.session.proxies = Config.PROXIES

    def safe_request(self, url, method='GET', retry=3, **kwargs):
        for attempt in range(retry):
            try:
                time.sleep(random.uniform(7, 9))
                resp = self.session.request(method, url, **kwargs)
                resp.raise_for_status()
                if resp.status_code == 403:
                    raise Exception("Anti-scraping detected")
                return resp
            except Exception as e:
                print(f"Attempt {attempt+1} failed: {str(e)}")
        return None

    def parse_json(self, response):
        try:
            return response.json()
        except ValueError:
            return None

    def parse_html(self, response):
        return BeautifulSoup(response.text, 'html.parser')