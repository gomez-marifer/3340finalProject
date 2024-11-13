import mysql.connector

dataBase = mysql.connector.connect(
	host = 'localhost',
	user = 'root',
	passwd = 'Classof24@',
	)

#prepare cursor object (using the connector declare above)
cursorObject = dataBase.cursor() 

#create data base
cursorObject.execute("CREATE DATABASE projectDataFinal")

#Message in console to see if it worked 
print("Hello data base projectDataFinal")