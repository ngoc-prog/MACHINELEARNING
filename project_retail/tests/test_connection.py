import mysql.connector

server="localhost"
port=3306
database="k23e_retail"
username="ngot"
password="Obama@123"

conn = mysql.connector.connect(
                host=server,
                port=port,
                database=database,
                user=username,
                password=password)
print("Connected!!!!!")

