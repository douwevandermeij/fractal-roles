from abc import ABC
from typing import List

from fractal_roles.exceptions import NotAllowedException
from fractal_roles.models import Role, TokenPayloadRolesMixin


class Service(
    ABC
):  # TODO copied from fractal-toolkit until services are extracted to separate package
    @classmethod
    def install(cls, *args, **kwargs):
        yield cls()

    def is_healthy(self) -> bool:
        return True


class BaseRolesService(Service):
    roles: List[Role] = []

    def verify(
        self, payload: TokenPayloadRolesMixin, endpoint: str, method: str
    ) -> TokenPayloadRolesMixin:
        for role in self.roles:
            if role.__class__.__name__.lower() in payload.roles:
                if e := getattr(role, endpoint, None):
                    if getattr(e, method, None):
                        if m := getattr(e, method, None):
                            payload.specification_func = m.specification_func
                        return payload
        raise NotAllowedException("No permission!")
