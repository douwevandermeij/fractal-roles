from dataclasses import dataclass

from readme.roles import RolesService, TokenPayloadRoles


@dataclass
class Wallet:
    id: int
    account_id: str
    created_by: str
    total_amount_cents: int


if __name__ == "__main__":
    roles_service = RolesService()

    data = [
        Wallet(1, "67890", "12345", 100),
        Wallet(2, "67890", "11111", 1000),
        Wallet(3, "00000", "12345", 10000),
    ]

    payload = TokenPayloadRoles(roles=["student"], account="67890", sub="12345")
    payload = roles_service.verify(payload, "order_pizza")
    print(
        list(
            map(
                lambda i: i.total_amount_cents,
                filter(payload.specification.is_satisfied_by, data),
            )
        )
    )

    payload = roles_service.verify(payload, "pay_for_pizza")
    print(
        list(
            map(
                lambda i: i.total_amount_cents,
                filter(payload.specification.is_satisfied_by, data),
            )
        )
    )
