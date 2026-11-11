import math
import random
import pygame

def calculate_ai_shot(cue_ball, balls, table_pockets, table_rect, active_group="Unassigned"):
    active_target_balls = [
        b for b in balls 
        if not b.is_cue and not b.in_pocket and not b.is_pocketing
    ]

    valid_targets = []
    for b in active_target_balls:
        if active_group == "Unassigned":
            valid_targets.append(b)
        elif active_group == "Solids" and not b.is_striped and b.number != 8:
            valid_targets.append(b)
        elif active_group == "Stripes" and b.is_striped:
            valid_targets.append(b)
        elif b.number == 8:
            group_rem = [
                ball for ball in balls if not ball.in_pocket and 
                ((active_group == "Solids" and not ball.is_striped and ball.number != 8) or 
                 (active_group == "Stripes" and ball.is_striped))
            ]
            if len(group_rem) == 0:
                valid_targets.append(b)

    if not valid_targets:
        valid_targets = active_target_balls

    if not valid_targets:
        angle = random.uniform(0, math.pi * 2)
        power = random.uniform(10.0, 18.0)
        return pygame.math.Vector2(math.cos(angle), math.sin(angle)), power

    best_target = None
    best_pocket = None
    best_score = 99999.0

    for target in valid_targets:
        for pocket in table_pockets:
            pocket_vec = pygame.math.Vector2(pocket)
            target_to_pocket = pocket_vec - target.pos
            cue_to_target = target.pos - cue_ball.pos

            dist_to_pocket = target_to_pocket.length()
            dist_cue_to_target = cue_to_target.length()

            alignment = cue_to_target.normalize().dot(target_to_pocket.normalize()) if dist_to_pocket > 0 and dist_cue_to_target > 0 else -1

            if alignment > 0.1:
                score = dist_cue_to_target + dist_to_pocket * 0.8 - (alignment * 200)
                if score < best_score:
                    best_score = score
                    best_target = target
                    best_pocket = pocket_vec

    if best_target and best_pocket:
        target_to_pocket_dir = (best_pocket - best_target.pos).normalize()
        ghost_hit_pos = best_target.pos - target_to_pocket_dir * (cue_ball.radius + best_target.radius)
        
        shot_dir = (ghost_hit_pos - cue_ball.pos).normalize()
        shot_power = min(18.0, max(8.0, (ghost_hit_pos - cue_ball.pos).length() * 0.05 + 10.0))
        return shot_dir, shot_power

    closest_target = min(valid_targets, key=lambda b: (b.pos - cue_ball.pos).length_squared())
    shot_dir = (closest_target.pos - cue_ball.pos).normalize()
    return shot_dir, 14.0
