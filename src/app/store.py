from pydantic import BaseModel
from typing import TypeVar, Generic

T = TypeVar("T", bound=BaseModel)


class Store(BaseModel, Generic[T]):
    data: T
