import os
import sqlite3

DB_NAME = "CPARprojects.db"
PROJ_DIR = "projects"

connection = sqlite3.connect(DB_NAME)
cursor = connection.cursor()



for project_folder in os.listdir(PROJ_DIR):
    project_folder_path = os.path.join(PROJ_DIR, project_folder)
    if os.path.isdir(project_folder_path):
        img_folder = os.path.join(project_folder_path, "images")
        txt_folder = os.path.join(project_folder_path, "text")

        thumbnail_path = os.path.join(img_folder, "thumbnail.jpg")
        description_path = os.path.join(txt_folder, "projdescription.txt")
        title_path = os.path.join(txt_folder, "title.txt")
        thumbnail_path = os.path.join(img_folder, "thumbnail.jpg")

        if os.path.exists(thumbnail_path) and os.path.exists(description_path) and os.path.exists(title_path):
            with open(description_path, "r") as description_file:
                description = description_file.read().strip()
            with open(title_path, "r") as title_file:
                project_title = title_file.read().strip()

            if description and project_title:
                # Insert title, description, and image file path into the database
                cursor.execute('''
                    INSERT INTO projects (project_title, project_description, thumbnail_path) VALUES (?, ?, ?)
                ''', (project_title, description, thumbnail_path))
        else:
            print(f"Skipping {project_folder} due to missing image, title, or description file.")



connection.commit()
connection.close()