from db import DbConnection


class DataInteract:
    def __init__(self, connector: DbConnection):
        self.connector = connector

    # query 1
    def get_moving_targets(self):
        query = """
                SELECT entity_id, target_name, priority_level
                FROM targets
                WHERE priority_level BETWEEN 1 AND 2 AND movement_distance_km > 5
                """
        return self.connector.run_query(query)

    # query 2
    def get_signal_count(self):
        query = """
                SELECT signal_type, COUNT(*) AS count
                FROM intel_signals
                GROUP BY signal_type
                ORDER BY count DESC
                """
        return self.connector.run_query(query)

    # query 3
    def get_top_3_unknown_entities(self):
        query = """
                SELECT entity_id, COUNT(*) AS count
                FROM intel_signals
                WHERE priority_level = 99
                GROUP BY entity_id
                ORDER BY count DESC
                LIMIT 3;
                """
        return self.connector.run_query(query)

    # query 4
    def get_extreme_entities(self):
        query = """
                SELECT DISTINCT entity_id
                FROM intel_signals 
                WHERE TIME(`timestamp`) BETWEEN '08:00:00' AND '20:00:00'
                GROUP BY entity_id, DATE(`timestamp`)
                HAVING SUM(distance_from_last) = 0
                AND entity_id IN (
                    SELECT entity_id
                    FROM intel_signals
                    WHERE TIME(`timestamp`) <= '08:00:00' OR TIME(`timestamp`) <= '08:00:00'
                    GROUP BY entity_id
                    HAVING SUM(distance_from_last) >= 10
                )
                """
        return self.connector.run_query(query)

    def get_cords_order_by_date(self, entity_id):
        query = f"""
                SELECT reported_lat, reported_lon
                FROM intel_signals
                WHERE entity_id = "{entity_id}"
                ORDER BY timestamp
                """
        return self.connector.run_query(query)
