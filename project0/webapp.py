#!/usr/bin/env python3
# encoding: UTF-8

## Веб сервер
import cherrypy

from connect import parse_cmd_line
from connect import create_connection
from static import index

@cherrypy.expose
class App(object):
    def __init__(self, args):
        self.args = args

    @cherrypy.expose
    def start(self):
        return "Hello web app"

    @cherrypy.expose
    def index(self):
      return index()

    @cherrypy.expose
    def update_retail(self,
                      drug_id: int,
                      pharmacy_id: int,
                      remainder: int,
                      price: float):
        '''
            Обновляет остаток данного лекар-
        ства в данной аптеке, или вносит
        его в случае отсутствия. Все аргу-
        менты обязательные. Целочислен-
        ный аргумент remainder означа-
        ет абсолютный остаток в отпуск-
        ных упаковках. Численный аргу-
        мент price означает цену данного
        лекарства в данной аптеке.
        '''
        drug_id = int(drug_id)
        pharmacy_id = int(pharmacy_id)
        remainder = int(remainder)
        price = float(price)
        with create_connection(self.args) as db:
            cur = db.cursor()
            # TODO find out why this does not wrok
            cur.execute('''
                if EXISTS (select from PharmacyGood where drug_id=%s and pharmacy_id=%s) then
                    update PharmacyGood
                    set price=%s, quantity=%s
                    where drug_id=%s and pharmacy_id=%s;
                else
                    insert into PharmacyGood (drug_id, pharmacy_id, quantity, price)
                    values (%s, %s, %s, %s);
                end if
                ''', (
                drug_id, pharmacy_id,
                drug_id, pharmacy_id, remainder, price,
                price, remainder, drug_id, pharmacy_id
            ))

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def drugs(self):
        with create_connection(self.args) as db:
            cur = db.cursor()
            cur.execute("SELECT id, trade_name, international_name FROM Drug")
            drugs = cur.fetchall()
            result = [
                {"id": id_, "name": name, "inn": inn} for id_, name, inn in drugs
            ]
            return result


    @cherrypy.expose
    @cherrypy.tools.json_out()
    def planets(self, planet_id = None):
        with create_connection(self.args) as db:
            cur = db.cursor()
            if planet_id is None:
              cur.execute("SELECT id, name FROM Planet P")
            else:
              cur.execute("SELECT id, name FROM Planet WHERE id= %s", planet_id)
            result = []
            planets = cur.fetchall()
            for p in planets:
                result.append({"id": p[0], "name": p[1]})
            return result

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def commanders(self):
        with create_connection(self.args) as db:
            cur = db.cursor()
            cur.execute("SELECT id, name FROM Commander")
            result = []
            commanders = cur.fetchall()
            for c in commanders:
                result.append({"id": c[0], "name": c[1]})
            return result


cherrypy.config.update({
  'server.socket_host': '0.0.0.0',
  'server.socket_port': 8080,
})
cherrypy.quickstart(App(parse_cmd_line()))

