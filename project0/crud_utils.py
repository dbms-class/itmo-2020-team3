from typing import Dict, Any, List, Optional
from connect import create_connection_pg
from dataclasses import dataclass
from abc import ABC


def get_one_by_id(props: List[str], object_id: int, table_name: str) -> Optional[Dict[str, Any]]:
    connection = create_connection_pg({}) # FIXME: pass facture
    try:
        db_cursor = connection.cursor()
        db_cursor.execute(
            f"SELECT {','.join(props)} FROM {table_name} WHERE id=%s", (object_id,)
        )

        result = dict(zip(props, db_cursor.fetchone()))
    finally:
        connection.close()

    return result


def get_all_from_table(props: List[str], table_name: str) -> List[Dict[str, Any]]:
    connection = create_connection_pg({})  # FIXME: pass facture

    results = []

    try:
        db_cursor = connection.cursor()
        db_cursor.execute(f"SELECT {','.join(props)} FROM {table_name}")

        while True:
            rows = db_cursor.fetchmany(size=100)
            if not rows:
                break

            for row in rows:
                results.append(dict(zip(props, row)))
    finally:
        connection.close()

    return results
