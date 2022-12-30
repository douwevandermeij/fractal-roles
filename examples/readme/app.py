from dataclasses import dataclass

from readme.roles import RolesService, TokenPayloadRoles


@dataclass
class Task:
    id: int
    account_id: str
    created_by: str
    name: str


if __name__ == "__main__":
    roles_service = RolesService()

    data = [
        Task(1, "67890", "12345", "A"),
        Task(2, "67890", "11111", "B"),
        Task(3, "00000", "12345", "C"),
    ]

    payload = TokenPayloadRoles(roles=["user"], account="67890", sub="12345")
    payload = roles_service.verify(payload, "get_data", "get")
    print(
        list(map(lambda i: i.name, filter(payload.specification.is_satisfied_by, data)))
    )

    payload = TokenPayloadRoles(roles=["admin", "user"], account="67890", sub="12345")
    payload = roles_service.verify(payload, "get_data", "get")
    print(
        list(map(lambda i: i.name, filter(payload.specification.is_satisfied_by, data)))
    )
