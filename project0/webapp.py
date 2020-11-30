#!/usr/bin/env python3
# encoding: UTF-8

## Веб сервер
import cherrypy

from connect import parse_cmd_line, create_connection_factory
from crud_utils import get_joined_relation
from model import *
from static import index


@cherrypy.expose
class App(object):
    def __init__(self, args):
        self.args = args
        self.connection_factory = create_connection_factory(args)

    @cherrypy.expose
    def start(self):
        return "Hello web app"

    @cherrypy.expose
    def index(self):
        return index()

    # @cherrypy.expose
    # def update_retail(self,
    #                   drug_id: int,
    #                   pharmacy_id: int,
    #                   remainder: int,
    #                   price: float):
    #     '''
    #     Обновляет остаток данного лекарства в данной аптеке,
    #     или вносит его в случае отсутствия.
    #     Все аргументы обязательные. Целочисленный аргумент remainder
    #     означает абсолютный остаток в отпускных упаковках.
    #     Численный аргумент price означает цену данного
    #     лекарства в данной аптеке.
    #     '''
    #     with get_connection(self.connection_factory) as db:
    #         cur = db.cursor()
    #         cur.execute('''
    #                insert into PharmacyGood
    #                (pharmacy_id, drug_id, price, quantity)
    #                values (%s, %s, %s, %s)
    #                on conflict(pharmacy_id, drug_id) do update set price=%s, quantity=%s
    #                where drug_id=%s and pharmacy_id=%s;''' % (
    #             pharmacy_id, drug_id, price, remainder,
    #             price, remainder, drug_id, pharmacy_id
    #         ))

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def drugs(self):
        return [drug.to_json() for drug in Drug.get_all(self.connection_factory)]

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def pharmacies(self):
        return [pharm.to_json() for pharm in Pharmacy.get_all(self.connection_factory)]

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def status_retail(self, drug_id=None, min_remainder=None,
                    max_price=None):
        drug_id_filter = f"drug_id = {drug_id} " if drug_id else ""
        min_remainder_filter = f"min_remainder = {min_remainder} " if min_remainder else ""
        max_price_filter = f"max_price = {max_price} " if max_price else ""
        filtering_predicate = ""
        if drug_id_filter or min_remainder_filter or max_price_filter:
            filtering_predicate = "where " + drug_id_filter + min_remainder_filter + max_price_filter

        props = "drug_id,trade_name,international_name,pharmacy_id,address,quantity,price".split(',')

        constructed_res = get_joined_relation(props, self.connection_factory,
                                              filtering_predicate, "Pharmacy", "PharmacyGood",
                                                  "id", "pharmacy_id",
                                                  "Drug", "id", "drug_id")

        return [RetailStatus(*r).to_json() for r in constructed_res]



cherrypy.config.update({
    'server.socket_host': '0.0.0.0',
    'server.socket_port': 8081,
})
cherrypy.quickstart(App(parse_cmd_line()))
