from db import *

def add_room(type, price): #функция для админа
    connection = get_connection()

    with connection.cursor() as curs:
        curs.execute(
            "INSERT INTO rooms(room_type, price) VALUES (%s, %s)",
            (type, price)
        )

    connection.close()


def show_all_rooms():
    connection = get_connection()

    with connection.cursor() as curs:
        curs.execute(
            "SELECT room_id, room_type, price FROM rooms"
        )
        all_rooms = curs.fetchall()

    connection.close()

    return all_rooms

def show_free_rooms(date_from, date_to):
    connection = get_connection()

    with connection.cursor() as curs:
        curs.execute(
            """SELECT room_id, room_type, price
            FROM rooms r
            where not exists(
                SELECT 1
                FROM bookings b
                WHERE room_id = r.room_id
                AND daterange(date_from, date_to) && daterange(%s, %s)
            )
            ORDER BY price
            """, (date_from, date_to)
        )

        free_rooms = curs.fetchall()

        connection.close()

        return free_rooms

def add_guest(first_name, last_name, phone):
    connection = get_connection()

    with connection.cursor() as curs:
        curs.execute(
            "INSERT INTO guests( first_name, last_name, phone) VALUES (%s, %s, %s) "
            "RETURNING guest_id;",
            (first_name, last_name, phone)
        )

        guest = curs.fetchone()[0]

        connection.close()

        return guest


def create_booking(room_id, guest_id, date_from, date_to):
    connection = get_connection()

    with connection.cursor() as curs:
        curs.execute(
            "INSERT INTO bookings(room_id, guest, date_from, date_to) VALUES (%s, %s, %s, %s)"
            "RETURNING booking_id;",
            (room_id, guest_id, date_from, date_to)
        )

        booking = curs.fetchone()[0]

    connection.close()

    return booking


