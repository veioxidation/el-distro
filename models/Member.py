from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from config import SCHEMA_NAME
from models.CoreModel import CoreModel
from models.MemberSkillsets import member_skillsets


class Member(CoreModel):
    __tablename__ = 'members'
    __table_args__ = {'schema': SCHEMA_NAME}

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    capacity = Column(Integer, nullable=False, default=100)
    email = Column(String(100), nullable=True)

    # Define the many-to-many relationship with skillsets
    skillsets = relationship('Skillset', secondary=member_skillsets, back_populates=f'members')

    # Define the one-to-many relationship with assignments
    assignments = relationship('Assignment', back_populates=f'member', cascade='all, delete')

    def get_skills_for_member(member_id):
        member = Member.query.get(member_id)
        skillsets = []
        for skill in member.skills:
            skillsets.append(skill.name)
        return skillsets

    def get_free_capacity(self):
        return self.capacity - sum([a.capacity for a in self.assignments])

    def get_full_capacity(self):
        return self.capacity

    def get_assignments(self):
        return self.assignments