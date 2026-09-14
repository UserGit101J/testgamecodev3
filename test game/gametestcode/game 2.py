import pygame 
from sys import exit


pygame.init()


screen = pygame.display.set_mode((800, 400)) 
surface = pygame.Surface((800, 400))

ground = pygame.image.load("Grass.png").convert()
sky = pygame.image.load("sky.png").convert()

pygame.display.set_caption("Weather simulator test")
clock = pygame.time.Clock()




while True:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    
    screen.blit(ground, (0, 350))   
    screen.blit(sky,  (0, -250))

    pygame.display.update()
    clock.tick(60)
