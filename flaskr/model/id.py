from dataclasses import dataclass
# from marshmallow import ValidationError
# from model.error import BadRequest
# from schema.id import IDSchema

@dataclass
class ID():
    id: str

    # def __post_init__(self):
    #     try:
    #         IDSchema().dump(self)
    #     except Exception as e:
    #         print(e.args)
    #         raise BadRequest(e.args[0])