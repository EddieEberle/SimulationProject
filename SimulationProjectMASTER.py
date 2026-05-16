import pygame
import math
pygame.init()
import random

#dimensions and setting up the window
WIDTH, HEIGHT = 800,800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gas Simulation")

Ideal = False

Number_of_Particles = 300
T = 1.0  
Max_speed = math.sqrt(8 * T / (math.pi))
Particle_size = 4
Sigma = 1
Epsilon = 1
dt = 0.025
Box = 15.0  
Cutoff = 2.5

total_momentum = 0
elapsed_time = 0

FONT = pygame.font.SysFont("comicsans", 16)

class Particle:

    SCALE = WIDTH / (2 * Box)

    def __init__(self,x,y,radius,colour,mass): #sets initial values
        self.x = x
        self.y = y
        self.radius = radius
        self.colour = colour
        self.mass = mass 

        self.x_vel = 0
        self.y_vel = 0

    def draw(self, win): #set initial position
        x = int(self.x * self.SCALE + WIDTH/2)
        y = int(self.y * self.SCALE + HEIGHT/2)
        pygame.draw.circle(win, self.colour, (x,y), self.radius,1)

    def collide(self ,other ):
        dx = self.x - other.x
        dy = self.y - other.y
        distance = math.sqrt(dx**2+dy**2)
        radius_lj = self.radius / self.SCALE 

        if distance <= radius_lj * 2:
    

            dvx = self.x_vel - other.x_vel
            dvy = self.y_vel - other.y_vel
            
            rel_vel = dvx * dx + dvy * dy

            if rel_vel > 0:
                return

            self.x_vel -= (2*other.mass/(self.mass+other.mass))*(rel_vel/(distance**2))*dx
            self.y_vel -= (2*other.mass/(self.mass+other.mass))*(rel_vel/(distance**2))*dy
            other.x_vel += (2*self.mass/(self.mass+other.mass))*(rel_vel/(distance**2))*dx
            other.y_vel += (2*self.mass/(self.mass+other.mass))*(rel_vel/(distance**2))*dy

    def collide_wall(self):
        wall = Box - self.radius / self.SCALE
        global total_momentum
        
        if self.x  >= wall:
            self.x = wall
            self.x_vel = self.x_vel*-1
            total_momentum += 2*abs(self.mass*self.x_vel)

        if self.x <= -wall:
            self.x = -wall
            self.x_vel = self.x_vel*-1
            total_momentum += 2*abs(self.mass*self.x_vel)

        if self.y >= wall:
            self.y = wall
            self.y_vel = self.y_vel*-1
            total_momentum += 2*abs(self.mass*self.y_vel)

        if self.y  <= -wall:
            self.y = -wall
            self.y_vel = self.y_vel*-1
            total_momentum += 2*abs(self.mass*self.y_vel)

    def Potential(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        distance1 = math.sqrt(dx**2 + dy**2)

        if distance1 > Cutoff*Sigma or distance1 < 1e-4:
            return

        F = 24*Epsilon*(2*(Sigma**12/distance1**13) - (Sigma**6/distance1**7))
        F = max(min(F, 1000), -1000)

        Fx = F*dx/distance1
        Fy = F*dy/distance1

        self.x_vel += Fx/(self.mass)*dt
        self.y_vel += Fy/(self.mass)*dt

        other.x_vel -= Fx/(other.mass)*dt
        other.y_vel -= Fy/(other.mass)*dt
        
    def update(self):
        self.x += self.x_vel *dt 
        self.y += self.y_vel *dt

        speed = math.sqrt(self.x_vel**2 + self.y_vel**2)
        if speed > 7.5:
            self.x_vel = self.x_vel / speed * 7.5
            self.y_vel = self.y_vel / speed * 7.5


    
    
Particles = []

def main():
    global total_momentum, elapsed_time
    run = True
    clock = pygame.time.Clock()

    for i in range(Number_of_Particles):
        while True:
            x = random.uniform(-Box+1,Box-1)
            y = random.uniform(-Box+1,Box-1)
            if all(math.sqrt((x-p.x)**2 + (y-p.y)**2) > Sigma*1.2 for p in Particles):
                break

        Particle_i = Particle(x,y,Particle_size,(0,255,0), 1)

        std = math.sqrt(T/1)
        Particle_i.x_vel = random.gauss(0, std)
        Particle_i.y_vel = random.gauss(0, std)

        Particles.append(Particle_i)

    while run:
        clock.tick(60)
        elapsed_time += dt
        WIN.fill((0,0,0)) #fills the background with colour

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for i in range(len(Particles)):
            for j in range(i + 1, len(Particles)):
                if Ideal:
                    Particles[i].collide(Particles[j])
                else:
                    Particles[i].Potential(Particles[j])

        for particle in Particles:
            particle.collide_wall()
            particle.colour = (0,150,35)
            particle.update()
            particle.draw(WIN)

        Perimeter = 8*Box
        Pressure = total_momentum/(Perimeter*elapsed_time)

        Pressure_ideal = (Number_of_Particles*T)/((2*Box)**2)

        Pressure_text = FONT.render(f"P_sim={Pressure:.3f}  P_ideal={Pressure_ideal:.3f}", True, (255,255,255))
        WIN.blit(Pressure_text, (10,10))

        pygame.display.update()

    pygame.quit()

main()