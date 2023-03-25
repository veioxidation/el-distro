from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from config import SCHEMA_NAME
from models.CoreModel import CoreModel
from models.MemberSkills import member_skills


class Member(CoreModel):
    __tablename__ = 'members'
    __table_args__ = {'schema': SCHEMA_NAME}
    __mapper_args__ = {"exclude_properties": ["uploaded"]}

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    capacity = Column(Integer, nullable=False, default=100)
    email = Column(String(100), nullable=True)

    # Define the many-to-many relationship with skills
    skills = relationship('Skill', secondary=member_skills, back_populates=f'members')

    # Define the one-to-many relationship with assignments
    assignments = relationship('Assignment', back_populates=f'member', cascade='all, delete')

    @hybrid_property
    def skills_list(self):
        return [skill.name for skill in self.skills]

    def get_free_capacity(self):
        return self.capacity - sum([a.capacity for a in self.assignments])

    def get_full_capacity(self):
        return self.capacity

    def get_assignments(self):
        return self.assignments

    @classmethod
    def query_by_name(cls, s, **kwargs):
        return s.query(cls).filter_by(name=kwargs['name']).first()
