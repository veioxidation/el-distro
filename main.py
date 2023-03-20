from flask import Flask, request, jsonify, render_template

from create_engine import DB_URI
from functions import *

# from flask_sqlalchemy import SQLAlchemy
from models.Project import Project

app = Flask(__name__)

# Configuration for the database
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# db = SQLAlchemy(app)
# db.init_app(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/members')
def members():
    return render_template('members.html')


@app.route('/assign_member', methods=['POST'])
def assign_member():
    project_id = request.json['project_id']
    member_id = request.json['member_id']
    capacity = request.json['capacity']

    # Assign the member to the project
    assignment = assign_member_to_project(project_id, member_id, capacity)

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
    unassign_member_from_project(project_id, member_id)

    return jsonify({'message': f'Member {member_id} unassigned from project {project_id}'}), 200


@app.route('/change_capacity', methods=['POST'])
def change_capacity():
    project_id = request.json['project_id']
    member_id = request.json['member_id']
    new_capacity = request.json['new_capacity']

    # Change the capacity for the assignment
    change_assignment_capacity(project_id, member_id, new_capacity)

    return jsonify(
        {'message': f'Capacity for member {member_id} on project {project_id} changed to {new_capacity}'}), 200


@app.route('/check_assignments', methods=['POST'])
def check_assignments():
    project_id = request.json['project_id']

    # Check the assignments for the project
    assignments = get_assignments_for_project(project_id)
    estimated_effort = Project.query.filter_by(id=project_id).first().estimated_effort

    total_capacity = sum([a.capacity for a in assignments])

    if total_capacity >= estimated_effort:
        return jsonify({'message': f'Assignments are sufficient to deliver project {project_id}'}), 200
    else:
        return jsonify({'error': f'Assignments are not sufficient to deliver project {project_id}'}), 400


@app.route('/calculate_due_date', methods=['POST'])
def calculate_due_date():
    project_id = request.json['project_id']

    # Calculate the due date for the project
    due_date = calculate_project_due_date(project_id)

    return jsonify({'due_date': str(due_date)}), 200


@app.route('/check_capacity', methods=['GET'])
def check_capacity():
    # Check the overall capacity for the team
    total_capacity = get_total_capacity()
    over_capacity = [m.id for m in get_over_capacity_members()]

    return jsonify({'total_capacity': total_capacity, 'over_capacity': over_capacity}), 200


@app.route('/members', methods=['POST'])
def create_member():
    member_name = request.json.get('name')
    member_email = request.json.get('email')
    member_skills = request.json.get('skills')
    member_capacity = request.json.get('capacity')

    if not all([member_name, member_email, member_skills, member_capacity]):
        return jsonify({'error': 'Missing fields'}), 400

    # Check if member with the same email already exists
    add_new_member(name=member_name, email=member_email, skills=member_skills, capacity=member_capacity)
    return jsonify({'message': 'Member created successfully'}), 201


@app.route('/members/<int:member_id>', methods=['DELETE'])
def remove_member(member_id):
    remove_member_by_id(member_id)
    return jsonify({'message': 'Member deleted successfully'}), 200


if __name__ == '__main__':
    app.run()
