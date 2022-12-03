from tkinter import Place
from dash import Dash, dcc, html, callback_context as ctx
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
import json

app = Dash(__name__)

dataframes = {}
dataframe_name = None
guidance = json.loads(open("data/data-guidance.json", "r").read())

#--------------------------------------------------------------------------------------------------------
# Functions
#--------------------------------------------------------------------------------------------------------
def trim_dropdown_option(input):
    try: 
        return input.replace(".csv", "")\
            .replace("_", " ")\
            .title() 
    except:  
        return input 

# Load CSV names for data folder
def load_csv_names():
    import os
    csv_names = []
    for file in os.listdir("data"):
        if file.endswith(".csv") and "pupil_characteristic" in file:
            csv_names.append({"label": trim_dropdown_option(file), "value": file})
    return csv_names

# Top-level category handler is based on filename loaded
def get_category_options(filename):
    match filename:
        case "ks2_national_pupil_characteristics_2016_to_2022_provisional.csv":
            return [
                {"label": trim_dropdown_option(col), "value": col} 
                for col in dataframes[
                    "ks2_national_pupil_characteristics_2016_to_2022_provisional.csv"
                    ]["characteristic_group"].unique()]
        case _:
            return []
        
# get sub category options based on filename and category
def get_sub_category_options(filename, category):
    match filename:
        case "ks2_national_pupil_characteristics_2016_to_2022_provisional.csv":
            return [
                {"label": trim_dropdown_option(col), "value": col} 
                for col in dataframes[
                    "ks2_national_pupil_characteristics_2016_to_2022_provisional.csv"
                    ].query(
                        f"characteristic_group == '{category}'"
                        )["characteristic"].unique()]
            
        case _:
            return []
        
# figure handler
def get_figure(file, year, category, sub_category, metric):
     df = px.data.iris() 
     default = px.scatter(df,title = "Default, override later", x="sepal_width", y="sepal_length", color="species")
     if None not in [file, year, category, sub_category, metric]:
        match file:
            case "ks2_national_pupil_characteristics_2016_to_2022_provisional.csv":
                df = dataframes[
                    "ks2_national_pupil_characteristics_2016_to_2022_provisional.csv"
                    ].query(
                        f"characteristic_group == '{category}' \
                        and characteristic == '{sub_category}' \
                        and time_period == {year}"
                        )
                
                fig = px.bar(
                    df, 
                    x="time_period", 
                    y="pt_mat_working_below_assessment", 
                    color="characteristic", 
                    title=f"{sub_category} by {year}"
                    )
                return fig
            case _:
                return default
     else:
        return default

# get metric options from file
def get_metric_options(filename):
    match filename:
        case "ks2_national_pupil_characteristics_2016_to_2022_provisional.csv":
            return [
                {"label": trim_dropdown_option(col), "value": col} 
                for col in dataframes[
                    "ks2_national_pupil_characteristics_2016_to_2022_provisional.csv"
                    ].columns if (col.startswith("pt_") or col.startswith("t_"))]
        case _:
            return []
#--------------------------------------------------------------------------------------------------------
# Iniitalization
#--------------------------------------------------------------------------------------------------------

# Load CSV names
filenames = load_csv_names()

# Load data frames
for filename in filenames:
    dataframes[filename["value"]] = pd.read_csv("data/" + filename["value"])
    

#--------------------------------------------------------------------------------------------------------
# layout
#--------------------------------------------------------------------------------------------------------
app.layout = html.Div([
    dcc.Graph(id='graph'),
    dcc.Dropdown(
        id='file-selector',
        options=filenames,
        placeholder="Select a Data Set...",
        ),
    dcc.Dropdown(
        id='year-selector' ,
        placeholder='Select a Year... (All by default)',
        style={"display": "none"}
        ),
    dcc.Dropdown(
        id='category-selector', 
        placeholder="Select a category...",
        style={'display': 'none'}
        ),
    dcc.Dropdown(
        id='sub-category-selector',
        placeholder="Select a sub-category...",
        style={'display': 'none'}
    ),
    dcc.Dropdown(
        id='metric-selector',
        placeholder="Select a metric...",
        style={'display': 'none'}
        ),  
])

