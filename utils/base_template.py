from abc import ABC, abstractmethod

from typing import List, Union, Tuple

class _Template(ABC):

    @classmethod
    @abstractmethod
    def get_fields(cls) -> List:
        raise NotImplementedError("Base class method")

    @classmethod
    def get_levels(cls) -> Union[List[str], str]:
        return cls.LEVELS

class Field:

    def __init__(self, name: str, types: Tuple, reqs: List):

        self.name = name
        self.types = types 
        self.reqs = reqs 

    def get_name(self):
        return self.name 

    def get_types(self):
        return self.types 

    def get_reqs(self):
        return self.reqs