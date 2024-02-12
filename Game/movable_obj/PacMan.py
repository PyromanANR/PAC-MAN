import os
import pygame
from Game.game_controllers.Direction import Direction
from Game.movable_obj.MovableObject import MovableObject


class PacMan(MovableObject):
    def __init__(self, in_surface, x, y, in_size: int):
        super().__init__(in_surface, x, y, in_size, (255, 255, 0), False)
        self.last_non_colliding_position = (0, 0)


    def tick(self):
        # TELEPORT(Start to end screen)
        if self.x < 0:
            self.x = self._renderer._width

        if self.y < 0:
            self.y = self._renderer._height

        if self.x > self._renderer._width:
            self.x = 0

        if self.y > self._renderer._height:
            self.y = 0

        self.last_non_colliding_position = self.position

        if self.check_collision_in_direction(self.direction_buffer)[0]:
            self.automatic_move(self.current_direction)
        else:
            self.automatic_move(self.direction_buffer)
            self.current_direction = self.direction_buffer

        if self.collides_with_wall((self.x, self.y)):
            self.position = self.last_non_colliding_position

        #self.handle_cookie_pickup()

    def automatic_move(self, in_direction: Direction):
        collision_result = self.check_collision_in_direction(in_direction)
        desired_position_collides = collision_result[0]
        if not desired_position_collides:
            self.last_working_direction = self.current_direction
            desired_position = collision_result[1]
            self.position = desired_position
        else:
            self.current_direction = self.last_working_direction








