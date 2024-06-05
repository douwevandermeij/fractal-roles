from dataclasses import dataclass

from fractal_specifications.generic.operators import EqualsSpecification
from fractal_specifications.generic.specification import Specification

from fractal_roles.models import Method, Methods, Role, TokenPayloadRolesMixin
from fractal_roles.services import RolesService as BaseRolesService


@dataclass
class TokenPayloadRoles(TokenPayloadRolesMixin):
    account: str = ""
    sub: str = ""


def my_account(payload: TokenPayloadRoles) -> Specification:
    return EqualsSpecification("account_id", payload.account)


def my_data(payload: TokenPayloadRoles) -> Specification:
    return my_account(payload) & EqualsSpecification("created_by", payload.sub)


class Admin(Role):
    get_data = Methods(None, get=Method(my_account))


class User(Role):
    get_data = Methods(None, get=Method(my_data))


class RolesService(BaseRolesService):
    def __init__(self):
        self.roles = [Admin(), User()]
