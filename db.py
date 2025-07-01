import psycopg2

def get_connection():
    '''
    подключение к Базе Данных
    connection.autocomit -   каждый отдельный cur.execute() сразу фиксируется в базе.
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

    # ищем пересечение с существующими бронями
    sql_booking_overlap = """
    CREATE OR REPLACE FUNCTION check_booking_overlap()
    RETURNS TRIGGER AS
    $$
    BEGIN
        IF EXISTS (
            SELECT 1
            FROM   bookings
            WHERE  room_id = NEW.room_id
              AND  NEW.date_from <= date_to      
              AND  NEW.date_to   >= date_from
        ) THEN
            RAISE EXCEPTION
              'Room % already booked for % – %',
              NEW.room_id, NEW.date_from, NEW.date_to;
        END IF;
    
        RETURN NEW;      
    END;
    $$ LANGUAGE plpgsql;

    """

    sql_trigger_booking = """
    CREATE TRIGGER trg_booking_overlap
    BEFORE INSERT OR UPDATE ON bookings
    FOR EACH ROW
    EXECUTE FUNCTION check_booking_overlap();
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
        cur.execute(sql_booking_overlap)
        cur.execute(sql_trigger_booking)

    connection.close()

