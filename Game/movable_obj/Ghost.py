import pygame
from Game.game_controllers.Direction import Direction
from Game.game_controllers.GhostBehaviour import GhostBehaviour
from Game.game_controllers.Translate_func import unified_size
from Game.movable_obj.MovableObject import MovableObject


class Ghost(MovableObject):
    def __init__(self, in_surface, x, y, in_size: int, in_game_controller, sprite_path, sprite_fright):
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
        from Game.movable_obj.Ghosts.Blinky import Blinky
        from Game.movable_obj.Ghosts.Clyde import Clyde
        from Game.movable_obj.Ghosts.Inky import Inky
        from Game.movable_obj.Ghosts.Pinky import Pinky
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
        self.draw_path()
        if (self.x, self.y) == self.next_target:
            self.next_target = self.next_location()
        self.current_direction = self.calculate_direction_to_next_target()

    def next_location(self):
        return None if len(self.location_queue) == 0 else self.location_queue.pop(0)

    def new_path(self, in_path):
        self._path = in_path
        self.location_queue.clear()
        for item in in_path:
            self.location_queue.append(item)
        self.next_target = self.next_location()

    def calculate_direction_to_next_target(self) -> Direction:
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

    def request_path_to_player(self):
        pass

    def automatic_move(self, in_direction: Direction):
        if in_direction == Direction.UP:
            self.position = self.x, self.y - 1
        elif in_direction == Direction.DOWN:
            self.position = self.x, self.y + 1
        elif in_direction == Direction.LEFT:
            self.position = self.x - 1, self.y
        elif in_direction == Direction.RIGHT:
            self.position = self.x + 1, self.y

    def activate_death(self):
        self.death = True
        pygame.time.set_timer(self.death_event, 10000)


    def draw(self):
        self.image = self.sprite_fright if self._renderer.kokoro_active else self.sprite_normal
        super(Ghost, self).draw()
