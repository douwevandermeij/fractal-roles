from dataclasses import dataclass
from typing import Optional

from fractal_specifications.generic.operators import EqualsSpecification
from fractal_specifications.generic.specification import Specification

from fractal_roles.models import Method, Role, TokenPayloadRolesMixin
from fractal_roles.services import RolesService as BaseRolesService


@dataclass
class TokenPayloadRoles(TokenPayloadRolesMixin):
    account: str = ""
    sub: str = ""


def my_account(payload: TokenPayloadRoles) -> Specification:
    return EqualsSpecification("account_id", payload.account)


def my_data(payload: TokenPayloadRoles) -> Specification:
    return my_account(payload) & EqualsSpecification("created_by", payload.sub)


@dataclass
class Action:
    execute: Optional[Method] = None


class Student(Role):
    def __getattr__(self, item):
        return Action()

    order_pizza = Action(execute=Method(my_data))
    pay_for_pizza = Action(execute=Method(my_data))


class RolesService(BaseRolesService[TokenPayloadRoles]):
    def __init__(self):
        self.roles = [Student()]

    def verify(
        self, payload: TokenPayloadRoles, endpoint: str, method: str = "execute"
    ) -> TokenPayloadRoles:
        return super().verify(payload, endpoint, method)
