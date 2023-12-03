import os
from flask import Flask, session, request, redirect, make_response, render_template, url_for
from flask_session import Session
from flask_cas import CAS, login_required, login, logout, routing
import sqlite3
import json
import logging

setattr(routing, 'basestring', str)
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

# This is code from the retired homepage
# @app.route('/', methods=['GET'])
# @app.route('/index', methods=['GET'])
# @login_required
# def index():

#     html = render_template('index.html')
#         #username=cas.username) # Can get token with cas.token if needed
#     response = make_response(html)
#     return response

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
@app.route('/projects')
@login_required
def project_nav():

    #Collecting information needed for the project thumbnail
    query = "SELECT id, project_title, student_name, classyear, track, thumbnail_alt FROM student_projects"
    with sqlite3.connect('projects.db') as connection:
        cursor = connection.cursor()
        cursor.execute(query)
        projects_data = cursor.fetchall()

    #Filling projects info to pass into template for rendering
    projects = []
    for project_data in projects_data:
        formatted_title = project_data[1].replace(' ', '-')
        project = {
            'id': project_data[0],
            'url': f"/project/{project_data[0]}/{formatted_title}",
            'thumbnail_path': url_for('static', filename=f'projects/{project_data[0]}/images/thumbnail.png'),
            'project_title': project_data[1],
            'student_name': project_data[2],
            'classyear': project_data[3],
            'track': project_data[4],
            'thumbnail_alt': project_data[5],
            }
        projects.append(project)
       
    # Adding years to the dropdown
    yearquery = "SELECT DISTINCT classyear FROM student_projects"
    with sqlite3.connect('projects.db') as connection:
        cursor = connection.cursor()
        cursor.execute(yearquery)
        classyears_data = cursor.fetchall()
        classyear_options = [years[0] for years in classyears_data]

    # Adding tracks to the dropdown
    track_query = "SELECT DISTINCT track FROM student_projects"
    with sqlite3.connect('projects.db') as connection:
        cursor = connection.cursor()
        cursor.execute(track_query)
        tracks_data = cursor.fetchall()
        track_options = [track[0] for track in tracks_data]

    return render_template('project_nav.html', projects=projects, classyear_options=classyear_options, track_options=track_options)


def format_title_from_url(url_title):
    return url_title.replace('-', ' ')



#Route for when new page is opened with the project details
@app.route('/project/<int:project_id>/<path:project_title>')
def project_details(project_id, project_title):

    #This is how we handle making the title with dashes and then getting rid of them for the query
    formatted_title = project_title
    original_title = format_title_from_url(formatted_title)

    #Data we need for project details
    with sqlite3.connect('projects.db') as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM student_projects WHERE id = ? AND project_title = ?", (project_id, original_title))
        project_data = cursor.fetchone()

    if project_data:
        project = {
            'id': project_data[0],
            'project_title': project_data['project_title'],
            'student_name': project_data['student_name'],
            'project_description': project_data['project_description'],
            'track': project_data['track'],
            'classyear': project_data['classyear'],
            'thumbnail_alt': project_data['thumbnail_alt'],
            'thumbnail_path': url_for('static', filename=f'projects/{project_data[0]}/images/thumbnail.png'),
             # if os.path.exists(f'projects/{project_data[0]}/images/thumbnail.png') else '',
            'image1_alt': project_data['image1_alt'],
            'image1_path': url_for('static', filename=f'projects/{project_data[0]}/images/image1.png'),#if os.path.exists(f'projects/{project_data[0]}/images/image1.png') else '',
            'image2_alt': project_data['image2_alt'],
            'image2_path': url_for('static', filename=f'projects/{project_data[0]}/images/image2.png'), # if os.path.exists(f'projects/{project_data[0]}/images/image2.png') else '',
            'video1_link': project_data['video1_link'] if project_data['video1_link'] else None,  # Check if video1_link exists in the database
            'video1_alt': project_data['video1_alt'] if project_data['video1_link'] else None,  # If video1_link doesn't exist, set video1_alt to None
            'video2_link': project_data['video2_link'] if project_data['video2_link'] else None,  # Check if video2_link exists in the database
            'video2_alt': project_data['video2_alt'] if project_data['video2_link'] else None,  # If video2_link doesn't exist, set video2_alt to None
            'sourcecode_path': url_for('static', filename=f'projects/{project_data[0]}/sourcecode.zip'),
            #if os.path.exists(f'projects/{project_data[0]}/sourcecode.zip') else '',
            'finalreport_path': url_for('static', filename=f'projects/{project_data[0]}/finalreport.pdf'),
             # if os.path.exists(f'projects/{project_data[0]}/finalreport.pdf') else '',
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

    #This is initializing success message so we can use it later
    #to show success in uploading to database
    success_message = None  

    if request.method == "POST":
        #Getting all the information from the form
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
            sourcecode = request.files['sourcecode']
            final_report = request.files['final_report']


            #Making the query for inserting all of the information into the database
            query = """
                    INSERT INTO student_projects (student_name, project_title, classyear, track, project_description,thumbnail_alt, image1_alt, image2_alt, video1_link, video2_link, video1_alt, video2_alt)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """
            #Getting all the information and inserting into the database with the query above
            data = (student_name, project_title, classyear, track, project_description,thumbnail_alt, image1_alt, image2_alt, video1_link, video2_link, video1_alt, video2_alt)
            with sqlite3.connect('projects.db') as connection:
                    cursor = connection.cursor()
                    cursor.execute(query, data)
                    project_id = cursor.lastrowid
                    connection.commit()
            
            #Once the data is uploaded, this acts as a confirmation to the user
            #and will appear on top of the screen
            success_message = "Project successfully uploaded!"
            
            # Creating folder to store images and source code
            project_folder = os.path.join("static", "projects", str(project_id))
            images_folder = os.path.join(project_folder, "images")
            os.makedirs(images_folder)

            #Only saving things if they were uploaded
            if thumbnail:
                thumbnail.save(os.path.join(images_folder, "thumbnail.png"))
            if image1:
                image1.save(os.path.join(images_folder, "image1.png"))
            if image2:
                image2.save(os.path.join(images_folder, "image2.png"))
            if sourcecode:
                sourcecode.save(os.path.join(project_folder, "sourcecode.zip"))
            if final_report:
                final_report.save(os.path.join(project_folder, "finalreport.pdf"))
            
            return render_template('newproject.html', success_message=success_message)
     #Data we need for project details
    with sqlite3.connect('projects.db') as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM admin_users WHERE netid = ?", (cas.username,))
        admin_user = cursor.fetchone()
    if admin_user:
        return render_template('newproject.html', success_message=success_message)
    else:
        return render_template('forbidden.html')


#------------------------------------------------------------------

if __name__ == "__main__": 
    app.run(debug=True) 