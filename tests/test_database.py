import unittest

from create_engine import db
from models.Assignment import Assignment
from models.Member import Member
from models.Project import Project


class TestDatabase(unittest.TestCase):
    def test_create_member(self):
        # create a new member
        member = Member(name='John Doe')
        db.session.add(member)
        db.session.commit()

        # check that the member was added to the database
        assert Member.query.filter_by(name='John Doe').first() is not None

    def test_update_member(self):
        # create a new member
        member = Member(name='John Doe')
        db.session.add(member)
        db.session.commit()

        # update the member's name
        member.name = 'Jane Doe'
        db.session.commit()

        # check that the member's name was updated in the database
        assert Member.query.filter_by(name='Jane Doe').first() is not None

    # def test_delete_member(self):
    #     # create a new member
    #     member = Member(name='John Doe')
    #     db.session.add(member)
    #     db.session.commit()
    #
    #     # delete the member
    #     db.session.delete(member)
    #     db.session.commit()
    #
    #     # check that the member was deleted from the database
    #     assert Member.query.filter_by(name='John Doe').first() is None

    # def test_create_assignment(self):
    #     # create a new member
    #     member = Member(name='John Doe')
    #     db.session.add(member)
    #     db.session.commit()
    #
    #     # create a new project
    #     project = Project(name='Project A', estimated_effort=5, skill='Python')
    #     db.session.add(project)
    #     db.session.commit()
    #
    #     # assign the member to the project
    #     assignment = Assignment(member_id=member.id, project_id=project.id, capacity=4)
    #     db.session.add(assignment)
    #     db.session.commit()
    #
    #     # check that the assignment was added to the database
    #     assert Assignment.query.filter_by(member_id=member.id, project_id=project.id).first() is not None


if __name__ == '__main__':
    unittest.main()
