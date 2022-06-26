import platform



ostype = platform.uname()
is_localhost = True if ostype[1] == "localhost" else False

if ostype[0] in ("Windows",  "Linux") and is_localhost:
	from termux import Termuxconfig as Config
else: 
	from config import Config

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session




def start() -> scoped_session:
	engine = create_engine(Config.DB_URI)
	BASE.metadata.bind = engine
	BASE.metadata.create_all(engine)
	return scoped_session(sessionmaker(bind=engine, autoflush=False))


BASE = declarative_base()
SESSION = start()

