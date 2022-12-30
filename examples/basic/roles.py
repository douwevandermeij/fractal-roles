from dataclasses import dataclass

from fractal_roles.models import Role, TokenPayloadRolesMixin
from fractal_roles.services import BaseRolesService


@dataclass
class TokenPayloadRoles(TokenPayloadRolesMixin):
    ...


class User(Role):
    ...


class RolesService(BaseRolesService):
    def __init__(self):
        self.roles = [User()]
