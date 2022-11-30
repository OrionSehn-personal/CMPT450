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
        return input.replace("_", " ").replace(".csv", "").title() 
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
            print("default")
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
    dcc.Dropdown(
        id='file-selector',
        options=filenames,
        placeholder="Select a Data Set...",
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
    )
])

#--------------------------------------------------------------------------------------------------------
# callbacks
#--------------------------------------------------------------------------------------------------------

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

#---------------------------------------------------------------------------------------------------------
# Run the app
#---------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
