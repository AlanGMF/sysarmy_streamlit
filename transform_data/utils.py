import re
import numpy as np


def extract_numbers(string: str) -> str:
    """
    Extracts numbers from a string and returns either the extracted
    number as a string or NaN if no number or multiple numbers are found.

    :param string: The string to search for a number.
    :type string: str
    :return: If a single number is found, it is returned as a string.
        Otherwise, np.NaN is returned.
    :rtype: str or np.NaN
    """
    numbers = re.findall(r'\d+(?:,\d{2})?', string.replace(",", "."))

    if len([int(number) for number in numbers]) == 1:
        return str([int(number) for number in numbers][0])

    return np.NaN


def replace_list_values(
            list_of_values: list[str],
            list_of_valid_values: list[str],
            fill: str, function
        ) -> list[str]:
    """Replace values in a list based on a provided function.

    :param list_of_values: A list of values to be replaced.
    :type list_of_values: list[str]
    :param list_of_valid_values: A list of valid values.
    :type list_of_valid_values: list[str]
    :param fill: A value to fill in for invalid values.
    :type fill: str
    :param function: A function to apply on each value in the list_of_values.
    :type function: function
    :return: A list of values with replacements applied.
    :rtype: list[str]
    """
    if type(list_of_values) != list:
        return list_of_values

    for index, values in enumerate(list_of_values):

        fix_value = function(values)

        if fix_value not in list_of_valid_values:
            list_of_values[index] = fill
        else:
            list_of_values[index] = fix_value

    # if all the values in the list are the same
    # return a list with this single value
    if len(list_of_values) > 1 and (
                all(element == list_of_values[0] for element in list_of_values)
            ):
        return [list_of_values[0]]

    return list_of_values


def cut_string(string: str) -> list[str]:
    """Splits a comma-separated string into a list of strings,
    and groups together any substrings that are enclosed in parentheses.

    :param string: The comma-separated string to be split.
    :type string: str
    :return: A list of strings, where each element is either a standalone
             substring, or a substring enclosed in parentheses that was
             grouped together with other substrings in the original string.
    :rtype: list[str]
    """
    if type(string) != str:
        return string

    separator = ', '
    strings_list = string.split(separator)

    i = 0
    while i < len(strings_list):
        if '(' in strings_list[i] and ')' not in strings_list[i]:
            j = i + 1
            while j < len(strings_list) and ')' not in strings_list[j]:
                j += 1
            strings_list[i:j+1] = [separator.join(strings_list[i:j+1])]
        i += 1

    return strings_list


def fix_benefit_name(benefit: str) -> str:
    """Fixes the name of a benefit based on rules.

    :param benefit: The original name of the benefit.
    :type benefit: str
    :return: The fixed name of the benefit.
    :rtype: str
    """
    if (
            ("obra" in benefit.lower() and "social" in benefit.lower()) or
            ("prepaga" in benefit.lower())
            ):
        return "Obra Social Prepaga"
    if (
            (
                "home" in benefit.lower() and
                ("office" in benefit.lower() or "working" in benefit.lower())
                ) or
            ("remoto" in benefit.lower())
            ):
        return "Home office"
    if (
            (
                ("día" in benefit.lower() or "dia" in benefit.lower()) and
                "cumple" in benefit.lower()) or
            ("cumpleaños" in benefit.lower())
            ):
        return "Día de cumpleaños libre"
    if ("viernes" in benefit.lower() and "f" in benefit.lower()):
        return "Horarios flexibles"
    if (
            ("día" in benefit.lower() or "dia" in benefit.lower()) and
            ("off" in benefit.lower() or "libre" in benefit.lower())
            ):
        return "Días off"
    if ("caja" in benefit.lower() and "navid" in benefit.lower()):
        return "Caja Navideña"
    if (
            ("día" in benefit.lower() or "dia" in benefit.lower()) and
            ("4" in benefit.lower())
            ):
        return "Semana laboral de 4 días"
    elif ("masajes" in benefit.lower()):
        return "Masajes"
    elif benefit.lower().startswith("no "):
        return "No utilizo"

    return benefit