#--------------------------------------------------------------------------------------------------------
# callbacks
#--------------------------------------------------------------------------------------------------------

# Callack to update the year selector visibility
@app.callback(
    Output('year-selector', 'style'),
    Input('file-selector', 'value')
    )
def update_year_selector_visibility(value):
    if value is None:
        return {"display": "none"}
    else:
        return {"display": "block"}

# callback to update the year selector options
@app.callback(
    Output('year-selector', 'options'),
    Input('file-selector', 'value')
    )
def update_year_selector_options(value):
    if value is None:
        return []
    else:
        return [{"label": "All available years", "value": "all"}] + [
            {"label": str(year)[0:4] + "-" + str(year)[4:], "value": year} 
            for year in dataframes[value]["time_period"].unique()]
        

    # callback to update the category selector visibility
    @app.callback(
        Output('category-selector', 'style'),
        Input('file-selector', 'value')
        )
    def update_category_selector_visibility(value):
        if value is None:
            return {"display": "none"}
        else:
            return {"display": "block"}

    # callback to update the category selector options
    @app.callback(
        Output('category-selector', 'options'),
        Input('file-selector', 'value')
        )
    def update_category_selector_options(value):
        if value is None:
            return []
        else:
            return get_category_options(value)

    # callback to update the sub-category selector visibility
    @app.callback(
        Output('sub-category-selector', 'style'),
        Input('file-selector', 'value')
        )
    def update_sub_category_selector_visibility(value):
        if value is None:
            return {"display": "none"}
        else:
            return {"display": "block"}

    # callback to update the sub-category selector options
    @app.callback(
        Output('sub-category-selector', 'options'),
        Input('file-selector', 'value'),
        Input('category-selector', 'value')
        )
    def update_sub_category_selector_options(value, category):
        if value is None:
            return []
        else:
            return get_sub_category_options(value, category)
# Callback to update the category options visibility
@app.callback(
    Output('category-selector', 'style'),
    Input('file-selector', 'value')
    )
def update_category_visibility(value):
    if value is None:
        return {'display': 'none'}
    return {'display': 'block'}

# Callback to update the category options
@app.callback(
    Output('category-selector', 'options'),
    Input('file-selector', 'value')
    )
def update_column_options(value):
    if value is None:
        return []
    return get_category_options(value)


# Callback to update the sub-category options visibility
@app.callback(
    Output('sub-category-selector', 'style'),
    Input('category-selector', 'value'),
    )
def update_sub_column_visibility(value):
    if value is None:
        return {'display': 'none'}
    return {'display': 'block'}

# Callback to update the sub-category options
@app.callback(
    Output('sub-category-selector', 'options'),
    [Input('category-selector', 'value'),
     Input('file-selector', 'value')]
    )
def update_sub_category_options(category, file):
    if category is None:
        return []
    if 'file-selector' in ctx.triggered:
        return []
    
    return get_sub_category_options(file, category)

# Callback to update the metric selector visibility and options
@app.callback(
    [Output('metric-selector', 'style'),
     Output('metric-selector', 'options')],
     [Input('sub-category-selector', 'value'),
      Input('file-selector', 'value')]
     )
def update_metric_selector(sub_category, file):
    if sub_category is None:
        return {'display': 'none'}, []
    if 'file-selector' in ctx.triggered:
        return {'display': 'none'}, []
    
    return {'display': 'block'}, get_metric_options(file)
     


# Callback to update the graph
@app.callback(
    Output('graph', 'figure'),
    [Input('file-selector', 'value'),
     Input('year-selector', 'value'),
     Input('category-selector', 'value'),
     Input('sub-category-selector', 'value'),
     Input('metric-selector', 'value')]
    
    )
def update_graph(file, year, category, sub_category, metric):
    return get_figure(file, year, category, sub_category, metric)
#---------------------------------------------------------------------------------------------------------
# Run the app
#---------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
