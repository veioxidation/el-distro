import plotly.express as px
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

from models.Member import Member
from models.Project import Project
from . import ids


def render(app: Dash, data: dict) -> html.Div:
    @app.callback(
        Output(ids.PROJECT_GANTT_CHART, "children"),
        [
            Input(ids.PROJECT_DROPDOWN, "value"),
        ],
    )
    def update_gantt_chart(
        project_list: list[str]
    ) -> html.Div:
        df = data[Project.__name__]
        filtered_data = df[df[Project.name.name].isin(project_list)]

        fig = px.timeline(
            filtered_data,
            y=Project.name.name,
            x_start=Project.start_date.name,
            x_end=Project.due_date.name,
        )
        fig.update_yaxes(autorange="reversed")  # otherwise tasks are listed from the bottom up

        return html.Div(dcc.Graph(figure=fig), id=ids.PROJECT_GANTT_CHART)

    return html.Div(id=ids.PROJECT_GANTT_CHART)
