from Game.game_controllers.Translate_func import translate_screen_to_maze
from Game.movable_obj.Ghost import Ghost


class Inky(Ghost):
    def __init__(self, in_surface, x, y, in_size, in_game_controller, sprite_path, sprite_fright):
        super().__init__(in_surface, x, y, in_size, in_game_controller, sprite_path, sprite_fright)

    def mirror_position_relative_to_pacman(self, pacman_position, blinky_position):
        maze = self.game_controller.numpy_maze
        x_p, y_p = pacman_position
        x_b, y_b = blinky_position

        new_x = 2 * x_p - x_b
        new_y = 2 * y_p - y_b

        if 0 <= new_x < len(maze[0]) and 0 <= new_y < len(maze):
            if maze[new_y][new_x] == 1:
                return new_x, new_y
            else:
                for distance in range(1, 10):
                    for dy in range(-distance, distance + 1):
                        for dx in range(-distance, distance + 1):
                            if abs(dx) + abs(dy) == distance:
                                next_x, next_y = new_x + dx, new_y + dy
                                if 0 <= next_x < len(maze[0]) and 0 <= next_y < len(maze):
                                    if maze[next_y][next_x] == 1:
                                        return next_x, next_y
        return x_p, y_p

    def find_target_position(self):
        blinky = self._renderer.ghost[0]
        blinky_position = translate_screen_to_maze(blinky.position)
        player_position = translate_screen_to_maze(self._renderer.hero_position())
        new_inky_position = self.mirror_position_relative_to_pacman(player_position, blinky_position)
        return new_inky_position
