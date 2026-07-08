from typing import Type, TypeVar

from models.base import Base
from models.user import User

MODEL = TypeVar("MODEL", bound=Base)

TypeModel = Type[MODEL]
