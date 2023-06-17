from server import app
from . import response
from flask import redirect, request
from flask_wtf.csrf import generate_csrf, validate_csrf
from model import database_connection
from hashlib import sha256
from model import course_data

@app.route('/course_registration')
@app.route('/course_registration/')
def course_registration():
    response_data = {}
    form_csrf_token = generate_csrf(token_key="course_registration_form")
    response_data['form_csrf_token'] = form_csrf_token
    return response.ok(response_data)

@app.route('/course_registration/submit', methods=['POST'])
def submit_course_registration():
    response_data = {}
    form_csrf_token = request.form['form_csrf_token']
    validate_csrf(form_csrf_token)
    # TODO
    dbconn = database_connection.get_postgres_connection()
    return response.ok("")


@app.route('/')
def home():
    return response.ok("")

@app.route('/course/')
@app.route('/course')
def course():
    return redirect('/course/recommended')

@app.route('/course/recommended')
def course_recommended():
    recommended_course = course_data.get_course_recommended()
    # TODO
    return response.ok("")



