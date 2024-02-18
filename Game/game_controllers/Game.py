from enum import Enum
import pygame
from Game.game_controllers.Direction import Direction
from Game.main.button import Button
from Game.main.menu import Menu


class GhostBehaviour(Enum):
    PEACEFUL = 1
    AGGRESSIVE = 2


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
        self._menu: Menu = Menu()
        self._button: Button = Button(375, 430, 150, 50, 'Go back', (255, 255, 255),
                                      lambda: setattr(self, '_done', True), (147, 196, 125),
                                      (0, 0, 0))
        self._game_objects = []
        self._walls = []
        self._cookies = []
        self._unstoppability = []
        self._hero = None
        self._current_mode = GhostBehaviour.PEACEFUL
        self._mode_switch = pygame.USEREVENT + 1

    def tick(self, in_fps: int):
        black = (0, 0, 0)

        pygame.time.set_timer(self._mode_switch, 10000)  # 10c
        while not self.done:
            self._screen.fill(black)

            for game_object in self._game_objects:
                game_object.tick()
                game_object.draw()

            mouse = pygame.mouse.get_pos()
            self._button.draw(self._screen, mouse)
            pygame.display.flip()
            self._clock.tick(in_fps)
            self._handle_events()

        print("Game over")
        self._menu.levels_menu()
        self.restart_game()

    def restart_game(self):
        from Game.main.initialization import Initialization
        game = Initialization(self._menu.levelId)
        game.create_game()

    def add_game_object(self, obj: GameObject):
        self._game_objects.append(obj)

    @property
    def done(self) -> bool:
        return self._done

    @done.setter
    def done(self, value: bool):
        self._done = value

    @property
    def current_mode(self):
        return self._current_mode

    @current_mode.setter
    def current_mode(self, value):
        self._current_mode = value

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
                self.done = True

            if event.type == self._mode_switch:
                self.handle_mode_switch()
                
            self._button.click(event)

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]:
            self._hero.direction = Direction.UP
        elif pressed[pygame.K_LEFT]:
            self._hero.direction = Direction.LEFT
        elif pressed[pygame.K_DOWN]:
            self._hero.direction = Direction.DOWN
        elif pressed[pygame.K_RIGHT]:
            self._hero.direction = Direction.RIGHT

    def handle_mode_switch(self):
        if self.current_mode == GhostBehaviour.PEACEFUL:
            self.current_mode = GhostBehaviour.AGGRESSIVE
        elif self.current_mode == GhostBehaviour.AGGRESSIVE:
            self.current_mode = GhostBehaviour.PEACEFUL
        print(f"Current mode: {str(self.current_mode)}")
