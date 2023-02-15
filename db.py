from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

connection_db= "postgresql://postgres:123456@localhost:5432/flask_db"
base = declarative_base()
engine = create_engine(connection_db)
Session = sessionmaker(bind=engine)

