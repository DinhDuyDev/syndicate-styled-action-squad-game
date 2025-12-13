import pygame
import ALL_SPRITES

# Sprites
def get_tiles(pth="tiles_mapping.dtl") -> dict[int,pygame.Surface]:
    if not pygame.display.get_init():
        return {}
    else:
        all_tiles = ["EMPTY", "NORMAL_BRICK", "DIRTY_BRICK", "NO_ACCESS", "CONCRETE", "SHINY_BRICK"]
        ind = 0
        return_dict = dict()
        for tile_name in all_tiles:
            return_dict[ind] = ALL_SPRITES.ASP[tile_name]
            ind += 1
        return return_dict