import math

import Sprites
import pygame
import random

# Decorations ADT:
# x, y: (loc)
# repr_name: for file editor
# sprite: Sprite Object
# xy(): tuple of x and y
# render(dest, x, y): draws on the specified surface
# __copy__(): to copy itself
# __repr__(): Code representation so that the map editor can at least read.
# All significant attributes necessary for object initialization must be available on the constructor
class Crate:
    def __init__(self, loc:tuple[int, int], is_wep_crate=False, destroyed=False):
        self.x, self.y = loc
        self.is_wep_crate = is_wep_crate

        self.sprite = Sprites.Sprite(
            (
                # Okay
                ("CRATE_NORMAL_TOP" if not destroyed else "CRATE_NORMAL_TOP_BROKEN")
                if not is_wep_crate else
                ("CRATE_WEAPONS_TOP" if not destroyed else "CRATE_WEAPONS_BROKEN_TOP"),
                "CRATE_BODY"
            )
        )
        self.repr_name = ""
        self.destroyed = destroyed
        self.angle = random.randint(0, 360)

    def set_xy(self, loc:tuple[float, float]):
        self.x, self.y = loc

    def xy(self):
        return self.x, self.y

    def render(self, dest:pygame.Surface, x, y):
        # self.angle += 0.5
        top_spr = self.sprite.get_image_at(0) #if not self.destroyed else self.sprite.get_image_at(2)
        body_spr = self.sprite.get_image_at(1) #if not self.destroyed else self.sprite.get_image_at(3)

        top_spr = pygame.transform.rotate(top_spr, self.angle)
        body_spr = pygame.transform.rotate(body_spr, self.angle)

        # Bottom
        dest.blit(top_spr, top_spr.get_rect(center=(x, y+2.5)))
        # Draw
        for i in range(1, 5):
            dest.blit(body_spr, body_spr.get_rect(center=(x, y+2.5-i)))
        # Top
        dest.blit(top_spr, top_spr.get_rect(center=(x, y-2.5)))

    def __copy__(self):
        return_obj = Crate((0, 0), is_wep_crate=self.is_wep_crate, destroyed=self.destroyed)
        return_obj.repr_name = self.repr_name
        return return_obj

    def __repr__(self):
        return f"{self.repr_name}->({self.x}, {self.y})"

    def __lt__(self, other):
        return self.y < other.y

    def __gt__(self, other):
        return self.y > other.y

    def __eq__(self, other):
        return self.y == other.y

class Barrel:
    def __init__(self, loc:tuple[int, int], destroyed=False):
        self.x, self.y = loc

        self.sprite = Sprites.Sprite(
            (
                # Okay
                "BARREL_TOP" if not destroyed else "BARREL_TOP_BROKEN",
                "BARREL_BODY"
            )
        )
        self.repr_name = ""
        self.destroyed = destroyed
        self.angle = random.randint(0, 360)

    def set_xy(self, loc:tuple[float, float]):
        self.x, self.y = loc

    def xy(self):
        return self.x, self.y

    def render(self, dest:pygame.Surface, x, y):
        # self_spr = self.sprite.get_image_at(0) #if not self.destroyed else self.sprite.get_image_at(2)
        #
        # # Bottom
        # dest.blit(self_spr, self_spr.get_rect(center=(x, y)))

        top_spr = self.sprite.get_image_at(0)  # if not self.destroyed else self.sprite.get_image_at(2)
        body_spr = self.sprite.get_image_at(1)  # if not self.destroyed else self.sprite.get_image_at(3)

        # Bottom
        dest.blit(top_spr, top_spr.get_rect(center=(x, y + 2.5)))
        # Draw
        for i in range(1, 5):
            dest.blit(body_spr, body_spr.get_rect(center=(x, y + 2.5 - i)))
        # Top
        dest.blit(top_spr, top_spr.get_rect(center=(x, y - 2.5)))


    def __copy__(self):
        return_obj = Barrel((0, 0), destroyed=self.destroyed)
        return_obj.repr_name = self.repr_name
        return return_obj

    def __repr__(self):
        return f"{self.repr_name}->({self.x}, {self.y})"

    def __lt__(self, other):
        return self.y < other.y

    def __gt__(self, other):
        return self.y > other.y

    def __eq__(self, other):
        return self.y == other.y

