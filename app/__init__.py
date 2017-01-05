from flask import Flask, request, send_from_directory, render_template, redirect, url_for, Blueprint
import mysql.connector
from mysql.connector import errorcode
from staff import staff
from customer import customer
from evil import evil
import helpers

app = Flask(__name__, static_url_path='')
app.register_blueprint(staff)
app.register_blueprint(customer)
app.register_blueprint(evil)

@app.route("/")
def main():
	customers=helpers.getData("select distinct idCustomer, FirstName, LastName from Customer", [], False)
	return render_template('index.html', customers=customers)

if __name__ == "__main__":
	app.run(host="0.0.0.0", debug=True)