def lighten_color(color, factor = 3.25):
        new_color = '#'
        for val in color[1:]:
            val = int( max(2, min(int(val, 16) * factor, 14)) )
            new_color += f"{val:x}"
        return new_color


def get_contrasting_text(bg):
    color = "#FFF"
    if int(bg[1:], 16) > int("666666", 16):
        color = "#000"
    return color