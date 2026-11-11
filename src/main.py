import sys
import math
import pygame

from ball import Ball, BALL_RADIUS
from physics import resolve_collisions
from table import Table, POCKET_RADIUS, TABLE_THEMES
from ui import (
    Button, draw_main_menu, draw_pause_menu, draw_victory_modal, draw_help_screen,
    draw_power_bar, calculate_and_draw_trajectory, draw_spin_control_widget
)
from sound import SoundEngine
from particles import ParticleSystem
from ai_bot import calculate_ai_shot
from save_system import save_game_state, load_game_state

pygame.init()
pygame.font.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2D Billiards Championship V5 - Full English UI & Game Modes")

CLOCK = pygame.time.Clock()
FPS = 60

COLOR_WHITE = (245, 245, 245)
MAX_POWER = 24.0

BALL_COLORS = [
    (240, 200, 0), (0, 80, 200), (220, 30, 30), (120, 40, 160), (240, 120, 0),
    (20, 120, 40), (140, 20, 20), (20, 20, 20), (240, 200, 0), (0, 80, 200),
    (220, 30, 30), (120, 40, 160), (240, 120, 0), (20, 120, 40), (140, 20, 20)
]

TABLE_RECT = pygame.Rect(100, 100, 800, 400)

# ------------------------------------------------------------------------------
# حالات اللعبة (Game States)
# ------------------------------------------------------------------------------
STATE_MAIN_MENU = "MAIN_MENU"
STATE_PLAYING = "PLAYING"
STATE_PAUSED = "PAUSED"
STATE_GAME_OVER = "GAME_OVER"
STATE_HELP = "HELP"

def create_rack(start_x, start_y):
    balls = []
    cue_ball = Ball(250, 300, COLOR_WHITE, is_cue=True)
    balls.append(cue_ball)

    dx = BALL_RADIUS * math.sqrt(3) + 0.5
    dy = BALL_RADIUS + 0.5
    ball_idx = 0

    for row in range(5):
        for col in range(row + 1):
            x = start_x + row * dx
            y = start_y + (col * 2 - row) * dy
            color = BALL_COLORS[ball_idx % len(BALL_COLORS)]
            ball = Ball(x, y, color, number=ball_idx + 1)
            balls.append(ball)
            ball_idx += 1

    return balls, cue_ball

def create_trick_shot_puzzle():
    balls = []
    cue_ball = Ball(200, 300, COLOR_WHITE, is_cue=True)
    balls.append(cue_ball)

    target1 = Ball(600, 200, BALL_COLORS[0], number=1)
    target2 = Ball(600, 400, BALL_COLORS[1], number=2)
    obstacle = Ball(400, 300, BALL_COLORS[7], number=8)

    balls.extend([target1, target2, obstacle])
    return balls, cue_ball


