import math
import pygame

def resolve_collisions(balls, sound_engine=None):
    active_balls = [b for b in balls if not b.in_pocket and not b.is_pocketing]
    n = len(active_balls)

    for i in range(n):
        for j in range(i + 1, n):
            b1 = active_balls[i]
            b2 = active_balls[j]

            delta = b2.pos - b1.pos
            dist_sq = delta.length_squared()
            min_dist = b1.radius + b2.radius

            if dist_sq < min_dist * min_dist and dist_sq > 0:
                dist = math.sqrt(dist_sq)
                normal = delta / dist

                overlap = min_dist - dist
                b1.pos -= normal * (overlap * 0.5)
                b2.pos += normal * (overlap * 0.5)

                relative_vel = b2.vel - b1.vel
                vel_along_normal = relative_vel.dot(normal)

                if vel_along_normal < 0:
                    restitution = 0.96
                    impulse_j = -(1 + restitution) * vel_along_normal / 2.0
                    impulse = normal * impulse_j

                    b1.vel -= impulse
                    b2.vel += impulse

                    if sound_engine and abs(vel_along_normal) > 0.4:
                        sound_engine.play_hit()
