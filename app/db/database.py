# app/db/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()  # Carga las variables de .env
# Carga desde variable de entorno o puedes hardcodear si estás empezando
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:@localhost:3307/python_bakdend")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()
