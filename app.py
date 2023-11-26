import os
from flask import Flask, session, request, redirect, make_response, render_template
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

app = Flask(__name__, template_folder='templates')
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

#how do we add the projects data here from DATABASE

projects = [
    {
    'id': 1,
    'project_title': 'Hi there',
    'project_description': 'I am project',
    'author': 'Rosa Chang',
    }

]



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

    query = "SELECT id, project_title, student_name FROM student_projects"

    with sqlite3.connect('student_projects.db') as connection:
        cursor = connection.cursor()
        cursor.execute(query)
        projects = cursor.fetchall()

    for project in projects:
        #maybe buikd paths here to pass to template
        project['thumbnail_path'] = f'./static/projects/{project["id"]}/images/thumbnail.png'
        # project_title_path = project['project_title']
        # student_name_path = project['student_path']
        # try:
        #     with open(project_title_path, 'r') as title_file:
        #         project['project_title'] = title_file.read()
        # except FileNotFoundError:
        #     project['project_title'] = 'Title not found'
        # try:
        #     with open(student_name_path, 'r') as name_file:
        #         project['student_path'] = name_file.read()
        # except FileNotFoundError:
        #     project['student_path'] = 'Name not found'
    return render_template('project_nav.html', projects=projects)

@app.route("/newproject", methods=["GET", "POST"])
@login_required
def newproject():

    if request.method == "POST":
        student_name = request.form.get("student_name")
        project_title = request.form.get("project_title")
        classyear = request.form.get("classyear")
        track = request.form.get("track")
        project_description = request.form.get("project_description")
        thumbnail_alt = request.form.get("thumbnail_alt")
        image1_alt = request.form.get("image1_alt")
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
                connection.commit()

    return render_template('newproject.html')


# @app.route('/project/<int:project_id>')
# def project_detail(project_id):
#     # In a real application, you'd fetch project details from your database
#     # or data source based on project_id.
#     # For this example, we'll use sample data.
#     project = next((p for p in projects if p['id'] == project_id), None)
#     if project:
#         return render_template('project_detail.html', project=project)
#     else:
#         return 'Project not found'


# @app.route('/projects', methods=['GET'])
# @login_required
# def projects():
#     # how would we get the list of all projects and their thumbnails?
#     #something like 
#     return render_template("project_nav.html") #info=info, etc etc something like that
#     #would include thumbnail image, title of project and person who made it, and link to the page?
#     #how would we generate these pages?


#------------------------------------------------------------------

if __name__ == "__main__": 
    app.run(debug=True) 