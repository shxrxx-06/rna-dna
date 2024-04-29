import mysql

# database connection
connection = mysql.connect(host="10.0.4.161", user="sharaaa06", passwd="@shara#23@", database="sharaaa06$rna ")

cursor = connection.cursor()
# some other statements with the help of cursor
connection.close()