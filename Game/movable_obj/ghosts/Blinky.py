from Game.movable_obj.Ghost import Ghost
from Game.game_controllers.Translate_func import translate_screen_to_maze


class Blinky(Ghost):
    def __init__(self, in_surface, x, y, in_size, in_game_controller, sprite_path, sprite_fright):
        super().__init__(in_surface, x, y, in_size, in_game_controller, sprite_path, sprite_fright)

    def find_target_position(self):
        return translate_screen_to_maze(self._renderer.hero_position())