def group_jobs(job: str) -> str:
    """This function takes a string that represents a job
    and returns a string that represents the group of the job.
    If the input parameter is not a string, it is returned
    unchanged.

    :param career: The name of the career to evaluate.
    :type career: str
    :return: A string representing the group of the career.
    :rtype: str
    """
    if type(job) != str:
        return job

    if (
            ("devops" in job.lower()) or
            ("infra" in job.lower()) or
            ("sysadmin" in job.lower())
            ):
        return "SysAdmin / DevOps / SRE"
    if "manager" in job.lower():
        return 'Manager / Director'
    if "rpa" in job.lower():
        return 'RPA'
    if "full" in job.lower():
        return "Fullstack"
    if "cloud" in job.lower():
        return 'Cloud Engineer'
    if (
            ("cyber" in job.lower()) or
            ("secur" in job.lower()) or
            ("ciber" in job.lower()) or
            ("pentest" in job.lower()) or
            ("seg" in job.lower() and "inf" in job.lower())
            ):
        return "Cybersecurity"
    if ("ux" in job.lower()) or ("designer" in job.lower()):
        return 'UX/UI Designer'
    if "lead" in job.lower() or "lider" in job.lower():
        return 'Technical Leader'
    if ("dba" in job.lower()) or ("BD" in job):
        return "DBA"
    if ("soport" in job.lower()) or ("supp" in job.lower()):
        return "Soporte IT"
    if ("test" in job.lower()) or ("qa" in job.lower()):
        return "QA / Tester"
    if (
            ("CIO" in job) or
            ("CEO" in job) or
            ("CTO" in job) or
            "c-" in job.lower()
            ):
        return "VP / C-Level"
    if (
            ("machin" in job.lower()) or
            ("nlp" in job.lower()) or
            ("mlops" in job.lower()) or
            ("AI" in job)
            ):
        return "Machine Learning Engineer"
    if "help" in job.lower():
        return "HelpDesk"
    if (
            ("funcion" in job and "analista" in job.lower()) or
            ("funcion" in job.lower()) or
            ("functional" in job.lower())
            ):
        return "Analista Funcional"
    if "developer" in job.lower():
        return "Developer"
    if "writer" in job.lower():
        return 'Technical Writer'

    return job


