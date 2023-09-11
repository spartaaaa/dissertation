#!/usr/bin/env python
import sqlite3
from datetime import datetime

def calculate_time_difference_and_average():
    conn = sqlite3.connect('ldata.db')
    cursor = conn.cursor()

    total_time_difference = 0
    num_unique_messages = 0  # Initialize the count of unique messages

    # Calculate the time difference and sum of CPU usage for each unique message value
    cursor.execute("SELECT DISTINCT msg FROM ldata")
    unique_messages = [row[0] for row in cursor.fetchall()]

    for msg in unique_messages:
        cursor.execute("SELECT MIN(time), MAX(time) FROM ldata WHERE msg = ?", (msg,))
        min_time_str, max_time_str = cursor.fetchone()

        if min_time_str and max_time_str:
            # Convert string timestamps to datetime objects
            min_time = datetime.strptime(min_time_str, '%Y-%m-%d %H:%M:%S.%f')
            max_time = datetime.strptime(max_time_str, '%Y-%m-%d %H:%M:%S.%f')

            # Calculate the time difference in seconds and add it to the total
            time_difference = (max_time - min_time).total_seconds()
            total_time_difference += time_difference
            num_unique_messages += 1  # Increment the count for each unique message

    # Calculate the average time difference by dividing by the number of unique messages
    average_time_difference = total_time_difference / num_unique_messages if num_unique_messages > 0 else 0

    total_time_difference_ms = total_time_difference * 1000  # Convert to milliseconds
    average_time_difference_ms = average_time_difference * 1000  # Convert to milliseconds

    print(f"Total Time Difference (milliseconds): {total_time_difference_ms:.2f}")
    print(f"Average Time Difference (milliseconds): {average_time_difference_ms:.2f}")


    conn.close()

if __name__ == '__main__':
    calculate_time_difference_and_average()