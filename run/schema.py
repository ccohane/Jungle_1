#!/usr/bin/env python3

import sqlite3

connection = sqlite3.connect('jungle.db', check_same_thread=False)
cursor = connection.cursor()

# TO create db and tables
cursor.execute(
    """CREATE TABLE users(
        pk INTEGER PRIMARY KEY AUTOINCREMENT,
        username VARCHAR,
        password VARCHAR
    );"""
)

cursor.execute(
    """CREATE TABLE restaurants(
        pk INTEGER PRIMARY KEY AUTOINCREMENT,
        business_id VARCHAR,
        categories VARCHAR,
        name VARCHAR,
        is_open VARCHAR,
        view_count INTEGER,
        stars INTEGER,
        address VARCHAR,
        state VARCHAR,
        city VARCHAR,
        postal_code VARCHAR
    );"""
)

cursor.execute(
    """CREATE TABLE reviews(
        pk INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id VARCHAR,
        business_id VARCHAR,
        stars INTEGER,
        date  INTEGER,
        review VARCHAR
    );"""
)


