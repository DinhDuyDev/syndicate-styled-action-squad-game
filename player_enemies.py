import pygame
import math
import copy
import ALL_SPRITES
import settings
import utilityfuncs
import Sprites
import random
import Weapons
import Bullet
import effects
import camera
import deletor
import entities
import SlowMo
import pathfind

WEAPONS_REF = Weapons.WEAPONS_REF

class MapData:
    MAP_GEOMETRY:list[list[int]] = []

# Enemies all belong here
enemy_list = []

# Sprites
def gen_soldier_sprites():
    return {
        "Pistol" : Sprites.Sprite(
            (
                "SOLDIER_0_PISTOL",
                "SOLDIER_45_PISTOL",
                "SOLDIER_90_PISTOL",
                "SOLDIER_135_PISTOL",
                "SOLDIER_180_PISTOL",
                "SOLDIER_225_PISTOL",
                "SOLDIER_270_PISTOL",
                "SOLDIER_315_PISTOL",
            )
        ),

        "Revolver" : Sprites.Sprite(
            (
                "SOLDIER_0_REVOLVER",
                "SOLDIER_45_REVOLVER",
                "SOLDIER_90_REVOLVER",
                "SOLDIER_135_REVOLVER",
                "SOLDIER_180_REVOLVER",
                "SOLDIER_225_REVOLVER",
                "SOLDIER_270_REVOLVER",
                "SOLDIER_315_REVOLVER"
            )
        ),
        "Shotgun" : Sprites.Sprite(
            (
                "SOLDIER_0_SHOTGUN",
                "SOLDIER_45_SHOTGUN",
                "SOLDIER_90_SHOTGUN",
                "SOLDIER_135_SHOTGUN",
                "SOLDIER_180_SHOTGUN",
                "SOLDIER_225_SHOTGUN",
                "SOLDIER_270_SHOTGUN",
                "SOLDIER_315_SHOTGUN",
            )
        ),
        "Thompson" : Sprites.Sprite(
            (
                "SOLDIER_0_THOMPSON",
                "SOLDIER_45_THOMPSON",
                "SOLDIER_90_THOMPSON",
                "SOLDIER_135_THOMPSON",
                "SOLDIER_180_THOMPSON",
                "SOLDIER_225_THOMPSON",
                "SOLDIER_270_THOMPSON",
                "SOLDIER_315_THOMPSON",
            )
        ),
        "Bar" : Sprites.Sprite(
            (
                "SOLDIER_0_BAR",
                "SOLDIER_45_BAR",
                "SOLDIER_90_BAR",
                "SOLDIER_135_BAR",
                "SOLDIER_180_BAR",
                "SOLDIER_225_BAR",
                "SOLDIER_270_BAR",
                "SOLDIER_315_BAR",
            )
        ),
        "GrenadeLauncher" : Sprites.Sprite(
            (
                "SOLDIER_0_GLAUNCHER",
                "SOLDIER_45_GLAUNCHER",
                "SOLDIER_90_GLAUNCHER",
                "SOLDIER_135_GLAUNCHER",
                "SOLDIER_180_GLAUNCHER",
                "SOLDIER_225_GLAUNCHER",
                "SOLDIER_270_GLAUNCHER",
                "SOLDIER_315_GLAUNCHER",
            )
        ),
        "RocketLauncher" : Sprites.Sprite(
            (
                "SOLDIER_0_RLAUNCHER",
                "SOLDIER_45_RLAUNCHER",
                "SOLDIER_90_RLAUNCHER",
                "SOLDIER_135_RLAUNCHER",
                "SOLDIER_180_RLAUNCHER",
                "SOLDIER_225_RLAUNCHER",
                "SOLDIER_270_RLAUNCHER",
                "SOLDIER_315_RLAUNCHER",
            )
        ),
        "None" : Sprites.Sprite(
            (
                "SOLDIER_BASIC",
                "SOLDIER_BASIC",
                "SOLDIER_BASIC",
                "SOLDIER_BASIC",
                "SOLDIER_BASIC",
                "SOLDIER_BASIC",
                "SOLDIER_BASIC",
                "SOLDIER_BASIC",
            )
        ),
        "LEGS" : Sprites.Sprite(
            (
                "SOLDIER_LEGS_LEFT",
                "SOLDIER_LEGS_RIGHT",
                "SOLDIER_LEGS_NORMAL"
            )
        )
    }


def gen_mobster_sprites():
    return {
        "Pistol" : Sprites.Sprite(
            (
                "MOBSTER_0_PISTOL",
                "MOBSTER_45_PISTOL",
                "MOBSTER_90_PISTOL",
                "MOBSTER_135_PISTOL",
                "MOBSTER_180_PISTOL",
                "MOBSTER_225_PISTOL",
                "MOBSTER_270_PISTOL",
                "MOBSTER_315_PISTOL",
            )
        ),

        "Revolver" : Sprites.Sprite(
            (
                "MOBSTER_0_REVOLVER",
                "MOBSTER_45_REVOLVER",
                "MOBSTER_90_REVOLVER",
                "MOBSTER_135_REVOLVER",
                "MOBSTER_180_REVOLVER",
                "MOBSTER_225_REVOLVER",
                "MOBSTER_270_REVOLVER",
                "MOBSTER_315_REVOLVER",
            )
        ),
        "Shotgun" : Sprites.Sprite(
            (
                "MOBSTER_0_SHOTGUN",
                "MOBSTER_45_SHOTGUN",
                "MOBSTER_90_SHOTGUN",
                "MOBSTER_135_SHOTGUN",
                "MOBSTER_180_SHOTGUN",
                "MOBSTER_225_SHOTGUN",
                "MOBSTER_270_SHOTGUN",
                "MOBSTER_315_SHOTGUN",
            )
        ),
        "Thompson" : Sprites.Sprite(
            (
                "MOBSTER_0_THOMPSON",
                "MOBSTER_45_THOMPSON",
                "MOBSTER_90_THOMPSON",
                "MOBSTER_135_THOMPSON",
                "MOBSTER_180_THOMPSON",
                "MOBSTER_225_THOMPSON",
                "MOBSTER_270_THOMPSON",
                "MOBSTER_315_THOMPSON",
            )
        ),
        "Bar" : Sprites.Sprite(
            (
                "MOBSTER_0_BAR",
                "MOBSTER_45_BAR",
                "MOBSTER_90_BAR",
                "MOBSTER_135_BAR",
                "MOBSTER_180_BAR",
                "MOBSTER_225_BAR",
                "MOBSTER_270_BAR",
                "MOBSTER_315_BAR",
            )
        ),

        "GrenadeLauncher" : Sprites.Sprite(
            (
                "MOBSTER_0_GLAUNCHER",
                "MOBSTER_45_GLAUNCHER",
                "MOBSTER_90_GLAUNCHER",
                "MOBSTER_135_GLAUNCHER",
                "MOBSTER_180_GLAUNCHER",
                "MOBSTER_225_GLAUNCHER",
                "MOBSTER_270_GLAUNCHER",
                "MOBSTER_315_GLAUNCHER",
            )
        ),

        "RocketLauncher": Sprites.Sprite(
            (
                "MOBSTER_0_RLAUNCHER",
                "MOBSTER_45_RLAUNCHER",
                "MOBSTER_90_RLAUNCHER",
                "MOBSTER_135_RLAUNCHER",
                "MOBSTER_180_RLAUNCHER",
                "MOBSTER_225_RLAUNCHER",
                "MOBSTER_270_RLAUNCHER",
                "MOBSTER_315_RLAUNCHER",
            )
        ),
        "None" : Sprites.Sprite(
            (
                "MOBSTER",
                "MOBSTER",
                "MOBSTER",
                "MOBSTER",
                "MOBSTER",
                "MOBSTER",
                "MOBSTER",
                "MOBSTER",
            )
        ),
        "LEGS" : Sprites.Sprite(
            (
                "MOBSTER_LEG_LEFTUP",
                "MOBSTER_LEG_RIGHTUP",
                "MOBSTER_LEG_NORMAL"
            )
        )
    }

