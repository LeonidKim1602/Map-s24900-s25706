from collections.abc import MutableMapping
from typing import Iterable
from uuid import uuid4


class CookieStorage(MutableMapping):
    def __init__(self):
        self._cookies: dict[str, int] = {}
        self._users: dict[int, str] = {}

    def __getitem__(self, key: str) -> int:
        return self._cookies[key]

    def __setitem__(self, key: str, value: int) -> None:
        if value in self._users:
            del self._cookies[self._users[value]]

        self._cookies[key] = value
        self._users[value] = key

        print(key, ": ", value)

    def __delitem__(self, key: str) -> None:
        del self._users[self._cookies[key]]
        del self._cookies[key]

    def __iter__(self) -> Iterable[str]:
        return iter(self._cookies)

    def __len__(self) -> int:
        return len(self._cookies)

    def clear(self) -> None:
        self._cookies.clear()
        self._users.clear()


def get_storage_functions():
    storage = CookieStorage()

    def issue_token(user: int) -> str:
        token = str(uuid4())
        storage[token] = user
        return token

    def authenticate_user(token: str) -> int | None:
        if token in storage:
            return storage[token]
        return None

    return issue_token, authenticate_user


issue_token, authenticate_user = get_storage_functions()