class Skull:
    def __init__(self, loc:tuple[int, int]):
        self.x, self.y = loc

        self.sprite = Sprites.Sprite(
            (
                # Okay
                "SKULL",
                "SKULL"
            )
        )
        self.repr_name = ""

    def set_xy(self, loc:tuple[float, float]):
        self.x, self.y = loc

    def xy(self):
        return self.x, self.y

    def render(self, dest:pygame.Surface, x, y):
        self_spr = self.sprite.get_image_at(0) #if not self.destroyed else self.sprite.get_image_at(2)

        # Bottom
        dest.blit(self_spr, self_spr.get_rect(center=(x, y)))

    def __copy__(self):
        return_obj = Skull((0, 0))
        return_obj.repr_name = self.repr_name
        return return_obj

    def __repr__(self):
        return f"{self.repr_name}->({self.x}, {self.y})"

    def __lt__(self, other):
        return self.y < other.y

    def __gt__(self, other):
        return self.y > other.y

    def __eq__(self, other):
        return self.y == other.y

class Crack:
    def __init__(self, loc:tuple[int, int], crack_type=1):
        self.x, self.y = loc

        spr_tuple = ()
        self.crack_type = crack_type
        if crack_type == 2:
            spr_tuple = (
                # Okay
                "CRACK_2",
                "CRACK_2"
            )
        elif crack_type == 3:
            spr_tuple = (
                # Okay
                "CRACK_3",
                "CRACK_3"
            )
        else:
            spr_tuple = (
                # Okay
                "CRACK_1",
                "CRACK_1"
            )
        self.sprite = Sprites.Sprite(
            spr_tuple
        )
        self.repr_name = ""

    def set_xy(self, loc:tuple[float, float]):
        self.x, self.y = loc

    def xy(self):
        return self.x, self.y

    def render(self, dest:pygame.Surface, x, y):
        self_spr = self.sprite.get_image_at(0) #if not self.destroyed else self.sprite.get_image_at(2)

        # Bottom
        dest.blit(self_spr, self_spr.get_rect(center=(x, y)))

    def __copy__(self):
        return_obj = Crack((0, 0), crack_type=self.crack_type)
        return_obj.repr_name = self.repr_name
        return return_obj

    def __repr__(self):
        return f"{self.repr_name}->({self.x}, {self.y})"

    def __lt__(self, other):
        return self.y < other.y

    def __gt__(self, other):
        return self.y > other.y

    def __eq__(self, other):
        return self.y == other.y

class Table:
    def __init__(self, loc:tuple[int, int], angle=-1):
        self.x, self.y = loc
        self.sprite = Sprites.Sprite(
            (
                # Okay
                ("TABLE_TOP", "TABLE_LEG")
            )
        )
        self.repr_name = ""
        self.angle = random.randint(0, 360) if angle == -1 else angle
        self.random_angle = True if angle == -1 else False

    def set_xy(self, loc:tuple[float, float]):
        self.x, self.y = loc

    def xy(self):
        return self.x, self.y

    def render(self, dest:pygame.Surface, x, y):
        # self.angle += 0.5
        top_spr = self.sprite.get_image_at(0) #if not self.destroyed else self.sprite.get_image_at(2)
        leg_spr = self.sprite.get_image_at(1) #if not self.destroyed else self.sprite.get_image_at(3)

        top_spr = pygame.transform.rotate(top_spr, self.angle)
        leg_spr = pygame.transform.rotate(leg_spr, self.angle)

        # Legs
        for i in range(1, 5):
            dest.blit(leg_spr, leg_spr.get_rect(center=(x, y-2.5+i)))

        # Draw Top later
        dest.blit(top_spr, top_spr.get_rect(center=(x, y - 2.5)))


    def __copy__(self):
        return_obj = Table((0, 0), angle=random.randint(0, 360) if self.random_angle else self.angle)
        return_obj.repr_name = self.repr_name
        return return_obj

    def __repr__(self):
        return f"{self.repr_name}->({self.x}, {self.y})"

    def __lt__(self, other):
        return self.y < other.y

    def __gt__(self, other):
        return self.y > other.y

    def __eq__(self, other):
        return self.y == other.y


