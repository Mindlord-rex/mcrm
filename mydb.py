import psycopg2

dataBase = psycopg2.connect(
    host = 'localhost',
    user = 'postgres',
    password = '0000',
)

cursorObj = dataBase.cursor()

cursorObj.execute("CREATE DATABASE crm_database")