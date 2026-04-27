import pygame
import math
pygame.init()

#dimensions and setting up the window
WIDTH, HEIGHT = 800,800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gas Simulation")

class Particle:
    def __init__(self,x,y,radius,colour,mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.colour = colour
        self.mass = mass 

        self.x_vel = 0
        self.y_vel = 0

#closes the game if tab is closed, and if not keeps the game running. Also keeps refresh rate of 60
def main():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        #WIN.fill((221,231,119)) \\fills the background with colour
        #pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    pygame.quit()

main()