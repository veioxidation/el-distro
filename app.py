from flask import Flask, render_template

from create_engine import DB_URI
from routes.assignments import assignments_bp
from routes.members import members_bp
from routes.projects import projects_bp
from routes.skills import skills_bp

app = Flask(__name__)

# Configuration for the database
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# from app_members import members_interface
#
# app.register_blueprint(members_interface)

app.register_blueprint(members_bp)
app.register_blueprint(projects_bp)
app.register_blueprint(skills_bp)
app.register_blueprint(assignments_bp)


@app.route('/')
def index():
    return render_template('base.html')


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


## PROJECTS


if __name__ == '__main__':
    print(app.url_map)
    app.run()
