from db import *

def add_room(id, type, price):
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
        rows = curs.fetchall()

    connection.close()

    return rows



rooms = show_all_rooms()

for room_id, room_type, price in rooms:
    text = f"Room number: {room_id}  | type: {room_type}  |  price: {price} $"
    print(len(text) * "_")
    print(text)