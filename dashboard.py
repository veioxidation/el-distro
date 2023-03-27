import dash_bootstrap_components as dbc
from dash import Dash

from dashboard.layout import create_layout
from dashboard.load_data import load_data

# dash_app = Dash(__name__, server=app, url_base_pathname='/dashboard/', external_stylesheets=[dbc.themes.BOOTSTRAP])
dash_app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])




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
