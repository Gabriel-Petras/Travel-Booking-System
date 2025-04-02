import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('instance/travel_booking.db')

# Create a cursor object to interact with the database
cursor = conn.cursor()

# Query the User table (change table name if necessary)
cursor.execute("SELECT * FROM user")  # Replace 'user' with your table name

# Fetch all results
rows = cursor.fetchall()

# Print the rows
for row in rows:
    print(row)

# Close the connection to the database
conn.close()
