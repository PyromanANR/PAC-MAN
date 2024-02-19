import pygame

from Game.game_controllers.Game import GameObject

wall_image = pygame.image.load("..\..\images\Brick-wall.jpg")


class Wall(GameObject):
    # Gray - in_color=(128, 128, 128)
    def __init__(self, in_surface, x, y, in_size: int, in_color=(128, 128, 128)):
        super().__init__(in_surface, x * in_size, y * in_size, in_size, in_color)

    def draw(self):
        image = pygame.transform.scale(wall_image, (self._size, self._size))
        self._surface.blit(image, self.shape)
