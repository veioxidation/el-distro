from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from config import SCHEMA_NAME
from create_engine import Base, Session
from data_models.Assignment import Assignment
from data_models.CoreModel import CoreModel
from data_models.Member import Member
from data_models.MemberSkillsets import member_skillsets
from data_models.Project import Project


class Skillset(CoreModel):
    __tablename__ = 'skillsets'
    __table_args__ = {'schema': SCHEMA_NAME}

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    level = Column(String(20), nullable=True)

    # Define the many-to-many relationship with members
    members = relationship('Member', secondary=member_skillsets, back_populates=f'{SCHEMA_NAME}.skillsets')

if __name__ == '__main__':
    m = Member(name='John Doe')
    p = Project(name='Project 1')
    a = Assignment(capacity = 100, member_id=m.id, project_id=p.id)



    m = Skillset(name='Python', Level="Experienced")
    with Session() as s:
        s.add(m)
        s.commit()
        Skillset.remove_by_id(s, m.id)
