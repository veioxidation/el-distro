from sqlalchemy import Table, Column, Integer, ForeignKey

from config import SCHEMA_NAME
from models.CoreModel import CoreModel

member_skillsets = Table('member_skillsets', CoreModel.metadata,
                         Column('member_id', Integer, ForeignKey(f'members.id', ondelete='cascade')),
                         Column('skillset_id', Integer, ForeignKey(f'skillsets.id', ondelete='cascade')),
                         schema=SCHEMA_NAME
                         )