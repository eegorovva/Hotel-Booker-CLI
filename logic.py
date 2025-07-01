from db import *

def add_room(id, type, price): #функция для админа
    connection = get_connection()

    with connection.cursor() as curs:
        curs.execute(
            "INSERT INTO rooms(room_id, room_type, price) VALUES (%s, %s, %s)",
            (id, type, price)
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


rooms = show_free_rooms("10.12.2025","12.12.2025")

for room_id, room_type, price in rooms:
    text = f"Room number: {room_id}  | type: {room_type}  |  price: {price} $"
    print(len(text) * "_")
    print(text)