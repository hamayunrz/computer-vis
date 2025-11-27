from aimbot import Aimbot
from settings import *
from target import Target
import pygame, random

class Countdown():
    def __init__(self, aimbot_status, seconds):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(COUNTDOWN_FONT, 80)

        self.decrement_time = pygame.time.get_ticks()
        self.should_decrement = False

        self.aimbot_status = aimbot_status
        self.time_left = int(seconds)
        self.initial_countdown_length = self.time_left

        self.target_group = pygame.sprite.Group()
        self.targets_spawned = 0

        if self.aimbot_status:
            self.aimbot = Aimbot()

    def cooldowns(self):
        curr_time = pygame.time.get_ticks()

        # tick once a second
        if not self.should_decrement and self.time_left > 0:
            if curr_time - self.decrement_time > 999:
                self.should_decrement = True

    def draw_timer(self):
        if self.should_decrement:
            self.time_left -= 1
            self.decrement_time = pygame.time.get_ticks()
            self.should_decrement = False

        if self.time_left > 0:
            count_string = str(self.time_left)
        else:
            count_string = ""

        # draw timer bottom right
        count_surf = self.font.render(count_string, True, TEXT_COLOR, None)
        x, y = WIDTH - 20, HEIGHT - 10
        count_rect = count_surf.get_rect(bottomright=(x, y))
        self.display_surface.blit(count_surf, count_rect)

    # target is a 60x60 red square
    def spawn_target(self):
        # only spawn while timer is running, keep 1 target on screen
        if self.time_left > 0 and len(self.target_group) < 1:
            x, y = random.randint(0, 1860), random.randint(0, 1020)
            spawned_target = Target(x, y)
            self.target_group.add(spawned_target)
            self.targets_spawned += 1

        self.target_group.draw(self.display_surface)

    # per-frame update
    def update(self):
        self.cooldowns()
        self.draw_timer()
        self.spawn_target()
        if self.aimbot_status:
            self.aimbot.update()
