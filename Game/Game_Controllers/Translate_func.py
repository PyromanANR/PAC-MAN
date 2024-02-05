unified_size = 32
# General functions for coordinate conversion
def translate_screen_to_maze(in_coords, in_size = unified_size):
    return int(in_coords[0] / in_size), int(in_coords[1] / in_size)

def translate_maze_to_screen(in_coords, in_size = unified_size):
    return in_coords[0] * in_size, in_coords[1] * in_size