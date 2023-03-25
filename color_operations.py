'''This module contains a few functions for doing some color transformations.'''

def lighten_color(color, factor = 3.25):
    """" Lightens a hex color (format #FFFFFF) by a factor """
    new_color = '#'
    for val in color[1:]:
        val = int( max(2, min(int(val, 16) * factor, 14)) )
        new_color += f"{val:x}"
    return new_color


def get_contrasting_text_color(bg_color):
    """ Choses either black or white color that will contrast the given color """
    color = "#FFF"
    if int(bg_color[1:], 16) > int("666666", 16):
        color = "#000"
    return color
