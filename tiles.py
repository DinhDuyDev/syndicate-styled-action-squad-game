import pygame

# Sprites
def get_tiles(pth="tiles_mapping.dtl") -> dict[int,pygame.Surface]:
    if not pygame.display.get_init():
        return {}
    else:
        return_dict = dict()
        with open("tiles_mapping.dtl", 'r') as f:
            ls = [row.strip() for row in f]
            for s in ls:
                key, val = int(s.split(":")[0]), str((s.split(":")[1])).strip()
                return_dict[key] = pygame.image.load(val).convert()
        return return_dict