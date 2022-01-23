import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session




def start() -> scoped_session:
	from tronx.clients import app

	engine = create_engine(app.DB_URI)
	BASE.metadata.bind = engine
	BASE.metadata.create_all(engine)
	return scoped_session(sessionmaker(bind=engine, autoflush=False))


BASE = declarative_base()
SESSION = start()

