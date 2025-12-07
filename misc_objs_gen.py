import pygame
import decorations
import copy
def misc_objects_generator(): # CAN ONLY BE USED IF A VIDEO MODE HAS BEEN SET
    if pygame.display.get_init():
        misc_objs_dict = {
            "NormalCrate": decorations.Crate((0, 0)),
            "WeaponCrate": decorations.Crate((0, 0), True),
            "NormalCrateBroken": decorations.Crate((0, 0), destroyed=True),
            "WeaponCrateBroken": decorations.Crate((0, 0), is_wep_crate=True, destroyed=True),
            "Barrel": decorations.Barrel((0, 0)),
            "BarrelBroken": decorations.Barrel((0, 0), destroyed=True),
            "Skull": decorations.Skull((0, 0)),
            "TableRand": decorations.Table((0, 0)),
            "Table0": decorations.Table((0, 0),angle=0),
            "Table45": decorations.Table((0, 0),angle=45),
            "Table90": decorations.Table((0, 0),angle=90),
            "Table135": decorations.Table((0, 0),angle=135),
            "TableToppledRand": decorations.TableToppled((0, 0)),
            "TableToppled0": decorations.TableToppled((0, 0),angle=0),
            "TableToppled45": decorations.TableToppled((0, 0),angle=45),
            "TableToppled90": decorations.TableToppled((0, 0),angle=90),
            "TableToppled135": decorations.TableToppled((0, 0),angle=135),
            "TableToppled180": decorations.TableToppled((0, 0), angle=180),
            "TableToppled225": decorations.TableToppled((0, 0), angle=225),
            "TableToppled270": decorations.TableToppled((0, 0), angle=270),
            "TableToppled315": decorations.TableToppled((0, 0), angle=315)
        }
        return misc_objs_dict
    return AssertionError("PYGAME DISPLAY WAS NOT INITIALIZED")

# Get object from name
def get_miscellaneous_objects(template:str):
    if pygame.display.get_init():
        template = template.split("->")
        name = template[0]
        coordinates = template[1][1:-1].split(",")
        obj = copy.copy(misc_objects_generator()[name])
        obj.set_xy((float(coordinates[0]), float(coordinates[1])))
        obj.repr_name = name
        return obj
    return AssertionError("PYGAME DISPLAY WAS NOT INITIALIZED")
