from database.connector import Database
from crawlers.team_crawler import TeamCrawler
from crawlers.player_crawler import PlayerCrawler
from database.models import Team, Player

# main.py（主程序）
def main():
    # 初始化数据库
    db = Database()
    db.create_tables()
    
    # 爬取球队数据
    team_crawler = TeamCrawler()
    man_united = team_crawler.scrape_team(66)  # 曼联ID示例
    
    # 爬取球员数据
    player_crawler = PlayerCrawler()
    messi = player_crawler.get_player(1547)  # 梅西ID示例
    
    # 存储数据
    with db.Session() as session:
        session.add(Team(**man_united))
        session.add(Player(**messi))
        session.commit()

if __name__ == "__main__":
    main()