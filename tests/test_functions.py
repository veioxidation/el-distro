import unittest
import warnings
from datetime import date

from functions import assign_member_to_project, unassign_member_from_project, check_project_assignments, \
    calculate_project_due_date
from models.Member import Member
from models.Project import Project
from models.db import Session

warnings.filterwarnings("ignore", category=DeprecationWarning)


class AssignmentFunctions(unittest.TestCase):

    def test_assigning(self):
        with Session() as s:
            start_capacity = 100

            m = Member.add(s, name='Przemek', capacity=start_capacity)
            p = Project.add(s, name='wasting my life', effort_estimate=100)
            m_id = m.id
            p_id = p.id

            # Assign user to a project
            a = assign_member_to_project(s, m_id, p_id, 60)

            self.assertEqual(m.get_full_capacity(), start_capacity)
            self.assertEqual(m.get_free_capacity(), start_capacity - 60)

            # Change capacity to 20
            a.capacity = 20
            self.assertEqual(m.get_free_capacity(), 80)

            # Remove the assignment
            # Delete the assignment for the member and project
            unassign_member_from_project(s, m_id, p_id)
            self.assertEqual(m.get_free_capacity(), 100)

            s.delete(m)
            s.delete(p)
            s.commit()

    def test_assignment_capacity(self):
        with Session() as s:
            start_capacity = 100
            m = Member.add(s, name='Przemek', capacity=start_capacity)
            m2 = Member.add(s, name='Aarif', capacity=start_capacity)
            p = Project.add(s, name='wasting my life', effort_estimate=100)
            m_id = m.id
            m2_id = m2.id
            p_id = p.id

            # Assign user to a project
            assign_member_to_project(s, m_id, p_id, 60)

            self.assertFalse(check_project_assignments(s, p_id))

            # Assign user to a project
            assign_member_to_project(s, m2_id, p_id, 60)
            self.assertTrue(check_project_assignments(s, p_id))

            s.delete(m)
            s.delete(m2)
            s.delete(p)
            s.commit()

    def test_timeline_calculation(self):
        with Session() as s:
            start_capacity = 100

            m = Member.add(s, name='Przemek', capacity=start_capacity)
            m2 = Member.add(s, name='Aarif', capacity=start_capacity)
            p = Project.add(s, name='wasting my life', effort_estimate=20)
            m_id = m.id
            m2_id = m2.id
            p_id = p.id

            p.start_date = date(2024, 1, 1)
            a = assign_member_to_project(s, m_id, p_id, 50)
            # Assign user to a project
            dd1 = calculate_project_due_date(s, p_id)

            a.capacity = 100
            dd2 = calculate_project_due_date(s, p_id)

            # Assign user to a project
            _ = assign_member_to_project(s, m2_id, p_id, start_capacity)
            dd3 = calculate_project_due_date(s, p_id)

            self.assertEqual((dd1 - p.start_date).days, 40)
            self.assertEqual((dd2 - p.start_date).days, 20)
            self.assertEqual((dd3 - p.start_date).days, 10)

            s.delete(m)
            s.delete(m2)
            s.delete(p)
            s.commit()


if __name__ == '__main__':
    unittest.main()
