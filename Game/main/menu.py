import pygame
import sys
pygame.init()


def levels_menu():
    pass

class Button:
    def __init__(self, x, y, width, height, text, text_color, function_id, color_light, color_dark):
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

    def draw(self, screen, mouse):
        if self.x <= mouse[0] <= self.x+self.width and self.y <= mouse[1] <= self.y+self.height:
            self.current_color = self.color_light
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
        if self.function_id == '1':
            pygame.quit()
            sys.exit()
        elif self.function_id == '2':
            levels_menu()




