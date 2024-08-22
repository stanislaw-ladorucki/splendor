from typing import Optional, Self

from .cards import DevelopmentCard, DevelopmentCards
from .nobles import Noble
from .ruleset import Ruleset


class ShopTier:
    tier_numer: int = 1
    restock_pile: DevelopmentCards
    available_cards: list[Optional[DevelopmentCard]]

    def __init__(self, ruleset: Ruleset, tier_numer=1, restock_pile=None, available_cards=None):
        self.tier_numer = tier_numer
        self.restock_pile = restock_pile or DevelopmentCards()
        self.available_cards = available_cards or []

        self.available_cards += [  # ensure the correct amount of cards is available for sale
            self.restock_pile.pop()
            for _ in range(ruleset.SHOP_TIER_CARDS_COUNT - len(self.available_cards))
        ]

    def pick_and_replace(self, index: int) -> Optional[DevelopmentCard]:
        # TODO: may raise index error
        card = self.available_cards[index]
        self.available_cards[index] = (
            self.restock_pile and
            self.restock_pile.pop() or
            None
        )

        return card


class Shop:
    nobles: list[Noble]
    tiers: list[ShopTier]

    def get_tier(self, tier):
        return self.tiers[tier + 1]

    @classmethod
    def from_pools(cls, ruleset: Ruleset, card_pools: list[DevelopmentCards], nobles: list[Noble]) -> Self:
        for pool in card_pools:
            pool.shuffle()

        return cls(
            ruleset,
            tiers=[
                ShopTier(ruleset, tier_numer=i, restock_pile=pool)
                for i, pool in enumerate(card_pools, start=1)
            ],
            nobles=nobles,
        )

    def __init__(self, ruleset: Ruleset, nobles=None, tiers=None):
        self.nobles = nobles or []
        self.tiers = tiers or []

    @classmethod
    def get_initial_shop_state(cls, ruleset: Ruleset) -> Self:
        return cls.from_pools(ruleset, [
            DevelopmentCards(*ruleset.TIER_ONE_DEVELOPMENT_CARDS_POOL),
            DevelopmentCards(*ruleset.TIER_TWO_DEVELOPMENT_CARDS_POOL),
            DevelopmentCards(*ruleset.TIER_THREE_DEVELOPMENT_CARDS_POOL),
        ], [])
