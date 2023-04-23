import streamlit as st
import pandas as pd

import config
import graphics.streamlit_dashboard

if "file_name_to_load" not in st.session_state:
    st.session_state["file_name_to_load"] = None
if "dataframe" not in st.session_state:
    st.session_state["dataframe"] = None

# file form
st.markdown("# Filtros")
st.markdown("**En esta sección podes agregar filtros a los datos de la encuesta seleccionada para obtener resultados más específicos.**")
with st.form("seleccione un archivo"):
    select_file = st.selectbox(
        "Seleccione un archivo para borrar",
        [file.name for file in config.FOLDER_PATH.glob("*")],
        key="list_of_files_to_delete",
    )
    submit_f1 = st.form_submit_button("Cargar")
    if submit_f1:
        st.session_state["file_name_to_load"] = str(select_file)

if st.session_state["file_name_to_load"]:
    # Respondent filters form
    with st.form("formularioo"):
        # read the file
        file_name = st.session_state["file_name_to_load"]
        st.markdown("##### Archivo: ")
        st.markdown(f"###### *{file_name}*")
        path = config.FOLDER_PATH.joinpath(select_file)
        df = pd.read_csv(str(path))

        # filter positions to display
        jobs = df[config.POSITIONS].value_counts()
        otros_jobs = jobs[
            jobs.values <= config.MIN_NUMBER_OF_PARTICIPANTS_PER_JOB
        ].sum()
        other_jobs = pd.Series([otros_jobs], index=["Otros"])
        jobs_final = pd.concat(
            [
                jobs.loc[jobs.values > config.MIN_NUMBER_OF_PARTICIPANTS_PER_JOB],
                other_jobs,
            ]
        )

        role = st.selectbox(
            "Seleccione un rol", jobs.loc[jobs.values > 20].index, key="role"
        )
        ignore_roles = st.checkbox("Mostrar todos los roles")

        exp = st.slider(
            "Años de experiencia",
            min_value=int(df[config.YEARS_OF_EXPERIENCE].min()),
            max_value=int(df[config.YEARS_OF_EXPERIENCE].max()),
            value=(
                int(df[config.YEARS_OF_EXPERIENCE].min()),
                int(df[config.YEARS_OF_EXPERIENCE].max()),
            ),
            key="form_exp",
        )

        studies = st.selectbox(
            config.MAX_LVL_STUDIES,
            df[config.MAX_LVL_STUDIES].unique().tolist(),
            key="form_lvl_studies",
        )
        ignore_studies = st.checkbox("Ignorar estudios")

        if config.PAYMENTS_IN_DOLLARS in df.columns:
            type_of_salary = st.selectbox(
                config.PAYMENTS_IN_DOLLARS,
                df[config.PAYMENTS_IN_DOLLARS].unique().tolist(),
                key="form_payment",
            )
            ignore_payments = st.checkbox("Ignorar " + config.PAYMENTS_IN_DOLLARS)

        submit = st.form_submit_button(
            "Generar graficos",
        )

        st.session_state["dataframe"] = None

        if submit:
            # filter df
            min_exp, max_exp = exp
            df = df[df[config.YEARS_OF_EXPERIENCE].between(min_exp, max_exp)]
            if not ignore_roles:
                df = df[df[config.POSITIONS] == role]
            if config.PAYMENTS_IN_DOLLARS in df.columns and not ignore_payments:
                df = df[df[config.PAYMENTS_IN_DOLLARS] == type_of_salary]
            if not ignore_payments:
                df = df[df[config.MAX_LVL_STUDIES] == studies]

            length_df = len(df)

            if length_df == 0:
                st.error("No existen resultados en el archivo :(")
                st.session_state["dataframe"] = None
                st.stop()
            elif length_df <= config.MINIMUM_RESPONSES:
                st.warning(
                    f"""Se han encontrado {length_df} resultados.
                    Es posible que algunos gráficos no se muestren."""
                )
            elif length_df <= config.ADEQUATE_RESPONSES_INFO:
                st.info(
                    f"""Se encontraron {length_df} resultados.
                    Es posible que algunos gráficos no puedan
                    ser mostrados adecuadamente"""
                )
            else:
                st.success(f"Se encontraron {length_df} resultados")

            st.session_state["dataframe"] = df

if type(st.session_state["dataframe"]) == pd.DataFrame:
    st.markdown("---")
    st.markdown(f"# Resultado de: {file_name}")
    graphics.streamlit_dashboard.display_dashboard(st.session_state["dataframe"])
