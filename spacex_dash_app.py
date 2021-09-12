# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(id='site-dropdown',
                                             options=[{'label': 'All sites', 'value': 'All sites'},
                                                      {'label': 'CCAFS LC-40',
                                                                'value': 'CCAFS LC-40'},
                                                      {'label': 'CCAFS SLC-40',
                                                                'value': 'CCAFS SLC-40'},
                                                      {'label': 'KSC LC-39A',
                                                                'value': 'KSC LC-39A'},
                                                      {'label': 'VAFB SLC-4E',
                                                                'value': 'VAFB SLC-4E'},
                                                      ],
                                             value='All sites',
                                             placeholder='Select a Launch Site here',
                                             searchable=True),
                                # style={'width': '100%', 'align-items': 'center', 'display': 'block', 'justify-content': 'center',
                                # 'padding': '3px', 'text-align-last': 'center', 'font-size': '20px'}),
                                # style={'width': '80%', 'padding': '3px', 'font-size': '20px', 'text-align-last': 'center'}),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                # dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider', min=0, max=10000, step=1000,
                                                marks={
                                                    0: 0,
                                                    2500: 2500,
                                                    5000: 5000,
                                                    7500.65: 7500,
                                                    10000: 10000},
                                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(
                                    dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

sitesList = sorted(list(set(spacex_df['Launch Site'])))

# Add callback decorator
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
# Add computation to callback function and return pie
def get_pie(site_dropdown):
    if site_dropdown == 'All sites':
        piechart = px.pie(spacex_df, values='class', names='Launch Site',
                          title=f"Total Success Launches By Site")
        return piechart

    elif site_dropdown in sitesList:
        filtered_df = spacex_df[spacex_df['Launch Site'] == site_dropdown]
        filtered_df = filtered_df.groupby(
            ['Launch Site', 'class']).size().reset_index(name='class count')
        piechart = px.pie(filtered_df, values='class count', names='class',
                          title=f"Total Success Launches for site {site_dropdown}")
        return piechart


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output

# Add callback decorator
@app.callback(
    Output(component_id='success-payload-scatter-chart',
           component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id="payload-slider", component_property="value")]
)
# Add computation to callback function and return scatter
def get_scatter(entered_site, slider):
    if entered_site == "All sites":
        fig = px.scatter(spacex_df[spacex_df['Payload Mass (kg)'].between(slider[0], slider[1])],
                         x='Payload Mass (kg)', y='class', color='Booster Version Category', title="Correlation for All Sites")
        return fig
    else:
        filtered = spacex_df[spacex_df['Launch Site'] == entered_site]
        fig = px.scatter(filtered[filtered['Payload Mass (kg)'].between(slider[0], slider[1])], x='Payload Mass (kg)', y='class',
                         color='Booster Version Category', title="Correlation for " + entered_site)
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()

# Which site has the largest successful launches?


# Which site has the highest launch success rate?
# Which payload range(s) has the highest launch success rate?
# Which payload range(s) has the lowest launch success rate?
# Which F9 Booster version(v1.0, v1.1, FT, B4, B5, etc.) has the highest

# Plotly Dash Reference
# https://dash.plotly.com/dash-core-components/dropdown?utm_medium=Exinfluencer&utm_source=Exinfluencer&utm_content=000026UJ&utm_term=10006555&utm_id=NA-SkillsNetwork-Channel-SkillsNetworkCoursesIBMDS0321ENSkillsNetwork26802033-2021-01-01
# https://dash.plotly.com/dash-core-components/rangeslider?utm_medium=Exinfluencer&utm_source=Exinfluencer&utm_content=000026UJ&utm_term=10006555&utm_id=NA-SkillsNetwork-Channel-SkillsNetworkCoursesIBMDS0321ENSkillsNetwork26802033-2021-01-01
# https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/labs/Module%204/4.7_Dash_Interactivity.py
# https://plotly.com/python/pie-charts/?utm_medium=Exinfluencer&utm_source=Exinfluencer&utm_content=000026UJ&utm_term=10006555&utm_id=NA-SkillsNetwork-Channel-SkillsNetworkCoursesIBMDS0321ENSkillsNetwork26802033-2021-01-01
# https://plotly.com/python/line-and-scatter/?utm_medium=Exinfluencer&utm_source=Exinfluencer&utm_content=000026UJ&utm_term=10006555&utm_id=NA-SkillsNetwork-Channel-SkillsNetworkCoursesIBMDS0321ENSkillsNetwork26802033-2021-01-01
