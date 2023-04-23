from pathlib import Path


# Save files in:
FOLDER_NAME = "Processed_Files"
FOLDER_PATH = Path(FOLDER_NAME)

# --- # --- #

# Transform data

# supported columns
COUNTRIES = "Estoy trabajando en"  # OPTIONAL
PROVINCES = "Dónde estás trabajando"
GROSS_SALARY = "Último salario mensual o retiro BRUTO (en tu moneda local)"
NET_SALARY = "Último salario mensual o retiro NETO (en tu moneda local)"
PAYMENTS_IN_DOLLARS = "Pagos en dólares"

LAST_VALUE_EXCHANGE = (
    "Si tu sueldo está dolarizado ¿Cuál fue el último valor del dólar que tomaron?"
)
SALARY_COMPLIANCE = "¿Qué tan conforme estás con tus ingresos laborales?"
SEMI_ANNUAL_SALARY_COMPLIANCE = "Cómo considerás que están tus ingresos laborales comparados con el semestre anterior"
BENEFITS = "Con qué beneficios contas"
POSITIONS = "Trabajo de"

YEARS_OF_EXPERIENCE = "Años de experiencia"
TIME_IN_CURRENT_COMPANY = "Antigüedad en la empresa actual"
TIME_IN_CURRENT_ROLE = "Tiempo en el puesto actual"
DEPENDENTS = "¿Cuántas personas a cargo tenés?"

LANGUAGES = "Lenguajes de programación o tecnologías que utilices en tu puesto actual"
FRAMEWORKS = "Frameworks, herramientas y librerías que utilices en tu puesto actual"
PLATFORMS_COLUMN = "Plataformas que utilizas en tu puesto actual"
DATABASES_COLUMN = "Bases de datos"
QA = "QA / Testing"

DAYS_IN_OFFICE = (
    "Si trabajás bajo un esquema híbrido ¿Cuántos días a la semana vas a la oficina?"
)
WORKPLACE_RECOMMENDATION = "¿La recomendás como un buen lugar para trabajar?"
MAX_LVL_STUDIES = "Máximo nivel de estudios"
STUDIES_STATE = "Estado"
CAREER = "Carrera"
UNIV = "Universidad"

BOOTCAMP = "¿Participaste de algún Boot Camp?"
TRAINING_IN = "Si participaste de un Boot Camp, ¿qué carrera estudiaste?"
U_HAVE_GUARDS = "¿Tenés guardias?"
AGE = "Tengo (edad)"
GENDER = "Me identifico (género)"

ORGANIZATION_SIZE = "Cantidad de personas en tu organización"
CONTRACT = "Tipo de contrato"
WORK_MODALITY = "Modalidad de trabajo"
BONUS = "Recibís algún tipo de bono"
EMPLOYMENT_STATUS = "Dedicación"

# Columns that do not change between each year's surveys
REQUIRED_COLUMNS = [
    # COUNTRIES,
    PROVINCES,
    GROSS_SALARY,
    NET_SALARY,
    # PAYMENTS_IN_DOLLARS,
    # LAST_VALUE_EXCHANGE,
    SEMI_ANNUAL_SALARY_COMPLIANCE,
    BENEFITS,
    SALARY_COMPLIANCE,
    POSITIONS,
    YEARS_OF_EXPERIENCE,
    TIME_IN_CURRENT_COMPANY,
    TIME_IN_CURRENT_ROLE,
    DEPENDENTS,
    PLATFORMS_COLUMN,
    LANGUAGES,
    FRAMEWORKS,
    DATABASES_COLUMN,
    QA,
    # DAYS_IN_OFFICE,
    WORKPLACE_RECOMMENDATION,
    MAX_LVL_STUDIES,
    STUDIES_STATE,
    CAREER,
    UNIV,
    BOOTCAMP,
    # TRAINING_IN,
    U_HAVE_GUARDS,
    AGE,
    GENDER,
    ORGANIZATION_SIZE,
    CONTRACT,
    BONUS,
]


