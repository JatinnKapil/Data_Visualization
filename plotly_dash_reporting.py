import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
from sqlalchemy import create_engine

#Reading From a Database
# Connect to sqlite db
db_file = os.path.join(os.path.dirname(wb.fullname), 'proj.db')
engine = create_engine(r"sqlite:///{}".format(db_file))
  data = pd.read_sql(sql, engine)
  # Read query directly into a dataframe
  # Create SQL query
sql = 'SELECT * from table WHERE x="{}" AND date BETWEEN "{}" AND "{}"'.format()
  
# Read in the data from Excel
df = pd.read_excel(
    "/blob/master/data/funnel.xlsx"
)

# Get a list of all the avilable managers
mgr_options = df["Manager"].unique()

# Create the app
app = dash.Dash()

# Populate the layout with HTML and graph components
app.layout = html.Div([
    html.H2("Funnel Report"),
    html.Div(
        [
            dcc.Dropdown(
                id="Manager",
                options=[{
                    'label': i,
                    'value': i
                } for i in mgr_options],
                value='All Managers'),
        ],
        style={'width': '25%',
               'display': 'inline-block'}),
    dcc.Graph(id='funnel-graph'),
])


# Add the callbacks to support the interactive componets
@app.callback(
    dash.dependencies.Output('funnel-graph', 'figure'),
    [dash.dependencies.Input('Manager', 'value')])
def update_graph(Manager):
    if Manager == "All Managers":
        df_plot = df.copy()
    else:
        df_plot = df[df['Manager'] == Manager]

    pv = pd.pivot_table(
        df_plot,
        index=['Name'],
        columns=["Status"],
        values=['Quantity'],
        aggfunc=sum,
        fill_value=0)

    trace1 = go.Bar(x=pv.index, y=pv[('Quantity', 'declined')], name='Declined')
    trace2 = go.Bar(x=pv.index, y=pv[('Quantity', 'pending')], name='Pending')
    trace3 = go.Bar(x=pv.index, y=pv[('Quantity', 'presented')], name='Presented')
    trace4 = go.Bar(x=pv.index, y=pv[('Quantity', 'won')], name='Won')

    return {
        'data': [trace1, trace2, trace3, trace4],
        'layout':
        go.Layout(
            title='Customer Order Status for {}'.format(Manager),
            barmode='stack')
    }


if __name__ == '__main__':
    app.run_server(debug=True)
