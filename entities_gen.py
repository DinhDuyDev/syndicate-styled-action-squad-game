import entities
import pygame
import copy
def entities_generator(): # CAN ONLY BE USED IF A VIDEO MODE HAS BEEN SET
    if pygame.display.get_init():
        misc_objs_dict = {
            "EnemyMobsterPistol": entities.EnemyMobster((0, 0),weapon_type="Pistol"),
            "EnemyMobsterShotgun": entities.EnemyMobster((0, 0),weapon_type="Shotgun"),
            "EnemyMobsterThompson": entities.EnemyMobster((0, 0),weapon_type="Thompson"),
            "EnemyMobsterBar": entities.EnemyMobster((0, 0),weapon_type="Bar")
        }
        return misc_objs_dict
    return AssertionError("PYGAME DISPLAY WAS NOT INITIALIZED")

# Get object from name
def get_entities(template:str):
    if pygame.display.get_init():
        template = template.split("->")
        name = template[0]
        coordinates = template[1][1:-1].split(",")
        obj = copy.copy(entities_generator()[name])
        obj.set_xy((float(coordinates[0]), float(coordinates[1])))
        obj.repr_name = name
        return obj
    return AssertionError("PYGAME DISPLAY WAS NOT INITIALIZED")
