import tcod
import numpy as np
class Pathfinder:
    """
        A class used to find the shortest path in a maze using the A* algorithm.
    """
    def __init__(self, in_arr):
        """
         Initialize the Pathfinder with the given 2D array.

         Parameters:
         in_arr (2D array): The 2D array representing the maze. 1s represent reachable spaces and 0s represent walls.
        """
        cost = np.array(in_arr, dtype=np.bool_).tolist()
        self.pf = tcod.path.AStar(cost=cost, diagonal=0)

    def path(self, from_x, from_y, to_x, to_y) -> object:
        """
        Find the shortest path from the start coordinates to the end coordinates.

        Parameters:
        from_x (int): The x-coordinate of the start position.
        from_y (int): The y-coordinate of the start position.
        to_x (int): The x-coordinate of the end position.
        to_y (int): The y-coordinate of the end position.

        Returns:
        list: A list of tuples representing the path from the start position to the end position.
        """
        res = self.pf.get_path(from_x, from_y, to_x, to_y)
        return [(sub[1], sub[0]) for sub in res]