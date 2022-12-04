import dash
from dash import dcc, html, callback, Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc

dash.register_page(__name__, name='Regional Data')

# page 2 data
df = px.data.tips()

layout = html.Div(
    [
        dcc.Markdown('## UK Education System Heatmap')
    ]
)


@callback(
    Output('bar-fig', 'figure'),
    Input('day-choice', 'value')
)
def update_graph(value):
    dff = df[df.day==value]
    fig = px.bar(dff, x='smoker', y='total_bill')
    return fig