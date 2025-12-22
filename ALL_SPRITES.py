import pygame
pygame.init()

# Dummy screen
srf = pygame.display.set_mode((1,1), pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE|pygame.NOFRAME|pygame.SCALED,vsync=1) # this will close

ASP:dict[str, pygame.Surface] = {
    # barrel_spr
    "BARREL_BODY" : pygame.image.load("sprites/barrel_spr/barrel_body.png"),
    "BARREL_BROKEN": pygame.image.load("sprites/barrel_spr/barrel_broken.png").convert_alpha(),
    "BARREL_TOP": pygame.image.load("sprites/barrel_spr/barrel_top.png").convert_alpha(),
    "BARREL_TOP_BROKEN": pygame.image.load("sprites/barrel_spr/barrel_top_broken.png").convert_alpha(),

    # bullet_hole_spr
    "HOLE_1": pygame.image.load("sprites/bullet_hole_spr/hole1.png").convert_alpha(),
    "HOLE_2": pygame.image.load("sprites/bullet_hole_spr/hole2.png").convert_alpha(),
    "HOLE_3": pygame.image.load("sprites/bullet_hole_spr/hole3.png").convert_alpha(),

    # crack_spr
    "CRACK_1": pygame.image.load("sprites/crack_spr/crack1.png").convert_alpha(),
    "CRACK_2": pygame.image.load("sprites/crack_spr/crack2.png").convert_alpha(),
    "CRACK_3": pygame.image.load("sprites/crack_spr/crack3.png").convert_alpha(),

    # crate-spr
    "CRATE_BODY" : pygame.image.load("sprites/crate_spr/crate_body.png").convert_alpha(),
    "CRATE_BODY_BROKEN": pygame.image.load("sprites/crate_spr/crate_body_broken.png").convert_alpha(),
    "CRATE_NORMAL_TOP": pygame.image.load("sprites/crate_spr/crate_normal_top.png").convert_alpha(),
    "CRATE_NORMAL_TOP_BROKEN": pygame.image.load("sprites/crate_spr/crate_normal_top_broken.png").convert_alpha(),
    "CRATE_WEAPONS_BROKEN_TOP": pygame.image.load("sprites/crate_spr/crate_weapons_broken_top.png").convert_alpha(),
    "CRATE_WEAPONS_TOP": pygame.image.load("sprites/crate_spr/crate_weapons_top.png").convert_alpha(),

    # grenade_spr
    "GRENADE" : pygame.image.load("sprites/grenade_spr/grenade.png").convert_alpha(),

    # level_tiles
    "CONCRETE": pygame.image.load("sprites/level_tiles/concrete.png").convert(),
    "DIRTY_BRICK": pygame.image.load("sprites/level_tiles/dirty_brick.png").convert(),
    "EMPTY": pygame.image.load("sprites/level_tiles/empty.png").convert(),
    "NO_ACCESS": pygame.image.load("sprites/level_tiles/NO_ACCESS.png").convert(),
    "NORMAL_BRICK": pygame.image.load("sprites/level_tiles/normal_brick.png").convert(),
    "SHINY_BRICK": pygame.image.load("sprites/level_tiles/shiny_brick.png").convert(),

    # mob_spr (oh boy)
    "MOBSTER": pygame.image.load("sprites/mob_spr/mobster.png").convert_alpha(),
    "MOBSTER_LEG_CROUCHING_LEFT": pygame.image.load("sprites/mob_spr/mobster_leg_crouching_left.png").convert_alpha(),
    "MOBSTER_LEG_CROUCHING_RIGHT": pygame.image.load("sprites/mob_spr/mobster_leg_crouching_right.png").convert_alpha(),
    "MOBSTER_LEG_LEFTUP": pygame.image.load("sprites/mob_spr/mobster_leg_leftup.png").convert_alpha(),
    "MOBSTER_LEG_NORMAL": pygame.image.load("sprites/mob_spr/mobster_leg_normal.png").convert_alpha(),
    "MOBSTER_LEG_RIGHTUP": pygame.image.load("sprites/mob_spr/mobster_leg_rightup.png").convert_alpha(),
    "MOBSTER_TORSO": pygame.image.load("sprites/mob_spr/mobster_torso.png").convert_alpha(),
    "MOBSTER_TORSO_0BAR": pygame.image.load("sprites/mob_spr/mobster_torso_0bar.png").convert_alpha(),
    "MOBSTER_TORSO_0PISTOL": pygame.image.load("sprites/mob_spr/mobster_torso_0pistol.png").convert_alpha(),
    "MOBSTER_TORSO_0SHOTGUN": pygame.image.load("sprites/mob_spr/mobster_torso_0shotgun.png").convert_alpha(),
    "MOBSTER_TORSO_0THOMPSON": pygame.image.load("sprites/mob_spr/mobster_torso_0thompson.png").convert_alpha(),
    "MOBSTER_TORSO_45BAR": pygame.image.load("sprites/mob_spr/mobster_torso_45bar.png").convert_alpha(),
    "MOBSTER_TORSO_45PISTOL": pygame.image.load("sprites/mob_spr/mobster_torso_45pistol.png").convert_alpha(),
    "MOBSTER_TORSO_45SHOTGUN": pygame.image.load("sprites/mob_spr/mobster_torso_45shotgun.png").convert_alpha(),
    "MOBSTER_TORSO_45THOMPSON": pygame.image.load("sprites/mob_spr/mobster_torso_45thompson.png").convert_alpha(),
    "MOBSTER_TORSO_90BAR": pygame.image.load("sprites/mob_spr/mobster_torso_90bar.png").convert_alpha(),
    "MOBSTER_TORSO_90PISTOL": pygame.image.load("sprites/mob_spr/mobster_torso_90pistol.png").convert_alpha(),
    "MOBSTER_TORSO_90SHOTGUN": pygame.image.load("sprites/mob_spr/mobster_torso_90shotgun.png").convert_alpha(),
    "MOBSTER_TORSO_90THOMPSON": pygame.image.load("sprites/mob_spr/mobster_torso_90thompson.png").convert_alpha(),
    "MOBSTER_TORSO_135BAR": pygame.image.load("sprites/mob_spr/mobster_torso_135bar.png").convert_alpha(),
    "MOBSTER_TORSO_135PISTOL": pygame.image.load("sprites/mob_spr/mobster_torso_135pistol.png").convert_alpha(),
    "MOBSTER_TORSO_135SHOTGUN": pygame.image.load("sprites/mob_spr/mobster_torso_135shotgun.png").convert_alpha(),
    "MOBSTER_TORSO_135THOMPSON": pygame.image.load("sprites/mob_spr/mobster_torso_135thompson.png").convert_alpha(),
    "MOBSTER_TORSO_180BAR": pygame.image.load("sprites/mob_spr/mobster_torso_180bar.png").convert_alpha(),
    "MOBSTER_TORSO_180PISTOL": pygame.image.load("sprites/mob_spr/mobster_torso_180pistol.png").convert_alpha(),
    "MOBSTER_TORSO_180SHOTGUN": pygame.image.load("sprites/mob_spr/mobster_torso_180shotgun.png").convert_alpha(),
    "MOBSTER_TORSO_180THOMPSON": pygame.image.load("sprites/mob_spr/mobster_torso_180thompson.png").convert_alpha(),
    "MOBSTER_TORSO_225BAR": pygame.image.load("sprites/mob_spr/mobster_torso_225bar.png").convert_alpha(),
    "MOBSTER_TORSO_225PISTOL": pygame.image.load("sprites/mob_spr/mobster_torso_225pistol.png").convert_alpha(),
    "MOBSTER_TORSO_225SHOTGUN": pygame.image.load("sprites/mob_spr/mobster_torso_225shotgun.png").convert_alpha(),
    "MOBSTER_TORSO_225THOMPSON": pygame.image.load("sprites/mob_spr/mobster_torso_225thompson.png").convert_alpha(),
    "MOBSTER_TORSO_270BAR": pygame.image.load("sprites/mob_spr/mobster_torso_270bar.png").convert_alpha(),
    "MOBSTER_TORSO_270PISTOL": pygame.image.load("sprites/mob_spr/mobster_torso_270pistol.png").convert_alpha(),
    "MOBSTER_TORSO_270SHOTGUN": pygame.image.load("sprites/mob_spr/mobster_torso_270shotgun.png").convert_alpha(),
    "MOBSTER_TORSO_270THOMPSON": pygame.image.load("sprites/mob_spr/mobster_torso_270thompson.png").convert_alpha(),
    "MOBSTER_TORSO_315BAR": pygame.image.load("sprites/mob_spr/mobster_torso_315bar.png").convert_alpha(),
    "MOBSTER_TORSO_315PISTOL": pygame.image.load("sprites/mob_spr/mobster_torso_315pistol.png").convert_alpha(),
    "MOBSTER_TORSO_315SHOTGUN": pygame.image.load("sprites/mob_spr/mobster_torso_315shotgun.png").convert_alpha(),
    "MOBSTER_TORSO_315THOMPSON": pygame.image.load("sprites/mob_spr/mobster_torso_315thompson.png").convert_alpha(),

    # soldier_spr
    "SOLDIER_BASIC": pygame.image.load("sprites/soldier_spr/soldier_basic.png").convert_alpha(),

    "SOLDIER_0_PISTOL": pygame.image.load("sprites/soldier_spr/soldier_0_pistol.png").convert_alpha(),
    "SOLDIER_45_PISTOL": pygame.image.load("sprites/soldier_spr/soldier_45_pistol.png").convert_alpha(),
    "SOLDIER_90_PISTOL": pygame.image.load("sprites/soldier_spr/soldier_90_pistol.png").convert_alpha(),
    "SOLDIER_135_PISTOL": pygame.image.load("sprites/soldier_spr/soldier_135_pistol.png").convert_alpha(),
    "SOLDIER_180_PISTOL": pygame.image.load("sprites/soldier_spr/soldier_180_pistol.png").convert_alpha(),
    "SOLDIER_225_PISTOL": pygame.image.load("sprites/soldier_spr/soldier_225_pistol.png").convert_alpha(),
    "SOLDIER_270_PISTOL": pygame.image.load("sprites/soldier_spr/soldier_270_pistol.png").convert_alpha(),
    "SOLDIER_315_PISTOL": pygame.image.load("sprites/soldier_spr/soldier_315_pistol.png").convert_alpha(),

    "SOLDIER_0_REVOLVER": pygame.image.load("sprites/soldier_spr/soldier_0_revolver.png").convert_alpha(),
    "SOLDIER_45_REVOLVER": pygame.image.load("sprites/soldier_spr/soldier_45_revolver.png").convert_alpha(),
    "SOLDIER_90_REVOLVER": pygame.image.load("sprites/soldier_spr/soldier_90_revolver.png").convert_alpha(),
    "SOLDIER_135_REVOLVER": pygame.image.load("sprites/soldier_spr/soldier_135_revolver.png").convert_alpha(),
    "SOLDIER_180_REVOLVER": pygame.image.load("sprites/soldier_spr/soldier_180_revolver.png").convert_alpha(),
    "SOLDIER_225_REVOLVER": pygame.image.load("sprites/soldier_spr/soldier_225_revolver.png").convert_alpha(),
    "SOLDIER_270_REVOLVER": pygame.image.load("sprites/soldier_spr/soldier_270_revolver.png").convert_alpha(),
    "SOLDIER_315_REVOLVER": pygame.image.load("sprites/soldier_spr/soldier_315_revolver.png").convert_alpha(),

    "SOLDIER_0_SHOTGUN": pygame.image.load("sprites/soldier_spr/soldier_0_shotgun.png").convert_alpha(),
    "SOLDIER_45_SHOTGUN": pygame.image.load("sprites/soldier_spr/soldier_45_shotgun.png").convert_alpha(),
    "SOLDIER_90_SHOTGUN": pygame.image.load("sprites/soldier_spr/soldier_90_shotgun.png").convert_alpha(),
    "SOLDIER_135_SHOTGUN": pygame.image.load("sprites/soldier_spr/soldier_135_shotgun.png").convert_alpha(),
    "SOLDIER_180_SHOTGUN": pygame.image.load("sprites/soldier_spr/soldier_180_shotgun.png").convert_alpha(),
    "SOLDIER_225_SHOTGUN": pygame.image.load("sprites/soldier_spr/soldier_225_shotgun.png").convert_alpha(),
    "SOLDIER_270_SHOTGUN": pygame.image.load("sprites/soldier_spr/soldier_270_shotgun.png").convert_alpha(),
    "SOLDIER_315_SHOTGUN": pygame.image.load("sprites/soldier_spr/soldier_315_shotgun.png").convert_alpha(),

    "SOLDIER_0_THOMPSON": pygame.image.load("sprites/soldier_spr/soldier_0_thompson.png").convert_alpha(),
    "SOLDIER_45_THOMPSON": pygame.image.load("sprites/soldier_spr/soldier_45_thompson.png").convert_alpha(),
    "SOLDIER_90_THOMPSON": pygame.image.load("sprites/soldier_spr/soldier_90_thompson.png").convert_alpha(),
    "SOLDIER_135_THOMPSON": pygame.image.load("sprites/soldier_spr/soldier_135_thompson.png").convert_alpha(),
    "SOLDIER_180_THOMPSON": pygame.image.load("sprites/soldier_spr/soldier_180_thompson.png").convert_alpha(),
    "SOLDIER_270_THOMPSON": pygame.image.load("sprites/soldier_spr/soldier_270_thompson.png").convert_alpha(),
    "SOLDIER_225_THOMPSON": pygame.image.load("sprites/soldier_spr/soldier_225_thompson.png").convert_alpha(),
    "SOLDIER_315_THOMPSON": pygame.image.load("sprites/soldier_spr/soldier_315_thompson.png").convert_alpha(),

    "SOLDIER_0_BAR": pygame.image.load("sprites/soldier_spr/soldier_0_bar.png").convert_alpha(),
    "SOLDIER_45_BAR": pygame.image.load("sprites/soldier_spr/soldier_45_bar.png").convert_alpha(),
    "SOLDIER_90_BAR": pygame.image.load("sprites/soldier_spr/soldier_90_bar.png").convert_alpha(),
    "SOLDIER_135_BAR": pygame.image.load("sprites/soldier_spr/soldier_135_bar.png").convert_alpha(),
    "SOLDIER_180_BAR": pygame.image.load("sprites/soldier_spr/soldier_180_bar.png").convert_alpha(),
    "SOLDIER_225_BAR": pygame.image.load("sprites/soldier_spr/soldier_225_bar.png").convert_alpha(),
    "SOLDIER_270_BAR": pygame.image.load("sprites/soldier_spr/soldier_270_bar.png").convert_alpha(),
    "SOLDIER_315_BAR": pygame.image.load("sprites/soldier_spr/soldier_315_bar.png").convert_alpha(),

    "SOLDIER_0_GLAUNCHER": pygame.image.load("sprites/soldier_spr/soldier_0_glauncher.png").convert_alpha(),
    "SOLDIER_45_GLAUNCHER": pygame.image.load("sprites/soldier_spr/soldier_45_glauncher.png").convert_alpha(),
    "SOLDIER_90_GLAUNCHER": pygame.image.load("sprites/soldier_spr/soldier_90_glauncher.png").convert_alpha(),
    "SOLDIER_135_GLAUNCHER": pygame.image.load("sprites/soldier_spr/soldier_135_glauncher.png").convert_alpha(),
    "SOLDIER_180_GLAUNCHER": pygame.image.load("sprites/soldier_spr/soldier_180_glauncher.png").convert_alpha(),
    "SOLDIER_225_GLAUNCHER": pygame.image.load("sprites/soldier_spr/soldier_225_glauncher.png").convert_alpha(),
    "SOLDIER_270_GLAUNCHER": pygame.image.load("sprites/soldier_spr/soldier_270_glauncher.png").convert_alpha(),
    "SOLDIER_315_GLAUNCHER": pygame.image.load("sprites/soldier_spr/soldier_315_glauncher.png").convert_alpha(),

    "SOLDIER_LEGS_LEFT": pygame.image.load("sprites/soldier_spr/soldier_legs_left.png").convert_alpha(),
    "SOLDIER_LEGS_NORMAL": pygame.image.load("sprites/soldier_spr/soldier_legs_normal.png").convert_alpha(),
    "SOLDIER_LEGS_RIGHT": pygame.image.load("sprites/soldier_spr/soldier_legs_right.png").convert_alpha(),

    # muzzle_flash_spr
    "FLASH" : pygame.image.load("sprites/muzzle_flash_spr/flash.png").convert_alpha(),

    # smoke_spr
    "SMOKE1": pygame.image.load("sprites/smoke_spr/smoke1.png").convert_alpha(),
    "SMOKE2": pygame.image.load("sprites/smoke_spr/smoke2.png").convert_alpha(),
    "SMOKE3": pygame.image.load("sprites/smoke_spr/smoke3.png").convert_alpha(),

    # skull_spr
    "SKULL": pygame.image.load("sprites/skull_spr/skull.png").convert_alpha(),

    # table_spr
    "TABLE_LEG": pygame.image.load("sprites/table_spr/table_leg.png").convert_alpha(),
    "TABLE_TOP": pygame.image.load("sprites/table_spr/table_top.png").convert_alpha(),
    "TABLE_TOP_TOPPLED_BORDER": pygame.image.load("sprites/table_spr/table_top_toppled_border.png").convert_alpha(),
    "TABLE_TOP_TOPPLED_INNER": pygame.image.load("sprites/table_spr/table_top_toppled_inner.png").convert_alpha(),
    "TABLE_TOPPLED_LEG": pygame.image.load("sprites/table_spr/table_toppled_leg.png").convert_alpha(),

    # weapons_spr
    "COLT": pygame.image.load("sprites/weapons_spr/colt.png").convert_alpha(),
    "COLT1": pygame.image.load("sprites/weapons_spr/colt1.png").convert_alpha(),
    "COLT2": pygame.image.load("sprites/weapons_spr/colt2.png").convert_alpha(),

    # Sprite_Editor
    "ERASER": pygame.image.load("sprites/Sprite_Editor/Tools/eraser.png").convert_alpha(),
    "LINE": pygame.image.load("sprites/Sprite_Editor/Tools/line.png").convert_alpha(),
    "SELECT": pygame.image.load("sprites/Sprite_Editor/Tools/select.png").convert_alpha(),

    # Level Editor
    "BUCKET": pygame.image.load("sprites/Level Editor/bucket.png").convert_alpha(),
    "ENEMY_TOOL": pygame.image.load("sprites/Level Editor/enemy_tool.png").convert_alpha(),
    "MISCELLANEOUS": pygame.image.load("sprites/Level Editor/miscellaneous.png").convert_alpha(),
    "PENCIL": pygame.image.load("sprites/Level Editor/pencil.png").convert_alpha(),
    "PLAYER_SPAWN": pygame.image.load("sprites/Level Editor/player_spawn.png").convert_alpha(),
    "CUTSCENE_ELEMENTS" : pygame.image.load("sprites/Level Editor/cutscene_elements.png").convert_alpha(),

    # enemy_alerted_spr
    "ALERTED0" : pygame.image.load("sprites/enemy_alerted_spr/alerted0.png").convert_alpha(),
    "ALERTED1": pygame.image.load("sprites/enemy_alerted_spr/alerted1.png").convert_alpha(),

    # trigger_spr
    "TRIGGER" : pygame.image.load("sprites/trigger_spr/trigger.png").convert()
}

# I don't have a work-around for this. This is the best I've got. Holy fuck
pygame.display.quit()
pygame.display.init()

with open("temp.txt", 'r') as f:
    for filename in f:
        fn = filename.strip()
        fn_key = fn.strip().split("/")[2].split(".")[0]
        print(f'\t"{fn_key.upper()}" : pygame.image.load("{fn}").convert_alpha(),')
