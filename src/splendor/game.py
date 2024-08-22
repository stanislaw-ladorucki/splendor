from typing import Self

from .player import Player, PlayerAction
from .ruleset import Ruleset
from .shop import Shop
from .tokens import Gems, Tokens


class GameState:
    ruleset: Ruleset
    player_turn: int = 0
    players: ['Player']
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
