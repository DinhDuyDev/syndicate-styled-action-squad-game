import pygame
import deletor
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
class Trigger:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 0
        self.height = 0
        all_triggers.append(self)
    def action(self):
        pass
    def render(self, dest:pygame.Surface):
        pygame.draw.rect(dest, (255, 255, 255), (self.x, self.y, self.width, self.height), width=2)
        pygame.draw.rect(dest, (255, 0, 0), (self.x, self.y, self.width, self.height))
    def destroy(self):
        deletor.Deleter.request_delete(self, all_triggers)