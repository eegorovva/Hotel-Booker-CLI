import psycopg2

def get_connection():
    '''
    подключение к Базе Данных
    connection.autocomit -  выключает режим транзакций: каждый отдельный cur.execute() сразу фиксируется в базе.
    '''
    try:
        connection = psycopg2.connect(dbname='hotel_db', user='postgres', password='849562', host='localhost')

        connection.autocommit = True
        return connection

    except:
        print('Can`t establish connection to database')
        return None




def creat_db():
    sql_enum = """
    CREATE TYPE room_type_enum
    AS ENUM ('single', 'double', 'triple');
    """


    sql_rooms = """
    CREATE TABLE if not exists rooms (
	room_id text primary key,
	room_type room_type_enum,
	price numeric
);
    """

    sql_guests = """
    CREATE TABLE IF NOT EXISTS guests (
	guest_id SERIAL PRIMARY KEY,
	first_name text not null,
	last_name text not null,
	phone text not null
);
    """

    sql_bookings = """
    CREATE TABLE IF NOT EXISTS bookings (
	booking_id SERIAL PRIMARY KEY,
	room_id TEXT references rooms(room_id),
	guest INTEGER references guests(guest_id),
	date_from DATE NOT NULL,
	date_to DATE NOT NULL
);
    """

    sql_idx_book_dates = """
    CREATE INDEX IF NOT EXISTS idx_book_dates
    ON bookings(room_id, date_from, date_to);
    """

    connection = get_connection()

    with connection.cursor() as cur:
        try:
            cur.execute(sql_enum)
        except psycopg2.errors.DuplicateObject:
            connection.rollback()
        cur.execute(sql_rooms)
        cur.execute(sql_guests)
        cur.execute(sql_bookings)
        cur.execute(sql_idx_book_dates)

    connection.close()

