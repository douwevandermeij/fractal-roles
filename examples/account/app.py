from dataclasses import dataclass
from pprint import pprint

from account.roles import RolesService, TokenPayloadRoles


@dataclass
class Task:
    id: int
    account_id: int
    name: str


if __name__ == "__main__":
    roles_service = RolesService()

    payload = TokenPayloadRoles(roles=["admin"], account_id=1)
    payload = roles_service.verify(payload, "demo", "get")

    data = [
        Task(1, 1, "A"),
        Task(2, 1, "B"),
        Task(3, 2, "C"),
    ]

    pprint(
        list(map(lambda i: i.name, filter(payload.specification.is_satisfied_by, data)))
    )
