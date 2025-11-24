# Sprite editor
from PIL import Image # pip3 install pillow
from pathlib import Path
import pygame
pygame.init()
pygame.font.init()
import screen
import settings
import utilityfuncs
import colors

# Screen setup
game_screen = screen.Screen(settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT)
draw_dest = game_screen.screen.copy()
running = True
clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 10)

# Sprite setup
hor_space = 320
ver_space = 320

class spr:
    sprite_dimensions = (16, 16)
    cell_size = hor_space / max(sprite_dimensions[0], sprite_dimensions[1])
    sprite_arr:list[list[tuple[int, int, int, int]]] = [[(0, 0, 0, 0) for x in range(16)] for y in range(16)]

# Color palette
palette_width = len(colors.colors[0])
palette_height = len(colors.colors)
colors_arr:list[list[tuple[int, int, int]]] = [[(0, 0, 0) for _x in range(palette_width)] for _y in range(palette_height)]
for i in range(palette_height):
    for j in range(palette_width):
        colors_arr[i][j] = colors.colors[i][j]

current_color = (75, 75, 75)

# Tools
sprite_tools = {
    "Pencil": pygame.image.load("sprites/Sprite_Editor/Tools/pencil.png"),
    "Line": pygame.image.load("sprites/Sprite_Editor/Tools/line.png"),
    "Bucket": pygame.image.load("sprites/Sprite_Editor/Tools/bucket.png"),
    "Select": pygame.image.load("sprites/Sprite_Editor/Tools/select.png"),
    "Eraser": pygame.image.load("sprites/Sprite_Editor/Tools/eraser.png"),
}
current_mode = "Pencil"

class select_tool:
    select_coordinates:list[tuple[int, int]] = []

    selected_data:list[list[tuple[int, int, int, int]]] = []

# Naming
using_commands = False
name = ""


########## SPRITE OPERATION

# Resize
def resize_sprite(width, height):
    spr.sprite_dimensions = (width, height)
    spr.cell_size = hor_space / max(spr.sprite_dimensions[0], spr.sprite_dimensions[1])
    spr.sprite_arr = [[(0, 0, 0, 0) for x in range(width)] for y in range(height)]