def fix_platform_name(platform: str) -> str:
    """Fixes the name of a platform based on provided rules.

    :param platform: The original name of the platform.
    :type platform: str
    :return: The fixed name of the platform.
    :rtype: str
    """
    if type(platform) != str:
        return platform

    if "office" in platform.lower() or "o365" in platform.lower():
        return "Office 365"
    elif "teradata" in platform.lower():
        return "Teradata"
    elif "cisco" in platform.lower():
        return "Cisco"
    elif "sas" in platform.lower():
        return "SAS"
    elif "azure" in platform.lower():
        return "Azure"
    elif "figma" in platform.lower():
        return "Figma"
    elif "odoo" in platform.lower():
        return "Odoo"
    elif "postman" in platform.lower():
        return "Postman"
    elif "microstrategy" in platform.lower():
        return "Microstrategy"
    elif "excel" in platform.lower():
        return "Excel"
    elif "jira" in platform.lower():
        return "Jira"
    elif "oracle" in platform.lower():
        return "Oracle"
    elif "fortinet" in platform.lower():
        return "Fortinet"
    elif "grafana" in platform.lower():
        return "Grafana"
    elif "gitlab" in platform.lower():
        return "Gitlab"
    elif "informatica" in platform.lower():
        return "Informatica"
    elif "miro" in platform.lower():
        return "Miro"
    elif "databricks" in platform.lower():
        return "Databricks"
    elif "uipath" in platform.lower():
        return "UiPath"
    elif "aws" in platform.lower():
        return "Amazon Web Services"
    elif "plesk" in platform.lower():
        return "Plesk"
    elif "confluen" in platform.lower():
        return "Confluence"
    elif "terraform" in platform.lower():
        return "Terraform"
    elif "crm" in platform.lower():
        return "CRM"
    elif "looker" in platform.lower():
        return "Looker"
    elif "microtik" in platform.lower() or "mikrotik" in platform.lower():
        return "Mikrotik"
    elif "qlik" in platform.lower():
        return "Qlik View/ Qlik Sense"
    elif "pl" in platform.lower() and "sql" in platform.lower():
        return "PL/ SQL"
    elif "click" in platform.lower() and "up" in platform.lower():
        return "ClickUp"
    elif "service" in platform.lower() and "now" in platform.lower():
        return "ServiceNow"
    elif "power" in platform.lower() and "bi" in platform.lower():
        return "Power BI"
    elif "github" in platform.lower() and "action" in platform.lower():
        return "Github Actions"
    elif "control" in platform.lower() and "m" in platform.lower():
        return "Control-M"
    elif "virtual" in platform.lower() and "box" in platform.lower():
        return "VirtualBox"
    elif "big" in platform.lower() and "query" in platform.lower():
        return "BigQuery"
    elif "android" in platform.lower() and "studio" in platform.lower():
        return "Android Studio"
    elif (
            ("visual" in platform.lower() and "studio" in platform.lower()) or
            "vsc" in platform.lower()
            ):
        return "Visual Studio"
    return platform


def fix_languages_name(languages: str) -> str:
    """Fixes the name of a programming language based on provided rules.

    :param platform: The original name of the programming language.
    :type platform: str
    :return: The fixed name of the programming language.
    :rtype: str
    """
    if type(languages) != str:
        return languages

    if "pl" in languages.lower() and "sql" in languages.lower():
        return "PL/ SQL"
    elif "visual" in languages.lower() and "fox" in languages.lower():
        return "Visual Fox Pro"
    elif "visual" in languages.lower() and "basic" in languages.lower():
        return "Visual Basic"
    elif "power" in languages.lower() and "shell" in languages.lower():
        return "PowerShell"
    elif (
            "power" in languages.lower() and
            ("script" in languages.lower() or "builder" in languages.lower())
            ):
        return "PowerScript"
    elif "sas" in languages.lower():
        return "SAS"
    elif "qlik" in languages.lower():
        return "Qlik"
    elif "excel" in languages.lower():
        return "Excel"
    elif "oracle" in languages.lower():
        return "Oracle"
    elif "dax" in languages.lower():
        return "Dax"

    return languages


def fix_framework_name(framework: str) -> str:
    """Fixes the name of the frameworks based on provided rules.

    :param platform: The original name of the frameworks.
    :type platform: str
    :return: The fixed name the frameworks.
    :rtype: str
    """
    if type(framework) != str:
        return framework

    lower_framework = framework.lower()

    if "nest" in lower_framework:
        return "Nest Js"
    if "svelte" in lower_framework:
        return "Svelte Js"
    if "jira" in lower_framework:
        return "Jira"
    if "yii" in lower_framework:
        return "Yii"
    if "symfony" in lower_framework:
        return "Symfony"
    if "angular" in lower_framework:
        return "Angular"
    if ".net" in lower_framework:
        return ".NET Core"
    elif "tailwind" in lower_framework:
        return "Tailwind"
    elif "react" in lower_framework and "native" in lower_framework:
        return "React Native"
    elif "pho" in lower_framework and "ix" in lower_framework:
        return "Phoenix "
    elif "material" in lower_framework and "ui" in lower_framework:
        return "Material UI"
    elif "react" in lower_framework:
        return "React.js"
    elif (
            "gin" in lower_framework and
            (len(lower_framework.strip()) == 3 or "gonic" in lower_framework)
            ):
        return "Gin Gonic"
    elif "spring" in lower_framework and "boot" in lower_framework:
        return "Spring Boot"
    elif "fast" in lower_framework and "api" in lower_framework:
        return "FastAPI"
    elif "oracle" in lower_framework:
        return "Oracle"
    elif "vert" in lower_framework:
        return "Vertx"
    elif "xamarin" in lower_framework:
        return "Xamarin"
    elif "micronaut" in lower_framework:
        return "Micronaut"
    elif "grails" in lower_framework:
        return "Grails"
    elif "play" in lower_framework:
        return "Play Framework"
    elif "unity" in lower_framework:
        return "Unity"
    elif len(lower_framework) < 2 or "ningun" in lower_framework:
        return "Ninguno de los anteriores"
    elif "pandas" in lower_framework or "numpy" in lower_framework:
        return "Pandas/ Numpy"

    return framework


