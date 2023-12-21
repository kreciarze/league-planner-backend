from typing import Protocol

from rest_framework.authtoken.admin import User


class ResourceWithOwner(Protocol):
    def is_owner(self, user: User) -> bool:
        ...
