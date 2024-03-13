from Game.game_controllers.PacmanGameController import PacmanGameController
from Game.game_controllers.Direction import Direction
from Game.game_controllers.Game import GameRenderer
from Game.movable_obj.PacMan import PacMan
from Game.movable_obj.Ghost import Ghost
from Game.game_controllers.ScoreType import ScoreType
from unittest.mock import Mock, MagicMock, patch
import pytest
from copy import deepcopy


class TestPacman:
    @pytest.fixture
    def pacman(self):
        # Mock the in_surface and in_game_controller arguments as we don't need them for these tests
        in_surface = MagicMock()
        in_game_controller = MagicMock()

        # Create mock images
        open_image = MagicMock()
        closed_image = MagicMock()

        # Mock pygame.image.load to return the mock images
        with patch('pygame.image.load', side_effect=[open_image, closed_image]):
            return PacMan(in_surface, 0, 0, 30, in_game_controller)

    def test_tick(self, pacman):
        game_renderer = GameRenderer(800, 600)
        pacman_game = PacmanGameController(0)
        pacman._renderer._width = 800
        pacman._renderer._height = 600

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

    def test_automatic_move(self, pacman):
        game_renderer = GameRenderer(800, 600)
        pacman_game = PacmanGameController(0)

        # Mock the check_collision_in_direction method
        pacman.check_collision_in_direction = Mock(return_value=[False, (10, 10)])

        initial_position = pacman.position
        initial_direction = pacman.current_direction

        pacman.automatic_move(Direction.UP)

        # Check if the position and direction are updated correctly
        assert pacman.position != initial_position
        assert pacman.current_direction == initial_direction
        assert pacman.last_working_direction == initial_direction

    @pytest.fixture
    def ghost(self):
        # Mock the in_surface and in_game_controller arguments as we don't need them for these tests
        in_surface = MagicMock()
        in_game_controller = MagicMock()

        # Create mock images
        mock_image = MagicMock()
        sprite_path = MagicMock()
        sprite_fright = MagicMock()

        # Mock pygame.image.load to return the mock images
        with patch('pygame.image.load', return_value=mock_image):
            return Ghost(in_surface, 0, 0, 30, in_game_controller, sprite_path, sprite_fright)

    def test_handle_ghosts(self, ghost, pacman):
        game_renderer = GameRenderer(800, 600)
        pacman._renderer = game_renderer
        pacman_game = PacmanGameController(0)
        game_renderer.hero = pacman

        # Add the ghost to the game objects and the ghost list
        game_renderer.game_object.append(ghost)
        game_renderer.ghost.append(ghost)

        # Mock the add_score and kill_pacman methods
        game_renderer.add_score = Mock()

        # Set the kokoro_active attribute to True
        game_renderer.kokoro_active = True

        pacman.handle_ghosts()

        # Check if the add_score method is called correctly
        game_renderer.add_score.assert_called_once_with(ScoreType.GHOST)

        # Set the kokoro_active attribute to False and the won attribute to False
        game_renderer.kokoro_active = False
        game_renderer.won = False
        game_renderer.kill_pacman = Mock()
        pacman.handle_ghosts()

        # Check if the kill_pacman method is called
        game_renderer.kill_pacman.assert_called_once()


