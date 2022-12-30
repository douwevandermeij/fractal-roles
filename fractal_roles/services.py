from abc import ABC
from typing import List

from fractal_roles.exceptions import NotAllowedException
from fractal_roles.models import Methods, Role, TokenPayloadRolesMixin


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
            if self._check_role(payload, endpoint, method, role):
                return payload
        raise NotAllowedException("No permission!")

    def _check_role(
        self, payload: TokenPayloadRolesMixin, endpoint: str, method: str, role: Role
    ):
        if role.__class__.__name__.lower() in payload.roles:
            if self._check_endpoint(payload, endpoint, method, role):
                return payload

    def _check_endpoint(
        self, payload: TokenPayloadRolesMixin, endpoint: str, method: str, role: Role
    ):
        if methods := getattr(role, endpoint, None):
            if self._check_method(payload, method, methods):
                return payload

    def _check_method(
        self, payload: TokenPayloadRolesMixin, method: str, methods: Methods
    ):
        if getattr(methods, method, None):
            if m := getattr(methods, method, None):
                payload.specification_func = m.specification_func
            return payload
