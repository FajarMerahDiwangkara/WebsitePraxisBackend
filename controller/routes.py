from server import app
from . import response

from flask import redirect, request, make_response, jsonify
from http import HTTPStatus
from flask_wtf.csrf import generate_csrf, validate_csrf

import math
import re

from model import database_connection   
from datetime import date, datetime
from uuid import uuid4

import bcrypt

@app.route('/', methods=['GET'])
def home_page():
    return home_page_function()

@app.route('/login', methods=['GET'])
@app.route('/login/', methods=['GET'])
def login_page():
    return login_page_function()

@app.route('/login/submit', methods=['POST'])
def login_submit():
    return login_submit_function()

@app.route('/register', methods=['GET'])
@app.route('/register/', methods=['GET'])
def register_page():
    return register_page_function()

@app.route('/register/submit', methods=['POST'])
def register_submit():
    return register_submit_function()

# route function

def home_page_function():
    return response.ok("")

def register_page_function():
    response_data = {}
    response_code = HTTPStatus.OK.value
    if 'session' not in request.cookies:
        # call flask_wtf.csrf.generate_csrf() to force flask-wtf to generate and set session cookie to user
        generate_csrf()
    register_form_csrf_token = generate_csrf()
    response_data["register_form_csrf_token"] = register_form_csrf_token
    response = make_response(jsonify(response_data))
    # remove existing login_session_cookie
    response.set_cookie('login_session_uuid', "", 0, 0)
    return response,response_code

