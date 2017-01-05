import mysql.connector
from mysql.connector import errorcode

def getData(query, data, withColumns):
	cnx = mysql.connector.connect(user='root', database='MovieTheatre')
	cursor = cnx.cursor()
	result = []
	if len(data) == 0:
		cursor.execute(query)
	else:
		cursor.execute(query, data)
	if withColumns:
		attributes = []
		for i in cursor.description:
			attributes.append(i[0])
		result.append(attributes)		
	records=[]
	for i in cursor:
		tuple = []
		for j in i:
			tuple.append(j)
		records.append(tuple)
	cursor.close()
	cnx.close()
	if withColumns:
		result.append(records)
		return result
	else:
		return records

def changeDB(statement, data):
	if len(data)==0:
		input("Empty Query")
		return "Empty Query"
	cnx = mysql.connector.connect(user='root', database='MovieTheatre')
	cursor = cnx.cursor()
	try:
		cursor.execute(statement, data)
		cnx.commit()
	except mysql.connector.Error as err:
		return err.msg
	cnx.close()
	return "Success!"