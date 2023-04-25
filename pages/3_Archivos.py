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
if "saved file" not in st.session_state:
    st.session_state["saved file"] = False
if "rename_manually" not in st.session_state:
    st.session_state["rename_manually"] = False
if "file" not in st.session_state:
    st.session_state["file"] = False

st.markdown("# Archivos")
st.markdown("Agregar archivos al programa o borrarlos")
st.markdown("---")

# create folder if not exist
if not config.FOLDER_PATH.exists():
    config.FOLDER_PATH.mkdir(parents=True)

# Load file
st.subheader("Cargar archivos")
file = st.file_uploader("Cargar archivo", type=["csv"])

if not file:
    st.session_state["file_name"] = False
    st.session_state["saved file"] = False

elif file.name != st.session_state["file_name"]:
    # if :
    
    # read file
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
                    # Rename columns
                    df = df.rename(columns=lambda x: x.replace("  ", " ").rstrip())
                    df = df.iloc[(index + 1):, :]
                    # rename columns based on constants.SAME_COLUMNS
                    df.rename(columns=config.SAME_COLUMNS, inplace=True)

                    for column in df.columns:
                        if '¿Tuviste ajustes por inflación' in column or "¿Tuviste actualizaciones de tus ingresos" in column:
                            df.rename(columns={column: '¿Tuviste ajustes por inflación el último año?'}, inplace=True)
                    if "¿Salir o seguir contestando?" in df.columns:
                        df.drop(
                            "¿Salir o seguir contestando?", axis=1, inplace=True
                        )
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
    
    st.session_state["file"] = df
    st.session_state["file_name"] = file.name

if st.session_state["saved file"]:
    st.info("Archivo cargado")
    st.session_state["file"] = False

# display form to rename columns to supported columns
if type(st.session_state["file"]) == pd.DataFrame:

    # rename remaining columns manually
    if not set(config.REQUIRED_COLUMNS).issubset(st.session_state["file"].columns):
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
            st.session_state["rename_manually"] = rename_dict

    # Display the original column names along with the new names
    # that will be used to replace them
    if st.session_state["rename_manually"]:
        st.markdown("#### Se renombraron las columnas:")
        st.write(rename_dict)

    # Add dollar values inputs

    st.markdown(
        "**Podes encontrar los valores historicos en:** https://www.dolarito.ar/cotizaciones-historicas/oficial"
    )
    official_dollar = st.number_input(
        "Agregar valor del Dólar oficial",
        key="official_dollar",
    )
    blue_dollar = st.number_input(
        "Agregar valor del Dólar blue",
        key="blue_dollar",
    )
    mep_dollar = st.number_input(
        "Agregar valor del Dólar MEP",
        key="mep_dollar",
    )

    add_dollar_values = st.checkbox(
        "Ignorar valores del dolar",
    )
    if add_dollar_values:
        st.warning("""Los valores del dólar se utilizan como filtro para
            establecer los sueldos mínimos y máximos. Si no se incluyen,
            es posible que los gráficos muestren distorsiones
            significativas debido a datos corruptos.""")

        official_dollar = None
        blue_dollar = None
        mep_dollar = None

    transform = st.button(
        "Cargar archivo",
        type="primary",
        key="load_file",
    )

    if transform:
        if st.session_state["rename_manually"]:
            st.session_state["file"].rename(
                columns=st.session_state["rename_manually"],
                inplace=True
            )

        st.session_state["rename_manually"] = False

        with st.spinner("Cargando archivo al programa"):
            result = main(
                st.session_state["file"],
                st.session_state["file_name"],
                mep_dollar,
                blue_dollar,
                official_dollar,
            )
        st.session_state["file"] = False
        # st.session_state["file_name"] = False
        if result:
            st.success("Archivo subido correctamente")
            st.balloons()
            st.session_state["saved file"] = True
            time.sleep(2)
            st.experimental_rerun()
        else:
            st.error("No se pudo cargar el archivo")


st.markdown("##### Anteriores encuestas:")
st.markdown("*Los archivos se descargan desde el [repo](https://github.com/openqube/openqube-sueldos/tree/release-2023.01/data/csv/argentina) de Openqube*")

survey = st.selectbox(
    "Elegir encuesta:",
    config.SURVEYS.keys(),
    key="anteriores_encuestas"
)

download_n_transform = st.button("Descargar", key="download_n_transform", type="primary",)

if download_n_transform:
    with st.spinner("Cargando archivo al programa"):
        try:
            df = pd.read_csv(config.SURVEYS[survey]["url"])
        except Exception as e:
            st.error(f"""No se pude descargar el archivo 
                desde {config.SURVEYS[survey]["url"]}""")
            st.exception(e)
        df = df.rename(columns=lambda x: x.replace("  ", " ").rstrip())
        df.rename(columns=config.SAME_COLUMNS, inplace=True)

        for column in df.columns:
            if '¿Tuviste ajustes por inflación' in column or "¿Tuviste actualizaciones de tus ingresos" in column:
                df.rename(columns={column: '¿Tuviste ajustes por inflación el último año?'}, inplace=True)
        if "¿Salir o seguir contestando?" in df.columns:
            df.drop(
                "¿Salir o seguir contestando?", axis=1, inplace=True
            )

        try:
            result = main(
                df,
                survey,
                config.SURVEYS[survey]["dollar_values"][0],
                config.SURVEYS[survey]["dollar_values"][1],
                config.SURVEYS[survey]["dollar_values"][2],
            )
        except Exception as e:
            st.error(f"""No se pude cargar el archivo 
                {config.SURVEYS[survey]["url"]}""")
            st.exception(e)

        if result:
            st.success("Archivo subido correctamente")
            st.balloons()

st.markdown("---")
# DELETE FILE
st.subheader("Borrar Archivos")

with st.form("Seleccione un archivo para borrar"):
    delete_file = st.selectbox(
        "Seleccione un archivo para borrar",
        [file.name for file in config.FOLDER_PATH.glob("*")],
        key="list_of_files_to_delete",
    )
    disabled = False
    if not [file.name for file in config.FOLDER_PATH.glob("*")]:
        disabled = True
    delete_button = st.form_submit_button(
        "Borrar",
        disabled=disabled)

    if delete_button:
        st.session_state["saved file"] = False
        delete_file = Path(config.FOLDER_PATH).joinpath(delete_file)
        st.write(delete_file)
        try:
            delete_file.unlink(missing_ok=False)
        except Exception as e:
            st.error(e)
        st.success("Se borro correctamente el archivo")
        time.sleep(2)
        st.experimental_rerun()
