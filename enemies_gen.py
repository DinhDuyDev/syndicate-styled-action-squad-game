import player_enemies
import pygame
import copy
def enemies_generator(): # CAN ONLY BE USED IF A VIDEO MODE HAS BEEN SET
    if pygame.display.get_init():
        misc_objs_dict = {
            "EnemyMobsterPistol": player_enemies.Enemy((0, 0), weapon_type="Pistol", exclude=True),
            "EnemyMobsterShotgun": player_enemies.Enemy((0, 0), weapon_type="Shotgun", exclude=True),
            "EnemyMobsterThompson": player_enemies.Enemy((0, 0), weapon_type="Thompson", exclude=True),
            "EnemyMobsterBar": player_enemies.Enemy((0, 0), weapon_type="Bar", exclude=True)
        }
        return misc_objs_dict
    return AssertionError("PYGAME DISPLAY WAS NOT INITIALIZED")

# Get object from name
def get_enemies(template:str):
    if pygame.display.get_init():
        template = template.split("->")
        name = template[0]
        coordinates = template[1][1:-1].split(",")
        obj = copy.copy(enemies_generator()[name])
        obj.set_xy((float(coordinates[0]), float(coordinates[1])))
        obj.repr_name = name
        return obj
    return AssertionError("PYGAME DISPLAY WAS NOT INITIALIZED")
