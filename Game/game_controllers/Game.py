from enum import Enum
import pygame
from Game.game_controllers.Direction import Direction
from Game.game_controllers.ScoreType import ScoreType
from Game.game_controllers.GhostBehaviour import GhostBehaviour
from Game.game_controllers.Translate_func import translate_maze_to_screen
from Game.main.button import Button
from Game.main.menu import Menu
import os


class GameObject:
    def __init__(self, in_surface, x, y,
                 in_size: int, in_color=(255, 0, 0),
                 is_circle: bool = False):
        """
              Initialize the GameObject with the given parameters.

              Parameters:
              in_surface (GameRenderer): The surface on which the game object will be rendered.
              x (int): The x-coordinate of the game object.
              y (int): The y-coordinate of the game object.
              in_size (int): The size of the game object.
              in_color (tuple): The color of the game object. Default is red (255, 0, 0).
              is_circle (bool): A flag indicating whether the game object is a circle. Default is False.
        """
        self._size = in_size
        self._renderer: GameRenderer = in_surface
        self._surface = in_surface._screen
        self.y = y
        self.x = x
        self._color = in_color
        self._circle = is_circle
        self._shape = pygame.Rect(self.x, self.y, in_size, in_size)

        self._size = in_size
        self._renderer: GameRenderer = in_surface
        self._surface = in_surface._screen
        self.y = y
        self.x = x
        self._color = in_color
        self._circle = is_circle
        self._shape = pygame.Rect(self.x, self.y, in_size, in_size)

    def draw(self):
        """
             Draw the game object on the surface. If the game object is a circle, draw a circle. Otherwise, draw a rectangle.
        """
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
        """
               This method is called every frame. Override this method to add custom behavior.
        """
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
    def __init__(self, in_width: int, in_height: int, background_color='black', difficulty=1, devmode=False):
        """
             Initialize the GameRenderer with the given parameters.

             Parameters:
             in_width (int): The width of the game screen.
             in_height (int): The height of the game screen.
             background_color (str): The color of the game screen. Default is 'black'.
             difficulty (int): The difficulty level of the game. Default is 1.
             devmode (bool): A flag indicating whether the game is in development mode. Default is False.
        """
        pygame.init()
        self._width = in_width
        self._height = in_height
        self._screen = pygame.display.set_mode((in_width, in_height))
        pygame.display.set_caption('Pacman')
        self._screen_color = background_color
        self._difficulty = difficulty
        self._devmode = devmode
        self._clock = pygame.time.Clock()
        self._rest_time = 1
        self._done = False
        self._won = False
        self._menu: Menu = Menu()
        self._button: Button = Button(self._width - 165, self._height - 65, 150, 50, 'Go back', (0, 0, 0),
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
        self._current_phase = 0

    def tick(self, in_fps: int):
        """
             This method is called every frame. It handles the game logic and updates the game state.

             Parameters:
             in_fps (int): The frames per second at which the game runs.
        """
        self.handle_mode_switch()
        pygame.time.set_timer(self._pakupaku_event, 200)
        while not self.done:
            for game_object in self._game_objects:
                game_object.tick()
                game_object.draw()

            for i in range(self._lives):
                self._screen.blit(pygame.transform.scale(pygame.image.load(os.path.join("..", "..", "images", "lives.png")), (30, 30)),
                                  (320 + i * 40, self._height - 55))
            self.display_text(f"Score: {self._score} Lives: ", in_position=(15, self._height - 72), in_size=45)
            if self._hero is None: self.display_text("YOU DIED", (255, 0, 0),
                                                     (self._width / 2 - 200, self._height / 2 - 100), 100)
            if self.won: self.display_text("YOU WON", (0, 153, 0), (self._width / 2 - 200, self._height / 2 - 100), 100)
            dt = self._clock.tick(in_fps)
            self._rest_time -= dt
            if self.devmode: self.display_text(f"GhostBehaviour Time: {self._rest_time}", (0, 153, 0), in_position=(480, self._height - 55), in_size=25)
            mouse = pygame.mouse.get_pos()
            self._button.draw(self._screen, mouse)
            pygame.display.flip()
            self._screen.fill(self._screen_color)
            self._handle_events()

        print("Game over")
        self._menu.levels_menu()
        self.restart_game()

    def display_text(self, text, color=(255, 255, 255), in_position=(32, 0), in_size=30, ):
        """
              Display the given text on the game screen at the given position.

              Parameters:
              text (str): The text to be displayed.
              color (tuple): The color of the text. Default is white (255, 255, 255).
              in_position (tuple): The position at which the text is displayed. Default is (32, 0).
              in_size (int): The size of the text. Default is 30.
        """
        font = pygame.font.SysFont('DejaVuSans', in_size)
        text_surface = font.render(text, False, color)
        self._screen.blit(text_surface, in_position)

    def restart_game(self):
        """
               Restart the game by creating a new game instance.
        """
        from Game.main.initialization import Initialization
        game = Initialization(self._menu.levelId)
        game.create_game()

    @property
    def devmode(self):
        return self._devmode

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
        """
          Activates the 'kokoro' mode in the game and starts its timeout.
        """
        self._kokoro_active = True
        self._current_mode = GhostBehaviour.PEACEFUL
        print(f"Current mode: {str(self.current_mode)}")
        self.start_kokoro_timeout()

    def start_kokoro_timeout(self):
        """
        Starts a timer for the 'kokoro' mode which lasts for 10 seconds.
        """
        pygame.time.set_timer(self._kokoro_end_event, 10000)  # 10s

    def kill_pacman(self):
        """
        Decreases the lives of the pacman by 1. If the lives reach 0, the game ends.
        """
        self._lives -= 1
        translated = translate_maze_to_screen(self._hero.game_controller.hero_position[0])
        self._hero.position = (translated[0], translated[1])
        self._hero.direction = Direction.NONE
        self._current_mode = GhostBehaviour.PEACEFUL
        print(f"Current mode: {str(self.current_mode)}")
        if self._lives == 0: self.end_game()

    def end_game(self):
        """
        Ends the game by removing the hero from the game objects and setting it to None.
        """
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
        """
        Returns the position of the hero. If the hero is None, it returns (0, 0).
        """
        return self._hero.position if self._hero is not None else (0, 0)

    def _handle_events(self):
        """
        Handles all the events in the game such as quitting the game, switching modes, ending 'kokoro' mode,
        opening and closing the pacman's mouth, and the death of a ghost.
        """
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

            else:
                for ghost in self._ghost:
                    if event.type == ghost.death_event:
                        pygame.time.set_timer(ghost.death_event, 0)
                        ghost.death = False
                        ghost.location_queue.clear()
                        position = (
                            ghost.game_controller.cell_spaces[4][0] - 3, ghost.game_controller.cell_spaces[4][1] - 2)
                        translated = translate_maze_to_screen(position)
                        ghost.position = (translated[0], translated[1])

            self._button.click(event)
            self.handle_move_switch()

    def handle_move_switch(self):
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
        """
        Handles the switching of modes between 'PEACEFUL' and 'AGGRESSIVE'. The time for each mode is set here.
        """
        if self.current_mode == GhostBehaviour.PEACEFUL and not self.kokoro_active:
            self.current_mode = GhostBehaviour.AGGRESSIVE
        else:
            self.current_mode = GhostBehaviour.PEACEFUL
        used_timing = 8 if self.current_mode == GhostBehaviour.PEACEFUL else 20
        time = 1000 * used_timing if self.current_mode == GhostBehaviour.PEACEFUL else 1000 * used_timing * self._difficulty
        self._rest_time = time
        pygame.time.set_timer(self._mode_switch, time)
        print(f"Current mode: {str(self.current_mode)}")

    def add_score(self, in_score: ScoreType):
        """
        Adds the given score to the total score.

        Parameters:
        in_score (ScoreType): The score to be added.
        """
        self._score += in_score.value

