# Fractal Roles

> Fractal Roles provides a flexible way to define fine-grained roles & permissions for users of your Python applications.

[![PyPI Version][pypi-image]][pypi-url]
[![Build Status][build-image]][build-url]
[![Code Coverage][coverage-image]][coverage-url]
[![Code Quality][quality-image]][quality-url]

<!-- Badges -->

[pypi-image]: https://img.shields.io/pypi/v/fractal-roles
[pypi-url]: https://pypi.org/project/fractal-roles/
[build-image]: https://github.com/douwevandermeij/fractal-roles/actions/workflows/build.yml/badge.svg
[build-url]: https://github.com/douwevandermeij/fractal-roles/actions/workflows/build.yml
[coverage-image]: https://codecov.io/gh/douwevandermeij/fractal-roles/branch/main/graph/badge.svg?token=Jv2ShlaVf8
[coverage-url]: https://codecov.io/gh/douwevandermeij/fractal-roles
[quality-image]: https://api.codeclimate.com/v1/badges/754713b64573aa47571d/maintainability
[quality-url]: https://codeclimate.com/github/douwevandermeij/fractal-roles

## Installation

```sh
pip install fractal-roles
```

## Development

Setup the development environment by running:

```sh
make deps
```

Happy coding.

Occasionally you can run:

```sh
make lint
```

This is not explicitly necessary because the git hook does the same thing.

**Do not disable the git hooks upon commit!**


## Usage

To be able to use Fractal Roles you first need to define which roles are available in your application.\
Let's say you have an **Admin** user and a regular **User**. You can then create the following roles in your application:

```python
from fractal_roles.models import Role


class Admin(Role):
    ...


class User(Role):
    ...
```

For now, we skip permissions, we'll get back to it later.

Next you can create a RolesService to install the roles.

```python
from fractal_roles.services import BaseRolesService


class RolesService(BaseRolesService):
    def __init__(self):
        self.roles = [Admin(), User()]
```

Last but not least we need to define a dataclass for the user's (authentication token) payload:

```python
from dataclasses import dataclass

from fractal_roles.models import TokenPayloadRolesMixin


@dataclass
class TokenPayloadRoles(TokenPayloadRolesMixin):
    sub: str = ""  # JWT's standard claim for the subject of the token (for example, the user id)
    account: str = ""  # a custom claim, in this case, to point to the account where the user belongs to
```

**The application in which this RolesService will be used, needs to provide the payload everytime a user tries to access a so-called endpoint.**\
When building an API application, the request should contain a header with the authentication token, which usually is in the form of JWT,
and should contain the user's assigned role(s).

### Verifying a user's payload

Example payload:

```json
{
  "roles": ["user"],
  "sub": "12345",
  "account": "67890"
}
```

The json above should be loaded into a TokenPayloadRoles object. From now on, when we refer to `payload` we mean such an object.

When a user tries to access an endpoint, before it actually executes, the application should **verify** the `payload`.
Suppose the user tries to **get** the endpoint **get_data**, then the verification can be done as follows:

```python
roles_service = RolesService()
payload = roles_service.verify(payload, "get_data", "get")  # Note that it returns a payload as well
```

If the code didn't raise a `NotAllowedException`, then the `payload` is now enriched with a [specification](https://github.com/douwevandermeij/fractal-specifications).
You can use that specification to filter the data that can be accessed by **get_data** to return back to the user.

For example:

```python
data = [...]
return list(filter(payload.specification.is_satisfied_by, data))
```

When using a real database and, for example, Django to manage it, you can convert the specification into a Django ORM query easily.
To do so please check out the [specification documentation](https://github.com/douwevandermeij/fractal-specifications).

A quick example:
```python
from fractal_specifications.contrib.django.specifications import DjangoOrmSpecificationBuilder


q = DjangoOrmSpecificationBuilder.build(payload.specification)
return Data.objects.filter(q)
```

We will now dive deeper into permissions, but the way to verify a user's payload stays the same.

### Fine-grained permissions

In the example above we defined the roles **Admin** and **User** and we didn't set any permissions.
By default, any method (get, post, put, delete) on any endpoint will get an empty specification which is always
evaluates to `True` so no data will be filtered.

To change this, we need to define more specific permissions. Let's say both **Admin** and **User** roles may only **get**
their own data, by `account_id`, and on top of that the **User** may only **get** its own created data by `created_by`.
We will also only limit this to the **get_data** function, which in our case is the only external available endpoint.

```python
from fractal_roles.models import Method, Methods, Role
from fractal_specifications.generic.operators import EqualsSpecification
from fractal_specifications.generic.specification import Specification


def my_account(payload: TokenPayloadRoles) -> Specification:
    return EqualsSpecification(
        "account_id", payload.account
    )


def my_data(payload: TokenPayloadRoles) -> Specification:
    return my_account(payload) & EqualsSpecification(
        "created_by", payload.sub
    )


class Admin(Role):
    get_data = Methods(get=Method(my_account), post=None, put=None, delete=None)


class User(Role):
    get_data = Methods(get=Method(my_data), post=None, put=None, delete=None)
```

To see this code in action, please check out the examples directory in this repository.

### Multiple roles

A user payload may also include multiple roles, for example:

```json
{
  "roles": ["user", "admin"],
  "sub": "12345",
  "account": "67890"
}
```

The first matched Role, from the perspective of the RolesService, will be used for verification.

In our case, this will be **Admin**:

```python
class RolesService(BaseRolesService):
    def __init__(self):
        self.roles = [Admin(), User()]  # Admin Role will first be checked against the payload
```
