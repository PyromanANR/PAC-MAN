import argparse

from Game.game_controllers.Game import GameRenderer
from Game.game_controllers.PacmanGameController import PacmanGameController
from Game.game_controllers.Translate_func import translate_maze_to_screen, unified_size
from Game.movable_obj.Ghost import Ghost
from Game.movable_obj.ghosts.Blinky import Blinky
from Game.movable_obj.ghosts.Clyde import Clyde
from Game.movable_obj.ghosts.Inky import Inky
from Game.movable_obj.ghosts.Pinky import Pinky
from Game.movable_obj.PacMan import PacMan
from Game.not_movable_obj.Cell import Cell
from Game.not_movable_obj.Cookie import Cookie
from Game.not_movable_obj.Unstoppability import Unstoppability
from Game.not_movable_obj.Wall import Wall

# color - black, white
# difficulty - 1, 2
# dev - True, False
#--difficulty 1 --background black --dev
parser = argparse.ArgumentParser(description='Програма для зміни налаштувань гри')
parser.add_argument('--difficulty', type=int, help='Рівень складності гри')
parser.add_argument('--background', type=str, help='Колір фону гри')
parser.add_argument('--dev', action='store_true', help='Інструменти розробника')
args = parser.parse_args()

class Initialization:
    def __init__(self, levelId):
        self.levelId = levelId

    def create_game(self):
        """
        Initializes and starts the Pacman game.

        Usage:
        - This method is used to initialize and start the Pacman game.
        - It creates a new PacmanGameController with the current level ID.
        - It translates the maze size to screen coordinates and creates a GameRenderer.
        - It creates walls, cookies, unstoppability power-ups, cells, ghosts, and the hero (Pacman) based on the game state.
        - It starts the game loop by calling the tick method on the GameRenderer.

        Returns:
        - None
        """
        print(f'Рівень складності: {args.difficulty}')
        print(f'Колір фону: {args.background}')
        pacman_game = PacmanGameController(self.levelId)
        size = pacman_game.size
        actual_size = translate_maze_to_screen(size)
        game_renderer = GameRenderer(actual_size[0], actual_size[1]+80, args.background, args.difficulty, args.dev)

        for y, row in enumerate(pacman_game.numpy_maze):
            for x, column in enumerate(row):
                if column == 0 and (x, y) not in pacman_game.cell_spaces:
                    game_renderer.wall = Wall(game_renderer, x, y, unified_size)

        for cookie_space in pacman_game.cookie_spaces:
            translated = translate_maze_to_screen(cookie_space)
            cookie = Cookie(game_renderer, translated[0] + unified_size / 2, translated[1] + unified_size / 2)
            game_renderer.cookie = cookie

        for unstoppability_space in pacman_game.unstoppability_spaces:
            translated = translate_maze_to_screen(unstoppability_space)
            unstop = Unstoppability(game_renderer, translated[0] + unified_size / 2, translated[1] + unified_size / 2)
            game_renderer.unstoppability = unstop

        for cell_spaces in pacman_game.cell_spaces:
            translated = translate_maze_to_screen(cell_spaces)
            cell = Cell(game_renderer, translated[0], translated[1], unified_size)
            game_renderer.cell = cell

        ghost_classes = {0: Blinky, 1: Pinky, 2: Clyde, 3: Inky}

        for i, ghost_spawn in enumerate(pacman_game.ghost_spawns):
            translated = translate_maze_to_screen(ghost_spawn)
            if i in ghost_classes:
                ghost = ghost_classes[i](game_renderer, translated[0], translated[1], unified_size, pacman_game,
                                         pacman_game.ghost_colors[i % 4], pacman_game.ghost_sprite_fright)
                game_renderer.ghost = ghost

        translated = translate_maze_to_screen(pacman_game.hero_position[0])
        pacman = PacMan(game_renderer, translated[0], translated[1], unified_size, pacman_game)
        game_renderer.hero = pacman
        game_renderer.tick(120)