def register_submit_function():
    response_data = {
        "data_complete" : None,
        "csrf_token_valid" : None,
        "name_valid" : None,
        "password_valid" : None,
        "email_valid" : None,
        "email_already_exist" : None,
        "address_valid" : None,
        "education_valid" : None,
        "phone_number_valid" : None
    }
    response_code = HTTPStatus.OK.value
    # verify user sent all the data
    response_data['data_complete'] = False
    if 'name' in request.form and 'password' in request.form and 'email' in request.form and 'address' in request.form \
        and 'education' in request.form and 'phone_number' in request.form \
        and 'register_form_csrf_token' in request.form and 'session' in request.cookies:
        response_data['data_complete'] = True
        account_name = request.form['name'].strip()
        account_email = request.form['email'].strip()
        account_address = request.form['address'].strip()
        account_education = request.form['education'].strip()
        account_phone_number = request.form['phone_number'].strip()
        response_data['csrf_token_valid'] = False
        validate_csrf(request.form['register_form_csrf_token'])
        response_data['csrf_token_valid'] = True
        # https://stackoverflow.com/questions/181530/styling-multi-line-conditions-in-if-statements
        response_data['name_valid'] = False
        if (len(account_name) == 0 or account_name.isspace() or
            len(account_name) > app.config['account_name_max_length'] or 
            not re.match(app.config['account_name_regex'], account_name)):
            response_data['error_log'] = "Account name invalid, either contain invalid character, is empty string, or too long."
            response_code = HTTPStatus.BAD_REQUEST.value
            return make_response(jsonify(response_data)), response_code
        response_data['name_valid'] = True
        response_data['password_valid'] = False
        if (len(request.form['password']) == 0 or request.form['password'].isspace() or 
            len(request.form['password']) > app.config['account_password_max_length']):
            response_data['error_log'] = "Account password invalid, either contain invalid character, is empty string, or too long."
            response_code = HTTPStatus.BAD_REQUEST.value
            return make_response(jsonify(response_data)), response_code
        response_data['password_valid'] = True
        # From https://stackoverflow.com/questions/16454939/regex-to-validate-international-email
        # Regex to verify email format which include international domain email is too complicated/long/impractical, 
        # the current best way to check whether email is valid or not is to try to send verification mail to the email
        response_data['email_valid'] = False
        if (len(account_email) == 0 or account_email.isspace() or
            len(account_email) > app.config['account_email_max_length']):
            response_data['error_log'] = "Account email invalid, either contain invalid character, is empty string, or too long."
            response_code = HTTPStatus.BAD_REQUEST.value
            return make_response(jsonify(response_data)), response_code
        response_data['email_valid'] = True
        response_data['email_already_exist'] = True
        db_conn = database_connection.get_postgres_connection(
                app.config['databasewebsitepraxis_username'],
                app.config['databasewebsitepraxis_password'],
                app.config['databasewebsitepraxis_host'],
                app.config['databasewebsitepraxis_port'],
                "databasewebsitepraxis"
            )
        with db_conn.cursor() as db_cursor:
            sql_query = "SELECT * FROM " + app.config['databasewebsitepraxis_schema'] + ".account_data WHERE email = %s"
            db_cursor.execute(sql_query, (
                account_email,
            ))
            db_conn.commit()
            account_data = db_cursor.fetchone()
            if account_data is not None:
                response_data['error_log'] = "Account email already exist, unable to register."
                response_code = HTTPStatus.CONFLICT.value
                return make_response(jsonify(response_data)), response_code
        response_data['email_already_exist'] = False
        response_data['address_valid'] = False
        if (len(account_address) == 0 or account_address.isspace() or
            len(account_address) > app.config['account_address_max_length']):
            response_data['error_log'] = "Account address invalid, either is empty string, or too long."
            response_code = HTTPStatus.BAD_REQUEST.value
            return make_response(jsonify(response_data)), response_code
        response_data['address_valid'] = True
        response_data['education_valid'] = False
        if (len(account_education) == 0 or account_education.isspace() or
            len(account_education) > app.config['account_education_max_length']):
            response_data['error_log'] = "Account education invalid, either is empty string, or too long."
            response_code = HTTPStatus.BAD_REQUEST.value
            return make_response(jsonify(response_data)), response_code
        response_data['education_valid'] = True
        response_data['phone_number_valid'] = False
        if (len(account_phone_number) == 0 or account_phone_number.isspace() or
            len(account_phone_number) > app.config['account_phone_number_max_length'] or 
            not re.match(app.config['account_phone_number_regex'], account_phone_number)):
            response_data['error_log'] = "Account phone number invalid, either contain invalid character, is empty string, or too long."
            response_code = HTTPStatus.BAD_REQUEST.value
            return make_response(jsonify(response_data)), response_code
        response_data['phone_number_valid'] = True

        # at this stage, the data is valid and email does not exist, register account
        with db_conn.cursor() as db_cursor:
            sql_query = """INSERT INTO """ + app.config['databasewebsitepraxis_schema'] + \
                """.account_data VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            db_cursor.execute(sql_query, (
                str(uuid4()),
                account_name,
                hash_account_password(request.form['password']),
                account_email,
                account_address,
                account_education,
                account_phone_number,
                # TODO
                # Email verification, for now set email verified True
                True,
                datetime.strftime(datetime.now(), app.config['timestamp_format'])
            ))
            db_conn.commit()
        return make_response(jsonify(response_data)), response_code
    else:
        response_data['error_log'] =  "Some required account data or csrf token or session cookie is missing"
        return make_response(jsonify(response_data)), HTTPStatus.BAD_REQUEST.value
    
def register_success():
    response_data = {}
    response_code = HTTPStatus.OK.value

    return make_response(jsonify(response_data)), response_code

def login_page_function():
    # verify user isnt logged in
    if verify_login_status():
        return redirect('/')
    response_data = {}
    response_code = HTTPStatus.OK.value
    if 'session' not in request.cookies:
        # call flask_wtf.csrf.generate_csrf() to force flask-wtf to generate and set session cookie to user
        generate_csrf()
    login_form_csrf_token = generate_csrf()
    response_data['login_form_csrf_token'] = login_form_csrf_token
    response = make_response(jsonify(response_data))
    # remove existing login_session_cookie
    response.set_cookie('login_session_uuid', "", 0, 0)
    return response,response_code

def login_submit_function():
    # verify user isnt logged in
    if verify_login_status():
        return redirect('/')
    response_data = {}
    response_code = HTTPStatus.OK.value
    if 'session' not in request.cookies:
        # call flask_wtf.csrf.generate_csrf() to force flask-wtf to generate and set session cookie to user
        generate_csrf()
    # verify user sent all the data
    if 'email' in request.form and 'password' in request.form and 'login_form_csrf_token' in request.form and 'session' in request.cookies:
        validate_csrf(request.form['login_form_csrf_token'])
        email = request.form['email'].strip()
        password = hash_account_password(request.form['password'])
        db_conn = database_connection.get_postgres_connection(
                app.config['databasewebsitepraxis_username'],
                app.config['databasewebsitepraxis_password'],
                app.config['databasewebsitepraxis_host'],
                app.config['databasewebsitepraxis_port'],
                "databasewebsitepraxis"
            )
        with db_conn.cursor() as db_cursor:
            sql_query = "SELECT * FROM " + app.config['databasewebsitepraxis_schema'] + ".account_data WHERE email = %s and password = %s;"
            db_cursor.execute(sql_query, (
                email,
                password
            ))
            db_conn.commit()
            account_data = db_cursor.fetchone()
            if account_data is not None:
                account_uuid = account_data[0]
                session_token = request.cookies.get('session')
                session_data = generate_new_login_session_data(account_uuid, session_token)
                response = make_response(jsonify(response_data))
                response.set_cookie('login_session_uuid', session_data['login_session_uuid'])
                return response, response_code
            else:
                response_data['error_log'] = "Email or password is incorrect"
                return make_response(jsonify(response_data)), HTTPStatus.UNAUTHORIZED.value
    else:
        response_data['error_log'] =  "Email or password or csrf token or session cookie is missing"
        return make_response(jsonify(response_data)), HTTPStatus.BAD_REQUEST.value

# working function

def hash_account_password(password_string):
    # https://www.geeksforgeeks.org/hashing-passwords-in-python-with-bcrypt/
    # https://stackoverflow.com/questions/48761260/bcrypt-encoding-error
    return bcrypt.hashpw(password_string.encode('utf-8'), app.config['bcrypt_salt']).decode('utf-8')

def verify_login_status():
    # check if user logged in
    # https://stackoverflow.com/questions/13531149/check-for-a-cookie-with-python-flask
    if not 'login_session_uuid' in request.cookies:
        # if user not logged in
        return False
    else:
        # user have login session uuid cookie, check if user have session cookie
        # session cookie is automatically set by Flask-WTF
        if 'session' in request.cookies:
            # if user have login session uuid cookie and session cookie, check if login session still valid
            login_session_uuid = request.cookies.get('login_session_uuid')
            session_token = request.cookies.get('session')
            if verify_login_session(login_session_uuid, session_token):
                # login_session_uuid and session_token valid
                return True
            else:
                # login_session_uuid expired or invalid
                return False
        else:
            # user does not have session cookie
            return False

def generate_new_login_session_data(account_uuid, session_token):
    login_session_data = {
        "account_uuid" : account_uuid,
        "login_session_uuid" : str(uuid4()),
        "session_start_timestamp" : datetime.strftime(datetime.now(),
                                                      app.config["timestamp_format"]),
        "user_session_token" : session_token,
        "last_refresh_timestamp" : datetime.strftime(datetime.now(),
                                                      app.config["timestamp_format"])
    }
    db_conn = database_connection.get_postgres_connection(
        app.config['databasewebsitepraxis_username'],
        app.config['databasewebsitepraxis_password'],
        app.config['databasewebsitepraxis_host'],
        app.config['databasewebsitepraxis_port'],
        "databasewebsitepraxis"
    )
    with db_conn.cursor() as db_cursor:
        sql_query = "INSERT INTO " + app.config['databasewebsitepraxis_schema'] + ".account_login_session VALUES (%s, %s, %s, %s, %s);"
        db_cursor.execute(sql_query, (
            login_session_data['account_uuid'],
            login_session_data['login_session_uuid'],
            login_session_data['session_start_timestamp'],
            login_session_data['user_session_token'],
            login_session_data['last_refresh_timestamp']
        ))
        db_conn.commit()
    return login_session_data

def verify_login_session(login_session_uuid, session_token):
    db_conn = database_connection.get_postgres_connection(
        app.config['databasewebsitepraxis_username'],
        app.config['databasewebsitepraxis_password'],
        app.config['databasewebsitepraxis_host'],
        app.config['databasewebsitepraxis_port'],
        "databasewebsitepraxis"
    )
    with db_conn.cursor() as db_cursor:
        # https://stackoverflow.com/questions/45128902/psycopg2-and-sql-injection-security
        sql_query = """SELECT * FROM """ + app.config['databasewebsitepraxis_schema'] + """.account_login_session WHERE login_session_uuid = %s 
        AND user_session_token = %s;"""
        db_cursor.execute(sql_query, (
            login_session_uuid, 
            session_token))
        db_conn.commit()
        sql_query_result = db_cursor.fetchone()
        if sql_query_result is not None:
            # login session exist, check if login session has expired
            login_session_data = {}
            login_session_data["account_uuid"] = sql_query_result[0]
            login_session_data["login_session_uuid"] = sql_query_result[1]
            login_session_data["session_start_timestamp"] = sql_query_result[2]
            login_session_data["user_session_token"] = sql_query_result[3]
            login_session_data["last_refresh_timestamp"] = sql_query_result[4]
            login_session_last_refresh_timestamp = datetime.strptime(
                datetime.strftime(login_session_data["last_refresh_timestamp"], app.config['timestamp_format']), 
                app.config['timestamp_format'])
            # subtracting two datetime yield the result in datetime, to get total second call the total_second()
            elapsed_time_second = abs((datetime.now() - login_session_last_refresh_timestamp).total_seconds())
            if elapsed_time_second >= app.config['user_login_session_timeout_seconds']:
                # login session still active
                return True
            else:
                # login session timeout, remove session and return false
                sql_query = """DELETE FROM """ + app.config['databasewebsitepraxis_schema'] +  """.account_login_session WHERE login_session_uuid = %s 
                AND user_session_token = %s;"""
                db_cursor.execute(sql_query, 
                                  (login_session_uuid, 
                                   session_token))
                db_conn.commit()
                return False
        # no login session found
        else:
            return False

# return new login session data when success, otherwise return None
def refresh_login_session(login_session_uuid, session_token):
    if verify_login_session(login_session_uuid, session_token):
        # get account uuid
        db_conn = database_connection.get_postgres_connection(
            app.config['databasewebsitepraxis_username'],
            app.config['databasewebsitepraxis_password'],
            app.config['databasewebsitepraxis_host'],
            app.config['databasewebsitepraxis_port'],
            "databasewebsitepraxis"
        )
        with db_conn.cursor() as db_cursor:
            sql_query = """SELECT * FROM """ + app.config['databasewebsitepraxis_schema'] + """.account_login_session WHERE 
            login_session_uuid = %s AND user_session_token = %s;"""
            db_cursor.execute(sql_query, 
                          (app.config['databasewebsitepraxis_schema'], 
                           login_session_uuid, 
                           session_token))
            db_conn.commit()
            sql_query_result = db_cursor.fetchone()
            if sql_query_result is not None:
                account_uuid = sql_query_result[0]
                session_start_timestamp = sql_query_result[2]
                new_login_session_data = {
                    "account_uuid" : account_uuid,
                    "login_session_uuid" : login_session_uuid,
                    "session_start_timestamp" : session_start_timestamp,
                    "user_session_token" : session_token,
                    "last_refresh_timestamp" : datetime.strftime(datetime.now(),
                                                        app.config["timestamp_format"])
                }
                return new_login_session_data
            else:
                return None
    else:
        return None



