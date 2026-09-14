import pygame 
import sys  
pygame.init()

screen = pygame.display.set_mode((800, 600)) 

surface = pygame.Surface((200, 100))
surface.fill("red")
x=0
#game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.fill("black")
    screen.blit(surface, (x,250)) #Blit means to draw the surface onto the screen
    if x > 800:
        x=0
    x+=.1
    pygame.display.flip() 








    