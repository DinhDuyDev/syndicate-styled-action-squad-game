import random
class Weapons:
    def __init__(self, name, fire_cooldown, damage, pellets, inaccuracy, ammo, damage_modifier=0, lives=1, create_ray=False):
        self.name = name
        self.fire_cooldown = fire_cooldown
        self.damage = damage
        self.pellets = pellets
        self.inaccuracy = inaccuracy
        self.ammo = ammo
        self.lives = lives # determines piercing of number of people
        self.create_ray = create_ray

    def __copy__(self):
        return Weapons(self.name, self.fire_cooldown, self.damage, self.pellets, self.inaccuracy, self.ammo, lives=self.lives, create_ray=self.create_ray)

WEAPONS_REF = {
    "Colt 1911": Weapons("Colt 1911", 30, 25, 1, 4, 7),
    "Magnum": Weapons("Magnum", 60, 100, 1, 1, 7,lives=2, create_ray=True),
    "RMT 970": Weapons("FMT 970",  60, 10, 15, 7, 6),
    "Thompson": Weapons("Thompson",  5, 7, 1, 4, 50)
}