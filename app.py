import dash_bootstrap_components as dbc
from dash import Dash
from flask import Flask, render_template, redirect
from werkzeug import run_simple
from werkzeug.middleware.dispatcher import DispatcherMiddleware

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

@app.route('/dashboard')
def render_dashboard():
    return redirect('/dash')

# dash_app = Dash(__name__, server=app, url_base_pathname='/dashboard/', external_stylesheets=[dbc.themes.BOOTSTRAP])
# dash_app = Dash(__name__, server=app, url_base_pathname='/dashboard', external_stylesheets=[dbc.themes.BOOTSTRAP])
dash_app = Dash(__name__, server=app, external_stylesheets=[dbc.themes.BOOTSTRAP])


if __name__ == '__main__':
    print(app.url_map)
    app.run()
    # application = DispatcherMiddleware(app, {'/dash': dash_app.server})
    # run_simple('0.0.0.0', 8080, application, use_reloader=True, use_debugger=True)