import pytest
from unittest.mock import MagicMock, patch
from Game.movable_obj.ghosts.Pinky import Pinky


class TestPinky:
    @pytest.fixture
    def pinky(self):
        # Mock the in_surface and in_game_controller arguments as we don't need them for these tests
        in_surface = MagicMock()
        in_game_controller = MagicMock()
        # Create mock images
        mock_image = MagicMock()
        sprite_path = MagicMock()
        sprite_fright = MagicMock()

        # Mock pygame.image.load to return the mock images
        with patch('pygame.image.load', return_value=mock_image):
            return Pinky(in_surface, 0, 0, 10, in_game_controller, sprite_path, sprite_fright)

    @pytest.mark.parametrize("character_position, expected", [
        ((1, 1), (0, 0)),
        ((3, 3), (1, 3)),
    ])
    @pytest.mark.ghost
    def test_find_position_relative_to_character(self, pinky, character_position, expected):
        # Mock the game_controller.numpy_maze method to return a specific maze
        pinky.game_controller.numpy_maze = [[1 for _ in range(10)] for _ in range(10)]

        relative_position = pinky.find_position_relative_to_character(character_position)

        assert relative_position == expected