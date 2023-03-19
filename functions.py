from sqlalchemy import func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

# Create a session factory for connecting to the database
from data_models.Assignment import Assignment
from data_models.Project import Project
from data_models.Member import Member
from create_engine import db

import datetime


Session = sessionmaker(bind=db)


# Assign a member to a project, taking into consideration existing assignments
def assign_member_to_project(member_id, project_id, capacity):
    session = Session()
    try:
        # Check if the member is already assigned to the project
        existing_assignment = session.query(Assignment).filter_by(member_id=member_id, project_id=project_id).first()
        if existing_assignment:
            # Update the existing assignment's capacity
            existing_assignment.capacity = capacity
        else:
            # Create a new assignment for the member and project
            assignment = Assignment(member_id=member_id, project_id=project_id, capacity=capacity)
            session.add(assignment)
        session.commit()
    except IntegrityError:
        # Handle any database errors that may occur
        session.rollback()
        raise ValueError('Invalid member or project ID')
    finally:
        session.close()


# Unassign a member from a project
def unassign_member_from_project(member_id, project_id):
    session = Session()
    try:
        # Delete the assignment for the member and project
        session.query(Assignment).filter_by(member_id=member_id, project_id=project_id).delete()
        session.commit()
    except IntegrityError:
        # Handle any database errors that may occur
        session.rollback()
        raise ValueError('Invalid member or project ID')
    finally:
        session.close()


def change_assignment_capacity(project_id, member_id, new_capacity):
    session = Session()
    try:
        assignment = session.query(Assignment).filter_by(project_id=project_id, member_id=member_id).first()
        if not assignment:
            raise ValueError(f"No assignment found for project id {project_id} and member id {member_id}")
        assignment.capacity_level = new_capacity
        session.commit()
        return assignment
    except IntegrityError:
        # Handle any database errors that may occur
        session.rollback()
        raise ValueError('Wrong Values')
    finally:
        session.close()


# Check if the assignments for a project are sufficient to deliver the project
def check_project_assignments(project_id):
    session = Session()
    try:
        # Get the project and its assignments
        project = session.query(Project).get(project_id)
        assignments = project.assignments

        # Calculate the total capacity of all assignments
        total_capacity = sum(assignment.capacity for assignment in assignments)

        # Check if the total capacity is sufficient to deliver the project
        return total_capacity >= project.effort_estimate
    except IntegrityError:
        # Handle any database errors that may occur
        session.rollback()
        raise ValueError('Invalid project ID')
    finally:
        session.close()


# Calculate the due date for a project
def calculate_project_due_date(project_id):
    session = Session()
    try:
        project = session.query(Project).get(project_id)
        if not project:
            raise ValueError(f"Project with id {project_id} does not exist")

        total_effort = project.estimated_effort
        total_capacity = 0
        for assignment in project.assignments:
            total_capacity += assignment.capacity_level

        if total_capacity == 0:
            raise ValueError("Total capacity of assigned team members is 0")

        days_remaining = total_effort / total_capacity

        today = datetime.date.today()
        due_date = today + datetime.timedelta(days=days_remaining)

        return due_date
    except IntegrityError:
        # Handle any database errors that may occur
        session.rollback()
        raise ValueError('Invalid project ID')
    finally:
        session.close()


def get_total_capacity():
    session = Session()
    try:
        return session.query(func.sum(Assignment.capacity_level)).scalar()
    except IntegrityError:
        # Handle any database errors that may occur
        session.rollback()
        raise ValueError('Invalid project ID')
    finally:
        session.close()


def get_over_capacity_members():
    session = Session()
    try:
        members = session.query(Member).all()
        over_capacity_members = []
        for member in members:
            total_capacity = sum([assignment.capacity_level for assignment in member.assignments])
            if total_capacity > member.capacity:
                over_capacity_members.append(member)
        return over_capacity_members
    except IntegrityError:
        # Handle any database errors that may occur
        session.rollback()
        raise ValueError('Invalid project ID')
    finally:
        session.close()


def get_assignments_for_project(project_id):
    session = Session()
    try:
        project = session.query(Project).get(project_id)
        if not project:
            raise ValueError(f"Project with id {project_id} does not exist")
        return project.assignments
    except IntegrityError:
        # Handle any database errors that may occur
        session.rollback()
        raise ValueError('Invalid project ID')
    finally:
        session.close()



def add_new_member(name, email, skills, capacity):
    session = Session()
    try:
        m = Member(name=name, email=email, skills=skills, capacity=capacity)
        session.add(m)
        session.commit()
    except IntegrityError:
        # Handle any database errors that may occur
        session.rollback()
        raise ValueError('Invalid project ID')
    finally:
        session.close()


def remove_member_by_id(member_id):
    session = Session()
    try:
        session.query(Member).get(member_id).delete()
        session.commit()
    except IntegrityError:
        # Handle any database errors that may occur
        session.rollback()
        raise ValueError('Invalid member ID')
    finally:
        session.close()
