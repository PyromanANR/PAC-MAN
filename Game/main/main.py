from Game.game_controllers.Game import GameRenderer
from Game.game_controllers.PacmanGameController import PacmanGameController
from Game.game_controllers.Translate_func import translate_maze_to_screen, unified_size
from Game.movable_obj.Ghost import Ghost
from Game.movable_obj.PacMan import PacMan
from Game.not_movable_obj.Cookie import Cookie
from Game.not_movable_obj.Unstoppability import Unstoppability
from Game.not_movable_obj.Wall import Wall
from Game.main.menu import Menu

if __name__ == "__main__":
    menu = Menu()
    menu.main_menu()
    print
    pacman_game = PacmanGameController()
    size = pacman_game.size
    actual_size = translate_maze_to_screen(size)
    game_renderer = GameRenderer(actual_size[0], actual_size[1])

    for y, row in enumerate(pacman_game.numpy_maze):
        for x, column in enumerate(row):
            if column == 0:
                game_renderer.wall = Wall(game_renderer, x, y, unified_size)


    for cookie_space in pacman_game.cookie_spaces:
        translated = translate_maze_to_screen(cookie_space)
        cookie = Cookie(game_renderer, translated[0] + unified_size / 2, translated[1] + unified_size / 2)
        game_renderer.cookie = cookie

    for unstoppability_space in pacman_game.unstoppability_spaces:
        translated = translate_maze_to_screen(unstoppability_space)
        unstop = Unstoppability(game_renderer, translated[0] + unified_size / 2, translated[1] + unified_size / 2)
        game_renderer.unstoppability = unstop

    for i, ghost_spawn in enumerate(pacman_game.ghost_spawns):
        translated = translate_maze_to_screen(ghost_spawn)
        ghost = Ghost(game_renderer, translated[0], translated[1], unified_size, pacman_game,
                      pacman_game.ghost_colors[i % 4], pacman_game.ghost_sprite_fright)
        game_renderer.add_game_object(ghost)

    translated = translate_maze_to_screen(pacman_game.hero_position[0])
    pacman = PacMan(game_renderer,  translated[0],  translated[1], unified_size, pacman_game.pac_man_image)
    game_renderer.hero = pacman
    game_renderer.tick(120)
