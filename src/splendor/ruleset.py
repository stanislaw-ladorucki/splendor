from typing import Self

from .cards import DevelopmentCards, TIER_ONE_CARDS, TIER_TWO_CARDS, TIER_THREE_CARDS
from .exceptions import OverPlayerLimit, NotEnoughPlayers


class Ruleset:
    MAX_PLAYER_TOKENS: int
    MAX_PLAYER_RESERVED_CARDS: int
    PLAYER_COUNT: int
    MAX_PLAYERS: int
    MIN_PLAYERS: int
    SHOP_TIER_CARDS_COUNT: int
    SHOP_TIER_COUNT: int
    COMMUNITY_GEMS_COUNT: int
    COMMUNITY_GOLD_COUNT: int
    TIER_ONE_DEVELOPMENT_CARDS_POOL: DevelopmentCards
    TIER_TWO_DEVELOPMENT_CARDS_POOL: DevelopmentCards
    TIER_THREE_DEVELOPMENT_CARDS_POOL: DevelopmentCards


class ClassicRuleset(Ruleset):
    MAX_PLAYER_TOKENS: int = 10
    MAX_PLAYER_RESERVED_CARDS: int = 3
    PLAYER_COUNT: int = 4
    MAX_PLAYERS: int = 4
    MIN_PLAYERS: int = 2
    SHOP_TIER_CARDS_COUNT: int = 4
    SHOP_TIER_COUNT: int = 3
    COMMUNITY_GEMS_COUNT: int = 7
    COMMUNITY_GOLD_COUNT: int = 5
    TIER_ONE_DEVELOPMENT_CARDS_POOL: DevelopmentCards = TIER_ONE_CARDS
    TIER_TWO_DEVELOPMENT_CARDS_POOL: DevelopmentCards = TIER_TWO_CARDS
    TIER_THREE_DEVELOPMENT_CARDS_POOL: DevelopmentCards = TIER_THREE_CARDS

    @classmethod
    def from_players(cls, player_count: int) -> Self:
        if player_count > cls.MAX_PLAYERS:
            raise OverPlayerLimit
        if player_count > cls.MAX_PLAYERS:
            raise NotEnoughPlayers

        ruleset = cls()
        ruleset.PLAYER_COUNT = player_count
        ruleset.COMMUNITY_GEMS_COUNT = (
            4 if player_count < 3 else
            5 if player_count < 4 else
            7
        )

        return ruleset
