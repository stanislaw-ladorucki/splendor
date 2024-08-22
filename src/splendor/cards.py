from random import shuffle
from typing import MutableSequence, TypeVar

from .tokens import Gem, Gems


class DevelopmentCard:
    gem: Gem
    prestige: int
    cost: Gems
    tier: int

    def __init__(self, gem, prestige, cost, tier):
        self.gem = gem
        self.prestige = prestige
        self.cost = cost
        self.tier = tier


T = TypeVar('T')


class AbstractCards(MutableSequence[T]):
    def __init__(self, *cards: T):
        self._cards: list[T] = list(cards)

    def shuffle(self) -> None:
        shuffle(self)

    def insert(self, index, value):
        return self._cards.insert(index, value)

    def __getitem__(self, index):
        return self._cards.__getitem__(index)

    def __setitem__(self, index, value):
        return self._cards.__setitem__(index, value)

    def __delitem__(self, index):
        return self._cards.__delitem__(index)

    def __len__(self):
        return self._cards.__len__()


DevelopmentCards = AbstractCards[DevelopmentCard]

TIER_ONE_CARDS = [
    DevelopmentCard(gem=Gem.ONYX, prestige=0, cost=Gems(diamond=1, sapphire=1, emerald=1, ruby=1, onyx=0), tier=1),
    DevelopmentCard(gem=Gem.ONYX, prestige=0, cost=Gems(diamond=1, sapphire=2, emerald=1, ruby=1, onyx=0), tier=1),
    DevelopmentCard(gem=Gem.ONYX, prestige=0, cost=Gems(diamond=2, sapphire=2, emerald=0, ruby=1, onyx=0), tier=1),
    DevelopmentCard(gem=Gem.ONYX, prestige=0, cost=Gems(diamond=0, sapphire=0, emerald=1, ruby=3, onyx=1), tier=1),
    DevelopmentCard(gem=Gem.ONYX, prestige=0, cost=Gems(diamond=0, sapphire=0, emerald=2, ruby=1, onyx=0), tier=1),
    DevelopmentCard(gem=Gem.ONYX, prestige=0, cost=Gems(diamond=2, sapphire=0, emerald=2, ruby=0, onyx=0), tier=1),
    DevelopmentCard(gem=Gem.ONYX, prestige=0, cost=Gems(diamond=0, sapphire=0, emerald=3, ruby=0, onyx=0), tier=1),
    DevelopmentCard(gem=Gem.ONYX, prestige=1, cost=Gems(diamond=0, sapphire=4, emerald=0, ruby=0, onyx=0), tier=1),
    DevelopmentCard(gem=Gem.SAPPHIRE, prestige=0, cost=Gems(diamond=1, sapphire=0, emerald=1, ruby=1, onyx=1), tier=1),
    DevelopmentCard(gem=Gem.SAPPHIRE, prestige=0, cost=Gems(diamond=1, sapphire=0, emerald=1, ruby=2, onyx=1), tier=1),
    DevelopmentCard(gem=Gem.SAPPHIRE, prestige=0, cost=Gems(diamond=1, sapphire=0, emerald=2, ruby=2, onyx=0), tier=1),
    DevelopmentCard(gem=Gem.SAPPHIRE, prestige=0, cost=Gems(diamond=0, sapphire=1, emerald=3, ruby=1, onyx=0), tier=1),
    DevelopmentCard(gem=Gem.SAPPHIRE, prestige=0, cost=Gems(diamond=1, sapphire=0, emerald=0, ruby=0, onyx=2), tier=1),
    DevelopmentCard(gem=Gem.SAPPHIRE, prestige=0, cost=Gems(diamond=0, sapphire=0, emerald=2, ruby=0, onyx=2), tier=1),
    DevelopmentCard(gem=Gem.SAPPHIRE, prestige=0, cost=Gems(diamond=0, sapphire=0, emerald=0, ruby=0, onyx=3), tier=1),
    DevelopmentCard(gem=Gem.SAPPHIRE, prestige=1, cost=Gems(diamond=0, sapphire=0, emerald=0, ruby=4, onyx=0), tier=1),
    DevelopmentCard(gem=Gem.DIAMOND, prestige=0, cost=Gems(diamond=0, sapphire=1, emerald=1, ruby=1, onyx=1), tier=1),
    DevelopmentCard(gem=Gem.DIAMOND, prestige=0, cost=Gems(diamond=0, sapphire=1, emerald=2, ruby=1, onyx=1), tier=1),
    DevelopmentCard(gem=Gem.DIAMOND, prestige=0, cost=Gems(diamond=0, sapphire=2, emerald=2, ruby=0, onyx=1), tier=1),
    DevelopmentCard(gem=Gem.DIAMOND, prestige=0, cost=Gems(diamond=3, sapphire=1, emerald=0, ruby=0, onyx=1), tier=1),
    DevelopmentCard(gem=Gem.DIAMOND, prestige=0, cost=Gems(diamond=0, sapphire=0, emerald=0, ruby=2, onyx=1), tier=1),
    DevelopmentCard(gem=Gem.DIAMOND, prestige=0, cost=Gems(diamond=0, sapphire=2, emerald=0, ruby=0, onyx=2), tier=1),
    DevelopmentCard(gem=Gem.DIAMOND, prestige=0, cost=Gems(diamond=0, sapphire=3, emerald=0, ruby=0, onyx=0), tier=1),
    DevelopmentCard(gem=Gem.DIAMOND, prestige=1, cost=Gems(diamond=0, sapphire=0, emerald=4, ruby=0, onyx=0), tier=1),
    DevelopmentCard(gem=Gem.EMERALD, prestige=0, cost=Gems(diamond=1, sapphire=1, emerald=0, ruby=1, onyx=1), tier=1),
    DevelopmentCard(gem=Gem.EMERALD, prestige=0, cost=Gems(diamond=1, sapphire=1, emerald=0, ruby=1, onyx=2), tier=1),
    DevelopmentCard(gem=Gem.EMERALD, prestige=0, cost=Gems(diamond=0, sapphire=1, emerald=0, ruby=2, onyx=2), tier=1),
    DevelopmentCard(gem=Gem.EMERALD, prestige=0, cost=Gems(diamond=1, sapphire=3, emerald=1, ruby=0, onyx=0), tier=1),
    DevelopmentCard(gem=Gem.EMERALD, prestige=0, cost=Gems(diamond=2, sapphire=1, emerald=0, ruby=0, onyx=0), tier=1),
    DevelopmentCard(gem=Gem.EMERALD, prestige=0, cost=Gems(diamond=0, sapphire=2, emerald=0, ruby=2, onyx=0), tier=1),
    DevelopmentCard(gem=Gem.EMERALD, prestige=0, cost=Gems(diamond=0, sapphire=0, emerald=0, ruby=3, onyx=0), tier=1),
    DevelopmentCard(gem=Gem.EMERALD, prestige=1, cost=Gems(diamond=0, sapphire=0, emerald=0, ruby=0, onyx=4), tier=1),
    DevelopmentCard(gem=Gem.RUBY, prestige=0, cost=Gems(diamond=1, sapphire=1, emerald=1, ruby=0, onyx=1), tier=1),
    DevelopmentCard(gem=Gem.RUBY, prestige=0, cost=Gems(diamond=2, sapphire=1, emerald=1, ruby=0, onyx=1), tier=1),
    DevelopmentCard(gem=Gem.RUBY, prestige=0, cost=Gems(diamond=2, sapphire=0, emerald=1, ruby=0, onyx=2), tier=1),
    DevelopmentCard(gem=Gem.RUBY, prestige=0, cost=Gems(diamond=1, sapphire=0, emerald=0, ruby=1, onyx=3), tier=1),
    DevelopmentCard(gem=Gem.RUBY, prestige=0, cost=Gems(diamond=0, sapphire=2, emerald=1, ruby=0, onyx=0), tier=1),
    DevelopmentCard(gem=Gem.RUBY, prestige=0, cost=Gems(diamond=2, sapphire=0, emerald=0, ruby=2, onyx=0), tier=1),
    DevelopmentCard(gem=Gem.RUBY, prestige=0, cost=Gems(diamond=3, sapphire=0, emerald=0, ruby=0, onyx=0), tier=1),
    DevelopmentCard(gem=Gem.RUBY, prestige=1, cost=Gems(diamond=4, sapphire=0, emerald=0, ruby=0, onyx=0), tier=1),
]

