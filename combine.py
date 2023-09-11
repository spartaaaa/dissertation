#!/usr/bin/env python
import sqlite3

def create_ldata_table(cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS ldata (
                        time TIMESTAMP DEFAULT (STRFTIME('%Y-%m-%d %H:%M:%f', 'NOW')),
                        msg INTEGER,
                        cpu_usage FLOAT,
                        ram_usage FLOAT
                    )''')

def combine_tables():
    # Connect to the databases
    conn_sdata = sqlite3.connect('sdata.db')
    conn_pdata = sqlite3.connect('pdata.db')
    conn_ldata = sqlite3.connect('ldata.db')

    cursor_sdata = conn_sdata.cursor()
    cursor_pdata = conn_pdata.cursor()
    cursor_ldata = conn_ldata.cursor()

    # Create the ldata table if it doesn't exist
    create_ldata_table(cursor_ldata)

    # Retrieve data from sdata and insert it into ldata
    cursor_sdata.execute("SELECT * FROM sdata")
    sdata_rows = cursor_sdata.fetchall()
    for row in sdata_rows:
        cursor_ldata.execute("INSERT INTO ldata VALUES (?, ?, ?, ?)", row)

    # Retrieve data from pdata and insert it into ldata
    cursor_pdata.execute("SELECT * FROM pdata")
    pdata_rows = cursor_pdata.fetchall()
    for row in pdata_rows:
        cursor_ldata.execute("INSERT INTO ldata VALUES (?, ?, ?, ?)", row)

    # Commit the changes and close connections
    conn_ldata.commit()
    conn_sdata.close()
    conn_pdata.close()
    conn_ldata.close()

if __name__ == '__main__':
    combine_tables()
