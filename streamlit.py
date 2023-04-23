import streamlit as st
import config

#
st.title("Resultados de la Encuesta Sysarmy")
st.markdown("---")
st.markdown("""##### **Consulta los resultados, aplicar filtros y gestionar archivos para obtener la información que necesitas.**""")
st.markdown("***Podes encontrar los informes mas elaborados de las encuestas hechos por Openqube [aca](https://sueldos.openqube.io/encuesta-sueldos-2023.01/)***")

st.markdown("---")

st.markdown("#### Sobre Sysarmy:")
st.markdown("Sysarmy es la comunidad de sistemas que nuclea a profesionales del área para favorecer el contacto y el intercambio de conocimiento de manera informal. [Su Blog!](https://sysarmy.com/blog/)")

st.markdown("###  ")

st.markdown("### Sobre este proyecto:")
st.markdown("Complementar la informacion de Openqube sobre los salarios en el sector IT, en función de la posición y características individuales, para tener una visión más completa y detallada.")
st.markdown("---")

#
st.markdown("## Páginas:")
st.markdown("#### Resultados Generales")

st.write("Se muestran los gráficos con todos los resultados de la encuesta seleccionada.")

st.markdown("#### Filtros")

st.write("En esta sección podes agregar filtros a los datos de la encuesta seleccionada para obtener resultados más específicos.")

st.markdown("#### Archivos")

st.write("Puedes agregar archivos al programa o borrarlos")

st.markdown("---")
st.markdown("##### Detalles extra:")

st.write("Podes hacer las modificaciones necesarias en:")
st.write(config.CONFIG_FILE)
