import pytest
from Game.game_controllers.Game import GameRenderer
from Game.game_controllers.Game import GhostBehaviour
from unittest.mock import patch, PropertyMock


class TestGameRenderer:
    @pytest.fixture
    def game_renderer(self):
        return GameRenderer(800, 600)

    @pytest.mark.parametrize("initial_mode, kokoro_active, expected_mode", [
        (GhostBehaviour.PEACEFUL, False, GhostBehaviour.AGGRESSIVE),
        (GhostBehaviour.AGGRESSIVE, False, GhostBehaviour.PEACEFUL),
        (GhostBehaviour.PEACEFUL, True, GhostBehaviour.PEACEFUL)
    ])
    @patch.object(GameRenderer, 'kokoro_active', new_callable=PropertyMock)
    @patch('pygame.time.set_timer')
    def test_handle_mode_switch(self, mock_set_timer, mock_kokoro_active, game_renderer, initial_mode, kokoro_active, expected_mode):
        game_renderer.current_mode = initial_mode
        mock_kokoro_active.return_value = kokoro_active

        game_renderer.handle_mode_switch()

        mock_set_timer.assert_called_once()
        assert game_renderer.current_mode == expected_mode
