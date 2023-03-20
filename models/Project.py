from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship

from config import SCHEMA_NAME
from models.CoreModel import CoreModel


class Project(CoreModel):
    __tablename__ = 'projects'
    __table_args__ = {'schema': SCHEMA_NAME}

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    effort_estimate = Column(Integer, nullable=True)
    start_date = Column(Date, nullable=True)
    due_date = Column(Date, nullable=True)

    # Define the many-to-one relationship with skill sets
    # skillset_id = Column(Integer, ForeignKey(f'skillsets.id'))
    # skillset = relationship('Skillset', back_populates=f'projects')

    # Define the one-to-many relationship with assignments
    assignments = relationship('Assignment', back_populates=f'project', cascade='all, delete')

    def get_all_capacity_assigned(self):
        return sum([a.capacity for a in self.assignments])

    def get_assigned(self):
        return [a.member for a in self.assignments]

    def get_timelines(self):
        return self.start_date, self.due_date
