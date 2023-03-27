import plotly.express as px
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

from models.Member import Member
from . import ids


def render(app: Dash, data: dict) -> html.Div:
    @app.callback(
        Output(ids.MEMBER_BAR_CHART, "children"),
        [
            Input(ids.MEMBER_DROPDOWN, "value"),
        ],
    )
    def update_bar_chart(
        members_list: list[str]
    ) -> html.Div:
        df = data[Member.__name__]
        filtered_data = df[df[Member.name.name].isin(members_list)]

        # if filtered_data.shape[0] == 0:
        #     return html.Div("No data selected.", id=ids.BAR_CHART)

        fig = px.bar(
            filtered_data,
            x=Member.name.name,
            y=Member.capacity.name,
        )

        return html.Div(dcc.Graph(figure=fig), id=ids.MEMBER_BAR_CHART)

    return html.Div(id=ids.MEMBER_BAR_CHART)
