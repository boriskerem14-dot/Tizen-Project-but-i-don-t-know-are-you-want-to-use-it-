import pygame
import sys
import urllib.request
import json
import os

# Инициализация
pygame.init()

WIDTH, HEIGHT = 320, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Samsung Galaxy Store")

# Цветове
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 113, 206)      # Samsung Blue
GRAY = (50, 50, 50)
LIGHT_GRAY = (90, 90, 90)
GREEN = (0, 200, 100)

font = pygame.font.SysFont("Arial", 16, bold=True)
font_small = pygame.font.SysFont("Arial", 14)

# Състояния на приложението
STATE_LOGIN = 1
STATE_SMS = 2
STATE_STORE = 3
current_state = STATE_LOGIN

# Полета за вход
email_input = "user@samsung.com"
pass_input = "********"
sms_input = ""
server_status = "Готов за връзка със сървъра"

# Приложение от магазина за сваляне
store_apps = [
    {"name": "Samsung Health Pro", "size": "12 MB", "file": "health_app.py"},
    {"name": "Tizen Browser", "size": "8 MB", "file": "browser_app.py"},
    {"name": "Galaxy Notes", "size": "5 MB", "file": "notes_app.py"}
]
download_status = ""

# Бутони
login_btn = pygame.Rect(20, 310, 280, 40)
verify_btn = pygame.Rect(20, 310, 280, 40)

def draw_store():
    screen.fill(BLACK)
    
    if current_state == STATE_LOGIN:
        # Екран за Samsung Account - Имейл и Парола
        title = font.render("Samsung Account", True, BLUE)
        screen.blit(title, (20, 30))
        
        lbl = font_small.render("Въведете имейл адрес:", True, WHITE)
        screen.blit(lbl, (20, 80))
        pygame.draw.rect(screen, GRAY, (20, 110, 280, 40), border_radius=6)
        screen.blit(font.render(email_input, True, WHITE), (30, 120))
        
        lbl_p = font_small.render("Парола:", True, WHITE)
        screen.blit(lbl_p, (20, 170))
        pygame.draw.rect(screen, GRAY, (20, 200, 280, 40), border_radius=6)
        screen.blit(font.render(pass_input, True, WHITE), (30, 210))
        
        st = font_small.render(server_status, True, LIGHT_GRAY)
        screen.blit(st, (20, 260))

# Бутон за вход
        pygame.draw.rect(screen, BLUE, login_btn, border_radius=6)
        screen.blit(font.render("Вход / Изпрати SMS код", True, WHITE), (45, 320))

    elif current_state == STATE_SMS:
        # Екран за въвеждане на SMS верификационен код
        title = font.render("Потвърждение с SMS", True, BLUE)
        screen.blit(title, (20, 30))
        
        info = font_small.render("Кодът е изпратен от Samsung до", True, WHITE)
        info2 = font_small.render(email_input, True, GREEN)
        screen.blit(info, (20, 70))
        screen.blit(info2, (20, 95))
        
        pygame.draw.rect(screen, GRAY, (20, 150, 280, 45), border_radius=6)
        screen.blit(font.render(sms_input if sms_input else "Въведете 6-цифрен код...", True, WHITE), (35, 163))
        
        pygame.draw.rect(screen, GREEN, verify_btn, border_radius=6)
        screen.blit(font.render("Потвърди и Свържи със сървъра", True, WHITE), (25, 320))

    elif current_state == STATE_STORE:
        # Главен екран на Galaxy Store
        title = font.render("Galaxy Store - Сървър онлайн", True, BLUE)
        screen.blit(title, (20, 20))
        
        y_off = 70
        for app in store_apps:
            rect = pygame.Rect(20, y_off, 280, 60)
            pygame.draw.rect(screen, GRAY, rect, border_radius=8)
            
            name_s = font.render(app["name"], True, WHITE)
            size_s = font_small.render(f"Размер: {app['size']}", True, LIGHT_GRAY)
            screen.blit(name_s, (35, y_off + 10))
            screen.blit(size_s, (35, y_off + 32))
            
            # Бутон "Сваляне"
            dl_btn = pygame.Rect(205, y_off + 15, 85, 30)
            pygame.draw.rect(screen, BLUE, dl_btn, border_radius=4)
            screen.blit(font_small.render("Инсталирай", True, WHITE), (212, y_off + 22))
            app['btn_rect'] = dl_btn
            
            y_off += 75
            
        # Статус на сваляне долу
        st_dl = font_small.render(download_status, True, GREEN)
        screen.blit(st_dl, (20, 440))

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            
            if current_state == STATE_LOGIN:
                if login_btn.collidepoint(pos):
                    server_status = "Свързване със сървърите на Samsung..."
                    current_state = STATE_SMS  # Преминаваме към SMS проверка
                    
            elif current_state == STATE_SMS:
                if verify_btn.collidepoint(pos):
                    # Симулираме успешен отговор от сървъра
                    current_state = STATE_STORE
                    server_status = "Успешна оторизация!"
                    
            elif current_state == STATE_STORE:
                for app in store_apps:
                    if 'btn_rect' in app and app['btn_rect'].collidepoint(pos):
                        download_status = f"Сваляне на {app['name']} от сървъра..."
                        # Тук симулираме мрежово изтегляне на приложението
                        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif current_state == STATE_SMS:
                if event.unicode.isdigit() and len(sms_input) < 6:
                    sms_input += event.unicode
                elif event.key == pygame.K_BACKSPACE:
                    sms_input = sms_input[:-1]

    draw_store()
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
