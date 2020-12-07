import json

import peewee as pw

from abc import ABC

from connect import ConnectionFactory


class ORMBase(ABC):
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, ensure_ascii=False)

    @classmethod
    def bind_to_database(cls, connection):
        raise NotImplemented


class Pharmacy(ORMBase):
    def __init__(self, id: int, name: str = None, address: str = None, number: int = None):
        self.id = id
        self.name = name
        self.address = address
        self.number = number

    @classmethod
    def get(cls, connection_factory: ConnectionFactory, pharmacy_id: int = None):
        with connection_factory.get_connection() as connection:
            pharmacy_table = cls.bind_to_database(connection)

            q = pharmacy_table.select(
                pharmacy_table.c.id,
                pharmacy_table.c.name,
                pharmacy_table.c.address,
                pharmacy_table.c.number,
            )

            if pharmacy_id is not None:
                q = q.where(pharmacy_table.c.id == pharmacy_id)

            obj = [f for f in q.objects(cls)]

        return obj

    @classmethod
    def bind_to_database(cls, connection):
        return pw.Table('pharmacy').bind(connection)


class Drug(ORMBase):
    def __init__(self, id: int, trade_name: str = None, international_name: str = None):
        self.id = id
        self.trade_name = trade_name
        self.international_name = international_name

    @classmethod
    def get(cls, connection_factory: ConnectionFactory, drug_id: int = None):
        with connection_factory.get_connection() as connection:
            drugs_table = cls.bind_to_database(connection)

            q = drugs_table.select(
                drugs_table.c.id,
                drugs_table.c.trade_name,
                drugs_table.c.international_name,
            )

            if drug_id is not None:
                q = q.where(drugs_table.c.id == drug_id)

            obj = [f for f in q.objects(cls)]

        return obj

    @classmethod
    def bind_to_database(cls, connection):
        return pw.Table('drug').bind(connection)


class PharmacyGood(ORMBase):
    @classmethod
    def update(cls, connection_factory: ConnectionFactory,
               drug_id: int, pharmacy_id: int, remainder: int, price: float):
        with connection_factory.get_connection() as connection:
            pharmacy_good_table = cls.bind_to_database(connection)

            q = pharmacy_good_table.update(
                quantity = int(remainder),
                price = float(price)
            ).where(
                pharmacy_good_table.c.drug_id == drug_id,
                pharmacy_good_table.c.pharmacy_id == pharmacy_id,
            )

            q.execute()

    @classmethod
    def bind_to_database(cls, connection):
        return pw.Table('pharmacygood').bind(connection)


class RetailStatus(ORMBase):
    def __init__(self, drug_id: int, drug_trade_name: str, drug_inn: str, pharmacy_id: int, pharmacy_address: str,
                 remainder: int, price: float, min_price: float, max_price: float):
        self.drug_id = drug_id
        self.drug_trade_name = drug_trade_name
        self.drug_inn = drug_inn
        self.pharmacy_id = pharmacy_id
        self.pharmacy_address = pharmacy_address
        self.remainder = remainder
        self.price = price
        self.min_price = min_price
        self.max_price = max_price

    @classmethod
    def get(cls, connection_factory: ConnectionFactory, drug_id: int = None, min_remainder: int = None,
            max_price: int = None):
        with connection_factory.get_connection() as connection:
            pharmacy_good_table = PharmacyGood.bind_to_database(connection)
            drugs_table = Drug.bind_to_database(connection)
            pharmacy_table = Pharmacy.bind_to_database(connection)

            min_max_query = pharmacy_good_table.select(
                pw.fn.MIN(pharmacy_good_table.c.price).alias('min_price'),
                pw.fn.MAX(pharmacy_good_table.c.price).alias('max_price')
            )

            q = pharmacy_good_table.select(
                drugs_table.c.id.alias('drug_id'),
                drugs_table.c.trade_name.alias('drug_trade_name'),
                drugs_table.c.international_name.alias('drug_inn'),

                pharmacy_table.c.id.alias('pharmacy_id'),
                pharmacy_table.c.address.alias('pharmacy_address'),

                pharmacy_good_table.c.quantity.alias('remainder'),
                pharmacy_good_table.c.price,

                min_max_query.c.min_price,
                min_max_query.c.max_price
            ).join(
                drugs_table, on=(drugs_table.c.id == pharmacy_good_table.c.drug_id)
            ).join(
                pharmacy_table, on=(pharmacy_table.c.id == pharmacy_good_table.c.pharmacy_id)
            )

            if drug_id is not None:
                q = q.where(pharmacy_good_table.c.drug_id == int(drug_id))
                min_max_query = min_max_query.where(pharmacy_good_table.c.drug_id == int(drug_id))

            if min_remainder is not None:
                q = q.where(pharmacy_good_table.c.quantity >= int(min_remainder))
                min_max_query = min_max_query.where(pharmacy_good_table.c.quantity >= int(min_remainder))

            if max_price is not None:
                q = q.where(pharmacy_good_table.c.price <= float(max_price))
                min_max_query = min_max_query.where(pharmacy_good_table.c.price <= float(max_price))

            q = q.join(
                min_max_query, join_type=pw.JOIN.CROSS
            )

            obj = [f for f in q.objects(cls)]

        return obj

    @classmethod
    def bind_to_database(cls, connection):
        pass