class TableToppled:
    def __init__(self, loc:tuple[int, int], angle=-1):
        self.x, self.y = loc
        self.sprite = Sprites.Sprite(
            (
                # Okay
                ("TABLE_TOP_TOPPLED_BORDER", "TABLE_TOP_TOPPLED_INNER"
                 , "TABLE_TOPPLED_LEG")
            )
        )
        self.repr_name = ""
        self.angle = random.randint(0, 360) if angle == -1 else angle
        self.random_angle = True if angle == -1 else False

    def set_xy(self, loc:tuple[float, float]):
        self.x, self.y = loc

    def xy(self):
        return self.x, self.y

    def render(self, dest:pygame.Surface, x, y):
        # self.angle += 0.5
        top_border_spr = self.sprite.get_image_at(0) #if not self.destroyed else self.sprite.get_image_at(2)
        top_inner_spr = self.sprite.get_image_at(1) #if not self.destroyed else self.sprite.get_image_at(2)
        leg_spr = self.sprite.get_image_at(2) #if not self.destroyed else self.sprite.get_image_at(3)

        top_border_spr = pygame.transform.rotate(top_border_spr, self.angle)
        top_inner_spr = pygame.transform.rotate(top_inner_spr, self.angle)

        # Legs
        ## TOP LEGS
        def draw_legs():
            top_left = (math.cos(math.radians(self.angle)) * -12, math.sin(math.radians(self.angle)) * -12)
            top_right = (math.cos(math.radians(self.angle)) * 12, math.sin(math.radians(self.angle)) * 12)

            for i in range(8):
                vec_x = math.cos(math.radians(self.angle + 90))*i
                vec_y = math.sin(math.radians(self.angle + 90))*i

                dest.blit(leg_spr, leg_spr.get_rect(center=(x + vec_x + top_left[0], y - vec_y + 2.5 - top_left[1])))
                dest.blit(leg_spr, leg_spr.get_rect(center=(x + vec_x + top_right[0], y - vec_y + 2.5 - top_right[1])))

                dest.blit(leg_spr, leg_spr.get_rect(center=(x+vec_x+top_left[0], y-vec_y-2.5-top_left[1])))
                dest.blit(leg_spr, leg_spr.get_rect(center=(x+vec_x+top_right[0], y-vec_y-2.5-top_right[1])))


        # Drawing top
        def draw_top():
            dest.blit(top_border_spr, top_border_spr.get_rect(center=(x, y - 3.5)))
            top_height = 7
            for i in range(1, top_height):
                dest.blit(top_inner_spr, top_inner_spr.get_rect(center=(x, y - 3.5+i)))
            dest.blit(top_border_spr, top_border_spr.get_rect(center=(x, y - 3.5 + top_height+1)))

            # pygame.draw.rect(dest, (255, 0, 0), (x-2, y-2, 4, 4))
            # pygame.draw.line(dest, (0, 255, 0), (x, y),
            #                  (x+math.cos(math.radians(self.angle))*64,y-math.sin(math.radians(self.angle))*64))

        if 0 <= self.angle < 90 or 270 < self.angle < 360:
            draw_legs()
            draw_top()
        else:
            draw_top()
            draw_legs()

    def __copy__(self):
        return_obj = TableToppled((0, 0), angle=random.randint(0, 360) if self.random_angle else self.angle)
        return_obj.repr_name = self.repr_name
        return return_obj

    def __repr__(self):
        return f"{self.repr_name}->({self.x}, {self.y})"

    def __lt__(self, other):
        return self.y < other.y

    def __gt__(self, other):
        return self.y > other.y

    def __eq__(self, other):
        return self.y == other.y

# All the types of decoration (just to make sure when I code the completion doesn't freak out)
all_decoration_types = Crate|Barrel|Skull