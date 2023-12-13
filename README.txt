Welcome to the CPAR Senior Project archive website!

To run the application once everything is installed and ready, you can type "flask run" into the terminal.

To get started, you should run the CREATE TABLE commands in databasemaker.sql to create 
the database and tables necessary if they do not appear.

You must add people to the admin_users database for them to be able to add projects using /newprojects.
Information on how to do so is in databasemaker.sql

Projects will be automatically rendered once added on the /newproject, with limited fields for now.
Each field MUST be filled out for the projects to render correctly.

In terms of content: each project will have a Student Name, Project Title, Grad Year, Track, and alt text
In terms of media: each project should have a thumbnail image (300px by 300 px) and two additional videos
as well as two Youtube videos, Source Code and a pdf of the final report.


In the newproject.html, years for class years should be added each year, as well as tracks if new ones are added.

Things need to be installed:
Flask: pip install Flask https://flask.palletsprojects.com/en/3.0.x/installation/
CAS: python3 -m pip install Flask-cas-ng https://github.com/MasterRoshan/flask-cas-ng
Jinja: pip install Jinja2 https://jinja.palletsprojects.com/en/2.9.x/intro/
Sqlite3: Can be downloaded and then accessed. https://www.sqlitetutorial.net/download-install-sqlite/
SSL Cert: Current certificate is generated locally with:
     openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem  -days 365, 
     this helped resolve an error:https://stackoverflow.com/questions/68275857/urllib-error-urlerror-urlopen-error-ssl-certificate-verify-failed-certifica
    SSL should not be generated locally when this is actually used.




