from Game.game_controllers.Game import GameRenderer
from Game.game_controllers.GhostBehaviour import GhostBehaviour
from Game.game_controllers.ScoreType import ScoreType
from Game.movable_obj.PacMan import PacMan
from Game.game_controllers.PacmanGameController import PacmanGameController
import pygame
import pytest
from unittest.mock import patch
from Game.game_controllers.Direction import Direction


class TestGameRenderer:
    def test_kill_pacman(self):
        game_renderer = GameRenderer(800, 600)
        pacman_game = PacmanGameController(0)
        pacman = PacMan(game_renderer, 0, 0, 30, pacman_game)
        game_renderer.hero = pacman

        initial_lives = game_renderer._lives
        game_renderer.kill_pacman()

        assert game_renderer._lives == initial_lives - 1
        assert game_renderer._current_mode == GhostBehaviour.PEACEFUL

    @pytest.mark.parametrize("key,expected_direction", [
        (pygame.K_LEFT, Direction.LEFT),
        (pygame.K_UP, Direction.UP),
        (pygame.K_DOWN, Direction.DOWN),
        (pygame.K_RIGHT, Direction.RIGHT)
    ])
    def test_handle_move_switch(self, key, expected_direction):
        game_renderer = GameRenderer(800, 600)
        pacman_game = PacmanGameController(0)
        pacman = PacMan(game_renderer, 0, 0, 30, pacman_game)
        game_renderer.hero = pacman

        with patch('pygame.key.get_pressed') as mock_get_pressed:
            keys = {key: 0 for key in [pygame.K_LEFT, pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT]}
            keys[key] = 1  # simulate key press
            mock_get_pressed.return_value = keys
            game_renderer.handle_move_switch()

        assert game_renderer._hero.direction[0] == expected_direction

    def test_add_score(self):
        game_renderer = GameRenderer(800, 600)

        initial_score = game_renderer._score
        score_to_add = ScoreType.COOKIE

        game_renderer.add_score(score_to_add)

        assert game_renderer._score == initial_score + score_to_add.value