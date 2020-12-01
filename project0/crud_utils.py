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

def get_one_by_kwargs(
        props: List[str], table_name: str, connection_factory: ConnectionFactory, **kwargs
) -> Optional[Dict[str, Any]]:
    with get_connection(connection_factory) as connection:
        db_cursor = connection.cursor()
        db_cursor.execute(
            f"SELECT {','.join(props)} FROM {table_name} WHERE {' and '.join(f'{k}=%s' for k in kwargs.keys())}", tuple(kwargs.values())
        )

        result = dict(zip(props, db_cursor.fetchone()))

    return result

def upsert_one_by_kwargs(
        props: List[str], table_name: str, connection_factory: ConnectionFactory, **kwargs
) -> None:
    pass
    with get_connection(connection_factory) as connection:
        cur = connection.cursor()
        #TODO find out how to send partial update
        statement = f"INSERT INTO {table_name} {','.join(props)} VALUES (','.join(kwargs.values()))" \
                    f" ON CONFLICT (','.join(kwargs.keys()))) DO UPDATE SET price=%s, quantity=%s" \
                    f" where drug_id=%s and pharmacy_id=%s;"
        print(statement)
        cur.execute(statement)


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


'''
Makes JOIN on any number of pairs of tables and args. 
Contract: first_table, second_table, (first_table.lhs_param, second_table.rhs_param), *args
* args <=> table_name, table.lhs_param, rhs_param as full reference so far 
Фильтр типа готового условия: "where ..."
'''
# todo: тип join тоже может пригодиться как аргумент


def get_joined_relation(
      props: List[str], connection_factory: ConnectionFactory, where: str,
        first_table_name: str, second_table_name: str, lhs_param: str, rhs_param: str, *args
):
    with get_connection(connection_factory) as connection:
        db_cursor = connection.cursor()
        query = f"SELECT {','.join(props)} FROM {first_table_name} a " \
            f"INNER JOIN {second_table_name} b ON a.{lhs_param}=b.{rhs_param} "
        i = 0
        while i < len(args):
            params = args[i:i + 3]
            query += f"INNER JOIN {params[0]} i{i} ON i{i}.{params[1]}={params[2]} "
            i += 3

        if where:
            query += where
        db_cursor.execute(query)
        result = db_cursor.fetchall()

        return result


