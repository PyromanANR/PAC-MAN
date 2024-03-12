import pygame
import pytest
from Game.main.button import Button

class TestButton:
    @pytest.mark.parametrize("mouse,expected_color", [
        ((200, 200), (100, 100, 100)),  # mouse is not over the button
        ((50, 50), (200, 200, 200))  # mouse is over the button
    ])
    def test_button_draw(self, mouse, expected_color):
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        button = Button(0, 0, 100, 100, 'Test', (255, 255, 255), None, (200, 200, 200), (100, 100, 100))

        button.draw(screen, mouse)
        assert button.current_color == expected_color

        pygame.quit()