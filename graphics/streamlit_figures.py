import pandas as pd
import plotly.express as px
import plotly.graph_objs as go


def get_pie(serie, title, layout_showlegend=True):
    """
    Crea un gráfico de pastel interactivo con Plotly.

    Args:
        serie (pd.Series): Serie de pandas con los datos de la gráfica de pastel.
        title (str): Título de la gráfica de pastel.
        layout_showlegend (bool, optional): Indica si se mostrará la leyenda. Por defecto False.

    Returns:
        plotly.graph_objs._figure.Figure: Objeto de Plotly con el gráfico de pastel.
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
    fig = px.histogram(serie, y=serie.index, x=serie.values)
    fig = update_yaxis(fig)
    fig.update(layout_title_text=title)
    fig.update_layout(yaxis_title=yaxis_title, xaxis_title=xaxis_title)
    return fig
