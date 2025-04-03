from sqlalchemy import create_engine, inspect

DATABASE_URI = 'sqlite:///travel_booking.db' 

engine = create_engine(DATABASE_URI)

inspector = inspect(engine)

tables = inspector.get_table_names()

for table in tables:
    print(f"Table: {table}")
    columns = inspector.get_columns(table)
    column_names = [column['name'] for column in columns]
    print(f"  Columns: {', '.join(column_names)}")
    print()
