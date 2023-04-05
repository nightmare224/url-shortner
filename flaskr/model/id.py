from dataclasses import dataclass
from dataclass_type_validator import dataclass_type_validator
from model.error import BadRequest

@dataclass
class ID():
    id: str

    def __post_init__(self):
        try:
            dataclass_type_validator(self)
        except Exception as e:
            raise BadRequest(e.errors)