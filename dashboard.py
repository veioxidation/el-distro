import dash_bootstrap_components as dbc
import dash_html_components as html
import pandas as pd
import plotly.express as px
from dash import html, Dash
from dash.dependencies import Input, Output

from app import app
from dashboard import member_dropdown
from dashboard.load_data import load_data

dash_app = Dash(__name__, server=app, url_base_pathname='/dashboard/', external_stylesheets=[dbc.themes.BOOTSTRAP])


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
                            member_dropdown.render(app, data)
                        ]
                    ),

                    # dbc.Col(
                    #     [
                    #         dcc.Graph(id="total-capacity-chart", className="mb-4"),
                    #     ],
                    #     width=6,
                    # ),
                    # dbc.Col(
                    #     [
                    #         dcc.Graph(id="gantt-chart", className="mb-4"),
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


# dash_app.layout = create_layout


# @app.callback(
#     Output("total-capacity-chart", "figure"),
#     Input("your_input_id", "value"),  # Replace this with the proper input for filtering your data
# )
# def update_total_capacity_chart(input_value):
#     # Replace this section with your logic to filter and process your data based on the input
#     df = pd.DataFrame()  # Your filtered and processed data
#     fig = px.line(df, x="date", y="total_capacity", title="Total Capacity Over Time")
#     return fig
#
#
# @app.callback(
#     Output("gantt-chart", "figure"),
#     Input("your_input_id", "value"),  # Replace this with the proper input for filtering your data
# )
# def update_gantt_chart(input_value):
#     # Replace this section with your logic to filter and process your data based on the input
#     df = pd.DataFrame()  # Your filtered and processed data
#     fig = px.timeline(df, x_start='start_date', x_end='end_date', y='member', color='project',
#                       title='Gantt Chart of Projects')
#     fig.update_yaxes(autorange="reversed")
#     return fig


# @app.callback(
#     Output("free-capacity-table", "children"),
#     Input("your_input_id", "value"),  # Replace this with the proper input for filtering your data
# )
# def update_free_capacity_table(input_value):
#     # Replace this section with your logic to filter and process your data based on the input
#     data = []  # Your filtered and processed data as a list of dictionaries
#
#     table_header = [
#         html.Thead(html.Tr([html.Th("Member"), html.Th("Free Capacity Today")]))
#     ]
#     rows = [html.Tr([html.Td(item["member"]), html.Td(item["free_capacity"])]) for item in data]
#     table_body = [html.Tbody(rows)]
#
#     return dbc.Table(table_header + table_body, bordered=True, striped=True, hover=True)


if __name__ == '__main__':
    print(dash_app.server.url_map)

    dash_app.title = "Distro"
    dash_app.layout = create_layout(app=dash_app, data=load_data())
    dash_app.run()