def fix_DB_name(db_name: str) -> str:
    """Fixes the name of a database based on provided rules.

    :param db_name: The original name of the database.
    :type db_name: str
    :return: The fixed name of the database.
    :rtype: str
    """
    if type(db_name) != str:
        return db_name

    db_name_lower = db_name.lower()

    if "big" in db_name_lower and "query" in db_name_lower:
        return "BigQuery"
    if "sql" in db_name_lower and "server" in db_name_lower:
        return "Microsoft SQL Server"
    if "fire" in db_name_lower and "bird" in db_name_lower:
        return "Firebird"
    if "fire" in db_name_lower and "base" in db_name_lower:
        return "Firebase"
    if "soql" in db_name_lower or "salesforce" in db_name_lower:
        return "SOQL"
    if "influxdb" in db_name_lower or "influx" in db_name_lower:
        return "InfluxDB"
    if "snowf" in db_name_lower:
        return "Snowflake"
    elif db_name_lower.startswith("no ") or len(db_name_lower) < 2:
        return "Ninguna de las anteriores"

    return db_name


def fix_testing_tool_name(tool: str) -> str:
    """Fixes the name of a testing tool based on provided rules.

    :param db_name: The original name of the testing tool.
    :type db_name: str
    :return: The fixed name of the testing tool.
    :rtype: str
    """
    if ("pytest" in tool.lower()):
        return "Pytest"
    elif ("tosca" in tool.lower()):
        return "Tosca"
    elif (
            "ning" in tool.lower() or
            len(tool) < 2 or
            tool.lower().startswith("no ")
            ):
        return "Ninguna de las anteriores"
    elif ("jasmine" in tool.lower()):
        return "Jasmine"
    elif ("mockito" in tool.lower()):
        return "Mockito"
    elif ("qmetry" in tool.lower()):
        return "QMetry"
    elif ("scalatest" in tool.lower()):
        return "ScalaTest"
    elif ("locust" in tool.lower()):
        return "Locust"
    elif ("gtest" in tool.lower()):
        return "GTest"
    elif ("insomnia" in tool.lower()):
        return "Insomnia"
    elif ("jmeter" in tool.lower()):
        return "Jmeter"
    elif ("playwright" in tool.lower()):
        return "Playwright"
    elif ("webdriver" in tool.lower() and ("io" in tool.lower())):
        return "WebDriverIO"
    elif ("quick" in tool.lower() and ("nimble" in tool.lower())):
        return "Quick & Nimble"
    elif ("manual" in tool.lower() and "test" in tool.lower()):
        return "Test Manual"
    elif ("testing" in tool.lower() and "react" in tool.lower()):
        return "React Testing Library"
    elif ("unit" in tool.lower() and ("test" in tool.lower())):
        return "Unittest"
    elif ("eclipse" in tool.lower() or ("rcptt" in tool.lower())):
        return "Eclipse RCPTT"
    return tool


