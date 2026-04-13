from pathlib import Path

import pandas as pd
from dash import Dash, Input, Output, dcc, html
import plotly.graph_objects as go


DATA_PATH = Path(__file__).with_name("formatted_sales_data.csv")
PRICE_INCREASE_DATE = pd.Timestamp("2021-01-15")
REGION_COLORS = {
    "north": "#7c3aed",
    "east": "#0f766e",
    "south": "#d97706",
    "west": "#2563eb",
    "all": "#1f2937",
}


def load_sales_data() -> pd.DataFrame:
    sales_data = pd.read_csv(DATA_PATH, parse_dates=["Date"])
    return sales_data


sales_data = load_sales_data()


def build_figure(region: str) -> go.Figure:
    filtered_sales = sales_data if region == "all" else sales_data[sales_data["Region"] == region]
    daily_sales = (
        filtered_sales.groupby("Date", as_index=False)["Sales"]
        .sum()
        .sort_values("Date")
    )

    figure = go.Figure(
        data=[
            go.Scatter(
                x=daily_sales["Date"],
                y=daily_sales["Sales"],
                mode="lines",
                line=dict(color=REGION_COLORS[region], width=3.5),
                name=region.title(),
            )
        ]
    )
    figure.add_vline(
        x=PRICE_INCREASE_DATE,
        line_width=2,
        line_dash="dash",
        line_color="#b91c1c",
    )
    figure.add_annotation(
        x=PRICE_INCREASE_DATE,
        y=1,
        yref="paper",
        text="Pink Morsel price increase",
        showarrow=False,
        yshift=12,
        font=dict(color="#b91c1c", size=12),
    )
    figure.update_layout(
        title=f"{region.title()} Region Sales by Date" if region != "all" else "All Regions Sales by Date",
        xaxis_title="Date",
        yaxis_title="Total Sales",
        template="plotly_white",
        margin=dict(l=40, r=20, t=80, b=40),
        title_x=0.5,
        hovermode="x unified",
        plot_bgcolor="rgba(255,255,255,0)",
        paper_bgcolor="rgba(255,255,255,0)",
        font=dict(family="Georgia, serif", color="#24303f"),
    )
    figure.update_xaxes(showgrid=False)
    figure.update_yaxes(gridcolor="rgba(36, 48, 63, 0.12)")
    return figure


app = Dash(__name__)
app.title = "Pink Morsel Sales Visualiser"
server = app.server

app.layout = html.Div(
    style={
        "minHeight": "100vh",
        "padding": "40px 24px",
        "backgroundColor": "#f6f3ee",
        "backgroundImage": "radial-gradient(circle at top, rgba(201, 228, 255, 0.45), transparent 42%), linear-gradient(135deg, rgba(245, 238, 226, 0.95), rgba(250, 248, 244, 1))",
        "fontFamily": "Georgia, serif",
    },
    children=[
        html.Div(
            style={
                "maxWidth": "1100px",
                "margin": "0 auto",
                "backgroundColor": "rgba(255, 255, 255, 0.94)",
                "borderRadius": "24px",
                "padding": "32px 28px 28px",
                "boxShadow": "0 22px 50px rgba(55, 46, 34, 0.12)",
                "border": "1px solid rgba(80, 64, 43, 0.08)",
            },
            children=[
                html.H1(
                    "Pink Morsel Sales Visualiser",
                    style={
                        "marginBottom": "8px",
                        "letterSpacing": "0.4px",
                        "fontSize": "2.4rem",
                        "color": "#1f2937",
                    },
                ),
                html.P(
                    "Use the region selector to compare local sales patterns and see whether the Pink Morsel price increase changed the story.",
                    style={
                        "marginTop": 0,
                        "marginBottom": "18px",
                        "color": "#4a453d",
                        "maxWidth": "760px",
                        "fontSize": "1.03rem",
                        "lineHeight": "1.6",
                    },
                ),
                html.Div(
                    style={
                        "display": "flex",
                        "justifyContent": "space-between",
                        "alignItems": "center",
                        "gap": "16px",
                        "flexWrap": "wrap",
                        "marginBottom": "18px",
                        "padding": "16px 18px",
                        "background": "linear-gradient(135deg, rgba(33, 150, 243, 0.08), rgba(124, 58, 237, 0.06))",
                        "borderRadius": "16px",
                        "border": "1px solid rgba(36, 48, 63, 0.08)",
                    },
                    children=[
                        html.Div(
                            [
                                html.Div("Filter by region", style={"fontWeight": 700, "marginBottom": "4px"}),
                                html.Div(
                                    "Choose a region to update the line chart.",
                                    style={"color": "#5b6470", "fontSize": "0.95rem"},
                                ),
                            ]
                        ),
                        dcc.RadioItems(
                            id="region-selector",
                            options=[
                                {"label": "North", "value": "north"},
                                {"label": "East", "value": "east"},
                                {"label": "South", "value": "south"},
                                {"label": "West", "value": "west"},
                                {"label": "All", "value": "all"},
                            ],
                            value="all",
                            inline=True,
                            labelStyle={
                                "marginRight": "16px",
                                "fontWeight": 600,
                                "color": "#24303f",
                            },
                            inputStyle={"marginRight": "6px"},
                            style={"display": "flex", "flexWrap": "wrap", "rowGap": "10px"},
                        ),
                    ],
                ),
                dcc.Graph(
                    id="sales-chart",
                    figure=build_figure("all"),
                    style={"height": "72vh"},
                    config={"displayModeBar": False},
                ),
            ],
        ),
    ],
)


@app.callback(Output("sales-chart", "figure"), Input("region-selector", "value"))
def update_chart(selected_region: str) -> go.Figure:
    return build_figure(selected_region)


if __name__ == "__main__":
    app.run(debug=True)