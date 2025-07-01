CREATE TYPE room_type_enum as ENUM ('single', 'double', 'triple')

CREATE TABLE if not exists rooms (
	room_id text primary key,
	room_type room_type_enum,
	price numeric
)

CREATE TABLE IF NOT EXISTS guests (
	guest_id SERIAL PRIMARY KEY,
	first_name text not null,
	last_name text not null,
	phone text not null
)

CREATE TABLE IF NOT EXISTS bookings (
	booking_id SERIAL PRIMARY KEY,
	room_id TEXT references rooms(room_id),
	guest INTEGER references guests(guest_id),
	date_from DATE NOT NULL,
	date_to DATE NOT NULL
)

CREATE INDEX IF NOT EXISTS idx_book_dates
    ON bookings(room_id, date_from, date_to);