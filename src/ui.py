import math
import pygame

COLOR_WHITE = (255, 255, 255)
COLOR_YELLOW = (255, 215, 0)
COLOR_RED = (220, 50, 50)
COLOR_GREEN = (50, 205, 50)
COLOR_CYAN = (80, 220, 255)
COLOR_DARK_BG = (15, 22, 32)
COLOR_CARD_BG = (24, 34, 48)

class Button:
    def __init__(self, x, y, width, height, text, bg_color=(40, 60, 90), hover_color=(60, 90, 140), text_color=COLOR_WHITE, font_size=18):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.font = pygame.font.SysFont("arial", font_size, bold=True)
        self.is_hovered = False

    def update(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.bg_color
        pygame.draw.rect(surface, color, self.rect, border_radius=8)
        pygame.draw.rect(surface, (200, 220, 255), self.rect, 2, border_radius=8)

        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered


def draw_main_menu(surface, buttons):
    surface.fill(COLOR_DARK_BG)

    font_title = pygame.font.SysFont("arial", 38, bold=True)
    font_sub = pygame.font.SysFont("arial", 16)

    title_surf = font_title.render("🎱 2D BILLIARDS CHAMPIONSHIP", True, COLOR_YELLOW)
    sub_surf = font_sub.render("Realistic Physics • AI Bot • Trick Shots • Custom Themes", True, (180, 200, 220))

    surface.blit(title_surf, (surface.get_width() // 2 - title_surf.get_width() // 2, 80))
    surface.blit(sub_surf, (surface.get_width() // 2 - sub_surf.get_width() // 2, 135))

    for btn in buttons:
        btn.draw(surface)


def draw_pause_menu(surface, buttons):
    overlay = pygame.Surface((surface.get_width(), surface.get_height()), pygame.SRCALPHA)
    overlay.fill((10, 15, 22, 200))
    surface.blit(overlay, (0, 0))

    panel_rect = pygame.Rect(surface.get_width() // 2 - 180, 100, 360, 400)
    pygame.draw.rect(surface, COLOR_CARD_BG, panel_rect, border_radius=14)
    pygame.draw.rect(surface, (80, 120, 180), panel_rect, 2, border_radius=14)

    font_title = pygame.font.SysFont("arial", 26, bold=True)
    title_surf = font_title.render("⏸️ GAME PAUSED", True, COLOR_YELLOW)
    surface.blit(title_surf, (surface.get_width() // 2 - title_surf.get_width() // 2, 125))

    for btn in buttons:
        btn.draw(surface)


def draw_victory_modal(surface, winner_text, buttons):
    overlay = pygame.Surface((surface.get_width(), surface.get_height()), pygame.SRCALPHA)
    overlay.fill((10, 15, 22, 210))
    surface.blit(overlay, (0, 0))

    panel_rect = pygame.Rect(surface.get_width() // 2 - 200, 120, 400, 340)
    pygame.draw.rect(surface, COLOR_CARD_BG, panel_rect, border_radius=14)
    pygame.draw.rect(surface, COLOR_YELLOW, panel_rect, 3, border_radius=14)

    font_trophy = pygame.font.SysFont("arial", 40, bold=True)
    font_win = pygame.font.SysFont("arial", 24, bold=True)

    trophy_surf = font_trophy.render("🏆 VICTORY! 🏆", True, COLOR_YELLOW)
    win_surf = font_win.render(winner_text, True, COLOR_WHITE)

    surface.blit(trophy_surf, (surface.get_width() // 2 - trophy_surf.get_width() // 2, 145))
    surface.blit(win_surf, (surface.get_width() // 2 - win_surf.get_width() // 2, 200))

    for btn in buttons:
        btn.draw(surface)


def draw_help_screen(surface, back_button):
    surface.fill(COLOR_DARK_BG)

    panel_rect = pygame.Rect(100, 50, 800, 500)
    pygame.draw.rect(surface, COLOR_CARD_BG, panel_rect, border_radius=14)
    pygame.draw.rect(surface, (80, 120, 180), panel_rect, 2, border_radius=14)

    font_title = pygame.font.SysFont("arial", 28, bold=True)
    font_h = pygame.font.SysFont("arial", 18, bold=True)
    font_b = pygame.font.SysFont("arial", 14)

    title_surf = font_title.render("📖 HOW TO PLAY & FEATURES GUIDE", True, COLOR_YELLOW)
    surface.blit(title_surf, (surface.get_width() // 2 - title_surf.get_width() // 2, 70))

    guides = [
        ("🎮 Game Controls:", "Click & Drag from Cue Ball to aim & adjust shot power, then Release to strike."),
        ("🎯 Trajectory Arrows:", "Dotted white line shows Cue Ball path; Yellow arrow shows target ball deflection."),
        ("🎯 Spin / English Widget:", "Click the bottom-left Cue Ball circle to apply Topspin, Backspin, or Sidespin."),
        ("⚡ Fire Trail Effect:", "Striking with high power spawns fire particle trails behind the Cue Ball."),
        ("🟢🔴 Pocket Flashes:", "Pocketing legal target balls spawns GREEN sparks; Fouls spawn RED sparks."),
        ("🎨 Table Themes (Skins):", "Press 'T' during gameplay to switch between Green, Blue, Red, and Purple felts."),
        ("⏸️ Pause & Controls:", "Press 'ESC' or click [PAUSE] button anytime to pause or restart the match.")
    ]

    y_off = 120
    for header, body in guides:
        h_surf = font_h.render(header, True, COLOR_CYAN)
        b_surf = font_b.render(body, True, COLOR_WHITE)
        surface.blit(h_surf, (130, y_off))
        surface.blit(b_surf, (130, y_off + 22))
        y_off += 50

    back_button.draw(surface)


def draw_power_bar(surface, power, max_power, x=750, y=535, width=200, height=18):
    ratio = min(max(power / max_power, 0.0), 1.0)
    
    if ratio < 0.5:
        bar_color = COLOR_GREEN
    elif ratio < 0.8:
        bar_color = COLOR_YELLOW
    else:
        bar_color = COLOR_RED

    pygame.draw.rect(surface, (30, 35, 40), (x, y, width, height), border_radius=6)
    fill_width = int(width * ratio)
    if fill_width > 0:
        pygame.draw.rect(surface, bar_color, (x, y, fill_width, height), border_radius=6)

    pygame.draw.rect(surface, (200, 200, 200), (x, y, width, height), 2, border_radius=6)

    font = pygame.font.SysFont("arial", 12, bold=True)
    text = font.render(f"POWER: {int(ratio * 100)}%", True, COLOR_WHITE)
    surface.blit(text, (x + width // 2 - text.get_width() // 2, y - 16))


def draw_spin_control_widget(surface, spin_offset, x=50, y=530, radius=22):
    pygame.draw.circle(surface, (230, 230, 230), (x, y), radius)
    pygame.draw.circle(surface, (50, 50, 50), (x, y), radius, 2)
    pygame.draw.line(surface, (180, 180, 180), (x - radius + 3, y), (x + radius - 3, y), 1)
    pygame.draw.line(surface, (180, 180, 180), (x, y - radius + 3), (x, y + radius - 3), 1)

    dot_x = int(x + spin_offset.x * (radius - 4))
    dot_y = int(y + spin_offset.y * (radius - 4))
    pygame.draw.circle(surface, COLOR_RED, (dot_x, dot_y), 4)

    font = pygame.font.SysFont("arial", 12, bold=True)
    text = font.render("SPIN", True, COLOR_WHITE)
    surface.blit(text, (x - text.get_width() // 2, y - radius - 16))


def calculate_and_draw_trajectory(surface, cue_ball, aim_dir, balls, table_rect):
    if aim_dir.length_squared() == 0:
        return

    aim_dir = aim_dir.normalize()
    active_target_balls = [b for b in balls if not b.is_cue and not b.in_pocket and not b.is_pocketing]

    closest_hit_dist = 1000.0
    hit_ball = None

    for ball in active_target_balls:
        to_ball = ball.pos - cue_ball.pos
        projection = to_ball.dot(aim_dir)

        if projection > 0:
            perp_dist_sq = to_ball.length_squared() - (projection * projection)
            min_allow_dist = (cue_ball.radius + ball.radius)

            if perp_dist_sq < min_allow_dist * min_allow_dist:
                d = projection - math.sqrt(max(0, min_allow_dist * min_allow_dist - perp_dist_sq))
                if d < closest_hit_dist and d > 0:
                    closest_hit_dist = d
                    hit_ball = ball

    hit_pos = cue_ball.pos + aim_dir * closest_hit_dist
    hit_pos.x = max(table_rect.left + cue_ball.radius, min(table_rect.right - cue_ball.radius, hit_pos.x))
    hit_pos.y = max(table_rect.top + cue_ball.radius, min(table_rect.bottom - cue_ball.radius, hit_pos.y))

    pygame.draw.line(surface, COLOR_WHITE, cue_ball.pos, hit_pos, 2)
    pygame.draw.circle(surface, (255, 255, 255, 160), (int(hit_pos.x), int(hit_pos.y)), cue_ball.radius, 1)

    if hit_ball and closest_hit_dist < 900:
        target_deflect = (hit_ball.pos - hit_pos).normalize()
        target_end = hit_ball.pos + target_deflect * 55
        pygame.draw.line(surface, COLOR_YELLOW, hit_ball.pos, target_end, 3)
        arrow_p1 = target_end - target_deflect * 8 + target_deflect.rotate(90) * 5
        arrow_p2 = target_end - target_deflect * 8 - target_deflect.rotate(90) * 5
        pygame.draw.polygon(surface, COLOR_YELLOW, [target_end, arrow_p1, arrow_p2])

        cue_deflect = aim_dir - target_deflect * aim_dir.dot(target_deflect)
        if cue_deflect.length_squared() > 0:
            cue_deflect = cue_deflect.normalize()
            cue_end = hit_pos + cue_deflect * 45
            pygame.draw.line(surface, COLOR_CYAN, hit_pos, cue_end, 2)
            arrow_c1 = cue_end - cue_deflect * 7 + cue_deflect.rotate(90) * 4
            arrow_c2 = cue_end - cue_deflect * 7 - cue_deflect.rotate(90) * 4
            pygame.draw.polygon(surface, COLOR_CYAN, [cue_end, arrow_c1, arrow_c2])
