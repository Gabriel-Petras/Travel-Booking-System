from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Date
from sqlalchemy.exc import SQLAlchemyError

# Set up the database connection (this will create a new empty database)
DATABASE_URI = 'sqlite:///travel_booking.db'  # This will overwrite the existing file if you delete the old one
engine = create_engine(DATABASE_URI)
metadata = MetaData()

# Define the new tables (columns with 'airline' and 'hotel' are excluded)
def create_new_db():
    try:
        # Define tables without the unwanted columns
        # Flight table without 'airline'
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

        # Booking table without 'hotel'
        booking_table = Table('booking', metadata,
            Column('id', Integer, primary_key=True),
            Column('destination', String(100)),
            Column('check_in', Date),
            Column('check_out', Date),
            Column('user_id', Integer),
            Column('flight_id', Integer),
        )

        # User table (no changes here)
        user_table = Table('user', metadata,
            Column('id', Integer, primary_key=True),
            Column('username', String(100)),
            Column('email', String(100)),
            Column('password', String(100)),
        )

        # Create all tables in the database
        metadata.create_all(engine)
        print("New empty database created successfully with the required tables.")

    except SQLAlchemyError as e:
        print(f"Error: {e}")
        engine.rollback()

# Create the new database with the modified structure
create_new_db()