TIER_TWO_CARDS = [
    DevelopmentCard(gem=Gem.ONYX, prestige=1, cost=Gems(diamond=3, sapphire=2, emerald=2, ruby=0, onyx=0), tier=2),
    DevelopmentCard(gem=Gem.ONYX, prestige=1, cost=Gems(diamond=3, sapphire=0, emerald=3, ruby=0, onyx=2), tier=2),
    DevelopmentCard(gem=Gem.ONYX, prestige=2, cost=Gems(diamond=0, sapphire=1, emerald=4, ruby=2, onyx=0), tier=2),
    DevelopmentCard(gem=Gem.ONYX, prestige=2, cost=Gems(diamond=0, sapphire=0, emerald=5, ruby=3, onyx=0), tier=2),
    DevelopmentCard(gem=Gem.ONYX, prestige=2, cost=Gems(diamond=5, sapphire=0, emerald=0, ruby=0, onyx=0), tier=2),
    DevelopmentCard(gem=Gem.ONYX, prestige=3, cost=Gems(diamond=0, sapphire=0, emerald=0, ruby=0, onyx=6), tier=2),
    DevelopmentCard(gem=Gem.SAPPHIRE, prestige=1, cost=Gems(diamond=0, sapphire=2, emerald=2, ruby=3, onyx=0), tier=2),
    DevelopmentCard(gem=Gem.SAPPHIRE, prestige=1, cost=Gems(diamond=0, sapphire=2, emerald=3, ruby=0, onyx=3), tier=2),
    DevelopmentCard(gem=Gem.SAPPHIRE, prestige=2, cost=Gems(diamond=5, sapphire=3, emerald=0, ruby=0, onyx=0), tier=2),
    DevelopmentCard(gem=Gem.SAPPHIRE, prestige=2, cost=Gems(diamond=2, sapphire=0, emerald=0, ruby=1, onyx=4), tier=2),
    DevelopmentCard(gem=Gem.SAPPHIRE, prestige=2, cost=Gems(diamond=0, sapphire=5, emerald=0, ruby=0, onyx=0), tier=2),
    DevelopmentCard(gem=Gem.SAPPHIRE, prestige=3, cost=Gems(diamond=0, sapphire=6, emerald=0, ruby=0, onyx=0), tier=2),
    DevelopmentCard(gem=Gem.DIAMOND, prestige=1, cost=Gems(diamond=0, sapphire=0, emerald=3, ruby=2, onyx=2), tier=2),
    DevelopmentCard(gem=Gem.DIAMOND, prestige=1, cost=Gems(diamond=2, sapphire=3, emerald=0, ruby=3, onyx=0), tier=2),
    DevelopmentCard(gem=Gem.DIAMOND, prestige=2, cost=Gems(diamond=0, sapphire=0, emerald=1, ruby=4, onyx=2), tier=2),
    DevelopmentCard(gem=Gem.DIAMOND, prestige=2, cost=Gems(diamond=0, sapphire=0, emerald=0, ruby=5, onyx=3), tier=2),
    DevelopmentCard(gem=Gem.DIAMOND, prestige=2, cost=Gems(diamond=0, sapphire=0, emerald=0, ruby=5, onyx=0), tier=2),
    DevelopmentCard(gem=Gem.DIAMOND, prestige=3, cost=Gems(diamond=6, sapphire=0, emerald=0, ruby=0, onyx=0), tier=2),
    DevelopmentCard(gem=Gem.EMERALD, prestige=1, cost=Gems(diamond=3, sapphire=0, emerald=2, ruby=3, onyx=0), tier=2),
    DevelopmentCard(gem=Gem.EMERALD, prestige=1, cost=Gems(diamond=2, sapphire=3, emerald=0, ruby=0, onyx=2), tier=2),
    DevelopmentCard(gem=Gem.EMERALD, prestige=2, cost=Gems(diamond=4, sapphire=2, emerald=0, ruby=0, onyx=1), tier=2),
    DevelopmentCard(gem=Gem.EMERALD, prestige=2, cost=Gems(diamond=0, sapphire=5, emerald=3, ruby=0, onyx=0), tier=2),
    DevelopmentCard(gem=Gem.EMERALD, prestige=2, cost=Gems(diamond=0, sapphire=0, emerald=5, ruby=0, onyx=0), tier=2),
    DevelopmentCard(gem=Gem.EMERALD, prestige=3, cost=Gems(diamond=0, sapphire=0, emerald=6, ruby=0, onyx=0), tier=2),
    DevelopmentCard(gem=Gem.RUBY, prestige=1, cost=Gems(diamond=2, sapphire=0, emerald=0, ruby=2, onyx=3), tier=2),
    DevelopmentCard(gem=Gem.RUBY, prestige=1, cost=Gems(diamond=0, sapphire=3, emerald=0, ruby=2, onyx=3), tier=2),
    DevelopmentCard(gem=Gem.RUBY, prestige=2, cost=Gems(diamond=1, sapphire=4, emerald=2, ruby=0, onyx=0), tier=2),
    DevelopmentCard(gem=Gem.RUBY, prestige=2, cost=Gems(diamond=3, sapphire=0, emerald=0, ruby=0, onyx=5), tier=2),
    DevelopmentCard(gem=Gem.RUBY, prestige=2, cost=Gems(diamond=0, sapphire=0, emerald=0, ruby=0, onyx=5), tier=2),
    DevelopmentCard(gem=Gem.RUBY, prestige=3, cost=Gems(diamond=0, sapphire=0, emerald=0, ruby=6, onyx=0), tier=2),
]

