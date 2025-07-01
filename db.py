import psycopg2

def get_connection():
    try:
        connection = psycopg2.connect(dbname='hotel_db', user='postgres', password='849562', host='localhost')
        print('Successful connection to the database')

        connection.autocommit = True
        return connection

    except:
        print('Can`t establish connection to database')
        return None




