import requests, os, json
import pandas as pd
import time
from a00_contant import *
from datetime import datetime
from dotenv import load_dotenv

# ----------------------------
# 配置API参数
# ----------------------------
# API_KEY = 'YOUR_API_KEY'  # 替换为你的API密钥
API_HOST = api_host
SEASON = 2023
LEAGUE_ID = 39  # 英超联赛ID（完整联赛ID列表见文档）

class MyDataset():
    def __init__(self):
        load_dotenv(dotenv_path)
        self.API_KEY = os.getenv("API_FOOTBALL_KEY")

    def request_data(self, url_path, params):
        url = base_api_url + url_path
        headers = {
            'x-rapidapi-host': API_HOST,
            'x-rapidapi-key': self.API_KEY
        }

        # 2. 发送API请求
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            print(f"请求失败，状态码：{response.status_code}")
            return None
        
        data = response.json()

        return data

    def find_read_json(self, dir_path, fixture_id):
        result = None
        with os.scandir(dir_path) as files:
            print(fixture_id)
            for entry in files:
                if entry.is_file() and entry.name.endswith("json"):
                    file_path = str(entry.path)
                    data = self.read_json(file_path)
                    tem_fixture_id = int(data["parameters"]["fixture"])
                    # print(f"type tem_fixture_id: {type(tem_fixture_id)}, type fixture_id: {type(fixture_id)}")
                    # print(f"current tem_fixture_id: {tem_fixture_id}, file_path: {file_path}")
                    if tem_fixture_id == fixture_id:
                        result = data
                        break
        return result


    def read_json(self, file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        return data
    
    def json_to_file(self, data, file_name):
        file_path = os.path.join(json_out_dir, file_name)
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def to_float(self, str: str):
        aa = float(str.strip("%"))
        aa = aa / 100.0
        return aa

    def get_statistics(self, fixture_id, home_id, away_id, statistics_index) -> dict:
        params = dict(
            fixture=fixture_id
        )

        # 从api读取数据
        # data  = self.request_data("/fixtures/statistics", params)

        # self.json_to_file(data, "statics/statics-" + statistics_index + ".json")

        # 从json读取数据
        # file_path = "17_football_predict/02_league/data/statics.json"
        # data  = self.read_json(file_path)["response"]

        json_dir = os.path.join(json_out_dir, "statics") 
        data = self.find_read_json(json_dir, fixture_id)
        
        stats_dict = {}
        if data:
            for team_info in data['response']:
                stats = team_info["statistics"]
                for stat in stats:
                    if team_info["team"]["id"] == home_id:
                        if stat['type'] == 'Shots on Goal':
                            stats_dict['home_shots_on_target'] = stat["value"]
                        if stat['type'] == 'Ball Possession':
                            stats_dict['home_possession'] = self.to_float(stat["value"])
                    elif team_info["team"]["id"] == away_id:
                        if stat['type'] == 'Shots on Goal':
                            stats_dict['away_shots_on_target'] = stat["value"]
                        if stat['type'] == 'Ball Possession':
                            stats_dict['away_possession'] = self.to_float(stat["value"])

        return stats_dict

    # ----------------------------
    # 定义核心函数
    # ----------------------------
    def get_fixtures_data(self, league_id, season, update_existing=True, fixtures_index=1):
        """
        采集指定联赛和赛季的比赛数据（赛程、比分、统计）
        Args:
            league_id (int): 联赛ID（如英超=39）
            season (int): 赛季年份（如2023）
            update_existing (bool): 是否追加新数据到现有文件
        Returns:
            DataFrame: 包含比赛数据的表格
        """
        # 1. 初始化请求参数
        # url = base_api_url + '/fixtures'
        # headers = {
        #     'x-rapidapi-host': API_HOST,
        #     'x-rapidapi-key': self.API_KEY
        # }
        params = {
            'league': league_id,
            'season': season,
            'timezone': 'Asia/Shanghai'
        }

        # 2. 发送API请求
        # response = requests.get(url, headers=headers, params=params)
        # if response.status_code != 200:
        #     print(f"请求失败，状态码：{response.status_code}")
        #     return None
        
        # data = response.json()['response']

        # 从api读数据
        # data = self.request_data("/fixtures", params)

        # self.json_to_file(data, "fixtures/fixtures-" + str(fixtures_index) + ".json")

        # 从json读数据
        file_path = "17_football_predict/02_league/data/fixtures.json"
        data = self.read_json(file_path)
        
        # 3. 解析数据
        matches = []
        for i, match in enumerate(data['response']):
            # 提取基础信息
            fixture = match['fixture']
            teams = match['teams']
            goals = match['goals']

            
            # stats = match.get('statistics', [])
            # 解析详细统计（射门、控球等）
            # stats_dict = {}
            # for stat in stats:
            #     if stat['type'] == 'Shots on Goal':
            #         stats_dict['home_shots_on_target'] = stat['home']
            #         stats_dict['away_shots_on_target'] = stat['away']
            #     elif stat['type'] == 'Ball Possession':
            #         stats_dict['home_possession'] = float(stat['home'].replace('%', ''))
            #         stats_dict['away_possession'] = float(stat['away'].replace('%', ''))
            
            fixture_id = fixture['id']
            home_id = teams['home']['id']
            away_id = teams['away']['id']
            statistics_index = str(fixtures_index) + "-" + str(i)
            stats_dict = self.get_statistics(fixture_id, home_id, away_id, statistics_index)

                        
            # 构建单场比赛数据
            match_data = {
                'match_id': fixture['id'],
                'date': fixture['date'],
                'league_id': league_id,
                'season': season,
                'home_team': teams['home']['name'],
                'away_team': teams['away']['name'],
                'home_goals': goals['home'],
                'away_goals': goals['away'],
                'venue': fixture['venue']['name'],
                'referee': fixture['referee'],
                **stats_dict  # 合并统计信息
            }
            matches.append(match_data)
        
        # 4. 转换为DataFrame
        df = pd.DataFrame(matches)
        
        # 5. 保存到CSV（按日期追加）
        filename = f'football_data_league_{league_id}_season_{season}.csv'
        if update_existing:
            try:
                existing_df = pd.read_csv(filename)
                combined_df = pd.concat([existing_df, df], ignore_index=True)
                combined_df.to_csv(filename, index=False)
            except FileNotFoundError:
                df.to_csv(filename, index=False)
        else:
            df.to_csv(filename, index=False)
        
        print(f"已保存{len(df)}条比赛数据到{filename}")
        return df

# ----------------------------
# 执行数据采集
# ----------------------------
if __name__ == '__main__':

    # print(os.path.join(json_out_dir, "fixtures/fixtures-"+"1"+".json"))

    # json_dir = os.path.join(json_out_dir, "statics")
    # with os.scandir(json_dir) as it:
    #     for entry in it:
    #         if entry.name.endswith("json") and entry.is_file():
    #             print(entry.name, entry.path)

    my_dataset = MyDataset()

    # fixture_id = "1035037"
    # home_id = 44
    # away_id = 50
    # data = my_dataset.get_statistics(fixture_id, home_id, away_id)


    # 采集英超2023赛季数据
    df = my_dataset.get_fixtures_data(league_id=39, season=2023)
    
    # 示例输出前5行
    print("\n采集到的数据示例:")
    print(df.head())