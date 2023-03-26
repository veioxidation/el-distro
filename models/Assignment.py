from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from config import SCHEMA_NAME
from models.CoreModel import CoreModel


class Assignment(CoreModel):
    __tablename__ = 'assignments'
    __table_args__ = {'schema': SCHEMA_NAME}
    __mapper_args__ = {"exclude_properties": ["uploaded"]}

    id = Column(Integer, primary_key=True)
    capacity = Column(Integer, nullable=False)

    # Define the many-to-one relationship with members
    member_id = Column(Integer, ForeignKey(f'members.id', ondelete='cascade'))
    member = relationship('Member', back_populates=f'assignments')

    # Define the many-to-one relationship with projects
    project_id = Column(Integer, ForeignKey(f'projects.id', ondelete='cascade'))
    project = relationship('Project', back_populates=f'assignments')

    def change_capacity(self, new_capacity):
        self.capacity = new_capacity

    def change_member(self, new_member):
        self.capacity = new_member

    @classmethod
    def query_by_project_id(cls, s, project_id):
        return s.query(cls).filter_by(project_id=project_id).all()

    @classmethod
    def query_by_member_id(cls, s, member_id):
        return s.query(cls).filter_by(member_id=member_id).all()

    @classmethod
    def query_by_member_and_project_id(cls, s, project_id, member_id):
        return s.query(cls).filter_by(project_id=project_id,
                                      member_id=member_id).first()

    def json(self):
        return { 'id': self.id,
                 'capacity' : self.capacity,
                 'member_id': self.member_id,
                 'project_id': self.project_id,
                 'member': self.member.json(),
                 'project': self.project.json(),
        }