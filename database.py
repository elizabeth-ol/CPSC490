import sqlite3
from sqlite3 import connect
from contextlib import closing

DB_NAME = "CPARprojects.db"

connection = sqlite3.connect(DB_NAME)
cursor = connection.cursor()

# Table that stores project info
#look for documentation - with terminal
#need to add error checkign 

#add UPI as id??? does that make sense? 
#maybe add CAS so they can view their own page 
cursor.execute('''
    CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY,
        project_title TEXT NOT NULL,
        project_description TEXT NOT NULL,
        thumbnail_path TEXT NOT NULL,
        student_name TEXT NOT NULL,
        image1_path TEXT,
        image2_path TEXT,
        image3_path TEXT,
        video1_path TEXT,
        video2_path TEXT,
        video3_path TEXT,
        track TEXT

    )
''')
connection.commit()
connection.close()
