
class PacmanGameController:
    def __init__(self):
        self.ascii_maze = [
            "WWWWWWWWWWWWWWWWWWWWWWWWWWWW",
            "W P           W G        G W",
            "WWWWW WWWWWWWWWWWWWWWW WWWWW",
            "WWWWW WWWWWWWWWWWWWWWW WWWWW",
            "W       G    G             W",
            "WWWWWWWWWWWWWWWWWWWWWWWWWWWW",
        ]

        self.numpy_maze = []
        self.cookie_spaces = []
        self.reachable_spaces = []
        self.ghost_spawns = []
        self.ghost_colors = [
            (255, 0, 0),
            (255, 184, 255),
            (0, 255, 255),
            (255, 184, 82)
        ]

        self.size = (0, 0)
        self.convert_maze_to_numpy()

    def convert_maze_to_numpy(self):
        for x, row in enumerate(self.ascii_maze):
            self.size = (len(row), x + 1)
            binary_row = []
            for y, column in enumerate(row):
                if column == "G":
                    self.ghost_spawns.append((y, x))

                if column == "W":
                    binary_row.append(0)
                else:
                    binary_row.append(1)
                    self.cookie_spaces.append((y, x))
                    self.reachable_spaces.append((y, x))
            self.numpy_maze.append(binary_row)