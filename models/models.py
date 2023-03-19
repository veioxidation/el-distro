from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey, Date
from sqlalchemy import Table
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker, relationship

from config import SCHEMA_NAME
from create_engine import Base
from create_engine import db

# from models.MemberSkillsets import member_skillsets
Session = sessionmaker(db)


class CoreModel(Base):
    __abstract__ = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.create_db()

    @classmethod
    def create_db(cls):
        Base.metadata.create_all(db)

    @classmethod
    def _query_by_id(cls, s, _id):
        try:
            return s.query(cls).filter_by(id=_id).first()
        except IntegrityError:
            # Handle any database errors that may occur
            s.rollback()
            raise ValueError(f'Invalid ID of {cls.__tablename__}')

    @classmethod
    def query_all(s, cls):
        return s.query(cls).all()

    @classmethod
    def add(cls, s, **kwargs):
        i = cls(**kwargs)
        s.add(i)
        s.commit()

    @classmethod
    def update_value(cls, s, _id, name, value):
        i = cls._query_by_id(s, _id)
        if not hasattr(i, name):
            raise ValueError(f'{name} property not found in {cls.__tablename__}')
        try:
            setattr(i, name, value)
            s.commit()
        except IntegrityError:
            # Handle any database errors that may occur
            s.rollback()
            raise ValueError(f'Error setting value ({value}) for ({name}) in the item {_id}')

    @classmethod
    def remove_by_id(cls, s, _id):
        i = cls._query_by_id(s, _id)
        s.delete(i)
        s.commit()

    def json(self):
        return {k: v for k, v in self.__dict__.items() if not k.startswith("__")}


member_skillsets = Table('member_skillsets', CoreModel.metadata,
                         Column('member_id', Integer, ForeignKey(f'members.id')),
                         Column('skillset_id', Integer, ForeignKey(f'skillsets.id')),
                         schema=SCHEMA_NAME
                         )


class Skillset(CoreModel):
    __tablename__ = 'skillsets'
    __table_args__ = {'schema': SCHEMA_NAME}

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

    # Define the many-to-many relationship with members
    members = relationship('Member', secondary=member_skillsets, back_populates=f'skillsets')

    # Define the one-to-many relationship with projects
    # projects = relationship('Project', back_populates=f'skillset')


class Assignment(CoreModel):
    __tablename__ = 'assignments'
    __table_args__ = {'schema': SCHEMA_NAME}

    id = Column(Integer, primary_key=True)
    capacity = Column(Integer, nullable=False)

    # Define the many-to-one relationship with members
    member_id = Column(Integer, ForeignKey(f'members.id'))
    member = relationship('Member', back_populates=f'assignments')

    # Define the many-to-one relationship with projects
    project_id = Column(Integer, ForeignKey(f'projects.id'))
    project = relationship('Project', back_populates=f'assignments')


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
    assignments = relationship('Assignment', back_populates=f'project')


class Member(Base):
    __tablename__ = 'members'
    __table_args__ = {'schema': SCHEMA_NAME}

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    capacity = Column(Integer, nullable=False)
    email = Column(String(100), nullable=True)

    # Define the many-to-many relationship with skillsets
    skillsets = relationship('Skillset', secondary=member_skillsets, back_populates=f'members')

    # Define the one-to-many relationship with assignments
    assignments = relationship('Assignment', back_populates=f'member')

    # def get_skills_for_member(member_id):
    #     member = Member.query.get(member_id)
    #     skillsets = []
    #     for skill in member.skills:
    #         skillsets.append(skill.name)
    #     return skillsets


Base.metadata.schema = SCHEMA_NAME
Base.metadata.create_all(db)

if __name__ == '__main__':
    ss = Skillset(name='Python')
    ss2 = Skillset(name='AA')
    m = Member(name='Przemek', capacity=100)
    m.skillsets = [ss, ss2]
    p = Project(name='Project 1')

    a = Assignment(capacity=100, member_id=m.id, project_id=p.id)


    with Session() as s:
        s.add(m)
        s.add(ss)
        s.add(p)
        s.add(a)
        s.commit()
        # Skillset.remove_by_id(s, m.id)
