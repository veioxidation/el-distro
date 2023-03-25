from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import SCHEMA_NAME
from create_engine import DB_URI, Base
from models.Assignment import Assignment
from models.Member import Member
from models.Project import Project
from models.Skill import Skill

db = create_engine(DB_URI)

Base.metadata.schema = SCHEMA_NAME

# Tables which need to be initialized as per existing relationships.
tables = {
    Member, Project, Assignment, Skill
}
Base.metadata.create_all(db)
Session = sessionmaker(db)
