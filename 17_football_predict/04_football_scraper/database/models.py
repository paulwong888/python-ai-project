from sqlalchemy import create_engine, Column, Integer, String, JSON, Date, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Team(Base):
    __tablename__ = 'teams'
    
    id = Column(Integer, primary_key=True)
    founded_date = Column(Date)
    home_stadium = Column(String)
    league_titles = Column(JSON)  # 存储{年份: 冠军名称}
    transfer_budget = Column(Float)
    financial_data = Column(JSON)

class Player(Base):
    __tablename__ = 'players'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    height = Column(Float)
    weight = Column(Float)
    contract_expiry = Column(Date)
    transfer_history = Column(JSON)

class Match(Base):
    __tablename__ = 'matches'
    
    id = Column(Integer, primary_key=True)
    competition = Column(String)
    season = Column(String)
    stats = Column(JSON)
    heatmaps = Column(JSON)