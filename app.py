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


if __name__ == '__main__':
    print(app.url_map)
    app.run()
