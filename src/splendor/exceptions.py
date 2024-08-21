class IllegalPlayerActionError(Exception):
    pass


class TokenError(IllegalPlayerActionError):
    pass


class InvalidTokenTypeError(TokenError):
    pass


class InvalidTokenValueError(TokenError):
    pass


class InvalidTokenPullError(TokenError):
    pass


class OverPlayerTokenLimit(TokenError):
    pass


class IllegalTokenSelection(IllegalPlayerActionError):
    pass


class IllegalCardReservation(IllegalPlayerActionError):
    pass


class NotEnoughCommunityTokensError(InvalidTokenPullError):
    pass


class InvalidGameConfiguration(Exception):
    pass


class OverPlayerLimit(InvalidGameConfiguration):
    pass


class NotEnoughPlayers(InvalidGameConfiguration):
    pass


class InvalidShopTierCount(InvalidGameConfiguration):
    pass
