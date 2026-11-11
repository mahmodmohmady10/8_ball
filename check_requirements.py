import sys
import os
import subprocess
import importlib

def check_and_install_requirements():
    print("=" * 68)
    print(" 🔍 Environment & Dependencies Inspector - Billiards 2D V5")
    print("=" * 68)

    python_ver = sys.version_info
    print(f"[*] Current Python Version: {python_ver.major}.{python_ver.minor}.{python_ver.micro}")
    if python_ver.major < 3 or (python_ver.major == 3 and python_ver.minor < 8):
        print("❌ Warning: Python 3.8 or higher is recommended.")
    else:
        print("✅ Python version is fully supported.")

    print("-" * 68)

    required_packages = [
        {
            "import_name": "pygame",
            "package_name": "pygame-ce",
            "label": "Pygame-CE (2D Engine, Audio & UI Framework)",
            "download_size": "~12 - 15 MB"
        }
    ]

    missing_packages = []

    print("[*] Checking Required Python Libraries:")
    for pkg in required_packages:
        try:
            mod = importlib.import_module(pkg["import_name"])
            version = getattr(mod, "__version__", "Unknown")
            print(f"  └─ ✅ {pkg['label']} is installed (Version: {version}).")
        except ImportError:
            print(f"  └─ ❌ {pkg['label']} is MISSING!")
            missing_packages.append(pkg)

    print("-" * 68)

    project_files = [
        "requirements.txt",
        "README.md",
        "CHANGELOG.md",
        "src/main.py",
        "src/ai_bot.py",
        "src/save_system.py",
        "src/physics.py",
        "src/ball.py",
        "src/table.py",
        "src/ui.py",
        "src/particles.py",
        "src/sound.py"
    ]

    print("[*] Verifying V5 Project Structure & Assets:")
    all_files_exist = True
    for file_path in project_files:
        if os.path.exists(file_path):
            print(f"  └─ ✅ {file_path}")
        else:
            print(f"  └─ ❌ {file_path} MISSING!")
            all_files_exist = False

    print("=" * 68)

    if missing_packages:
        print("⚠️ Missing required libraries detected:\n")
        for item in missing_packages:
            print(f"   📦 Package: {item['package_name']}")
            print(f"   📊 Estimated Download Size: {item['download_size']}\n")

        prompt_msg = "❓ Would you like to download and install missing packages now? (y/n): "
        try:
            user_input = input(prompt_msg).strip().lower()
        except EOFError:
            user_input = "n"

        if user_input in ["y", "yes", "1"]:
            print("\n🚀 Starting installation via pip...")
            for item in missing_packages:
                cmd = [sys.executable, "-m", "pip", "install", item["package_name"]]
                print(f"[*] Running command: {' '.join(cmd)}")
                try:
                    subprocess.check_call(cmd)
                    print(f"🎉 Successfully installed {item['package_name']}!")
                except subprocess.CalledProcessError:
                    print(f"⚠️ Primary package failed, trying fallback (pygame)...")
                    try:
                        subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame"])
                        print("🎉 Fallback pygame installed successfully!")
                    except Exception as e:
                        print(f"❌ Automatic install failed: {e}")
                        print("Please run manually: pip install pygame-ce")

            print("\n✅ Setup complete! Launch the game with: python start.py")
        else:
            print("\n⏸️ Installation canceled by user.")
            print("You can install manually anytime with: pip install pygame-ce")

    else:
        if all_files_exist:
            print("🎉 All requirements and project files are ready!")
            print("🚀 Launching Game Menu via: python start.py")
        else:
            print("⚠️ Packages installed but some project files are missing.")

if __name__ == "__main__":
    check_and_install_requirements()
