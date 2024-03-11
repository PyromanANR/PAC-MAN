import pytest
from unittest.mock import MagicMock, patch
from Game.movable_obj.Ghost import Ghost
from Game.game_controllers.Direction import Direction


class TestGhost:
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
            return Ghost(in_surface, 0, 0, 10, in_game_controller, sprite_path, sprite_fright)

    def test_reached_target(self, ghost):
        # Set the next_target to the current position
        ghost.next_target = (ghost.x, ghost.y)

        # Mock the next_location and calculate_direction_to_next_target methods
        with patch.object(Ghost, 'next_location', return_value='next_location'), \
                patch.object(Ghost, 'calculate_direction_to_next_target', return_value=Direction.NONE):
            ghost.reached_target()

        # Check that next_target and current_direction were updated
        assert ghost.next_target == 'next_location'
        assert ghost.current_direction == Direction.NONE

    def test_next_location(self, ghost):
        # Test when location_queue is empty
        ghost.location_queue = []
        assert ghost.next_location() is None

        # Test when location_queue is not empty
        ghost.location_queue = ['location1', 'location2']
        assert ghost.next_location() == 'location1'
        assert ghost.location_queue == ['location2']

    def test_new_path(self, ghost):
        # Mock the next_location method
        with patch.object(Ghost, 'next_location', return_value='next_location'):
            ghost.new_path(['path1', 'path2'])

        # Check that _path, location_queue, and next_target were updated
        assert ghost._path == ['path1', 'path2']
        assert ghost.location_queue == ['path1', 'path2']
        assert ghost.next_target == 'next_location'
    @pytest.mark.parametrize("direction, expected_position", [
        (Direction.UP, (0, -1)),
        (Direction.DOWN, (0, 1)),
        (Direction.LEFT, (-1, 0)),
        (Direction.RIGHT, (1, 0)),
    ])
    def test_automatic_move(self, ghost, direction, expected_position):
        ghost.automatic_move(direction)

        # Check that the position was updated correctly
        assert ghost.position == expected_position

    @patch('pygame.time.set_timer')
    def test_activate_death(self, mock_set_timer, ghost):
        ghost.activate_death()

        # Check that death was set to True, location_queue was cleared, and set_timer was called
        assert ghost.death
        assert not ghost.location_queue
        mock_set_timer.assert_called_once_with(ghost.death_event, 10000)
