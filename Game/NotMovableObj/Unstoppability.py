from Game.Game_Controllers.Game import GameObject


class Unstoppability(GameObject):
    def __init__(self, in_surface, x, y):
        super().__init__(in_surface, x, y, 8, (255, 255, 255), True)