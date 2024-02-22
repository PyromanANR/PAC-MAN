unified_size = 30
# General functions for coordinate conversion
def translate_screen_to_maze(in_coords, in_size = unified_size):
    """
    Translates screen coordinates to maze coordinates.

    Parameters:
    in_coords (tuple): The screen coordinates to be translated.
    in_size (int): The size of a single unit in the maze. Default is unified_size.

    Returns:
    tuple: The translated maze coordinates.
    """
    return int(in_coords[0] / in_size), int(in_coords[1] / in_size)

def translate_maze_to_screen(in_coords, in_size = unified_size):
    """
    Translates maze coordinates to screen coordinates.

    Parameters:
    in_coords (tuple): The maze coordinates to be translated.
    in_size (int): The size of a single unit in the maze. Default is unified_size.

    Returns:
    tuple: The translated screen coordinates.
    """
    return in_coords[0] * in_size, in_coords[1] * in_size