import streamlit as st
import pandas as pd

import config
import graphics.streamlit_dashboard

if "file_load_general_general" not in st.session_state:
    st.session_state["file_load_general"] = None

st.markdown("# Resultados generales")
st.markdown("**Se muestran los gráficos con todos los resultados de la encuesta seleccionada.**")
if [file.name for file in config.FOLDER_PATH.glob("*")]:
    # file form
    with st.form("seleccione un archivo"):
        select_file = st.selectbox(
            "Seleccione una encuesta",
            [file.name for file in config.FOLDER_PATH.glob("*")],
            key="list_of_files_to_delete",
        )

        submit = st.form_submit_button("Cargar")
        if submit:
            path = config.FOLDER_PATH.joinpath(select_file)
            st.session_state["file_load_general"] = pd.read_csv(str(path))
else:
    st.session_state["file_load_general"] = None
    st.info(f"No hay se encuentran archivos guardados en: {str(config.FOLDER_PATH.absolute())}, cargalos en la seccion ***Archivos***.")

if type(st.session_state["file_load_general"]) == pd.DataFrame:
    st.markdown("---")
    st.markdown(f"# Resultado de: {select_file}")
    graphics.streamlit_dashboard.display_dashboard(
        st.session_state["file_load_general"]
    )
