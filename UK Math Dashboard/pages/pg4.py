import dash
from dash import dcc, html

dash.register_page(__name__, name='School Characteristics')

layout = html.Div(
    [
        dcc.Markdown('## Education Statistics by School Characteristic')
    ]
)
