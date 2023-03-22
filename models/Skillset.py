from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from config import SCHEMA_NAME
from models.CoreModel import CoreModel
from models.MemberSkillsets import member_skillsets


class Skillset(CoreModel):
    __tablename__ = 'skillsets'
    __table_args__ = {'schema': SCHEMA_NAME}
    __mapper_args__ = {"exclude_properties": ["uploaded"]}

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)

    # Define the many-to-many relationship with members
    members = relationship('Member', secondary=member_skillsets, back_populates=f'skillsets')

    @classmethod
    def add(cls, s, **kwargs):
        result = s.query(cls).filter_by(name=kwargs['name']).first()
        if result:
            return result
        else:
            return super().add(s, **kwargs)

    @classmethod
    def query_by_name(cls, s, **kwargs):
        return s.query(cls).filter_by(name=kwargs['name']).first()
