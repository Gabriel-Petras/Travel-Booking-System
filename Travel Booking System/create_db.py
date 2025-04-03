from app import app, db
from app import Flight
from datetime import datetime, timedelta
import random

def random_date(start_date, end_date):
    return start_date + timedelta(days=random.randint(0, (end_date - start_date).days))

with app.app_context():
    db.create_all()

    db.session.query(Flight).delete()
    db.session.commit()

    flights = []
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 12, 31)
    
    cities = ["New York", "Los Angeles", "Paris", "London", "Berlin", "Tokyo"]
    flight_times = ["Morning", "Afternoon", "Evening", "Night"]

    for _ in range(100):
        from_city = random.choice(cities)
        to_city = random.choice(cities)

        while from_city == to_city:
            to_city = random.choice(cities)
        
        departure_date = random_date(start_date, end_date)
        return_date = departure_date + timedelta(days=random.randint(3, 14))
        available_seats = random.randint(50, 150)
        booked_seats = random.randint(0, available_seats)
        price = round(random.uniform(200.0, 1000.0), 2)

        flight_number = f"{random.choice(['A', 'B', 'C', 'D', 'E'])}{random.randint(100, 999)}"
        
        
        flight_time = random.choice(flight_times)

        flight = Flight(
            from_city=from_city, 
            to_city=to_city, 
            departure_date=departure_date, 
            return_date=return_date, 
            available_seats=available_seats, 
            booked_seats=booked_seats, 
            price=price,
            flight_number=flight_number,
            flight_time=flight_time 
        )
        flights.append(flight)

    db.session.add_all(flights)

    db.session.commit()

    print("100 flights have been added to the database (existing records have been overwritten)!")
