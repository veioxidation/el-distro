import unittest

from models.Assignment import Assignment
from models.Member import Member
from models.Project import Project
from models.Skillset import Skillset
from models.db import Session

session = Session()


class TestDatabase(unittest.TestCase):
    def test_create_member(self):
        # create a new member
        _name = 'Test Member'
        member = Member(name=_name, capacity=100)
        session.add(member)
        session.commit()

        # check that the member was added to the database
        assert session.query(Member).filter_by(name=_name).first() is not None
        Member.remove_by_id(session, member.id)

    def test_create_member_2(self):
        # create a new member
        _name = 'Test Member 2'
        member = Member.add(session, name=_name, capacity=100)

        # check that the member was added to the database
        self.assertIsNotNone(session.query(Member).filter_by(name=_name).first())
        Member.remove_by_id(session, member.id)

    def test_update_member(self):
        # create a new member
        member = Member(name='Przemek', capacity=100)
        session.add(member)
        session.commit()

        # update the member's name
        member.name = 'Jane Doe'
        member.email = 'random@email.com'
        session.commit()

        # check that the member's name was updated in the database
        self.assertIsNotNone(session.query(Member).filter_by(name='Jane Doe').first())
        # Member.remove_by_id(session, member.id)

    def test_skills(self):
        skills_names = ['Python', 'AA', 'Kofax']
        skills = [Skillset.add(session, name=x) for x in skills_names]
        member = Member.add(session, name='Przemked', skillsets=skills, capacity=100)
        self.assertEqual(len(skills), 3)
        Member.remove_by_id(session, member.id)



    def test_project_assignment(self):
        ss1 = Skillset.add(session, name='Python')
        ss2 = Skillset.add(session, name='AA')
        m = Member(name='Przemek', capacity=100, skillsets = [ss1, ss2])
        p = Project(name='Project 1')
        a = Assignment(capacity=100, member_id=m.id, project_id=p.id)

        session.add(m)
        session.add(p)
        session.add(a)
        session.commit()
        Member.remove_by_id(session, m.id)
        Project.remove_by_id(session, p.id)


if __name__ == '__main__':
    unittest.main()
