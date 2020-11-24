from crud_utils import get_one_by_id, get_all_from_table
from dataclasses import dataclass
from abc import ABC


class ORMBase(ABC):
    @classmethod
    def get_by_id(cls, object_id: int):
        params = get_one_by_id(list(cls.__annotations__.keys()), object_id, cls.__name__)
        if not params:
            return None

        return cls(**params)

    @classmethod
    def get_all(cls):
        objects_params = get_all_from_table(list(cls.__annotations__.keys()), cls.__name__)
        return [cls(**params) for params in objects_params]


@dataclass
class Pharmacy(ORMBase):
    id: int
    name: str
    address: str
    number: int


@dataclass
class Drug(ORMBase):
    id: int
    trade_name: str
    international_name: str
    medical_form: int
    manufacturer_id: int
    main_chemicalcompound_id: int
    cert_number: int
