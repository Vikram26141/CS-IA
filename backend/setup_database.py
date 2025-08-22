#!/usr/bin/env python3
"""
Database setup script for Football Coach application
Run this script to create the MySQL database and tables
"""

import mysql.connector
from config import Config

def create_database():
    """Create the database if it doesn't exist"""
    try:
        # Connect without specifying database
        conn = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD
        )
        cursor = conn.cursor()
        
        # Create database
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {Config.MYSQL_DATABASE}")
        print(f"Database '{Config.MYSQL_DATABASE}' created successfully!")
        
        cursor.close()
        conn.close()
        return True
    except mysql.connector.Error as e:
        print(f"Error creating database: {e}")
        return False

def setup_tables():
    """Create necessary tables"""
    try:
        conn = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DATABASE
        )
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                email VARCHAR(255) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        print("Users table created successfully!")
        
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except mysql.connector.Error as e:
        print(f"Error creating tables: {e}")
        return False

if __name__ == "__main__":
    print("Setting up Football Coach database...")
    print(f"Host: {Config.MYSQL_HOST}")
    print(f"User: {Config.MYSQL_USER}")
    print(f"Database: {Config.MYSQL_DATABASE}")
    print("-" * 40)
    
    if create_database():
        if setup_tables():
            print("\n✅ Database setup completed successfully!")
            print("\nYou can now run the application with:")
            print("python app.py")
        else:
            print("\n❌ Failed to create tables")
    else:
        print("\n❌ Failed to create database")
