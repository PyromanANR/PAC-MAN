from Game.game_controllers.Translate_func import translate_screen_to_maze
from Game.movable_obj.Ghost import Ghost


class Pinky(Ghost):
    def __init__(self, in_surface, x, y, in_size, in_game_controller, sprite_path, sprite_fright):
        super().__init__(in_surface, x, y, in_size, in_game_controller, sprite_path, sprite_fright)

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

    def find_target_position(self):
        player_position = translate_screen_to_maze(self._renderer.hero_position())
        relative_position = self.find_position_relative_to_character(player_position)
        return relative_position

