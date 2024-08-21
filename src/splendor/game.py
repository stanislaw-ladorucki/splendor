from dataclasses import dataclass
from enum import Enum
from typing import Self, Optional

from .exceptions import (
    OverPlayerTokenLimit, IllegalTokenSelection,
    IllegalCardReservation,
)
from .cards import DevelopmentCard, DevelopmentCards
from .ruleset import Ruleset
from .tokens import Tokens, Gems


class PlayerAction(Enum):
    SELECT_TOKENS = 'select_tokens'
    RESERVE_CARD = 'reserve_card'
    BUY_CARD = 'buy_card'


class Player:
    reserved_cards: DevelopmentCards
    development_cards: DevelopmentCards
    nobles: list['Noble']
    tokens: Tokens

    def __init__(self, ruleset: Ruleset, reserved_cards=None, development_cards=None, nobles=None, tokens=None):
        self.reserved_cards = reserved_cards or DevelopmentCards()
        self.development_cards = development_cards or DevelopmentCards()
        self.nobles = nobles or []
        self.tokens = tokens or Tokens()

    def get_development_cards_gem_value(self) -> Gems:
        return Gems(**{
            gem: len([card for card in self.development_cards if card.gem == gem])
            for gem in Gems.TOKEN_TYPES
        })

    def action_select_tokens(self, game: 'GameState', tokens: Tokens) -> None:
        self._ensure_player_select_tokens_legal(game, tokens)
        self.tokens += game.community_tokens.pull(tokens)

        if self.tokens.get_total_count() > game.ruleset.MAX_PLAYER_TOKENS:
            raise OverPlayerTokenLimit  # TODO: should allow discarding

    def _ensure_player_select_tokens_legal(self, game, tokens: Tokens):
        # TODO: split exceptions, or add messages
        if not tokens.is_positive():
            raise IllegalTokenSelection

        if tokens.get_total_count() > 3:
            # the player may not select more than three tokens
            raise IllegalTokenSelection

        if any(value > 1 for value in tokens.values()):
            if tokens.get_total_count() > 2:
                # when player is only allowed to pick two of the same token
                raise IllegalTokenSelection

            token_type = next(token for token, value in tokens if value)
            if game.community_tokens[token_type] < 4:
                # the player may not pick two tokens from a pile with less than four tokens
                raise IllegalTokenSelection

        if tokens.get_total_count() == 3 and all(value in (0, 1) for value in tokens.values()):
            # when three tokens are picked, they must all be of different king
            raise IllegalTokenSelection

    def action_reserve_card(self, game: 'GameState', card_placement: tuple[int, int]):
        # TODO: implement drawing from the restock pile
        self._ensure_player_reserve_card_legal(game, card_placement)
        tier, column = card_placement
        self.reserved_cards.append(game.shop.get_tier(tier).pick_and_replace(column))
        self.tokens += game.community_tokens.pull(Tokens(gold=1))

    def _ensure_player_reserve_card_legal(self, game: 'GameState', card_placement: tuple[int, int]):
        tier, column = card_placement
        if len(self.reserved_cards) > game.ruleset.MAX_PLAYER_RESERVED_CARDS:
            raise

        if tier < 1 or tier > game.ruleset.SHOP_TIER_COUNT:
            # there are only three tiers
            raise IllegalCardReservation

        if not game.shop.get_tier(tier).available_cards[column]:
            # tried to pick an empty slot
            raise IllegalCardReservation


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


@dataclass
class Noble:
    cost: Gems
    prestige: int


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


class GameState:
    ruleset: Ruleset
    player_turn: int = 0
    players: [Player]
    shop: Shop
    community_tokens: Tokens

    @classmethod
    def from_ruleset(cls, ruleset: Ruleset) -> Self:
        return cls(
            ruleset=ruleset,
            players=cls._get_initial_player_states(ruleset),
            shop=cls._get_initial_shop_state(ruleset),
            community_tokens=cls._get_initial_community_currency_value(ruleset),
        )

    def __init__(self, ruleset, players, shop, community_tokens):
        self.ruleset = ruleset
        self.players = players
        self.shop = shop
        self.community_tokens = community_tokens
        self.player_turn = 0

    @staticmethod
    def _get_initial_community_currency_value(ruleset: Ruleset) -> Tokens:
        return Tokens(
            gold=ruleset.COMMUNITY_GOLD_COUNT,
            **{gem: ruleset.COMMUNITY_GEMS_COUNT for gem in Gems.TOKEN_TYPES}
        )

    @staticmethod
    def _get_initial_player_states(ruleset: Ruleset) -> ['Player']:
        return [Player(ruleset) for _ in range(ruleset.PLAYER_COUNT)]

    @staticmethod
    def _get_initial_shop_state(ruleset: Ruleset):
        return Shop.get_initial_shop_state(ruleset)

    def get_current_player(self) -> 'Player':
        return self.get_player(self.player_turn)

    def get_player(self, player: int) -> 'Player':
        return self.players[player]

    def perform_player_turn(self, turn_action: PlayerAction, **action_params):
        player = self.get_current_player()
        getattr(player, f'action_{turn_action.value}')(self, **action_params)

        self.progress_player_turn()

    def progress_player_turn(self):
        self.player_turn = (self.player_turn + 1) % len(self.players)