TIER_THREE_CARDS = [
    DevelopmentCard(gem=Gem.ONYX, prestige=3, cost=Gems(diamond=3, sapphire=3, emerald=5, ruby=3, onyx=0), tier=3),
    DevelopmentCard(gem=Gem.ONYX, prestige=4, cost=Gems(diamond=0, sapphire=0, emerald=0, ruby=7, onyx=0), tier=3),
    DevelopmentCard(gem=Gem.ONYX, prestige=4, cost=Gems(diamond=0, sapphire=0, emerald=3, ruby=6, onyx=3), tier=3),
    DevelopmentCard(gem=Gem.ONYX, prestige=5, cost=Gems(diamond=0, sapphire=0, emerald=0, ruby=7, onyx=3), tier=3),
    DevelopmentCard(gem=Gem.SAPPHIRE, prestige=3, cost=Gems(diamond=3, sapphire=0, emerald=3, ruby=3, onyx=5), tier=3),
    DevelopmentCard(gem=Gem.SAPPHIRE, prestige=4, cost=Gems(diamond=7, sapphire=0, emerald=0, ruby=0, onyx=0), tier=3),
    DevelopmentCard(gem=Gem.SAPPHIRE, prestige=4, cost=Gems(diamond=6, sapphire=3, emerald=0, ruby=0, onyx=3), tier=3),
    DevelopmentCard(gem=Gem.SAPPHIRE, prestige=5, cost=Gems(diamond=7, sapphire=3, emerald=0, ruby=0, onyx=0), tier=3),
    DevelopmentCard(gem=Gem.DIAMOND, prestige=3, cost=Gems(diamond=0, sapphire=3, emerald=3, ruby=5, onyx=3), tier=3),
    DevelopmentCard(gem=Gem.DIAMOND, prestige=4, cost=Gems(diamond=0, sapphire=0, emerald=0, ruby=0, onyx=7), tier=3),
    DevelopmentCard(gem=Gem.DIAMOND, prestige=4, cost=Gems(diamond=3, sapphire=0, emerald=0, ruby=3, onyx=6), tier=3),
    DevelopmentCard(gem=Gem.DIAMOND, prestige=5, cost=Gems(diamond=3, sapphire=0, emerald=0, ruby=0, onyx=7), tier=3),
    DevelopmentCard(gem=Gem.EMERALD, prestige=3, cost=Gems(diamond=5, sapphire=3, emerald=0, ruby=3, onyx=3), tier=3),
    DevelopmentCard(gem=Gem.EMERALD, prestige=4, cost=Gems(diamond=0, sapphire=7, emerald=0, ruby=0, onyx=0), tier=3),
    DevelopmentCard(gem=Gem.EMERALD, prestige=4, cost=Gems(diamond=3, sapphire=6, emerald=3, ruby=0, onyx=0), tier=3),
    DevelopmentCard(gem=Gem.EMERALD, prestige=5, cost=Gems(diamond=0, sapphire=7, emerald=3, ruby=0, onyx=0), tier=3),
    DevelopmentCard(gem=Gem.RUBY, prestige=3, cost=Gems(diamond=3, sapphire=5, emerald=3, ruby=0, onyx=3), tier=3),
    DevelopmentCard(gem=Gem.RUBY, prestige=4, cost=Gems(diamond=0, sapphire=0, emerald=7, ruby=0, onyx=0), tier=3),
    DevelopmentCard(gem=Gem.RUBY, prestige=4, cost=Gems(diamond=0, sapphire=3, emerald=6, ruby=3, onyx=0), tier=3),
    DevelopmentCard(gem=Gem.RUBY, prestige=5, cost=Gems(diamond=0, sapphire=0, emerald=7, ruby=3, onyx=0), tier=3),
]
