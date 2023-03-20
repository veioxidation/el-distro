import unittest

from functions import assign_member_to_project, unassign_member_from_project, change_assignment_capacity
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
            assign_member_to_project(s, m_id, p_id, 60)
            self.assertEqual(m.get_full_capacity(), 100)
            self.assertEqual(m.get_free_capacity(), 40)

            # Change capacity to 20
            change_assignment_capacity(s, m_id, p_id, 20)
            self.assertEqual(m.get_free_capacity(), 80)

            # Remove the assignment
            unassign_member_from_project(s, m_id, p_id)
            self.assertEqual(m.get_free_capacity(), 100)

if __name__ == '__main__':
    unittest.main()
