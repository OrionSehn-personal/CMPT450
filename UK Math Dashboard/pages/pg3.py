import dash
from dash import dcc, html

dash.register_page(__name__, name='Student Characteristics')

layout = html.Div(
    [
        dcc.Markdown('## Education Statistics by Student Characteristic')
    ]
)