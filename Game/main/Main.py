from Game.Game_Controllers.Game import GameRenderer, Wall
from Game.Game_Controllers.PacmanGameController import PacmanGameController


if __name__ == "__main__":
    unified_size = 40
    pacman_game = PacmanGameController()
    size = pacman_game.size
    game_renderer = GameRenderer(size[0] * unified_size, size[1] * unified_size)

    for y, row in enumerate(pacman_game.numpy_maze):
        for x, column in enumerate(row):
            if column == 0:
                game_renderer.add_wall(Wall(game_renderer, x, y, unified_size))

    game_renderer.tick(120)
