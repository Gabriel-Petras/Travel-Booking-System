from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Date
from sqlalchemy.exc import SQLAlchemyError

DATABASE_URI = 'sqlite:///travel_booking.db'
engine = create_engine(DATABASE_URI)
metadata = MetaData()

def create_new_db():
    try:
        flight_table = Table('flight', metadata,
            Column('id', Integer, primary_key=True),
            Column('from_city', String(100)),
            Column('to_city', String(100)),
            Column('departure_date', Date),
            Column('return_date', Date),
            Column('available_seats', Integer),
            Column('booked_seats', Integer),
            Column('price', Integer),
            Column('flight_number', String(50)),
            Column('flight_time', String(100)),
        )

        booking_table = Table('booking', metadata,
            Column('id', Integer, primary_key=True),
            Column('destination', String(100)),
            Column('check_in', Date),
            Column('check_out', Date),
            Column('user_id', Integer),
            Column('flight_id', Integer),
        )

        user_table = Table('user', metadata,
            Column('id', Integer, primary_key=True),
            Column('username', String(100)),
            Column('email', String(100)),
            Column('password', String(100)),
        )

        metadata.create_all(engine)
        print("New empty database created successfully with the required tables.")

    except SQLAlchemyError as e:
        print(f"Error: {e}")
        engine.rollback()

create_new_db()
