import time

import pandas as pd
import streamlit as st
from pathlib import Path

import config
from transform_data.transform_data import main


if "file_name" not in st.session_state:
    st.session_state["file_name"] = False
if "show_buttons" not in st.session_state:
    st.session_state["show_buttons"] = False
if "disable_load" not in st.session_state:
    st.session_state["disable_load"] = True
if "rename_button" not in st.session_state:
    st.session_state["rename_button"] = False
if "file" not in st.session_state:
    st.session_state["file"] = False

st.subheader("Cargar archivos")

file = st.file_uploader("Cargar archivo", type=["csv"])
if file:
    st.write(st.session_state["rename_button"])

    if file or (file and file.name != st.session_state["file_name"]):
        st.session_state["file_name"] = file.name
        try:
            df = pd.read_csv(file)
        except Exception as e:
            st.error(e)
            st.stop()

        # skip the first blank lines when searching for the survey questions
        if df.columns.str.contains("Unnamed").any() or not set(
            config.REQUIRED_COLUMNS
        ).issubset(df.columns):
            for index, row in df.iterrows():
                if row.notnull().all() and any(
                    column not in df.columns for column in config.REQUIRED_COLUMNS
                ):
                    try:
                        df.columns = df.iloc[index]
                        df = df.rename(columns=lambda x: x.replace("  ", " ").rstrip())
                        df = df.iloc[(index + 1):, :]
                        # rename columns based on constants.SAME_COLUMNS
                        df.rename(columns=config.SAME_COLUMNS, inplace=True)
                        if "¿Salir o seguir contestando?" in df.columns:
                            df.drop(
                                "¿Salir o seguir contestando?", axis=1, inplace=True
                            )
                        st.session_state["file"] = df
                        break
                    except Exception as e:
                        st.error(e)
                        st.stop()

                # stop searching
                if index == 25:
                    st.error(
                        "No se encontró ninguna de las columnas correspondientes a la encuesta de sysarmy"
                    )
                    st.stop()

        # create folder if not exist
        if not config.FOLDER_PATH.exists():
            config.FOLDER_PATH.mkdir(parents=True)

    # display form to rename columns to supported columns
    if type(st.session_state["file"]) == pd.DataFrame:
        if not set(config.REQUIRED_COLUMNS).issubset(st.session_state["file"].columns):
            # st.session_state["disable_load"] = True
            missing_columns = list(
                set(config.REQUIRED_COLUMNS) - set(st.session_state["file"].columns)
            )
            leftover_columns = list(
                set(st.session_state["file"].columns) - set(config.REQUIRED_COLUMNS)
            )

            rename_dict = {}

            with st.form("select missing column"):
                st.markdown(
                    r"""Es posible que alguna columna esté escrita de manera diferente.
                            Seleccione la columna que mejor responda: """
                )
                for column in missing_columns:
                    leftover_column = st.selectbox(column, leftover_columns, key=column)
                    rename_dict[leftover_column] = column
                submit = st.form_submit_button("Renombrar")

            if submit:
                st.session_state["rename_button"] = rename_dict

        else:
            st.success("Estan todas las columnas necesarias.")
            st.session_state["disable_load"] = False

        if st.session_state["rename_button"]:
            st.markdown("#### Se renombraron las columnas:")
            st.write(rename_dict)
            st.session_state["disable_load"] = False

        add_dollar_values = st.checkbox(
            "Agregar valores del dolar", disabled=st.session_state["disable_load"]
        )

        if add_dollar_values:
            st.markdown(
                "**:green[Podes encontrar los valores historicos en:]** https://www.dolarito.ar/cotizaciones-historicas/oficial"
            )
            mep_dollar = st.number_input(
                "Agregar valor del Dólar Blue",
                disabled=st.session_state["disable_load"],
                key="mep_dollar",
            )
            blue_dollar = st.number_input(
                "Agregar valor del Dólar Oficial",
                disabled=st.session_state["disable_load"],
                key="blue_dollar",
            )
            official_dollar = st.number_input(
                "Agregar valor del Dólar MEP",
                disabled=st.session_state["disable_load"],
                key="official_dollar",
            )
        else:
            mep_dollar = None
            blue_dollar = None
            official_dollar = None

        transform = st.button(
            "Cargar archivo",
            type="primary",
            disabled=st.session_state["disable_load"],
            key="load_file",
        )

        if transform:
            if st.session_state["rename_button"]:
                st.session_state["file"].rename(columns=rename_dict, inplace=True)

            st.markdown("#### Se renombraron las columnas:")
            st.markdown("#### run transform:")
            st.session_state["disable_load"] = True
            st.session_state["rename_button"] = False

            if add_dollar_values:
                result = main(
                    st.session_state["file"],
                    st.session_state["file_name"],
                    mep_dollar,
                    blue_dollar,
                    official_dollar,
                )
            else:
                result = main(
                    st.session_state["file"], name=st.session_state["file_name"]
                )
            time.sleep(2)
            if result:
                st.balloons()
            else:
                st.error("No se pudo cargar el archivo")

            st.session_state["file"] = False
            st.session_state["file_name"] = False
            time.sleep(2)
            st.experimental_rerun()

        st.checkbox("prueba")
    st.write(type(st.session_state["file"]))

# DELETE FILE
st.subheader("Borrar Archivos")

with st.form("Seleccione un archivo para borrar"):
    delete_file = st.selectbox(
        "Seleccione un archivo para borrar",
        [file.name for file in config.FOLDER_PATH.glob("*")],
        key="list_of_files_to_delete",
    )

    delete_button = st.form_submit_button("Delete")

    if delete_button:
        delete_file = Path(config.FOLDER_PATH).joinpath(delete_file)
        st.write(delete_file)
        try:
            delete_file.unlink(missing_ok=False)
        except Exception as e:
            st.error(e)
        st.success("Se borro correctamente el archivo")


st.write("")
st.markdown("***Los archivos se guardan en:***")
st.write(config.FOLDER_PATH.absolute())
