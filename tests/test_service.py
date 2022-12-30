import pytest

from fractal_roles.exceptions import NotAllowedException


def test_basic(dataset, payload, basic_roles_service):
    payload = basic_roles_service.verify(payload, "demo", "get")
    assert len(list(filter(payload.specification.is_satisfied_by, dataset))) == 3


def test_account(dataset, payload, account_roles_service):
    payload = account_roles_service.verify(payload, "demo", "get")
    assert len(list(filter(payload.specification.is_satisfied_by, dataset))) == 2


def test_account_user(dataset, payload, account_user_roles_service):
    payload = account_user_roles_service.verify(payload, "demo", "get")
    assert len(list(filter(payload.specification.is_satisfied_by, dataset))) == 1


def test_error(payload, account_user_roles_service):
    with pytest.raises(NotAllowedException):
        account_user_roles_service.verify(payload, "demo", "post")


def test_fractal_service(basic_roles_service):
    assert next(basic_roles_service.__class__.install())
    assert basic_roles_service.is_healthy()