# Flip
def mirror_sprite():
    for i in range(spr.sprite_dimensions[1]):
        for j in range(spr.sprite_dimensions[0]//2):
            w = spr.sprite_dimensions[0]-1
            spr.sprite_arr[i][j], spr.sprite_arr[i][w-j] = spr.sprite_arr[i][w-j], spr.sprite_arr[i][j]

# Creating sprites
def generate_sprite(spr_arr:list[list[tuple[int, int, int, int]]], n):
    # Create a new image with RGB mode and specified dimensions
    result_image = Image.new('RGBA', spr.sprite_dimensions, color='red')

    for i in range(len(spr_arr)):
        for j in range(len(spr_arr[i])):
            result_image.putpixel((j, i), spr_arr[i][j])

    # Save the image as a PNG file - has to include png
    result_image.save(f'{n}')

# Loading Sprites
def load_sprite(pth:str):
    img_path = Path(pth)
    if img_path.exists():
        with Image.open(pth) as img:
            width, height = img.size
            resize_sprite(width, height)
            for y in range(height):
                for x in range(width):
                    spr.sprite_arr[y][x] = tuple(img.getpixel((x, y)))


while running:
    mx, my = utilityfuncs.mouse_xy_transformation(draw_dest, game_screen.screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                using_commands = not using_commands
            if using_commands:
                if event.key == pygame.K_RETURN:
                    if len(name) != 0: # Save or load functionality
                        n = name.split("=")
                        if len(n) == 1:
                            if n[0] in "new":
                                resize_sprite(spr.sprite_dimensions[0], spr.sprite_dimensions[1])
                            elif n[0] in "mirror":
                                mirror_sprite()
                        elif len(n) == 2:
                            if n[1].lower() in "save":
                                generate_sprite(spr.sprite_arr, n[0])
                            elif n[1].lower() in "load":
                                load_sprite(n[0])
                        elif len(n) == 3:
                            if n[2].lower() in "resize":
                                resize_sprite(int(n[0]), int(n[1]))

                elif event.key == pygame.K_BACKSPACE:
                    if pygame.key.get_pressed()[pygame.K_LSHIFT]:
                        name = ""
                    if len(name) != 0:
                        name = name[:len(name)-1]
                else:
                    if event.key != pygame.K_TAB:
                        name += event.unicode
    # Resetting image
    draw_dest.fill((0, 0, 0))

    # Pixel grid
    for i in range(len(spr.sprite_arr)):
        for j in range(len(spr.sprite_arr[0])):
            pygame.draw.line(draw_dest, (75, 75, 75),
                             (j * spr.cell_size, i * spr.cell_size),
                             (j * spr.cell_size + spr.cell_size, i * spr.cell_size))
            pygame.draw.line(draw_dest, (75, 75, 75),
                             (j * spr.cell_size, i * spr.cell_size),
                             (j * spr.cell_size, i * spr.cell_size + spr.cell_size))

            if spr.sprite_arr[i][j] != (0, 0, 0, 0):
                pygame.draw.rect(draw_dest, spr.sprite_arr[i][j], (j * spr.cell_size, i * spr.cell_size, spr.cell_size, spr.cell_size))
            else:
                if (i+j) % 2 == 0:
                    pygame.draw.rect(draw_dest, (25, 25, 25), (j * spr.cell_size+1, i * spr.cell_size+1, spr.cell_size-1, spr.cell_size-1))
                else:
                    pygame.draw.rect(draw_dest, (50, 50, 50), (j * spr.cell_size+1, i * spr.cell_size+1, spr.cell_size-1, spr.cell_size-1))

    pygame.draw.line(draw_dest, (75, 75, 75), (spr.sprite_dimensions[0] * spr.cell_size, 0),
                     (spr.sprite_dimensions[0] * spr.cell_size, spr.sprite_dimensions[1] * spr.cell_size))
    pygame.draw.line(draw_dest, (75, 75, 75), (0, spr.sprite_dimensions[1] * spr.cell_size),
                     (spr.sprite_dimensions[0] * spr.cell_size, spr.sprite_dimensions[1] * spr.cell_size))

    for i in range(len(colors_arr)):
        for j in range(len(colors_arr[0])):
            pygame.draw.rect(draw_dest, colors_arr[i][j], (settings.WINDOW_WIDTH-palette_width*16+j*16, i*16, 16, 16))

    # Drawing
    if 0 <= mx < spr.sprite_dimensions[0] * spr.cell_size and 0 <= my < spr.sprite_dimensions[1] * spr.cell_size:
        _x = int(mx / spr.cell_size)
        _y = int(my / spr.cell_size)

        if current_mode == "Pencil":
            if pygame.mouse.get_pressed()[0]:
                spr.sprite_arr[_y][_x] = current_color
            elif pygame.mouse.get_pressed()[2]:
                spr.sprite_arr[_y][_x] = (0, 0, 0, 0)

            cursor_x = int(mx / spr.cell_size) * spr.cell_size
            cursor_y = int(my / spr.cell_size) * spr.cell_size
            pygame.draw.rect(draw_dest, current_color, (cursor_x, cursor_y, spr.cell_size, spr.cell_size))

        elif current_mode == "Select":
            if pygame.mouse.get_pressed()[0]:
                if len(select_tool.select_coordinates) < 2:
                    # First coordinates
                    if (_x, _y) not in select_tool.select_coordinates:
                        select_tool.select_coordinates.append((_x, _y))
                    start_x, start_y = select_tool.select_coordinates[0]
                    pygame.draw.circle(draw_dest, (175, 0, 0), (start_x*spr.cell_size+spr.cell_size/2, start_y*spr.cell_size+spr.cell_size/2), 3)
                # else:
                elif len(select_tool.select_coordinates) == 2:
                    if select_tool.select_coordinates[0] < select_tool.select_coordinates[1]:
                        select_tool.select_coordinates.insert(0, select_tool.select_coordinates.pop(0))
            else:
                if len(select_tool.select_coordinates) == 2:
                    dist_x = select_tool.select_coordinates[1][0] - select_tool.select_coordinates[0][0] + 1
                    dist_y = select_tool.select_coordinates[1][1] - select_tool.select_coordinates[0][1] + 1
                    start_x, start_y = select_tool.select_coordinates[0]
                    pygame.draw.circle(draw_dest, (175, 0, 0), (start_x*spr.cell_size+spr.cell_size/2, start_y*spr.cell_size+spr.cell_size/2), 3)
                    pygame.draw.rect(draw_dest, (175, 0, 0), (start_x*spr.cell_size, start_y*spr.cell_size, dist_x*spr.cell_size, dist_y*spr.cell_size), width=1)

        elif current_mode == "Bucket":
            if pygame.mouse.get_pressed()[0]:
                utilityfuncs.flood_fill(_x, _y, spr.sprite_arr, current_color, spr.sprite_arr[_y][_x])

        elif current_mode == "Eraser":
            if pygame.mouse.get_pressed()[0]:
                resize_sprite(spr.sprite_dimensions[0], spr.sprite_dimensions[1])
        # elif current_mode == "Line":


    # Selecting Color
    elif settings.WINDOW_WIDTH-palette_width*16 <= mx < settings.WINDOW_WIDTH and 0 <= my < palette_height*16:
        dx = mx - (settings.WINDOW_WIDTH - palette_width*16)
        dy = my
        _x = int(dx / 16)
        _y = int(dy / 16)
        if pygame.mouse.get_pressed()[0]:
            current_color = colors_arr[_y][_x]

        cursor_x = int(mx / 16) * 16
        cursor_y = int(my / 16) * 16
        pygame.draw.rect(draw_dest, current_color, (cursor_x, cursor_y, 16, 16))

    # Outline for color palette
    pygame.draw.line(draw_dest, (75, 75, 75), (settings.WINDOW_WIDTH-palette_width*16, 0), (settings.WINDOW_WIDTH-palette_width*16, palette_height*16))
    pygame.draw.line(draw_dest, (75, 75, 75), (settings.WINDOW_WIDTH-palette_width*16, palette_height*16), (settings.WINDOW_WIDTH, palette_height*16))

    # Tools
    c = 0
    for tool_name, tool_sprite in sprite_tools.items():
        c += 1
        tx, ty = settings.WINDOW_WIDTH-16, settings.WINDOW_HEIGHT-16*c
        if tool_sprite.get_rect(topleft=(tx, ty)).collidepoint(mx, my):
            if pygame.mouse.get_pressed()[0]:
                pygame.draw.rect(draw_dest, (0, 255, 0), (tx, ty, 16, 16))
                current_mode = tool_name
                select_tool.select_coordinates.clear()
            else:
                pygame.draw.rect(draw_dest, (0, 255, 0), (tx, ty, 16, 16))
        draw_dest.blit(tool_sprite, tool_sprite.get_rect(topleft=(tx, ty)))

    draw_dest.blit(pygame.transform.scale_by(sprite_tools[current_mode], 1), sprite_tools[current_mode].get_rect(topleft=(mx+4, my-15)))

    # Commands
    y_name = 330
    text_col = (255, 255, 255)
    if not using_commands:
        text_col = (255, 0, 0)

    name_surf = font.render(f"> {name}<", False, text_col)
    name_rect = name_surf.get_rect(topleft=(80, y_name))
    draw_dest.blit(name_surf, name_rect)

    size_surf = font.render(str(spr.sprite_dimensions), False, (255, 255, 255))
    size_rect = size_surf.get_rect(topleft=(80, 340))
    draw_dest.blit(size_surf, size_rect)


    game_screen.screen.blit(pygame.transform.scale(draw_dest, (game_screen.get_dimensions())), (0, 0))
    pygame.display.flip()
    clock.tick(60)



