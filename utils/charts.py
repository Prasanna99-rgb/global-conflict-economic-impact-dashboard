# ============================================================
# charts.py
# Reusable Plotly Chart Functions
# ============================================================

import plotly.express as px
import plotly.graph_objects as go


# ============================================================
# Common Layout
# ============================================================

def apply_layout(fig, title):

    fig.update_layout(

        template="plotly_dark",

        title=title,

        title_x=0.5,

        height=500,

        legend_title="",

        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20
        )

    )

    return fig


# ============================================================
# Line Chart
# ============================================================

def line_chart(
    data,
    x,
    y,
    title,
    color="#00CC96"
):

    fig = px.line(

        data,

        x=x,

        y=y,

        markers=True

    )

    fig.update_traces(

        line=dict(
            color=color,
            width=3
        )

    )

    return apply_layout(
        fig,
        title
    )


# ============================================================
# Multi Line Chart
# ============================================================

def multi_line_chart(
    data,
    x,
    y,
    title
):

    fig = px.line(

        data,

        x=x,

        y=y,

        markers=True

    )

    return apply_layout(
        fig,
        title
    )


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

        text_auto=".2s"

    )

    return apply_layout(
        fig,
        title
    )


# ============================================================
# Horizontal Bar
# ============================================================

def horizontal_bar_chart(
    data,
    x,
    y,
    title
):

    fig = px.bar(

        data,

        x=x,

        y=y,

        orientation="h",

        text_auto=".2s",

        color=x

    )

    return apply_layout(
        fig,
        title
    )


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

        size_max=15

    )

    return apply_layout(
        fig,
        title
    )


# ============================================================
# Pie Chart
# ============================================================

def pie_chart(
    data,
    names,
    values,
    title
):

    fig = px.pie(

        data,

        names=names,

        values=values,

        hole=0.4

    )

    return apply_layout(
        fig,
        title
    )


# ============================================================
# Donut Chart
# ============================================================

def donut_chart(
    data,
    names,
    values,
    title
):

    fig = px.pie(

        data,

        names=names,

        values=values,

        hole=0.65

    )

    return apply_layout(
        fig,
        title
    )


# ============================================================
# Histogram
# ============================================================

def histogram_chart(
    data,
    column,
    title
):

    fig = px.histogram(

        data,

        x=column,

        nbins=30

    )

    return apply_layout(
        fig,
        title
    )


# ============================================================
# Box Plot
# ============================================================

def box_chart(
    data,
    x,
    y,
    title
):

    fig = px.box(

        data,

        x=x,

        y=y,

        points="outliers"

    )

    return apply_layout(
        fig,
        title
    )


# ============================================================
# Area Chart
# ============================================================

def area_chart(
    data,
    x,
    y,
    title
):

    fig = px.area(

        data,

        x=x,

        y=y

    )

    return apply_layout(
        fig,
        title
    )


# ============================================================
# Correlation Heatmap
# ============================================================

def correlation_heatmap(corr):

    fig = px.imshow(

        corr,

        text_auto=True,

        aspect="auto",

        color_continuous_scale="RdBu"

    )

    return apply_layout(
        fig,
        "Correlation Matrix"
    )


# ============================================================
# Choropleth World Map
# ============================================================

def world_map(
    data,
    locations,
    color,
    title
):

    fig = px.choropleth(

        data,

        locations=locations,

        locationmode="country names",

        color=color,

        color_continuous_scale="Reds"

    )

    return apply_layout(
        fig,
        title
    )


# ============================================================
# Bubble Chart
# ============================================================

def bubble_chart(
    data,
    x,
    y,
    size,
    color,
    hover,
    title
):

    fig = px.scatter(

        data,

        x=x,

        y=y,

        size=size,

        color=color,

        hover_name=hover

    )

    return apply_layout(
        fig,
        title
    )


# ============================================================
# Ranking Table
# ============================================================

def ranking_table(df):

    df = df.copy()

    df.insert(0, "Rank", range(1, len(df)+1))

    return df
