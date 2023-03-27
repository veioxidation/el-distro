import dash_bootstrap_components as dbc
import dash_html_components as html
from dash import Dash

from dashboard import member_dropdown, member_bar_chart, project_gantt_chart, project_dropdown


# def create_layout(app: Dash, data: pd.DataFrame) -> html.Div:
#     return html.Div(
#         className="app-div",
#         children=[
#             html.H1(app.title),
#             html.Hr(),
#             html.Div(
#                 className="dropdown-container",
#                 children=[
#                     year_dropdown.render(app, data),
#                     month_dropdown.render(app, data),
#                     category_dropdown.render(app, data),
#                 ],
#             ),
#             bar_chart.render(app, data),
#             pie_chart.render(app, data),
#         ],
#     )


def create_layout(app: Dash, data: dict):
    return html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(html.H3("Team Capacity Dashboard"), className="mb-4 mt-4")
                ]
            ),
            dbc.Row(
                [
                    html.Div(
                        className='dropdown-container',
                        children=[
                            member_dropdown.render(app, data),
                            project_dropdown.render(app, data)
                        ]
                    ),


                    dbc.Col(
                        [
                            member_bar_chart.render(app, data),
                        ],
                    ),
                    dbc.Col(
                        [
                            project_gantt_chart.render(app, data),

                        ],
                    ),
                    # dbc.Col(
                    #     [
                    #         # dcc.Graph(id="gantt-chart", className="mb-4"),
                    #     ],
                    #     width=6,
                    # ),
                ]
            ),
            # dbc.Row(
            #     [
            #         dbc.Col(
            #             [
            #                 html.H4("Free Capacity for Today"),
            #                 html.Table(id="free-capacity-table", className="mb-4"),
            #             ]
            #         )
            #     ]
            # ),
        ]
    )