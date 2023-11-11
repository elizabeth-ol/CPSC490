import os
from flask import Flask, session, request, redirect, make_response, render_template
from flask_session import Session
from flask_cas import CAS, login_required, login, logout, routing
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
    'project_title': 'static/projects/RosaChang/text/title.txt',
    'thumbnail_path': 'static/projects/RosaChang/images/thumbnail.webp',
    'student_path': 'static/projects/RosaChang/text/name.txt'
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
    for project in projects:
        project_title_path = project['project_title']
        student_name_path = project['student_path']
        try:
            with open(project_title_path, 'r') as title_file:
                project['project_title'] = title_file.read()
        except FileNotFoundError:
            project['project_title'] = 'Title not found'
        try:
            with open(student_name_path, 'r') as name_file:
                project['student_path'] = name_file.read()
        except FileNotFoundError:
            project['student_path'] = 'Name not found'
    return render_template('project_nav.html', projects=projects)


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