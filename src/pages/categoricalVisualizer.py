import dash
from dash import dcc, html, callback_context as ctx, callback
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import json

dash.register_page(__name__, name='Student Characteristic')

dataframes = {}
dataframe_name = None
guidance = json.loads(open("../data/data-guidance.json", "r").read())

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
    for file in os.listdir("../data"):
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
def get_sub_category_options(filename, categories):
    match filename:
        case "ks2_national_pupil_characteristics_2016_to_2022_provisional.csv":
            return [
                {"label": trim_dropdown_option(col), "value": col} 
                for col in dataframes[
                    "ks2_national_pupil_characteristics_2016_to_2022_provisional.csv"
                    ].query(
                        f"characteristic_group in {categories}"
                        )["characteristic"].unique()]
            
        case _:
            return []
        
# figure handler
def get_figure(file, year, categories, sub_categories, metric, gender, chart_type, description):
    
     if None not in [file, year, categories, sub_categories, metric]:
        match file:
            case "ks2_national_pupil_characteristics_2016_to_2022_provisional.csv":
                query = f"characteristic_group in {categories} \
                        and characteristic in {sub_categories} \
                        and gender=='{gender}' \
                        and {metric}!='x'"
                        
                if year != "all":
                    query += f" and time_period=={year}"
                
                
                df = dataframes[
                    "ks2_national_pupil_characteristics_2016_to_2022_provisional.csv"
                    ].query(query)
                chart_title = f"{description} by year" if year == "all" else f"{description} for Academic Year: {year}"
                fig = None
                if chart_type == 'bar': 
                    fig = px.bar(
                        df, 
                        x="characteristic" if year!="all" else df.time_period.astype('string'),
                        y=metric,
                        barmode='group',
                        title=chart_title,
                        text_auto=True,
                        color='characteristic'
                    )
                    fig.update_xaxes(title_text="Year" if year=="all" else "Characteristic",
                                 type="category",
                                 
                                 )
                    fig.update_layout(
                        xaxis = dict(
                            tickmode = 'array',
                            tickvals = [201516, 201617, 201718, 201819, 201920, 202021, 202122],
                            ticktext = ['2015-16','2016-17', '2017-18', '2018-19', '2019-20', '2020-21', '2021-22']
                            )
                    )
                
                elif chart_type == 'line' and year == "all":
                    fig = px.line(
                        df,
                        x=df.time_period.astype('string'),
                        y=metric,
                        title=chart_title,
                        color="characteristic"
                        )
                    fig.update_xaxes(title_text="Year")
                    fig.update_layout(
                        xaxis = dict(
                            tickmode = 'array',
                            tickvals = [201617, 201718, 201819, 201920, 202021, 202122],
                            ticktext = ['2016-17', '2017-18', '2018-19', '2019-20', '2020-21', '2021-22']
                            )
                    )

                else:
                    fig = px.scatter(
                        df,
                        x="characteristic",
                        y=metric,
                        title=chart_title,
                        text=metric,
                        color="characteristic"
                        )
                    fig.update_traces(textposition='top center')
                    fig.update_xaxes(title_text="Characteristic")
                    
                fig.update_yaxes(type="linear", autotypenumbers='convert types', visible=False)
                return fig
            case _:
                return get_figure(
                        "ks2_national_pupil_characteristics_2016_to_2022_provisional.csv",
                        "all",
                        ['All pupils', 'Ethnic minor', 'First language'],
                        ['Total', 'Known or believed to be English'],
                        "pt_mat_met_higher_standard", 
                        "Total", 
                        "bar"
                    )
     else:
        return get_figure(
                        "ks2_national_pupil_characteristics_2016_to_2022_provisional.csv",
                        "all",
                        ['All pupils', 'Ethnic minor', 'First language'],
                        ['Total', 'Known or believed to be English'],
                        "pt_mat_met_higher_standard", 
                        "Total", 
                        "bar",
                        "Percentage met or exceeded Maths Standard"
                    )

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
    dataframes[filename["value"]] = pd.read_csv("../data/" + filename["value"])

#--------------------------------------------------------------------------------------------------------
# layout
#--------------------------------------------------------------------------------------------------------

