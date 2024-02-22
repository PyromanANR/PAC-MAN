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
        """
        Checks if a given position collides with a wall.

        Parameters:
        - in_position (Tuple[int, int]): The position to check for collision.

        Usage:
        - This method is used to check if a given position collides with any of the walls in the game.

        Returns:
        - bool: True if the given position collides with a wall, False otherwise.
        """

        collision_rect = pygame.Rect(in_position[0], in_position[1], self._size, self._size)
        collides = False
        walls = self._renderer.walls
        cells = self._renderer.cell
        for obstacle in walls + cells:
            collides = collision_rect.colliderect(obstacle.shape)
            if collides:
                break
        return collides

    def check_collision_in_direction(self, in_direction: Direction):
        """
        Checks for a collision in a given direction.

        Parameters:
        - in_direction (Direction): The direction to check for collision.

        Usage:
        - This method is used to check for a collision in a given direction.
        - It calculates the desired position based on the current position and the given direction.
        - It then checks if the desired position collides with a wall.

        Returns:
        - Tuple[bool, Tuple[int, int]]: A tuple containing a boolean indicating whether a collision occurred, and the desired position.
        """

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
        """
        Automatically moves the object in a given direction.

        Parameters:
        - in_direction (Direction): The direction in which to move the object.

        Usage:
        - This method is used to automatically move the object in a given direction.
        - The specific implementation of this method is not provided here.

        Returns:
        - None
        """
        pass

    def tick(self):
        """
        Updates the state of the object for each tick of the game loop.

        Usage:
        - This method is used to update the state of the object for each tick of the game loop.
        - It checks if the object has reached its target and then moves the object in its current direction.

        Returns:
        - None
        """

        self.reached_target()
        self.automatic_move(self.current_direction)

    def reached_target(self):
        """
        Checks if the object has reached its target.

        Usage:
        - This method is used to check if the object has reached its target.
        - The specific implementation of this method is not provided here.

        Returns:
        - None
        """
        pass

    def draw(self):
        """
        Draws the object on the screen.

        Usage:
        - This method is used to draw the object on the screen.
        - It scales the object's image to the unified size and then blits it onto the screen at the object's shape.

        Returns:
        - None
        """

        self.image = pygame.transform.scale(self.image, (unified_size, unified_size))
        self._surface.blit(self.image, self.shape)
