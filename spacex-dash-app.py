# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df["Payload Mass (kg)"].max()
min_payload = spacex_df["Payload Mass (kg)"].min()

print(spacex_df)

launch_sites_options = [
    {"label": launch_site, "value": launch_site}
    for launch_site in spacex_df["Launch Site"].unique()
]
launch_sites_options.insert(0, {"label": "All Sites", "value": "ALL"})
# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(
    children=[
        html.H1(
            "SpaceX Launch Records Dashboard",
            style={"textAlign": "center", "color": "#503D36", "font-size": 40},
        ),
        # TASK 1: Add a dropdown list to enable Launch Site selection
        # The default select value is for ALL sites
        dcc.Dropdown(
            id="site-dropdown",
            options=launch_sites_options,
            value="ALL",
            placeholder="place holder here",
            searchable=True,
        ),
        html.Br(),
        # TASK 2: Add a pie chart to show the total successful launches count for all sites
        # If a specific launch site was selected, show the Success vs. Failed counts for the site
        html.Div(dcc.Graph(id="success-pie-chart")),
        html.Br(),
        html.P("Payload range (Kg):"),
        # TASK 3: Add a slider to select payload range
        dcc.RangeSlider(
            id="payload-slider",
            min=min_payload,
            max=max_payload,
            value=[min_payload, max_payload],
            marks={0: "0", 100: "100"},
            step=1000,
        ),
        # TASK 4: Add a scatter chart to show the correlation between payload and launch success
        html.Div(dcc.Graph(id="success-payload-scatter-chart")),
    ]
)


# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id="success-pie-chart", component_property="figure"),
    Input(component_id="site-dropdown", component_property="value"),
)
def get_pie_chart(entered_site):
    print(entered_site)
    if entered_site == "ALL":
        fig = px.pie(spacex_df, values="class", names="Launch Site", title="All Sites")
        return fig
    else:
        filtered_df = spacex_df[spacex_df["Launch Site"] == entered_site]
        fig = px.pie(filtered_df, values="class", names="class", title=entered_site)
        return fig


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id='payload-slider', component_property='value')])
def get_scatter_chart(entered_site, payload_range):
    print(entered_site)
    filtered_df = spacex_df
    if entered_site == 'ALL':
        filtered_df = filtered_df[(filtered_df['Payload Mass (kg)'] >= payload_range[0]) & (filtered_df['Payload Mass (kg)'] <= payload_range[1])]
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', 
        color='Booster Version',
        title='Correlation between Payload and Success for All Sites')
        return fig
    else:
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        filtered_df = filtered_df[(filtered_df['Payload Mass (kg)'] >= payload_range[0]) & (filtered_df['Payload Mass (kg)'] <= payload_range[1])]
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', 
        color='Booster Version',
        title=f'Correlation between Payload and Success for {entered_site}')
        return fig

# Run the app
if __name__ == "__main__":
    app.run()
