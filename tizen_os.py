import subprocess
import sys
import os

def run_boot_animation():
    """Етап 1: Стартира буут анимацията (ако съществува)"""
    if os.path.exists("boot_sim.py"):
        print("[Tizen OS] Стартиране на буут анимация...")
        try:
            subprocess.run(["python3", "boot_sim.py"])
        except Exception as e:
            print(f"Грешка в буут скрипта: {e}")

def run_main_launcher():
    """Етап 2: Стартира главното меню с приложенията (Launcher)"""
    if os.path.exists("main_launcher.py"):
        print("[Tizen OS] Зареждане на главното меню (Launcher)...")
        try:
            subprocess.run(["python3", "main_launcher.py"])
        except Exception as e:
            print(f"Грешка в лаунчъра: {e}")
    else:
        print("[Грешка] Файлът main_launcher.py не е намерен!")

if __name__ == "__main__":
    print("=== Tizen OS за iPhone 2G / Debian стартира ===")
    
    # 1. Изпълняваме буут последователността
    run_boot_animation()
    
    # 2. След като зареди, преминаваме към лаунчъра и приложенията
    run_main_launcher()
    
    print("=== Tizen OS е изключена ===")
    sys.exit()
