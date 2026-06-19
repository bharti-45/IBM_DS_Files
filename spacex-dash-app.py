import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

# Load dataset
spacex_df = pd.read_csv("spacex_launch_dash.csv")

# Create app
app = dash.Dash(__name__)

# -------------------------
# Layout
# -------------------------
app.layout = html.Div([

    html.H1("SpaceX Launch Dashboard", style={'textAlign': 'center'}),

    # Dropdown
    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'All Sites', 'value': 'ALL'},
            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
            {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
        ],
        value='ALL',
        searchable=True
    ),

    html.Br(),

    # Pie chart
    dcc.Graph(id='success-pie-chart'),

    html.Br(),

    html.P("Payload Range (Kg):"),

    # Slider
    dcc.RangeSlider(
        id='payload-slider',
        min=0,
        max=10000,
        step=1000,
        marks={0: '0', 2500: '2500', 5000: '5000', 7500: '7500', 10000: '10000'},
        value=[0, 10000]
    ),

    html.Br(),

    # Scatter plot
    dcc.Graph(id='success-payload-scatter-chart')
])

# -------------------------
# PIE CHART CALLBACK
# -------------------------
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def update_pie(site):

    if site == 'ALL':
        fig = px.pie(
            spacex_df,
            names='Launch Site',
            values='class',
            title='Total Launches by Site'
        )
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == site]

        fig = px.pie(
            filtered_df,
            names='class',
            values='class',
            title=f'Success vs Failure for {site}'
        )

    return fig

# -------------------------
# SCATTER CALLBACK
# -------------------------
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [
        Input('site-dropdown', 'value'),
        Input('payload-slider', 'value')
    ]
)
def update_scatter(site, payload_range):

    low, high = payload_range

    df_filtered = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= low) &
        (spacex_df['Payload Mass (kg)'] <= high)
    ]

    if site != 'ALL':
        df_filtered = df_filtered[df_filtered['Launch Site'] == site]

    fig = px.scatter(
        df_filtered,
        x='Payload Mass (kg)',
        y='class',
        color='Booster Version',
        title='Payload vs Launch Outcome'
    )

    return fig

# -------------------------
# RUN APP (FIXED FOR NEW DASH)
# -------------------------
if __name__ == '__main__':
    app.run(debug=True)