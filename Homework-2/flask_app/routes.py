# Author: Prof. MM Ghassemi <ghassem3@msu.edu>
from flask import current_app as app
from flask import render_template, redirect, request
from .utils.database.database  import database
from werkzeug.datastructures import ImmutableMultiDict
from pprint import pprint
import json
import random
db = database()

@app.route('/')
def root():
	return redirect('/home')

@app.route('/home')
def home():
	x     = random.choice(['I love to read books.','My favorite season is summer.','My favorite animal is a cow'])
	return render_template('home.html', fun_fact = x)

@app.route('/resume')
def resume():
	resume_data = db.getResumeData()
	# pprint(resume_data)
	return render_template('resume.html', resume_data = resume_data)

@app.route('/projects')
def projects():
	return render_template('projects.html')

@app.route('/processfeedback', methods = ['POST'])
def processfeedback():
	feedback = request.form
	name = feedback.get("name")
	email = feedback.get("email")
	comment = feedback.get("comment") 
	db.insertRows(table="feedback", columns=["name", "email", "comment"], parameters=[[name, email, comment]])
	feedback_data = db.getFeedbackRows()
	return render_template('processfeedback.html', feedback_data=feedback_data)



