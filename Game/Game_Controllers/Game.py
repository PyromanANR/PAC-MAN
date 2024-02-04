import pygame

class GameObject:
    def __init__(self, in_surface, x, y,
                 in_size: int, in_color=(255, 0, 0),
                 is_circle: bool = False):
        self._size = in_size
        self._renderer: GameRenderer = in_surface
        self._surface = in_surface._screen
        self.y = y
        self.x = x
        self._color = in_color
        self._circle = is_circle
        self._shape = pygame.Rect(self.x, self.y, in_size, in_size)

    def draw(self):
        if self._circle:
            pygame.draw.circle(self._surface,
                               self._color,
                               (self.x, self.y),
                               self._size)
        else:
            rect_object = pygame.Rect(self.x, self.y, self._size, self._size)
            pygame.draw.rect(self._surface,
                             self._color,
                             rect_object,
                             border_radius=4)

    def tick(self):
        pass


class Wall(GameObject):
    # Gray - in_color=(128, 128, 128)
    def __init__(self, in_surface, x, y, in_size: int, in_color=(128, 128, 128)):
        super().__init__(in_surface, x * in_size, y * in_size, in_size, in_color)


class Cookie(GameObject):
    def __init__(self):
        self


class Powerup(GameObject):
    def __init__(self):
        self


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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._done = True


class MovableObject(GameObject):
    def __init__(self):
        self


class PacMan(MovableObject):
    def __init__(self):
        self


class Ghost(MovableObject):
    def __init__(self):
        self