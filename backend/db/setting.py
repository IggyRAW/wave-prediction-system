from sqlalchemy import create_engine
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base

URL = "sqlite:///./db/wave-prediction-system.db"
engine = create_engine(URL, echo=False)  # Trueの場合実行時にSQLが出力

session = scoped_session(
    sessionmaker(autocommit=False, autoflush=True, bind=engine)
)

# modelで使用
Base = declarative_base()
Base.query = session.query_property()
