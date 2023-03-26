import datetime

from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

# Create a session factory for connecting to the database
import routes.assignments
from models.Assignment import Assignment
from models.Member import Member
from models.Project import Project
# Assign a member to a project, taking into consideration existing assignments
from models.Skill import Skill


def assign_member_to_project(session, member_id, project_id, capacity):
    try:
        # Check if the member is already assigned to the project
        assignment = session.query(Assignment).filter_by(member_id=member_id, project_id=project_id).first()
        if assignment:
            # Update the existing assignment's capacity
            assignment.capacity = capacity
        else:
            # Create a new assignment for the member and project
            assignment = Assignment(member_id=member_id, project_id=project_id, capacity=capacity)
            session.add(assignment)
            session.commit()
        return assignment
    except IntegrityError:
        # Handle any database errors that may occur
        session.rollback()
        raise ValueError('Invalid member or project ID')


# Unassign a member from a project
def unassign_member_from_project(session, member_id, project_id):
    try:
        # Delete the assignment for the member and project
        session.query(Assignment).filter_by(member_id=member_id, project_id=project_id).delete()
        session.commit()
    except IntegrityError:
        # Handle any database errors that may occur
        session.rollback()
        raise ValueError('Invalid member or project ID')


def check_project_assignments(session, project_id):
    """
    # Check if the assignments for a project are sufficient to deliver the project
    Args:
        session: db session
        project_id: Look at the project timelines and assignments and say if this is enough.

    Returns:

    """
    try:
        # TODO -> Assignments should be timed.
        # Get the project and its assignments
        project = session.query(Project).get(project_id)
        assignments = routes.assignments.assignments

        # Calculate the total capacity of all assignments
        total_capacity = sum(assignment.capacity for assignment in assignments)

        # Check if the total capacity is sufficient to deliver the project
        return total_capacity >= project.effort_estimate
    except IntegrityError:
        # Handle any database errors that may occur
        session.rollback()
        raise ValueError('Invalid project ID')


# Calculate the due date for a project
def calculate_project_due_date(session, project_id):
    try:
        project = session.query(Project).get(project_id)
        if not project:
            raise ValueError(f"Project with id {project_id} does not exist")

        total_effort = project.effort_estimate
        total_capacity = sum([a.capacity for a in routes.assignments.assignments])
        if total_capacity == 0:
            raise ValueError("Total capacity of assigned team members is 0")

        days_remaining = total_effort / total_capacity * 100

        due_date = project.start_date + datetime.timedelta(days=days_remaining)
        return due_date
    except IntegrityError:
        # Handle any database errors that may occur
        session.rollback()
        raise ValueError('Invalid project ID')


def get_total_capacity(session):
    try:
        return session.query(func.sum(Assignment.capacity)).scalar()
    except IntegrityError:
        # Handle any database errors that may occur
        session.rollback()
        raise ValueError('Invalid project ID')


def get_over_capacity_members(session):
    try:
        members = session.query(Member).all()
        over_capacity_members = []
        return over_capacity_members
    except IntegrityError:
        # Handle any database errors that may occur
        session.rollback()
        raise ValueError('Invalid project ID')


def get_assignments_for_project(session, project_id):
    try:
        project = session.query(Project).get(project_id)
        if not project:
            raise ValueError(f"Project with id {project_id} does not exist")
        return routes.assignments.assignments
    except IntegrityError:
        # Handle any database errors that may occur
        session.rollback()
        raise ValueError('Invalid project ID')


def add_new_member(session, name: str, email: str, skill_id_list: list, capacity: int):
    try:
        skill_list = [Skill.query_by_id(session, skill_id) for skill_id in skill_id_list]
        m = Member(name=name, email=email, skills=skill_list, capacity=capacity)
        session.add(m)
        session.commit()
        return m
    except IntegrityError:
        # Handle any database errors that may occur
        session.rollback()
        raise ValueError('Invalid project ID')


def remove_member_by_id(session, member_id):
    try:
        session.query(Member).get(member_id).delete()
        session.commit()
    except IntegrityError:
        # Handle any database errors that may occur
        session.rollback()
        raise ValueError('Invalid member ID')
