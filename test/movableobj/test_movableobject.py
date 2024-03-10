import pytest
import pygame
from unittest.mock import MagicMock, patch
from Game.movable_obj.MovableObject import MovableObject
from Game.game_controllers.Direction import Direction


class TestMovableObject:
    @pytest.fixture
    def movable_object(self):
        # Mock the in_surface argument as we don't need it for these tests
        in_surface = MagicMock()
        return MovableObject(in_surface, 0, 0, 10)

    def test_collides_with_wall(self, movable_object):
        # Mock the walls and cells attributes of _renderer
        movable_object._renderer.walls = [MagicMock(shape=pygame.Rect(0, 0, 10, 10))]
        movable_object._renderer.cell = []

        # Test collision with a wall
        assert movable_object.collides_with_wall((5, 5))

        # Test no collision
        assert not movable_object.collides_with_wall((20, 20))

    @patch.object(MovableObject, 'collides_with_wall')
    def test_check_collision_in_direction(self, mock_collides_with_wall, movable_object):
        # Mock collides_with_wall to always return False
        mock_collides_with_wall.return_value = False

        # Test each direction
        for direction in Direction:
            collision, desired_position = movable_object.check_collision_in_direction(direction)
            assert not collision
            if direction == Direction.UP:
                assert desired_position == (0, -1)
            elif direction == Direction.DOWN:
                assert desired_position == (0, 1)
            elif direction == Direction.LEFT:
                assert desired_position == (-1, 0)
            elif direction == Direction.RIGHT:
                assert desired_position == (1, 0)
            else:  # Direction.NONE
                assert desired_position == (0, 0)
