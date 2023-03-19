from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from config import SCHEMA_NAME
from create_engine import Base
from data_models.CoreModel import CoreModel


class Assignment(CoreModel):
    __tablename__ = 'assignments'
    __table_args__ = {'schema': SCHEMA_NAME}

    id = Column(Integer, primary_key=True)
    capacity = Column(Integer, nullable=False)

    # Define the many-to-one relationship with members
    member_id = Column(Integer, ForeignKey(f'{SCHEMA_NAME}.members.id'))
    member = relationship('Member', back_populates='assignments')

    # Define the many-to-one relationship with projects
    project_id = Column(Integer, ForeignKey(f'{SCHEMA_NAME}.projects.id'))
    project = relationship('Project', back_populates=f'{SCHEMA_NAME}.assignments')
