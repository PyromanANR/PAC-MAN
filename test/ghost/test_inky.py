import pytest
from unittest.mock import MagicMock, patch
from Game.movable_obj.ghosts.Inky import Inky


class TestInky:
    @pytest.fixture
    def inky(self):
        # Mock the in_surface and in_game_controller arguments as we don't need them for these tests
        in_surface = MagicMock()
        in_game_controller = MagicMock()
        # Create mock images
        mock_image = MagicMock()
        sprite_path = MagicMock()
        sprite_fright = MagicMock()

        # Mock pygame.image.load to return the mock images
        with patch('pygame.image.load', return_value=mock_image):
            return Inky(in_surface, 0, 0, 10, in_game_controller, sprite_path, sprite_fright)

    @pytest.mark.parametrize("pacman_position, blinky_position, expected", [
        ((1, 1), (2, 2), (0, 0)),
        ((3, 3), (1, 1), (5, 5)),
    ])
    @pytest.mark.ghost
    def test_mirror_position_relative_to_pacman(self, inky, pacman_position, blinky_position, expected):
        # Mock the game_controller.numpy_maze method to return a specific maze
        inky.game_controller.numpy_maze = [[1 for _ in range(10)] for _ in range(10)]

        mirrored_position = inky.mirror_position_relative_to_pacman(pacman_position, blinky_position)

        assert mirrored_position == expected