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
    def __init__(self, pharmacy_id: int, quantity: int, price: int):
        self.pharmacy_id = pharmacy_id
        self.quantity = quantity
        self.price = price

    @classmethod
    def update_retail(cls, connection_factory: ConnectionFactory,
                      drug_id: int, pharmacy_id: int, remainder: int, price: float):
        with connection_factory.get_connection() as connection:
            pharmacy_good_table: pw.Table = cls.bind_to_database(connection)

            if pharmacy_good_table.select().where(
                    pharmacy_good_table.c.drug_id == drug_id,
                    pharmacy_good_table.c.pharmacy_id == pharmacy_id,
            ).count() > 0:
                q = pharmacy_good_table.update(
                    quantity=remainder,
                    price=price
                ).where(
                    pharmacy_good_table.c.drug_id == drug_id,
                    pharmacy_good_table.c.pharmacy_id == pharmacy_id,
                )
            else:
                q = pharmacy_good_table.insert(
                    pharmacy_id=pharmacy_id,
                    drug_id=drug_id,
                    price=price,
                    quantity=remainder
                )

            q.execute()

    @classmethod
    def drug_move(cls, connection_factory: ConnectionFactory,
                  drug_id: int, min_remainder: int,
                  target_income_increase: float):
        with connection_factory.get_connection() as connection:
            pharmacy_good_table: pw.Table = cls.bind_to_database(
                connection)

            drug_moves = []

            while target_income_increase > 0:
                min_price_select = pharmacy_good_table.select(
                    pw.fn.MIN(pharmacy_good_table.c.price).alias('min_price')
                ).where(
                    pharmacy_good_table.c.drug_id == drug_id,
                    pharmacy_good_table.c.quantity > min_remainder
                )
                min_price = [f for f in min_price_select][0]['min_price']
                max_price_select = pharmacy_good_table.select(
                    pw.fn.MAX(pharmacy_good_table.c.price).alias('max_price')
                ).where(
                    pharmacy_good_table.c.drug_id == drug_id,
                    pharmacy_good_table.c.quantity < min_remainder
                )
                max_price = [f for f in max_price_select][0]['max_price']
                if min_price is None or max_price is None or min_price >= max_price:
                    break

                # TODO is transaction started?
                from_pharmacy_select = pharmacy_good_table.select(
                    pharmacy_good_table.c.pharmacy_id,
                    pharmacy_good_table.c.quantity,
                    pharmacy_good_table.c.price
                ).where(
                    pharmacy_good_table.c.drug_id == drug_id,
                    pharmacy_good_table.c.price == min_price
                )
                from_pharmacy = [f for f in from_pharmacy_select.objects(cls)]
                from_pharmacy = from_pharmacy[0]
                to_pharmacy_select = pharmacy_good_table.select(
                    pharmacy_good_table.c.pharmacy_id,
                    pharmacy_good_table.c.quantity,
                    pharmacy_good_table.c.price
                ).where(
                    pharmacy_good_table.c.drug_id == drug_id,
                    pharmacy_good_table.c.price == max_price
                )
                to_pharmacy = [f for f in to_pharmacy_select.objects(cls)][0]
                amount_diff = from_pharmacy.quantity - min_remainder
                price_diff = to_pharmacy.price * amount_diff - from_pharmacy.price * amount_diff
                target_income_increase -= price_diff

                q1 = pharmacy_good_table.update(
                    quantity=min_remainder,
                ).where(
                    pharmacy_good_table.c.drug_id == drug_id,
                    pharmacy_good_table.c.pharmacy_id == from_pharmacy.pharmacy_id,
                )
                q2 = pharmacy_good_table.update(
                    quantity=to_pharmacy.quantity + amount_diff,
                ).where(
                    pharmacy_good_table.c.drug_id == drug_id,
                    pharmacy_good_table.c.pharmacy_id == from_pharmacy.pharmacy_id,
                )
                q1.execute()
                q2.execute()
                drug_moves.append({
                    "from_pharmacy_id": from_pharmacy.pharmacy_id,
                    "to_pharmacy_id": to_pharmacy.pharmacy_id,
                    "price_difference": price_diff,
                    "count": amount_diff
                })
            return drug_moves

    @classmethod
    def bind_to_database(cls, connection):
        return pw.Table('pharmacygood').bind(connection)


class RetailStatus(ORMBase):
    def __init__(self, drug_id: int, drug_trade_name: str, drug_inn: str, pharmacy_id: int,
                 pharmacy_address: str,
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
    def get(cls, connection_factory: ConnectionFactory, drug_id: int = None,
            min_remainder: int = None,
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
                min_max_query = min_max_query.where(
                    pharmacy_good_table.c.quantity >= int(min_remainder))

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
