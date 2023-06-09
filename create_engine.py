import os

from dotenv import load_dotenv

# Load environment variables from .env file
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from config import SCHEMA_NAME

load_dotenv()

# Define database connection
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

Base = declarative_base()


# Create tables in the database
# Base.metadata.create_all(db, schema='team_capacity')

