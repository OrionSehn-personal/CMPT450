# import dash
# from dash import dcc, html, callback, Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
import json
import pandas as pd
import pickle

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


def gen_pickle():
    authorities = json.load(open(r'..\data\Counties_and_Unitary_Authorities_(December_2021)_UK_BGC.geojson'))

    # Iterative over JSON
    for i in range(len(authorities["features"])):
        # Extract local authority name
        la = authorities["features"][i]['properties']['CTYUA21NM']
        # Assign the local authority name to a new 'id' property for later linking to dataframe
        authorities["features"][i]['id'] = la

    df = pd.read_csv(r'..\data\ks2_regional_and_local_authority_2016_to_2022_provisional.csv', dtype={'la_name': str})
    fig = plot_animation_map(df, authorities, "pt_mat_met_expected_standard")

    #write and pickle the figure
    with open('fig.pickle', 'wb') as f:
        pickle.dump(fig, f)


gen_pickle()
#read and unpickle the figure
# with open('fig.pickle', 'rb') as f:
#     fig = pickle.load(f)

# fig.show()

