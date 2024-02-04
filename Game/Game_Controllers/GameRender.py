import pygame
from Game.MovableObject import PacMan
import GameObject
from Game.Object_not_movable.Objnotmove import Wall


class GameRenderer:
    def __init__(self, in_width: int, in_height: int):
        pygame.init()
        self._width = in_width
        self._height = in_height
        self._screen = pygame.display.set_mode((in_width, in_height))
        pygame.display.set_caption('Pacman')
        self._clock = pygame.time.Clock()
        self._done = False
        self._game_objects = []
        self._walls = []
        self._cookies = []
        self._hero: PacMan = None

    def tick(self, in_fps: int):
        black = (0, 0, 0)
        while not self._done:
            for game_object in self._game_objects:
                game_object.tick()
                game_object.draw()

            pygame.display.flip()
            self._clock.tick(in_fps)
            self._screen.fill(black)
            self._handle_events()

        print("Game over")

    def add_game_object(self, obj: GameObject):
        self._game_objects.append(obj)

    def add_wall(self, obj: Wall):
        self.add_game_object(obj)
        self._walls.append(obj)

    def _handle_events(self):
        None