from dataclasses import dataclass
from pprint import pprint

from basic.roles import RolesService, TokenPayloadRoles


@dataclass
class Task:
    id: int
    name: str


if __name__ == "__main__":
    roles_service = RolesService()

    payload = TokenPayloadRoles(roles=["user"])
    payload = roles_service.verify(payload, "demo", "get")

    data = [
        Task(1, "A"),
        Task(2, "B"),
        Task(3, "C"),
    ]

    pprint(
        list(map(lambda i: i.name, filter(payload.specification.is_satisfied_by, data)))
    )
