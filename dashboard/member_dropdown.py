import pandas as pd
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

from models.Member import Member
from . import ids


def render(app: Dash, data: dict) -> html.Div:

    # Loading data for members
    members: list[str] = data[Member.__name__][Member.name.name].tolist()

    @app.callback(
        Output(ids.MEMBER_DROPDOWN, "value"),
        Input(ids.SELECT_ALL_MEMBERS_BUTTON, "n_clicks"),
    )
    def select_all_years(_: int) -> list[str]:
        return members

    return html.Div(
        children=[
            html.H6("Year"),
            dcc.Dropdown(
                id=ids.MEMBER_DROPDOWN,
                options=[{"label": member, "value": member} for member in members],
                value=members,
                multi=True,
            ),
            html.Button(
                className="dropdown-button",
                children=["Select all members"],
                id=ids.SELECT_ALL_MEMBERS_BUTTON,
                n_clicks=0,
            ),
        ]
    )
