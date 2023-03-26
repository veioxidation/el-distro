from flask import Flask, render_template, request, jsonify

from create_engine import DB_URI
from functions import *
# from flask_sqlalchemy import SQLAlchemy
from models.Project import Project
from models.db import Session

app = Flask(__name__)

# Configuration for the database
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# from app_members import members_interface
#
# app.register_blueprint(members_interface)


@app.route('/')
def index():
    return render_template('base.html')


@app.route('/skills', methods=['GET'])
def skills():
    with Session() as s:
        skills = s.query(Skill).all()
    return render_template('skills.html', skills=skills)


# MEMBERS
@app.route('/members', methods=['GET'])
def members():
    with Session() as s:
        members = s.query(Member).all()
        skills = s.query(Skill).all()
        return render_template('members.html', members=members, skills=skills)


@app.route('/add_member', methods=['POST'])
def add_member():
    member_name = request.form['name']
    member_email = request.form['email']
    member_skills = request.form.getlist('skills')
    member_capacity = int(request.form['capacity'])

    if not all([member_name, member_email, member_skills, member_capacity]):
        return jsonify({'error': 'Missing fields'}), 400

    # Check if member with the same email already exists
    with Session() as s:
        try:
            new_member = add_new_member(s,
                                        name=member_name,
                                        email=member_email,
                                        skill_id_list=member_skills,
                                        capacity=member_capacity)

            # Render the new member row and return it
            # new_member_row = render_template('member_row.html', member=new_member)

            return jsonify(success=True, member={'id': new_member.id,
                                                 'name': new_member.name,
                                                 'capacity': new_member.capacity,
                                                 'skills_list': new_member.skills_list}, )
        except Exception as e:
            # Handle any errors that occur during the database operation
            s.rollback()
            return jsonify(success=False, error=str(e))


