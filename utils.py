import pygame

def create_triangle_surface(size, color, direction):
    width, height = size
    surface = pygame.Surface(size, pygame.SRCALPHA)
    points = []  # Initialize points to an empty list
    if direction == "up":
        points = [(width // 2, 0), (0, height), (width, height)]
    elif direction == "down":
        points = [(0, 0), (width, 0), (width // 2, height)]
    elif direction == "left":
        points = [(width, 0), (width, height), (0, height // 2)]
    elif direction == "right":
        points = [(0, 0), (0, height), (width, height // 2)]
    pygame.draw.polygon(surface, color, points)
    return surface

def format_time(milliseconds):
    seconds = milliseconds // 1000
    minutes = seconds // 60
    hours = minutes // 60
    milliseconds = milliseconds % 1000
    seconds = seconds % 60
    minutes = minutes % 60
    return f"{hours:02}:{minutes:02}:{seconds:02}.{milliseconds:03}"
