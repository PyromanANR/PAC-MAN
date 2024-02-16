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
        exit_button = Button(375, 500, 150, 50, 'Exit', (255, 255, 255), sys.exit, (204, 0, 0),
                             (0, 0, 0))
        levels_button = Button(375, 430, 150, 50, 'Start', (255, 255, 255), self.levels_menu, (147, 196, 125),
                               (0, 0, 0))
        self.create_menu("Menu", [exit_button, levels_button])

    def levels_menu(self):
        level2_button = Button(375, 500, 150, 50, 'Level 2', (255, 255, 255), lambda: setattr(self, 'levelId', 1),
                               (170, 170, 170), (0, 0, 0), '..\..\images\level2.png')
        level1_button = Button(375, 430, 150, 50, 'Level 1', (255, 255, 255), lambda: setattr(self, 'levelId', 0),
                               (170, 170, 170), (0, 0, 0), '..\..\images\level1.png')
        back_button = Button(15, 15, 40, 40, '<-', (255, 255, 255), self.main_menu, (170, 170, 170),
                             (0, 0, 0))
        self.create_menu("Choose a level", [level1_button, level2_button, back_button])



