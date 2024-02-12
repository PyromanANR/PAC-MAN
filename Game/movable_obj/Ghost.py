import os

import pygame
from Game.game_controllers.Direction import Direction
from Game.game_controllers.Translate_func import unified_size
from Game.movable_obj.MovableObject import MovableObject


class Ghost(MovableObject):
    def __init__(self, in_surface, x, y, in_size: int, in_game_controller, sprite_path):
        super().__init__(in_surface, x, y, in_size)
        self.game_controller = in_game_controller
        self.sprite_normal = pygame.image.load(sprite_path)
        self.sprite_fright = pygame.image.load(os.path.join('..', '..', 'images', 'ghost_fright.png'))

    def reached_target(self):
        if (self.x, self.y) == self.next_target:
            self.next_target = self.next_location()
        self.current_direction = self.calculate_direction_to_next_target()

    def next_location(self):
        return None if len(self.location_queue) == 0 else self.location_queue.pop(0)

    def new_path(self, in_path):
        for item in in_path:
            self.location_queue.append(item)
        self.next_target = self.next_location()

    def calculate_direction_to_next_target(self) -> Direction:
        if self.next_target is None:
            self.game_controller.request_new_random_path(self)
            return Direction.NONE

        diff_x = self.next_target[0] - self.x
        diff_y = self.next_target[1] - self.y

        if diff_x == 0:
            return Direction.DOWN if diff_y > 0 else Direction.UP
        if diff_y == 0:
            return Direction.LEFT if diff_x < 0 else Direction.RIGHT

        self.game_controller.request_new_random_path(self)
        return Direction.NONE

    def automatic_move(self, in_direction: Direction):
        if in_direction == Direction.UP:
            self.position = self.x, self.y - 1
        elif in_direction == Direction.DOWN:
            self.position = self.x, self.y + 1
        elif in_direction == Direction.LEFT:
            self.position = self.x - 1, self.y
        elif in_direction == Direction.RIGHT:
            self.position = self.x + 1, self.y

    def draw(self):
        self.image = self.sprite_normal
        super(Ghost, self).draw()

