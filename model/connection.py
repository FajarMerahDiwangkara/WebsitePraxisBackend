import psycopg2
from psycopg2 import Error

def get_postgres_connection(user, password, host, port, database):
    try:
        # Connect to an existing database
        connection = psycopg2.connect(user=user,
                                    password=password,
                                    host=host,
                                    port=port,
                                    database=database)
        return connection
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)