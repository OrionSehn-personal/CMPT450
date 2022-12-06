import dash
from dash import dcc, html, callback, Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
import json
import pandas as pd
import pickle
from flask_caching import Cache

dash.register_page(__name__, name='Regional Data')


layout = html.Div(
    [
        dcc.Markdown('## UK Education System Heatmap')
    ]
)
cache = Cache(dash.get_app().server, config={
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': 'cache'
})

@cache.memoize()
def horizontal_total_students(df):
    '''
    Plot a horizontal bar chart of the number of students who achieved expected standard in maths in each local authority
    '''

    df = df[df["geographic_level"] == "Local authority"]
    df = df[df["pt_mat_met_expected_standard"] != "c"]

    df = df[df["pt_mat_met_expected_standard"] != "x"]
    df = df[df["gender"] == "Total"]

    df["pt_mat_met_expected_standard"] = df["pt_mat_met_expected_standard"].astype(float)
    df = df.sort_values(by=["time_period", "pt_mat_met_expected_standard"], ascending=True)
    fig = px.bar(df,
        x="pt_mat_met_expected_standard", 
        y="la_name", 
        orientation='h', 
        title=None, 
        width=400, 
        height=600, 
        labels={"pt_mat_met_expected_standard":"% Passing", "la_name": "Local Authority"}, 
        color= "pt_mat_met_expected_standard", 
        color_continuous_scale="Hot_r", 
        range_color=[55,90], 
        animation_frame="time_period"
        )

    fig.update(layout_coloraxis_showscale=False)
    fig.update_yaxes(visible=False, showticklabels=False)
    fig.update_xaxes(range=[0,100])
    fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 1000

    return fig

@cache.memoize()
def plot_animation_map(df, authorities, column):
    '''
    generate an animation of the UK with a colour scale based on the values in the column

    :param df: dataframe containing the data to be plotted
    :param authorities: geojson containing the boundaries of the local authorities
    :param column: the column in the dataframe to be plotted
    :param title: the title of the plot
    :return: None

    '''


    df = df[df["geographic_level"] == "Local authority"]
    df = df[df["geographic_level"] == "Local authority"]
    df = df[df["gender"] == "Total"]
    df = df[df[column] != "c"]
    df = df[df[column] != "x"]
    df[column] = df[column].astype(float)
    df["% Passing"] = df[column]

    fig = px.choropleth_mapbox(
    df,
    geojson=authorities,
    locations='la_name',
    featureidkey="properties.CTYUA21NM",
    color_continuous_scale="Hot_r",
    mapbox_style="carto-positron",
    center={"lat": 53, "lon": -1.5},
    zoom=4.5,
    range_color=(55,90),
    labels=None,
    opacity=0.5,
    title=None,
    color="% Passing",
    animation_frame="time_period",
    width=800,
    height=550)
    fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 1000
    return fig

with open(r'..\src\assets\fig.pickle', 'rb') as f:
    fig1 = pickle.load(f)


df = pd.read_csv(r'..\data\ks2_regional_and_local_authority_2016_to_2022_provisional.csv', dtype={'la_name': str})

fig2 = horizontal_total_students(df)

layout = html.Div(className='row', children=[
    html.H1("Educational Progress Based on Location over Time"),
    html.Div(children=[
        dcc.Graph(id="graph1", style={'display': 'inline-block'}, figure=fig1),
        dcc.Graph(id="graph2", style={'display': 'inline-block'}, figure=fig2),
    ])
])