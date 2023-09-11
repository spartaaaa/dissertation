#!/usr/bin/env python
import sqlite3

def calculate_average_cpu_usage():
    conn = sqlite3.connect('sdata.db')
    cursor = conn.cursor()

    # Get unique message values from the sdata table
    cursor.execute("SELECT DISTINCT msg FROM sdata")
    unique_messages = [row[0] for row in cursor.fetchall()]

    total_cpu_usage = 0
    num_entries = 0

    # Calculate the sum of CPU usage for each unique message
    for msg in unique_messages:
        cursor.execute("SELECT cpu_usage FROM sdata WHERE msg = ?", (msg,))
        cpu_usages = [row[0] for row in cursor.fetchall()]

        if cpu_usages:
            # Calculate the average CPU usage for the current message
            average_cpu_usage = sum(cpu_usages) / len(cpu_usages)
            total_cpu_usage += average_cpu_usage
            num_entries += 1

            print(f"Average CPU Usage for message '{msg}': {average_cpu_usage:.2f}%")

    # Calculate the overall average CPU usage
    overall_average_cpu_usage = total_cpu_usage / num_entries if num_entries > 0 else 0

    print(f"Overall Average CPU Usage: {overall_average_cpu_usage:.2f}%")

    conn.close()

if __name__ == '__main__':
    calculate_average_cpu_usage()