@app.route('/delete_member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    with Session() as s:
        try:
            Member.remove_by_id(s, member_id)
            return jsonify(success=True), 200
        except Exception as e:
            return jsonify(success=False, error="Member not found"), 404


@app.route('/add_skill', methods=['POST'])
def add_skill():
    skill_name = request.form['name']
    if not all([skill_name]):
        return jsonify(success=False), 400

    # Add new skill
    with Session() as s:
        new_skill = Skill.add(s, name=skill_name)
        return jsonify(success=True,
                       skill={'id': new_skill.id,
                              'name': new_skill.name}), 201


@app.route('/delete_skill/<int:skill_id>', methods=['DELETE'])
def delete_skill(skill_id):
    with Session() as s:
        try:
            Skill.remove_by_id(s, skill_id)
            return jsonify(success=True), 200
        except Exception as e:
            return jsonify(success=False, error="Skill not found"), 404


# @app.route('/assign_member', methods=['POST'])
# def assign_member():
#     project_id = request.json['project_id']
#     member_id = request.json['member_id']
#     capacity = request.json['capacity']
#
#     # Assign the member to the project
#     with Session() as s:
#         assignment = assign_member_to_project(s, project_id, member_id, capacity)
#
#     if assignment is not None:
#         return jsonify(
#             {'message': f'Member {member_id} has been assigned to project {project_id} with capacity {capacity}'}), 200
#     else:
#         return jsonify({'error': 'Could not assign member to project'}), 400


# @app.route('/unassign_member', methods=['POST'])
# def unassign_member():
#     project_id = request.json['project_id']
#     member_id = request.json['member_id']
#
#     # Unassign the member from the project
#     with Session() as s:
#         unassign_member_from_project(s, project_id, member_id)
#
#     return jsonify({'message': f'Member {member_id} unassigned from project {project_id}'}), 200


# ASSIGNMENTS
@app.route('/add_assignment', methods=['POST'])
def add_assignment():
    project_id = int(request.form['project'])
    member_id = int(request.form['member'])
    capacity = int(request.form['capacity'])
    if not all([project_id, member_id, capacity]):
        return jsonify(success=False), 400

    with Session() as s:
        assignment = assign_member_to_project(s, project_id=project_id, member_id=member_id, capacity=capacity)

        if assignment is not None:
            return jsonify(success=True, assignment=assignment.json()), 200
        else:
            return jsonify(success=False), 400

@app.route('/delete_assignment/<int:assignment_id>', methods=['DELETE'])
def delete_assignment(assignment_id):
    with Session() as s:
        try:
            Assignment.remove_by_id(s, assignment_id)
            return jsonify(success=True), 200
        except Exception as e:
            return jsonify(success=False, error="Assignment not found"), 404

# @app.route('/change_capacity', methods=['POST'])
# def change_capacity():
#     project_id = request.json['project_id']
#     member_id = request.json['member_id']
#     new_capacity = request.json['new_capacity']
#
#     # Change the capacity for the assignment
#     with Session() as s:
#         a = Assignment.query_by_member_and_project_id(s, project_id=project_id, member_id=member_id)
#         a.capacity = new_capacity
#         s.commit()
#
#     return jsonify(
#         {'message': f'Capacity for member {member_id} on project {project_id} changed to {new_capacity}'}), 200
#
#
# @app.route('/check_assignments', methods=['POST'])
# def check_assignments():
#     project_id = request.json['project_id']
#
#     # Check the assignments for the project
#     with Session() as s:
#         assignments = get_assignments_for_project(s, project_id)
#         estimated_effort = s.query(Project).filter_by(id=project_id).first().estimated_effort
#
#     total_capacity = sum([a.capacity for a in assignments])
#
#     if total_capacity >= estimated_effort:
#         return jsonify({'message': f'Assignments are sufficient to deliver project {project_id}'}), 200
#     else:
#         return jsonify({'error': f'Assignments are not sufficient to deliver project {project_id}'}), 400


# @app.route('/calculate_due_date', methods=['POST'])
# def calculate_due_date():
#     project_id = request.json['project_id']
#
#     # Calculate the due date for the project
#     with Session() as s:
#         due_date = calculate_project_due_date(s, project_id)
#
#     return jsonify({'due_date': str(due_date)}), 200
#
#
# @app.route('/check_capacity', methods=['GET'])
# def check_capacity():
#     # Check the overall capacity for the team
#     with Session() as s:
#         total_capacity = get_total_capacity(s)
#         over_capacity = [m.id for m in get_over_capacity_members(s)]
#
#     return jsonify({'total_capacity': total_capacity, 'over_capacity': over_capacity}), 200


@app.route('/assignments', methods=['GET'])
def assignments():
    with Session() as s:
        projects = s.query(Project).all()
        assignments = s.query(Assignment).all()
        members = s.query(Member).all()
        return render_template('assignments.html', projects=projects, assignments=assignments, members=members)


## PROJECTS

@app.route('/projects', methods=['GET'])
def projects():
    with Session() as s:
        projects = s.query(Project).all()
    return render_template('projects.html', projects=projects)


@app.route('/add_project', methods=['POST'])
def add_project():
    project_name = request.form['name']
    project_effort = int(request.form['effort_estimate'])
    project_start_date = request.form['start_date'] or None
    project_due_date = request.form['due_date'] or None

    if not all([project_name, project_effort]):
        return jsonify(success=False), 400

    # Check if member with the same email already exists
    with Session() as s:
        p = Project.add(s, name=project_name,
                        effort_estimate=project_effort,
                        start_date=project_start_date,
                        due_date=project_due_date)
        data = p.json()
        return jsonify(success=True, project=data), 201


@app.route('/delete_project/<int:project_id>', methods=['DELETE'])
def delete_project(project_id):
    with Session() as s:
        try:
            Project.remove_by_id(s, project_id)
            return jsonify(success=True), 200
        except Exception as e:
            return jsonify(success=False, error="Project not found"), 404


@app.route('/skills', methods=['GET'])
def get_all_skills():
    with Session() as s:
        resp = [skill.json() for skill in s.query(Skill).all()]

    return jsonify(resp), 200


if __name__ == '__main__':
    print(app.url_map)
    app.run()
