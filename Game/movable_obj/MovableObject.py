import pygame
from Game.game_controllers.Direction import Direction
from Game.game_controllers.Game import GameObject
from Game.game_controllers.Translate_func import unified_size


class MovableObject(GameObject):
    def __init__(self, in_surface, x, y, in_size: int, in_color=(255, 0, 0), is_circle: bool = False):
        super().__init__(in_surface, x, y, in_size, in_color, is_circle)
        self.current_direction = Direction.NONE
        self.direction_buffer = Direction.NONE
        self.last_working_direction = Direction.NONE
        self.location_queue = []
        self.next_target = None
        self.image = None

    @property
    def direction(self):
        return self.current_direction, self.direction_buffer

    @direction.setter
    def direction(self, in_direction):
        self.current_direction = in_direction
        self.direction_buffer = in_direction

    def collides_with_wall(self, in_position):
        collision_rect = pygame.Rect(in_position[0], in_position[1], self._size, self._size)
        collides = False
        walls = self._renderer.walls
        for wall in walls:
            collides = collision_rect.colliderect(wall.shape)
            if collides: break
        return collides

    def check_collision_in_direction(self, in_direction: Direction):
        desired_position = (0, 0)
        if in_direction == Direction.NONE: return False, desired_position
        if in_direction == Direction.UP:
            desired_position = (self.x, self.y - 1)
        elif in_direction == Direction.DOWN:
            desired_position = (self.x, self.y + 1)
        elif in_direction == Direction.LEFT:
            desired_position = (self.x - 1, self.y)
        elif in_direction == Direction.RIGHT:
            desired_position = (self.x + 1, self.y)

        return self.collides_with_wall(desired_position), desired_position

    def automatic_move(self, in_direction: Direction):
        pass

    def tick(self):
        self.reached_target()
        self.automatic_move(self.current_direction)

    def reached_target(self):
        pass

    def draw(self):
        self.image = pygame.transform.scale(self.image, (unified_size, unified_size))
        self._surface.blit(self.image, self.shape)
