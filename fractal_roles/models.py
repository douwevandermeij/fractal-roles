from dataclasses import dataclass
from typing import Callable, Optional, Protocol, Union

from fractal_specifications.generic.specification import (
    EmptySpecification,
    Specification,
)


class Role:
    def __getattr__(self, item):
        return Methods()


class RestrictiveRole:
    pass


@dataclass
class Method:
    specification_func: Union[Callable, None] = lambda payload: EmptySpecification()


@dataclass
class Methods:
    get: Optional[Method]
    post: Optional[Method]
    put: Optional[Method]
    delete: Optional[Method]

    def __init__(self, method: Optional[Method] = Method(), **kwargs):
        self.get = kwargs.get("get", method)
        self.post = kwargs.get("post", method)
        self.put = kwargs.get("put", method)
        self.delete = kwargs.get("delete", method)


@dataclass
class TokenPayloadRolesMixin(Protocol):
    roles: Optional[list] = None
    specification_func: Callable = lambda **kwargs: None

    @property
    def specification(self) -> Specification:
        if self.specification_func is not None:
            return self.specification_func(self)
        return EmptySpecification()
