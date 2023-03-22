import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from dash import html
from dash import dcc
from dash.dependencies import Input, Output

data = pd.DataFrame({
    'Task': ['Task 1', 'Task 2', 'Task 3'],
    'Start': ['2022-01-01', '2022-01-05', '2022-01-10'],
    'Finish': ['2022-01-10', '2022-01-15', '2022-01-20'],
    'Capacity': [50, 70, 80]
})

fig = px.timeline(data, x_start="Start", x_end="Finish", y="Task")
fig.update_yaxes(autorange="reversed")


timeline = go.Figure()
timeline.add_trace(go.Scatter(x=data['Start'], y=data['Capacity'], name='Capacity'))
timeline.update_layout(title='Team Capacity Timeline', xaxis_title='Date', yaxis_title='Capacity')


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    html.H1('Team Capacity Dashboard'),
    dcc.Graph(id='gantt', figure=fig),
    dcc.Graph(id='timeline', figure=timeline)
])

if __name__ == '__main__':
    app.run_server(debug=True)
