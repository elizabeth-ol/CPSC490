import os
from flask import Flask, session, request, redirect, make_response, render_template, url_for
from flask_session import Session
from flask_cas import CAS, login_required, login, logout, routing
import sqlite3
import json

setattr(routing, 'basestring', str)


# app = Flask(__name__, template_folder='pages')
# app.config['SECRET_KEY'] = os.urandom(64)
# app.config['SESSION_TYPE'] = 'filesystem'
# app.config['SESSION_FILE_DIR'] = './.flask_session/'
# Session(app)

app = Flask(__name__, template_folder='templates', static_folder='static')
cas = CAS(app)
app.config['CAS_SERVER'] = 'https://secure6.its.yale.edu/cas/'
app.config['CAS_AFTER_LOGIN'] = 'https://127.0.0.1:5001/'
app.config['CAS_AFTER_LOGOUT'] = 'https://127.0.0.1:5001/'
app.secret_key = os.urandom(64)

#----------------------------------------------------------
# @app.before_request
# def before_request():
#     if not request.is_secure:
#         url = request.url.replace('http://', 'https://', 1)
#         return redirect(url, code=301)

#-----------------------------------------------------------------

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
@login_required
def index():

    html = render_template('index.html')
        #username=cas.username) # Can get token with cas.token
        #could we add a button that leads to CAS log-in?
    response = make_response(html)
    return response

@app.route('/projects')
def project_nav():

    query = "SELECT id, project_title, student_name, classyear, track, thumbnail_alt FROM student_projects"

    with sqlite3.connect('projects.db') as connection:
        cursor = connection.cursor()
        cursor.execute(query)
        projects_data = cursor.fetchall()

    projects = []
    for project_data in projects_data:
        project = {
            'id': project_data[0],
            'url': f"/project/{project_data[0]}",
            'thumbnail_path': url_for('static', filename=f'projects/{project_data[0]}/images/thumbnail.png'),
            'project_title': project_data[1],
            'student_name': project_data[2],
            'classyear': project_data[3],
            'track': project_data[4],
            'thumbnail_alt': project_data[5],
            }
        projects.append(project)
       
    yearquery = "SELECT DISTINCT classyear FROM student_projects"
    
    with sqlite3.connect('projects.db') as connection:
        cursor = connection.cursor()
        cursor.execute(yearquery)
        classyears_data = cursor.fetchall()

    # Extract years from the result
        classyear_options = [years[0] for years in classyears_data]

    # Query for distinct tracks
    track_query = "SELECT DISTINCT track FROM student_projects"
    with sqlite3.connect('projects.db') as connection:
        cursor = connection.cursor()
        cursor.execute(track_query)
        tracks_data = cursor.fetchall()
        track_options = [track[0] for track in tracks_data]

    return render_template('project_nav.html', projects=projects, classyear_options=classyear_options, track_options=track_options)


#Route for showing details of a project when it is selected
@app.route('/project/<int:project_id>')
def project_details(project_id):

    #Get all the data we need for project details
    with sqlite3.connect('projects.db') as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM student_projects WHERE id = ?", (project_id,))
        project_data = cursor.fetchone()

    if project_data:
        # Dictionary with info about project to use in template
        project = {
            'id': project_data[0],
            'project_title': project_data['project_title'],
            'student_name': project_data['student_name'],
            'project_description': project_data['project_description'],
            'thumbnail_path': url_for('static', filename=f'projects/{project_data[0]}/images/thumbnail.png'),
            'thumbnail_alt': project_data['thumbnail_alt'],
            'track': project_data['track'],
            'classyear': project_data['classyear'],
            'image1_path': url_for('static', filename=f'projects/{project_data[0]}/images/image1.png'),
            'image1_alt': project_data['image1_alt'],
            'image2_alt': project_data['image2_alt'],
            'video1_link': project_data['video1_link'],
            'video1_alt': project_data['video1_alt'],
            'video2_link': project_data['video2_link'],
            'video2_alt': project_data['video2_alt'],
        }

        # Render project page with all details
        return render_template('project_details.html', project=project)
    else:
        # Error with finding project
        return 'Project not found', 404


#Route for adding new projects
@app.route("/newproject", methods=["GET", "POST"])
@login_required
def newproject():

    if request.method == "POST":
        student_name = request.form.get("student_name")
        project_title = request.form.get("project_title")
        classyear = request.form.get("classyear")
        track = request.form.get("track")
        project_description = request.form.get("project_description")
        thumbnail = request.files['thumbnail']
        thumbnail_alt = request.form.get("thumbnail")
        image1 = request.files['image1']
        image1_alt = request.form.get("image1_alt")
        image2 = request.files['image2']
        image2_alt = request.form.get("image2_alt")
        video1_link = request.form.get("video1_link")
        video2_link = request.form.get("video2_link")
        video1_alt = request.form.get("video1_alt")
        video2_alt = request.form.get("video2_alt")


        query = """
                INSERT INTO student_projects (student_name, project_title, classyear, track, project_description,thumbnail_alt, image1_alt, image2_alt, video1_link, video2_link, video1_alt, video2_alt)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """

        data = (student_name, project_title, classyear, track, project_description,thumbnail_alt, image1_alt, image2_alt, video1_link, video2_link, video1_alt, video2_alt)

        with sqlite3.connect('projects.db') as connection:
                cursor = connection.cursor()
                cursor.execute(query, data)
                project_id = cursor.lastrowid
                connection.commit()
        
        # Creating the folder
        project_folder = os.path.join("static", "projects", str(project_id))
        images_folder = os.path.join(project_folder, "images")
        os.makedirs(images_folder)

        # Saving uploaded images to folder based on id for rendering later
        thumbnail = request.files['thumbnail']
        image1 = request.files['image1']
        image2 = request.files['image2']

        thumbnail.save(os.path.join(images_folder, "thumbnail.png"))
        image1.save(os.path.join(images_folder, "image1.png"))
        image2.save(os.path.join(images_folder, "image2.png"))

    return render_template('newproject.html')



#------------------------------------------------------------------

if __name__ == "__main__": 
    app.run(debug=True) 