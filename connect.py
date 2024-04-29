import mysql

# database connection
connection = mysql.connect(host="localhost", user="root", passwd="@Shara#23@", database="rna")

cursor = connection.cursor()
# some other statements with the help of cursor
connection.close()