#!/usr/bin/env python3
# encoding: UTF-8

## Веб сервер
import cherrypy

from connect import parse_cmd_line, connection_factory
from static import index
from model import *


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
        Обновляет остаток данного лекарства в данной аптеке,
        или вносит его в случае отсутствия.
        Все аргументы обязательные. Целочисленный аргумент remainder
        означает абсолютный остаток в отпускных упаковках.
        Численный аргумент price означает цену данного
        лекарства в данной аптеке.
        '''
        drug_id = int(drug_id)
        pharmacy_id = int(pharmacy_id)
        remainder = int(remainder)
        price = float(price)
        db = connection_factory.getconn(self.args)
        try:
            cur = db.cursor()
            # replace with upsert if sqlite supports it
            cur.execute('''
                   insert into PharmacyGood 
                   (pharmacy_id, drug_id, price, quantity)
                   values (%s, %s, %s, %s)
                   on conflict do update set price=%s, quantity=%s
                   where drug_id=%s and pharmacy_id=%s;''' % (
                pharmacy_id, drug_id, price, remainder,
                price, remainder, drug_id, pharmacy_id
            ))
        finally:
            connection_factory.putconn(db)

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def drugs(self):
        db = connection_factory.getconn(self.args)
        try:
            cur = db.cursor()
            cur.execute(
                "SELECT id, trade_name, international_name FROM Drug")
            drugs = cur.fetchall()
            result = [
                {"id": id_, "name": name, "inn": inn} for
                id_, name, inn in drugs
            ]
            return result

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def pharmacies(self):
        # todo: utf-8 is ignored
        cherrypy.response.headers['Content-Type'] = 'charset=utf-8' # no effect
        db = connection_factory.getconn(self.args)
        try:
            cur = db.cursor()
            cur.execute("SELECT id, name, address, number FROM Pharmacy")
            pharms = cur.fetchall()
            result = [
                Pharmacy(id_, name, address, number).to_json()
                        for id_, name, address, number in pharms
            ]
            return result
        finally:
            connection_factory.putconn(db)

cherrypy.config.update({
  'server.socket_host': '0.0.0.0',
  'server.socket_port': 8081,
})
cherrypy.quickstart(App(parse_cmd_line()))