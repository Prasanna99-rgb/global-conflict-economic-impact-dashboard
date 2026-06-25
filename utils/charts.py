# ============================================================
# Charts Utility Functions
# ============================================================

import plotly.express as px


# ============================================================
# Line Chart
# ============================================================

def line_chart(
    data,
    x,
    y,
    title,
    color="#4CAF50"
):

    fig = px.line(
        data,
        x=x,
        y=y,
        title=title,
        markers=True
    )

    fig.update_traces(
        line=dict(color=color, width=3)
    )

    fig.update_layout(
        template="plotly_dark",
        height=450,
        title_x=0.5
    )

    return fig


# ============================================================
# Bar Chart
# ============================================================

def bar_chart(
    data,
    x,
    y,
    title,
    color=None
):

    fig = px.bar(
        data,
        x=x,
        y=y,
        color=color if color else y,
        title=title
    )

    fig.update_layout(
        template="plotly_dark",
        height=450,
        title_x=0.5
    )

    return fig


# ============================================================
# Scatter Plot
# ============================================================

def scatter_chart(
    data,
    x,
    y,
    color=None,
    hover=None,
    title=""
):

    fig = px.scatter(
        data,
        x=x,
        y=y,
        color=color,
        hover_name=hover,
        title=title
    )

    fig.update_layout(
        template="plotly_dark",
        height=450,
        title_x=0.5
    )

    return fig


# ============================================================
# Correlation Heatmap
# ============================================================

def correlation_heatmap(corr):

    fig = px.imshow(
        corr,
        text_auto=True,
        color_continuous_scale="RdBu",
        aspect="auto"
    )

    fig.update_layout(
        template="plotly_dark",
        height=550,
        title="Correlation Matrix",
        title_x=0.5
    )

    return fig
