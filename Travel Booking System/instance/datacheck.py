from datetime import datetime

def is_date(value):
    return isinstance(value, datetime.date)

test_values = [
    "2025-04-02",
    datetime.now(),
    datetime(2025, 4, 2).date(),
    20250402,
    "March 15, 2025",
]

for value in test_values:
    result = is_date(value)
    print(f"Value: {value} - Is date? {result}")
