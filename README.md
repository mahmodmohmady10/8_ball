# 🎱 2D Billiards Championship - Version 5.0 (V5)

A complete, commercial-grade 2D Billiards game built with **Python** and **Pygame-CE**, featuring a **Full English Interface**, **Interactive Main Menu**, **In-Game Pause Menu**, **Victory Screen**, **AI Opponent**, **Trick Shots**, and **Realistic Physics**.

---

## 📁 Project Directory Structure (V5)

```text
billiards_project_v5/
├── start.py                # 🚀 Smart One-Click Game Launcher V5
├── check_requirements.py   # Environment & Dependencies Inspector V5
├── requirements.txt        # Required Packages List
├── README.md               # English Documentation V5
├── CHANGELOG.md            # Complete Release Notes for V5
└── src/
    ├── __init__.py        # Python package initialization
    ├── main.py            # Main State Machine (Menu, Playing, Pause, Victory, Help)
    ├── ai_bot.py          # AI Opponent Shot Vector & Angle Calculations
    ├── save_system.py     # JSON Auto-Save & Resume System
    ├── ball.py            # Solid vs Striped Balls, Target Glow, Pocket Animations
    ├── physics.py          # Elastic Impulse Collision Engine
    ├── table.py            # Customizable Felt Themes & Scoreboard HUD
    ├── ui.py              # English Buttons, Menus, Aim Line, Power Bar & Spin Widget
    ├── particles.py        # Fire Trail & Green/Red Pocket Flash Spark Systems
    └── sound.py            # Self-Contained Procedural Sound Engine
```

---

## 🚀 How to Launch (One-Click Launch V5)

Simply run the smart launcher to inspect dependencies and boot into the Main Menu:

```bash
python start.py
```

---

## 🌟 Major V5 Highlights & Controls

1. **Interactive Main Menu:** Choose between 1v1 PvP, VS AI Bot, Trick Shots, or view the How to Play Guide.
2. **In-Game Pause Overlay (`ESC` / `[PAUSE]`):** Pause anytime to resume, restart match, toggle table felts, or return to the menu.
3. **Victory Screen Modal:** End-of-match popup announcing the Winner with `Play Again` and `Main Menu` options.
4. **Controls:**
   - **Aiming & Shooting:** Click & Drag from Cue Ball to aim and adjust power, then release to shoot.
   - **Spin / English:** Click the bottom-left Cue Ball widget to apply Topspin, Backspin, or Sidespin.
   - **Table Felt Themes:** Press `T` during gameplay to switch between Classic Green, Royal Blue, Ruby Red, and Midnight Purple.
