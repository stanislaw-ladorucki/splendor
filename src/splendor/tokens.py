from collections import defaultdict
from enum import Enum
from typing import MutableMapping, Self

from .exceptions import InvalidTokenPullError


class Token(Enum):
    GOLD = 'gold'
    RUBY = 'ruby'
    EMERALD = 'emerald'
    SAPPHIRE = 'sapphire'
    DIAMOND = 'diamond'
    ONYX = 'onyx'


class Gem(Enum):
    RUBY = 'ruby'
    EMERALD = 'emerald'
    SAPPHIRE = 'sapphire'
    DIAMOND = 'diamond'
    ONYX = 'onyx'


class Tokens(MutableMapping[str, int]):
    TOKEN_TYPES = [
        'gold',
        'ruby',
        'emerald',
        'sapphire',
        'diamond',
        'onyx',
    ]

    def pull(self, tokens: Self) -> Self:
        result = self.__class__()
        for token, value in tokens.items():
            if not value:
                continue

            if self[token] >= value:
                result[token] = value
                self[token] -= value
            else:
                result[token] = self[token]
                self[token] = 0

        return result

    def pull_exact(self, tokens: Self) -> Self:
        if all(a >= b for a, b in zip(self.values(), tokens.values())):
            return self.pull(tokens)
        raise InvalidTokenPullError

    def get_total_count(self):
        return sum(self.values())

    def is_positive(self):
        return all(value >= 0 for value in self.values())

    def __init__(self, **kw):
        self._tokens = defaultdict(lambda: 0, **kw)

    def __getitem__(self, item):
        if item not in self.TOKEN_TYPES:
            raise KeyError()
        return self._tokens.__getitem__(item)

    def __setitem__(self, key, value):
        if key not in self.TOKEN_TYPES:
            raise KeyError
        if not isinstance(value, int):
            raise ValueError
        return self._tokens.__setitem__(key, value)

    def __delitem__(self, key):
        self._tokens[key] = 0

    def __len__(self):
        return len(self.TOKEN_TYPES)

    def __iter__(self):
        yield from self.TOKEN_TYPES

    def __add__(self, other: Self):
        return self.__class__(**{
            token: self[token] + value
            for token, value in other.items()
        })

    def __iadd__(self, other: Self):
        for token, value in other.items():
            self[token] += value
        return self

    def __sub__(self, other: Self):
        return self.__class__(**{
            token: self[token] - value
            for token, value in other.items()
        })

    def __isub__(self, other: Self):
        for token, value in other.items():
            self[token] -= value
        return self

    def __neg__(self):
        self.__class__(**{
            token: -self[token]
            for token, value in self.items()
        })

    def __repr__(self):
        members = ', '.join(f'{token}={value}' for token, value in self.items())
        return f'{self.__class__.__name__}({members})'


class Gems(Tokens):
    TOKEN_TYPES = [
        'ruby',
        'emerald',
        'sapphire',
        'diamond',
        'onyx',
    ]
