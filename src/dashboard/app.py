import plotly.graph_objects as go
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from sqlalchemy.orm import Session

from src.db.models.flight import Flight
from src.db.models.parameter import Parameter
from src.db.session import engine

app = Dash(__name__, requests_pathname_prefix='/price-history/')
app.layout = html.Div([
    html.H1(children="Price History", style={"textAlign": "center"}),
    dcc.Dropdown(
        id="parameter-dropdown",
        options=[],
        value=None,
        placeholder="Select flight option"
    ),
    dcc.Graph(id="price-plot")
])


@app.callback(
    Output(component_id='parameter-dropdown', component_property='options'),
    Output(component_id='parameter-dropdown', component_property='value'),
    Input(component_id='parameter-dropdown', component_property='value')
)
def update_dropdown_selection(selected_option: int):
    session = Session(engine)
    selectable_params = session.query(Parameter).all()
    session.close()
    options = [
        {
            "label":
                f"{p.departure_location}-{p.arrival_location}, {p.departure_date}\t ||| \t"
                f"{p.departure_location_comeback}-{p.arrival_location_comeback}, {p.departure_date_comeback}",
            "value": p.id
        }
        if p.departure_location_comeback is not None
        else {
            "label":
                f"{p.departure_location}-{p.arrival_location}, {p.departure_date}",
            "value": p.id
        }
        for p in selectable_params
    ]
    if not selected_option and options:
        selected_option = options[0]["value"]
    return options, selected_option


@app.callback(
    Output(component_id="price-plot", component_property="figure"),
    Input(component_id="parameter-dropdown", component_property="value")
)
def update_plot(selected_option: int):
    if not selected_option:
        return go.Figure()
    session = Session(engine)
    flight_data = session.query(Flight).filter(
        Flight.parameters_id == selected_option
    ).all()
    session.close()
    figure = go.Figure(
        data=go.Scatter(
            x=[
                flight.created_at.isoformat(timespec="minutes")
                for flight in flight_data
            ],
            y=[flight.price for flight in flight_data],
            mode="markers",
            name="Prices",
            text=[
                f"{f.departure_date}-{f.arrival_date}\t ||| \t"
                f"{f.departure_date_comeback}-{f.arrival_date_comeback}"
                if f.departure_date_comeback is not None
                else f"{f.departure_date}-{f.arrival_date}"
                for f in flight_data
            ]
        )
    )
    figure.update_layout(
        title="Price History",
        xaxis={"title": "Sampling date"},
        yaxis={"title": "Price (Euro)"},
    )
    return figure
