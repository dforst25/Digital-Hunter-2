import os
import mysql.connector


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

    def run_query(self, query: str, params=None):
        cnx = self.get_connection()
        if not cnx:
            return []

        with cnx.cursor(dictionary=True) as cursor:
            cursor.execute(f"USE {self.database}")
            if params is None:
                cursor.execute(query)
            else:
                cursor.execute(query, params)
            rows = cursor.fetchall()
            return rows
