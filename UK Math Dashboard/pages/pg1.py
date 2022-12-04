import dash
from dash import dcc, html, callback, Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import plotly.io as pio
import pandas as pd
pio.templates.default = "simple_white"

dash.register_page(__name__, path='/', name='Overview') # '/' is home page

# chart one
figchart1 = go.Figure(
    data=[go.Scatter(y=[70, 75, 75, 79, 76.33, 73.66, 71], x=[2016, 2017, 2018, 2019, 2020, 2021, 2022])],
    layout=go.Layout(
        title=go.layout.Title(text="Percentage of pupils meeting expected standard in math")
        )
    )

figchart1.update_layout(
    xaxis_title="Data Source: Key stage 2 attainment: National headlines (England, all schools)",
    height=530,
    title={
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font_color': '#5E5E5E',
        }
    )

dot_opacity= [1, 1, 1, 1, 0, 0, 1]

figchart1.update_xaxes(title_font=dict(size=12, color='#A4A5A5'), linecolor='#7D7D7D', ticks="", color='#7D7D7D')
figchart1.update_yaxes(linecolor='#7D7D7D', ticks="", color='#7D7D7D', range=[65, 85])
figchart1.update_traces(line=dict(color="#356CB0", width=3), marker=dict(size=10, opacity=dot_opacity))


# chart two
figchart2 = go.Figure(
    data=[go.Scatter(
        y=[3.43, 3.23, 3.16, 3.15, 3.10, 3.03, 3.00, 2.90, 2.91, 3.01, 3.11, 3.21], 
        x=[2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022])
        ],
    layout=go.Layout(
        title=go.layout.Title(text="Disadvantaged gap index")
        )
    )

figchart2.update_layout(
    xaxis_title="Data Source: Key stage 2 disadvantage gap index (England, state-funded schools)",
    height=530,
    title={
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font_color': "#5E5E5E",
        }
    )

dot_opacity= [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1]

figchart2.update_xaxes(title_font=dict(size=12, color='#A4A5A5'), linecolor='#7D7D7D', ticks="", color='#7D7D7D')
figchart2.update_yaxes(linecolor='#7D7D7D', ticks="", color='#7D7D7D', range=[2.6, 3.6])
figchart2.update_traces(line=dict(color="#356CB0", width=3), marker=dict(size=10, opacity=dot_opacity))

# chart three

# science
figchart3 = go.Figure(
    data=[go.Scatter(
        y=[81, 82, 82, 83, 81.7, 80.4, 79], 
        x=[2016, 2017, 2018, 2019, 2020, 2021, 2022], 
        name="Science", 
        line=dict(color="#EE8636")
        )
    ],
    layout=go.Layout(
        title=go.layout.Title(text="Percentage of pupils meeting expected standard by subject")
        )
    )

# math
figchart3.add_trace(
    go.Scatter(
        y=[70, 75, 75, 79, 76.33, 73.66, 71], 
        x=[2016, 2017, 2018, 2019, 2020, 2021, 2022], 
        name="Math",
        line=dict(color="#356CB0")
        )
    )

# writing
figchart3.add_trace(
    go.Scatter(
        y=[74, 76, 78, 78, 75, 72, 69], 
        x=[2016, 2017, 2018, 2019, 2020, 2021, 2022], 
        name="Writing",
        line=dict(color="#529E3E")
        )
    )

# grammar
figchart3.add_trace(
    go.Scatter(
        y=[73, 77, 78, 78, 76, 74, 72], 
        x=[2016, 2017, 2018, 2019, 2020, 2021, 2022], 
        name="Grammar", 
        line=dict(color="#7D7D7D"),
        visible='legendonly'
        )
    )

figchart3.update_layout(
    xaxis_title="Data Source: Key stage 2 attainment: National headlines (England, all schools)",
    height=530,
    title={
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font_color': "#5E5E5E",
        }
    )

figchart3.update_xaxes(title_font=dict(size=12, color='#A4A5A5'), linecolor='#7D7D7D', ticks="", color='#7D7D7D')
figchart3.update_yaxes(linecolor='#7D7D7D', ticks="", color='#7D7D7D', range=[65, 85])
figchart3.update_traces(line=dict(width=3), marker=dict(opacity=0))

# chart four

