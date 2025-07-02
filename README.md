# Hotel-Booker CLI

Консольная утилита на **Python + PostgreSQL** для бронирования номеров в отели.

(В config.py необходимо прописать свою строку подключения, например
DSN = "postgresql://postgres:<password>@localhost:5432/hotel_db")

# Запускаем программу

**python main.py**

В консоли сразу появляется главное меню:

===HOTEL BOOKER===
1. View available rooms
2. Book a room
0. Exit

# 1.View available rooms


Specify arrival and departure dates. Example (YYYY-MM-DD)
>>> 2025-08-01

>>> 2025-08-04

Скрипт вызывает show_free_rooms()

Если что-то найдено, выведет, например:

_______________________________________________
Room number: 101  | type: single  |  price: 35 $
_______________________________________________
Room number: 201  | type: double  |  price: 60 $


В конце необходимо ввести 0, чтобы вернуться в меню.

# 2.Book a room



Enter rooms number:
>>> 1            

Enter your firstname
>>> something

Enter your lastname
>>> something

Enter your phone number
>>> +71110000000

Specify arrival and departure dates. Example (YYYY-MM-DD)
>>> 2025-08-01

>>> 2025-08-04

Что происходит под капотом:

registration_for_guest()
→ создаёт гостя и получает guest_id.

create_booking()
→ делает INSERT в bookings.
→ если даты не пересекаются, БД возвращает booking_id, и скрипт пишет:

The reservation has been confirmed!
Если даты пересекаются, триггер в БД кидает RAISE EXCEPTION,
код ловит RaiseException и выводит:

Room already booked for this dates
