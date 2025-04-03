from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///travel_booking.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

app.secret_key = 'your_secret_key'



class Flight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    from_city = db.Column(db.String(100), nullable=False)
    to_city = db.Column(db.String(100), nullable=False)
    departure_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date, nullable=False)
    available_seats = db.Column(db.Integer, nullable=False)
    booked_seats = db.Column(db.Integer, nullable=False, default=0)
    price = db.Column(db.Float, nullable=False)
    flight_number = db.Column(db.String(50), nullable=True)
    flight_time = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        return f'<Flight {self.from_city} to {self.to_city} on {self.departure_date}>'



@app.route('/book_flight/<int:flight_id>', methods=['GET', 'POST'])
def book_flight(flight_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    flight = Flight.query.get(flight_id)
    if flight is None:
        return "Flight not found", 404

    user = User.query.get(session['user_id'])

    if flight.available_seats <= 0:
        return render_template('book_flight.html', flight=flight, user=user, message="Sorry, no available seats for this flight.")

    if request.method == 'POST':
        try:
            guests = int(request.form['guests'])

            if guests < 1:
                return render_template('book_flight.html', flight=flight, user=user, message="You must book at least one guest.")

            if guests > flight.available_seats:
                return render_template('book_flight.html', flight=flight, user=user, message="Not enough available seats.")

            new_booking = Booking(
                destination=flight.to_city,
                check_in=flight.departure_date,
                check_out=flight.return_date,
                user_id=session['user_id'],
                flight_id=flight.id
            )

            db.session.add(new_booking)
            db.session.commit()

            flight.available_seats -= guests
            db.session.commit()

            return redirect(url_for('profile', user_id=session['user_id']))

        except ValueError:
            return render_template('book_flight.html', flight=flight, user=user, message="Invalid number of guests.")

    return render_template('book_flight.html', flight=flight, user=user)






@app.route('/flight', methods=['GET', 'POST'])
def flight():
    if request.method == 'POST':
        from_city = request.form['from']
        to_city = request.form['to']
        dates = request.form['dates'].split(' → ')
        departure_date = datetime.strptime(dates[0], '%b %d')
        return_date = datetime.strptime(dates[1], '%b %d')
        guests = int(request.form['guests'])
        price = 100.0 

        flight = Flight(from_city=from_city, to_city=to_city, departure_date=departure_date, 
                        return_date=return_date, available_seats=100, booked_seats=0, price=price)
        db.session.add(flight)
        db.session.commit()

        return redirect(url_for('home'))
    
    return render_template('flight_form.html')

@app.route('/add_flight', methods=['GET', 'POST'])
def add_flight():
    if request.method == 'POST':
        from_city = request.form['from']
        to_city = request.form['to']
        dates = request.form['dates'].split(' → ')
        departure_date = datetime.strptime(dates[0], '%b %d')
        return_date = datetime.strptime(dates[1], '%b %d')
        guests = int(request.form['guests'])
        price = 200.0 

        new_flight = Flight(
            from_city=from_city, to_city=to_city, departure_date=departure_date, 
            return_date=return_date, available_seats=100, booked_seats=0, price=price
        )
        db.session.add(new_flight)
        db.session.commit()

        return redirect(url_for('home'))
    
    return render_template('add_flight_form.html')


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    bookings = db.relationship('Booking', backref='user', lazy=True)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    destination = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    flight_id = db.Column(db.Integer, db.ForeignKey('flight.id'), nullable=False)
    
    flight = db.relationship('Flight', backref='bookings', lazy=True)

    check_in = db.Column(db.Date, nullable=False)
    check_out = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f"<Booking {self.id} for {self.destination}>"



@app.route('/')
def home():
    page = request.args.get('page', 1, type=int)

    user_logged_in = 'user_id' in session
    user = None
    if user_logged_in:
        user = User.query.get(session['user_id'])

    booked_flight_ids = []
    if user_logged_in:
        booked_flight_ids = [booking.flight_id for booking in user.bookings]

    flights = Flight.query.filter(Flight.id.notin_(booked_flight_ids)) \
                          .paginate(page=page, per_page=15, error_out=False)

    return render_template('index.html', 
                           flights=flights.items, 
                           pagination=flights,
                           user_logged_in=user_logged_in,
                           user=user)



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('home'))
        
        return "Invalid credentials", 401

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('home'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('signup.html')

from datetime import datetime



@app.route('/search', methods=['GET'])
def search():
    from_city = request.args.get('from')
    to_city = request.args.get('to')
    dates = request.args.get('dates')
    guests = request.args.get('guests', type=int)
    page = request.args.get('page', 1, type=int)

    date_range = dates.split('→') if dates else []
    start_date = None
    end_date = None

    current_year = datetime.now().year

    if len(date_range) == 2:
        try:
            start_date = datetime.strptime(f'{current_year} {date_range[0].strip()}', '%Y %b %d').date()
            end_date = datetime.strptime(f'{current_year} {date_range[1].strip()}', '%Y %b %d').date()
            
            if start_date > datetime.now().date():
                start_date = start_date.replace(year=current_year - 1)
            if end_date > datetime.now().date():
                end_date = end_date.replace(year=current_year - 1)

        except ValueError as e:
            print(f"Error parsing dates: {e}")
            start_date = None
            end_date = None

    query = Flight.query

    if from_city:
        print(f"Filtering by from_city: {from_city}")
        query = query.filter(Flight.from_city.ilike(f'%{from_city}%'))
    if to_city:
        print(f"Filtering by to_city: {to_city}")
        query = query.filter(Flight.to_city.ilike(f'%{to_city}%'))
    
    if start_date and end_date:
        print(f"Filtering by dates: {start_date} to {end_date}")
        query = query.filter(
            (Flight.departure_date >= start_date) & (Flight.departure_date <= end_date) |
            (Flight.return_date >= start_date) & (Flight.return_date <= end_date)
        )
        
    if guests:
        print(f"Filtering by guests: {guests}")
        query = query.filter(Flight.available_seats >= guests)

    flights = query.paginate(page=page, per_page=9, error_out=False)

    search_message = []
    if from_city:
        search_message.append(f"Searching flights from {from_city}")
    if to_city:
        search_message.append(f"to {to_city}")
    if dates:
        search_message.append(f"for dates {dates}")
    if guests:
        search_message.append(f"for {guests} guest(s)")
    
    search_message = " ".join(search_message) if search_message else "Please enter your search criteria."

    user_logged_in = 'user_id' in session
    user = None
    if user_logged_in:
        user = User.query.get(session['user_id'])

    return render_template('index.html', 
                           flights=flights.items, 
                           search_message=search_message, 
                           pagination=flights, 
                           from_city=from_city, 
                           to_city=to_city, 
                           dates=dates, 
                           guests=guests,
                           user_logged_in=user_logged_in, 
                           user=user)






@app.route('/view_booking/<int:booking_id>', methods=['GET'])
def view_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    return render_template('view_booking.html', booking=booking)

@app.route('/cancel_booking/<int:booking_id>', methods=['GET', 'POST'])
def cancel_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)

    if 'user_id' not in session:
        return redirect(url_for('login')) 
    user = User.query.get(session['user_id'])

    if request.method == 'POST':
        db.session.delete(booking)
        db.session.commit()

        return redirect(url_for('profile', user_id=user.id))

    return render_template('cancel_booking.html', booking=booking, user=user)




@app.route('/profile/<int:user_id>', methods=['GET'])
def profile(user_id):
    if 'user_id' not in session or session['user_id'] != user_id:
        return redirect(url_for('login'))

    user = User.query.get_or_404(user_id)
    
    bookings = Booking.query.filter_by(user_id=user_id).all()
    
    flight_booked_seats = {}
    
    for booking in bookings:
        flight = booking.flight
        if flight.id not in flight_booked_seats:
            flight_booked_seats[flight.id] = 0
        flight_booked_seats[flight.id] += 1
    
    return render_template('profile.html', user=user, bookings=bookings, flight_booked_seats=flight_booked_seats)




@app.route('/booking', methods=['POST'])
def booking():
    if request.method == 'POST':
        destination = request.form['destination']
        check_in = request.form['check_in']
        check_out = request.form['check_out']
        user_id = request.form['user_id']
        flight_id = request.form['flight_id']
        
        new_booking = Booking(
            destination=destination, 
            check_in=check_in, 
            check_out=check_out, 
            user_id=user_id,
            flight_id=flight_id
        )
        db.session.add(new_booking)
        db.session.commit()

        return redirect(url_for('profile', user_id=user_id))


if __name__ == '__main__':
    app.run(debug=True)
