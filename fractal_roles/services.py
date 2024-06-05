from typing import Generic, List, TypeVar

from fractal_roles.exceptions import ForbiddenException
from fractal_roles.models import Methods, Role, TokenPayloadRolesMixin

TokenPayloadRolesClass = TypeVar("TokenPayloadRolesClass", bound=TokenPayloadRolesMixin)


class RolesService(Generic[TokenPayloadRolesClass]):
    roles: List[Role] = []

    def verify(
        self, payload: TokenPayloadRolesClass, endpoint: str, method: str
    ) -> TokenPayloadRolesClass:
        for role in self.roles:
            if self._check_role(payload, endpoint, method, role):
                return payload
        raise ForbiddenException("No permission!")

    def _check_role(
        self, payload: TokenPayloadRolesClass, endpoint: str, method: str, role: Role
    ):
        if payload.roles and role.__class__.__name__.lower() in payload.roles:
            if self._check_endpoint(payload, endpoint, method, role):
                return payload

    def _check_endpoint(
        self, payload: TokenPayloadRolesClass, endpoint: str, method: str, role: Role
    ):
        if methods := getattr(role, endpoint, None):
            if self._check_method(payload, method, methods):
                return payload

    def _check_method(
        self, payload: TokenPayloadRolesClass, method: str, methods: Methods
    ):
        if getattr(methods, method, None):
            if m := getattr(methods, method, None):
                payload.specification_func = m.specification_func
            return payload