def main():
    table = Table(TABLE_RECT)
    sound_engine = SoundEngine()
    particle_system = ParticleSystem()

    current_state = STATE_MAIN_MENU
    mode_str = "1 VS 1 PvP"
    winner_text = ""

    current_player = 1
    scores = {1: 0, 2: 0}
    player_groups = {1: "Open", 2: "Open"}

    balls, cue_ball = create_rack(700, 300)
    spin_offset = pygame.math.Vector2(0, 0)
    
    aiming = False
    drag_start = pygame.math.Vector2(0, 0)
    turn_in_progress = False
    pocketed_this_turn = []
    cue_ball_scratched = False
    foul_message = ""
    ai_timer = 0

    # --------------------------------------------------------------------------
    # أزرار القائمة الرئيسية (Main Menu Buttons)
    # --------------------------------------------------------------------------
    cx = SCREEN_WIDTH // 2 - 140
    btn_pvp = Button(cx, 190, 280, 45, "🎮 1 VS 1 Local PvP")
    btn_ai = Button(cx, 250, 280, 45, "🤖 Player VS AI Bot")
    btn_puzzle = Button(cx, 310, 280, 45, "🧩 Trick Shots & Puzzles")
    btn_help = Button(cx, 370, 280, 45, "📖 How to Play & Features")
    btn_exit = Button(cx, 430, 280, 45, "❌ Quit Game", bg_color=(80, 30, 30), hover_color=(120, 40, 40))

    main_menu_buttons = [btn_pvp, btn_ai, btn_puzzle, btn_help, btn_exit]

    # أزرار قائمة التوقف (Pause Menu Buttons)
    btn_pause = Button(880, 25, 90, 32, "PAUSE ⏸️", font_size=12)
    btn_resume = Button(SCREEN_WIDTH // 2 - 120, 180, 240, 42, "▶️ Resume Game")
    btn_restart = Button(SCREEN_WIDTH // 2 - 120, 240, 240, 42, "🔄 Restart Match")
    btn_theme = Button(SCREEN_WIDTH // 2 - 120, 300, 240, 42, "🎨 Change Table Felt")
    btn_menu_p = Button(SCREEN_WIDTH // 2 - 120, 360, 240, 42, "🏠 Main Menu")
    btn_quit_p = Button(SCREEN_WIDTH // 2 - 120, 420, 240, 42, "❌ Quit", bg_color=(80, 30, 30), hover_color=(120, 40, 40))

    pause_buttons = [btn_resume, btn_restart, btn_theme, btn_menu_p, btn_quit_p]

    # أزرار شاشة نهاية اللعبة (Victory Buttons)
    btn_replay_v = Button(SCREEN_WIDTH // 2 - 120, 250, 240, 42, "🔄 Play Again")
    btn_menu_v = Button(SCREEN_WIDTH // 2 - 120, 310, 240, 42, "🏠 Main Menu")
    btn_quit_v = Button(SCREEN_WIDTH // 2 - 120, 370, 240, 42, "❌ Quit Game", bg_color=(80, 30, 30), hover_color=(120, 40, 40))

    victory_buttons = [btn_replay_v, btn_menu_v, btn_quit_v]

    # زر العودة للشاشة الرئيسية من شاشة التوجيهات
    btn_back_help = Button(SCREEN_WIDTH // 2 - 100, 490, 200, 42, "⬅️ Back to Menu")

    font_ui = pygame.font.SysFont("arial", 15, bold=True)

    def reset_match(mode):
        nonlocal current_player, scores, player_groups, balls, cue_ball, turn_in_progress, foul_message, winner_text
        current_player = 1
        scores = {1: 0, 2: 0}
        player_groups = {1: "Open", 2: "Open"}
        turn_in_progress = False
        foul_message = ""
        winner_text = ""

        if mode == "Trick Shots":
            balls, cue_ball = create_trick_shot_puzzle()
        else:
            balls, cue_ball = create_rack(700, 300)

    running = True
    while running:
        CLOCK.tick(FPS)
        mouse_pos = pygame.math.Vector2(pygame.mouse.get_pos())

        # ----------------------------------------------------------------------
        # 1. حالة القائمة الرئيسية (MAIN MENU STATE)
        # ----------------------------------------------------------------------
        if current_state == STATE_MAIN_MENU:
            for btn in main_menu_buttons:
                btn.update(mouse_pos)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if btn_pvp.is_clicked(event):
                    mode_str = "1 VS 1 Local PvP"
                    reset_match("PvP")
                    current_state = STATE_PLAYING

                elif btn_ai.is_clicked(event):
                    mode_str = "Player VS AI Bot"
                    reset_match("PvP")
                    current_state = STATE_PLAYING

                elif btn_puzzle.is_clicked(event):
                    mode_str = "Trick Shots"
                    reset_match("Trick Shots")
                    current_state = STATE_PLAYING

                elif btn_help.is_clicked(event):
                    current_state = STATE_HELP

                elif btn_exit.is_clicked(event):
                    running = False

            draw_main_menu(screen, main_menu_buttons)

        # ----------------------------------------------------------------------
        # 2. حالة دليل الميزات والشرح (HELP GUIDE STATE)
        # ----------------------------------------------------------------------
        elif current_state == STATE_HELP:
            btn_back_help.update(mouse_pos)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif btn_back_help.is_clicked(event) or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    current_state = STATE_MAIN_MENU

            draw_help_screen(screen, btn_back_help)

        # ----------------------------------------------------------------------
        # 3. حالة اللعب النشط وقائمة التوقف ونهاية المباراة
        # ----------------------------------------------------------------------
        else:
            all_stopped = all(b.vel.length_squared() == 0 and not b.is_pocketing for b in balls if not b.in_pocket)

            # معالجة منطق تبادل الأدوار والتحقق من الفوز
            if current_state == STATE_PLAYING and turn_in_progress and all_stopped:
                turn_in_progress = False

                if player_groups[1] == "Open" and len(pocketed_this_turn) > 0:
                    first_ball = pocketed_this_turn[0]
                    if not first_ball.is_cue and first_ball.number != 8:
                        if first_ball.is_striped:
                            player_groups[current_player] = "Stripes"
                            player_groups[3 - current_player] = "Solids"
                        else:
                            player_groups[current_player] = "Solids"
                            player_groups[3 - current_player] = "Stripes"

                if cue_ball_scratched:
                    foul_message = f"FOUL! Cue ball pocketed - Turn switched to Player {3 - current_player}"
                    current_player = 3 - current_player
                elif len(pocketed_this_turn) > 0:
                    foul_message = f"GREAT SHOT! Player {current_player} retains turn"
                else:
                    foul_message = ""
                    current_player = 3 - current_player

                # فحص شروط نهاية المباراة والفوز (Victory Condition)
                remaining_object_balls = [b for b in balls if not b.is_cue and not b.in_pocket]
                if len(remaining_object_balls) == 0:
                    if mode_str == "Trick Shots":
                        winner_text = "PUZZLE CLEARED PERFECTLY!"
                    else:
                        winner_text = f"PLAYER {1 if scores[1] > scores[2] else 2} WINS THE MATCH!"
                    current_state = STATE_GAME_OVER

                pocketed_this_turn = []
                cue_ball_scratched = False

            # رمية الذكاء الاصطناعي (AI Bot Turn)
            if current_state == STATE_PLAYING and mode_str == "Player VS AI Bot" and current_player == 2 and all_stopped and not turn_in_progress:
                ai_timer += 1
                if ai_timer > 30:
                    ai_timer = 0
                    ai_dir, ai_power = calculate_ai_shot(cue_ball, balls, table.pockets, TABLE_RECT, player_groups[2])
                    cue_ball.vel = ai_dir * ai_power
                    turn_in_progress = True
                    sound_engine.play_cue()

            # التوهج للكرات المستهدفة
            active_group = player_groups[current_player]
            for b in balls:
                b.is_target_glow = False
                if not b.is_cue and not b.in_pocket and not b.is_pocketing:
                    if active_group == "Open":
                        b.is_target_glow = True
                    elif active_group == "Solids" and not b.is_striped and b.number != 8:
                        b.is_target_glow = True
                    elif active_group == "Stripes" and b.is_striped:
                        b.is_target_glow = True

            btn_pause.update(mouse_pos)

            # ------------------------------------------------------------------
            # الأحداث في الأنماط الحية (PLAYING / PAUSED / GAME OVER)
            # ------------------------------------------------------------------
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    save_game_state(balls, current_player, scores, player_groups, table.theme_idx)
                    running = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if current_state == STATE_PLAYING:
                            current_state = STATE_PAUSED
                        elif current_state == STATE_PAUSED:
                            current_state = STATE_PLAYING
                    elif event.key == pygame.K_t:
                        table.next_theme()

                # أحداث أثناء اللعب النشط
                if current_state == STATE_PLAYING:
                    if btn_pause.is_clicked(event):
                        current_state = STATE_PAUSED

                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        spin_widget_vec = pygame.math.Vector2(50, 530)
                        if mouse_pos.distance_to(spin_widget_vec) <= 22:
                            diff = (mouse_pos - spin_widget_vec) / 22.0
                            spin_offset = diff if diff.length() <= 1.0 else diff.normalize()
                        elif all_stopped and not cue_ball.in_pocket and not cue_ball.is_pocketing:
                            if not (mode_str == "Player VS AI Bot" and current_player == 2):
                                aiming = True
                                drag_start = mouse_pos
                                foul_message = ""

                    elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                        if aiming:
                            aiming = False
                            pull_vector = drag_start - mouse_pos
                            power = min(pull_vector.length() * 0.18, MAX_POWER)
                            if power > 0.5:
                                direction = pull_vector.normalize() if pull_vector.length() > 0 else pygame.math.Vector2(1, 0)
                                cue_ball.vel = direction * power
                                cue_ball.spin = spin_offset * (power * 0.4)
                                turn_in_progress = True
                                sound_engine.play_cue()

                # أحداث قائمة التوقف (PAUSED)
                elif current_state == STATE_PAUSED:
                    for btn in pause_buttons:
                        btn.update(mouse_pos)

                    if btn_resume.is_clicked(event):
                        current_state = STATE_PLAYING
                    elif btn_restart.is_clicked(event):
                        reset_match(mode_str)
                        current_state = STATE_PLAYING
                    elif btn_theme.is_clicked(event):
                        table.next_theme()
                    elif btn_menu_p.is_clicked(event):
                        save_game_state(balls, current_player, scores, player_groups, table.theme_idx)
                        current_state = STATE_MAIN_MENU
                    elif btn_quit_p.is_clicked(event):
                        running = False

                # أحداث شاشة نهاية اللعبة (GAME OVER)
                elif current_state == STATE_GAME_OVER:
                    for btn in victory_buttons:
                        btn.update(mouse_pos)

                    if btn_replay_v.is_clicked(event):
                        reset_match(mode_str)
                        current_state = STATE_PLAYING
                    elif btn_menu_v.is_clicked(event):
                        current_state = STATE_MAIN_MENU
                    elif btn_quit_v.is_clicked(event):
                        running = False

            # تحديث الفيزياء والجسيمات
            if current_state == STATE_PLAYING:
                for ball in balls:
                    ball.update(TABLE_RECT)

                if cue_ball.vel.length() > 12.0:
                    particle_system.spawn_fire_trail(cue_ball.pos, cue_ball.vel)

                for _ in range(3):
                    resolve_collisions(balls, sound_engine)

                for ball in balls:
                    if not ball.in_pocket and not ball.is_pocketing:
                        for pocket in table.pockets:
                            pocket_vec = pygame.math.Vector2(pocket)
                            if ball.pos.distance_to(pocket_vec) < POCKET_RADIUS:
                                ball.start_pocket_animation(pocket)
                                sound_engine.play_pocket()

                                if ball.is_cue:
                                    cue_ball_scratched = True
                                    particle_system.spawn_pocket_flash(pocket, is_success=False)
                                else:
                                    pocketed_this_turn.append(ball)
                                    scores[current_player] += 10
                                    particle_system.spawn_pocket_flash(pocket, is_success=True)

                if cue_ball.in_pocket:
                    cue_ball.in_pocket = False
                    cue_ball.is_pocketing = False
                    cue_ball.pos = pygame.math.Vector2(250, 300)
                    cue_ball.vel = pygame.math.Vector2(0, 0)

            # ------------------------------------------------------------------
            # رسم الطاولة والواجهة الرئيسية
            # ------------------------------------------------------------------
            table.draw(screen, current_player=current_player, scores=scores, foul_msg=foul_message, player_groups=player_groups, mode_str=mode_str)
            particle_system.update_and_draw(screen)

            for ball in balls:
                ball.draw(screen)

            current_power = 0.0
            if aiming and all_stopped and not cue_ball.in_pocket:
                pull_vector = drag_start - mouse_pos
                current_power = min(pull_vector.length() * 0.18, MAX_POWER)

                if pull_vector.length() > 0:
                    aim_dir = pull_vector.normalize()
                    calculate_and_draw_trajectory(screen, cue_ball, aim_dir, balls, TABLE_RECT)

                    stick_start = cue_ball.pos - aim_dir * (20 + current_power * 2)
                    stick_end = stick_start - aim_dir * 180
                    pygame.draw.line(screen, (139, 69, 19), stick_start, stick_end, 6)

            draw_power_bar(screen, current_power, MAX_POWER, x=760, y=540, width=200, height=18)
            draw_spin_control_widget(screen, spin_offset, x=50, y=530, radius=22)
            btn_pause.draw(screen)

            help_surface = font_ui.render(f"PLAYER {current_player} TURN | Drag from Cue Ball to aim & shoot | ESC to Pause", True, (190, 210, 230))
            screen.blit(help_surface, (120, SCREEN_HEIGHT - 35))

            # ------------------------------------------------------------------
            # رسم الطبقات الشفافة للقوائم (PAUSED / GAME OVER)
            # ------------------------------------------------------------------
            if current_state == STATE_PAUSED:
                draw_pause_menu(screen, pause_buttons)
            elif current_state == STATE_GAME_OVER:
                draw_victory_modal(screen, winner_text, victory_buttons)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