def group_careers(career: str):
    """This function takes a string that represents a career
    and returns a string that represents the group of the career.
    If the input parameter is not a string, it is returned
    unchanged.

    :param career: The name of the career to evaluate.
    :type career: str
    :return: A string representing the group of the career.
    :rtype: str
    """
    if type(career) != str:
        return career

    if ("econom" in career.lower()):
        return "Licenciatura en Economía"
    if ("traduc" in career.lower()):
        return "Traductorado"
    if ("sociolog" in career.lower()):
        return "Licenciatura en Sociología"
    elif ("marketing" in career.lower()):
        return "Marketing"
    elif ("contador" in career.lower()):
        return "Contador Público"
    elif ("filosof" in career.lower()):
        return "Filosofía"
    elif ("política" in career.lower()):
        return "Licenciatura en Ciencia Política"
    elif ("psicolog" in career.lower()):
        return "Licenciatura en Psicología"
    elif ("analista " in career.lower()) and ("computac" in career.lower()):
        return 'Analista de Computación'
    elif ("diseño " in career.lower()) and ("industrial" in career.lower()):
        return 'Diseño Industrial'
    elif ("program" in career.lower()) and ("tecnicatura " in career.lower()):
        return 'Tecnicatura en Programación'
    elif ("comunicaci" in career.lower()) and ("social" in career.lower()):
        return 'Licenciatura en Comunicación Social'
    elif (career.lower().startswith('lic')) and (
            "comunicaci" in career.lower()):
        return 'Licenciatura en Comunicación'
    elif (("comunicaci" in career.lower()) and ((len(career) <= 14))):
        return "Licenciatura en Comunicación"
    elif (
            (career.lower().startswith('lic')) and
            ("gesti" in career.lower()) and
            ("inform" in career.lower())
            ):
        return 'Licenciatura en Gestión de la Información'
    elif (
            (career.lower().startswith('lic')) and
            ("en ciencia" in career.lower()) and
            (" de datos" in career.lower())
            ):
        return 'Licenciatura en Ciencia de Datos'
    elif ("ciencia de datos" in career.lower()):
        return 'Ciencia de Datos'
    elif (career.lower().startswith('lic')) and ("matem" in career.lower()):
        return "Licenciatura en Matemática"
    elif (
            (career.lower().startswith('lic')) and
            (("fisica" in career.lower()) or ("física" in career.lower()))
            ):
        return 'Licenciatura en Física'
    elif (
            "recursos humanos" in career.lower() or
            "hr" in career.lower() or
            "rrhh" in career.lower()
            ):
        return "Recursos Humanos"
    elif ("ciber" in career.lower()) and ("seguridad" in career.lower()):
        return "Ciberseguridad"
    elif ("inf" in career.lower()) and ("seguridad" in career.lower()):
        return "Seguridad Informática"
    elif (career.lower().startswith('ing')) and ("meca" in career.lower()):
        return "Ingeniería en Mecatrónica"
    elif (
            (career.lower().startswith('tec')) and
            ("web" in career.lower()) and
            ("desarrollo" in career.lower())
            ):
        return "Tecnicatura en Desarrollo Web"
    elif ("abog" in career.lower()) or ("derecho" in career.lower()):
        return "Derecho"
    elif (
            (career.lower().startswith('lic')) and
            "inter" in career.lower() and
            ("rela" in career.lower())
            ):
        return "Licenciatura en Relaciones Internacionales"
    return career


