from .base_crawler import BaseCrawler
from database.models import Team
from a01_config import Config

# （球队爬虫）
class TeamCrawler(BaseCrawler):
    def scrape_team(self, team_id):
        url = Config.API_URL + f"teams/{team_id}"
        response = self.safe_request(url)
        
        if response:
            data = self.parse_json(response)
            return self._transform_team_data(data)
        return None

    def _transform_team_data(self, raw_data):
        """清洗转换球队数据"""
        return {
            'founded_date': raw_data.get('founded'),
            'home_stadium': raw_data.get('venue'),
            'league_titles': self._parse_titles(raw_data),
            'financial_data': {
                'transfer_budget': raw_data.get('transferBudget'),
                'sponsors': raw_data.get('sponsors')
            }
        }

    def _parse_titles(self, data):
        # 解析冠军数据的自定义逻辑
        return {title['season']: title['name'] for title in data.get('trophies', [])}