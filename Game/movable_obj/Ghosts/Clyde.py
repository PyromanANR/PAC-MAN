from Game.game_controllers.Direction import Direction
from Game.game_controllers.GhostBehaviour import GhostBehaviour
from Game.game_controllers.Translate_func import translate_screen_to_maze, translate_maze_to_screen
from Game.movable_obj.Ghost import Ghost


class Clyde(Ghost):
    def __init__(self, in_surface, x, y, in_size, in_game_controller, sprite_path, sprite_fright):
        super().__init__(in_surface, x, y, in_size, in_game_controller, sprite_path, sprite_fright)

    def find_position_outside_radius(self, character_position, current_maze_coord):
        maze = self.game_controller.numpy_maze
        radius = 8

        for dx in range(-radius, len(maze[0])):
            for dy in range(-radius, len(maze)):
                new_x, new_y = character_position[0] + dx, character_position[1] + dy
                if 0 <= new_x < len(maze[0]) and 0 <= new_y < len(maze):
                    if maze[new_y][new_x] == 1:
                        return new_x, new_y

        return current_maze_coord

    def request_path_to_player(self):
        player_position = translate_screen_to_maze(self._renderer.hero_position())
        current_maze_coord = translate_screen_to_maze(self.position)
        new_clyde_position = self.find_position_outside_radius(player_position, current_maze_coord)
        path = self.game_controller.p.path(current_maze_coord[1], current_maze_coord[0],
                                           new_clyde_position[1], new_clyde_position[0])

        new_path = [translate_maze_to_screen(item) for item in path]
        self.new_path(new_path)
