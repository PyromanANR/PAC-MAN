import pygame

from Game.game_controllers.Game import GameObject
# Load the image for the wall
wall_image = pygame.image.load("..\..\images\Brick-wall.jpg")


class Wall(GameObject):
    # Gray - in_color=(128, 128, 128)
    def __init__(self, in_surface, x, y, in_size: int, in_color=(128, 128, 128)):
        """
        Initialize the Wall with the given parameters.

        Parameters:
        in_surface (GameRenderer): The surface on which the wall will be rendered.
        x (int): The x-coordinate of the wall.
        y (int): The y-coordinate of the wall.
        in_size (int): The size of the wall.
        in_color (tuple): The color of the wall. Default is gray (128, 128, 128).
        """
        super().__init__(in_surface, x * in_size, y * in_size, in_size, in_color)

    def draw(self):
        """
        Draws the wall on the surface using the loaded wall image.
        """
        image = pygame.transform.scale(wall_image, (self._size, self._size))
        self._surface.blit(image, self.shape)
