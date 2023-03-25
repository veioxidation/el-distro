from sqlalchemy import Table, Column, Integer, ForeignKey

from config import SCHEMA_NAME
from models.CoreModel import CoreModel

member_skills = Table('member_skills', CoreModel.metadata,
                         Column('member_id', Integer, ForeignKey(f'members.id', ondelete='cascade')),
                         Column('skillset_id', Integer, ForeignKey(f'skills.id', ondelete='cascade')),
                         schema=SCHEMA_NAME
                         )