layout = dbc.Container([
    html.Div([
        dcc.Markdown('## Education Statistics by Student Characteristic'),
        dcc.Graph(id='graph')]),
    dbc.Row([
        dbc.Col(
                dcc.Dropdown(
                    id='file-selector',
                    options=filenames,
                    placeholder="Select a Data Set...",
                    )
        ),
        dbc.Col(
                html.P(children="", id = 'file-selector-description')
            )]),
    dbc.Row([
        dbc.Col(
            dcc.Dropdown(
                id='year-selector' ,
                placeholder='Select a Year...',
                style={"display": "none"}
                ),
            ),
        dbc.Col(
                html.P(children="", id = 'year-description')
            )
        ]),
    dbc.Row([
        dbc.Col(
            dcc.Dropdown(
                id='category-selector', 
                placeholder="Select a category...",
                style={'display': 'none'},
                multi=True
                )
        ),
        dbc.Col(
                html.P(children="", id='category-selector-description')
            )
 
        ]),
    dbc.Row([
        dbc.Col(
            dcc.Dropdown(
                id='sub-category-selector',
                placeholder="Select a sub-category...",
                style={'display': 'none'},
                multi=True
            )
        ),
        dbc.Col(
                html.P(id = "sub-category-description", children="")
            )
    ]),
    dbc.Row([
        dbc.Col(
            dcc.Dropdown(
                id='metric-selector',
                placeholder="Select a metric...",
                style={'display': 'none'}
                )
        ),
        dbc.Col(
                html.P(id='metric-description', children ='')
            )
    ]),
    dbc.Row([
        dbc.Col([
            html.P("Select gender: "),
            dcc.RadioItems(
                id='gender-selector',
                options=[
                    {'label': " All_ ", 'value': "Total"},
                    {'label': " Male_ ", 'value': "Boys"},
                    {'label': " Female ", 'value': "Girls"},
                    ],
                value='Total'
                )
        ]),
        dbc.Col([
            html.P("Select chart type:"),
            dcc.RadioItems(
                id='chart-type-selector',
                options=[
                    {'label': " Line Chart_ ", 'value': "line"},
                    {'label': " Bar Chart ", 'value': "bar"},
                    ],
                value='bar'
            )
        ]),
        dbc.Col(),
        dbc.Col()
        ]),
        html.P(),
        html.P("Note: data was not widely collected during the 2019-20 and 2020-21 academic years due to covid"),
    ])  


#--------------------------------------------------------------------------------------------------------
# callbacks
#--------------------------------------------------------------------------------------------------------

# Callback to show file description
@callback(
    Output('file-selector-description', 'children'), 
    Input('file-selector', 'value')
    )
def populate_file_description(value):
    if value == None:
        return [""]

    return [guidance[value]["summary"]]

# Callback to populate category description
@callback(
    Output('category-selector-description', 'children'),
     Input('year-selector', 'value')
    )
def populate_category_description(file):
    if file == None:
        return ""
    else:
        return "The characteristic group(s) of children"

# Callback to update the metric description
@callback(
    Output('metric-description', 'children'),
    [Input('metric-selector', 'value'),
     Input('file-selector', 'value')]
    )
def populate_metric_description(value, filename):
    if value == None:
        return ""
    else:
        return guidance[filename][value]
# Callack to update the year selector visibility
@callback(
    [Output('year-selector', 'style'),
    Output('year-description', 'children')],
    Input('file-selector', 'value')
    )
def update_year_selector_visibility(value):
    if value is None:
        return {"display": "none"}, ""
    else:
        return {"display": "block"}, "Academic year"

# callback to update the year selector options
@callback(
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
        
# Callback to update the category options visibility
@callback(
    Output('category-selector', 'style'),
    Input('year-selector', 'value')
    )
def update_category_visibility(value):
    if value is None:
        return {'display': 'none'}
    return {'display': 'block'}

# Callback to update the category options
@callback(
    Output('category-selector', 'options'),
    Input('file-selector', 'value')
    )
def update_column_options(value):
    if value is None:
        return []
    return get_category_options(value)


# Callback to update the sub-category options visibility
@callback(
    [Output('sub-category-selector', 'style'),
     Output('sub-category-description', 'children')],
    Input('category-selector', 'value'),
    )
def update_sub_column_visibility(value):
    if value is None:
        return {'display': 'none'}, ""
    return {'display': 'block'}, "The Characteristic(s)"

# Callback to update the sub-category options
@callback(
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
@callback(
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
@callback(
    Output('graph', 'figure'),
    [Input('file-selector', 'value'),
     Input('year-selector', 'value'),
     Input('category-selector', 'value'),
     Input('sub-category-selector', 'value'),
     Input('metric-selector', 'value'),
     Input('gender-selector', 'value'),
     Input('chart-type-selector', 'value'),
     Input('metric-description', 'children')
    ]
    
    )
def update_graph(file, year, categories, sub_categories, metric, gender, chart_type, description):
    return get_figure(file, year, categories, sub_categories, metric, gender, chart_type, description)

