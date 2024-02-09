class PacmanGameController:
    def __init__(self):
        self.ascii_maze = [
            "WWWWWWWWWWWWWWWWWWWWWWWWWWWW",
            "W      S   P  W G        G W",
            "WWWWW WWWWWWWWWWWWWWWW WWWWW",
            "WWWWW WWWWWWWWWWWWWWWW WWWWW",
            "W    S  G    G        S    W",
            "WWWWWWWWWWWWWWWWWWWWWWWWWWWW",
        ]

        self.numpy_maze = []
        self.hero_position = []
        self.cookie_spaces = []
        self.reachable_spaces = []
        self.unstoppability_spaces = []
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
                if column == "P":
                    self.hero_position.append((y, x))

                if column == "G":
                    self.ghost_spawns.append((y, x))

                if column == "W":
                    binary_row.append(0)
                else:
                    binary_row.append(1)
                    self.cookie_spaces.append((y, x))
                    self.reachable_spaces.append((y, x))
                    if column == "S":
                        self.unstoppability_spaces.append((y, x))

            self.numpy_maze.append(binary_row)
