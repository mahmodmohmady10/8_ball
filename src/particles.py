import random
import math
import pygame

class Particle:
    def __init__(self, x, y, vx, vy, color, radius=5, lifetime=20, is_fire=False):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.radius = radius
        self.initial_radius = radius
        self.lifetime = lifetime
        self.age = 0
        self.is_fire = is_fire

    def update(self):
        self.age += 1
        self.x += self.vx
        self.y += self.vy
        
        if self.is_fire:
            self.vy -= 0.1
            self.vx *= 0.95

    def is_dead(self):
        return self.age >= self.lifetime

    def draw(self, surface):
        if self.is_dead():
            return
        
        life_ratio = 1.0 - (self.age / self.lifetime)
        current_r = max(1, int(self.initial_radius * life_ratio))
        alpha = int(255 * life_ratio)
        
        p_surf = pygame.Surface((current_r * 2, current_r * 2), pygame.SRCALPHA)
        c = (self.color[0], self.color[1], self.color[2], alpha)
        pygame.draw.circle(p_surf, c, (current_r, current_r), current_r)
        surface.blit(p_surf, (int(self.x - current_r), int(self.y - current_r)))


class ParticleSystem:
    def __init__(self):
        self.particles = []

    def spawn_fire_trail(self, cue_pos, cue_vel):
        speed = cue_vel.length()
        if speed < 12.0:
            return
        
        direction = -cue_vel.normalize()
        for _ in range(4):
            offset = direction * random.uniform(5, 12) + pygame.math.Vector2(random.uniform(-4, 4), random.uniform(-4, 4))
            p_pos = cue_pos + offset
            p_vel = direction * random.uniform(1.0, 3.0) + pygame.math.Vector2(random.uniform(-0.8, 0.8), random.uniform(-0.8, 0.8))
            
            colors = [(255, 255, 200), (255, 200, 50), (255, 100, 20), (220, 40, 10)]
            color = random.choice(colors)
            radius = random.randint(4, 7)
            lifetime = random.randint(12, 22)
            
            self.particles.append(Particle(p_pos.x, p_pos.y, p_vel.x, p_vel.y, color, radius, lifetime, is_fire=True))

    def spawn_pocket_flash(self, pocket_pos, is_success=True):
        base_color = (50, 255, 100) if is_success else (255, 50, 60)
        alt_color = (180, 255, 190) if is_success else (255, 160, 160)

        for _ in range(25):
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(2.0, 6.0)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            
            color = base_color if random.random() > 0.3 else alt_color
            radius = random.randint(3, 6)
            lifetime = random.randint(18, 32)
            
            self.particles.append(Particle(pocket_pos[0], pocket_pos[1], vx, vy, color, radius, lifetime))

    def update_and_draw(self, surface):
        alive_particles = []
        for p in self.particles:
            p.update()
            if not p.is_dead():
                p.draw(surface)
                alive_particles.append(p)
        self.particles = alive_particles
