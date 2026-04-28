import pygame
import math
pygame.init()
import random

#dimensions and setting up the window
WIDTH, HEIGHT = 800,800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gas Simulation")

Number_of_Particles = 500
Max_speed = 0
Particle_size = 5

class Particle:

    SCALE = 1

    def __init__(self,x,y,radius,colour,mass): #sets initial values
        self.x = x
        self.y = y
        self.radius = radius
        self.colour = colour
        self.mass = mass 

        self.x_vel = 0
        self.y_vel = 0

    def draw(self, win): #set initial position
        x = self.x * self.SCALE + WIDTH/2
        y = self.y * self.SCALE + HEIGHT/2
        pygame.draw.circle(win, self.colour, (x,y), self.radius)

    def collide(self ,other ):
        dx = self.x - other.x
        dy = self.y - other.y
        distance = math.sqrt(dx**2+dy**2)

        if distance <= self.radius + other.radius:

            Normal_x_vel = dx/distance
            Normal_y_vel = dy/distance

            dvx = self.x_vel - other.x_vel
            dvy = self.y_vel - other.y_vel
            
            rel_vel = dvx * Normal_x_vel + dvy * Normal_y_vel

            impulse = (2 * rel_vel) / (self.mass + other.mass)

            if rel_vel > 0:
                return

            self.x_vel -= impulse * other.mass * Normal_x_vel
            self.y_vel -= impulse * other.mass * Normal_y_vel
            other.x_vel += impulse * self.mass * Normal_x_vel
            other.y_vel += impulse * self.mass * Normal_y_vel

    def collide_wall(self):
        if self.x + self.radius >= 400:
            self.x = 400-self.radius
            self.x_vel = self.x_vel*-1

        if self.x - self.radius <= -400:
            self.x = -400+self.radius
            self.x_vel = self.x_vel*-1

        if self.y + self.radius >= 400:
            self.y = 400-self.radius
            self.y_vel = self.y_vel*-1

        if self.y - self.radius <= -400:
            self.y = -400+self.radius
            self.y_vel = self.y_vel*-1
    
    def update(self):
        self.x += self.x_vel
        self.y += self.y_vel

    
Particles = []
#closes the game if tab is closed, and if not keeps the game running. Also keeps refresh rate of 60
def main():
    run = True
    clock = pygame.time.Clock()

    Particle_x = Particle(0,0,Particle_size,(0,225,0), 1.67*10**-24)
    Particle_x.x_vel = 25

    Particles.append(Particle_x)

    for i in range(Number_of_Particles):
        x = random.uniform(-300,300)
        y = random.uniform(-300,300)

        Particle_i = Particle(random.uniform(-400,400),random.uniform(-400,400),Particle_size,(0,255,0), 1.67*10**-24)

        Particle_i.x_vel = random.uniform(-Max_speed,Max_speed)
        Particle_i.y_vel = random.uniform(-Max_speed,Max_speed)

        Particles.append(Particle_i)
        

#    Particle1 = Particle(random.uniform(-400,400),random.uniform(-400,400),10,(0,255,0), 1.67*10**-24)
#    Particle1.x_vel = random.uniform(-1,1)
 #   Particle1.y_vel = random.uniform(-1,1)
 #   Particle1.Particle1 = True

 #   Particle2 = Particle(random.uniform(-400,400),random.uniform(-400,400),10,(255,255,0), 1.67*10**-24)
 #   Particle1.Particle1 = True
 #   Particle2.x_vel = random.uniform(-1,1)
#    Particle1.y_vel = random.uniform(-1,1)

 #  Particles = [Particle1, Particle2]

    while run:
        clock.tick(60)
        WIN.fill((0,0,0)) #fills the background with colour

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for i in range(len(Particles)):
            for j in range(i + 1, len(Particles)):
                Particles[i].collide(Particles[j])

        for particle in Particles:

            particle.collide_wall()
            particle.colour = (75,75,35)
            particle.update()
            particle.draw(WIN)

        pygame.display.update()

    pygame.quit()

main()