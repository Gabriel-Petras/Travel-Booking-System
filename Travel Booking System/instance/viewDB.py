from sqlalchemy import create_engine, inspect

# Set up the database connection
DATABASE_URI = 'sqlite:///travel_booking.db'  # Path to your SQLite database

# Create an engine and connect to the database
engine = create_engine(DATABASE_URI)

# Create an inspector object to inspect the database
inspector = inspect(engine)

# Get all table names in the database
tables = inspector.get_table_names()

# Loop through each table and print its column names
for table in tables:
    print(f"Table: {table}")
    columns = inspector.get_columns(table)
    column_names = [column['name'] for column in columns]
    print(f"  Columns: {', '.join(column_names)}")
    print()  # Print a blank line between tables