def fire_gun(obj, direction):
    obj.cooldown += 1 * SlowMo.SlowMo.slow_motion_ratio
    if obj.cooldown > obj.get_weapon().fire_cooldown:
        base_ref = WEAPONS_REF[obj.current_weapon_name].damage
        total_damage = base_ref
        md_dir = direction
        d = md_dir // 45
        vec_x = math.cos(math.radians(d * 45)) * 8
        vec_y = math.sin(math.radians(d * 45)) * 8
        obj.focused = False
        wep = obj.get_weapon()

        for i in range(wep.pellets):
            _damage = wep.damage
            # total_damage += _damage
            _inaccuracies = wep.inaccuracy
            _lives = wep.lives
            _projectile_type = wep.projectile_type
            _create_ray = wep.create_ray
            if _projectile_type == "GRENADE":
                entities.Grenade(obj.x+vec_x, obj.y - vec_y, md_dir, SquadMan.squad_list + enemy_list)
            elif _projectile_type == "ROCKET":
                extra_inaccuracy = 0
                if len(obj.move_path) > 0:
                    extra_inaccuracy = random.randrange(-32, 32)
                enemy = SquadMan.squad_list if not isinstance(obj, SquadMan) else enemy_list
                entities.Rocket(obj.x + vec_x, obj.y - vec_y, md_dir + extra_inaccuracy
                                , targets=enemy, explosion_affects=SquadMan.squad_list + enemy_list, spawner=obj)
            else:
                Bullet.PlayerBullet(obj.xy()[0] + vec_x, obj.xy()[1] - vec_y, md_dir, obj, damage=_damage,
                                    deviation=_inaccuracies, lives=_lives, create_ray=_create_ray)
                effects.MuzzleFlash(obj.xy()[0] + vec_x, obj.xy()[1] - vec_y)

        entities.SoundSource(obj.xy()[0], obj.xy()[1], (total_damage / (base_ref+1)) * 30)
        obj.sprite.set_image_index(d)
        obj.knockback((total_damage / 50) ** 0.8 + random.randint(1, 2) * (bool(total_damage > 0)), direction + 180)
        obj.cooldown = 0

def switch_sprite(obj):
    if obj.current_weapon_name == "Pistol":
        obj.sprite = obj.pistol_sprite
    elif obj.current_weapon_name == "Revolver":
        obj.sprite = obj.revolver_sprite
    elif obj.current_weapon_name == "Shotgun":
        obj.sprite = obj.shotgun_sprite
    elif obj.current_weapon_name == "Thompson":
        obj.sprite = obj.thompson_sprite
    elif obj.current_weapon_name == "Bar":
        obj.sprite = obj.bar_sprite
    elif obj.current_weapon_name == "GrenadeLauncher":
        obj.sprite = obj.grenade_sprite
    elif obj.current_weapon_name == "RocketLauncher":
        obj.sprite = obj.rocket_sprite
    else:
        obj.sprite = obj.basic_sprite
def random_weapon():
    return random.choice(["Pistol", "Revolver", "Shotgun", "Thompson", "Bar", "GrenadeLauncher", "RocketLauncher"])
