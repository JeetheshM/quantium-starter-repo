from pathlib import Path

import pandas as pd
from dash import Dash, dcc, html
import plotly.graph_objects as go


DATA_PATH = Path(__file__).with_name("formatted_sales_data.csv")
PRICE_INCREASE_DATE = pd.Timestamp("2021-01-15")


def load_sales_data() -> pd.DataFrame:
    sales_data = pd.read_csv(DATA_PATH, parse_dates=["Date"])
    daily_sales = (
        sales_data.groupby("Date", as_index=False)["Sales"]
        .sum()
        .sort_values("Date")
    )
    return daily_sales


daily_sales = load_sales_data()

fig = go.Figure(
    data=[
        go.Scatter(
            x=daily_sales["Date"],
            y=daily_sales["Sales"],
            mode="lines",
            line=dict(color="#1f77b4", width=3),
            name="Total Sales",
        )
    ]
)
fig.add_vline(
    x=PRICE_INCREASE_DATE,
    line_width=2,
    line_dash="dash",
    line_color="#d62728",
)
fig.add_annotation(
    x=PRICE_INCREASE_DATE,
    y=1,
    yref="paper",
    text="Pink Morsel price increase",
    showarrow=False,
    yshift=12,
    font=dict(color="#d62728"),
)
fig.update_layout(
    title="Total Sales by Date",
    xaxis_title="Date",
    yaxis_title="Total Sales",
    template="plotly_white",
    margin=dict(l=40, r=20, t=80, b=40),
    title_x=0.5,
    hovermode="x unified",
)


app = Dash(__name__)
app.title = "Pink Morsel Sales Visualiser"
server = app.server

app.layout = html.Div(
    style={
        "minHeight": "100vh",
        "padding": "40px 24px",
        "backgroundColor": "#f4f1ea",
        "backgroundImage": "linear-gradient(135deg, rgba(229, 222, 210, 0.9), rgba(244, 241, 234, 1))",
        "fontFamily": "Georgia, serif",
    },
    children=[
        html.Div(
            style={
                "maxWidth": "1100px",
                "margin": "0 auto",
                "backgroundColor": "rgba(255, 255, 255, 0.92)",
                "borderRadius": "20px",
                "padding": "32px 28px 24px",
                "boxShadow": "0 18px 45px rgba(70, 60, 45, 0.12)",
            },
            children=[
                html.H1(
                    "Pink Morsel Sales Visualiser",
                    style={"marginBottom": "8px", "letterSpacing": "0.3px"},
                ),
                html.P(
                    "Sales are grouped by day and sorted chronologically to show the effect of the January 15, 2021 price increase.",
                    style={"marginTop": 0, "marginBottom": "24px", "color": "#4a453d"},
                ),
                dcc.Graph(figure=fig, style={"height": "70vh"}),
            ],
        ),
    ],
)


if __name__ == "__main__":
    app.run(debug=True)