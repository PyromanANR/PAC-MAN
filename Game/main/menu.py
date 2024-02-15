import pygame
import sys
import os

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
        exit_button = Button(375, 500, 150, 50, 'Exit', (255, 255, 255), sys.exit, (170, 170, 170),
                             (100, 100, 100), self)
        levels_button = Button(375, 430, 150, 50, 'Start', (255, 255, 255), self.levels_menu, (170, 170, 170),
                               (100, 100, 100), self)
        self.create_menu("Menu", [exit_button, levels_button])

    def levels_menu(self):
        level2_button = Button(375, 500, 150, 50, 'Level 2', (255, 255, 255), lambda: setattr(self, 'levelId', 2),
                               (170, 170, 170), (100, 100, 100), self, '..\..\images\level1.png')
        level1_button = Button(375, 430, 150, 50, 'Level 1', (255, 255, 255), lambda: setattr(self, 'levelId', 1),
                               (170, 170, 170), (100, 100, 100), self, '..\..\images\level1.png')
        back_button = Button(50, 50, 150, 50, 'Back', (255, 255, 255), self.main_menu, (170, 170, 170),
                             (100, 100, 100), self)
        self.create_menu("Choose a level", [level1_button, level2_button, back_button])


class Button:
    def __init__(self, x, y, width, height, text, text_color, function, color_light, color_dark, menu, image_path=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.text_color = text_color
        self.function = function
        self.color_light = color_light
        self.color_dark = color_dark
        self.current_color = self.color_dark
        self.font = pygame.font.SysFont('Corbel', 35)
        self.image_path = image_path
        self.menu: Menu = menu

    def draw(self, screen, mouse):
        if self.x <= mouse[0] <= self.x + self.width and self.y <= mouse[1] <= self.y + self.height:
            self.current_color = self.color_light
        else:
            self.current_color = self.color_dark

        pygame.draw.rect(screen, self.current_color, [self.x, self.y, self.width, self.height])

        text = self.font.render(self.text, True, self.text_color)
        screen.blit(text, (
            self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def draw_with_images(self, screen, mouse):
        if self.x <= mouse[0] <= self.x + self.width and self.y <= mouse[1] <= self.y + self.height:
            self.current_color = self.color_light
            image = pygame.image.load(self.image_path)  # Завантажте малюнок
            screen.blit(image, (100, 200))
        else:
            self.current_color = self.color_dark

        pygame.draw.rect(screen, self.current_color, [self.x, self.y, self.width, self.height])

        text = self.font.render(self.text, True, self.text_color)
        screen.blit(text, (
            self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.x <= event.pos[0] <= self.x + self.width and self.y <= event.pos[1] <= self.y + self.height:
                self.function()
