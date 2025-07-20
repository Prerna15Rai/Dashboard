import numpy as np
import pandas as pd
import plotly.graph_objects as go
import dash
import dash_html_components as html
from dash import html
import dash_core_components as dcc
from dash import dcc
from dash.dependencies import Input,Output
import plotly.express as px



# external CSS stylesheets
external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
        'crossorigin': 'anonymous'
    }
]

patients=pd.read_csv('IndividualDetails(1).csv')

total=patients.shape[0]
active=patients[patients['current_status']=='Hospitalized'].shape[0]
recovered=patients[patients['current_status']=='Recovered'].shape[0]
deaths=patients[patients['current_status']=='Deceased'].shape[0]

age = pd.read_csv('C:/Users/DELL/Downloads/corona/AgeGroupDetails (2).csv')
age['Percentage'] = age['Percentage'].str.replace('%', '').astype(float)

# Create a pie chart figure
fig1 = px.pie(age, values='Percentage', names='AgeGroup', title='')

ag2 = pd.read_csv('C:/Users/DELL/Downloads/corona/AgeGroupDetails(2).csv')
ag2['Percentage'] = ag2['Percentage'].str.replace('%', '').astype(float)

fig2 = px.line(ag2, x='AgeGroup', y='Percentage', title='')



app = dash.Dash(__name__,external_stylesheets=external_stylesheets)
server=app.server

options=[
    {'label':'All','value':'All'},
    {'label':'Hospitalized','value':'Hospitalized'},
    {'label':'Recovered','value':'Recovered'},
    {'label':'Deceased','value':'Deceased'},

]

app.layout=html.Div([
    html.H1("India's COVID-19 Situation Report",style={'color':'#fff','text-align':'center','font-size':'40px'}),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.H3("Total Cases",className='text-light',),
                    html.H4(total,className='text-light')
                ],className='card-body')
            ],className='card bg-danger')
        ],className='col-md-3'),
        html.Div([  html.Div([
                html.Div([
                    html.H3("Active Cases",className='text-light'),
                    html.H4(active,className='text-light')
                ],className='card-body')
            ],className='card bg-info')
        ],className='col-md-3'),

        html.Div([  html.Div([
                html.Div([
                    html.H3("Recovered Cases",className='text-light'),
                    html.H4(recovered,className='text-light')
                ],className='card-body')
            ],className='card bg-warning')
        ],className='col-md-3'),
        html.Div([  html.Div([
                html.Div([
                    html.H3("Deaths Cases",className='text-light'),
                    html.H4(deaths,className='text-light')
                ],className='card-body')
            ],className='card bg-success')
        ],className='col-md-3'),

    ],className='row'),
html.Div(style={'height': 20}),

    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.H1('Age Distribution by pic chart', style={'textAlign': 'center', 'fontFamily': 'Arial', 'fontSize': 24, 'color': '#337ab7'}),
                    dcc.Graph(id='age-distribution-graph-1', figure=fig1)
                ],className='cadr-body')
            ],className='card')
        ],className='col-md-6'),
    html.Div([
            html.Div([
                html.Div([
                       html.H1('Age Distribution by Line chart', style={'textAlign': 'center', 'fontFamily': 'Arial', 'fontSize': 24, 'color': '#337ab7'}),
                       dcc.Graph(figure=fig2)
                ],className='cadr-body')
            ],className='card')
        ],className='col-md-6'),
    ], className='row'),

html.Div(style={'height': 20}),

    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    dcc.Dropdown(id='picker',options=options, value='All', style={'fontSize':18}),
                    html.H1('State total count',
                            style={'textAlign': 'center', 'fontFamily': 'Arial', 'fontSize': 34, 'color': '#337ab7'}),
                    dcc.Graph(id='bar')
                ],className='card-body')
            ],className='card')
        ],className='col-md-12')
    ],className='row')
], className='container')

@app.callback(Output('bar','figure'), [Input('picker','value')]) #decorator function
def update_graph(type):

    if type=='All':
     pbar = patients['detected_state'].value_counts().reset_index()
     return{'data':[go.Bar(x=pbar['detected_state'], y=pbar['count'])],
             'layout':go.Layout(title='')}
    else:
        npat = patients[patients['current_status'] ==type]
        pbar = npat['detected_state'].value_counts().reset_index()
        return {'data': [go.Bar(x=pbar['detected_state'], y=pbar['count'])],
                'layout': go.Layout(title='')}

if __name__ == "__main__":
    app.run(debug=True)