figchart4 = go.Figure(
    data=[
        go.Bar(
            name='Boys', 
            x=["Meeting Expected Standard", "Reaching Higher Standard", "Not Meeting Expected Standard"],
            y=[-5.2, -3, 3.8],
            text=['-5.2%', '-3%', '3.8%'],
            textposition='auto',
            marker_color="#356CB0"
            ),
        go.Bar(
            name='Girls', 
            x=["Meeting Expected Standard", "Reaching Higher Standard", "Not Meeting Expected Standard"],
            y=[-8.1, -3.3, 6.6],
            text=['-8.1%', '-3.3%', '6.6%'],
            textposition='auto',
            marker_color="#529E3E"
            )
        ],
    layout=go.Layout(
        title=go.layout.Title(text="Percentage Change in Math Scores by Gender")
        )
    )

figchart4.update_layout(
    xaxis_title="Data Source: Key stage 2 attainment by pupil characteristics (England, all schools)",
    height=516,
    barmode='group',
    title={
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font_color': '#5E5E5E',
        }
    )

figchart4.update_xaxes(
    title_font=dict(size=12, 
    color='#A4A5A5'), 
    linecolor='#7D7D7D', 
    ticks="", 
    color='#7D7D7D',
    tickmode='array',
    tickvals=[0,1,2,3],
    ticktext=["Meeting Expected</br></br>Standard", "Reaching Higher</br></br>Standard", "Not Meeting</br></br>Expected Standard"]
    )
figchart4.update_yaxes(linecolor='#7D7D7D', ticks="", ticksuffix = "%", color='#7D7D7D', range=[-9, 7])


layout = html.Div(
    [
        dbc.Row(
            [
                html.Div(
                    [
                        html.Div('Education Statistics Overview', 
                        className="title"),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Div("Percentage of pupils meeting expected standards in math is down",
                                        className="figure-text1"
                                        ),
                                        html.Div("-8%",
                                        className="figure-text2"
                                        )
                                    ], className="figures-box-top"
                                ),
                            html.Div(
                                    [
                                        html.Div("Percentage of boys not reaching expected standards in math is up",
                                        className="figure-text1"
                                        ),
                                        html.Div("+3.8%",
                                        className="figure-text2"
                                        )
                                    ], className="figures-box-bottom"
                                )
                            ], className="figures-group"
                        ),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Div("Percentage of boys meeting expected standards in math is down",
                                        className="figure-text1"
                                        ),
                                        html.Div("-5.2%",
                                        className="figure-text2"
                                        )
                                    ], className="figures-box-top"
                                ),
                            html.Div(
                                    [
                                        html.Div("Percentage of girls not reaching expected standards in math is up",
                                        className="figure-text1"
                                        ),
                                        html.Div("+6.6%",
                                        className="figure-text2"
                                        )
                                    ], className="figures-box-bottom"
                                )
                            ], className="figures-group"
                        ),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Div("Percentage of girls meeting expected standards in math is down",
                                        className="figure-text1"
                                        ),
                                        html.Div("-8.1%",
                                        className="figure-text2"
                                        )
                                    ], className="figures-box-top"
                                ),
                            html.Div(
                                    [
                                        html.Div("Disadvantage gap index is up compared to non-disadvantaged pupils",
                                        className="figure-text1"
                                        ),
                                        html.Div("+10%",
                                        className="figure-text2"
                                        )
                                    ], className="figures-box-bottom"
                                )
                            ], className="figures-group"
                        ),
                        html.Div("* When compared to 2019 levels",
                        className="text3"
                        ),
                        html.Div("* No assessments were conducted in 2020 or 2021 (due to school closures)",
                        className="text3"
                        )
                    ]
                )
            ]
        ),
        dbc.Row(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                dcc.Graph(
                                    id='g1', 
                                    figure=figchart1
                                )
                            ], className="chart"
                        ),
                        html.Div(
                            [
                                dcc.Graph(
                                    id='g2', 
                                    figure=figchart3
                                ),
                            ], className="chart"
                        ),
                    ], className="charts"
                )
            ]
        ),
        dbc.Row(
            [
                html.Div(
                    [
                        html.Div(
                            [
                                dcc.Graph(
                                    id='g3', 
                                    figure=figchart2
                                )
                            ], className="chart"
                        ),
                        html.Div(
                            [
                                dcc.Graph(
                                    id='g4', 
                                    figure=figchart4
                                )
                            ], className="bar-graph"
                        ),
                    ],
                )
            ]
        )
    ]
)

