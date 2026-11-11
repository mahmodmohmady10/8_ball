import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

from check_requirements import check_and_install_requirements

def start_application():
    print("\n" + "=" * 68)
    print(" 🚀 2D Billiards Game Launcher - Version 5.0 (V5)")
    print("=" * 68 + "\n")

    check_and_install_requirements()

    try:
        import pygame
    except ImportError:
        print("\n❌ Pygame library is not installed.")
        print("💡 Please install manually via: pip install pygame-ce")
        sys.exit(1)

    print("\n🚀 All dependencies verified! Opening Game Main Menu...\n")
    
    try:
        from src.main import main
        main()
    except Exception as e:
        print(f"\n❌ Unexpected error while launching game: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    start_application()
