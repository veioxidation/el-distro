from flask import render_template, request, jsonify, Blueprint

from models.Project import Project
from models.db import Session

projects_bp = Blueprint('projects', __name__)


@projects_bp.route('/projects', methods=['GET'])
def projects():
    with Session() as s:
        projects = s.query(Project).all()
    return render_template('projects.html', projects=projects)


@projects_bp.route('/add_project', methods=['POST'])
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


@projects_bp.route('/delete_project/<int:project_id>', methods=['DELETE'])
def delete_project(project_id):
    with Session() as s:
        try:
            Project.remove_by_id(s, project_id)
            return jsonify(success=True), 200
        except Exception as e:
            return jsonify(success=False, error="Project not found"), 404
