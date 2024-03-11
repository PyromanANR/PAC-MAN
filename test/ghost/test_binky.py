import pytest
from unittest.mock import MagicMock, patch
from Game.movable_obj.ghosts.Blinky import Blinky


class TestBlinky:
    @pytest.fixture
    def blinky(self):
        # Mock the in_surface and in_game_controller arguments as we don't need them for these tests
        in_surface = MagicMock()
        in_game_controller = MagicMock()
        # Create mock images
        mock_image = MagicMock()
        sprite_path = MagicMock()
        sprite_fright = MagicMock()

        # Mock pygame.image.load to return the mock images
        with patch('pygame.image.load', return_value=mock_image):
            return Blinky(in_surface, 0, 0, 10, in_game_controller, sprite_path, sprite_fright)

    @pytest.mark.parametrize("hero_position, expected", [
        ((100, 100), (3, 3)),
        ((200, 200), (6, 6)),
    ])
    @pytest.mark.ghost
    def test_find_target_position(self, blinky, hero_position, expected):
        # Mock the _renderer.hero_position method to return a specific position
        blinky._renderer.hero_position.return_value = hero_position
        target_position = blinky.find_target_position()
        assert target_position == expected
