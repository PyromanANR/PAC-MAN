from Game.main.menu import Menu
from Game.main.initialization import Initialization

if __name__ == "__main__":
    menu = Menu()
    menu.main_menu()
    game = Initialization(menu.levelId)
    game.create_game()


