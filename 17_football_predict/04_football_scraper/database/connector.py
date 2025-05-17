from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from a01_config import Config

# （数据库连接）
class Database:
    def __init__(self):
        self.engine = create_engine(f'sqlite:///{Config.DB_PATH}')
        self.Session = sessionmaker(bind=self.engine)
        
    def create_tables(self):
        from .models import Base
        Base.metadata.create_all(self.engine)