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

    def get_all(self, table):
        return self.run_query(f"SELECT * FROM {table}")

    # query 1
    def get_moving_targets(self):
        query = """
                SELECT entity_id, target_name, priority_level
                FROM targets
                WHERE priority_level BETWEEN 1 AND 2 AND movement_distance_km > 5
                """
        return self.run_query(query)

    # query 2
    def get_signal_count(self):
        query = """
                SELECT signal_type, COUNT(*) AS count
                FROM intel_signals
                GROUP BY signal_type
                ORDER BY count DESC
                """
        return self.run_query(query)

    # query 3
    def get_top_3_unknown_entities(self):
        query = """
                SELECT entity_id, SUM(count) as count
                FROM   (SELECT entity_id, COUNT(*) AS count
                        FROM intel_signals
                        WHERE entity_id not in (SELECT entity_id
                                                FROM targets)
                        GROUP BY entity_id
                        UNION ALL
                        SELECT entity_id, COUNT(*) AS count
                        FROM attacks
                        WHERE entity_id not in (SELECT entity_id
                                                FROM targets)
                        GROUP BY entity_id
                        UNION ALL
                        SELECT entity_id, COUNT(*) AS count
                        FROM damage_assessments
                        WHERE entity_id not in (SELECT entity_id
                                                FROM targets)
                        GROUP BY entity_id) AS t
                GROUP BY entity_id
                ORDER BY count DESC
                LIMIT 3;
                """
        return self.run_query(query)


db = DbConnection()

pprint(db.get_top_3_unknown_entities())
