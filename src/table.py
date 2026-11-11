import pygame

COLOR_BG = (12, 16, 22)
COLOR_BLACK = (10, 10, 10)
COLOR_WHITE = (245, 245, 245)
COLOR_GOLD = (255, 215, 0)
COLOR_P1 = (50, 150, 255)
COLOR_P2 = (255, 100, 50)

TABLE_THEMES = [
    {"name": "Classic Green", "felt": (28, 120, 55), "border": (18, 80, 35), "cushion": (90, 50, 20)},
    {"name": "Royal Blue", "felt": (20, 70, 150), "border": (12, 45, 100), "cushion": (40, 50, 70)},
    {"name": "Ruby Red", "felt": (150, 25, 40), "border": (95, 15, 25), "cushion": (80, 20, 30)},
    {"name": "Midnight Purple", "felt": (80, 25, 110), "border": (50, 15, 75), "cushion": (55, 20, 65)}
]

POCKET_RADIUS = 22
SCREEN_WIDTH = 1000

class Table:
    def __init__(self, rect):
        self.rect = rect
        self.theme_idx = 0
        self.pockets = [
            (rect.left, rect.top),
            (rect.centerx, rect.top - 4),
            (rect.right, rect.top),
            (rect.left, rect.bottom),
            (rect.centerx, rect.bottom + 4),
            (rect.right, rect.bottom)
        ]

    def next_theme(self):
        self.theme_idx = (self.theme_idx + 1) % len(TABLE_THEMES)

    def draw(self, surface, current_player=1, scores=None, foul_msg="", player_groups=None, mode_str="1 VS 1 PvP"):
        if scores is None:
            scores = {1: 0, 2: 0}
        if player_groups is None:
            player_groups = {1: "Open", 2: "Open"}

        theme = TABLE_THEMES[self.theme_idx]

        surface.fill(COLOR_BG)

        pygame.draw.rect(surface, (40, 20, 10), self.rect.inflate(40, 40), border_radius=18)
        pygame.draw.rect(surface, theme["cushion"], self.rect.inflate(26, 26), border_radius=14)
        
        pygame.draw.rect(surface, theme["border"], self.rect.inflate(6, 6))
        pygame.draw.rect(surface, theme["felt"], self.rect)

        for p in self.pockets:
            pygame.draw.circle(surface, COLOR_BLACK, p, POCKET_RADIUS)

        font_name = pygame.font.SysFont("arial", 15, bold=True)
        font_big = pygame.font.SysFont("arial", 19, bold=True)

        # Player 1 Card
        p1_color = COLOR_GOLD if current_player == 1 else (150, 150, 150)
        pygame.draw.rect(surface, (22, 32, 42), (100, 12, 195, 60), border_radius=8)
        if current_player == 1:
            pygame.draw.rect(surface, COLOR_P1, (100, 12, 195, 60), 2, border_radius=8)
        
        p1_grp = f" ({player_groups[1]})" if player_groups[1] != "Open" else ""
        text_p1 = font_name.render(f"PLAYER 1{p1_grp} {'◄' if current_player == 1 else ''}", True, p1_color)
        text_p1_score = font_big.render(f"SCORE: {scores[1]}", True, COLOR_WHITE)
        surface.blit(text_p1, (110, 16))
        surface.blit(text_p1_score, (110, 40))

        # Player 2 / AI Card
        p2_label = "AI BOT" if "AI" in mode_str else "PLAYER 2"
        p2_color = COLOR_GOLD if current_player == 2 else (150, 150, 150)
        pygame.draw.rect(surface, (22, 32, 42), (705, 12, 195, 60), border_radius=8)
        if current_player == 2:
            pygame.draw.rect(surface, COLOR_P2, (705, 12, 195, 60), 2, border_radius=8)
            
        p2_grp = f" ({player_groups[2]})" if player_groups[2] != "Open" else ""
        text_p2 = font_name.render(f"{p2_label}{p2_grp} {'◄' if current_player == 2 else ''}", True, p2_color)
        text_p2_score = font_big.render(f"SCORE: {scores[2]}", True, COLOR_WHITE)
        surface.blit(text_p2, (715, 16))
        surface.blit(text_p2_score, (715, 40))

        # Mode and Theme HUD
        font_mode = pygame.font.SysFont("arial", 13, bold=True)
        mode_text = font_mode.render(f"MODE: {mode_str}  |  THEME: {theme['name']} (Press T)", True, (200, 220, 240))
        surface.blit(mode_text, (SCREEN_WIDTH // 2 - mode_text.get_width() // 2, 18))

        if foul_msg:
            foul_font = pygame.font.SysFont("arial", 14, bold=True)
            foul_text = foul_font.render(foul_msg, True, (255, 90, 90) if "FOUL" in foul_msg else (100, 240, 120))
            surface.blit(foul_text, (SCREEN_WIDTH // 2 - foul_text.get_width() // 2, 42))