class SquadMan:
    INDEX = 0
    MAX_SQUAD = 4
    squad_list:list = []
    squad_footstep_counter = 0
    inventory:list[Weapons.InventoryWeapon] = [
        Weapons.InventoryWeapon("None", 0, 9, 9),
        Weapons.InventoryWeapon(random_weapon(), 6, -1, -1),
        Weapons.InventoryWeapon(random_weapon(), 6, -1, -1),
        Weapons.InventoryWeapon(random_weapon(), 6, -1, -1),
        Weapons.InventoryWeapon(random_weapon(), 6, -1, -1),
    ]
    @classmethod
    def nums_active(cls):
        nums = 0
        for i in SquadMan.squad_list:
            if (not i.is_dead) and i.being_used:
                nums += 1
        return nums
    @classmethod
    def nums_alive(cls):
        nums = 0
        for i in SquadMan.squad_list:
            if not i.is_dead:
                nums += 1
        return nums
    @classmethod
    def make_footsteps(cls):
        spd_modifier = (2-SquadMan.nums_active()/4) * 1.25
        if SquadMan.squad_footstep_counter >= 30 * (1/spd_modifier):
            for e in SquadMan.squad_list:
                if (not e.is_dead) and e.being_used and len(e.move_path) != 0:
                    entities.SoundSource(e.x, e.y, 10 * (6 / spd_modifier ** 2)) # Making footstep noises
                    break
            SquadMan.squad_footstep_counter = 0
        else:
            SquadMan.squad_footstep_counter += 1

    @classmethod
    def living_squad_members(cls):
        return [sq_member for sq_member in SquadMan.squad_list if sq_member is not None]

    @classmethod
    def first_living_member(cls):
        for i in SquadMan.squad_list:
            if not i.is_dead:
                return i
        return None

    def __init__(self, loc:tuple[float, float]):
        super().__init__()
        self.x, self.y = loc
        self.max_hp = 100
        self.hp = self.max_hp
        self.pain_amount = 0
        self.max_pain_amount = 100
        self.dest_x = self.x
        self.dest_y = self.y
        self.index = SquadMan.INDEX
        SquadMan.INDEX += 1

        all_sprites = gen_soldier_sprites()

        self.references = []

        self.pistol_sprite = all_sprites["Pistol"]
        self.revolver_sprite = all_sprites["Revolver"]
        self.shotgun_sprite = all_sprites["Shotgun"]
        self.thompson_sprite = all_sprites["Thompson"]
        self.bar_sprite = all_sprites["Bar"]
        self.grenade_sprite = all_sprites["GrenadeLauncher"]
        self.rocket_sprite = all_sprites["RocketLauncher"]
        self.basic_sprite = all_sprites["None"]

        self.leg_normal_sprite = all_sprites["LEGS"]

        self.leg_crouch_sprite = Sprites.Sprite(
            (
                "MOBSTER_LEG_CROUCHING_LEFT",
                "MOBSTER_LEG_CROUCHING_RIGHT",
                "MOBSTER_LEG_CROUCHING_RIGHT"
            )
        )
        self.leg_sprite = self.leg_normal_sprite

        self.front_dir:float = 0

        self.crouching = False # Crouching enemy
        self.sprite = self.pistol_sprite
        self.move_path = []
        self.focused = True # so that they look at where they're going
        self.being_used = True

        self.knock_back_strength = 0
        self.knock_back_dir = 0

        self.current_item_used = SquadMan.inventory[0]
        self.current_weapon_name = self.current_item_used.weapon_name
        self.current_weapon = WEAPONS_REF[self.current_weapon_name]

        self.cooldown = 0
        self.cooldown_steps = 0
        self.speed = 0.5

        self.target:Enemy|None = None

        self.is_dead = False

        #SquadMan.squad_list.append(self)
        SquadMan.squad_list.append(self)

    def set_dest(self, x, y, m):
        self.move_path.clear()
        self.dest_x, self.dest_y = x, y
        def conv(val):
            return int(val/settings.cell_dimension)
        self.move_path = pathfind.pathfind(conv(self.x), conv(self.y), conv(self.dest_x), conv(self.dest_y), m)

    def xy(self):
        return self.x, self.y

    def action(self):
        if self.focused:
            self.sprite.set_image_index(int(self.front_dir / 45))
        if self.hp < self.max_hp/2:
            self.hp = min(self.hp + 0.2 * SlowMo.SlowMo.slow_motion_ratio * (1 - (self.pain_amount / 200)), self.max_hp)
        self.pain_amount = min(max(self.pain_amount - 0.1, 0), 200)

        if self.knock_back_strength >= 0.001:
            self.knock_back_strength *= 0.9
            self.leg_sprite.set_image_speed(4/30)
        else:
            self.knock_back_strength = 0

        self.movement()


    def auto_aim(self): # Soldiers will fire themselves if they're unused
        for enemy in enemy_list:
            if utilityfuncs.point_distance(self.x, self.y, enemy.x, enemy.y) < 90:
                if utilityfuncs.line_of_sight(self.x, self.y, enemy.x, enemy.y, MapData.MAP_GEOMETRY):
                    self.front_dir = utilityfuncs.point_direction(self.x, self.y, enemy.x, enemy.y)
                    self.focused = True
                    fire_gun(self, self.front_dir)
                    break


    def movement(self):
        spd_modifier = (2 - SquadMan.nums_active() / 4) * 1.25
        if len(self.move_path) == 0:
            if utilityfuncs.point_distance(self.dest_x, self.dest_y, self.x, self.y) > 2:
                dir_ = utilityfuncs.point_direction(self.x, self.y, self.dest_x, self.dest_y)
                self.x += math.cos(math.radians(dir_)) * self.speed * self.get_weapon().speed_modifier * spd_modifier #* (SlowMo.SlowMo.slow_motion_ratio * 2)
                self.y -= math.sin(math.radians(dir_)) * self.speed * self.get_weapon().speed_modifier * spd_modifier #* (SlowMo.SlowMo.slow_motion_ratio * 2)
            else:
                self.dest_x, self.dest_y = self.x, self.y
                self.leg_sprite.set_image_index(2)
                self.leg_sprite.set_image_speed(0)
        else:
            x, y = (self.move_path[0][0] * settings.cell_dimension + settings.cell_dimension / 2
                        , self.move_path[0][1] * settings.cell_dimension + settings.cell_dimension / 2 - 2.5)

            if utilityfuncs.point_distance(self.x, self.y, x, y) > 5:
                dir_ = utilityfuncs.point_direction(self.x, self.y, x, y)
                self.front_dir = dir_
                self.x += math.cos(math.radians(dir_)) * self.speed * self.get_weapon().speed_modifier * spd_modifier #* (SlowMo.SlowMo.slow_motion_ratio * 2)
                self.y -= math.sin(math.radians(dir_)) * self.speed * self.get_weapon().speed_modifier * spd_modifier #* (SlowMo.SlowMo.slow_motion_ratio * 2)
            else:
                self.move_path.pop(0)

            self.leg_sprite.run_sprite()
            self.leg_sprite.set_image_speed(4 / 30)
            if self.leg_sprite.image_index > 2:
                self.leg_sprite.image_index = 0


    def render(self, dest:pygame.Surface, x, y, show_stats=False):
        if not self.is_dead:
            # Being used
            vec_x = math.cos(math.radians(self.knock_back_dir)) * self.knock_back_strength
            vec_y = math.sin(math.radians(self.knock_back_dir)) * self.knock_back_strength
            x += vec_x
            y -= vec_y

            self.switch_sprites()
            dest.blit(self.sprite.get_current_image(), self.sprite.get_current_image().get_rect(center=(x, y)))
            dest.blit(self.leg_sprite.get_current_image(), self.leg_sprite.get_current_image().get_rect(center=(x, y)))

            # Health
            if show_stats:
                pygame.draw.rect(dest, (255, 0, 0), (x - 5, y - 9, 10, 2))
                pygame.draw.rect(dest, (0, 255, 0), (x - 5, y - 9, 10 * self.hp / self.max_hp, 2))

                pygame.draw.rect(dest, (0, 0, 0), (x - 10, y-3, 2, 13))
                r = self.cooldown / self.get_weapon().fire_cooldown
                pygame.draw.rect(dest, (255, 255, 255), (x - 10, y+10 - 13 * r, 2, 13 * r))

            # Drawing move path
            # if len(self.move_path) > 0:
            #     for i in range(len(self.move_path)):
            #         offset_x = self.move_path[i][0] * settings.cell_dimension - self.x + settings.cell_dimension/2
            #         offset_y = self.move_path[i][1] * settings.cell_dimension - self.y + settings.cell_dimension/2
            #         pygame.draw.circle(dest, (0, 255, 0), (x+offset_x, y+offset_y), 1)
        else:
            side_ways = pygame.transform.rotate(ALL_SPRITES.ASP["SOLDIER_DEAD_BODY"], 270)
            side_ways_rect = side_ways.get_rect(center=(x,y))
            dest.blit(side_ways, side_ways_rect)


    def get_hitbox(self):
        return self.sprite.get_current_image().get_rect(center=(self.x, self.y))


    def take_damage(self, amount, source=None):
        self.hp -= amount
        camera.Camera.activeCam.screen_shake(((amount / 10) ** 0.5) * 3)
        self.pain_amount += amount / 2

        source_dir = random.random() * 360
        if source is not None:
            source_dir = utilityfuncs.point_direction(self.x, self.y, source.x, source.y)+180

        num_splots = int(1 + amount / 20)
        for i in range(num_splots):
            r = random.randrange(6, 23) + 2 * (amount / 32)
            _rd = random.randrange(-11, 11)
            vec_x = math.cos(math.radians(source_dir+_rd)) * r
            vec_y = math.sin(math.radians(source_dir+_rd)) * r
            effects.BloodSplot(self.x + vec_x, self.y - vec_y)


    def cooldown_ratio(self):
        r = self.cooldown / self.get_weapon().fire_cooldown
        return r


    def health_ratio(self):
        return self.hp / self.max_hp


    def check_death(self):
        if self.hp < 0:
            self.is_dead = True
            self.being_used = False
            # self.destroy()
            self.deselect_weapon()

    def deselect_weapon(self):
        self.current_item_used.being_used = False
        self.current_item_used.used_by_obj = None
        self.current_item_used = SquadMan.inventory[0]

    def destroy(self):
        deletor.Deleter.request_delete(self, SquadMan.squad_list)
        # SquadMan.squad_list.insert(SquadMan.squad_list.index(self), None)
        for l in self.references:
            deletor.Deleter.request_delete(self, l)

    def switch_sprites(self):
        switch_sprite(self)

    def select_current_item(self, item:Weapons.InventoryWeapon):
        if item is not self.current_item_used:
            self.cooldown = 0
            # Unuse that item
            self.current_item_used.being_used = False
            self.current_item_used.used_by_obj = None

            # Get new item
            self.current_item_used = item
            if item.weapon_name != "None":
                self.current_item_used.used_by_obj = self
                self.current_item_used.being_used = True
            self.current_weapon_name = item.weapon_name
            self.current_weapon = Weapons.WEAPONS_REF[item.weapon_name]

    def firing(self, direction):
        if self.being_used:
            if pygame.key.get_pressed()[pygame.K_e] or pygame.mouse.get_pressed()[2]:
                fire_gun(self, direction)
        else:
            self.auto_aim()


    def knockback(self, strength, knock_dir):
        self.knock_back_dir = knock_dir
        self.knock_back_strength = strength


    def get_weapon(self):
        return self.current_weapon


    def get_weapon_name(self):
        return self.current_weapon_name


    def __lt__(self, other):
        return self.y < other.y


    def __gt__(self, other):
        return self.y > other.y


    def __eq__(self, other):
        return self.y == other.y



