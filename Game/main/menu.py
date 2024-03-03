import pygame
import sys
import os
from Game.main.button import Button

pygame.init()
class Menu:
    def __init__(self):
        self.level_Id = None
        self.running = True

    @property
    def levelId(self):
        return self.level_Id

    @levelId.setter
    def levelId(self, value):
        self.level_Id = value
        self.running = False
        pygame.quit()

    def create_menu(self, title, buttons):
        """
        Creates the main game menu with the given title and buttons.

        Parameters:
        - title (str): The title of the menu, displayed at the top of the screen.
        - buttons (List[Button]): A list of Button objects to be displayed on the screen.

        Usage:
        - This method is used to create the main game menu.
        - It displays the given title and set of buttons on the screen.
        - Each button can have its own image and click behavior.
        - The loop continues until the game is closed or another command is received.

        Returns:
        - None
        """

        WIDTH, HEIGHT = 900, 600
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(title)
        image_path = os.path.join('..', '..', 'images', 'background.jpg')
        main_background = pygame.image.load(image_path)

        while self.running:
            font = pygame.font.SysFont(None, 72)
            text_surface = font.render(title, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(WIDTH / 2, 80))

            screen.blit(main_background, (0, 0))
            screen.blit(text_surface, text_rect)

            mouse = pygame.mouse.get_pos()
            for button in buttons:
                if button.image_path != None:
                    button.draw_with_images(screen, mouse)
                else:
                    button.draw(screen, mouse)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()

                for button in buttons:
                    button.click(event)

            if self.running:
                pygame.display.update()

    def main_menu(self):
        """
        Creates the main menu of the game.

        Usage:
        - This method is used to create the main menu of the game.
        - It creates an 'Exit' button and a 'Start' button.
        - The 'Exit' button will close the game when clicked.
        - The 'Start' button will take the user to the levels menu when clicked.

        Returns:
        - None
        """

        exit_button = Button(375, 500, 150, 50, 'Exit', (255, 255, 255), sys.exit, (204, 0, 0),
                             (0, 0, 0))
        levels_button = Button(375, 430, 150, 50, 'Start', (255, 255, 255), self.levels_menu, (147, 196, 125),
                               (0, 0, 0))
        self.create_menu("Menu", [exit_button, levels_button])

    def levels_menu(self):
        """
        Creates the levels menu of the game.

        Usage:
        - This method is used to create the levels menu of the game.
        - It creates a 'Level 1' button, a 'Level 2' button, and a 'Back' button.
        - The 'Level 1' button will set the game's level to 1 when clicked.
        - The 'Level 2' button will set the game's level to 2 when clicked.
        - The 'Back' button will take the user back to the main menu when clicked.

        Returns:
        - None
        """

        level2_button = Button(375, 500, 150, 50, 'Level 2', (255, 255, 255), lambda: setattr(self, 'levelId', 1),
                               (170, 170, 170), (0, 0, 0), os.path.join('..', '..', 'images', 'level2.png'))
        level1_button = Button(375, 430, 150, 50, 'Level 1', (255, 255, 255), lambda: setattr(self, 'levelId', 0),
                               (170, 170, 170), (0, 0, 0), os.path.join('..', '..', 'images', 'level1.png'))
        back_button = Button(15, 15, 40, 40, '<-', (255, 255, 255), self.main_menu, (170, 170, 170),
                             (0, 0, 0))
        self.create_menu("Choose a level", [level1_button, level2_button, back_button])




