import pygame

class Button:
    def __init__(self, x, y, width, height, text, text_color, function, color_light, color_dark, image_path=None):
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
            screen.blit(image, (205, 50))
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