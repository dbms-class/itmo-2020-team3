from typing import Dict, Any, List, Optional
from connect import ConnectionFactory, get_connection


def get_one_by_id(
        props: List[str], object_id: int, table_name: str, connection_factory: ConnectionFactory
) -> Optional[Dict[str, Any]]:
    with get_connection(connection_factory) as connection:
        db_cursor = connection.cursor()
        db_cursor.execute(
            f"SELECT {','.join(props)} FROM {table_name} WHERE id=%s", (object_id,)
        )

        result = dict(zip(props, db_cursor.fetchone()))

    return result


def get_all_from_table(
        props: List[str], table_name: str, connection_factory: ConnectionFactory
) -> List[Dict[str, Any]]:
    results = []

    with get_connection(connection_factory) as connection:
        db_cursor = connection.cursor()
        db_cursor.execute(f"SELECT {','.join(props)} FROM {table_name}")

        while True:
            rows = db_cursor.fetchmany(size=100)
            if not rows:
                break

            for row in rows:
                results.append(dict(zip(props, row)))

    return results