def fix_bootcamp_name(bootcamp: str) -> str:
    """Corrects the name of a bootcamp based on certain known patterns.

    :param bootcamp: The name of the bootcamp to be corrected.
    :type bootcamp: str
    :return: The corrected name of the bootcamp.
    :rtype: str
    """
    if ("ada" in bootcamp.lower()):
        return "ADA ITW"
    elif ("SAP" in bootcamp.lower()):
        return "SAP"
    elif ("alkemy" in bootcamp.lower()):
        return "Alkemy"
    elif ("udemy" in bootcamp.lower()):
        return "Udemy"
    elif ("nucba" in bootcamp.lower()):
        return "Nucba"
    elif ("accentur" in bootcamp.lower()):
        return "Accenture"
    elif ("platzi" in bootcamp.lower()):
        return "Platzi"
    elif ("henry" in bootcamp.lower()):
        return "Soy Henry"
    elif ("globant" in bootcamp.lower()):
        return "Globant"
    elif ("egg" in bootcamp.lower()):
        return "Egg Educacion"
    elif ("codo " in bootcamp.lower()):
        return "Codo a Codo"
    elif ("free" in bootcamp.lower()):
        return "Freecodecamp"
    elif ("acamica" in bootcamp.lower() or ("acámica" in bootcamp.lower())):
        return "Acámica"
    elif ("mercado" in bootcamp.lower() or ("meli" in bootcamp.lower())):
        return "BootCamp MercadoLibre"
    elif ("mind" in bootcamp.lower() and ("hub" in bootcamp.lower())):
        return "Mindhub"
    elif ("comunidad" in bootcamp.lower() and ("it" in bootcamp.lower())):
        return "Comunidad IT"
    elif ("code" in bootcamp.lower() and ("house" in bootcamp.lower())):
        return "Coderhouse"
    elif ("digital" in bootcamp.lower() and ("house" in bootcamp.lower())):
        return "Digital House"
    elif ("educaci" in bootcamp.lower() and ("it" in bootcamp.lower())):
        return "Educación IT"
    elif (
            "argentina" in bootcamp.lower() and
            "programa" in bootcamp.lower()
            ):
        return "Argentina Programa"
    elif ("plataforma" in bootcamp.lower() and ("5" in bootcamp.lower())):
        return "Plataforma 5"
    elif ("open" in bootcamp.lower() and ("bootcamp" in bootcamp.lower())):
        return "Open BootCamp"
    elif (
            "mujeres" in bootcamp.lower() or
            "met " in bootcamp.lower() or
            ("met" in bootcamp.lower() and (len(bootcamp) <= 3))
            ):
        return "Mujeres en Tecnologia"
    elif (
            ("utn" in bootcamp.lower() and (len(bootcamp) <= 3)) or
            (" utn" in bootcamp.lower()) or
            ("utn " in bootcamp.lower())
            ):
        return "UTN"

    return bootcamp


def fix_bootcamp_theme_name(theme: str) -> str:
    """Corrects the name of a theme based on certain known patterns.

    :param theme: The name of the theme to be corrected.
    :type theme: str
    :return: The corrected name of the theme.
    :rtype: str
    """
    if type(theme) != str:
        return theme

    theme_lower = theme.lower()

    if ("full" in theme_lower) or ("mern" in theme_lower):
        return "Full Stack Developer"
    elif ("javas" in theme_lower):
        return "Javascript"
    elif ("certified tech developer" in theme_lower):
        return "Certified Tech Developer"
    elif ("java" in theme_lower):
        return "Java"
    elif ("salesfor" in theme_lower):
        return "Salesforce"
    elif (".net" in theme_lower):
        return ".NET"
    elif ("python" in theme_lower):
        return "Python"
    elif ("devops" in theme_lower):
        return "DevOps"
    elif ("web" in theme_lower):
        return "Web Developer"
    elif ("ux" in theme_lower and "ui" in theme_lower) or "ux" in theme_lower:
        return "UX/UI"
    elif "front" in theme_lower:
        return "Frontend"
    elif "back" in theme_lower and "end" in theme_lower:
        return "Backend"
    elif "data" in theme_lower and "aly" in theme_lower:
        return "Data Analyst"
    elif "dat" in theme_lower and (
            "scien" in theme_lower or "cien" in theme_lower):
        return "Data Science"
    elif "dat" in theme_lower and (
            "big" in theme_lower or "engin" in theme_lower):
        return "Big Data"
    elif "qa" in theme_lower or "test" in theme_lower:
        return "QA Testing"
    elif ("react" in theme_lower):
        return "React.js"
    elif (
            "mobile" in theme_lower or
            "movil" in theme_lower or
            "android" in theme_lower or
            "swift" in theme_lower or
            "ios" in theme_lower):
        return "Desarrollo Mobile"
    elif (
            theme_lower.startswith("sap ") or
            (theme_lower.startswith("sap") and len(theme) <= 3)):
        return "SAP"
    elif (
        theme_lower.startswith("no ") or
        (theme_lower.startswith("no") and
         len(theme) <= 3) or len(theme) == 1):

        return "Ninguna de las anteriores"

    return theme


