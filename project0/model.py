import json
from abc import ABC
from dataclasses import dataclass

from connect import ConnectionFactory
from crud_utils import get_one_by_id, get_all_from_table, get_one_by_kwargs


class ORMBase(ABC):
    @classmethod
    def get_by_id(cls, connection_factory: ConnectionFactory, object_id: int):
        params = get_one_by_id(list(cls.__annotations__.keys()), object_id, cls.__name__, connection_factory)
        if not params:
            return None

        return cls(**params)

    @classmethod
    def get_by_kwargs(cls, connection_factory: ConnectionFactory, **kwargs):
        params = get_one_by_kwargs(list(cls.__annotations__.keys()), cls.__name__, connection_factory, **kwargs)
        if not params:
            return None

        return cls(**params)

    @classmethod
    def get_all(cls, connection_factory: ConnectionFactory):
        objects_params = get_all_from_table(list(cls.__annotations__.keys()), cls.__name__, connection_factory)
        return [cls(**params) for params in objects_params]
    # need to rename overlapping names in RetailStatus to do so
    # @classmethod
    # def get_joined(cls, connection_factory, filtering_predicate, first_table_name: str, second_table_name: str,
    #                lhs_param: str, rhs_param: str, *join_args):
    #
    #     constructed_res = get_joined_dependencies(list(cls.__annotations__.keys()), connection_factory,
    #                                               filtering_predicate, first_table_name, second_table_name,
    #                                               lhs_param, rhs_param, join_args)
    #
    #     return [cls(*constructed_res) for r in constructed_res]


    # simple approach with no decoder/encoder classes
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, ensure_ascii=False)


@dataclass
class Pharmacy(ORMBase):
    id: int
    name: str
    address: str
    number: int


@dataclass
class PharmacyGood(ORMBase):
    pharmacy_id: int
    drug_id: int
    price: int
    quantity: int


@dataclass
class Drug(ORMBase):
    id: int
    trade_name: str
    international_name: str
    medical_form: int
    manufacturer_id: int
    main_chemicalcompound_id: int
    cert_number: int


@dataclass
class RetailStatus(ORMBase):
    drug_id: int
    drug_trade_name: str
    drug_inn: str
    pharmacy_id: int
    pharmacy_address: str
    quantity: int
    price: int
    # min_price: int # todo
    # max_price: int