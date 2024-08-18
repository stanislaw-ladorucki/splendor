from dataclasses import dataclass, field
from enum import Enum
from typing import Self

from constants import (
    MAX_PLAYER_TOKENS, MAX_PLAYERS, MIN_PLAYERS, SHOP_TIER_CARDS_COUNT, SHOP_TIER_COUNT,
    MAX_PLAYER_RESERVED_CARDS,
)
from exceptions import (
    OverPlayerTokenLimit, OverPlayerLimit, NotEnoughPlayers, IllegalTokenSelection,
    IllegalCardReservation,
)
from items import DevelopmentCard, Noble, TIER_ONE_CARDS, TIER_TWO_CARDS, TIER_THREE_CARDS
from tokens import Tokens, Gems


class PlayerAction(Enum):
    SELECT_TOKENS = 'select_tokens'
    RESERVE_CARD = 'reserve_card'
    BUY_CARD = 'buy_card'


@dataclass
class Player:
    reserved_cards: list[DevelopmentCard] = field(default_factory=list)
    development_cards: list[DevelopmentCard] = field(default_factory=list)
    nobles: list[Noble] = field(default_factory=list)
    tokens: Tokens = field(default_factory=Tokens)

    def get_development_cards_gem_value(self) -> Gems:
        return Gems(**{
            gem: len([card for card in self.development_cards if card.gem == gem])
            for gem in Gems.TOKEN_TYPES
        })

    def action_select_tokens(self, game: 'Game', tokens: Tokens) -> None:
        self._ensure_player_select_tokens_legal(game, tokens)
        self.tokens += game.community_tokens.pull(tokens)

        if self.tokens.get_total_count() > MAX_PLAYER_TOKENS:
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

    def action_reserve_card(self, game: 'Game', card_placement: tuple[int, int]):
        # TODO: implement drawing from the restock pile
        self._ensure_player_reserve_card_legal(game, card_placement)
        tier, column = card_placement
        self.reserved_cards.append(game.shop.get_tier(tier).take_card(column))
        self.tokens += game.community_tokens.pull(Tokens(gold=1))

    def _ensure_player_reserve_card_legal(self, game: 'Game', card_placement: tuple[int, int]):
        tier, column = card_placement
        if len(self.reserved_cards) > MAX_PLAYER_RESERVED_CARDS:
            raise

        if tier < 1 or tier > SHOP_TIER_COUNT:
            # there are only three tiers
            raise IllegalCardReservation


@dataclass
class ShopTier:
    tier_numer: int = 1
    restock_pile: list[DevelopmentCard] = field(default_factory=list)
    available_cards: list[DevelopmentCard] = field(default_factory=list)

    def __post_init__(self):
        self.available_cards += [  # ensure the correct amount of cards is available for sale
            self.restock_pile.pop()
            for _ in range(SHOP_TIER_CARDS_COUNT - len(self.available_cards))
        ]

    def take_card(self, index: int):
        # TODO: may raise index error
        card = self.available_cards[index]
        try:
            self.available_cards[index] = self.restock_pile.pop()

        except IndexError:
            self.available_cards.pop(index)

        return card


@dataclass
class Shop:
    nobles: list[Noble] = field(default_factory=list)
    tiers: list[ShopTier] = field(default_factory=list)

    def get_tier(self, tier):
        return self.tiers[tier + 1]

    @classmethod
    def get_initial_shop_state(cls) -> Self:
        # TODO: add nobles
        # TODO: shuffle cards
        return cls(
            tiers=[
                ShopTier(tier_numer=1, restock_pile=TIER_ONE_CARDS.copy()),
                ShopTier(tier_numer=2, restock_pile=TIER_TWO_CARDS.copy()),
                ShopTier(tier_numer=3, restock_pile=TIER_THREE_CARDS.copy()),
            ]
        )


class Game:
    player_turn: int = 0
    players: [Player]
    shop: Shop
    community_tokens: Tokens

    @classmethod
    def start(cls, player_count: int) -> Self:
        if player_count > MAX_PLAYERS:
            raise OverPlayerLimit

        if player_count < MIN_PLAYERS:
            raise NotEnoughPlayers

        return cls(
            players=cls._get_initial_players(player_count),
            shop=cls._get_initial_shop_state(),
            community_tokens=cls._get_initial_community_currency_value(player_count),
        )

    def __init__(self, players, shop, community_tokens):
        self.players = players
        self.shop = shop
        self.community_tokens = community_tokens
        self.player_turn = 0

    @staticmethod
    def _get_initial_community_currency_value(player_count: int) -> Tokens:
        gem_count = (
            4 if player_count < 3 else
            5 if player_count < 4 else
            7
        )
        return Tokens(gold=5, **{gem: gem_count for gem in Gems.TOKEN_TYPES})

    @staticmethod
    def _get_initial_players(player_count: int) -> ['Player']:
        return [Player() for _ in range(player_count)]

    @staticmethod
    def _get_initial_shop_state():
        return Shop.get_initial_shop_state()

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
