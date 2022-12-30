from dataclasses import dataclass

from account_user.roles import RolesService, TokenPayloadRoles


@dataclass
class Task:
    id: int
    account_id: int
    created_by: int
    name: str


if __name__ == "__main__":
    roles_service = RolesService()

    payload = TokenPayloadRoles(roles=["user"], account_id=1, user_id=1)
    payload = roles_service.verify(payload, "demo", "get")

    data = [
        Task(1, 1, 1, "A"),
        Task(2, 1, 2, "B"),
        Task(3, 2, 3, "C"),
    ]

    print(
        list(map(lambda i: i.name, filter(payload.specification.is_satisfied_by, data)))
    )
