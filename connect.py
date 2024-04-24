import pymysql

# database connection
connection = pymysql.connect(host="localhost:3306", user="geneprot_shara", passwd="@Shara#23@", database="geneprot_rnadna")

cursor = connection.cursor()
# some other statements with the help of cursor
connection.close()