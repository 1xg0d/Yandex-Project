import pygame
import sys
import random
from config import *


class Game:
    def __init__(self):
        pygame.init()

        self.gravity = GRAVITY
        self.game_active = False
        self.bird_movement = 0
        self.score = 0
        f = open('hs.txt')
        self.high_score = int(f.readline())
        f.close()
        self.screen = pygame.display.set_mode((576, 1024))
        self.clock = pygame.time.Clock()
        self.can_score = True

        self.bg_surface = pygame.image.load(background).convert()
        self.bg_surface = pygame.transform.scale2x(self.bg_surface)

        self.floor_surface = pygame.image.load(base).convert()
        self.floor_surface = pygame.transform.scale2x(self.floor_surface)
        self.floor_x_pos = 0

        self.bird_downflap = pygame.transform.scale2x(pygame.image.load(downflap).convert_alpha())
        self.bird_midflap = pygame.transform.scale2x(pygame.image.load(midflap).convert_alpha())
        self.bird_upflap = pygame.transform.scale2x(pygame.image.load(upflap).convert_alpha())
        self.bird_frames = [self.bird_downflap, self.bird_midflap, self.bird_upflap]
        self.bird_index = 0
        self.bird_surface = self.bird_frames[self.bird_index]
        self.bird_rect = self.bird_surface.get_rect(center=(100, 512))
        self.pipe_surface = pygame.image.load(pipe_red)
        self.pipe_surface = pygame.transform.scale2x(self.pipe_surface)
        self.pipe_list = []
        self.pipe_height = [400, 600, 800]

        self.game_over_surface = pygame.transform.scale2x(
            pygame.image.load(message).convert_alpha())
        self.game_over_rect = self.game_over_surface.get_rect(center=(288, 512))

        self.flap_sound = pygame.mixer.Sound(wing)
        self.death_sound = pygame.mixer.Sound(hit)
        self.score_sound = pygame.mixer.Sound(point)
        self.score_sound_countdown = 100
        self.main_song = pygame.mixer.Sound(main)
        self.game_font = pygame.font.Font(font, 40)

        self.BIRDFLAP = pygame.USEREVENT + 1
        pygame.time.set_timer(self.BIRDFLAP, 200)


        self.SPAWNPIPE = pygame.USEREVENT
        pygame.time.set_timer(self.SPAWNPIPE, 1200)

        self.SCOREEVENT = pygame.USEREVENT + 2

        pygame.time.set_timer(self.SCOREEVENT, 100)

    def draw_floor(self):
        self.screen.blit(self.floor_surface, (self.floor_x_pos, 900))
        self.screen.blit(self.floor_surface, (self.floor_x_pos + 576, 900))


    def create_pipe(self):
        self.random_pipe_pos = random.choice(self.pipe_height)
        self.bottom_pipe = self.pipe_surface.get_rect(midtop=(700, self.random_pipe_pos))
        self.top_pipe = self.pipe_surface.get_rect(midbottom=(700, self.random_pipe_pos - 300))
        return self.bottom_pipe, self.top_pipe


    def move_pipes(self,pipes):
        visible_pipes = []
        for pipe in pipes:
            pipe.centerx -= 5
            visible_pipes = [pipe for pipe in pipes if pipe.right > -50]
        return visible_pipes


    def draw_pipes(self,pipes):
        for pipe in pipes:
            if pipe.bottom >= 1024:
                self.screen.blit(self.pipe_surface, pipe)
            else:
                flip_pipe = pygame.transform.flip(self.pipe_surface, False, True)
                self.screen.blit(flip_pipe, pipe)


    def check_collision(self,pipes):
        for pipe in pipes:
            if self.bird_rect.colliderect(pipe):
                self.death_sound.play()
                self.can_score = True
                return False

        if self.bird_rect.top <= -100 or self.bird_rect.bottom >= 900:
            self.can_score = True
            return False

        return True


    def rotate_bird(self,bird):
        new_bird = pygame.transform.rotozoom(bird, -self.bird_movement * 3, 1)
        return new_bird


    def bird_animation(self):
        new_bird = self.bird_frames[self.bird_index]
        new_bird_rect = new_bird.get_rect(center=(100, self.bird_rect.centery))
        return new_bird, new_bird_rect


    def score_display(self, game_state):
        if game_state == 'main_game':
            score_surface = self.game_font.render(
                str(int(self.score)), True, (255, 255, 255))
            score_rect = score_surface.get_rect(center=(288, 100))
            self.screen.blit(score_surface, score_rect)
        if game_state == 'game_over':
            score_surface = self.game_font.render(
                f'Score: {int(self.score)}', True, (255, 255, 255))
            score_rect = score_surface.get_rect(center=(288, 100))
            self.screen.blit(score_surface, score_rect)

            high_score_surface = self.game_font.render(
                f'High score: {int(self.high_score)}', True, (255, 255, 255))
            high_score_rect = high_score_surface.get_rect(center=(288, 850))
            self.screen.blit(high_score_surface, high_score_rect)


    def update_score(self, score, high_score):
        if score > high_score:
            high_score = score
        return high_score


    def pipe_score_check(self):
        if self.pipe_list:
            for pipe in self.pipe_list:
                if 95 < pipe.centerx < 105 and self.can_score:
                    self.score += 1
                    self.score_sound.play()
                    self.can_score = False
                if pipe.centerx < 0:
                    self.can_score = True

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                f = open('hs.txt', 'w')
                f.write(str(self.high_score))
                f.close()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.game_active:
                    self.bird_movement = 0
                    self.bird_movement -= 12
                    self.flap_sound.play()
                if event.key == pygame.K_SPACE and self.game_active == False:
                    self.game_active = True
                    self.pipe_list.clear()
                    self.bird_rect.center = (100, 512)
                    self.bird_movement = 0
                    self.score = 0

            if event.type == self.SPAWNPIPE:
                self.pipe_list.extend(self.create_pipe())

            if event.type == self.BIRDFLAP:
                if self.bird_index < 2:
                    self.bird_index += 1
                else:
                    self.bird_index = 0

                self.bird_surface, self.bird_rect = self.bird_animation()

        self.screen.blit(self.bg_surface, (0, 0))

        if self.game_active:
            # Bird
            self.bird_movement += self.gravity
            rotated_bird = self.rotate_bird(self.bird_surface)
            self.bird_rect.centery += self.bird_movement
            self.screen.blit(rotated_bird, self.bird_rect)
            self.game_active = self.check_collision(self.pipe_list)

            # Pipes
            self.pipe_list = self.move_pipes(self.pipe_list)
            self.draw_pipes(self.pipe_list)

            # Score
            self.pipe_score_check()
            self.score_display('main_game')
        else:
            self.screen.blit(self.game_over_surface, self.game_over_rect)
            self.high_score = self.update_score(self.score, self.high_score)
            self.score_display('game_over')

        # Floor
        self.floor_x_pos -= 1
        self.draw_floor()
        if self.floor_x_pos <= -576:
            self.floor_x_pos = 0

        pygame.display.update()
        self.clock.tick(120)


    def run(self):
        while True:
            self.main_song.play()	
            self.events()


game = Game()
game.run()
