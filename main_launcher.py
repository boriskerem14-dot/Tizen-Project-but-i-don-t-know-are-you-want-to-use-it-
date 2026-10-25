import pygame
import sys
import subprocess

# Инициализация
pygame.init()

WIDTH, HEIGHT = 320, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tizen OS - Home Launcher")

# Цветове
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 113, 206)
GRAY = (45, 45, 45)
GREEN = (0, 200, 100)
RED = (200, 50, 50)
PURPLE = (150, 50, 200)
ORANGE = (220, 130, 0)

font = pygame.font.SysFont("Arial", 14, bold=True)
font_large = pygame.font.SysFont("Arial", 18, bold=True)

# Списък с всички наши приложения и техните файлове
apps = [
    {"name": "Health", "script": "health_app.py", "color": GREEN},
    {"name": "Phone", "script": "phone_app.py", "color": BLUE},
    {"name": "Alarm", "script": "alarm_app.py", "color": RED},
    {"name": "Contacts", "script": "contacts_app.py", "color": (80, 120, 200)},
    {"name": "Calendar", "script": "calendar_app.py", "color": ORANGE},
    {"name": "Gallery", "script": "gallery_app.py", "color": PURPLE},
    {"name": "Galaxy Store", "script": "galaxy_store_app.py", "color": BLUE},
    {"name": "Bixby", "script": "bixby_app.py", "color": (0, 150, 150)}
]

# Разпределение в мрежа (Grid) 2 колони х 4 реда
app_rects = []
start_x, start_y = 20, 70
size_w, size_h = 130, 80
margin_x, margin_y = 20, 15

for idx, app in enumerate(apps):
    row = idx // 2
    col = idx % 2
    x = start_x + col * (size_w + margin_x)
    y = start_y + row * (size_h + margin_y)
    rect = pygame.Rect(x, y, size_w, size_h)
    app_rects.append((rect, app["script"]))

def draw_launcher():
    screen.fill(BLACK)
    
    # Заглавна лента на Tizen
    title = font_large.render("Tizen OS Launcher", True, WHITE)
    screen.blit(title, (20, 25))
    
    # Рисуване на иконите на приложенията
    for idx, (rect, script) in enumerate(app_rects):
        app = apps[idx]
        pygame.draw.rect(screen, app["color"], rect, border_radius=12)
        
        # Име на приложението вътре в бутона
        name_surf = font.render(app["name"], True, WHITE)
        screen.blit(name_surf, (rect.x + 15, rect.y + 30))

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            # Проверяваме кое приложение е натиснато
            for rect, script in app_rects:
                if rect.collidepoint(pos):
                    print(f"Стартиране на {script}...")
                    try:
                        # Стартираме отделния Python скрипт на приложението
                        subprocess.run(["python3", script])
                    except Exception as e:
                        print(f"Грешка при стартиране: {e}")
                        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    draw_launcher()
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
