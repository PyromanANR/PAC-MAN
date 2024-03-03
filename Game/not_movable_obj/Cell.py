import pygame
import os
from Game.game_controllers.Game import GameObject
# Load the image for the cell
cell_image = pygame.image.load(os.path.join('..', '..', 'images', 'cell.png'))


class Cell(GameObject):
    def __init__(self, in_surface, x, y, in_size: int, in_color=(128, 128, 128)):
        """
            Initialize the Cell with the given parameters.

            Parameters:
            in_surface (GameRenderer): The surface on which the cell will be rendered.
            x (int): The x-coordinate of the cell.
            y (int): The y-coordinate of the cell.
            in_size (int): The size of the cell.
            in_color (tuple): The color of the cell. Default is gray (128, 128, 128).
        """
        super().__init__(in_surface, x, y, in_size, in_color)

    def draw(self):
        """
        Draws the cell on the surface using the loaded cell image.
        """
        image = pygame.transform.scale(cell_image, (self._size, self._size))
        self._surface.blit(image, self.shape)