from Game.game_controllers.Game import GameObject


class Cookie(GameObject):
    def __init__(self, in_surface, x, y):
        """
        Initialize the Cookie with the given parameters.

        Parameters:
        in_surface (GameRenderer): The surface on which the cookie will be rendered.
        x (int): The x-coordinate of the cookie.
        y (int): The y-coordinate of the cookie.

        The size of the cookie is set to 4, the color is set to yellow (255, 255, 0), and it is set to be a circle.
        """
        super().__init__(in_surface, x, y, 4, (255, 255, 0), True)