def move_squad(x, y, m):
    sq_ls = SquadMan.squad_list
    num_active = SquadMan.nums_active() if SquadMan.nums_active() > 0 else 1
    map_width = len(m[0])
    map_height = len(m)
    d = 45
    dist_travel = 7 * (num_active / SquadMan.MAX_SQUAD)

    for sq_m in sq_ls:
        if sq_m.being_used and (not sq_m.is_dead):
            dx, dy = x + math.cos(math.radians(d)) * dist_travel, y - math.sin(math.radians(d)) * dist_travel
            tx = int(dx/settings.cell_dimension)
            ty = int(dy/settings.cell_dimension)
            dist_from_squad_member = utilityfuncs.point_distance(sq_m.x, sq_m.y, dx, dy)
            if dist_from_squad_member < 200 and 0 <= ty < map_height and 0 <= tx < map_width:
                if m[ty][tx] == 0:
                    sq_m.set_dest(dx, dy, m)
                    sq_m.focused = True
            d +=  360 / num_active

# Default enemies are mobsters, so health will be a little lower
class Enemy:
    def __init__(self, loc:tuple[float, float], max_hp, exclude=False):
        self.x, self.y = loc
        self.dest_x, self.dest_y = self.x, self.y
        self.state = "IDLE"
        self.exclude = exclude
        self.max_hp = max_hp
        self.hp = max_hp
        self.is_dead = False
        self.repr_name = ""
        # The sound heard by the enemy
        self.sound_heard: entities.SoundSource | None = None
        self.references = []
        if not exclude:
            enemy_list.append(self)


    # Standard
    def action(self):
        pass


    def hear_sound(self, snd:entities.SoundSource):
        dist = utilityfuncs.point_distance(self.x, self.y, snd.x, snd.y)
        if dist < snd.radius:
            if snd.sound_tag == "GUNSHOT":
                self.sound_heard = snd
            elif snd.sound_tag == "ENEMY_DEATH":
                self.sound_heard = snd


    def render(self, dest:pygame.Surface, x, y):
        pass

    def destroy(self):
        entities.SoundSource(self.x, self.y,  150, sound_tag="ENEMY_DEATH")
        for l in self.references:
            deletor.Deleter.request_delete(self, l)
        deletor.Deleter.request_delete(self, enemy_list)


    def check_death(self):
        if self.hp <= 0:
            self.destroy()
            SlowMo.SlowMo.slow_motion_amount_left += SlowMo.SlowMo.slow_motion_max_amount / 5

    # Recommended to override
    def __copy__(self):
        return Enemy((self.x, self.y), self.max_hp, exclude=False)

    def __repr__(self):
        return f"{self.repr_name}->({self.x}, {self.y})"

    # Standard
    def __lt__(self, other):
        return self.y < other.y

    def __gt__(self, other):
        return self.y > other.y

    def __eq__(self, other):
        return self.y == other.y

