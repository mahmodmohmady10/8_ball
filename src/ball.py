import math
import pygame

COLOR_WHITE = (245, 245, 245)
COLOR_BLACK = (20, 20, 20)
COLOR_GOLD = (255, 215, 0)
FRICTION = 0.986
BALL_RADIUS = 12

class Ball:
    def __init__(self, x, y, color, number=0, is_cue=False):
        self.pos = pygame.math.Vector2(x, y)
        self.vel = pygame.math.Vector2(0, 0)
        self.spin = pygame.math.Vector2(0, 0)
        self.color = color
        self.number = number
        self.is_cue = is_cue
        self.radius = BALL_RADIUS
        self.in_pocket = False
        
        self.is_striped = (number >= 9 and number <= 15)
        self.is_target_glow = False
        self.glow_timer = 0.0

        self.is_pocketing = False
        self.anim_progress = 0.0
        self.target_pocket_pos = None

    def start_pocket_animation(self, pocket_pos):
        self.is_pocketing = True
        self.target_pocket_pos = pygame.math.Vector2(pocket_pos)
        self.vel = pygame.math.Vector2(0, 0)

    def update(self, table_rect):
        if self.in_pocket:
            return

        self.glow_timer += 0.08

        if self.is_pocketing:
            self.anim_progress += 0.08
            if self.target_pocket_pos:
                self.pos += (self.target_pocket_pos - self.pos) * 0.25
            
            if self.anim_progress >= 1.0:
                self.is_pocketing = False
                self.in_pocket = True
            return

        if self.spin.length_squared() > 0:
            self.vel += self.spin * 0.12
            self.spin *= 0.92

        self.pos += self.vel
        self.vel *= FRICTION

        if self.vel.length_squared() < 0.005:
            self.vel = pygame.math.Vector2(0, 0)

        if self.pos.x - self.radius < table_rect.left:
            self.pos.x = table_rect.left + self.radius
            self.vel.x *= -0.95
        elif self.pos.x + self.radius > table_rect.right:
            self.pos.x = table_rect.right - self.radius
            self.vel.x *= -0.95

        if self.pos.y - self.radius < table_rect.top:
            self.pos.y = table_rect.top + self.radius
            self.vel.y *= -0.95
        elif self.pos.y + self.radius > table_rect.bottom:
            self.pos.y = table_rect.bottom - self.radius
            self.vel.y *= -0.95

    def draw(self, surface):
        if self.in_pocket:
            return

        current_radius = self.radius
        if self.is_pocketing:
            current_radius = max(1, int(self.radius * (1.0 - self.anim_progress)))

        if self.is_target_glow and not self.is_pocketing and not self.is_cue:
            pulse = (math.sin(self.glow_timer * 4) + 1.0) * 0.5
            glow_radius = current_radius + 3 + int(pulse * 3)
            
            glow_surf = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
            glow_alpha = 140 + int(80 * pulse)
            pygame.draw.circle(glow_surf, (255, 230, 100, glow_alpha), (glow_radius, glow_radius), glow_radius)
            pygame.draw.circle(glow_surf, (255, 255, 255, 220), (glow_radius, glow_radius), glow_radius - 2, 2)
            surface.blit(glow_surf, (int(self.pos.x - glow_radius), int(self.pos.y - glow_radius)))

        pygame.draw.circle(surface, (15, 50, 20), (int(self.pos.x + 2), int(self.pos.y + 2)), current_radius)

        if self.is_cue:
            pygame.draw.circle(surface, COLOR_WHITE, (int(self.pos.x), int(self.pos.y)), current_radius)
            pygame.draw.circle(surface, (200, 200, 200), (int(self.pos.x), int(self.pos.y)), current_radius, 1)

        elif self.is_striped and not self.is_pocketing:
            pygame.draw.circle(surface, COLOR_WHITE, (int(self.pos.x), int(self.pos.y)), current_radius)
            
            stripe_height = int(current_radius * 1.2)
            stripe_surf = pygame.Surface((current_radius * 2, current_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(stripe_surf, self.color, (current_radius, current_radius), current_radius)
            pygame.draw.rect(stripe_surf, (0, 0, 0, 0), (0, 0, current_radius * 2, current_radius - stripe_height // 2))
            pygame.draw.rect(stripe_surf, (0, 0, 0, 0), (0, current_radius + stripe_height // 2, current_radius * 2, current_radius))
            
            surface.blit(stripe_surf, (int(self.pos.x - current_radius), int(self.pos.y - current_radius)))
            pygame.draw.circle(surface, COLOR_WHITE, (int(self.pos.x), int(self.pos.y)), int(current_radius * 0.55))

        else:
            pygame.draw.circle(surface, self.color, (int(self.pos.x), int(self.pos.y)), current_radius)
            if self.number > 0 and not self.is_pocketing:
                pygame.draw.circle(surface, COLOR_WHITE, (int(self.pos.x), int(self.pos.y)), int(current_radius * 0.55))

        if not self.is_cue and self.number > 0 and not self.is_pocketing:
            font = pygame.font.SysFont("arial", 9, bold=True)
            text = font.render(str(self.number), True, COLOR_BLACK)
            text_rect = text.get_rect(center=(int(self.pos.x), int(self.pos.y)))
            surface.blit(text, text_rect)