# Rename columns in file to upload
SAME_COLUMNS = {
    "Salario mensual o retiro NETO (en tu moneda local)": NET_SALARY,
    "Salario mensual NETO (en tu moneda local)": NET_SALARY,
    "Salario mensual o retiro BRUTO (en tu moneda local)": GROSS_SALARY,
    "Salario mensual BRUTO (en tu moneda local)": GROSS_SALARY,
    "¿Qué tan conforme estás con tu sueldo?": SALARY_COMPLIANCE,
    "Años en la empresa actual": TIME_IN_CURRENT_COMPANY,
    "Cómo creés que está tu sueldo con respecto al último semestre": SEMI_ANNUAL_SALARY_COMPLIANCE,
    "Realizaste cursos de especialización": BOOTCAMP,
    "Nivel de estudios alcanzado": MAX_LVL_STUDIES,
    "¿Cuántas veces a la semana vas a trabajar a la oficina?": DAYS_IN_OFFICE,
    "Si trabajas bajo un esquema híbrido ¿Cuántos días a la semana vas a la oficina?": DAYS_IN_OFFICE,
    "Años en el puesto actual": TIME_IN_CURRENT_ROLE,
    "Plataformas": PLATFORMS_COLUMN,
    "Lenguajes de programación o tecnologías.": LANGUAGES,
    "¿Gente a cargo?": DEPENDENTS,
    "¿Cuál fue el último valor de dólar que tomaron?": LAST_VALUE_EXCHANGE,
    "Frameworks, herramientas y librerías": FRAMEWORKS,
    "Me identifico": GENDER,
    "Tengo": AGE,
    "Cantidad de empleados": ORGANIZATION_SIZE,
    "Lenguajes de programación": LANGUAGES,
    "Beneficios extra": BENEFITS,
}

# --- # --- #

# Transform data constants:

ARGENTINE_PROVINCES = [
    "Catamarca",
    "Chaco",
    "Chubut",
    "Ciudad Autónoma de Buenos Aires",
    "Córdoba",
    "Corrientes",
    "Entre Ríos",
    "Formosa",
    "Jujuy",
    "La Pampa",
    "La Rioja",
    "Mendoza",
    "Misiones",
    "Neuquén",
    "Provincia de Buenos Aires",
    "Río Negro",
    "Salta",
    "San Juan",
    "San Luis",
    "Santa Cruz",
    "Santa Fe",
    "Santiago del Estero",
    "Tierra del Fuego",
    "Tucumán",
]

# Added to the end of the column name when
# the column is modified to be displayed differently in streamlit.
REWRITTEN_COLUMN_SUFFIX = " (valores reescritos)"

# the values are grouped according to utils.to_fibonacci_category
COLUMNS_TO_CAREGORIZE_AS_FIBONACCI = [
    YEARS_OF_EXPERIENCE,
    TIME_IN_CURRENT_COMPANY,
    TIME_IN_CURRENT_ROLE,
    DEPENDENTS,
]

# these categories are those defined for the 2023 survey
VALID_GENDER_CATEGORIES = [
    "Varón Cis",
    "Mujer Cis",
    "Prefiero no decir",
    "No binarie",
    "Agénero",
    "Fluido",
    "Varón Trans",
    "Mujer Trans",
]
FILL_NO_VALID_GENDERS_WITH = "Respuesta no valida"

# The maximum number of repetitions in which
#  the data is considered of little value and replaced with FILL_WITH.
MIN_AMOUNT = 10
FILL_WITH = "Otros"
FILL_NULL_VALUES = "No responde"

# The ages are grouped from START to STOP in groups defined by STEP.
# being MAX and MIN the maximum and minimum age allowed
START_AGE = 20
STOP_AGE = 75
STEP_AGE = 5

MAX_AGE = 75
MIN_AGE = 18

# max and min salary in dollars that someone
# can earn per month
MAX_WAGE_IN_USD = 25000
MIN_WAGE_IN_USD = 150

# Any value above it will be replaced
# by this maximum value.
MAXIMUM_PEOPLE_IN_CHARGE = 200

MAXIMUM_YEARS_OF_EXPERIENCE = 50

# --- # --- #

# Streamlit chart constants

ERROR_MSG = "No se pudo desplegar el grafico"
MINIMUM_RESPONSES = 10
ADEQUATE_RESPONSES_INFO = 200
MIN_NUMBER_OF_PARTICIPANTS_PER_JOB = 20
