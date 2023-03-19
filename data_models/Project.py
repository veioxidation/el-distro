from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship

from config import SCHEMA_NAME
from create_engine import Base
from data_models.CoreModel import CoreModel


class Project(CoreModel):
    __tablename__ = 'projects'
    __table_args__ = {'schema': SCHEMA_NAME}

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    effort_estimate = Column(Integer, nullable=True)
    start_date = Column(Date, nullable=True)
    due_date = Column(Date, nullable=True)

    # Define the many-to-one relationship with skill sets
    skillset_id = Column(Integer, ForeignKey(f'{SCHEMA_NAME}.skillsets.id'))
    skillset = relationship('Skillset', back_populates=f'{SCHEMA_NAME}.projects')

    # Define the one-to-many relationship with assignments
    assignments = relationship('Assignment', back_populates=f'{SCHEMA_NAME}.projects')
