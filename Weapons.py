import random
class Weapons:
    def __init__(self, name, fire_cooldown, damage, pellets, inaccuracy, ammo, lives=1, create_ray=False,sound_radius=15,speed_modifier:float=1, projectile_type="BULLET"):
        self.name = name
        self.fire_cooldown = fire_cooldown
        self.damage = damage
        self.pellets = pellets
        self.inaccuracy = inaccuracy
        self.ammo = ammo
        self.lives = lives # determines piercing of number of people
        self.create_ray = create_ray
        self.sound_radius = sound_radius
        self.speed_modifier = speed_modifier
        self.projectile_type = projectile_type

    def __copy__(self):
        return Weapons(self.name, self.fire_cooldown, self.damage, self.pellets, self.inaccuracy, self.ammo, lives=self.lives, create_ray=self.create_ray)

WEAPONS_REF = {
    "Pistol": Weapons("Colt 1911", 15, 15, 1, 4, 7, speed_modifier=1.5),
    "Revolver": Weapons("Magnum", 60, 100, 1, 1, 7,lives=2, create_ray=True, speed_modifier=1.5),
    "Shotgun": Weapons("RMT 970",  60, 11, 15, 8, 6, speed_modifier=1),
    "Thompson": Weapons("Thompson",  4, 10, 1, 6, 50, speed_modifier=0.8), # damage 8, cooldown 4, pellets 1
    "Bar": Weapons("Bar", 12, 30, 1, 1, 7, lives=2, create_ray=True, speed_modifier=0.6),
    "GrenadeLauncher": Weapons("Grenade Launcher", 70, 0, 1, 4, 7, speed_modifier=0.6, projectile_type="GRENADE"),
    "RocketLauncher" : Weapons("Rocket Launcher", 60, 35, 1, 4, 1, projectile_type="ROCKET", speed_modifier=0.5)
}