import mysql.connector
from db_credentials import db

mydb = mysql.connector.connect(
    host=db['host'],
    user=db['user'],
    password=db['password'],
    database='movies'
)

mycursor = mydb.cursor()
sql = "INSERT INTO customers (name, address) VALUES(%s,%s)"
sql2 = "SELECT * FROM customers WHERE address = %s"
sql3 = "DELETE FROM customers WHERE address = %s"

params2 = ["end"]
params3 = ["in the nether"]
params = [
    ("enderman","end"),
    ("blaze","nether"),
    ("steve","overworld")
]

#mycursor.executemany(sql, params)
#mydb.commit()

mycursor.execute(sql3, params3)
mydb.commit()
# commit -> to apply the commands modifying the database

mycursor.execute(sql2, params2)
res = mycursor.fetchall()
# fetchall -> to get the results of a command
for x in res:
    print(x)