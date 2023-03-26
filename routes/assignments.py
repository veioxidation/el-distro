from flask import request, jsonify, render_template, Blueprint

from functions import assign_member_to_project
from models.Assignment import Assignment
from models.Member import Member
from models.Project import Project
from models.db import Session

assignments_bp = Blueprint('assignments', __name__)


@assignments_bp.route('/add_assignment', methods=['POST'])
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


@assignments_bp.route('/delete_assignment/<int:assignment_id>', methods=['DELETE'])
def delete_assignment(assignment_id):
    with Session() as s:
        try:
            Assignment.remove_by_id(s, assignment_id)
            return jsonify(success=True), 200
        except Exception as e:
            return jsonify(success=False, error="Assignment not found"), 404


@assignments_bp.route('/assignments', methods=['GET'])
def assignments():
    with Session() as s:
        projects = s.query(Project).all()
        assignments = s.query(Assignment).all()
        members = s.query(Member).all()
        return render_template('assignments.html', projects=projects, assignments=assignments, members=members)