class EnemyMobster(Enemy):
    def __init__(self, loc:tuple[float, float], exclude=False, weapon_type="Pistol"):
        super().__init__(loc, 50, exclude)

        all_sprites = gen_mobster_sprites()
        self.pistol_sprite = all_sprites["Pistol"]
        self.revolver_sprite = all_sprites["Revolver"]
        self.shotgun_sprite = all_sprites["Shotgun"]
        self.thompson_sprite = all_sprites["Thompson"]
        self.bar_sprite = all_sprites["Bar"]
        self.grenade_sprite = all_sprites["GrenadeLauncher"]
        self.rocket_sprite = all_sprites["RocketLauncher"]
        self.basic_sprite = all_sprites["None"]
        self.sprite = self.thompson_sprite

        self.leg_sprite = all_sprites["LEGS"]

        self.alerted_saw_player = 0

        self.current_weapon_name = weapon_type
        self.current_weapon = WEAPONS_REF[self.current_weapon_name]
        self.move_path = []
        self.faction_color = (255, 0, 0)
        self.repr_name = ""

        self.target_x = 0
        self.target_y = 0

        self.front_direction = 0
        self.aim_direction = 0
        self.speed_factor = 1

        self.variable_space:list = [0] * 15 # 15 slots for different variables
        self.inaccuracy_multiplier = 1
        self.surprise_factor = 90

        self.cooldown = 0
        self.is_firing = False

        self.knock_back_dir = 0
        self.knock_back_strength = 0

    def set_dest(self, x, y, m):
        self.move_path.clear()
        self.dest_x, self.dest_y = x, y
        def conv(val):
            return int(val/settings.cell_dimension)
        self.move_path = pathfind.pathfind(conv(self.x), conv(self.y), conv(self.dest_x), conv(self.dest_y), m)

    def xy(self):
        return self.x, self.y

    def switch_state(self):
        self.variable_space.clear()

    def seeing_enemy(self, enemies:list, m:list[list[int]]):
        fov = 120
        for e in enemies:
            if (not e.is_dead) and utilityfuncs.line_of_sight(self.x, self.y, e.xy()[0], e.xy()[1], m):
                self.target_x = e.xy()[0]
                self.target_y = e.xy()[1]
                direction_to_enemy = utilityfuncs.point_direction(self.x, self.y, e.x, e.y)
                if abs(direction_to_enemy - self.front_direction) < fov/2:
                    self.front_direction = direction_to_enemy # Some extra things
                    return True
        return False

    def enemy_seen(self, enemies:list, m:list[list[int]]):
        for e in enemies:
            if (not e.is_dead) and utilityfuncs.line_of_sight(self.x, self.y, e.xy()[0], e.xy()[1], m):
                return e
        return None

    def clear_variable_space(self):
        for i in range(len(self.variable_space)):
            self.variable_space[i] = 0

    def stop_moving(self):
        self.dest_x, self.dest_y = self.x, self.y
        self.move_path.clear()

    def alert_others(self):
        alert_num = 2
        for e in enemy_list:
            if (not e.is_dead) and utilityfuncs.point_distance(self.x, self.y, e.x, e.y) < 60 and alert_num > 0:
                if utilityfuncs.line_of_sight(self.x, self.y, e.x, e.y, MapData.MAP_GEOMETRY):
                    if type(self) == type(e):
                        e.target_x = self.target_x
                        e.target_y = self.target_y
                        e.front_direction = utilityfuncs.point_direction(e.x, e.y, e.target_x, e.target_y)
                        e.set_dest(self.target_x, self.target_y, MapData.MAP_GEOMETRY) # This works
                        print("Alerted others")
                        alert_num -= 1

    def action(self):
        self.aim_direction = pygame.math.lerp(self.aim_direction, self.front_direction, 0.2)
        self.switch_sprites()
        if self.knock_back_strength >= 0.001:
            self.knock_back_strength *= 0.9
            self.leg_sprite.set_image_speed(4/30)
        else:
            self.knock_back_strength = 0

        if self.state == "IDLE":
            if self.sound_heard is not None:
                self.state = "DECISION"
                self.clear_variable_space()

            if self.seeing_enemy(SquadMan.squad_list, MapData.MAP_GEOMETRY):
                self.state = "ATTACK"
                # self.move_path.clear()
                self.stop_moving()
                self.cooldown = -10
                self.clear_variable_space()
                self.alerted_saw_player = 5
                self.alert_others()

            self.variable_space[0] += 1 * SlowMo.SlowMo.slow_motion_ratio
            if self.variable_space[0] >= 1 * 60:
                self.look_around(45)
                self.variable_space[0] = 0
                self.sprite.set_image_index(int(self.front_direction//45))

        elif self.state == "DECISION":
            # If heard a sound, decide what happens next
            if self.sound_heard is not None:
                # if utilityfuncs.point_distance(self.x, self.y, self.sound_heard.x, self.sound_heard) > 90:
                __x = int(self.sound_heard.x/settings.cell_dimension)
                __y = int(self.sound_heard.y/settings.cell_dimension)
                if MapData.MAP_GEOMETRY[__y][__x] == 0:
                    self.set_dest(self.sound_heard.x, self.sound_heard.y, MapData.MAP_GEOMETRY)
                    self.clear_variable_space()
                    self.sound_heard = None
                    self.state = "MOVE_TO_WHERE_LAST_SEEN_ENEMY"
                    self.set_speed_factor(random.random()*1 + 2)

        elif self.state == "MOVE_TO_WHERE_LAST_SEEN_ENEMY":
            # Using space 1 of variable space to hold cooldown
            # If the enemy cannot legitimately find player anymore, they move around in search of them
            if len(self.move_path) == 0:
                # Temporary Fix
                self.variable_space[14] = True # If didn't see the player anymore
                if self.sound_heard is not None:
                    self.state = "DECISION"
                    self.clear_variable_space()

                self.variable_space[0] += 1 * SlowMo.SlowMo.slow_motion_ratio
                if self.variable_space[0] >= 12 * 60:
                    self.state = "IDLE"
                    self.clear_variable_space()
                else:
                    self.variable_space[1] += 1 * SlowMo.SlowMo.slow_motion_ratio
                    if self.variable_space[1] >= 0.5 * 30 + self.variable_space[2]:
                        # Freakout cooldown
                        self.variable_space[2] += 20 * SlowMo.SlowMo.slow_motion_ratio
                        __search_range = 20
                        self.look_around(45)
                        self.move_forward_a_little(MapData.MAP_GEOMETRY, __search_range)
                        self.variable_space[1] = 0

            # Seeing player then destroy them
            if self.seeing_enemy(SquadMan.squad_list, MapData.MAP_GEOMETRY):
                self.state = "ATTACK"
                self.alerted_saw_player = 5
                # self.inaccuracy_multiplier = self.surprise_factor
                # self.move_path.clear()
                self.stop_moving()
                self.cooldown = 0 # Already expected the enemy
                self.clear_variable_space()
                self.alert_others()

        elif self.state == "ATTACK":
            # Move around a little
            self.inaccuracy_multiplier = max(self.inaccuracy_multiplier * 0.9, 1)
            __d = self.aim_direction# # utilityfuncs.point_direction(self.x, self.y, self.target_x, self.target_y) #
            if self.seeing_enemy(SquadMan.squad_list, MapData.MAP_GEOMETRY):
                self.sprite.set_image_index(int(__d / 45))
                dist_to_target = utilityfuncs.point_distance(self.x, self.y, self.target_x, self.target_y)
                can_fire = True
                if self.current_weapon_name == "RocketLauncher" and dist_to_target < 96:
                    can_fire = False
                if can_fire:
                    self.firing(__d + random.randrange(-1, 1)) #* self.inaccuracy_multiplier)
                self.stop_moving()
            else:
                self.is_firing = False
                self.state = "MOVE_TO_WHERE_LAST_SEEN_ENEMY" # when going to where enemy is last seen, do not have an empty move path
                self.clear_variable_space()
                self.set_dest(self.target_x, self.target_y, MapData.MAP_GEOMETRY)
                self.set_speed_factor(1)
                self.sound_heard = None

        self.movement()
        if self.alerted_saw_player > 0:
            self.alerted_saw_player = max(self.alerted_saw_player - 0.1, 0)

    def look_around(self, _range):
        self.front_direction += random.choice([-_range, _range])
        self.front_direction = max(min(self.front_direction, 360), 0)
        if self.front_direction >= 360:
            self.front_direction = 0

    def move_forward_a_little(self, m:list[list[int]], search_range=16):
        __x = self.x + math.cos(math.radians(self.front_direction)) * search_range
        __y = self.y - math.sin(math.radians(self.front_direction)) * search_range
        self.set_speed_factor(1)
        if m[int(__y / settings.cell_dimension)][int(__x / settings.cell_dimension)] != 0:
            return False
        else:
            self.set_dest(__x, __y, m)
            return True

    def set_speed_factor(self, spd:float):
        self.speed_factor = spd

    def firing(self, direction):
        fire_gun(self, direction)

    def hear_sound(self, snd:entities.SoundSource):
        # chance = random.randint(0, 100)
        # if chance < 33:
        dist = utilityfuncs.point_distance(self.x, self.y, snd.x, snd.y)
        if dist < snd.radius:
            if snd.sound_tag == "GUNSHOT":
                self.sound_heard = snd
            elif snd.sound_tag == "ENEMY_DEATH":
                self.sound_heard  = snd

    def get_weapon(self):
        return self.current_weapon

    def get_weapon_name(self):
        return self.current_weapon_name

    ## Pathfinding wing
    def movement(self):
        if len(self.move_path) == 0:
            if utilityfuncs.point_distance(self.dest_x, self.dest_y, self.x, self.y) > 5:
                dir_ = utilityfuncs.point_direction(self.x, self.y, self.dest_x, self.dest_y)
                self.front_direction = dir_
                self.x += math.cos(math.radians(dir_)) * 0.5 * self.get_weapon().speed_modifier * 0.8 * SlowMo.SlowMo.slow_motion_ratio
                self.y -= math.sin(math.radians(dir_)) * 0.5 * self.get_weapon().speed_modifier * 0.8 * SlowMo.SlowMo.slow_motion_ratio
            else:
                self.dest_x, self.dest_y = self.x, self.y
                self.leg_sprite.set_image_index(2)
                self.leg_sprite.set_image_speed(0)
        else:
            x, y = (self.move_path[0][0] * settings.cell_dimension + settings.cell_dimension/2
                        , self.move_path[0][1] * settings.cell_dimension + settings.cell_dimension/2 - 2.5)

            if utilityfuncs.point_distance(self.x, self.y, x, y) > 5:
                dir_ = utilityfuncs.point_direction(self.x, self.y, x, y)
                self.front_direction = dir_
                if not self.is_firing:
                    self.sprite.set_image_index(dir_//45)
                self.x += math.cos(math.radians(dir_)) * 0.5 * self.speed_factor * SlowMo.SlowMo.slow_motion_ratio
                self.y -= math.sin(math.radians(dir_)) * 0.5 * self.speed_factor * SlowMo.SlowMo.slow_motion_ratio
            else:
                self.move_path.pop(0)

            self.leg_sprite.run_sprite()
            self.leg_sprite.set_image_speed(4/30)
            if self.leg_sprite.image_index > 2:
                self.leg_sprite.image_index = 0


    def set_xy(self, loc:tuple[float, float]):
        self.x, self.y = loc
        self.dest_x, self.dest_y = loc

    def switch_sprites(self):
        switch_sprite(self)

    def render(self, dest:pygame.Surface, x, y):
        vec_x = math.cos(math.radians(self.knock_back_dir)) * self.knock_back_strength
        vec_y = math.sin(math.radians(self.knock_back_dir)) * self.knock_back_strength
        x += vec_x
        y -= vec_y
        self.switch_sprites()
        dest.blit(self.sprite.get_current_image(), self.sprite.get_current_image().get_rect(center=(x, y)), None)
        dest.blit(self.leg_sprite.get_current_image(), self.leg_sprite.get_current_image().get_rect(center=(x, y)))
        pygame.draw.rect(dest, (255, 0, 0), (x-5, y-9, 10, 2))
        pygame.draw.rect(dest, (0, 255, 0), (x-5, y-9, 10*self.hp/self.max_hp, 2))

        # Alerted
        if self.alerted_saw_player > 0:
            alr_spr = pygame.transform.scale_by(ALL_SPRITES.ASP["ALERTED0"], 0.25)
            fluctuate = random.randint(0, 100)
            if fluctuate <= 50:
                alr_spr = ALL_SPRITES.ASP["ALERTED1"]
            alr_rect = alr_spr.get_rect(center=(x, y-8))
            dest.blit(alr_spr, alr_rect)

    def get_hitbox(self):
        return self.sprite.get_current_image().get_rect(center=(self.x, self.y))

    def take_damage(self, amount, source):
        source_dir = random.random() * 360
        if source_dir is not None:
            source_dir = utilityfuncs.point_direction(self.x, self.y, source.x, source.y)
        damage_multiplier = (abs(self.front_direction - source_dir) / 180) * 1.25 + 1
        self.hp -= amount * damage_multiplier
        self.front_direction = source_dir
        # self.inaccuracy_multiplier = (self.surprise_factor/3) * damage_multiplier

        num_splots = int(1 + amount / 20)
        for i in range(num_splots):
            r = random.randrange(6, 23) + 2 * (amount / 32)
            _rd = random.randrange(-11, 11)
            vec_x = math.cos(math.radians(source_dir+_rd+180)) * r
            vec_y = math.sin(math.radians(source_dir+_rd+180)) * r
            effects.BloodSplot(self.x + vec_x, self.y - vec_y)

    def knockback(self, strength, knock_dir):
        self.knock_back_dir = knock_dir
        self.knock_back_strength = strength


    def __copy__(self):
        return EnemyMobster((self.x, self.y), exclude=False, weapon_type=self.current_weapon_name)

    def __repr__(self):
        return f"{self.repr_name}->({self.x}, {self.y})"

# Make the enemies' reaction speeds scale to the danger of the situation.
class EnemySoldier(Enemy):
    def __init__(self, loc:tuple[float, float], exclude=False, weapon_type="Pistol"):
        super().__init__(loc, 100, exclude)

        all_sprites = gen_soldier_sprites()
        self.pistol_sprite = all_sprites["Pistol"]
        self.revolver_sprite = all_sprites["Revolver"]
        self.shotgun_sprite = all_sprites["Shotgun"]
        self.thompson_sprite = all_sprites["Thompson"]
        self.bar_sprite = all_sprites["Bar"]
        self.grenade_sprite = all_sprites["GrenadeLauncher"]
        self.rocket_sprite = all_sprites["RocketLauncher"]
        self.basic_sprite = all_sprites["None"]
        self.sprite = self.thompson_sprite

        self.leg_sprite = all_sprites["LEGS"]

        self.deaths_heard = 0

        self.alerted_saw_player = 0

        self.current_weapon_name = weapon_type
        self.current_weapon = WEAPONS_REF[self.current_weapon_name]
        self.move_path = []
        self.faction_color = (255, 0, 0)
        self.repr_name = ""

        self.target_x = 0
        self.target_y = 0
        self.initial_x, self.initial_y = self.x, self.y # Initial positions
        self.target_obj : SquadMan|None = None

        self.front_direction = random.random() * 360
        self.aim_direction = 0
        self.speed_factor = 1
        self.is_stopping = False

        self.variable_space:list = [0] * 15 # 15 slots for different variables
        self.inaccuracy_multiplier = 1
        self.surprise_factor = 90

        self.cooldown = 0
        self.is_firing = False

        self.knock_back_dir = 0
        self.knock_back_strength = 0

        self.pain_amount = 0

    def set_dest(self, x, y, m):
        self.move_path.clear()
        self.dest_x, self.dest_y = x, y
        def conv(val):
            return int(val/settings.cell_dimension)
        self.move_path = pathfind.pathfind(conv(self.x), conv(self.y), conv(self.dest_x), conv(self.dest_y), m)

    def xy(self):
        return self.x, self.y

    def switch_state(self):
        self.variable_space.clear()

    def seeing_enemy(self, enemies:list, m:list[list[int]], fov=180):
        for e in enemies:
            if (not e.is_dead) and utilityfuncs.line_of_sight(self.x, self.y, e.xy()[0], e.xy()[1], m):
                self.target_x = e.xy()[0]
                self.target_y = e.xy()[1]
                self.target_obj = e
                direction_to_enemy = utilityfuncs.point_direction(self.x, self.y, e.x, e.y)
                if abs(direction_to_enemy - self.front_direction) < fov/2:
                    self.front_direction = direction_to_enemy # Some extra things
                    return True
        return False

    def enemy_seen(self, enemies:list, m:list[list[int]]):
        for e in enemies:
            if (not e.is_dead) and utilityfuncs.line_of_sight(self.x, self.y, e.xy()[0], e.xy()[1], m):
                return e
        return None

    def clear_variable_space(self):
        for i in range(len(self.variable_space)):
            self.variable_space[i] = 0

    def stop_moving(self):
        self.dest_x, self.dest_y = self.x, self.y
        self.move_path.clear()

    def alert_others(self):
        alert_num = 2
        for e in enemy_list:
            if type(e) == type(self):
                enemy_not_alerted_already = e.target_obj is None
                enemy_not_making_a_move_already = len(e.move_path) == 0
                enemy_not_dead = not e.is_dead
                can_call_enemy = utilityfuncs.point_distance(self.x, self.y, e.x, e.y) < 60
                maximum_enemies_alerted = alert_num > 0
                if enemy_not_alerted_already and enemy_not_dead and can_call_enemy and maximum_enemies_alerted \
                        and enemy_not_making_a_move_already:
                    if utilityfuncs.line_of_sight(self.x, self.y, e.x, e.y, MapData.MAP_GEOMETRY):
                        e.target_x = self.target_x
                        e.target_y = self.target_y
                        e.front_direction = utilityfuncs.point_direction(e.x, e.y, e.target_x, e.target_y)
                        e.set_dest(self.target_x, self.target_y, MapData.MAP_GEOMETRY) # This works
                        print("Alerted others")
                        alert_num -= 1

    def action(self):
        self.aim_direction = pygame.math.lerp(self.aim_direction, self.front_direction, 0.1)
        __d = int(self.aim_direction/45)
        self.switch_sprites()
        self.sprite.set_image_index(__d)
        if self.hp < self.max_hp/2:
            self.hp = min(self.hp + 0.2 * (1 - (self.pain_amount / 200)), self.max_hp)
        self.pain_amount = min(max(self.pain_amount - 0.1, 0), 200)
        self.alerted_saw_player = max(self.alerted_saw_player - 0.1, 0)

        if self.knock_back_strength >= 0.001:
            self.knock_back_strength *= 0.9
            self.leg_sprite.set_image_speed(4/30)
        else:
            self.knock_back_strength = 0

        # ALL THE FUNCTIONS AND TOOLS AT YOUR DISPOSAL
        # self.state                - state of the player
        # self.move_path            - movement path
        # self.seeing_enemy()       - sets the target coordinates of the player if seen
        # self.sound_heard          - any sound that is heard will be set to something not None
        # self.alert_otherS()       - alerting other soldiers of the type
        # self.variable_space       - any temporary variables that are persistent and needs storage will be put here.
        # self.clear_variable_space - turning all variable spaces to 0
        # self.look_around          - wondering.
        # self.cooldown             - cooldown of the
        # self.set_speed_factor     - sets the factor that the speed will be multiplied by
        # self.set_dest             - setting the destination for where the enemy object will be headed
        #
        # STATES:
        # "IDLE" - the starting state for everything
        #
        # CONVENTIONS:
        # if self.sound_heard is not None: -> if there is a sound.

        if self.state == "IDLE":
            if self.sound_heard is not None: # Heard a sound
                # Clearing the variable space, just in case
                self.clear_variable_space()
                sound = self.sound_heard
                # Move to Sound
                self.front_direction = utilityfuncs.point_direction(self.x, self.y, sound.x + random.randrange(-16, 16), sound.y + random.randrange(-16, 16))
                self.set_dest(sound.x, sound.y, MapData.MAP_GEOMETRY)
                self.set_speed_factor(1.5)
                self.state = "SCOUT_OUT0" if sound.sound_tag != "ENEMY_DEATH" else "SCOUT_OUT2"
                self.sound_heard = None
            # Looking around
            if self.variable_space[0] >= random.random() * 60 + 60:
                self.look_around(45)
                self.variable_space[0] = 0
            else:
                self.variable_space[0] += 1 * SlowMo.SlowMo.slow_motion_ratio

        elif self.state == "SCOUT_OUT0": # Stop for a second
            # Assuming a destination has been set
            self.is_stopping = True
            if self.variable_space[0] > 30:
                self.clear_variable_space()
                self.state = "SCOUT_OUT1"
            else:
                self.variable_space[0] += 1 * SlowMo.SlowMo.slow_motion_ratio

        elif self.state == "SCOUT_OUT1":
            # Going towards the destination, stopping if around the corner is the sound source
            # Use variable space as transition between states
            if self.variable_space[0] == 0:
                self.is_stopping = False
                if len(self.move_path) > 0:
                    check_index = 0
                    if len(self.move_path) > 1:
                        check_index = 1
                    vertex = self.move_path[check_index]
                    vertex_x = vertex[0] * settings.cell_dimension + settings.cell_dimension / 2
                    vertex_y = vertex[1] * settings.cell_dimension + settings.cell_dimension / 2
                    if utilityfuncs.line_of_sight(self.dest_x, self.dest_y, vertex_x, vertex_y, MapData.MAP_GEOMETRY):
                        self.variable_space[0] = 15
            else:
                self.is_stopping = True
                if self.variable_space[1] < 1 * 60:
                    self.variable_space[1] += 1 * SlowMo.SlowMo.slow_motion_ratio
                else:
                    self.clear_variable_space()
                    self.state = "SCOUT_OUT2"

        elif self.state == "SCOUT_OUT2":
            self.is_stopping = False
            # Run outside to see if there's an enemy
            if self.variable_space[0] == 0:
                # Waiting around the corner, and run out to see if there's an enemy.
                # See the spot. If there's an enemy, attack. Else, go to the spot.
                if not utilityfuncs.line_of_sight(self.x, self.y, self.dest_x, self.dest_y, MapData.MAP_GEOMETRY):
                    self.set_speed_factor(2)
                else:
                    if self.variable_space[1] > 60:
                        self.is_stopping = False
                        self.set_speed_factor(2)
                        self.variable_space[0] = 15
                    else:
                        self.variable_space[1] += 1 * SlowMo.SlowMo.slow_motion_ratio
                        self.is_stopping = True
            else:
                # Go to the path after doing stuff. If there is a destination.
                if self.variable_space[2] > 3 * 60:
                    self.is_stopping = False
                    if len(self.move_path) == 0:
                        self.clear_variable_space()
                        self.state = "WANDER"
                else:
                    self.variable_space[2] += 1 * SlowMo.SlowMo.slow_motion_ratio
        elif self.state == "MOVE_TO_WHERE_LAST_SEEN_ENEMY":
            if self.target_obj is not None:
                self.is_stopping = False
                # Try and predict the position of the enemy where they'd last been seen (getting their path information)
                if self.variable_space[0] == 0:
                    if len(self.target_obj.move_path) > 0:
                        e_move_path = self.target_obj.move_path
                        cutoff_vertex = e_move_path[int(len(e_move_path)//1.8)]
                        self.set_dest(cutoff_vertex[0] * settings.cell_dimension + settings.cell_dimension//2,
                                      cutoff_vertex[1] * settings.cell_dimension + settings.cell_dimension//2,
                                      MapData.MAP_GEOMETRY)
                    else:
                        self.set_dest(self.target_x, self.target_y, MapData.MAP_GEOMETRY)
                    self.variable_space[0] = 15
                    self.set_speed_factor(2)
                else:
                    # If at the end of the road, not finding anything, look around.
                    # IF haven't found anyone, then lost track of enemy
                    if len(self.move_path) == 0:
                        if self.variable_space[1] < 4 * 60:
                            self.variable_space[1] += 1 * SlowMo.SlowMo.slow_motion_ratio
                            self.set_speed_factor(1)
                        else:
                            self.target_obj = None
                            self.state = "WANDER"
                            self.clear_variable_space()
            else:
                self.target_obj = None
                self.state = "WANDER"
                self.clear_variable_space()

        elif self.state == "WANDER":
            if self.variable_space[0] > 6 * 60:
                self.target_obj = None
                self.state = "IDLE"
                self.clear_variable_space()
            else:
                self.variable_space[0] += 1 * SlowMo.SlowMo.slow_motion_ratio
                self.variable_space[1] += 1 * SlowMo.SlowMo.slow_motion_ratio
                if self.variable_space[1] > random.random() * 60 + 15:
                    self.move_forward_a_little(MapData.MAP_GEOMETRY, 20)
                    self.look_around(45)
                    self.variable_space[1] = 0

        elif self.state == "ATTACK":
            # self.stop_moving()
            # Move around a little
            self.inaccuracy_multiplier = max(self.inaccuracy_multiplier * 0.9, 1)
            __d = self.aim_direction
            if self.seeing_enemy(SquadMan.squad_list, MapData.MAP_GEOMETRY):
                self.sprite.set_image_index(int(__d / 45))
                self.firing(__d + random.randrange(-1, 1)) #* self.inaccuracy_multiplier)
                if self.target_obj is not None:
                    if self.target_obj.is_dead:
                        self.state = "MOVE_TO_WHERE_LAST_SEEN_ENEMY"
                        self.set_dest(self.target_obj.x, self.target_obj.y, MapData.MAP_GEOMETRY)
                self.stop_moving()
            else:
                self.is_firing = False
                self.state = "MOVE_TO_WHERE_LAST_SEEN_ENEMY" # when going to where enemy is last seen, do not have an empty move path
                self.clear_variable_space()
                self.set_speed_factor(1)
                self.sound_heard = None

        # Any sounds heard, report back to IDLE
        if self.seeing_enemy(SquadMan.squad_list, MapData.MAP_GEOMETRY):
            self.state = "ATTACK"
            self.clear_variable_space()
            self.alert_others()

        if self.sound_heard is not None:
            if self.sound_heard.sound_tag == "ENEMY_DEATH":
                sound = self.sound_heard
                self.seeing_enemy(SquadMan.squad_list, MapData.MAP_GEOMETRY, fov=360)
                # self.state = "MOVE_TO_WHERE_LAST_SEEN_ENEMY"
                if utilityfuncs.point_distance(self.x, self.y, sound.x, sound.y) < 75:
                    self.set_dest(sound.x, sound.y, MapData.MAP_GEOMETRY)
                    self.state = "IDLE"
            else:
                if self.state != "ATTACK": # So that enemies do not automatically retreat back into non-combat state
                    if len(self.move_path) == 0:
                        self.state = "IDLE"

        if not self.is_stopping:
            self.movement()
        if self.alerted_saw_player > 0:
            self.alerted_saw_player = max(self.alerted_saw_player - 0.1 * SlowMo.SlowMo.slow_motion_ratio, 0)

    def look_around(self, _range):
        self.front_direction += random.choice([-_range, _range])
        self.front_direction = max(min(self.front_direction, 360), 0)
        if self.front_direction >= 360:
            self.front_direction = 0

    def move_forward_a_little(self, m:list[list[int]], search_range=16):
        __x = self.x + math.cos(math.radians(self.front_direction)) * search_range
        __y = self.y - math.sin(math.radians(self.front_direction)) * search_range
        self.set_speed_factor(1)
        if m[int(__y / settings.cell_dimension)][int(__x / settings.cell_dimension)] != 0:
            return False
        else:
            self.set_dest(__x, __y, m)
            return True

    def set_speed_factor(self, spd:float):
        self.speed_factor = spd

    def firing(self, direction):
        fire_gun(self, direction)

    def hear_sound(self, snd:entities.SoundSource):
        # chance = random.randint(0, 100)
        # if chance < 33:
        dist = utilityfuncs.point_distance(self.x, self.y, snd.x, snd.y)
        if dist < snd.radius:
            if snd.sound_tag == "GUNSHOT":
                self.sound_heard = snd
            elif snd.sound_tag == "ENEMY_DEATH":
                self.sound_heard  = snd

    def get_weapon(self):
        return self.current_weapon

    def get_weapon_name(self):
        return self.current_weapon_name

    ## Pathfinding wing
    def movement(self):
        if len(self.move_path) == 0:
            if utilityfuncs.point_distance(self.dest_x, self.dest_y, self.x, self.y) > 5:
                dir_ = utilityfuncs.point_direction(self.x, self.y, self.dest_x, self.dest_y)
                self.front_direction = dir_
                self.x += math.cos(math.radians(dir_)) * 0.5 * self.get_weapon().speed_modifier * 0.8 * SlowMo.SlowMo.slow_motion_ratio
                self.y -= math.sin(math.radians(dir_)) * 0.5 * self.get_weapon().speed_modifier * 0.8 * SlowMo.SlowMo.slow_motion_ratio
            else:
                self.dest_x, self.dest_y = self.x, self.y
                self.leg_sprite.set_image_index(2)
                self.leg_sprite.set_image_speed(0)
        else:
            x, y = (self.move_path[0][0] * settings.cell_dimension + settings.cell_dimension/2
                        , self.move_path[0][1] * settings.cell_dimension + settings.cell_dimension/2 - 2.5)

            if utilityfuncs.point_distance(self.x, self.y, x, y) > 5:
                dir_ = utilityfuncs.point_direction(self.x, self.y, x, y)
                self.front_direction = dir_
                if not self.is_firing:
                    self.sprite.set_image_index(dir_//45)
                self.x += math.cos(math.radians(dir_)) * 0.5 * self.speed_factor * SlowMo.SlowMo.slow_motion_ratio
                self.y -= math.sin(math.radians(dir_)) * 0.5 * self.speed_factor * SlowMo.SlowMo.slow_motion_ratio
            else:
                self.move_path.pop(0)

            self.leg_sprite.run_sprite()
            self.leg_sprite.set_image_speed(4/30)
            if self.leg_sprite.image_index > 2:
                self.leg_sprite.image_index = 0


    def set_xy(self, loc:tuple[float, float]):
        self.x, self.y = loc
        self.dest_x, self.dest_y = loc

    def switch_sprites(self):
        switch_sprite(self)

    def render(self, dest:pygame.Surface, x, y):
        vec_x = math.cos(math.radians(self.knock_back_dir)) * self.knock_back_strength
        vec_y = math.sin(math.radians(self.knock_back_dir)) * self.knock_back_strength
        x += vec_x
        y -= vec_y
        self.switch_sprites()
        dest.blit(self.sprite.get_current_image(), self.sprite.get_current_image().get_rect(center=(x, y)), None)
        dest.blit(self.leg_sprite.get_current_image(), self.leg_sprite.get_current_image().get_rect(center=(x, y)))
        pygame.draw.rect(dest, (255, 0, 0), (x-5, y-9, 10, 2))
        pygame.draw.rect(dest, (0, 255, 0), (x-5, y-9, 10*self.hp/self.max_hp, 2))

        # Alerted
        if self.alerted_saw_player > 0:
            alr_spr = pygame.transform.scale_by(ALL_SPRITES.ASP["ALERTED0"], 0.25)
            fluctuate = random.randint(0, 100)
            if fluctuate <= 50:
                alr_spr = ALL_SPRITES.ASP["ALERTED1"]
            alr_rect = alr_spr.get_rect(center=(x, y-8))
            dest.blit(alr_spr, alr_rect)

    def get_hitbox(self):
        return self.sprite.get_current_image().get_rect(center=(self.x, self.y))

    def take_damage(self, amount, source):
        source_dir = random.random() * 360
        if source_dir is not None:
            source_dir = utilityfuncs.point_direction(self.x, self.y, source.x, source.y)
        damage_multiplier = (abs(self.front_direction - source_dir) / 180) * 1.25 + 1
        self.hp -= amount * damage_multiplier
        self.front_direction = source_dir
        self.pain_amount += amount/2

        num_splots = int(1 + amount / 20)
        for i in range(num_splots):
            r = random.randrange(6, 23) + 2 * (amount / 32)
            _rd = random.randrange(-11, 11)
            vec_x = math.cos(math.radians(source_dir+_rd+180)) * r
            vec_y = math.sin(math.radians(source_dir+_rd+180)) * r
            effects.BloodSplot(self.x + vec_x, self.y - vec_y)

    def knockback(self, strength, knock_dir):
        self.knock_back_dir = knock_dir
        self.knock_back_strength = strength


    def __copy__(self):
        return EnemySoldier((self.x, self.y), exclude=False, weapon_type=self.current_weapon_name)

    def __repr__(self):
        return f"{self.repr_name}->({self.x}, {self.y})"

all_enemies_type = EnemyMobster


def enemies_generator(): # CAN ONLY BE USED IF A VIDEO MODE HAS BEEN SET
    if pygame.display.get_init():
        misc_objs_dict = {
            "EnemyMobsterPistol": EnemyMobster((0, 0), weapon_type="Pistol", exclude=True),
            "EnemyMobsterRevolver": EnemyMobster((0, 0), weapon_type="Revolver", exclude=True),
            "EnemyMobsterShotgun": EnemyMobster((0, 0), weapon_type="Shotgun", exclude=True),
            "EnemyMobsterThompson": EnemyMobster((0, 0), weapon_type="Thompson", exclude=True),
            "EnemyMobsterBar": EnemyMobster((0, 0), weapon_type="Bar", exclude=True),
            "EnemyMobsterRocketLauncher" : EnemyMobster((0, 0), weapon_type="RocketLauncher", exclude=True),
            "EnemyMobsterGrenadeLauncher" : EnemyMobster((0, 0), weapon_type="GrenadeLauncher", exclude=True),
            "EnemySoldierPistol" : EnemySoldier((0, 0), weapon_type="Pistol", exclude=True),
            "EnemySoldierShotgun": EnemySoldier((0, 0), weapon_type="Shotgun", exclude=True),
            "EnemySoldierThompson": EnemySoldier((0, 0), weapon_type="Thompson", exclude=True),
            "EnemySoldierRevolver": EnemySoldier((0, 0), weapon_type="Revolver", exclude=True),
            "EnemySoldierBar": EnemySoldier((0, 0), weapon_type="Bar", exclude=True),
            "EnemySoldierRocketLauncher": EnemySoldier((0, 0), weapon_type="RocketLauncher", exclude=True),
            "EnemySoldierGrenadeLauncher": EnemySoldier((0, 0), weapon_type="GrenadeLauncher", exclude=True),
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
