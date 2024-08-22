from enum import Enum
from typing import TYPE_CHECKING

from .cards import DevelopmentCards
from .exceptions import IllegalCardReservation, IllegalTokenSelection, OverPlayerTokenLimit
from .ruleset import Ruleset
from .tokens import Gems, Tokens

if TYPE_CHECKING:
    from .game import GameState
    from .nobles import Noble


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
