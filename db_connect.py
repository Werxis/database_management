import mysql.connector

db_connection = mysql.connector.connect(host="sql11.freesqldatabase.com",
                                        user="sql11392799",
                                        password="fWevMJHwyB",
                                        database="sql11392799")
cursor = db_connection.cursor()
