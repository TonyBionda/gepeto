import pyodbc
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()


# This function returns all the dataframes needed for the machine learning part
def get_dataframes():
    # load .env file
    server = os.getenv('SERVER')
    database = os.getenv('DATABASE')
    username = os.getenv('USERNAME')
    password = os.getenv('PASSWORD')

    # check if all environment variables are set
    if server is None or database is None or username is None or password is None:
        print("Error: missing environment variables")
        exit(0)

    driver = "ODBC Driver 17 for SQL Server"

    try:
        # connect to the database
        with pyodbc.connect(
                'DRIVER=' + driver + ';SERVER=tcp:' + server + ';PORT=1433;DATABASE=' + database + ';UID=' + username + ';PWD=' + password) as conn:
            cursor = conn.cursor()

            # get sejours
            sejour_dataframe = get_sejours_dataframe(cursor)

            # get dates
            dates_dataframe = get_dates_dataframe(cursor)

            # store dates in csv to use in the app (for automatic calculation of full moon for example)
            store_df_in_csv(dates_dataframe, 'dates')

            # get matchs
            matchs_dataframe = get_matchs_dataframe(cursor)

            # get alertes
            alertes_dataframe = get_alertes_dataframe(cursor)

            # return dataframes
            return sejour_dataframe, dates_dataframe, matchs_dataframe, alertes_dataframe
    except Exception as e:
        print(e)


# This function store a dataframe in a csv file with the given name
def store_df_in_csv(df, name):
    df.to_csv(name + '.csv', index=False)


# This function returns a dataframe from the database
def get_dataframe(cursor, name):
    # Queries to get the dataframes
    queries = {
        "SEJOURS": "SELECT CAST(DATE_DEBUT_SEJOUR as DATETIME) as DATE_DEBUT_SEJOUR, COUNT(*) as NB_ENTREES "
                   "FROM DWH_FAIT_SEJOUR "
                   "WHERE TYPE_SEJOUR = 'X' "
                   "GROUP BY DATE_DEBUT_SEJOUR",
        "DATES": "SELECT * FROM DWH_DIM_DATE",
        "MATCHS": "SELECT CAST(DATE as DATETIME) as Date, * FROM DWH_DIM_MATCH",
        "ALERTES": "SELECT CAST(DATE as DATETIME) as Date, * FROM DWH_DIM_ALERTE"
    }

    # Check if the name is in the queries
    if name not in queries:
        return None

    # Get the dataframe and return it
    try:
        array = []
        query = queries[name]
        cursor.execute(query)
        for row in cursor:
            row_to_list = [elem for elem in row]
            array.append(row_to_list)
        dataframe = pd.DataFrame(array)
        dataframe.columns = [column[0] for column in cursor.description]
        return dataframe
    except Exception as e:
        print(e)
        return None


# This function returns the sejours dataframe
def get_sejours_dataframe(cursor):
    return get_dataframe(cursor, "SEJOURS")


# This function returns the dates dataframe
def get_dates_dataframe(cursor):
    return get_dataframe(cursor, "DATES")


# This function returns the matchs dataframe
def get_matchs_dataframe(cursor):
    return get_dataframe(cursor, "MATCHS")


# This function returns the alertes dataframe
def get_alertes_dataframe(cursor):
    return get_dataframe(cursor, "ALERTES")
