import pygame
from Game.game_controllers.Direction import Direction
from Game.game_controllers.ScoreType import ScoreType
from Game.movable_obj.MovableObject import MovableObject


class PacMan(MovableObject):
    def __init__(self, in_surface, x, y, in_size: int):
        super().__init__(in_surface, x, y, in_size, (255, 255, 0), False)
        self.last_non_colliding_position = (0, 0)
        self.open = pygame.image.load("..\..\images\paku.png")
        self.closed = pygame.image.load("..\..\images\man.png")
        self.image = self.open
        self.mouth_open = True


    def tick(self):
        """
        Updates the state of the object for each tick of the game loop.

        Usage:
        - This method is used to update the state of the object for each tick of the game loop.
        - It handles teleportation from one edge of the screen to the other.
        - It checks for collisions in the buffered direction and moves the object accordingly.
        - If a collision with a wall occurs after moving, it reverts the object's position to the last non-colliding position.
        - It also handles cookie pickup and interactions with ghosts.

        Returns:
        - None
        """

        # TELEPORT(Start to end screen)
        if self.x < 0:
            self.x = self._renderer._width

        if self.y < 0:
            self.y = self._renderer._height - 100

        if self.x > self._renderer._width:
            self.x = 0

        if self.y > self._renderer._height - 100:
            self.y = 0

        self.last_non_colliding_position = self.position

        if self.check_collision_in_direction(self.direction_buffer)[0]:
            self.automatic_move(self.current_direction)
        else:
            self.automatic_move(self.direction_buffer)
            self.current_direction = self.direction_buffer

        if self.collides_with_wall((self.x, self.y)):
            self.position = self.last_non_colliding_position

        self.handle_cookie_pickup()
        self.handle_ghosts()

    def automatic_move(self, in_direction: Direction):
        """
        Automatically moves the object in a given direction if there is no collision.

        Parameters:
        - in_direction (Direction): The direction in which to move the object.

        Usage:
        - This method is used to automatically move the object in a given direction.
        - It checks for a collision in the given direction.
        - If there is no collision, it updates the object's position to the desired position.
        - If there is a collision, it changes the current direction to the last working direction.

        Returns:
        - None
        """

        collision_result = self.check_collision_in_direction(in_direction)
        desired_position_collides = collision_result[0]
        if not desired_position_collides:
            self.last_working_direction = self.current_direction
            desired_position = collision_result[1]
            self.position = desired_position
        else:
            self.current_direction = self.last_working_direction

    def draw(self):
        """
        Draws the object on the screen.

        Usage:
        - This method is used to draw the object on the screen.
        - It selects the appropriate image based on whether the object's mouth is open or closed.
        - It rotates the image based on the object's current direction.
        - It then calls the parent class's draw method to draw the object on the screen.

        Returns:
        - None
        """

        self.image = self.open if self.mouth_open else self.closed
        self.image = pygame.transform.rotate(self.image, self.current_direction.value)
        super(PacMan, self).draw()

    def handle_cookie_pickup(self):
        """
        Handles the pickup of cookies and power-ups in the game.

        Usage:
        - This method is used to handle the pickup of cookies and power-ups in the game.
        - It checks for collisions between the object and cookies or power-ups.
        - If a collision with a cookie occurs, it removes the cookie from the game objects, adds to the score, and removes the cookie from the list of cookies.
        - If all cookies are picked up, it sets the game as won.
        - If a collision with a power-up occurs and the power-up is not already active, it removes the power-up from the game objects, adds to the score, and activates the power-up.

        Returns:
        - None
        """

        collision_rect = pygame.Rect(self.x, self.y, self._size, self._size)
        cookies = self._renderer.cookie
        powerups = self._renderer.unstoppability
        game_objects = self._renderer.game_object
        cookie_to_remove = None
        for cookie in cookies:
            collides = collision_rect.colliderect(cookie.shape)
            if collides and cookie in game_objects:
                game_objects.remove(cookie)
                self._renderer.add_score(ScoreType.COOKIE)
                cookie_to_remove = cookie

        if cookie_to_remove is not None:
            cookies.remove(cookie_to_remove)

        if len(self._renderer.cookie) == 0:
            self._renderer.won = True

        for powerup in powerups:
            collides = collision_rect.colliderect(powerup.shape)
            if collides and powerup in game_objects:
                if not self._renderer.kokoro_active:
                    game_objects.remove(powerup)
                    self._renderer.add_score(ScoreType.POWERUP)
                    self._renderer.activate_kokoro()

    def handle_ghosts(self):
        """
        Handles interactions with ghosts in the game.

        Usage:
        - This method is used to handle interactions with ghosts in the game.
        - It checks for collisions between the object and ghosts.
        - If a collision with a ghost occurs and the power-up is active, it removes the ghost from the game objects, and adds to the score.
        - If a collision with a ghost occurs and the power-up is not active, and the game is not won, it kills Pacman.

        Returns:
        - None
        """

        collision_rect = pygame.Rect(self.x, self.y, self._size, self._size)
        ghosts = self._renderer.ghost
        game_objects = self._renderer.game_object
        for ghost in ghosts:
            collides = collision_rect.colliderect(ghost.shape)
            if collides and ghost in game_objects:
                if self._renderer.kokoro_active:
                    game_objects.remove(ghost)
                    self._renderer.add_score(ScoreType.GHOST)
                else:
                    if not self._renderer.won:
                        self._renderer.kill_pacman()


