from Game.MovableObj.MovableObject import MovableObject


class Ghost(MovableObject):
    def __init__(self, in_surface, x, y, in_size: int, in_game_controller, in_color=(255, 0, 0)):
        super().__init__(in_surface, x, y, in_size, in_color, False)
        self.game_controller = in_game_controller