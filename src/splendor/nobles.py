from .tokens import Gems


class Noble:
    cost: Gems
    prestige: int

    def __init__(self, cost, prestige):
        self.cost = cost
        self.prestige = prestige
