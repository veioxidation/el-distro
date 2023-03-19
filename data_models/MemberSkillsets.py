from sqlalchemy import Table, Column, Integer, ForeignKey

from config import SCHEMA_NAME
from create_engine import Base

member_skillsets = Table('member_skillsets', Base.metadata,
                         Column('member_id', Integer, ForeignKey(f'{SCHEMA_NAME}.members.id')),
                         Column('skillset_id', Integer, ForeignKey(f'{SCHEMA_NAME}.skillsets.id')),
                         schema=SCHEMA_NAME
                         )
