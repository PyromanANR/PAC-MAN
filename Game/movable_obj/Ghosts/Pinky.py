from Game.game_controllers.Direction import Direction
from Game.game_controllers.GhostBehaviour import GhostBehaviour
from Game.game_controllers.Translate_func import translate_screen_to_maze, translate_maze_to_screen
from Game.movable_obj.Ghost import Ghost


class Pinky(Ghost):
    def __init__(self, in_surface, x, y, in_size, in_game_controller, sprite_path, sprite_fright):
        super().__init__(in_surface, x, y, in_size, in_game_controller, sprite_path, sprite_fright)

    def calculate_direction_to_next_target(self) -> Direction:
        if self._renderer.current_mode == GhostBehaviour.AGGRESSIVE:
            if not self.path_built:
                self.location_queue.clear()
                self.path_built = True
                self.request_path_to_player()
            elif self.next_target is None:
                self.request_path_to_player()
        elif self._renderer.current_mode == GhostBehaviour.PEACEFUL:
            self.path_built = False
        return super(Pinky, self).calculate_direction_to_next_target()

    def find_position_relative_to_character(self, character_position):
        maze = self.game_controller.numpy_maze
        x, y = character_position

        # along radius 2
        for dx in range(-3, 4):
            for dy in range(-3, 4):
                if abs(dx) + abs(dy) == 2:
                    new_x, new_y = x + dx, y + dy
                    if 0 <= new_x < len(maze[0]) and 0 <= new_y < len(maze):
                        if maze[new_y][new_x] == 1:
                            return new_x, new_y

        return x, y

    def request_path_to_player(self):
        player_position = translate_screen_to_maze(self._renderer.hero_position())
        relative_position = self.find_position_relative_to_character(player_position)
        current_maze_coord = translate_screen_to_maze(self.position)
        path = self.game_controller.p.path(current_maze_coord[1], current_maze_coord[0],
                                           relative_position[1], relative_position[0])

        new_path = [translate_maze_to_screen(item) for item in path]
        self.new_path(new_path)
