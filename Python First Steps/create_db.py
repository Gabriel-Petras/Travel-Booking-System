from app import app, db
from app import Flight  # Import the Flight model
from datetime import datetime, timedelta
import random

# Function to generate a random date within a given range
def random_date(start_date, end_date):
    return start_date + timedelta(days=random.randint(0, (end_date - start_date).days))

# Use the app context to interact with the database
with app.app_context():
    # Create the tables first (in case they are not created already)
    db.create_all()

    # Clear existing flights to overwrite them with new ones
    db.session.query(Flight).delete()
    db.session.commit()

    # Generate 100 new flights
    flights = []
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 12, 31)
    
    # List of cities
    cities = ["New York", "Los Angeles", "Paris", "London", "Berlin", "Tokyo"]
    flight_times = ["Morning", "Afternoon", "Evening", "Night"]  # Flight times options

    for _ in range(100):
        from_city = random.choice(cities)
        to_city = random.choice(cities)

        # Ensure the flight is not from the city to the same city (no duplicates)
        while from_city == to_city:
            to_city = random.choice(cities)
        
        departure_date = random_date(start_date, end_date)
        return_date = departure_date + timedelta(days=random.randint(3, 14))  # Random return date (3 to 14 days)
        available_seats = random.randint(50, 150)
        booked_seats = random.randint(0, available_seats)
        price = round(random.uniform(200.0, 1000.0), 2)  # Random price between 200 and 1000 USD

        # Generate random flight number (e.g., "ABC123")
        flight_number = f"{random.choice(['A', 'B', 'C', 'D', 'E'])}{random.randint(100, 999)}"
        
        
        # Randomly choose a flight time
        flight_time = random.choice(flight_times)

        # Create a new flight
        flight = Flight(
            from_city=from_city, 
            to_city=to_city, 
            departure_date=departure_date, 
            return_date=return_date, 
            available_seats=available_seats, 
            booked_seats=booked_seats, 
            price=price,
            flight_number=flight_number,  # Add the flight number
            flight_time=flight_time      # Add the flight time
        )
        flights.append(flight)

    # Add all flights to the session in one go
    db.session.add_all(flights)

    # Commit all the changes to the database
    db.session.commit()

    print("100 flights have been added to the database (existing records have been overwritten)!")
