from server import app
from . import response
from flask import redirect
from model import course_data

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
    print(recommended_course)
    return response.ok("")



