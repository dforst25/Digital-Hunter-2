import os

import mysql.connector

from pprint import pprint
class DbConnection:
    def __init__(self):
        self.config = {
            'host': os.getenv("MYSQL_HOST", "localhost"),
            'port': int(os.getenv("MYSQL_PORT", "3306")),
            'user': os.getenv("MYSQL_USER", "root"),
            'password': os.getenv("MYSQL_PASSWORD", "root")
        }
        self.database = os.getenv("MYSQL_DB", "digital_hunter")
        self.connection = None

    def get_connection(self):
        self.connection = mysql.connector.connect(**self.config)

        if not self.connection.is_connected:
            raise ConnectionError("Couldn't connect to the database")

        return self.connection

    def get_all(self, table):
        cnx = self.get_connection()
        if not cnx:
            return []

        with cnx.cursor(dictionary=True) as cursor:
            cursor.execute(f"USE {self.database}")
            cursor.execute(f"SELECT * FROM {table}")
            rows = cursor.fetchall()
            return rows


db = DbConnection()

pprint(db.get_all("targets"))
