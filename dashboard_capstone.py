# Import required libraries
import pandas as pd
import dash
from dash import dcc,html
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
sites= [{'label':'All sites','value':'all'}]
for site in pd.unique(spacex_df['Launch Site']):
    sites.append({'label':site, 'value':site})

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                             options=sites,
                                             value='all',
                                             placeholder= 'Select a Launch Site',
                                             searchable=True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',min= min_payload,max=max_payload,
                                                step=1000,value=[min_payload,max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart'))])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart',component_property='figure'),
              Input(component_id='site-dropdown',component_property= 'value'))

def pie_chart_maker(selected_site):
    if selected_site == 'all':
        dfg= spacex_df[spacex_df['class']==1]['Launch Site'].value_counts()
        fig= px.pie(values= dfg.values,names= dfg.index,
                    title='Per site contribution to successful attempts')
        return fig
    else:
        dfg= spacex_df[spacex_df['Launch Site']==selected_site]['class'].value_counts().sort_index()
        fig= px.pie(values= dfg.values,names= dfg.index,
                    color=dfg.index,color_discrete_map= {0:'red',1:'green'},
                    title='Success rate for site: {}'.format(selected_site))
        return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output

@app.callback(Output(component_id='success-payload-scatter-chart',component_property='figure'),
              [Input(component_id='site-dropdown',component_property='value'),
              Input(component_id='payload-slider',component_property='value')])

def scatter_chart_maker(selected_site,selected_payload):
    print(selected_payload)
    payload_df= spacex_df[(spacex_df['Payload Mass (kg)']>=selected_payload[0]) & (spacex_df['Payload Mass (kg)']<=selected_payload[1])]
    if selected_site== 'all':
        fig= px.scatter(payload_df,x='Payload Mass (kg)',y='class',
                        color='Booster Version Category',
                        title= 'Payload vs success for all sites')
        return fig

    else:
        dfg= payload_df[payload_df['Launch Site']==selected_site]
        fig= px.scatter(dfg,x='Payload Mass (kg)',y='class',
                        color= 'Booster Version Category',
                        title='Payload vs success for site: {}'.format(selected_site))

        return fig


# Run the app
if __name__ == '__main__':
    app.run_server()