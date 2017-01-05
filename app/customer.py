from flask import Flask, request, send_from_directory, render_template, redirect, url_for, Blueprint
import mysql.connector
from mysql.connector import errorcode
import helpers

customer = Blueprint('customer', __name__, template_folder='templates')

@customer.route("/customer/<id>")
def customerHome(id):
	return renderCustomer(id, "Success!")

@customer.route("/purchase/<id>", methods=["POST"])
def purchase(id):
	showId = request.form.getlist('id')[0]
	statement = "insert into Attend (Customer_idCustomer, Showing_idShowing) values(%s, %s)"
	data = (id, showId)
	err = helpers.changeDB(statement, data)
	return renderCustomer(id, err)

@customer.route("/search/<id>", methods=["POST"])
def search(id):
	statement = "select distinct idShowing, ShowingDateTime, TheatreRoom_RoomNumber, TicketPrice, MovieName, MovieYear from Showing inner join Movie on Showing.Movie_idMovie=Movie.idMovie inner join Genre on Genre.Movie_idMovie=Movie.idMovie inner join TheatreRoom on TheatreRoom.RoomNumber=Showing.TheatreRoom_RoomNumber"
	clauses=[]
	data=[]
	for item in request.form.items():
		if item[1] != "All" and item[1] != "":
			if item[0]=="genre": 
				clauses.append("Genre.Genre=%s")
			elif item[0]=="from":
				clauses.append("Showing.ShowingDateTime>=%s")
			elif item[0]=="to":
				clauses.append("Showing.ShowingDateTime<=%s")
			elif item[0]=="movie":
				clauses.append("Movie.MovieName=%s")
			data.append(item[1])	
			if item[0]=="seat":
				clauses.append("TheatreRoom.Capacity-(select count(*) from Attend where Attend.Showing_idShowing=Showing.idShowing)>=1")
	strClauses = " and ".join(clauses)
	statement += " where " + strClauses
	customer = helpers.getData("select * from Customer where idCustomer=%s",[id],False)[0]
	genres = [item[0] for item in helpers.getData("select distinct Genre from Genre",[],False)]
	dates = [item[0] for item in helpers.getData("select distinct ShowingDateTime from Showing",[],False)]
	showings = helpers.getData(statement,data,True)
	ratedAttends = helpers.getData("select Showing_idShowing, Rating, ShowingDateTime, TicketPrice, MovieName, MovieYear from Attend inner join Showing on Attend.Showing_idShowing=Showing.idShowing inner join Movie on Showing.Movie_idMovie=Movie.idMovie where Rating IS NOT NULL and Customer_idCustomer=%s",[customer[0]],True)
	unratedAttends = helpers.getData("select Showing_idShowing, ShowingDateTime, TicketPrice, MovieName, MovieYear from Attend inner join Showing on Attend.Showing_idShowing=Showing.idShowing inner join Movie on Showing.Movie_idMovie=Movie.idMovie where Rating IS NULL and Customer_idCustomer=%s",[customer[0]],True)
	return render_template('customerHome.html', customer=customer, showings=showings, genres=genres, dates=dates, ratedAttends=ratedAttends, unratedAttends=unratedAttends, err="Success!")

@customer.route("/rating/<id>", methods=["POST"])
def rating(id):
	rating = request.form.getlist('rating')[0]
	if rating != "None":
		showing = request.form.getlist('id')[0]
		statement = "update Attend set Rating=%s where Customer_idCustomer=%s and Showing_idShowing=%s"
		data = [rating, id, showing]
		err = helpers.changeDB(statement, data)
	return renderCustomer(id, err)

def renderCustomer(id, err):
	customer = helpers.getData("select * from Customer where idCustomer=%s",[id],False)[0]
	genres = [item[0] for item in helpers.getData("select distinct Genre from Genre",[],False)]
	dates = [item[0] for item in helpers.getData("select distinct ShowingDateTime from Showing",[],False)]
	showings = helpers.getData("select idShowing, ShowingDateTime, TheatreRoom_RoomNumber, TicketPrice, MovieName, MovieYear from Showing inner join Movie on Showing.Movie_idMovie=Movie.idMovie",[],True)
	ratedAttends = helpers.getData("select Showing_idShowing, Rating, ShowingDateTime, TicketPrice, MovieName, MovieYear from Attend inner join Showing on Attend.Showing_idShowing=Showing.idShowing inner join Movie on Showing.Movie_idMovie=Movie.idMovie where Rating IS NOT NULL and Customer_idCustomer=%s",[customer[0]],True)
	unratedAttends = helpers.getData("select Showing_idShowing, ShowingDateTime, TicketPrice, MovieName, MovieYear from Attend inner join Showing on Attend.Showing_idShowing=Showing.idShowing inner join Movie on Showing.Movie_idMovie=Movie.idMovie where Rating IS NULL and Customer_idCustomer=%s",[customer[0]],True)
	return render_template('customerHome.html', customer=customer, showings=showings, genres=genres, dates=dates, ratedAttends=ratedAttends, unratedAttends=unratedAttends, err=err)