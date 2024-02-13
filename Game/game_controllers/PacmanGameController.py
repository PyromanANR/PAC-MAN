import os
import random

from Game.game_controllers.Pathfinder import Pathfinder
from Game.game_controllers.Translate_func import translate_screen_to_maze, translate_maze_to_screen
from Game.movable_obj.Ghost import Ghost


class PacmanGameController:
    def __init__(self):
        self.ascii_maze = [
            "WWWWWWWWW WWWWWWWWWWW WWWWWWWWW",
            "WW      S   P  W G         G WW",
            "WW WW WWW WWW WWW WWW WWW WW WW",
            "WW WW WWW WWW WWW WWW WWW WW WW",
            "WW    S                S     WW",
            "WW WWW WW WWWW W WWWW WW WWW WW",
            "WW     WW WWW  W  WWW WW     WW",
            "WW WWW WW WWW  W  WWW WW WWW WW",
            "WW                           WW",
            "WW WWW WWWWWWW   WWWWWWW WWW WW",
            "WW WWW WWWWWWW   WWWWWWW WWW WW",
            "WW WWW WWWWWWW   WWWWWWW WWW WW",
            "WW WWW WWWWWWW   WWWWWWW WWW WW",
            "        S                      ",
            "WW WW WWW WWW WWW WWW WWW WW WW",
            "WW WW WWW WWW WWW WWW WWW WW WW",
            "WW    S                S     WW",
            "WW WWW WW WWW  W  WWW WW WWW WW",
            "WW     WW WWW  W  WWW WW     WW",
            "WW WWW WW WWWW W WWWW WW WWW WW",
            "WW G                      G  WW",
            "WWWWWWWWW WWWWWWWWWWW WWWWWWWWW"
        ]

        self.numpy_maze = []
        self.hero_position = []
        self.cookie_spaces = []
        self.reachable_spaces = []
        self.unstoppability_spaces = []
        self.ghost_spawns = []
        self.ghost_colors = [
            (255, 0, 0),
            (255, 184, 255),
            (0, 255, 255),
            (255, 184, 82)
        ]
        self.ghost_colors = [
            os.path.join('..', '..', 'images', 'ghost.png'),
            os.path.join('..', '..', 'images', 'ghost_pink.png'),
            os.path.join('..', '..', 'images', 'ghost_orange.png'),
            os.path.join('..', '..', 'images', 'ghost_blue.png')
        ]
        self.ghost_sprite_fright = os.path.join('..', '..', 'images', 'ghost_fright.png')
        self.pac_man_image = os.path.join('..', '..', 'images', 'man.png')
        self.size = (0, 0)
        self.convert_maze_to_numpy()
        self.p = Pathfinder(self.numpy_maze)

    def convert_maze_to_numpy(self):
        for x, row in enumerate(self.ascii_maze):
            self.size = (len(row), x + 1)
            binary_row = []
            for y, column in enumerate(row):
                if column == "P":
                    self.hero_position.append((y, x))

                if column == "G":
                    self.ghost_spawns.append((y, x))

                if column == "W":
                    binary_row.append(0)
                else:
                    binary_row.append(1)
                    self.cookie_spaces.append((y, x))
                    self.reachable_spaces.append((y, x))
                    if column == "S":
                        self.unstoppability_spaces.append((y, x))

            self.numpy_maze.append(binary_row)

    def request_new_random_path(self, in_ghost: Ghost):
        random_space = random.choice(self.reachable_spaces)
        current_maze_coord = translate_screen_to_maze(in_ghost.position)

        path = self.p.path(current_maze_coord[1], current_maze_coord[0],
                              random_space[1], random_space[0])
        test_path = [translate_maze_to_screen(item) for item in path]
        in_ghost.new_path(test_path)
