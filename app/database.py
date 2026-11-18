import sqlite3

def connect_db():
    connection = sqlite3.connect("expenses.db")
    return connection


def initialize_db():
    connection = connect_db()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            category TEXT,
            amount REAL,
            description TEXT
        )
    """)

    connection.commit()
    connection.close()

