import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
import numpy as np
import pandas as pd


import config
import graphics.streamlit_order_plots as streamlit_order_plots
import graphics.streamlit_figures as streamlit_figures


def display_dashboard(df):
    container = st.container()
    with container:
        # Salarios
        st.markdown("### Salarios :moneybag:")
        tabs = st.tabs(
            [
                "Salario mensual BRUTO",
                "Salario mensual NETO",
                "Actualizaciones de tus ingresos",
            ]
        )

        with tabs[0]:
            try:
                st.plotly_chart(
                    streamlit_figures.get_horizontal_histogram(
                        df,
                        config.GROSS_SALARY,
                        streamlit_order_plots.get_order(
                            df[config.GROSS_SALARY].unique().tolist()
                        ),
                        marginal="box",
                    ),
                    theme=None,
                )
            except Exception as e:
                st.error(config.ERROR_MSG)
                st.error(e)

        with tabs[1]:
            try:
                st.plotly_chart(
                    streamlit_figures.get_horizontal_histogram(
                        df,
                        config.NET_SALARY,
                        streamlit_order_plots.get_order(
                            df[config.NET_SALARY].unique().tolist()
                        ),
                        marginal="box",
                    ),
                    theme=None,
                )
            except Exception as e:
                st.error(config.ERROR_MSG)
                st.error(e)

        with tabs[2]:
            try:
                st.plotly_chart(
                    streamlit_figures.get_horizontal_histogram(
                        df,
                        "¿Tuviste actualizaciones de tus ingresos laborales durante 2022?",
                        streamlit_order_plots.ORDER_1_3,
                    ),
                    theme=None,
                )
            except Exception as e:
                st.error(config.ERROR_MSG)
                st.error(e)

        df_aux = (
            df.loc[
                (df[config.NET_SALARY].notna())
                & (df[config.YEARS_OF_EXPERIENCE].notna())
            ]
            .groupby([config.YEARS_OF_EXPERIENCE])[config.NET_SALARY]
            .median()
            .reset_index()
        )

        if df_aux[config.YEARS_OF_EXPERIENCE].count() >= config.MINIMUM_RESPONSES:
            fig = px.scatter(
                df_aux,
                y=df_aux[config.NET_SALARY].values,
                x=df_aux[config.YEARS_OF_EXPERIENCE].values,
                opacity=1,
                labels={
                    "x": config.YEARS_OF_EXPERIENCE,
                    "y": "Mediana del sueldo Neto segun experiencia",
                },
                title="Tendencia de sueldos segun experiencia",
            )

            X = df_aux[config.YEARS_OF_EXPERIENCE].values.reshape(-1, 1) + 0.1
            y = df_aux[config.NET_SALARY].values.reshape(-1, 1)
            model = LinearRegression()
            model.fit(np.log(X), y)

            angular_coefficient = model.coef_[0]
            intercept = model.intercept_
            fig.add_trace(
                go.Scatter(
                    x=X.flatten(),
                    y=angular_coefficient * np.log(X + 0.1).flatten() + intercept,
                    mode="lines",
                    name="Regresión logarítmica",
                )
            )

            try:
                st.plotly_chart(fig, theme=None)
            except Exception as e:
                st.error(config.ERROR_MSG)
                st.error(e)

        # Dolares

        if config.PAYMENTS_IN_DOLLARS in df.columns:
            st.markdown("### Proporción de salarios en dólares  :money_with_wings:")
            tabs = st.tabs([config.PAYMENTS_IN_DOLLARS, "Valor del tipo de cambio"])

            with tabs[0]:
                try:
                    st.plotly_chart(
                        streamlit_figures.get_pie(
                            serie=df[config.PAYMENTS_IN_DOLLARS]
                            .replace(np.NaN, "No responde")
                            .value_counts(),
                            title="¿Cobras en dólares?",
                        ),
                        theme=None,
                    )
                except Exception as e:
                    st.error(config.ERROR_MSG)
                    st.error(e)

            with tabs[1]:
                if (
                    config.LAST_VALUE_EXCHANGE + config.REWRITTEN_COLUMN_SUFFIX
                ) not in df.columns:
                    st.warning(
                        f"""No se encuentra la columna {
                            config.LAST_VALUE_EXCHANGE + config.REWRITTEN_COLUMN_SUFFIX
                            } en el archivo"""
                    )
                elif (
                    df[
                        config.LAST_VALUE_EXCHANGE + config.REWRITTEN_COLUMN_SUFFIX
                    ].count()
                    >= config.MINIMUM_RESPONSES
                ):
                    try:
                        st.plotly_chart(
                            streamlit_figures.get_horizontal_histogram(
                                df,
                                config.LAST_VALUE_EXCHANGE
                                + config.REWRITTEN_COLUMN_SUFFIX,
                                None,
                            ),
                            theme=None,
                        )
                    except Exception as e:
                        st.error(config.ERROR_MSG)
                        st.error(e)
                else:
                    st.warning("Faltan muestras, no fue posible desplegar el gráfico.")

            # Salarios en dólares
            st.markdown("### Salarios en dólares :money_with_wings:")

            # gross salary
            st.markdown("##### Salario Bruto")
            tabs = st.tabs(df[config.PAYMENTS_IN_DOLLARS].unique().tolist())

            figurs = {}
            for n, tab in enumerate(df[config.PAYMENTS_IN_DOLLARS].unique().tolist()):
                df_aux = df.loc[
                    df[config.PAYMENTS_IN_DOLLARS] == tab, config.GROSS_SALARY
                ]
                fig = px.histogram(
                    df_aux,
                    x=df_aux,
                    marginal="box",
                    opacity=1,
                    labels={
                        "count": "Cantidad de encuestados",
                        "x": "Valores salariales",
                    },
                    title="¿Cobras en dólares? " + tab,
                )

                figurs[tab] = fig

                with tabs[n]:
                    try:
                        st.plotly_chart(figurs[tab], theme=None)
                    except Exception as e:
                        st.error(config.ERROR_MSG)
                        st.error(e)

            df_aux = (
                df.loc[
                    (df[config.GROSS_SALARY].notna())
                    & (df[config.YEARS_OF_EXPERIENCE].notna())
                ]
                .groupby([config.PAYMENTS_IN_DOLLARS, config.YEARS_OF_EXPERIENCE])[
                    config.GROSS_SALARY
                ]
                .median()
                .reset_index()
            )
            #
            if df_aux[config.YEARS_OF_EXPERIENCE].count() >= config.MINIMUM_RESPONSES:
                type_salary_usd = np.unique(df[config.PAYMENTS_IN_DOLLARS])

                df_aux = (
                    df.loc[
                        (df[config.GROSS_SALARY].notna())
                        & (df[config.YEARS_OF_EXPERIENCE].notna())
                    ]
                    .groupby([config.PAYMENTS_IN_DOLLARS, config.YEARS_OF_EXPERIENCE])[
                        config.GROSS_SALARY
                    ]
                    .median()
                    .reset_index()
                )

                X = df_aux[config.YEARS_OF_EXPERIENCE].values.reshape(-1, 1) + 0.1
                y = df_aux[config.GROSS_SALARY].values.reshape(-1, 1)

                fig = px.scatter(
                    df_aux,
                    y=df_aux[config.GROSS_SALARY].values,
                    x=df_aux[config.YEARS_OF_EXPERIENCE].values,
                    color=df_aux[config.PAYMENTS_IN_DOLLARS].values,
                    opacity=1,
                    labels={
                        "x": config.YEARS_OF_EXPERIENCE,
                        "y": "Mediana del slario bruto",
                    },
                    title="Tendencia de sueldos segun experiencia y tipo de salario",
                )

                modelos = {}
                for type_salary in type_salary_usd:
                    X_genero = X[df_aux[config.PAYMENTS_IN_DOLLARS] == type_salary]
                    y_genero = y[df_aux[config.PAYMENTS_IN_DOLLARS] == type_salary]
                    modelos[type_salary] = LinearRegression()
                    modelos[type_salary].fit(np.log(X_genero), y_genero)

                for type_salary in type_salary_usd:
                    angular_coefficient = modelos[type_salary].coef_[0]
                    intercept = modelos[type_salary].intercept_
                    log_X = (
                        np.log(
                            X[df_aux[config.PAYMENTS_IN_DOLLARS] == type_salary] + 0.1
                        ).flatten())
                    fig.add_trace(
                        go.Scatter(
                            x=X[
                                df_aux[config.PAYMENTS_IN_DOLLARS] == type_salary
                            ].flatten(),
                            y=angular_coefficient * log_X + intercept,
                            mode="lines",
                            name=type_salary,
                        )
                    )

                try:
                    st.plotly_chart(fig, theme=None)
                except Exception as e:
                    st.error(config.ERROR_MSG)
                    st.error(e)

            # net salary
            st.markdown("##### Salario Neto")
            tabs = st.tabs(df[config.PAYMENTS_IN_DOLLARS].unique().tolist())

            figurs = {}
            for n, tab in enumerate(df[config.PAYMENTS_IN_DOLLARS].unique().tolist()):
                df_aux = df.loc[
                    df[config.PAYMENTS_IN_DOLLARS] == tab, config.NET_SALARY
                ]
                fig = px.histogram(
                    df_aux,
                    x=df_aux,
                    marginal="box",
                    opacity=1,
                    labels={
                        "count": "Cantidad de encuestados",
                        "x": "Valores salariales",
                    },
                    title="¿Cobras en dólares? " + tab,
                )
                figurs[tab] = fig

                with tabs[n]:
                    try:
                        st.plotly_chart(figurs[tab], theme=None)
                    except Exception as e:
                        st.error(config.ERROR_MSG)
                        st.error(e)

            df_aux = (
                df.loc[
                    (df[config.NET_SALARY].notna())
                    & (df[config.YEARS_OF_EXPERIENCE].notna())
                ]
                .groupby([config.PAYMENTS_IN_DOLLARS, config.YEARS_OF_EXPERIENCE])[
                    config.NET_SALARY
                ]
                .median()
                .reset_index()
            )

            ###
            if df_aux[config.YEARS_OF_EXPERIENCE].count() >= config.MINIMUM_RESPONSES:
                type_salary_usd = np.unique(df[config.PAYMENTS_IN_DOLLARS])

                df_aux = (
                    df.loc[
                        (df[config.NET_SALARY].notna())
                        & (df[config.YEARS_OF_EXPERIENCE].notna())
                    ]
                    .groupby([config.PAYMENTS_IN_DOLLARS, config.YEARS_OF_EXPERIENCE])[
                        config.NET_SALARY
                    ]
                    .median()
                    .reset_index()
                )

                X = df_aux[config.YEARS_OF_EXPERIENCE].values.reshape(-1, 1) + 0.1
                y = df_aux[config.NET_SALARY].values.reshape(-1, 1)

                fig = px.scatter(
                    df_aux,
                    y=df_aux[config.NET_SALARY].values,
                    x=df_aux[config.YEARS_OF_EXPERIENCE].values,
                    color=df_aux[config.PAYMENTS_IN_DOLLARS].values,
                    opacity=1,
                    labels={
                        "x": config.YEARS_OF_EXPERIENCE,
                        "y": "Mediana del slario neto",
                    },
                    title="Tendencia de sueldos segun experiencia y tipo de salario",
                )

                modelos = {}
                for type_salary in type_salary_usd:
                    X_genero = X[df_aux[config.PAYMENTS_IN_DOLLARS] == type_salary]
                    y_genero = y[df_aux[config.PAYMENTS_IN_DOLLARS] == type_salary]
                    modelos[type_salary] = LinearRegression()
                    modelos[type_salary].fit(np.log(X_genero), y_genero)

                for type_salary in type_salary_usd:
                    angular_coefficient = modelos[type_salary].coef_[0]
                    intercept = modelos[type_salary].intercept_
                    log_X = (
                        np.log(
                            X[df_aux[config.PAYMENTS_IN_DOLLARS] == type_salary] + 0.1
                        ).flatten())
                    fig.add_trace(
                        go.Scatter(
                            x=X[
                                df_aux[config.PAYMENTS_IN_DOLLARS] == type_salary
                            ].flatten(),
                            y=angular_coefficient * log_X + intercept,
                            mode="lines",
                            name=type_salary,
                        )
                    )

                try:
                    st.plotly_chart(fig, theme=None)
                except Exception as e:
                    st.error(config.ERROR_MSG)
                    st.error(e)

            payments = df[config.PAYMENTS_IN_DOLLARS].unique().tolist()
            if len(payments) == 1 and payments[0] == "Cobro todo el salario en dólares":
                st.markdown("### Salarios de ARG -> USD :money_with_wings:")
                tabs = st.tabs(
                    [
                        "Salario Bruto",
                        "Salario Neto",
                    ]
                )
                with tabs[0]:
                    try:
                        df_ax = df[
                            (
                                df[config.PAYMENTS_IN_DOLLARS]
                                == "Cobro todo el salario en dólares"
                            )
                            & (df[config.LAST_VALUE_EXCHANGE].notnull())
                            & (df[config.GROSS_SALARY].notnull())
                        ]

                        df_ax = (
                            (
                                df_ax[config.GROSS_SALARY]
                                / df_ax[config.LAST_VALUE_EXCHANGE]
                            )
                            .reset_index()
                            .rename(columns={0: "Salarios en USD"})
                        )

                        st.plotly_chart(
                            streamlit_figures.get_horizontal_histogram(
                                df_ax,
                                "Salarios en USD",
                                category_order=None,
                                marginal="box",
                            ),
                            theme=None,
                        )
                    except Exception as e:
                        st.error(config.ERROR_MSG)
                        st.error(e)
                with tabs[1]:
                    try:
                        df_ax = df[
                            (
                                df[config.PAYMENTS_IN_DOLLARS]
                                == "Cobro todo el salario en dólares"
                            )
                            & (df[config.LAST_VALUE_EXCHANGE].notnull())
                            & (df[config.NET_SALARY].notnull())
                        ]
                        df_ax = (
                            (
                                df_ax[config.NET_SALARY]
                                / df_ax[config.LAST_VALUE_EXCHANGE]
                            )
                            .reset_index()
                            .rename(columns={0: "Salarios en USD"})
                        )

                        st.plotly_chart(
                            streamlit_figures.get_horizontal_histogram(
                                df_ax,
                                "Salarios en USD",
                                category_order=None,
                                marginal="box",
                            ),
                            theme=None,
                        )
                    except Exception as e:
                        st.error(config.ERROR_MSG)
                        st.error(e)

        # Regiones
        st.markdown("### Regiones :world_map:")
        tabs = st.tabs([":world_map:"])

        with tabs[0]:
            try:
                st.plotly_chart(
                    streamlit_figures.get_vertical_histogram(df, config.PROVINCES),
                    theme=None,
                )
            except Exception as e:
                st.error(config.ERROR_MSG)
                st.error(e)

        # Genero y edades
        st.markdown("### Genero y edades :birthday:")
        tabs = st.tabs(
            [
                "Generos",
                "Edades",
                "Edades agrupadas",
            ]
        )

        with tabs[0]:
            try:
                st.plotly_chart(
                    streamlit_figures.get_pie(
                        df[config.GENDER].value_counts(), title="sdad"
                    ),
                    theme=None,
                )
            except Exception as e:
                st.error(config.ERROR_MSG)
                st.error(e)

        with tabs[1]:
            try:
                st.plotly_chart(
                    streamlit_figures.get_horizontal_histogram(
                        df, config.AGE, category_order=None, marginal="box"
                    ),
                    theme=None,
                )
            except Exception as e:
                st.error(config.ERROR_MSG)
                st.error(e)
        with tabs[2]:
            try:
                st.plotly_chart(
                    streamlit_figures.get_horizontal_histogram(
                        df,
                        config.AGE + config.REWRITTEN_COLUMN_SUFFIX,
                        streamlit_order_plots.get_order(
                            df[config.AGE + config.REWRITTEN_COLUMN_SUFFIX].unique()
                        ),
                    ),
                    theme=None,
                )
            except Exception as e:
                st.error(config.ERROR_MSG)
                st.error(e)

        # Experiencia
        st.markdown("### Experiencia :brain:")
        tabs = st.tabs(
            [
                config.YEARS_OF_EXPERIENCE,
                "Antiguedad en la empresa",
                "Tiempo en el actual puesto",
                "Relacion entre experiencia y antiguedad en la empresa",
            ]
        )

        with tabs[0]:
            try:
                st.plotly_chart(
                    streamlit_figures.get_horizontal_histogram(
                        df,
                        config.YEARS_OF_EXPERIENCE + config.REWRITTEN_COLUMN_SUFFIX,
                        streamlit_order_plots.FIBO_ORDER,
                    ),
                    theme=None,
                )
            except Exception as e:
                st.error(config.ERROR_MSG)
                st.error(e)

        with tabs[1]:
            try:
                st.plotly_chart(
                    streamlit_figures.get_horizontal_histogram(
                        df,
                        config.TIME_IN_CURRENT_COMPANY + config.REWRITTEN_COLUMN_SUFFIX,
                        streamlit_order_plots.FIBO_ORDER,
                    ),
                    theme=None,
                )
            except Exception as e:
                st.error(config.ERROR_MSG)
                st.error(e)

        with tabs[2]:
            try:
                st.plotly_chart(
                    streamlit_figures.get_horizontal_histogram(
                        df,
                        config.TIME_IN_CURRENT_ROLE + config.REWRITTEN_COLUMN_SUFFIX,
                        streamlit_order_plots.FIBO_ORDER,
                    ),
                    theme=None,
                )
            except Exception as e:
                st.error(config.ERROR_MSG)
                st.error(e)

        with tabs[3]:
            if df[config.YEARS_OF_EXPERIENCE].count() >= config.MINIMUM_RESPONSES:
                try:
                    X = df.loc[
                        df[config.YEARS_OF_EXPERIENCE].notna()
                        & df[config.TIME_IN_CURRENT_COMPANY].notna(),
                        config.YEARS_OF_EXPERIENCE,
                    ].values.reshape(-1, 1)

                    model = LinearRegression()
                    model.fit(
                        X,
                        df.loc[
                            df[config.YEARS_OF_EXPERIENCE].notna()
                            & df[config.TIME_IN_CURRENT_COMPANY].notna(),
                            config.TIME_IN_CURRENT_COMPANY,
                        ].values,
                    )

                    x_range = np.linspace(X.min(), X.max(), 100)
                    y_range = model.predict(x_range.reshape(-1, 1))

                    fig = px.scatter(
                        df,
                        x=df.loc[
                            df[config.YEARS_OF_EXPERIENCE].notna(),
                            config.YEARS_OF_EXPERIENCE,
                        ],
                        y=df.loc[
                            df[config.YEARS_OF_EXPERIENCE].notna(),
                            config.TIME_IN_CURRENT_COMPANY,
                        ],
                        opacity=0.35,
                        labels={
                            "y": "Años en la empresa",
                            "x": config.YEARS_OF_EXPERIENCE,
                        },
                        title="Relacion entre experiencia y antiguedad en la empresa",
                    )
                    fig.add_traces(go.Scatter(x=x_range, y=y_range, name="Regression"))
                    st.plotly_chart(fig, theme=None)
                except Exception as e:
                    st.error(config.ERROR_MSG)
                    st.error(e)
            else:
                st.warning("Faltan muestras, no fue posible desplegar el gráfico.")

        # Education
        st.markdown("### Educacion :mortar_board:")
        tabs = st.tabs(
            [
                config.CAREER,
                config.STUDIES_STATE,
                config.MAX_LVL_STUDIES,
            ]
        )

        with tabs[0]:
            try:
                st.plotly_chart(
                    streamlit_figures.get_vertical_histogram(
                        df, config.CAREER + config.REWRITTEN_COLUMN_SUFFIX
                    ),
                    use_container_width=True,
                    theme=None,
                )
                df[config.CAREER].fillna("No Contesta", inplace=True)
                total_count = len(df)
                total_na = df[config.CAREER].eq("No Contesta").sum()
                perc = (total_na / total_count) * 100

                st.markdown(
                    f"**El %{perc:.2f}({total_na}) del total({total_count}) no contesto esta pregunta.**"
                )
            except Exception as e:
                st.error(config.ERROR_MSG)
                st.error(e)

        with tabs[1]:
            try:
                st.plotly_chart(
                    streamlit_figures.get_pie(
                        df[config.STUDIES_STATE].value_counts(),
                        title="Estado de la carrera",
                    ),
                    theme=None,
                )
            except Exception as e:
                st.error(config.ERROR_MSG)
                st.error(e)

        with tabs[2]:
            try:
                st.plotly_chart(
                    streamlit_figures.get_vertical_histogram(
                        df, config.MAX_LVL_STUDIES, norm="percent"
                    ),
                    theme=None,
                )
            except Exception as e:
                st.error(config.ERROR_MSG)
                st.error(e)

        # Salary based on highest level of studies
        st.markdown("### Salario en base al máximo nivel de estudios")
        tabs = st.tabs(
            [
                "Salario Bruto",
                "Salario Neto",
            ]
        )
        with tabs[0]:
            df_aux = (
                df.loc[
                    (df[config.GROSS_SALARY].notna())
                    & (df[config.YEARS_OF_EXPERIENCE].notna())
                ]
                .groupby([config.MAX_LVL_STUDIES, config.YEARS_OF_EXPERIENCE])[
                    config.GROSS_SALARY
                ]
                .median()
                .reset_index()
            )

            if df_aux[config.YEARS_OF_EXPERIENCE].count() >= config.MINIMUM_RESPONSES:
                studies = np.unique(df[config.MAX_LVL_STUDIES])
                df_aux = (
                    df.loc[
                        (df[config.GROSS_SALARY].notna())
                        & (df[config.YEARS_OF_EXPERIENCE].notna())
                    ]
                    .groupby([config.MAX_LVL_STUDIES, config.YEARS_OF_EXPERIENCE])[
                        config.GROSS_SALARY
                    ]
                    .median()
                    .reset_index()
                )

                X = df_aux[config.YEARS_OF_EXPERIENCE].values.reshape(-1, 1) + 0.1
                y = df_aux[config.GROSS_SALARY].values.reshape(-1, 1)

                fig = px.scatter(
                    df_aux,
                    y=df_aux[config.GROSS_SALARY].values,
                    x=df_aux[config.YEARS_OF_EXPERIENCE].values,
                    color=df_aux[config.MAX_LVL_STUDIES].values,
                    opacity=1,
                    labels={
                        "x": config.YEARS_OF_EXPERIENCE,
                        "y": "MEDIANA del sueldo bruto segun experiencia y nivel de estudios",
                    },
                    title="tendencia de sueldos segun experiencia, separado por estudios",
                )

                modelos = {}
                for studie in studies:
                    if sum(df_aux[config.MAX_LVL_STUDIES] == studie) > 0:
                        X_genero = X[df_aux[config.MAX_LVL_STUDIES] == studie]
                        y_genero = y[df_aux[config.MAX_LVL_STUDIES] == studie]
                        modelos[studie] = LinearRegression()
                        modelos[studie].fit(np.log(X_genero), y_genero)

                for studie in studies:
                    if sum(df_aux[config.MAX_LVL_STUDIES] == studie) > 0:
                        angular_coefficient = modelos[studie].coef_[0]
                        intercept = modelos[studie].intercept_
                        fig.add_trace(
                            go.Scatter(
                                x=X[df_aux[config.MAX_LVL_STUDIES] == studie].flatten(),
                                y=angular_coefficient
                                * np.log(
                                    X[df_aux[config.MAX_LVL_STUDIES] == studie] + 0.1
                                ).flatten()
                                + intercept,
                                mode="lines",
                                name=studie,
                            )
                        )

                try:
                    st.plotly_chart(fig, theme=None)
                except Exception as e:
                    st.error(config.ERROR_MSG)
                    st.error(e)
        with tabs[1]:
            df_aux = (
                df.loc[
                    (df[config.NET_SALARY].notna())
                    & (df[config.YEARS_OF_EXPERIENCE].notna())
                ]
                .groupby([config.MAX_LVL_STUDIES, config.YEARS_OF_EXPERIENCE])[
                    config.NET_SALARY
                ]
                .median()
                .reset_index()
            )

            if df_aux[config.YEARS_OF_EXPERIENCE].count() >= config.MINIMUM_RESPONSES:
                studies = np.unique(df[config.MAX_LVL_STUDIES])
                df_aux = (
                    df.loc[
                        (df[config.NET_SALARY].notna())
                        & (df[config.YEARS_OF_EXPERIENCE].notna())
                    ]
                    .groupby([config.MAX_LVL_STUDIES, config.YEARS_OF_EXPERIENCE])[
                        config.NET_SALARY
                    ]
                    .median()
                    .reset_index()
                )

                X = df_aux[config.YEARS_OF_EXPERIENCE].values.reshape(-1, 1) + 0.1
                y = df_aux[config.NET_SALARY].values.reshape(-1, 1)

                fig = px.scatter(
                    df_aux,
                    y=df_aux[config.NET_SALARY].values,
                    x=df_aux[config.YEARS_OF_EXPERIENCE].values,
                    color=df_aux[config.MAX_LVL_STUDIES].values,
                    opacity=1,
                    labels={
                        "x": config.YEARS_OF_EXPERIENCE,
                        "y": "MEDIANA del sueldo bruto segun experiencia y nivel de estudios",
                    },
                    title="tendencia de sueldos segun experiencia, separado por estudios",
                )

                modelos = {}
                for studie in studies:
                    if sum(df_aux[config.MAX_LVL_STUDIES] == studie) > 0:
                        X_genero = X[df_aux[config.MAX_LVL_STUDIES] == studie]
                        y_genero = y[df_aux[config.MAX_LVL_STUDIES] == studie]
                        modelos[studie] = LinearRegression()
                        modelos[studie].fit(np.log(X_genero), y_genero)

                for studie in studies:
                    if sum(df_aux[config.MAX_LVL_STUDIES] == studie) > 0:
                        angular_coefficient = modelos[studie].coef_[0]
                        intercept = modelos[studie].intercept_
                        fig.add_trace(
                            go.Scatter(
                                x=X[df_aux[config.MAX_LVL_STUDIES] == studie].flatten(),
                                y=angular_coefficient
                                * np.log(
                                    X[df_aux[config.MAX_LVL_STUDIES] == studie] + 0.1
                                ).flatten()
                                + intercept,
                                mode="lines",
                                name=studie,
                            )
                        )

                try:
                    st.plotly_chart(fig, theme=None)
                except Exception as e:
                    st.error(config.ERROR_MSG)
                    st.error(e)

        # Bootcamp
        st.markdown("### Bootcamp :books:")
        tabs = st.tabs([config.BOOTCAMP, "¿Cual?", config.TRAINING_IN])

        with tabs[0]:
            try:
                serie = df[config.BOOTCAMP].notna().value_counts().reset_index()

                serie["index"].replace({True: "Si", False: "No"}, inplace=True)
                # serie
                fig = px.pie(
                    serie,
                    names=serie["index"],
                    values=serie[config.BOOTCAMP],
                    hole=0.4,
                )

                fig.update(layout_title_text=config.BOOTCAMP)

                st.plotly_chart(fig, theme=None)

            except Exception as e:
                st.error(config.ERROR_MSG)
                st.error(e)

        with tabs[1]:
            if len(df[df[config.BOOTCAMP].notna()]) == 0:
                st.warning("Faltan muestras, no fue posible desplegar el gráfico.")
            else:
                try:
                    st.plotly_chart(
                        streamlit_figures.get_vertical_graph_from_serie(
                            serie=pd.Series(
                                sum(
                                    df[df[config.BOOTCAMP].notnull()][
                                        config.BOOTCAMP
                                    ].apply(
                                        lambda x: x.split(" - ")
                                        if type(x) == str
                                        else x
                                    ),
                                    [],
                                )
                            ).value_counts(),
                            title=config.BOOTCAMP,
                        ),
                        theme=None,
                    )
                except Exception as e:
                    st.error(config.ERROR_MSG)
                    st.error(e)

        with tabs[2]:
            try:
                st.plotly_chart(
                    streamlit_figures.get_vertical_graph_from_serie(
                        df[config.TRAINING_IN].value_counts(),
                        "¿De que trato Boot Camp?",
                    ),
                    theme=None,
                )
            except Exception as e:
                st.error(config.ERROR_MSG)
                st.error(e)

        # Contrato laboral
        st.markdown("### Contrato laboral :scroll:")
        tabs = st.tabs(
            [
                config.CONTRACT,
                config.EMPLOYMENT_STATUS,
                config.WORK_MODALITY,
                "¿Cuántos días a la semana vas a la oficina?",
                config.ORGANIZATION_SIZE,
            ]
        )

        with tabs[0]:
            if config.CONTRACT not in df.columns:
                st.warning(
                    f"No se encuentra la columna {config.CONTRACT} en el archivo"
                )
            else:
                try:
                    st.plotly_chart(
                        streamlit_figures.get_pie(
                            df[config.CONTRACT].value_counts(), title=config.CONTRACT
                        ),
                        theme=None,
                    )
                except Exception as e:
                    st.error(config.ERROR_MSG)
                    st.error(e)
        with tabs[1]:
            if config.EMPLOYMENT_STATUS not in df.columns:
                st.warning(
                    f"No se encuentra la columna {config.EMPLOYMENT_STATUS} en el archivo"
                )
            else:
                try:
                    st.plotly_chart(
                        streamlit_figures.get_pie(
                            df[config.EMPLOYMENT_STATUS].value_counts(),
                            title=config.CONTRACT,
                        ),
                        theme=None,
                    )
                    st.markdown(
                        f"***Encuestados totales: {df[config.EMPLOYMENT_STATUS].count()}***"
                    )
                except Exception as e:
                    st.error(config.ERROR_MSG)
                    st.error(e)
        with tabs[2]:
            if config.WORK_MODALITY not in df.columns:
                st.warning(
                    f"No se encuentra la columna {config.WORK_MODALITY} en el archivo"
                )
            else:
                try:
                    st.plotly_chart(
                        streamlit_figures.get_pie(
                            df[config.WORK_MODALITY].value_counts(),
                            title=config.WORK_MODALITY,
                        ),
                        theme=None,
                    )
                except Exception as e:
                    st.error(config.ERROR_MSG)
                    st.error(e)
        with tabs[3]:
            if (
                config.DAYS_IN_OFFICE in df.columns
                and "Híbrido (presencial y remoto)" in df[config.WORK_MODALITY].unique()
            ):
                try:
                    st.plotly_chart(
                        streamlit_figures.get_horizontal_histogram(
                            df[
                                df[config.WORK_MODALITY]
                                == "Híbrido (presencial y remoto)"
                            ],
                            config.DAYS_IN_OFFICE + config.REWRITTEN_COLUMN_SUFFIX,
                            streamlit_order_plots.ORDER_5,
                        ),
                        theme=None,
                    )
                except Exception as e:
                    st.error(config.ERROR_MSG)
                    st.error(e)
            else:
                st.warning(
                    f"No se encuentra la columna {config.DAYS_IN_OFFICE} en el archivo"
                )
        with tabs[4]:
            if config.DEPENDENTS not in df.columns:
                st.warning(
                    f"No se encuentra la columna {config.DEPENDENTS} en el archivo"
                )
            else:
                try:
                    st.plotly_chart(
                        streamlit_figures.get_horizontal_histogram(
                            df,
                            config.DEPENDENTS + config.REWRITTEN_COLUMN_SUFFIX,
                            streamlit_order_plots.FIBO_ORDER,
                        ),
                        theme=None,
                    )
                except Exception as e:
                    st.error(config.ERROR_MSG)
                    st.error(e)

        # Herramientas
        st.markdown("### Herramientas :toolbox:")
        tabs = st.tabs(
            [
                "Plataformas",
                "Lenguajes",
                "Frameworks",
                config.DATABASES_COLUMN,
                "Testing",
            ]
        )

        with tabs[0]:
            try:
                st.plotly_chart(
                    streamlit_figures.get_vertical_graph_from_serie(
                        pd.Series(
                            sum(
                                df[df[config.PLATFORMS_COLUMN].notnull()][
                                    config.PLATFORMS_COLUMN
                                ].apply(
                                    lambda x: x.split(" - ") if type(x) == str else x
                                ),
                                [],
                            )
                        ).value_counts(),
                        config.PLATFORMS_COLUMN,
                    ),
                    use_container_width=True,
                    theme=None,
                )
            except Exception as e:
                st.error(config.ERROR_MSG)
                st.error(e)
        with tabs[1]:
            try:
                st.plotly_chart(
                    streamlit_figures.get_vertical_graph_from_serie(
                        pd.Series(
                            sum(
                                df[df[config.LANGUAGES].notnull()][
                                    config.LANGUAGES
                                ].apply(
                                    lambda x: x.split(" - ") if type(x) == str else x
                                ),
                                [],
                            )
                        ).value_counts(),
                        config.LANGUAGES,
                    ),
                    use_container_width=True,
                    theme=None,
                )
            except Exception as e:
                st.error(config.ERROR_MSG)
                st.error(e)
        with tabs[2]:
            try:
                st.plotly_chart(
                    streamlit_figures.get_vertical_graph_from_serie(
                        pd.Series(
                            sum(
                                df[df[config.FRAMEWORKS].notnull()][
                                    config.FRAMEWORKS
                                ].apply(
                                    lambda x: x.split(" - ") if type(x) == str else x
                                ),
                                [],
                            )
                        ).value_counts(),
                        title=config.FRAMEWORKS,
                    ),
                    use_container_width=True,
                    theme=None,
                )
            except Exception as e:
                st.error(config.ERROR_MSG)
                st.error(e)
        with tabs[3]:
            try:
                st.plotly_chart(
                    streamlit_figures.get_vertical_graph_from_serie(
                        pd.Series(
                            sum(
                                df[df[config.DATABASES_COLUMN].notnull()][
                                    config.DATABASES_COLUMN
                                ].apply(
                                    lambda x: x.split(" - ") if type(x) == str else x
                                ),
                                [],
                            )
                        ).value_counts(),
                        title=config.DATABASES_COLUMN,
                    ),
                    use_container_width=True,
                    theme=None,
                )
            except Exception as e:
                st.error(config.ERROR_MSG)
                st.error(e)
        with tabs[4]:
            try:
                st.plotly_chart(
                    streamlit_figures.get_vertical_graph_from_serie(
                        pd.Series(
                            sum(
                                df[df[config.QA].notnull()][config.QA].apply(
                                    lambda x: x.split(" - ") if type(x) == str else x
                                ),
                                [],
                            )
                        ).value_counts(),
                        title=config.QA,
                    ),
                    use_container_width=True,
                    theme=None,
                )
            except Exception as e:
                st.error(config.ERROR_MSG)
                st.error(e)

        # Bono y beneficios
        st.markdown("### Bonos y Beneficios :gift:")
        tabs = st.tabs([config.BONUS, "Beneficios"])

        with tabs[0]:
            try:
                st.plotly_chart(
                    streamlit_figures.get_pie(
                        df[config.BONUS].value_counts(),
                        title="¿Recibís algún tipo de bono?",
                    ),
                    theme=None,
                )
            except Exception as e:
                st.error(config.ERROR_MSG)
                st.error(e)
        with tabs[1]:
            try:
                st.plotly_chart(
                    streamlit_figures.get_vertical_graph_from_serie(
                        pd.Series(
                            sum(
                                df[df[config.BENEFITS].notnull()][
                                    config.BENEFITS
                                ].apply(
                                    lambda x: x.split(" - ") if type(x) == str else x
                                ),
                                [],
                            )
                        ).value_counts(),
                        title="Beneficios",
                    ),
                    use_container_width=True,
                    theme=None,
                )
            except Exception as e:
                st.error(config.ERROR_MSG)
                st.error(e)

        # Conformidad salarial
        st.markdown("### Conformidad salarial:+1::-1:")
        tabs = st.tabs(
            [
                "Conformidad salarial",
                "Conformidad salarial semestral",
                config.WORKPLACE_RECOMMENDATION,
            ]
        )

        with tabs[0]:
            try:
                st.plotly_chart(
                    streamlit_figures.get_horizontal_histogram(
                        df,
                        config.SALARY_COMPLIANCE + config.REWRITTEN_COLUMN_SUFFIX,
                        streamlit_order_plots.ORDER_1_4,
                    ),
                    theme=None,
                )
            except Exception as e:
                st.error(config.ERROR_MSG)
                st.error(e)
        with tabs[1]:
            try:
                st.plotly_chart(
                    streamlit_figures.get_horizontal_histogram(
                        df,
                        config.SEMI_ANNUAL_SALARY_COMPLIANCE
                        + config.REWRITTEN_COLUMN_SUFFIX,
                        streamlit_order_plots.ORDER_1_4,
                    ),
                    theme=None,
                )
            except Exception as e:
                st.error(config.ERROR_MSG)
                st.error(e)

        with tabs[2]:
            try:
                st.plotly_chart(
                    streamlit_figures.get_horizontal_histogram(
                        df,
                        config.WORKPLACE_RECOMMENDATION
                        + config.REWRITTEN_COLUMN_SUFFIX,
                        streamlit_order_plots.ORDER_0_10,
                    ),
                    theme=None,
                )
            except Exception as e:
                st.error(config.ERROR_MSG)
                st.error(e)

        #  Tamaño de las empresas
        st.markdown("### Tamaño de las empresas :office:")
        tabs = st.tabs(["Tamaño empresa", "Salario bruto segun tamaño de la empresa"])

        with tabs[0]:
            try:
                st.plotly_chart(
                    streamlit_figures.get_horizontal_histogram(
                        df, config.ORGANIZATION_SIZE, streamlit_order_plots.COMPANY_SIZE
                    ),
                    theme=None,
                )
            except Exception as e:
                st.error(config.ERROR_MSG)
                st.error(e)
        with tabs[1]:
            try:
                median_salary = df.groupby(config.ORGANIZATION_SIZE)[
                    config.GROSS_SALARY
                ].median()

                fig = px.histogram(
                    median_salary,
                    y=median_salary.values,
                    x=median_salary.index,
                    opacity=1,
                    labels={
                        "y": "cantidad de encuestados",
                        "x": "Valores salariales",
                    },
                    title="Salario bruto segun tamaño de la empresa",
                )
                fig.update_xaxes(
                    categoryorder="array",
                    categoryarray=streamlit_order_plots.COMPANY_SIZE,
                )
                st.plotly_chart(fig, theme=None)
            except Exception as e:
                st.error(config.ERROR_MSG)
                st.error(e)

    return container
