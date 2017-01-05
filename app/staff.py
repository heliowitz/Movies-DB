from flask import Flask, request, send_from_directory, render_template, redirect, url_for, Blueprint
import mysql.connector
from mysql.connector import errorcode
import helpers

staff = Blueprint('staff', __name__, template_folder='templates')

@staff.route("/staffHome")
def staffHome():
	return render_template('staffHome.html', attributes=getTableAttributes(None), err="Success!")

@staff.route("/staffHome/<table>")
def staffTable(table):
	return templateGenerator(table, "Success!")

@staff.route("/<method>/<tableName>", methods=["POST"])
def add(method, tableName):
	if method=="update":
		statement, data = constructUpdRequest(tableName, request.form.items())
	else:
		statement, data = constructAddDelRequest(tableName, method, request.form.items())
	err = helpers.changeDB(statement, data)
	return templateGenerator(tableName, err)

@staff.route("/view/<table>", methods=["POST"])
def changeView(table):
	view = ["Customer_idCustomer", "Showing_idShowing", "Rating"]
	for item in request.form.items():
		if item[0]=="customer":
			view.append("FirstName")
			view.append("LastName")
		if item[0]=="showing":
			view.append("ShowingDateTime")
		if item[0]=="movie":
			view.append("MovieName")
		if item[0]=="default":
			view = ["Customer_idCustomer", "Showing_idShowing", "Rating"]
	strView = ",".join(view)
	strQuery = "select " + strView + " from Attend inner join Showing on  Attend.Showing_idShowing = Showing.idShowing inner join Movie on Showing.Movie_idMovie=Movie.idMovie inner join Customer on Customer.idCustomer=Attend.Customer_idCustomer order by Rating"
	return render_template('sideBarAttend.html', table=table, data=helpers.getData(strQuery,[],True), err="Success!")	

def getTableAttributes(tableName):
	cnx = mysql.connector.connect(user='root', database='MovieTheatre')
	cursor = cnx.cursor()
	
	# Get all tables in MovieTheatre
	queryTables = ("show tables")
	cursor.execute(queryTables)
	tables = []
	for i in cursor:
		tables.append(i[0])

	# Get all attributes
	attributes = []
	for table in tables:
		queryAttributes = ("describe " + table)
		cursor.execute(queryAttributes)
		tableAttributes = []
		for j in cursor:
			tableAttributes.append(j[0])
		attributes.append([table,tableAttributes])

	cursor.close()
	cnx.close()
	if tableName is None:
		return attributes
	else:
		return attributes[tables.index(tableName)]

def constructAddDelRequest(table, method, form):
	formAttributes, formValues, parameters, conditions = ([] for i in range(4))
	for item in form:
		if item[1] is not "":
			if table=="Genre" and item[0]=="MovieName":
				conditions.append("(select idMovie from Movie where Movie.MovieName=%s)")
				parameters.append("(select idMovie from Movie where Movie.MovieName=%s)")
				formAttributes.append("Movie_idMovie")
			else:
				conditions.append(item[0] + "=" + "%s")
				parameters.append("%s")
				formAttributes.append(item[0])
			formValues.append(item[1])

	strAttributes = ",".join(formAttributes)
	strParameters = ",".join(parameters)
	strConditions = " AND ".join(conditions)

	if method=="insert":
		statement = "insert into " + table + " (" + str(strAttributes) + ") values(" + str(strParameters) + ") "
		data = (formValues)
	elif method=="delete":
		statement = "delete from " + table + " where " + str(strConditions)
		data = (formValues)
	return statement, data

def constructUpdRequest(tableName, form):
	formSetAttributes, formWhereAttributes, parameters, setConditions, whereConditions, formSetValues, formWhereValues = ([] for i in range(7))
	for item in form:
		if item[0].startswith("s") and item[1] is not "":
			setConditions.append(item[0][1:] + "=" + "%s")
			formSetValues.append(item[1])
		elif item[0].startswith("w") and item[1] is not "":
			whereConditions.append(item[0][1:] + "=" + "%s")
			formWhereValues.append(item[1])

	strSetConditions = ",".join(setConditions)
	strWhereConditions = ",".join(whereConditions)
	strValues = ",".join(formSetValues+formWhereValues)

	statement = "update " + tableName + " set " + str(strSetConditions) + " where " + str(strWhereConditions)
	data = formSetValues+formWhereValues
	return statement, data

def templateGenerator(table, err):
	if table=="Genre":
		return render_template('sideBarGenre.html', table=table, data=helpers.getData(queryGenerator(table),[],True), err=err)
	elif table=="Attend":
		return render_template('sideBarAttend.html', table=table, data=helpers.getData(queryGenerator(table),[],True), err=err)
	else:
		return render_template('sideBar.html', table=table, data=helpers.getData(queryGenerator(table),[],True), err=err)	

def queryGenerator(table):
	if table=="Genre":
		query = "select Genre.Genre, MovieName from Genre INNER JOIN Movie ON Genre.Movie_idMovie=Movie.idMovie ORDER BY Genre"
	elif table=="Movie":
		query = "select * from Movie order by MovieName"
	elif table=="Attend":
		query = "select * from Attend order by Rating"
	elif table=="Customer":
		query = "select * from Customer order by LastName"
	elif table=="TheatreRoom":
		query = "select * from TheatreRoom"
	elif table=="Showing":
		query = "select * from Showing order by ShowingDateTime"
	return query	

if __name__ == "__main__":
	app.run(host="0.0.0.0", debug=True)