import pygame
import pytest
from Game.game_controllers.Game import GameObject

class GameRenderer:
    def __init__(self, screen):
        self._screen = screen

@pytest.mark.parametrize("is_circle,color,expected_color", [
    (False, (255, 0, 0), (0, 0, 0, 255)),  # game object is a rectangle
    (True, (0, 255, 0), (0, 255, 0, 255))     # game object is a circle
])
def test_game_object_draw(is_circle, color, expected_color):
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    renderer = GameRenderer(screen)
    game_object = GameObject(renderer, 50, 50, 100, color, is_circle)

    game_object.draw()
    assert pygame.Surface.get_at(screen, (50, 50)) == expected_color

    pygame.quit()