def find_nearest_multiple(number: float, multiple: int) -> int:
    """Find the nearest multiple of the given number to the input.

    :param number: The number to find the nearest multiple of.
    :type number: float
    :param multiple: The multiple to find the nearest value to.
    :type multiple: int

    :return: The nearest multiple of the given number to the input.
    :rtype: int
    """
    nearest_lower_multiple = (number // multiple) * multiple
    nearest_higher_multiple = nearest_lower_multiple + multiple

    if number - nearest_lower_multiple < nearest_higher_multiple - number:
        return nearest_lower_multiple

    return nearest_higher_multiple


def to_category_number_category(
            number: float, start: int, stop: int, step: int
        ) -> str:
    """Given a number, converts it to a string representation
    of the category in which it falls based on the specified start,
    stop and step values. If the number is NaN, returns the same value.

    :param number: The number to be categorized.
    :type number: float
    :param start: The start of the first category.
    :type start: int
    :param stop: The end of the last category.
    :type stop: int
    :param step: The size of each category.
    :type step: int
    :return: The string representation of the category
            in which the number falls.
    :rtype: str
    """

    if type(number) == np.NaN:
        return number

    if number < start:
        return "<" + str(start)

    while (number < stop):
        if number <= (start + (step - 1)):
            return str(start) + " - " + str((start + (step - 1)))
        start += step

    return "+" + str(stop)


def to_category_number_category2(
            number: float, start: int, stop: int, step: int
        ) -> str:
    """Given a number, converts it to a string representation of the
    category in which it falls based on the specified start,
    stop and step values. If the number is NaN, returns the same value.

    :param number: The number to be categorized.
    :type number: float
    :param start: The start of the first category.
    :type start: int
    :param stop: The end of the last category.
    :type stop: int
    :param step: The size of each category.
    :type step: int
    :return: The string representation of the
    category in which the number falls.
    :rtype: str
    """

    start_string = start

    if type(number) == np.NaN:
        return number

    if number < start:
        return "<" + str(start_string - 1)

    while (number < stop):
        if number <= (start + (step - 1)):

            number_string = (start + (step - 1))
            start_string = start

            if 1000 < number_string < 1000000:
                number_string = str(int(number_string/1000)) + "k"
            elif number_string > 1000000:
                number_string = str(
                            round(float(number_string/1000000), 3)
                            ) + "mill"

            if 1000 < start < 1000000:
                start_string = str(int(start/1000)) + "k"
            elif start >= 1000000:
                start_string = str(round(float(start/1000000), 3)) + "mill"

            return str(start_string) + " - " + str((number_string))
        start += step

    return "+" + str(stop)


def to_fibonacci_category(number: float):
    """Function that determines the category to which a number
    belongs in the Fibonacci sequence.

    :param number: The number for which the category in the Fibonacci
                    sequence is to be determined.
    :type number: float
    :return: A string indicating the category
            of the number in the Fibonacci sequence.
    :rtype: str
    """
    n1 = 1
    n2 = 2
    n3 = 0

    if number < n1:
        return ("<" + str(n1))
    while (n1 < 21):
        if n1 <= number < n2:
            return (str(n1) + " - " + str(n2) + ")")
        n3 = n2
        n2 = (n1 + n2)
        n1 = n3

    return ("+" + str(n1))
