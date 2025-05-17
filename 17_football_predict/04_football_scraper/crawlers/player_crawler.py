from .base_crawler import BaseCrawler
from a01_config import Config

# （球员爬虫）
class PlayerCrawler(BaseCrawler):
    def get_player(self, player_id):
        url = Config.API_URL + f"persons/{player_id}"
        response = self.safe_request(url)
        
        if response:
            return self._process_player_data(self.parse_json(response))
        return None

    def _process_player_data(self, raw_data):
        """处理球员数据"""
        return {
            'name': raw_data.get('name'),
            'age': self._calculate_age(raw_data.get('dateOfBirth')),
            'height': raw_data.get('height'),
            'weight': raw_data.get('weight'),
            'contract_expiry': raw_data.get('contractUntil'),
            'transfer_history': self._parse_transfers(raw_data.get('transfers', []))
        }

    def _calculate_age(self, birth_date):
        # 实现年龄计算逻辑
        from datetime import datetime
        if birth_date:
            birth = datetime.strptime(birth_date, '%Y-%m-%d')
            return datetime.now().year - birth.year
        return None

    def _parse_transfers(self, transfers):
        return [{
            'date': t.get('date'),
            'type': t.get('type'),
            'clubs': {
                'from': t.get('fromTeam'),
                'to': t.get('toTeam')
            },
            'value': self._convert_transfer_value(t.get('marketValue'))
        } for t in transfers]

    def _convert_transfer_value(self, value_str):
        # 转换转会金额字符串为数值
        if '€' in value_str:
            value = value_str.replace('€', '').replace('m', '')
            return float(value) * 1e6
        return None