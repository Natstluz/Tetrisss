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


def color_select_menu(screen, selected_color):
    menu_font = pygame.font.Font(None, 40)
    color_options = list(COLORS_PRESETS.keys())
    selected_index = color_options.index(selected_color)

    while True:
        screen.fill((0, 0, 0))
        draw_text(screen, "Select Color Theme", 40, WIDTH // 2, 100, (255, 255, 255))

        for i, option in enumerate(color_options):
            text = menu_font.render(option, True, (255, 255, 255) if i != selected_index else (255, 255, 0))
            text_rect = text.get_rect(center=(WIDTH // 2, 180 + i * 50))
            screen.blit(text, text_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_index = (selected_index - 1) % len(color_options)
                elif event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % len(color_options)
                elif event.key == pygame.K_RETURN:
                    return color_options[selected_index]
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for i, option in enumerate(color_options):
                    text = menu_font.render(option, True, (255, 255, 255) if i != selected_index else (255, 255, 0))
                    text_rect = text.get_rect(center=(WIDTH // 2, 180 + i * 50))
                    if text_rect.collidepoint(mouse_pos):
                        return color_options[i]


# Меню выбора фона
def background_select_menu(screen, selected_background):
    menu_font = pygame.font.Font(None, 40)
    background_options = list(BACKGROUNDS.keys())
    selected_index = background_options.index(selected_background)

    while True:
        screen.fill((0, 0, 0))
        draw_text(screen, "Select Background", 40, WIDTH // 2, 100, (255, 255, 255))

        for i, option in enumerate(background_options):
            text = menu_font.render(option, True, (255, 255, 255) if i != selected_index else (255, 255, 0))
            text_rect = text.get_rect(center=(WIDTH // 2, 180 + i * 50))
            screen.blit(text, text_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_index = (selected_index - 1) % len(background_options)
                elif event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % len(background_options)
                elif event.key == pygame.K_RETURN:
                    return background_options[selected_index]
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for i, option in enumerate(background_options):
                    text = menu_font.render(option, True, (255, 255, 255) if i != selected_index else (255, 255, 0))
                    text_rect = text.get_rect(center=(WIDTH // 2, 180 + i * 50))
                    if text_rect.collidepoint(mouse_pos):
                        return background_options[i]
                    

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


def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    pygame.display.set_caption("Tetris")

    clock = pygame.time.Clock()

    global CURRENT_COLORS, CURRENT_BACKGROUND

    selected_colors = 'Classic'
    selected_background = 'None'

    while True:
        main_menu(screen, selected_colors, selected_background)

        game_grid = [[None] * GRID_WIDTH for _ in range(GRID_HEIGHT)]

        score = 0
        level = 1

        drop_speed = calculate_speed(level)

        drop_timer = 0

        current_tetromino = get_next_tetromino()
        next_tetromino = get_next_tetromino()
        game_active = True

        while game_active:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        current_tetromino.move(-1, 0)

                        if check_collision(current_tetromino, game_grid):
                            current_tetromino.move(1, 0)

                    elif event.key == pygame.K_RIGHT:
                        current_tetromino.move(1, 0)

                        if check_collision(current_tetromino, game_grid):
                            current_tetromino.move(-1, 0)

                    elif event.key == pygame.K_DOWN:
                        current_tetromino.move(0, 1)

                        if check_collision(current_tetromino, game_grid):
                            current_tetromino.move(0, -1)

                            lock_tetromino(current_tetromino, game_grid)
                            current_tetromino = next_tetromino

                            next_tetromino = get_next_tetromino()
                            score += clear_lines(game_grid) * 100 * level

                            level = calculate_level(score)
                            drop_speed = calculate_speed(level)

                    elif event.key == pygame.K_UP:
                        current_tetromino.rotate()

                        if check_collision(current_tetromino, game_grid):
                            for i in range(4):
                                current_tetromino.rotate()

            drop_timer += clock.tick(FPS)
            if drop_timer >= 1000 / drop_speed:
                drop_timer = 0
                current_tetromino.move(0, 1)

                if check_collision(current_tetromino, game_grid):
                    current_tetromino.move(0, -1)

                    lock_tetromino(current_tetromino, game_grid)
                    current_tetromino = next_tetromino

                    next_tetromino = get_next_tetromino()
                    score += clear_lines(game_grid) * 100 * level

                    level = calculate_level(score)
                    drop_speed = calculate_speed(level)

                    if check_collision(current_tetromino, game_grid):
                        game_active = False
                        break

            if CURRENT_BACKGROUND:
                screen.blit(pygame.transform.scale(CURRENT_BACKGROUND, (WIDTH, HEIGHT)), (0, 0))

            else:
                screen.fill(CURRENT_COLORS['BACKGROUND'])
            draw_grid(screen)
            draw_game_grid(screen, game_grid)

            current_tetromino.draw(screen)
            draw_next_tetromino(screen, next_tetromino)

            draw_text(screen, f"Score: {score}", 25, 720, 180, (255, 255, 255))
            draw_text(screen, f"Level: {level}", 25, 720, 220, (255, 255, 255))

            pygame.display.flip()

        if game_over(screen, score):
            continue
        else:
            break


if __name__ == "__main__":
    main()
