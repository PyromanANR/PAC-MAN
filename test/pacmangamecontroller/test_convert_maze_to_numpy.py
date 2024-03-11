import pytest
from unittest.mock import patch
from Game.game_controllers.PacmanGameController import PacmanGameController


class TestPacmanGameController:
    @pytest.fixture
    def game_controller(self, request):
        return PacmanGameController(request.param)

    @pytest.mark.parametrize("game_controller, expected_size", [
        (0, (31, 22)),
        (1, (33, 21)),
    ], indirect=["game_controller"])
    def test_convert_maze_to_numpy(self, game_controller, expected_size):
        assert game_controller.size == expected_size
        assert len(game_controller.ghost_spawns) == 4  # Check that there are 4 ghost spawns
