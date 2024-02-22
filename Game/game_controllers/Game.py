from enum import Enum
import pygame
from Game.game_controllers.Direction import Direction
from Game.game_controllers.ScoreType import ScoreType
from Game.game_controllers.GhostBehaviour import GhostBehaviour
from Game.main.button import Button
from Game.main.menu import Menu


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
        self._won = False
        self._menu: Menu = Menu()
        self._button: Button = Button(self._width-165, self._height-65, 150, 50, 'Go back', (0, 0, 0),
                                      lambda: setattr(self, '_done', True), (170, 170, 170),
                                      (255, 255, 255))
        self._game_objects = []
        self._walls = []
        self._cells = []
        self._cookies = []
        self._unstoppability = []
        self._ghost = []
        self._hero = None
        self._lives = 3
        self._score = 0
        self._kokoro_active = False
        self._current_mode = GhostBehaviour.AGGRESSIVE
        self._mode_switch = pygame.USEREVENT + 1
        self._kokoro_end_event = pygame.USEREVENT + 2
        self._pakupaku_event = pygame.USEREVENT + 3
        self._modes = [
            (7, 20),
            (7, 20),
            (5, 20),
            (5, 999999)  # 'infinite' chase seconds
        ]
        self._current_phase = 0

    def tick(self, in_fps: int):
        black = (0, 0, 0)
        self.handle_mode_switch()
        pygame.time.set_timer(self._pakupaku_event, 200)
        while not self.done:
            for game_object in self._game_objects:
                game_object.tick()
                game_object.draw()
            for i in range(self._lives):
                self._screen.blit(pygame.transform.scale(pygame.image.load("..\..\images\lives.png"), (30, 30)), (340 + i * 40, self._height-55))
            self.display_text(f"Score: {self._score}    Lives: ", in_position=(15, self._height-72), in_size=45)

            if self._hero is None: self.display_text("YOU DIED", (255, 0, 0),(self._width / 2 - 200, self._height / 2-100), 100)
            if self.won: self.display_text("YOU WON", (0, 153, 0), (self._width / 2 - 200, self._height / 2-100), 100)
            mouse = pygame.mouse.get_pos()
            self._button.draw(self._screen, mouse)
            pygame.display.flip()
            self._clock.tick(in_fps)
            self._screen.fill(black)
            self._handle_events()

        print("Game over")
        self._menu.levels_menu()
        self.restart_game()

    def display_text(self, text, color=(255, 255, 255), in_position=(32, 0), in_size=30, ):
        font = pygame.font.SysFont('DejaVuSans', in_size)
        text_surface = font.render(text, False, color)
        self._screen.blit(text_surface, in_position)


    def restart_game(self):
        from Game.main.initialization import Initialization
        game = Initialization(self._menu.levelId)
        game.create_game()

    @property
    def game_object(self):
        return self._game_objects

    @game_object.setter
    def game_object(self, obj: GameObject):
        self._game_objects.append(obj)

    @property
    def kokoro_active(self) -> bool:
        return self._kokoro_active

    @kokoro_active.setter
    def kokoro_active(self, value: bool):
        self._kokoro_active = value

    def activate_kokoro(self):
        self._kokoro_active = True
        self._current_mode = GhostBehaviour.PEACEFUL
        self.start_kokoro_timeout()

    def start_kokoro_timeout(self):
        pygame.time.set_timer(self._kokoro_end_event, 15000) #15s

    def kill_pacman(self):
        self._lives -= 1
        self._hero.position = (60, 30)
        self._hero.direction = Direction.NONE
        self._current_mode = GhostBehaviour.PEACEFUL
        if self._lives == 0: self.end_game()

    def end_game(self):
        if self._hero in self._game_objects:
            self._game_objects.remove(self._hero)
        self._hero = None

    @property
    def done(self) -> bool:
        return self._done

    @done.setter
    def done(self, value: bool):
        self._done = value

    @property
    def won(self):
        return self._won

    @won.setter
    def won(self, value):
        self._won = value

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
        self.game_object = obj
        self._walls.append(obj)

    @property
    def cell(self):
        return self._cells

    @cell.setter
    def cell(self, obj):
        self.game_object = obj
        self._cells.append(obj)

    @property
    def ghost(self):
        return self._ghost

    @ghost.setter
    def ghost(self, obj):
        self.game_object = obj
        self._ghost.append(obj)

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
        self.game_object = in_hero
        self._hero = in_hero

    def hero_position(self):
        return self._hero.position if self._hero is not None else (0, 0)

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True

            if event.type == self._mode_switch:
                self.handle_mode_switch()

            if event.type == self._kokoro_end_event:
                self._kokoro_active = False

            if event.type == self._pakupaku_event:
                if self._hero is None: break
                self._hero.mouth_open = not self._hero.mouth_open

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
        else:
            self.current_mode = GhostBehaviour.PEACEFUL
        used_timing = 8 if self.current_mode == GhostBehaviour.PEACEFUL else 20
        pygame.time.set_timer(self._mode_switch, 1000 * used_timing)
        print(f"Current mode: {str(self.current_mode)}")

    def add_score(self, in_score: ScoreType):
        self._score += in_score.value
