import pygame

import Sprites
import deletor
import copy
import player_enemies # mainly acting against the players
import ALL_SPRITES

### CUTSCENES ELEMENTS ###
# MUST HAVE SUPPORT FOR: #

# COLLISION WITH TRIGGER CAUSES SOMETHING TO HAPPEN.
# MAKING SOUNDS OR DESTROYING SOMETHING CAUSES SOMETHING TO HAPPEN.
# CAN BE DESTROYED FOR SOMETHING ELSE
# CAN MAKE OTHER ENTITIES / OBJECTS.
# THIS SHIT WILL BE HARD. FUCK.

# WILL NEED A CUTSCENE EDITOR

# Triggers:
#   - XY COORDS
#   - SIZE
#   - ON_COLLIDE (WITH SOMEONE)

# Actors:
#   - XY coords and sprites
#   - Will follow a pre-determined path.
#   - END ACT: whether it's done looping through a sprite or done running away.

all_triggers = []
all_cutscene_elements = []
class CollideTrigger:
    def __init__(self, loc, id):
        self.x = loc[0]
        self.y = loc[1]
        self.width = 64
        self.height = 64
        self.repr_name = ""
        self.id = id
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        self.hitbox.center = (self.x, self.y)
        self.sprite = Sprites.Sprite(
            (
                "TRIGGER", "TRIGGER"
            )
        )
        # Adding reference
        all_triggers.append(self)
    def set_xy(self, loc:tuple[float, float]):
        self.x, self.y = loc[0], loc[1]
    def action(self):
        pass
    def render(self, dest:pygame.Surface, x, y):
        w, h = self.width, self.height
        pygame.draw.rect(dest, (255, 0, 255), (x - w / 2, y - h / 2, w, h))
        pygame.draw.rect(dest, (255, 255, 255), (x - w / 2, y - h / 2, w, h), width=2)

    def destroy(self):
        deletor.Deleter.request_delete(self, all_triggers)
    def __repr__(self):
        return f"{self.repr_name}->({self.x}, {self.y}, w={self.width}, h={self.height})"

class SpawnEnemyTrigger:
    def __init__(self, loc, id):
        self.x = loc[0]
        self.y = loc[1]
        self.width = 64
        self.height = 64
        self.repr_name = ""
        self.id = id
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        self.hitbox.center = (self.x, self.y)
        self.sprite = Sprites.Sprite(
            (
                "TRIGGER", "TRIGGER",
            )
        )
        # Adding reference
        all_triggers.append(self)
    def set_xy(self, loc:tuple[float, float]):
        self.x, self.y = loc[0], loc[1]
    def action(self):
        for sq in player_enemies.SquadMan.squad_list:
            if self.hitbox.colliderect(sq.get_current_image().get_rect(center=(sq.x, sq.y))):
                self.destroy()
    def render(self, dest:pygame.Surface, x, y):
        w, h = self.width, self.height
        pygame.draw.rect(dest, (255, 0, 255), (x-w/2, y-h/2, w, h))
        pygame.draw.rect(dest, (255, 255, 255), (x-w/2, y-h/2, w, h), width=2)

    def destroy(self):
        deletor.Deleter.request_delete(self, all_triggers)
        for element in all_cutscene_elements:
            if element.id == self.id:
                element.action = True

    def __repr__(self):
        return f"{self.repr_name}->({self.x}, {self.y}, {self.id})"

def cutscene_elements_generator(): # CAN ONLY BE USED IF A VIDEO MODE HAS BEEN SET
        if pygame.display.get_init():
            cutscene_elements_dict = {
                "CollideTrigger": CollideTrigger((0, 0), id=-1), # when the player collides, destroy the trigger and anything with a
                "SpawnEnemyTrigger": SpawnEnemyTrigger((0, 0), id=-1), # when the player collides, destroy the trigger and anything with a
                # of the same id (given it's a cutscene elements), should start action

                # "TruckSwoopIn" -> swoops in and spawns a bunch of enemies
            }
            return cutscene_elements_dict
        return AssertionError("PYGAME DISPLAY WAS NOT INITIALIZED")

# Get object from name
def get_cutscene_elements(template: str):
    if pygame.display.get_init():
        template = template.split("->")
        name = template[0]
        data = template[1][1:-1].split(",")
        obj = copy.copy(cutscene_elements_generator()[name])
        obj.set_xy((float(data[0]), float(data[1])))
        obj.id = data[2]
        obj.repr_name = name
        return obj
    return AssertionError("PYGAME DISPLAY WAS NOT INITIALIZED")
