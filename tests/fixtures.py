from dataclasses import dataclass

import pytest
from fractal_specifications.generic.operators import EqualsSpecification
from fractal_specifications.generic.specification import Specification

from fractal_roles.models import Method, Methods, Role, TokenPayloadRolesMixin
from fractal_roles.services import BaseRolesService


@dataclass
class Task:
    id: int
    account_id: int
    created_by: int
    name: str


@pytest.fixture
def dataset():
    return [
        Task(1, 1, 1, "A"),
        Task(2, 1, 2, "B"),
        Task(3, 2, 3, "C"),
    ]


@dataclass
class TokenPayloadRoles(TokenPayloadRolesMixin):
    account_id: int = 0
    user_id: int = 0


@pytest.fixture
def payload():
    return TokenPayloadRoles(roles=["user"], account_id=1, user_id=1)


@pytest.fixture
def account_user_roles_service():
    class AccountMethods(Methods):
        def __init__(self, method: Method = None, **kwargs):
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

    def only_me(payload: TokenPayloadRoles) -> Specification:
        return AccountRole.filter_account(payload) & EqualsSpecification(
            "created_by", payload.user_id
        )

    get_only_me = Methods(get=Method(only_me), post=None, put=None, delete=None)

    class User(AccountRole):
        demo = get_only_me

    class RolesService(BaseRolesService):
        def __init__(self):
            self.roles = [Admin(), User()]

    return RolesService()


@pytest.fixture
def account_roles_service():
    class AccountMethods(Methods):
        def __init__(self, method: Method = None, **kwargs):
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

    return RolesService()


@pytest.fixture
def basic_roles_service():
    class User(Role):
        ...

    class RolesService(BaseRolesService):
        def __init__(self):
            self.roles = [User()]

    return RolesService()
