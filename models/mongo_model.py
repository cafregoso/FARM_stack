from bson import ObjectId
from bson.errors import InvalidId
from pydantic import BaseModel, BaseConfig


class OID(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        try:
            return ObjectId(str(v))
        except InvalidId as e:
            raise ValueError("Not a valid ObjectId") from e


class MongoModel(BaseModel):
    class Config(BaseConfig):
        json_encoders = {
            ObjectId: lambda oid: str(oid),
        }
