import pygame

class SlowMo:
    slow_motion_on : bool = False
    slow_motion_max_amount : int = 10 * 60
    slow_motion_amount_left : int = slow_motion_max_amount
    slow_motion_ratio : float = 1
    slow_motion_multiplier : float = 0.05

    @classmethod
    def slow_motion(cls):
        SlowMo.slow_motion_amount_left = min(SlowMo.slow_motion_amount_left, SlowMo.slow_motion_max_amount)
        # if pygame.key.get_pressed()[pygame.K_q]:
        #     if SlowMo.slow_motion_amount_left >= 1:
        #         SlowMo.slow_motion_on = True
        # else:
        #     SlowMo.slow_motion_on = False


        if SlowMo.slow_motion_on:
            SlowMo.slow_motion_amount_left = max(SlowMo.slow_motion_amount_left - 0, 0)
            SlowMo.slow_motion_ratio = SlowMo.slow_motion_multiplier
            if SlowMo.slow_motion_amount_left <= 1:
                SlowMo.slow_motion_on = False
        else:
            SlowMo.slow_motion_ratio = 1