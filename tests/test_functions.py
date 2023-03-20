import unittest

from functions import assign_member_to_project, unassign_member_from_project, change_assignment_capacity, \
    check_project_assignments
from models.Assignment import Assignment
from models.Member import Member
from models.Project import Project
from models.db import Session

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

class AssingmentFunctions(unittest.TestCase):

    def test_assigning(self):
        with Session() as s:
            m = Member.add(s, name='Przemek', capacity=100)
            p = Project.add(s, name='wasting my life', effort_estimate=100)
            m_id = m.id
            p_id = p.id

            # Assign user to a project
            # assign_member_to_project(s, m_id, p_id, 60)
            assignment = s.query(Assignment).filter_by(member_id=m_id, project_id=p_id).first()
            if assignment:
                # Update the existing assignment's capacity
                assignment.capacity = 60
            else:
                # Create a new assignment for the member and project
                assignment = Assignment(member_id=m_id, project_id=p_id, capacity=60)
                s.add(assignment)
                s.commit()

            self.assertEqual(m.get_full_capacity(), 100)
            self.assertEqual(m.get_free_capacity(), 40)

            # Change capacity to 20
            assignment = s.query(Assignment).filter_by(project_id=p_id, member_id=m_id).first()
            assignment.capacity = 20

            # change_assignment_capacity(s, m_id, p_id, 20)
            self.assertEqual(m.get_free_capacity(), 80)

            # Remove the assignment
            # Delete the assignment for the member and project
            s.query(Assignment).filter_by(member_id=m_id, project_id=p_id).delete()
            s.commit()
            self.assertEqual(m.get_free_capacity(), 100)

            # s.delete(m)
            # s.delete(p)

    # def test_assignment_capacity(self):
    #     with Session() as s:
    #         m = Member.add(s, name='Przemek', capacity=100)
    #         m2 = Member.add(s, name='Aarif', capacity=100)
    #         p = Project.add(s, name='wasting my life', effort_estimate=100)
    #         m_id = m.id
    #         m2_id = m2.id
    #         p_id = p.id
    #
    #         # Assign user to a project
    #         assign_member_to_project(s, m_id, p_id, 60)
    #
    #         self.assertFalse(check_project_assignments(s, p_id))
    #
    #         # Assign user to a project
    #         assign_member_to_project(s, m2_id, p_id, 60)
    #         self.assertTrue(check_project_assignments(s, p_id))
    #
    #
    #         s.delete(m)
    #         s.delete(m2)
    #         s.delete(p)
    #         s.commit()


if __name__ == '__main__':
    unittest.main()
