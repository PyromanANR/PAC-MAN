from Game.game_controllers.Game import GameObject


class Wall(GameObject):
    # Gray - in_color=(128, 128, 128)
    def __init__(self, in_surface, x, y, in_size: int, in_color=(128, 128, 128)):
        super().__init__(in_surface, x * in_size, y * in_size, in_size, in_color)