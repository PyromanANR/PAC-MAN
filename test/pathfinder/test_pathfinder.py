import pytest
from unittest.mock import MagicMock, patch
from Game.game_controllers.Pathfinder import Pathfinder
import tcod


class TestPathfinder:
    @pytest.fixture
    def pathfinder(self):
        # Create a 2D array representing a simple maze
        in_arr = [
            [1, 1, 0],
            [0, 1, 0],
            [0, 1, 1]
        ]
        return Pathfinder(in_arr)

    def test_path(self, pathfinder):
        # Test the path method
        path = pathfinder.path(0, 0, 2, 2)

        # Check that the path is correct
        assert path == [(1, 0), (1, 1), (1, 2), (2, 2)]
