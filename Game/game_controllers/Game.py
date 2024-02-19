import pygame
from Game.game_controllers.Direction import Direction


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

    @property
    def shape(self):
        self._shape = pygame.Rect(self.x, self.y, self._size, self._size)
        return self._shape

    @property
    def position(self):
        return (self.x, self.y)

    @position.setter
    def position(self, value):
        self.x, self.y = value


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
        self._unstoppability = []
        self._hero = None

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

    @property
    def walls(self):
        return self._walls

    @walls.setter
    def wall(self, obj):
        self.add_game_object(obj)
        self._walls.append(obj)

    @property
    def cookie(self):
        return self._cookies

    @cookie.setter
    def cookie(self, obj: GameObject):
        self._game_objects.append(obj)
        self._cookies.append(obj)

    @property
    def unstoppability(self):
        return self._unstoppability

    @unstoppability.setter
    def unstoppability(self, obj: GameObject):
        self._game_objects.append(obj)
        self._unstoppability.append(obj)

    @property
    def hero(self):
        return self._hero

    @hero.setter
    def hero(self, in_hero):
        self.add_game_object(in_hero)
        self._hero = in_hero

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._done = True

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]:
            self._hero.direction = Direction.UP
        elif pressed[pygame.K_LEFT]:
            self._hero.direction = Direction.LEFT
        elif pressed[pygame.K_DOWN]:
            self._hero.direction = Direction.DOWN
        elif pressed[pygame.K_RIGHT]:
            self._hero.direction = Direction.RIGHT
