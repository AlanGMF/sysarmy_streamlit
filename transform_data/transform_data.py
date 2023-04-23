import re

import numpy as np
import pandas as pd

import transform_data.utils as utils
import config


def main(
            df: pd.DataFrame,
            name: str,
            mep_dollar: int = None,
            blue_dollar: int = None,
            official_dollar: int = None
        ):

    max_wage_in_arg = None
    start_salary = None
    step_salary = None
    max_exchange_value = None

    if blue_dollar:
        max_wage_in_arg = config.MAX_WAGE_IN_USD * blue_dollar
        start_salary = round(blue_dollar * config.MIN_WAGE_IN_USD, -4)
        step_salary = start_salary
    if blue_dollar and official_dollar:
        max_exchange_value = blue_dollar + official_dollar

    # check if the values are from Argentina
    if config.COUNTRIES in df.columns:
        df = df[df[config.COUNTRIES] == 'Argentina']
    df.loc[
            ~(df[config.PROVINCES].isin(config.ARGENTINE_PROVINCES)),
            config.PROVINCES
        ] == np.NaN

    if len(df) == 0:
        return False

    # Último salario mensual o retiro BRUTO (en tu moneda local)

    # nullify invalid characters
    regex = r'[@,:óÚíéá$a-zA-Z-]'

    df[config.GROSS_SALARY] = df[config.GROSS_SALARY].str.replace(',', '')
    df[config.GROSS_SALARY] = df[config.GROSS_SALARY].str.replace(regex, '', regex=True)
    df[config.GROSS_SALARY] = pd.to_numeric(df[config.GROSS_SALARY], errors='coerce')

    # values less than constants.MIN_WAGE_IN_USD are nullify
    df.loc[
            df[config.GROSS_SALARY] < config.MIN_WAGE_IN_USD,
            config.GROSS_SALARY
        ] = np.NaN

    # Último salario mensual o retiro NETO (en tu moneda local)

    df[config.NET_SALARY] = df[config.NET_SALARY].str.replace(',', '')
    df[config.NET_SALARY] = df[config.NET_SALARY].str.replace(regex, '', regex=True)
    df[config.NET_SALARY] = pd.to_numeric(df[config.NET_SALARY], errors='coerce')
    # values less than constants.MIN_WAGE_IN_USD are nullify
    df.loc[df[config.NET_SALARY] < config.MIN_WAGE_IN_USD, config.NET_SALARY] = np.NaN

    # Values greater than max_wage_in_arg are nullify
    if max_wage_in_arg:
        df.loc[(df[config.GROSS_SALARY] > max_wage_in_arg), config.GROSS_SALARY] = np.NaN
        df.loc[(df[config.NET_SALARY] > max_wage_in_arg), config.NET_SALARY] = np.NaN

    # Pagos en dólares

    if config.PAYMENTS_IN_DOLLARS in df.columns:
        # fill null values
        df.loc[df[config.PAYMENTS_IN_DOLLARS].isna(), config.PAYMENTS_IN_DOLLARS] = config.FILL_NULL_VALUES

    # Si tu sueldo está dolarizado:
    # ¿Cuál fue el último valor del dólar que tomaron?

    if config.LAST_VALUE_EXCHANGE in df.columns:
        # Override alphanumeric values:
        # values that do not answer the question are nullify
        values_to_avoid = df[config.LAST_VALUE_EXCHANGE].apply(lambda x: isinstance(x, str) and  not (bool(re.search(r'\d+', x))) and ("no " in x.lower() or ("no" in x.lower() and len(x) < 3)))
        df.loc[values_to_avoid, config.LAST_VALUE_EXCHANGE] = np.NaN

        if official_dollar and type(official_dollar) == str:
            # the official dollar value is replaced
            # with predefined official_dollar
            values_to_reset = df[config.LAST_VALUE_EXCHANGE].apply(lambda x: isinstance(x, str)  and (bool(re.search(r'\d+', x))) and ("oficial" in x.lower() or "banco nac" in x.lower() or "bna" in x.lower()))
            df.loc[values_to_reset, config.LAST_VALUE_EXCHANGE] = official_dollar

        if mep_dollar and type(mep_dollar) == str:
            values_to_reset = df[config.LAST_VALUE_EXCHANGE].apply(lambda x: isinstance(x, str) and (bool(re.search(r'\d+', x))) and ("mep" in x.lower() or "crypto" in x.lower() or "cripto" in x.lower()))
            df.loc[values_to_reset, config.LAST_VALUE_EXCHANGE] = mep_dollar

        if blue_dollar and type(blue_dollar) == str:
            values_to_reset = df[config.LAST_VALUE_EXCHANGE].apply(lambda x: isinstance(x, str) and not (bool(re.search(r'\d+', x))) and "blue" in x.lower())
            df.loc[values_to_reset, config.LAST_VALUE_EXCHANGE] = blue_dollar

        # replace the remaining non-numeric values with np.NaN
        values_to_reset = df[config.LAST_VALUE_EXCHANGE].apply(lambda x:isinstance(x, str) and not (bool(re.search(r'\d+', x))))
        df.loc[values_to_reset, config.LAST_VALUE_EXCHANGE] = np.NaN

        # extract numbers from alphanumeric values
        df[config.LAST_VALUE_EXCHANGE] = df[config.LAST_VALUE_EXCHANGE].str.replace(r",",".").str.replace(r"\$", "", regex=True)
        values_to_reset = df[config.LAST_VALUE_EXCHANGE].apply(lambda x: isinstance(x, str) and x.isalnum())
        df.loc[values_to_reset, config.LAST_VALUE_EXCHANGE] = df.loc[values_to_reset, config.LAST_VALUE_EXCHANGE].apply(utils.extract_numbers)

        # converts strings that do not contain numbers and periods to NaN and converts numeric strings to numeric values
        values_to_avoid = df[config.LAST_VALUE_EXCHANGE].apply(lambda x: isinstance(x, str) and (bool(re.search(r'[^\d.]+', x))))
        df.loc[values_to_avoid, config.LAST_VALUE_EXCHANGE] = np.NaN

        # transform values to numeric values and filter them
        df[config.LAST_VALUE_EXCHANGE] = pd.to_numeric(df[config.LAST_VALUE_EXCHANGE], errors='coerce')
        if max_exchange_value:
            df.loc[df[config.LAST_VALUE_EXCHANGE] > max_exchange_value, config.LAST_VALUE_EXCHANGE] = np.NaN

        # Salaries are rewritten by calculating the value in ARG based on the exchange value
        df.loc[(df[config.GROSS_SALARY] < config.MAX_WAGE_IN_USD) & (df[config.LAST_VALUE_EXCHANGE].notnull()), [config.GROSS_SALARY]] *= df.loc[(df[config.GROSS_SALARY] < config.MAX_WAGE_IN_USD) & (df[config.LAST_VALUE_EXCHANGE].notnull()), [config.LAST_VALUE_EXCHANGE]]
        df.loc[(df[config.NET_SALARY] < config.MAX_WAGE_IN_USD) & (df[config.LAST_VALUE_EXCHANGE].notnull()), [config.NET_SALARY]] *= df.loc[(df[config.NET_SALARY] < config.MAX_WAGE_IN_USD) & (df[config.LAST_VALUE_EXCHANGE].notnull()), [config.LAST_VALUE_EXCHANGE]]
        # Values in dollars without exchange rate are nullify
        df.loc[(df[config.GROSS_SALARY] < config.MAX_WAGE_IN_USD) & (df[config.LAST_VALUE_EXCHANGE].isnull()), [config.GROSS_SALARY]] = np.NaN
        df.loc[(df[config.NET_SALARY] < config.MAX_WAGE_IN_USD) & (df[config.LAST_VALUE_EXCHANGE].isnull()), [config.NET_SALARY]] = np.NaN

        df[config.LAST_VALUE_EXCHANGE + config.REWRITTEN_COLUMN_SUFFIX] = df[config.LAST_VALUE_EXCHANGE].apply(lambda x: utils.find_nearest_multiple(x, 5)).replace(0.0, np.NaN)

    # Compare two salaries
    # Net salary values greater than gross salary and the difference
    # is greater than a total gross salary are nullify
    df.loc[((df[config.GROSS_SALARY] > df[config.NET_SALARY]) & ((df[config.GROSS_SALARY] - df[config.NET_SALARY]) > df[config.NET_SALARY] * 2)) | ((df[config.GROSS_SALARY] < df[config.NET_SALARY]) & ((df[config.NET_SALARY] - df[config.GROSS_SALARY]) > df[config.GROSS_SALARY] * 2)), [config.GROSS_SALARY, config.NET_SALARY]] = np.NaN
    df.drop(index=df[(df[config.GROSS_SALARY] < df[config.NET_SALARY]) & ((df[config.NET_SALARY] - df[config.GROSS_SALARY]) > df[config.GROSS_SALARY])].index, inplace=True)

    # Swapping Net salary with gross salary
    swap_values = df[(df[config.GROSS_SALARY] < df[config.NET_SALARY])][[config.GROSS_SALARY]]
    df.loc[swap_values.index, [config.GROSS_SALARY, config.NET_SALARY]] = df.loc[swap_values.index, [config.NET_SALARY, config.GROSS_SALARY]].values

    # Trabajo de

    df.loc[df[config.POSITIONS].notna(), config.POSITIONS].apply(utils.group_jobs)

    # restaurant jobs that have the word "data" are replaced
    # with "BI Analyst / Data Analyst"
    data_jobs = df.loc[df[config.POSITIONS].apply(lambda x: "data" in x.lower()), config.POSITIONS].value_counts()
    data_jobs = data_jobs.loc[data_jobs.values <= 1].index
    df.loc[df[config.POSITIONS].apply(lambda x: x in data_jobs), config.POSITIONS] = 'BI Analyst / Data Analyst'

    # Con qué beneficios contas

    df[config.BENEFITS] = df[config.BENEFITS].apply(utils.cut_string)
    benefits = pd.Series(sum(df.loc[df[config.BENEFITS].notna(), config.BENEFITS], []))
    benefits = benefits.apply(utils.fix_benefit_name).value_counts()
    valid_benefits = benefits[benefits >= config.MIN_AMOUNT].index.to_list()
    df.loc[df[config.BENEFITS].notna(), config.BENEFITS].apply(lambda x: utils.replace_list_values(x, valid_benefits, "Otros", utils.fix_benefit_name))
    df[config.BENEFITS] = df[config.BENEFITS].apply(lambda x: ' - '.join(x) if type(x) == list else x)

    # ¿Cuántas personas a cargo tenés?

    df[config.DEPENDENTS] = df[config.DEPENDENTS].astype('float64').clip(lower=0, upper=config.MAXIMUM_PEOPLE_IN_CHARGE)

    # Plataformas que utilizas en tu puesto actual

    df[config.PLATFORMS_COLUMN] = df[config.PLATFORMS_COLUMN].apply(utils.cut_string)
    platforms_s = pd.Series(sum(df.loc[df[config.PLATFORMS_COLUMN].notna(), config.PLATFORMS_COLUMN], []))
    platforms_s = platforms_s.apply(utils.fix_platform_name).value_counts()
    platforms = platforms_s[platforms_s >= config.MIN_AMOUNT].index.to_list()
    df.loc[df[config.PLATFORMS_COLUMN].notna(), config.PLATFORMS_COLUMN].apply(lambda x: utils.replace_list_values(x, platforms, config.FILL_WITH, utils.fix_platform_name))
    df[config.PLATFORMS_COLUMN] = df[config.PLATFORMS_COLUMN].apply(lambda x: ' - '.join(x) if type(x) == list else x)

    # Lenguajes de programación o tecnologías que utilices en tu puesto actual

    df[config.LANGUAGES] = df[config.LANGUAGES].apply(utils.cut_string)
    languages_s = pd.Series(sum(df.loc[df[config.LANGUAGES].notna(), config.LANGUAGES], []))
    languages_s = languages_s.apply(utils.fix_languages_name).value_counts()
    languages = languages_s[languages_s >= config.MIN_AMOUNT].index.to_list()
    df.loc[df[config.LANGUAGES].notna(), config.LANGUAGES].apply(lambda x: utils.replace_list_values(x, languages, config.FILL_WITH, utils.fix_languages_name))
    df[config.LANGUAGES] = df[config.LANGUAGES].apply(lambda x: ' - '.join(x) if type(x) == list else x)

    # Frameworks, herramientas y librerías que utilices en tu puesto actual

    df[config.FRAMEWORKS] = df[config.FRAMEWORKS].apply(utils.cut_string)
    frameworks_s = pd.Series(sum(df.loc[df[config.FRAMEWORKS].notna(), config.FRAMEWORKS], []))
    frameworks_s = frameworks_s.apply(utils.fix_framework_name).value_counts()
    frameworks = frameworks_s[frameworks_s >= config.MIN_AMOUNT].index.to_list()
    df.loc[df[config.FRAMEWORKS].notna(), config.FRAMEWORKS].apply(lambda x: utils.replace_list_values(x, frameworks, config.FILL_WITH, utils.fix_languages_name))
    df[config.FRAMEWORKS] = df[config.FRAMEWORKS].apply(lambda x: ' - '.join(x) if type(x) == list else x)

    # Bases de datos

    df[config.DATABASES_COLUMN] = df[config.DATABASES_COLUMN].apply(utils.cut_string)
    db_s = pd.Series(sum(df.loc[df[config.DATABASES_COLUMN].notna(), config.DATABASES_COLUMN], []))
    db_s = db_s.apply(utils.fix_DB_name).value_counts()
    db = db_s[db_s >= config.MIN_AMOUNT].index.to_list()
    df.loc[df[config.DATABASES_COLUMN].notna(), config.DATABASES_COLUMN].apply(lambda x: utils.replace_list_values(x, db, config.FILL_WITH, utils.fix_DB_name))
    df[config.DATABASES_COLUMN] = df[config.DATABASES_COLUMN].apply(lambda x: ' - '.join(x) if type(x) == list else x)

    # QA / Testing

    df[config.QA] = df[config.QA].apply(utils.cut_string)
    qa_serie = pd.Series(sum(df.loc[df[config.QA].notna(), config.QA], []))
    qa_serie = qa_serie.apply(utils.fix_testing_tool_name).value_counts()
    valid_qa = qa_serie[qa_serie >= config.MIN_AMOUNT].index.to_list()
    df.loc[df[config.QA].notna(), config.QA].apply(lambda x: utils.replace_list_values(x, valid_qa, config.FILL_WITH, utils.fix_testing_tool_name))
    df[config.QA] = df[config.QA].apply(lambda x: ' - '.join(x) if type(x) == list else x)

    # ¿Participaste de algún Boot Camp?

    df.loc[df[config.BOOTCAMP].apply(lambda x: type(x) == str and (("no" in x.lower() and len(x) < 3) or "no," in x.lower())), config.BOOTCAMP] = np.NaN

    # Normalize the separation of bootcamps
    df[config.BOOTCAMP] = df[config.BOOTCAMP].apply(lambda x: x.replace("Si,", " ").replace("ux/ui", " ") if isinstance(x, str) and (x.startswith("Si,") or "ux/ui" in x.lower()) else x)

    separators_regex = r"\s*(?: / | y |, |;)\s*"

    df[config.BOOTCAMP] = df[config.BOOTCAMP].apply(lambda x: re.sub(separators_regex, " - ", x) if isinstance(x, str) else x)
    df[config.BOOTCAMP] = df[config.BOOTCAMP].str.replace("/", " - ")
    df[config.BOOTCAMP] = df[config.BOOTCAMP].apply(lambda x: x.strip().split(" - ") if isinstance(x, str) else x)

    bootcamps_list = pd.Series(sum(df.loc[df[config.BOOTCAMP].notna(), config.BOOTCAMP], []))
    bootcamps_list = bootcamps_list.apply(utils.fix_bootcamp_name).value_counts()
    valid_bootcamps = bootcamps_list[bootcamps_list >= config.MIN_AMOUNT].index.to_list()
    df.loc[df[config.BOOTCAMP].notna(), config.BOOTCAMP].apply(lambda x: utils.replace_list_values(x, valid_bootcamps, config.FILL_WITH, utils.fix_bootcamp_name))
    df[config.BOOTCAMP] = df[config.BOOTCAMP].apply(lambda x: ' - '.join(x) if type(x) == list else x)

    # Máximo nivel de estudios

    df.loc[df[config.MAX_LVL_STUDIES].isna(), config.MAX_LVL_STUDIES] = config.FILL_NULL_VALUES

    # Carrera

    df.loc[df[config.CAREER].isna() & df[config.STUDIES_STATE].notna(), config.STUDIES_STATE] = np.NaN
    df[config.CAREER] = df[config.CAREER].apply(utils.group_careers)
    df.loc[df[config.CAREER].notna() & df[config.STUDIES_STATE].isna(), config.CAREER] = np.NaN

    # Si participaste de un Boot Camp, ¿qué carrera estudiaste

    if config.TRAINING_IN in df.columns:
        df[config.TRAINING_IN] = df[config.TRAINING_IN].apply(utils.fix_bootcamp_theme_name)
        valid_bootcamp_theme = df[config.TRAINING_IN].apply(utils.fix_bootcamp_theme_name).value_counts()
        valid_bootcamp_theme = valid_bootcamp_theme[valid_bootcamp_theme > config.MIN_AMOUNT].index.to_list()
        df[config.TRAINING_IN] = df[config.TRAINING_IN].apply(lambda x: config.FILL_WITH if (isinstance(x, str) and x not in valid_bootcamp_theme) else x)

    # Tengo (edad)

    values_to_avoid = df[config.AGE].apply(lambda x: isinstance(x, str) and not (bool(re.search(r'[\d+]', x))))
    df.loc[values_to_avoid, config.AGE] = np.NaN
    values_to_avoid = df[config.AGE].apply(lambda x: isinstance(x, str) and (bool(re.search(r'[a-zA-Z-]', x))))
    df.loc[values_to_avoid, config.AGE] = df[values_to_avoid][config.AGE].apply(utils.extract_numbers)
    df[config.AGE] = pd.to_numeric(df[config.AGE], errors='coerce')
    df.loc[df[config.AGE] > config.MAX_AGE, config.AGE] = np.NaN
    df.drop(index=df[df[config.AGE] < config.MIN_AGE].index, inplace=True)

    # Antigüedad en la empresa actual
    df[config.TIME_IN_CURRENT_COMPANY] = pd.to_numeric(df[config.TIME_IN_CURRENT_COMPANY], errors='coerce')
    df[config.TIME_IN_CURRENT_ROLE] = pd.to_numeric(df[config.TIME_IN_CURRENT_ROLE], errors='coerce')
    df[config.TIME_IN_CURRENT_COMPANY] = pd.to_numeric(df[config.TIME_IN_CURRENT_COMPANY], errors='coerce')
    df[config.YEARS_OF_EXPERIENCE] = pd.to_numeric(df[config.YEARS_OF_EXPERIENCE], errors='coerce')

    # the years of experience and Seniority in the current company
    # that are greater than the age and according to
    # constants.MAXIMUM_YEARS_OF_EXPERIENCE are nullified
    df.loc[df[config.TIME_IN_CURRENT_COMPANY] > df[config.AGE], config.TIME_IN_CURRENT_COMPANY] = np.NaN
    df.loc[df[config.YEARS_OF_EXPERIENCE] > df[config.AGE], config.YEARS_OF_EXPERIENCE] = np.NaN
    df.drop(index=df[df[config.YEARS_OF_EXPERIENCE] > config.MAXIMUM_YEARS_OF_EXPERIENCE].index, inplace=True)

    # the years of experience are nullify if they began when
    # the person was not of legal age
    df.loc[df[config.YEARS_OF_EXPERIENCE] > (df[config.AGE] - 17), config.YEARS_OF_EXPERIENCE] = np.NaN

    # Me identifico (género)

    # rename invalid responses
    if not df[config.GENDER].apply(lambda x: x not in config.VALID_GENDER_CATEGORIES).all():
        df.loc[df[config.GENDER].apply(lambda x: x not in config.VALID_GENDER_CATEGORIES), config.GENDER] = config.FILL_NO_VALID_GENDERS_WITH

    # Add columns to chart

    # Transform the data to strings and add • so that streamlit
    # can better read the plotly histogram in separate columns
    df[config.SEMI_ANNUAL_SALARY_COMPLIANCE + config.REWRITTEN_COLUMN_SUFFIX] = df[config.SEMI_ANNUAL_SALARY_COMPLIANCE].apply(lambda x: "•" + str(x))
    df[config.SALARY_COMPLIANCE + config.REWRITTEN_COLUMN_SUFFIX] = df[config.SALARY_COMPLIANCE].apply(lambda x: "•" + str(x))
    df[config.WORKPLACE_RECOMMENDATION + config.REWRITTEN_COLUMN_SUFFIX] = df[config.WORKPLACE_RECOMMENDATION].apply(lambda x: "•" + str(x))
    if config.DAYS_IN_OFFICE in df.columns:
        df[config.DAYS_IN_OFFICE + config.REWRITTEN_COLUMN_SUFFIX] = df[config.DAYS_IN_OFFICE].apply(lambda x: "•" + str(x))


    # Ages are grouped to be able to plot the data in columns of a histogram
    df[config.AGE + config.REWRITTEN_COLUMN_SUFFIX] = df[config.AGE].apply(lambda x: utils.to_category_number_category2(x, config.START_AGE, config.STOP_AGE, config.STEP_AGE))

    # salaries are grouped to be able to plot the data in columns
    # of a histogram
    if max_wage_in_arg and step_salary and start_salary:
        df.loc[df[config.GROSS_SALARY].notna(), config.GROSS_SALARY + config.REWRITTEN_COLUMN_SUFFIX] = df.loc[df[config.GROSS_SALARY].notna(), config.GROSS_SALARY].apply(lambda x: utils.to_category_number_category2(x, start_salary, max_wage_in_arg, step_salary))
        df.loc[df[config.NET_SALARY].notna(), config.GROSS_SALARY + config.REWRITTEN_COLUMN_SUFFIX] = df.loc[df[config.GROSS_SALARY].notna(), config.GROSS_SALARY].apply(lambda x: utils.to_category_number_category2(x, start_salary, max_wage_in_arg, step_salary))

    for column in config.COLUMNS_TO_CAREGORIZE_AS_FIBONACCI:
        df.loc[df[column].notna(), column + config.REWRITTEN_COLUMN_SUFFIX] = df.loc[df[column].notna(), column].apply(lambda x: utils.to_fibonacci_category(x))

    # The roles that appear rarely repeated are rewritten with
    # the value constants.FILL_WITH
    carreer_counts = df.groupby(config.POSITIONS).size()
    rare_carreers = carreer_counts[carreer_counts < config.MIN_AMOUNT].index
    df[config.POSITIONS + config.REWRITTEN_COLUMN_SUFFIX] = df[config.POSITIONS].map(lambda x: config.FILL_WITH if x in rare_carreers else x)

    # The careers that appear rarely repeated are rewritten with the value constants.FILL_WITH
    carreer_counts = df.groupby(config.CAREER).size()
    rare_carreers = carreer_counts[carreer_counts < config.MIN_AMOUNT].index
    df[config.CAREER + config.REWRITTEN_COLUMN_SUFFIX] = df[config.CAREER].map(lambda x: config.FILL_WITH if x in rare_carreers else x)

    # Save data
    config.FOLDER_PATH.mkdir(parents=True, exist_ok=True)
    df.to_csv(config.FOLDER_PATH / name)
    return True
