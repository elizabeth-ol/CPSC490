/* this is the command to make the student_projects table in projects.db */
CREATE TABLE student_projects(
id INTEGER PRIMARY KEY,
student_name TEXT,
project_title TEXT,
thumbnail_alt TEXT,
track TEXT,
project_description TEXT,
classyear TEXT,
image1_alt TEXT,
image2_alt TEXT,
video1_link TEXT,
video1_alt TEXT,
video2_link TEXT,
video2_alt TEXT
);

/* this is the command to make the admin users table in projects.db */
CREATE TABLE admin_users(
    id INTEGER PRIMARY KEY,
    netid TEXT
);