import os
import random

import pygame

from Game.game_controllers.Pathfinder import Pathfinder
from Game.game_controllers.Translate_func import translate_screen_to_maze, translate_maze_to_screen
from Game.movable_obj.Ghost import Ghost


# Test
# [
#     "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
#     "WW          P SWWWWWWWWWWWWWWWW",
#     "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
# ],

class PacmanGameController:
    def __init__(self, levelId):
        """
               Initialize the PacmanGameController with the given level ID.

               Parameters:
               levelId (int): The ID of the level to be loaded.
        """
        self.ascii_maze = [
            [
                "WWWWWWWWW WWWWWWWWWWW WWWWWWWWW",
                "WW      S   P  W G         G WW",
                "WW WW WWW WWW WWW WWW WWW WW WW",
                "WW WW WWW WWW WWW WWW WWW WW WW",
                "WW    S                S     WW",
                "WW WWW WW WWWW W WWWW WW WWW WW",
                "WW     WW WWWW W WWWW WW     WW",
                "WW WWW WW WWWW W WWWW WW WWW WW",
                "WW                           WW",
                "WW WWW WWWWWWWCCCWWWWWWW WWW WW",
                "WW WWW WWWWWWWCCCWWWWWWW WWW WW",
                "WW WWW WWWWWWWCCCWWWWWWW WWW WW",
                "WW WWW WWWWWWWWWWWWWWWWW WWW WW",
                "        S                      ",
                "WW WW WWW WWW WWW WWW WWW WW WW",
                "WW WW WWW WWW WWW WWW WWW WW WW",
                "WW    S                S     WW",
                "WW WWW WW WWWW W WWWW WW WWW WW",
                "WW     WW WWWW W WWWW WW     WW",
                "WW WWW WW WWWW W WWWW WW WWW WW",
                "WW G                      G  WW",
                "WWWWWWWWW WWWWWWWWWWW WWWWWWWWW"
            ],
            [
                "WWWWWWWWWW WWWWWWWWWWW WWWWWWWWWW",
                "W       W       W       W    G  W",
                "W WW WW W WWWWW W WWWWW W WWWWW W",
                "WP                              W",
                "WWW W WWWWW W WWWWW W WWWWW W WWW",
                "WWW W   W   W   W   W   W  SW WWW",
                "    W W W WWWWW W WWWWW W WWW    ",
                "WWW W W  G  W       W         WWW",
                "WWW W W WWW W WCCCW W WWW WWW WWW",
                "W       W     WCCCW     W   W   W",
                "W WWW WWW WWW WCCCW WWW WWW W W W",
                "W  SW       W WWWWW W       W W W",
                "W W W WWWWW W WWWWW W WWWWW W W W",
                "W W W W   W W            W    W W",
                "  W     W     WWWWWWW W    W     ",
                "W   WWG   W S   W     W WWWW  W W",
                "W WWWW W WWWWWW W W WWW   S  WW W",
                "W      W          W W   WWW     W",
                "W WWWWWWWW WWWW WWW W WWW   WWW W",
                "W                         G     W",
                "WWWWWWWWWW WWWWWWWWWWW WWWWWWWWWW"
            ],
        ]

        self.numpy_maze = []
        self.hero_position = []
        self.cookie_spaces = []
        self.reachable_spaces = []
        self.cell_spaces = []
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
        self.size = (0, 0)
        self.convert_maze_to_numpy(levelId)
        self.p = Pathfinder(self.numpy_maze)

    def convert_maze_to_numpy(self, id):
        """
              Convert the ASCII maze to a numpy array for easier manipulation.

              Parameters:
              id (int): The ID of the level to be converted.
        """
        for x, row in enumerate(self.ascii_maze[id]):
            self.size = (len(row), x + 1)
            binary_row = []
            for y, column in enumerate(row):

                if column == "W":
                    binary_row.append(0)
                elif column == "C":
                    if len(self.cell_spaces) >= 3:
                        binary_row.append(1)
                    else:
                        binary_row.append(0)
                    self.cell_spaces.append((y, x))
                else:
                    binary_row.append(1)
                    self.cookie_spaces.append((y, x))
                    self.reachable_spaces.append((y, x))
                    if column == "S":
                        self.unstoppability_spaces.append((y, x))
                        self.reachable_spaces.append((y, x))
                    if column == "P":
                        self.hero_position.append((y, x))
                        self.reachable_spaces.append((y, x))
                    if column == "G":
                        self.ghost_spawns.append((y, x))
                        self.reachable_spaces.append((y, x))

            self.numpy_maze.append(binary_row)

    def request_new_random_path(self, in_ghost: Ghost):
        """
          Requests a new random path for the given ghost.

          Parameters:
          in_ghost (Ghost): The ghost for which a new path is to be generated.

          This method first selects a random reachable space in the maze. Then it translates the current position of the ghost
          from screen coordinates to maze coordinates. If the ghost is in a 'death' state, it selects a random cell space and
          calculates a path to that space. Otherwise, it calculates a path to the previously selected random reachable space.
          The path is then translated back to screen coordinates and set as the new path for the ghost.
        """
        random_space = random.choice(self.reachable_spaces)
        current_maze_coord = translate_screen_to_maze(in_ghost.position)
        if in_ghost.death:
            random_space_cell = random.choice(self.cell_spaces)
            path = self.p.path(current_maze_coord[1], current_maze_coord[0],
                               random_space_cell[1], random_space_cell[0])
        else:
            path = self.p.path(current_maze_coord[1], current_maze_coord[0],
                               random_space[1], random_space[0])
        test_path = [translate_maze_to_screen(item) for item in path]
        in_ghost.new_path(test_path)
