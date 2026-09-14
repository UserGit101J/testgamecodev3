import pygame 
from sys import exit
import random


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("randomkid.png").convert_alpha()
        self.rect = self.image.get_rect(midbottom=(100, 360))
        self.gravity = 0

    def jump(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 360:
            self.gravity = -30

    def fast_fall(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN] and self.rect.bottom < 360:
            self.gravity += 3

    def fall(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 360:
            self.rect.bottom = 360

    def update(self):
        self.jump()
        self.fast_fall()
        self.fall()


class Target(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        self.start = random.randint(800, 1000)
        if type == "medkit":
            self.image = pygame.image.load("medkit.png").convert_alpha()
        elif type == "flashlight":
            self.image = pygame.image.load("flashlight.png").convert_alpha()
        else:
            self.image = pygame.image.load("water.png").convert_alpha()

        self.rect = self.image.get_rect(center=(self.start, 90))

    def update(self):
        self.rect.x -= 6
        return self.destroy()

    def destroy(self):
        if self.rect.right <= 0:
            self.kill()
            return True
        return False


class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.start = random.randint(800, 1000)
        self.image = pygame.image.load("rock.png").convert_alpha()
        self.rect = self.image.get_rect(midbottom=(self.start, 360))

    def update(self):
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.right <= 0:
            self.kill()


pygame.init()

game_state = 'START'
score = 0

font = pygame.font.Font(None, 30)
title_font = pygame.font.Font(None, 60)

screen = pygame.display.set_mode((800, 400)) 

ground = pygame.image.load("Grass.png").convert()
sky = pygame.image.load("sky.png").convert()

pygame.display.set_caption("Weather simulator test")
clock = pygame.time.Clock()

player = pygame.sprite.GroupSingle()
player.add(Player())

target_group = pygame.sprite.Group()
obstacle_group = pygame.sprite.Group()


def reset_game():
    global score
    score = 0
    player.sprite.rect.midbottom = (100, 360)
    player.sprite.gravity = 0
    target_group.empty()
    obstacle_group.empty()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
            if game_state == 'START':
                reset_game()
                game_state = 'PLAYING'
            elif game_state == 'END':
                reset_game()
                game_state = 'PLAYING'

    screen.blit(ground, (0, 350))   
    screen.blit(sky, (0, -250))

    if game_state == 'START':
        title_surf = title_font.render("Weather Simulator", True, (0, 0, 0))
        title_rect = title_surf.get_rect(center=(400, 150))
        
        start_surf = font.render("Click anywhere or press SPACE to Start", True, (50, 50, 50))
        start_rect = start_surf.get_rect(center=(400, 230))

        screen.blit(title_surf, title_rect)
        screen.blit(start_surf, start_rect)

    elif game_state == 'PLAYING':
        player.draw(screen)
        player.update()

        target_group.draw(screen)
        
        for target in target_group.sprites():
            if target.update():
                score -= 1

        if pygame.sprite.spritecollide(player.sprite, target_group, True):
            score += 1

        if not target_group:
            choices = ['medkit', 'flashlight', 'water']
            target_group.add(Target(random.choice(choices)))

        obstacle_group.draw(screen)
        obstacle_group.update()

        if pygame.sprite.spritecollide(player.sprite, obstacle_group, True):
            score -= 1

        if not obstacle_group:
            obstacle_group.add(Obstacle())

        score_surface = font.render(f'Score: {score}', True, (0, 0, 0))
        screen.blit(score_surface, (10, 10))

        if score >= 5:
            game_state = 'END'

    elif game_state == 'END':
        end_surf = title_font.render("You Win!", True, (0, 128, 0))
        end_rect = end_surf.get_rect(center=(400, 140))

        score_surf = font.render(f"Final Score: {score}", True, (0, 0, 0))
        score_rect = score_surf.get_rect(center=(400, 200))

        restart_surf = font.render("Click anywhere or press SPACE to Play Again", True, (50, 50, 50))
        restart_rect = restart_surf.get_rect(center=(400, 260))

        screen.blit(end_surf, end_rect)
        screen.blit(score_surf, score_rect)
        screen.blit(restart_surf, restart_rect)

    pygame.display.update()
    clock.tick(60)