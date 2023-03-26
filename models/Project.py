import enum
from datetime import datetime

from sqlalchemy import Column, Integer, String, Date, Enum
from sqlalchemy.orm import relationship

from config import SCHEMA_NAME
from models.CoreModel import CoreModel


class ProjectStatusEnum(enum.Enum):
    backlog = enum.auto()
    in_analysis = enum.auto()
    in_progress = enum.auto()
    in_testing = enum.auto()
    live = enum.auto()


class Project(CoreModel):
    __tablename__ = 'projects'
    __table_args__ = {'schema': SCHEMA_NAME}
    __mapper_args__ = {"exclude_properties": ["uploaded"]}

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    effort_estimate = Column(Integer, nullable=True)
    start_date = Column(Date, nullable=True)
    due_date = Column(Date, nullable=True)

    progress = Column(Integer, nullable=False, default=0)
    status = Column(Enum(ProjectStatusEnum), default=ProjectStatusEnum.backlog)

    # Define the many-to-one relationship with skill sets
    # skillset_id = Column(Integer, ForeignKey(f'skills.id'))
    # skillset = relationship('Skillset', back_populates=f'projects')

    # Define the one-to-many relationship with assignments
    assignments = relationship('Assignment', back_populates=f'project', cascade='all, delete')

    def get_all_capacity_assigned(self):
        return sum([a.capacity for a in self.assignments])

    def get_assigned(self):
        return [a.member for a in self.assignments]

    def get_timelines(self):
        return self.start_date, self.due_date

    def get_assignemnts(self):
        return self.assignments

    def get_progress(self):
        return self.progress

    def set_progress(self):
        return self.progress

    def start_today(self):
        self.start_date = datetime.today()

    @classmethod
    def query_by_name(cls, s, **kwargs):
        return s.query(cls).filter_by(name=kwargs['name']).first()

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'effort_estimate': self.effort_estimate,
            'start_date': self.start_date or "None",
            'due_date': self.due_date or "None",
            'status': self.status.name,
            'progress': self.progress,
        }
