from Game.Game_Controllers.Game import GameRenderer
from Game.Game_Controllers.PacmanGameController import PacmanGameController
from Game.Game_Controllers.Translate_func import translate_maze_to_screen, unified_size
from Game.MovableObj.Ghost import Ghost
from Game.MovableObj.PacMan import PacMan
from Game.NotMovableObj.Cookie import Cookie
from Game.NotMovableObj.Unstoppability import Unstoppability
from Game.NotMovableObj.Wall import Wall


if __name__ == "__main__":
    pacman_game = PacmanGameController()
    size = pacman_game.size
    actual_size = translate_maze_to_screen(size)
    game_renderer = GameRenderer(actual_size[0], actual_size[1])

    for y, row in enumerate(pacman_game.numpy_maze):
        for x, column in enumerate(row):
            if column == 0:
                game_renderer.add_wall(Wall(game_renderer, x, y, unified_size))


    for cookie_space in pacman_game.cookie_spaces:
        translated = translate_maze_to_screen(cookie_space)
        cookie = Cookie(game_renderer, translated[0] + unified_size / 2, translated[1] + unified_size / 2)
        game_renderer.add_cookie(cookie)

    for unstoppability_space in pacman_game.unstoppability_spaces:
        translated = translate_maze_to_screen(unstoppability_space)
        Unstop = Unstoppability(game_renderer, translated[0] + unified_size / 2, translated[1] + unified_size / 2)
        game_renderer.add_unstoppability(Unstop)

    for i, ghost_spawn in enumerate(pacman_game.ghost_spawns):
        translated = translate_maze_to_screen(ghost_spawn)
        ghost = Ghost(game_renderer, translated[0], translated[1], unified_size, pacman_game,
                      pacman_game.ghost_colors[i % 4])
        game_renderer.add_game_object(ghost)

    translated = translate_maze_to_screen(pacman_game.hero_position[0])
    pacman = PacMan(game_renderer,  translated[0],  translated[1], unified_size)
    game_renderer.add_hero(pacman)
    game_renderer.tick(120)
