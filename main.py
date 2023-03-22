from flask import Flask, request, jsonify, render_template

from create_engine import DB_URI
from functions import *
# from flask_sqlalchemy import SQLAlchemy
from models.Project import Project
from models.db import Session

app = Flask(__name__)

# Configuration for the database
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# db = SQLAlchemy(app)
# db.init_app(app)


# TEMPLATES

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/members_add')
def members():
    return render_template('members.html', members = get_all_members())


@app.route('/member_menu')
def member_menu():

    return render_template('new_members.html')


# MEMBERS

@app.route('/create_member', methods=['POST'])
def create_member():
    member_name = request.json.get('name')
    member_email = request.json.get('email')
    member_skills = request.json.get('skills')
    member_capacity = request.json.get('capacity')

    if not all([member_name, member_email, member_skills, member_capacity]):
        return jsonify({'error': 'Missing fields'}), 400

    # Check if member with the same email already exists
    with Session() as s:
        add_new_member(s, name=member_name, email=member_email, skills=member_skills, capacity=member_capacity)
    return jsonify({'message': 'Member created successfully'}), 201


@app.route('/members')
def get_all_members():
    with Session() as s:
        resp = [m.json() for m in s.query(Member).all()]

    return jsonify(resp), 200


# TODO - does it have to be a GET?
@app.route('/delete_member', methods=['GET'])
def delete_member():
    member_id = request.json['id']
    with Session() as s:
        remove_member_by_id(s, member_id)
    return jsonify({'message': 'Member deleted successfully'}), 200


@app.route('/assign_member', methods=['POST'])
def assign_member():
    project_id = request.json['project_id']
    member_id = request.json['member_id']
    capacity = request.json['capacity']

    # Assign the member to the project
    with Session() as s:
        assignment = assign_member_to_project(s, project_id, member_id, capacity)

    if assignment is not None:
        return jsonify(
            {'message': f'Member {member_id} assigned to project {project_id} with capacity {capacity}'}), 200
    else:
        return jsonify({'error': 'Could not assign member to project'}), 400


@app.route('/unassign_member', methods=['POST'])
def unassign_member():
    project_id = request.json['project_id']
    member_id = request.json['member_id']

    # Unassign the member from the project
    with Session() as s:
        unassign_member_from_project(s, project_id, member_id)

    return jsonify({'message': f'Member {member_id} unassigned from project {project_id}'}), 200


# ASSIGNMENTS

@app.route('/change_capacity', methods=['POST'])
def change_capacity():
    project_id = request.json['project_id']
    member_id = request.json['member_id']
    new_capacity = request.json['new_capacity']

    # Change the capacity for the assignment
    with Session() as s:
        a = Assignment.query_by_member_and_project_id(s, project_id=project_id, member_id=member_id)
        a.capacity = new_capacity
        s.commit()

    return jsonify(
        {'message': f'Capacity for member {member_id} on project {project_id} changed to {new_capacity}'}), 200


@app.route('/check_assignments', methods=['POST'])
def check_assignments():
    project_id = request.json['project_id']

    # Check the assignments for the project
    with Session() as s:
        assignments = get_assignments_for_project(s, project_id)
        estimated_effort = s.query(Project).filter_by(id=project_id).first().estimated_effort

    total_capacity = sum([a.capacity for a in assignments])

    if total_capacity >= estimated_effort:
        return jsonify({'message': f'Assignments are sufficient to deliver project {project_id}'}), 200
    else:
        return jsonify({'error': f'Assignments are not sufficient to deliver project {project_id}'}), 400


@app.route('/calculate_due_date', methods=['POST'])
def calculate_due_date():
    project_id = request.json['project_id']

    # Calculate the due date for the project
    with Session() as s:
        due_date = calculate_project_due_date(s, project_id)

    return jsonify({'due_date': str(due_date)}), 200


@app.route('/check_capacity', methods=['GET'])
def check_capacity():
    # Check the overall capacity for the team
    with Session() as s:
        total_capacity = get_total_capacity(s)
        over_capacity = [m.id for m in get_over_capacity_members(s)]

    return jsonify({'total_capacity': total_capacity, 'over_capacity': over_capacity}), 200


@app.route('/assignments', methods=['GET'])
def get_all_assignments():
    with Session() as s:
        resp = [a.json() for a in s.query(Assignment).all()]

    return jsonify(resp), 200


## PROJECTS

@app.route('/projects', methods=['GET'])
def get_all_projects():
    with Session() as s:
        resp = [proj.json() for proj in s.query(Project).all()]

    return jsonify(resp), 200


@app.route('/projects', methods=['POST'])
def create_project():
    name = request.json.get('name')
    effort_estimate = int(request.json.get('effort_estimate'))

    if not all([name, effort_estimate]):
        return jsonify({'error': 'Missing fields'}), 400

    # Check if member with the same email already exists
    with Session() as s:
        p = Project.add(s, name=name, effort_estimate=effort_estimate)
        s.commit()
    return jsonify({'message': 'Project created successfully'}), 201


@app.route('/projects/<int:member_id>', methods=['DELETE'])
def remove_project(project_id):
    with Session() as s:
        Project.remove_by_id(s, project_id)

    return jsonify({'message': 'Project deleted successfully'}), 200


@app.route('/skills', methods=['GET'])
def get_all_skills():
    with Session() as s:
        resp = [skill.json() for skill in s.query(Skillset).all()]

    return jsonify(resp), 200


if __name__ == '__main__':
    app.run()
