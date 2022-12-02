import dash
from dash import dcc, html, callback, Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
import json
import pandas as pd


dash.register_page(__name__, name='Regional Data')

# page 2 data
df = px.data.tips()

layout = html.Div(
    [
        dcc.Markdown('## UK Education System Heatmap')
    ]
)

def plot_map(df, authorities, column, title, date = 202122):
    '''
    generate a map of the UK with a colour scale based on the values in the column

    :param df: dataframe containing the data to be plotted
    :param authorities: geojson containing the boundaries of the local authorities
    :param column: the column in the dataframe to be plotted
    :param title: the title of the plot
    :return: None

    '''

    df = df[df["geographic_level"] == "Local authority"]
    df = df[df["gender"] == "Total"]
    df = df[df[column] != "c"]
    df = df[df[column] != "x"]
    df[column] = df[column].astype(float)

    sdf = df[df["time_period"] == date]

    fig = px.choropleth_mapbox(
        sdf,
        geojson=authorities,
        locations='la_name',
        featureidkey="properties.CTYUA21NM",
        color_continuous_scale="Hot_r",
        mapbox_style="carto-positron",
        center={"lat": 53, "lon": -1.5},
        zoom=5.5,
        range_color=(55,90),
        labels=None,
        opacity=0.5,
        title=title + str(date),
        color=column,
        width=500,
        height=500)

    return fig


def horizontal_total_students(df):
    '''
    Plot a horizontal bar chart of the number of students who achieved expected standard in maths in each local authority
    '''
    df = df[df["geographic_level"] == "Local authority"]
    # df = df[df["time_period"] == 201516]
    df = df[df["pt_mat_met_expected_standard"] != "c"]
    df = df[df["pt_mat_met_expected_standard"] != "x"]
    df = df[df["gender"] == "Total"]
    df["pt_mat_met_expected_standard"] = df["pt_mat_met_expected_standard"].astype(float)
    # df = df.head()
    df = df.sort_values(by=["time_period", "pt_mat_met_expected_standard"], ascending=True)
    # print(df)
    # print(list(df["pt_mat_met_expected_standard"]))   
    # df.to_csv("test.csv")
    fig = px.bar(df,
    x="pt_mat_met_expected_standard", 
    y="la_name", 
    orientation='h', 
    title="The number of students who achieved expected standard in maths in each local authority", 
    width=400, 
    height=600, 
    labels={"pt_mat_met_expected_standard":"Percentage of pupils meeting the expected standard in maths", "la_name": "Local Authority"}, 
    color= "pt_mat_met_expected_standard", 
    color_continuous_scale="Hot_r", 
    range_color=[55,90], 
    animation_frame="time_period")

    #make the graph less wide
    # fig.update_layout(showlegend=False)
    # fig.update_traces(showscale=False)
    fig.update(layout_coloraxis_showscale=False)
    fig.update_yaxes(visible=False, showticklabels=False)
    fig.update_xaxes(range=[0,100])
    fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 1000

    return fig


def plot_animation_map(df, authorities, column, title):
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

    fig = px.choropleth_mapbox(
    df,
    geojson=authorities,
    locations='la_name',
    featureidkey="properties.CTYUA21NM",
    color_continuous_scale="Hot_r",
    mapbox_style="carto-positron",
    center={"lat": 53, "lon": -1.5},
    zoom=5.5,
    range_color=(55,90),
    labels=None,
    opacity=0.5,
    title=title,
    color=column,
    animation_frame="time_period",
    width=500,
    height=500)
    fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 1000
    return fig


authorities = json.load(open(r'data\Counties_and_Unitary_Authorities_(December_2021)_UK_BGC.geojson'))

# Iterative over JSON
for i in range(len(authorities["features"])):
    # Extract local authority name
    la = authorities["features"][i]['properties']['CTYUA21NM']
    # Assign the local authority name to a new 'id' property for later linking to dataframe
    authorities["features"][i]['id'] = la

df = pd.read_csv(r'data\ks2_regional_and_local_authority_2016_to_2022_provisional.csv', dtype={'la_name': str})
fig1 = plot_animation_map(df, authorities, "pt_read_met_expected_standard", "Percentage of pupils reaching the higher standard in maths test")
fig2 = horizontal_total_students(df)

# layout = html.Div(children=[
#     html.Div(children=[
#         dcc.Graph(id="graph1",figure=fig1, style={'display': 'inline-block'}),
#         dcc.Graph(id="graph2", figure=fig2, style={'display': 'inline-block'})
#     ])
# ])


layout = html.Div(
    [
        dbc.Row(
            [
                dcc.Markdown('## Education Geographic Data Overview'),
                dcc.Graph(id="graph1",figure=fig1, style={'display': 'inline-block'}),

            ]
        ),
        dbc.Row(
            [
                dbc.Col(

                    [
                        dcc.Graph(id="graph2", figure=fig2, style={'display': 'inline-block'})
                    ], width=12

                )
            ]
        )
    ]
)
