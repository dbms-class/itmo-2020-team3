#!/usr/bin/env python3
# encoding: UTF-8

## Веб сервер
import cherrypy

from connect import parse_cmd_line, create_connection_factory
from model import Pharmacy, PharmacyGood, Drug, RetailStatus
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

    @cherrypy.expose
    def update_retail(self,
                      drug_id,
                      pharmacy_id,
                      remainder,
                      price):
        PharmacyGood.update(self.connection_factory, int(drug_id), int(pharmacy_id), int(remainder), float(price))

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def drugs(self):
        return [drug.to_json() for drug in Drug.get(self.connection_factory)]

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def pharmacies(self):
        return [pharm.to_json() for pharm in Pharmacy.get(self.connection_factory)]

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def status_retail(self, drug_id=None, min_remainder=None, max_price=None):
        return [rs.to_json() for rs in RetailStatus.get(self.connection_factory, drug_id, min_remainder, max_price)]


cherrypy.config.update({
    'server.socket_host': '0.0.0.0',
    'server.socket_port': 8081,
})
cherrypy.quickstart(App(parse_cmd_line()))
