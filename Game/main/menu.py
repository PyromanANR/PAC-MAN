import pygame
import sys
import os
pygame.init()

class Menu:
    def __init__(self):
        self.level_Id = None

    @property
    def levelId(self): return self.level_Id;

    @levelId.setter
    def levelId(self, value): self.level_Id = value;

    def main_menu(self):
        WIDTH, HEIGHT = 900, 600
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Menu")
        image_path = os.path.join('..', '..', 'images', 'background.jpg')
        main_background = pygame.image.load(image_path)
        # Створення об'єкта кнопки
        exit_button = Button(375, 500, 150, 50, 'Exit', (255, 255, 255), '0', (170, 170, 170), (100, 100, 100), self)
        levels_button = Button(375, 430, 150, 50, 'Start', (255, 255, 255), '1', (170, 170, 170), (100, 100, 100), self)

        running = True
        while running:

            font = pygame.font.SysFont(None, 72)
            text_surface = font.render("MENU", True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(WIDTH / 2, 80))

            # Відображення зображення та тексту на фоні
            screen.blit(main_background, (0, 0))
            screen.blit(text_surface, text_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()

                exit_button.click(event)
                levels_button.click(event)

            if self.levelId != None:
                running = False
                pygame.quit()

            mouse = pygame.mouse.get_pos()
            # Відображення кнопки
            exit_button.draw(screen, mouse)
            levels_button.draw(screen, mouse)
            # Оновлення дисплея
            pygame.display.update()



    def levels_menu(self):
        WIDTH, HEIGHT = 900, 600
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Choose a level")
        image_path = os.path.join('..', '..', 'images', 'background.jpg')
        main_background = pygame.image.load(image_path)
        # Створення об'єкта кнопки
        level2_button = Button(375, 500, 150, 50, 'Level 2', (255, 255, 255), '3', (170, 170, 170), (100, 100, 100), self)
        level1_button = Button(375, 430, 150, 50, 'Level 1', (255, 255, 255), '2', (170, 170, 170), (100, 100, 100), self)

        running = True
        while running:

            font = pygame.font.SysFont(None, 72)
            text_surface = font.render("Choose a level", True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(WIDTH / 2, 80))

            # Відображення зображення та тексту на фоні
            screen.blit(main_background, (0, 0))
            screen.blit(text_surface, text_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()

                # Виклик методу click кнопки
                level1_button.click(event)
                level2_button.click(event)


            # Отримання позиції миші
            mouse = pygame.mouse.get_pos()

            # Відображення кнопки
            level1_button.draw_with_images(screen, mouse)
            level2_button.draw_with_images(screen, mouse)

            # Оновлення дисплея
            pygame.display.update()

            if self.levelId != None:
                running = False
                pygame.quit()

class Button:
    def __init__(self, x, y, width, height, text, text_color, function_id, color_light, color_dark, menu):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.text_color = text_color
        self.function_id = function_id
        self.color_light = color_light
        self.color_dark = color_dark
        self.current_color = self.color_dark
        self.font = pygame.font.SysFont('Corbel', 35)
        self.menu: Menu = menu

    def draw(self, screen, mouse):
        if self.x <= mouse[0] <= self.x+self.width and self.y <= mouse[1] <= self.y+self.height:
            self.current_color = self.color_light
        else:
            self.current_color = self.color_dark

        pygame.draw.rect(screen, self.current_color, [self.x, self.y, self.width, self.height])

        text = self.font.render(self.text, True, self.text_color)
        screen.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))


    def draw_with_images(self, screen, mouse):
        if self.x <= mouse[0] <= self.x+self.width and self.y <= mouse[1] <= self.y+self.height:
            self.current_color = self.color_light
            if self.current_color == '2':
                image_path = os.path.join('..', '..', 'images', 'level1.png')
            else:
                image_path = os.path.join('..', '..', 'images', 'level1.png')
            image = pygame.image.load(image_path)  # Завантажте малюнок
            screen.blit(image, (100, 200))
        else:
            self.current_color = self.color_dark

        pygame.draw.rect(screen, self.current_color, [self.x, self.y, self.width, self.height])

        text = self.font.render(self.text, True, self.text_color)
        screen.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.x <= event.pos[0] <= self.x+self.width and self.y <= event.pos[1] <= self.y+self.height:
                self.switch_function()

    def switch_function(self):

        if self.function_id == '0':
            pygame.quit()
            sys.exit()
        elif self.function_id == '1':
            self.menu.levels_menu()
        elif self.function_id == '2':
            self.menu.levelId = 1
        elif self.function_id == '3':
            self.menu.levelId = 2