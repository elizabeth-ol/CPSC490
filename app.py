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
@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
@login_required
def index():

    html = render_template('index.html')
        #username=cas.username) # Can get token with cas.token
    response = make_response(html)
    return response

#------------------------------------------------------------------

if __name__ == "__main__": 
    app.run(debug=True) 