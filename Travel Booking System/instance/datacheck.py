from datetime import datetime

# Function to check if a given value is a date type
def is_date(value):
    return isinstance(value, datetime.date)

# Test examples
test_values = [
    "2025-04-02",  # string (not a date)
    datetime.now(),  # datetime object (not a date)
    datetime(2025, 4, 2).date(),  # date object (should return True)
    20250402,  # integer (not a date)
    "March 15, 2025",  # string (not a date)
]

# Check each test value
for value in test_values:
    result = is_date(value)
    print(f"Value: {value} - Is date? {result}")
