import pygame
import settings
import screen
import camera
import utilityfuncs
from pathlib import Path

pygame.init()
pygame.font.init()

# Screen setup
game_screen = screen.Screen(settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT)
draw_dest = game_screen.screen.copy()
running = True
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 10)

# Level Setup
LEVEL_WIDTH = settings.hor_cells
LEVEL_HEIGHT = settings.ver_cells
c_dimensions = settings.cell_dimension

level = []
def setup_level(lv, width, height):
    for i in range(height):
        row = []
        for j in range(width):
            row.append(0)
        lv.append(row)
setup_level(level, LEVEL_WIDTH, LEVEL_HEIGHT)

# Sprites
LEVEL_TILES = {
    1 : pygame.image.load("sprites/level_tiles/normal_brick.png").convert_alpha(),
    2 : pygame.image.load("sprites/level_tiles/dirty_brick.png").convert_alpha(),
    3 : pygame.image.load("sprites/level_tiles/NO_ACCESS.png").convert_alpha()
}
current_sprite = 1

# Tools
TOOLS = {
    "Pencil" : pygame.image.load("sprites/Level Editor/pencil.png").convert_alpha(),
    "Bucket": pygame.image.load("sprites/Level Editor/bucket.png").convert_alpha()
}
tool_mode = "Pencil"

# Camera
CameraView = camera.Camera()
CameraView.frames = 3

# Running
while running:
    # Mouse and Camera coordinates
    c_x, c_y = CameraView.get_pos()
    c_x = int(c_x)
    c_y = int(c_y)
    mx, my = utilityfuncs.mouse_xy_transformation(draw_dest, game_screen.screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

    # Camera action
    CameraView.action()

    # Clearing the screen
    draw_dest.fill((0, 0, 0))

    _x = c_x * settings.cell_dimension
    _y = c_y * settings.cell_dimension
    w = 32

    # Drawing level grid
    for i in range(LEVEL_HEIGHT//2):
        for j in range(LEVEL_WIDTH//2):
            pygame.draw.line(draw_dest, (75, 75, 75), (j * c_dimensions, i * c_dimensions)
                             , (j * c_dimensions + c_dimensions, i * c_dimensions))
            pygame.draw.line(draw_dest, (75, 75, 75), (j * c_dimensions, i * c_dimensions)
                             , (j * c_dimensions, i * c_dimensions + c_dimensions))
            if level[i][j] != 0:
                # pygame.draw.rect(draw_dest, (75, 75, 75), (j * c_dimensions-_x, i * c_dimensions-_y, c_dimensions, c_dimensions))
                curr_tile = LEVEL_TILES[current_sprite]
                draw_dest.blit(curr_tile, curr_tile.get_rect(topleft=(j*c_dimensions, i*c_dimensions)))

    # Drawing the center
    pygame.draw.line(draw_dest, (255, 0, 0), (settings.WINDOW_WIDTH - w - _x - 1, settings.WINDOW_HEIGHT - _y - 1),
                     (settings.WINDOW_WIDTH + w - _x - 1, settings.WINDOW_HEIGHT - _y - 1), 2)
    pygame.draw.line(draw_dest, (255, 0, 0), (settings.WINDOW_WIDTH - _x - 1, settings.WINDOW_HEIGHT - w - _y - 1),
                     (settings.WINDOW_WIDTH - _x - 1, settings.WINDOW_HEIGHT + w - _y - 1), 2)


    # Level Drawing
    _x, _y = int(mx / settings.cell_dimension), int(my / settings.cell_dimension)
    # Performance and Tools
    if pygame.key.get_pressed()[pygame.K_TAB]:
        pygame.draw.rect(draw_dest, (255, 0, 0), (0, 0, 32, 4))
        pygame.draw.rect(draw_dest, (0, 255, 0), (0, 0, 32 * (clock.get_fps() / 60), 4))

        x = 0
        for tool_name, image in TOOLS.items():
            draw_dest.blit(image, image.get_rect(topleft=(x * 16, 0)))
            x += 1

        SW = settings.WINDOW_WIDTH
        for index, tile in LEVEL_TILES.items():
            tile_rect = tile.get_rect(center=(SW - 16, (index + 1) * 16))
            draw_dest.blit(tile, tile_rect)

    else:
        if tool_mode == "Pencil":
            if pygame.mouse.get_pressed()[0]:
                level[_y][_x] = 1
            elif pygame.mouse.get_pressed()[2]:
                level[_y][_x] = 0
        elif tool_mode == "Bucket":
            if pygame.mouse.get_pressed()[0]:


    # Rendering on game
    game_screen.screen.blit(pygame.transform.scale(draw_dest, (game_screen.get_dimensions())), (0, 0))
    pygame.display.flip()
    clock.tick(60)