# encoding: UTF-8

import argparse
import abc

import cherrypy

# Драйвер PostgreSQL
# Находится в модуле psycopg2-binary, который можно установить командой
# pip install psycopg2-binary или её аналогом.
import psycopg2 as pg_driver
import psycopg2.pool
from contextlib import contextmanager

# Драйвер SQLite3
# Находится в модуле sqlite3, который можно установить командой
# pip install sqlite3 или её аналогом.
import sqlite3 as sqlite_driver
from playhouse.db_url import connect


# Разбирает аргументы командной строки.
# Выплевывает структуру с полями, соответствующими каждому аргументу.
def parse_cmd_line():
    parser = argparse.ArgumentParser(
        description='Эта программа вычисляет 2+2 при помощи реляционной СУБД')
    parser.add_argument('--pg-host', help='PostgreSQL host name',
                        default='localhost')
    parser.add_argument('--pg-port', help='PostgreSQL port',
                        default=5432)
    parser.add_argument('--pg-user', help='PostgreSQL user',
                        default='')
    parser.add_argument('--pg-password', help='PostgreSQL password',
                        default='')
    parser.add_argument('--pg-database', help='PostgreSQL database',
                        default='')
    parser.add_argument('--sqlite-file',
                        help='SQLite3 database file. Type :memory: to use in-memory SQLite3 database',
                        default='sqlite.db')
    return parser.parse_args()


class ConnectionFactory(abc.ABC):
    @contextmanager
    def get_connection(self):
        conn = self.__get_conn()
        try:
            yield conn
        finally:
            ConnectionFactory.__put_conn(conn)

    def __get_conn(self):
        return connect(self._get_db_url())

    @staticmethod
    def __put_conn(conn):
        conn.close()

    @abc.abstractmethod
    def _get_db_url(self):
        pass


class PGConnectionFactory(ConnectionFactory):
    def __init__(self, args):
        self.__db_url = f"postgres+pool://{args.pg_user}:{args.pg_password}@{args.pg_host}:{args.pg_port}/{args.pg_database}"

    def _get_db_url(self):
        return self.__db_url


class SQLiteConnectionFactory(ConnectionFactory):
    def __init__(self, args):
        self.__db_url = f"sqlite+pool:///{args.sqlite_file}"

    def _get_db_url(self):
        return self.__db_url


def create_connection_factory(args):
    if args.pg_database is None or args.pg_database == '':
        cherrypy.log("DB Use SQLite")
        return SQLiteConnectionFactory(args)
    else:
        cherrypy.log("DB Use PostgreSQL")
        return PGConnectionFactory(args)
