import pytest
from Game.game_controllers.Translate_func import translate_maze_to_screen, translate_screen_to_maze
class TestTranslateFunc:
    def test_translate_screen_to_maze(self):
        assert translate_screen_to_maze((60, 90)) == (2, 3)

    def test_translate_maze_to_screen(self):
        assert translate_maze_to_screen((2, 3)) == (60, 90)