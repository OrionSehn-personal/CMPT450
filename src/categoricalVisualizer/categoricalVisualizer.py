
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
def get_figure(file, year, categories, sub_categories, metric, gender, chart_type):
     df = px.data.iris() 
     default = px.scatter(df,title = "Default, override later", x="sepal_width", y="sepal_length", color="species")
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
                chart_title = f"{trim_dropdown_option(metric)} by year" if year == "all" else f"{trim_dropdown_option(metric)} for Academic Year: {year}"
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
        placeholder='Select a Year...',
        style={"display": "none"}
        ),
    dcc.Dropdown(
        id='category-selector', 
        placeholder="Select a category...",
        style={'display': 'none'},
        multi=True
        ),
    dcc.Dropdown(
        id='sub-category-selector',
        placeholder="Select a sub-category...",
        style={'display': 'none'},
        multi=True
    ),
    dcc.Dropdown(
        id='metric-selector',
        placeholder="Select a metric...",
        style={'display': 'none'}
        ),  
    dcc.RadioItems(
        id='gender-selector',
        options=[
            {'label': "All", 'value': "Total"},
            {'label': "Male", 'value': "Boys"},
            {'label': "Female", 'value': "Girls"},
            ],
        value='Total',
        style={'display': 'block'},
        inline=True
        ),
    dcc.RadioItems(
        id='chart-type-selector',
        options=[
            {'label': "Line Chart", 'value': "line"},
            {'label': "Bar Chart", 'value': "bar"},
            ],
        value='bar',
        inline=True,
        style={'display': 'block'}
    )

])

#--------------------------------------------------------------------------------------------------------
# callbacks
#--------------------------------------------------------------------------------------------------------

# Callback to show file description
@app.callback(
    [Output('file-summary', 'value'), 
     ],
    Input('file-selector', 'value')
    )
def populate_file_description(value):
    if value == None:
        return [""]

    return [guidance[value]["summary"]]

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
    def update_sub_category_selector_options(file, categories):
        if value is None:
            return []
        else:
            return get_sub_category_options(file, categories)
# Callback to update the category options visibility
@app.callback(
    Output('category-selector', 'style'),
    Input('year-selector', 'value')
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
     Input('metric-selector', 'value'),
     Input('gender-selector', 'value'),
     Input('chart-type-selector', 'value')
    ]
    
    )
def update_graph(file, year, categories, sub_categories, metric, gender, chart_type):
    return get_figure(file, year, categories, sub_categories, metric, gender, chart_type)
#---------------------------------------------------------------------------------------------------------
# Run the app
#---------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
