import pytest
from unittest.mock import MagicMock, patch
from Game.movable_obj.ghosts.Clyde import Clyde


class TestClyde:
    @pytest.fixture
    def clyde(self):
        # Mock the in_surface and in_game_controller arguments as we don't need them for these tests
        in_surface = MagicMock()
        in_game_controller = MagicMock()
        # Create mock images
        mock_image = MagicMock()
        sprite_path = MagicMock()
        sprite_fright = MagicMock()

        # Mock pygame.image.load to return the mock images
        with patch('pygame.image.load', return_value=mock_image):
            return Clyde(in_surface, 0, 0, 10, in_game_controller, sprite_path, sprite_fright)

    @pytest.mark.parametrize("character_position, current_maze_coord, expected", [
        (((100, 100), (3, 3), (3, 3))),
        (((200, 200), (6, 6), (6, 6))),
    ])
    @pytest.mark.ghost
    def test_find_position_outside_radius(self, clyde, character_position, current_maze_coord, expected):
        # Mock the game_controller.numpy_maze method to return a specific maze
        clyde.game_controller.numpy_maze = MagicMock(return_value=[[0, 1, 0], [1, 0, 1], [0, 1, 0]])

        target_position = clyde.find_position_outside_radius(character_position, current_maze_coord)

        assert target_position == expected
