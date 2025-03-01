import pygame
import random

pygame.init()

WIDTH = 800
HEIGHT = 600

GRID_SIZE = 25
GRID_WIDTH = 10
GRID_HEIGHT = 20

PLAY_AREA_X = 50
PLAY_AREA_Y = 50

BORDER_WIDTH = 2

FPS = 30

COLORS_PRESETS = {
    'Classic': {
        'I': (0, 255, 255), 'J': (0, 0, 255), 'L': (255, 165, 0),
        'O': (255, 255, 0), 'S': (0, 255, 0), 'T': (128, 0, 128),
        'Z': (255, 0, 0), 'BORDER': (128, 128, 128), 'BACKGROUND': (0, 0, 0), 'GRID': (50, 50, 50)
    },
    'Pastel': {
        'I': (173, 216, 230), 'J': (135, 206, 250), 'L': (255, 228, 181),
        'O': (255, 255, 224), 'S': (152, 251, 152), 'T': (221, 160, 221),
        'Z': (240, 128, 128), 'BORDER': (192, 192, 192), 'BACKGROUND': (245, 245, 245), 'GRID': (220, 220, 220)
    },
    'Dark': {
        'I': (0, 150, 150), 'J': (0, 0, 150), 'L': (150, 100, 0),
        'O': (150, 150, 0), 'S': (0, 150, 0), 'T': (80, 0, 80),
        'Z': (150, 0, 0), 'BORDER': (70, 70, 70), 'BACKGROUND': (20, 20, 20), 'GRID': (40, 40, 40)
    }
}

BACKGROUNDS = {
    'None': None,
    'Stars': pygame.image.load("stars.jpg") if pygame.image.load("stars.jpg") else None,
    'City': pygame.image.load("city.jpg") if pygame.image.load("city.jpg") else None
}

SHAPES = {
    'I': [[1, 1, 1, 1]],
    'J': [[1, 0, 0], [1, 1, 1]],
    'L': [[0, 0, 1], [1, 1, 1]],
    'O': [[1, 1], [1, 1]],
    'S': [[0, 1, 1], [1, 1, 0]],
    'T': [[0, 1, 0], [1, 1, 1]],
    'Z': [[1, 1, 0], [0, 1, 1]]
}

