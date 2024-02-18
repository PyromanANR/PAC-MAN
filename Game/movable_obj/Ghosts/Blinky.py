from Game.game_controllers.Direction import Direction
from Game.game_controllers.GhostBehaviour import GhostBehaviour
from Game.movable_obj.Ghost import Ghost
from Game.game_controllers.Translate_func import translate_screen_to_maze, translate_maze_to_screen


class Blinky(Ghost):
    def __init__(self, in_surface, x, y, in_size, in_game_controller, sprite_path, sprite_fright):
        super().__init__(in_surface, x, y, in_size, in_game_controller, sprite_path, sprite_fright)
        self.path_built = False

    def calculate_direction_to_next_target(self) -> Direction:
        if self._renderer.current_mode == GhostBehaviour.AGGRESSIVE and not self.path_built:
            self.location_queue.clear()
            self.path_built = True
            self.request_path_to_player()
        if self._renderer.current_mode == GhostBehaviour.AGGRESSIVE and self.next_target is None:
            self.request_path_to_player()
        if self._renderer.current_mode == GhostBehaviour.PEACEFUL:
            self.path_built = False
        return super(Blinky, self).calculate_direction_to_next_target()

    def request_path_to_player(self):
        player_position = translate_screen_to_maze(self._renderer.hero_position())
        current_maze_coord = translate_screen_to_maze(self.position)
        path = self.game_controller.p.path(current_maze_coord[1], current_maze_coord[0],
                                           player_position[1], player_position[0])

        new_path = [translate_maze_to_screen(item) for item in path]
        self.new_path(new_path)
