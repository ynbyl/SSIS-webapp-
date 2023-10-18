import mysql.connector

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "admin",
}

connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()

database_name = "mydb"
cursor.execute(f"CREATE DATABASE {database_name}")

cursor.execute(f"USE {database_name}")

cursor.execute('''CREATE TABLE Colleges (
    collegecode VARCHAR(255) PRIMARY KEY,
    collegename VARCHAR(255) NOT NULL
)''')

cursor.execute('''CREATE TABLE Courses (
    coursecode VARCHAR(255) PRIMARY KEY,
    coursename VARCHAR(255) NOT NULL,
    collegecode VARCHAR(255),
    FOREIGN KEY (collegecode) REFERENCES Colleges(collegecode)
)''')

cursor.execute('''CREATE TABLE Students (
    id VARCHAR(255) PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    year_level INT NOT NULL,
    gender VARCHAR(255) NOT NULL,
    coursecode VARCHAR(255),
    FOREIGN KEY (coursecode) REFERENCES Courses(coursecode)
)''')

connection.commit()
connection.close()
