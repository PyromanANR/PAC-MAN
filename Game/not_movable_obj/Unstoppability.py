from Game.game_controllers.Game import GameObject


class Unstoppability(GameObject):
    def __init__(self, in_surface, x, y):
        """
        Initialize the Unstoppability power-up with the given parameters.

        Parameters:
        in_surface (GameRenderer): The surface on which the power-up will be rendered.
        x (int): The x-coordinate of the power-up.
        y (int): The y-coordinate of the power-up.

        The size of the power-up is set to 8, the color is set to white (255, 255, 255), and it is set to be a circle.
        """
        super().__init__(in_surface, x, y, 8, (255, 255, 255), True)