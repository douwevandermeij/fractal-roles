from dataclasses import dataclass
from typing import Callable, Optional

from fractal_specifications.generic.specification import (
    EmptySpecification,
    Specification,
)


class Role:
    def __getattr__(self, item):
        return Methods()


@dataclass
class Method:
    specification_func: Callable = lambda payload: EmptySpecification()


class Methods:
    get: Optional[Method]
    post: Optional[Method]
    put: Optional[Method]
    delete: Optional[Method]

    def __init__(self, method: Method = None, **kwargs):
        if not method:
            method = Method()
        self.get = kwargs.get("get", method)
        self.post = kwargs.get("post", method)
        self.put = kwargs.get("put", method)
        self.delete = kwargs.get("delete", method)


@dataclass
class TokenPayloadRolesMixin:
    roles: Optional[list]
    specification_func: Callable = lambda **kwargs: None

    @property
    def specification(self) -> Optional[Specification]:
        if self.specification_func:
            return self.specification_func(self)
