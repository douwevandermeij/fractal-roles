from dataclasses import dataclass
from typing import Optional

from fractal_specifications.generic.operators import EqualsSpecification  # type: ignore
from fractal_specifications.generic.specification import Specification  # type: ignore

from fractal_roles.models import Method, Methods, Role, TokenPayloadRolesMixin
from fractal_roles.services import RolesService as BaseRolesService


@dataclass
class TokenPayloadRoles(TokenPayloadRolesMixin):
    account_id: int = 0


class AccountMethods(Methods):
    def __init__(self, method: Optional[Method] = None, **kwargs):
        if not method:
            method = Method(lambda payload: AccountRole.filter_account(payload))
        super().__init__(method, **kwargs)


class AccountRole(Role):
    def __getattr__(self, item):
        return AccountMethods()

    @staticmethod
    def filter_account(payload: TokenPayloadRoles) -> Specification:
        return EqualsSpecification("account_id", payload.account_id)


class Admin(AccountRole):
    ...


class User(AccountRole):
    ...


class RolesService(BaseRolesService):
    def __init__(self):
        self.roles = [Admin(), User()]
