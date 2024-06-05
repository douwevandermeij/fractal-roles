import pytest

from fractal_roles.exceptions import ForbiddenException


def test_basic(dataset, user_payload, basic_roles_service):
    payload = basic_roles_service.verify(user_payload, "demo", "get")
    assert len(list(filter(payload.specification.is_satisfied_by, dataset))) == 3


def test_basic_guest_get(dataset, guest_payload, basic_roles_service):
    payload = basic_roles_service.verify(guest_payload, "demo", "get")
    assert len(list(filter(payload.specification.is_satisfied_by, dataset))) == 3


def test_basic_guest_post(guest_payload, basic_roles_service):
    with pytest.raises(ForbiddenException):
        basic_roles_service.verify(guest_payload, "demo", "post")


def test_account(dataset, user_payload, account_roles_service):
    payload = account_roles_service.verify(user_payload, "demo", "get")
    assert len(list(filter(payload.specification.is_satisfied_by, dataset))) == 2


def test_account_user(dataset, user_payload, account_user_roles_service):
    payload = account_user_roles_service.verify(user_payload, "demo", "get")
    assert len(list(filter(payload.specification.is_satisfied_by, dataset))) == 1


def test_error(user_payload, account_user_roles_service):
    with pytest.raises(ForbiddenException):
        account_user_roles_service.verify(user_payload, "demo", "post")
