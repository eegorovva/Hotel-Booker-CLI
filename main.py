from psycopg2.errors import RaiseException

from db import *
from logic import *

def show_rooms():
    print("\nSpecify arrival and departure dates. Example (YYYY-MM-DD)")
    date_from = input(">>> ").strip()
    date_to = input(">>> ").strip()

    rooms = show_free_rooms(date_from, date_to)

    if rooms:
        for room_id, room_type, price in rooms:
            text = f"\nRoom number: {room_id}  | type: {room_type}  |  price: {price} $"
            print(len(text) * "_")
            print(text)
    else:
        print("There are no available rooms")



def registration_for_guest():
    print("\nEnter your firstname")
    f_name = input(">>> ").strip()

    print("\nEnter your lastname")
    l_name = input(">>> ").strip()

    print("\nEnter your phone number")
    phone = input(">>> ").strip()

    guest = add_guest(f_name, l_name, phone)

    return guest

def booking():
    print("\nEnter rooms number:")
    room = input(">>> ").strip()

    guest = registration_for_guest()

    print("\nSpecify arrival and departure dates. Example (YYYY-MM-DD)")
    date_from = input(">>> ").strip()
    date_to = input(">>> ").strip()

    try:
        booking_id = create_booking(room, guest, date_from, date_to)
        print(f"The reservation has been confirmed! №{booking_id}")
    except RaiseException:
        print("\nRoom already booked for this dates")



def main_menu():
    #creat_db()  создаем бд, если еще не создана

    while True:
        print("\n===HOTEL BOOKER===")
        print("\n1. View available rooms")
        print("2. Book a room")
        print("0. Exit")

        choice = input("\n>>> ").strip()

        if choice == "1":
            show_rooms()
            print("\nEnter 0 for exit")
            choice_for_exit = input(">>>").strip()

            if choice_for_exit == "0":
                continue
            else:
                print("Try again, please")

        elif choice == "2":
            booking()
        elif choice == "0":
            print("Bye!")
            break
        else:
            print("Try again, please")


if __name__ == "__main__":
    main_menu()