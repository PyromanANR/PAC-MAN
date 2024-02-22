import pygame
from Game.game_controllers.Direction import Direction
from Game.game_controllers.GhostBehaviour import GhostBehaviour
from Game.game_controllers.Translate_func import unified_size, translate_maze_to_screen, translate_screen_to_maze
from Game.movable_obj.MovableObject import MovableObject


class Ghost(MovableObject):
    def __init__(self, in_surface, x, y, in_size: int, in_game_controller, sprite_path, sprite_fright):
        """
        Initialize the Ghost with the given parameters.

        Parameters:
        in_surface (GameRenderer): The surface on which the ghost will be rendered.
        x (int): The x-coordinate of the ghost.
        y (int): The y-coordinate of the ghost.
        in_size (int): The size of the ghost.
        in_game_controller (PacmanGameController): The game controller.
        sprite_path (str): The path to the image file for the normal ghost sprite.
        sprite_fright (str): The path to the image file for the frightened ghost sprite.
        """
        super().__init__(in_surface, x, y, in_size)
        self.game_controller = in_game_controller
        self.sprite_normal = pygame.image.load(sprite_path)
        self.sprite_fright = pygame.image.load(sprite_fright)
        self._path = None
        self.path_built = False
        self.death_event = pygame.USEREVENT + pygame.time.get_ticks()
        self._death = False

    @property
    def death(self) -> bool:
        return self._death

    @death.setter
    def death(self, value: bool):
        self._death = value

    def draw_path(self):
        """
        Draw the path of the ghost on the surface. The color of the path depends on the type of the ghost.
        """
        from Game.movable_obj.ghosts.Blinky import Blinky
        from Game.movable_obj.ghosts.Clyde import Clyde
        from Game.movable_obj.ghosts.Inky import Inky
        from Game.movable_obj.ghosts.Pinky import Pinky
        color_mapping = {
            Blinky: "red",
            Clyde: "orange",
            Inky: "blue",
            Pinky: "pink"
        }
        if self._path is not None:
            for x, y in self._path:
                rect = pygame.Rect(x, y, 5, 5)
                ghost_color = color_mapping.get(type(self), "red")  # Default to red
                pygame.draw.rect(self._surface, ghost_color, rect)

    def reached_target(self):
        """
        Checks if the ghost has reached its target. If so, it gets the next target location and calculates the direction to it.
        """
        if self._renderer.devmode: self.draw_path()
        if (self.x, self.y) == self.next_target:
            self.next_target = self.next_location()
        self.current_direction = self.calculate_direction_to_next_target()

    def next_location(self):
        """
        Returns the next location in the ghost's path. If the path is empty, it returns None.
        """
        return None if len(self.location_queue) == 0 else self.location_queue.pop(0)

    def new_path(self, in_path):
        """
        Sets a new path for the ghost.

        Parameters:
        in_path (list): The new path for the ghost.
        """
        self._path = in_path
        self.location_queue.clear()
        for item in in_path:
            self.location_queue.append(item)
        self.next_target = self.next_location()

    def calculate_direction_to_next_target(self) -> Direction:
        """
         Calculates the direction to the next target based on the current mode of the game.
         If the next target is None, it requests a new random path.

         Returns:
         Direction: The direction to the next target.
         """
        if self._renderer.current_mode == GhostBehaviour.AGGRESSIVE:
            if not self.path_built:
                self.location_queue.clear()
                self.path_built = True
                self.request_path_to_player()
            elif self.next_target is None:
                self.request_path_to_player()
        elif self._renderer.current_mode == GhostBehaviour.PEACEFUL:
            if self.path_built:
                self.path_built = False
                self.location_queue.clear()

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

    def find_target_position(self):
        """
         This method should be overridden by subclasses to provide the target position based on the ghost's behavior.
        """
        pass

    def request_path_to_player(self):
        """
        Requests a path to the player's position and sets it as the new path for the ghost.
        """
        target_position = self.find_target_position()
        current_maze_coord = translate_screen_to_maze(self.position)
        path = self.game_controller.p.path(current_maze_coord[1], current_maze_coord[0],
                                           target_position[1], target_position[0])

        new_path = [translate_maze_to_screen(item) for item in path]
        self.new_path(new_path)

    def automatic_move(self, in_direction: Direction):
        """
         Moves the ghost automatically in the given direction.

         Parameters:
         in_direction (Direction): The direction in which to move the ghost.
         """
        if in_direction == Direction.UP:
            self.position = self.x, self.y - 1
        elif in_direction == Direction.DOWN:
            self.position = self.x, self.y + 1
        elif in_direction == Direction.LEFT:
            self.position = self.x - 1, self.y
        elif in_direction == Direction.RIGHT:
            self.position = self.x + 1, self.y

    def activate_death(self):
        """
        Activates the 'death' state of the ghost and starts a timer for it.
        """
        self.death = True
        self.location_queue.clear()
        pygame.time.set_timer(self.death_event, 10000)

    def draw(self):
        """
        Draws the ghost on the surface. If the 'kokoro' mode is active, it uses the frightened sprite. Otherwise, it uses the normal sprite.
        """
        self.image = self.sprite_fright if self._renderer.kokoro_active else self.sprite_normal
        super(Ghost, self).draw()
