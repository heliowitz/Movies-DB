from flask import Flask, request, send_from_directory, render_template, redirect, url_for, Blueprint
import mysql.connector
from mysql.connector import errorcode
import helpers

evil = Blueprint('evil', __name__, template_folder='templates')

@evil.route("/evil")
def evilHome():
	return render_template('evil.html', data=[])

@evil.route("/injection", methods=["POST"])
def injection():	
	search = request.form.getlist('movie')[0]
	query="select * from Movie where Movie.MovieName=\'"+search+"\'"
	data = helpers.getData(query,[],True)
	return render_template('evil.html', data=data)