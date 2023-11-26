import os
import sqlite3

def populate_db_text(txt_folder_path, db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    for file in os.listdir(txt_folder_path):
        if file.endswith('.txt'):
            file_path = os.path.join(txt_folder_path, file)
            with open(file_path, 'r') as txt_file:
                content = txt_file.read().strip()
                # Insert into the database
                cursor.execute("INSERT INTO projects (project_title, project_description, track, student_name) VALUES (?)", (content,))

    conn.commit()
    conn.close()

# Replace 'your_folder_path' and 'your_db_path' with actual paths
populate_db_text('your_folder_path', 'your_db_path')