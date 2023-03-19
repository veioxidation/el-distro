from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from config import SCHEMA_NAME
from create_engine import Session
from data_models.CoreModel import CoreModel
# from data_models.MemberSkillsets import member_skillsets
from data_models.MemberSkillsets import member_skillsets


class Member(CoreModel):
    __tablename__ = 'members'
    __table_args__ = {'schema': SCHEMA_NAME}

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    capacity = Column(Integer, nullable=False)
    email = Column(String(100), nullable=True)

    # Define the many-to-many relationship with skillsets
    skillsets = relationship('Skillset',
                             secondary=member_skillsets,
                             back_populates=f'{SCHEMA_NAME}.members')

    # Define the one-to-many relationship with assignments
    assignments = relationship('Assignment',
                               back_populates=f'{SCHEMA_NAME}.members')

    # def get_skills_for_member(member_id):
    #     member = Member.query.get(member_id)
    #     skillsets = []
    #     for skill in member.skills:
    #         skillsets.append(skill.name)
    #     return skillsets


if __name__ == '__main__':
    m = Member(name='John Doe', capacity=100)
    with Session() as s:
        s.add(m)
        s.commit()
        Member.remove_by_id(s, m.id)
