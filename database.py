from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,  declarative_base
import os


DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)
