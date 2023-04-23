import pandas as pd
import plotly.express as px
import plotly.graph_objs as go


def get_pie(serie, title, layout_showlegend=True):
    """
    Create an interactive pie chart using Plotly.

    Args:
        serie (pd.Series): A pandas Series containing the data for the pie chart.
        title (str): The title of the pie chart.
        layout_showlegend (bool, optional): Whether to show the legend. Default is True.

    Returns:
        plotly.graph_objs._figure.Figure: A Plotly figure object with the pie chart.

    """
    trace = go.Pie(
        labels=serie.index,
        values=serie.values,
        hole=0.4,
        hoverinfo="label+percent",
        textinfo="label+percent",
        textposition="outside",
    )
    layout = go.Layout(title=title, showlegend=layout_showlegend)

    fig = go.Figure(data=[trace], layout=layout)

    return fig


def get_horizontal_histogram(
    df: pd.DataFrame,
    column_name: str,
    category_order: list,
    norm: str = None,
    marginal: str = None,
    yaxis_title: str = "",
    xaxis_title: str = "",
):
    """
    Create a horizontal histogram using Plotly.

    Args:
        df (pd.DataFrame): A pandas DataFrame containing the data.
        column_name (str): The name of the column in the DataFrame to plot.
        category_order (list): A list specifying the category order for the x-axis.
        norm (str, optional): The normalization mode for the histogram.
        marginal (str, optional): The type of marginal plot to display.
        yaxis_title (str, optional): The title of the y-axis.
        xaxis_title (str, optional): The title of the x-axis.

    Returns:
        plotly.graph_objs._figure.Figure: A Plotly figure object with the horizontal histogram.

    """
    fig = px.histogram(
        df,
        x=column_name,
        histnorm=norm,
        marginal=marginal,
    )
    fig.update(layout_title_text=column_name)
    fig.update_layout(yaxis_title=yaxis_title, xaxis_title=xaxis_title)
    fig.update_xaxes(categoryorder="array", categoryarray=category_order)

    return fig


def update_yaxis(fig):
    """
    Update the y-axis of a Plotly figure.

    Args:
        fig (plotly.graph_objs._figure.Figure): The Plotly figure object to update.

    Returns:
        plotly.graph_objs._figure.Figure: The updated Plotly figure object.

    """
    fig.update_yaxes(automargin=True, categoryorder="total ascending")
    fig.update_traces(textposition="inside", selector=dict(type="histogram"))
    fig.update_layout(yaxis_title="")
    return fig


def get_vertical_histogram(
        df: pd.DataFrame,
        column: str,
        norm: str = None,
        yaxis_title: str = "",
        xaxis_title: str = "",
        ):
    """
    Create a vertical histogram with Plotly.

    Args:
        df (pd.DataFrame): Pandas DataFrame containing the data for the histogram.
        column (str): Name of the column in the DataFrame to plot as the histogram.
        norm (str, optional): Normalization mode for the histogram.
        yaxis_title (str, optional): Title for the y-axis.
        xaxis_title (str, optional): Title for the x-axis.

    Returns:
        plotly.graph_objs._figure.Figure: Plotly figure object containing the vertical histogram.

    """
    fig = px.histogram(df, y=column, histnorm=norm)
    fig = update_yaxis(fig)
    fig.update(layout_title_text=column)
    fig.update_layout(yaxis_title=yaxis_title, xaxis_title=xaxis_title)
    return fig


def get_vertical_graph_from_serie(
        serie: pd.Series,
        title: str,
        yaxis_title: str = "",
        xaxis_title: str = "",
        ):
    """
    Create a vertical graph from a Pandas Series using Plotly.

    Args:
        serie (pd.Series): Pandas Series containing the data for the graph.
        title (str): Title of the graph.
        yaxis_title (str, optional): Title for the y-axis.
        xaxis_title (str, optional): Title for the x-axis.

    Returns:
        plotly.graph_objs._figure.Figure: Plotly figure object containing the vertical graph.

    """
    fig = px.histogram(serie, y=serie.index, x=serie.values)
    fig = update_yaxis(fig)
    fig.update(layout_title_text=title)
    fig.update_layout(yaxis_title=yaxis_title, xaxis_title=xaxis_title)
    return fig
