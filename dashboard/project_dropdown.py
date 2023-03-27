from dash import Dash, dcc, html
from dash.dependencies import Input, Output

from models.Project import Project
from . import ids


def render(app: Dash, data: dict) -> html.Div:
    # Loading data for members
    projects_list: list[str] = data[Project.__name__][Project.name.name].tolist()

    @app.callback(
        Output(ids.PROJECT_DROPDOWN, "value"),
        Input(ids.SELECT_ALL_PROJECTS_BUTTON, "n_clicks"),
    )
    def update_projects(_: int) -> list[str]:
        return projects_list

    return html.Div(
        children=[
            html.H6("Year"),
            dcc.Dropdown(
                id=ids.PROJECT_DROPDOWN,
                options=[{"label": project, "value": project} for project in projects_list],
                value=projects_list,
                multi=True,
            ),
            html.Button(
                className="dropdown-button",
                children=["Select all projects"],
                id=ids.SELECT_ALL_PROJECTS_BUTTON,
                n_clicks=0,
            ),
        ]
    )
