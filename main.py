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

# Класс для представления отдельного блока
class Block:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x * GRID_SIZE + PLAY_AREA_X,
                                               self.y * GRID_SIZE + PLAY_AREA_Y,
                                               GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, CURRENT_COLORS['GRID'], (self.x * GRID_SIZE + PLAY_AREA_X,
                                                           self.y * GRID_SIZE + PLAY_AREA_Y,
                                                           GRID_SIZE, GRID_SIZE), 1)


# Класс для представления падающей фигуры тетриса
class Tetromino:
    def __init__(self, shape_type):
        self.shape_type = shape_type
        self.shape = SHAPES[shape_type]
        self.color = CURRENT_COLORS[shape_type]
        self.x = GRID_WIDTH // 2 - len(self.shape[0]) // 2
        self.y = 0
        self.rotation = 0
        self.blocks = self.get_blocks()

    def rotate(self):
        rotated_shape = list(zip(*reversed(self.shape)))

        if self.x + len(rotated_shape[0]) > GRID_WIDTH:
            self.x = GRID_WIDTH - len(rotated_shape[0])

        self.shape = [list(row) for row in rotated_shape]
        self.rotation = (self.rotation + 1) % 4
        self.blocks = self.get_blocks()

    def get_blocks(self):
        blocks = []
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    blocks.append(Block(self.x + x, self.y + y, self.color))
        return blocks

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        self.blocks = self.get_blocks()

    def draw(self, surface):
        for block in self.blocks:
            block.draw(surface)


def draw_grid(surface):
    pygame.draw.rect(surface, CURRENT_COLORS['BORDER'],
                     (PLAY_AREA_X - BORDER_WIDTH, PLAY_AREA_Y - BORDER_WIDTH,
                      GRID_WIDTH * GRID_SIZE + 2 * BORDER_WIDTH,
                      GRID_HEIGHT * GRID_SIZE + 2 * BORDER_WIDTH), BORDER_WIDTH)

    for x in range(GRID_WIDTH):

        for y in range(GRID_HEIGHT):
            pygame.draw.rect(surface, CURRENT_COLORS['GRID'],
                             (PLAY_AREA_X + x * GRID_SIZE, PLAY_AREA_Y + y * GRID_SIZE,
                              GRID_SIZE, GRID_SIZE), 1)


def draw_text(surface, text, size, x, y, color):
    font = pygame.font.Font(None, size)

    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)

    surface.blit(text_surface, text_rect)


def check_collision(tetromino, game_grid):
    for block in tetromino.blocks:

        x, y = block.x, block.y

        if x < 0 or x >= GRID_WIDTH or y >= GRID_HEIGHT or (y >= 0 and game_grid[y][x] is not None):
            return True

    return False


def lock_tetromino(tetromino, game_grid):
    for block in tetromino.blocks:
        game_grid[block.y][block.x] = block


def clear_lines(game_grid):
    lines_cleared = 0
    full_rows = []

    for y in range(GRID_HEIGHT):
        if all(cell is not None for cell in game_grid[y]):
            lines_cleared += 1
            full_rows.append(y)

    if lines_cleared > 0:
        for row in reversed(full_rows):
            del game_grid[row]
            game_grid.insert(0, [None] * GRID_WIDTH)

    return lines_cleared


def get_next_tetromino():
    shape_type = random.choice(list(SHAPES.keys()))
    return Tetromino(shape_type)


def draw_next_tetromino(surface, tetromino):
    draw_text(surface, "Next", 25, 720, 100, (255, 255, 255))

    for block in tetromino.blocks:
        x = block.x + 14
        y = block.y + 5

        pygame.draw.rect(surface, block.color, (x * GRID_SIZE + PLAY_AREA_X,
                                                y * GRID_SIZE + PLAY_AREA_Y,
                                                GRID_SIZE, GRID_SIZE))
    pygame.draw.rect(surface, CURRENT_COLORS['GRID'], (x * GRID_SIZE + PLAY_AREA_X,
                                                       y * GRID_SIZE + PLAY_AREA_Y,
                                                       GRID_SIZE, GRID_SIZE), 1)


def draw_game_grid(surface, game_grid):
    for y, row in enumerate(game_grid):

        for x, block in enumerate(row):

            if block:
                block.draw(surface)


def calculate_level(score):
    return min(score // 100 + 1, 10)


def calculate_speed(level):
    return min(1, FPS - (level - 1) * 2)


def game_over(surface, score):
    surface.fill(CURRENT_COLORS['BACKGROUND'])

    draw_text(surface, "Game Over", 60, WIDTH // 2, HEIGHT // 2 - 50, (255, 0, 0))
    draw_text(surface, f"Score: {score}", 40, WIDTH // 2, HEIGHT // 2 + 10, (255, 255, 255))
    draw_text(surface, "Press any key to restart", 30, WIDTH // 2, HEIGHT // 2 + 60, (200, 200, 200))

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                return True
    return False


def main_menu(screen, selected_colors, selected_background):
    global CURRENT_COLORS, CURRENT_BACKGROUND
    menu_font = pygame.font.Font(None, 40)

    menu_items = {
        "Start Game": (WIDTH // 2, 150),
        "Background": (WIDTH // 2, 250),
        "Color Theme": (WIDTH // 2, 350)
    }

    while True:
        screen.fill((0, 0, 0))

        for item, pos in menu_items.items():
            text = menu_font.render(item, True, (255, 255, 255))
            text_rect = text.get_rect(center=pos)
            screen.blit(text, text_rect)

        pygame.display.flip()
