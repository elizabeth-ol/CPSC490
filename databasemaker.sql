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


/* Command to open the SQL terminal*/
sqlite3 projects.db

/* this is the command to delete a project from the student_projects table in projects.db */
DELETE FROM student_projects WHERE id = #;

/* this is the command to add an admin user to the admin_users table in projects.db */
INSERT INTO admin_users (netid) VALUES ('insertnetidhere');

/* this is the command to insert multiple users to the admin_users table in projects.db */
INSERT INTO admin_users (netid) VALUES ('insertnetidhere'), ('insertnetidhere'), ('insertnetidhere');

/* this is the command to drop an admin user from the admin_users table in projects.db */
DELETE FROM admin_users WHERE netid = "insertnetidhere";

/* Command to close the SQL terminal*/
ctrl+D