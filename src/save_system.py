import json
import os

SAVE_FILE_PATH = "savegame.json"

def save_game_state(balls, current_player, scores, player_groups, table_theme_idx):
    try:
        balls_data = []
        for b in balls:
            balls_data.append({
                "number": b.number,
                "is_cue": b.is_cue,
                "x": b.pos.x,
                "y": b.pos.y,
                "vx": b.vel.x,
                "vy": b.vel.y,
                "in_pocket": b.in_pocket
            })

        state = {
            "current_player": current_player,
            "scores": scores,
            "player_groups": player_groups,
            "table_theme_idx": table_theme_idx,
            "balls": balls_data
        }

        with open(SAVE_FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"⚠️ Error saving game state: {e}")
        return False


def load_game_state():
    if not os.path.exists(SAVE_FILE_PATH):
        return None

    try:
        with open(SAVE_FILE_PATH, "r", encoding="utf-8") as f:
            state = json.load(f)
        return state
    except Exception as e:
        print(f"⚠️ Error loading game state: {e}")
        return None
