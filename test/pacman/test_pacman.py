from Game.game_controllers.PacmanGameController import PacmanGameController
from Game.game_controllers.Direction import Direction
from Game.game_controllers.Game import GameRenderer
from Game.movable_obj.PacMan import PacMan
from unittest.mock import Mock
import pytest


class TestPacman:
    def test_tick(self):
        game_renderer = GameRenderer(800, 600)
        pacman_game = PacmanGameController(0)
        pacman = PacMan(game_renderer, 0, 0, 30, pacman_game)

        # Mock the methods that tick calls
        pacman.check_collision_in_direction = Mock(return_value=[False])
        pacman.automatic_move = Mock()
        pacman.collides_with_wall = Mock(return_value=False)
        pacman.handle_cookie_pickup = Mock()
        pacman.handle_ghosts = Mock()

        pacman.tick()

        # Check if the mocked methods are called correctly
        pacman.check_collision_in_direction.assert_called_once_with(pacman.direction_buffer)
        pacman.automatic_move.assert_called_once_with(pacman.direction_buffer)
        pacman.collides_with_wall.assert_called_once_with((pacman.x, pacman.y))
        pacman.handle_cookie_pickup.assert_called_once()
        pacman.handle_ghosts.assert_called_once()

    def test_automatic_move(self):
        game_renderer = GameRenderer(800, 600)
        pacman_game = PacmanGameController(0)
        pacman = PacMan(game_renderer, 0, 0, 30, pacman_game)

        # Mock the check_collision_in_direction method
        pacman.check_collision_in_direction = Mock(return_value=[False, (10, 10)])

        initial_position = pacman.position
        initial_direction = pacman.current_direction

        pacman.automatic_move(Direction.UP)

        # Check if the position and direction are updated correctly
        assert pacman.position != initial_position
        assert pacman.current_direction == initial_direction
        assert pacman.last_working_direction == initial_direction

