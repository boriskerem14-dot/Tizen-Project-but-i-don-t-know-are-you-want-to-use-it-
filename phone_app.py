import pygame
import sys

# Инициализация
pygame.init()
WIDTH, HEIGHT = 320, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tizen Phone - Keypad & Calls")

# Цветове
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 200, 100)
RED = (220, 50, 50)
GRAY = (50, 50, 50)
LIGHT_GRAY = (80, 80, 80)

font = pygame.font.SysFont("Arial", 24, bold=True)
font_small = pygame.font.SysFont("Arial", 16)

# Набран номер
phone_number = ""
call_status = "Готов за набиране"

# Бутони на клавиатурата (позиции и символи)
buttons = [
    ("1", 30, 140), ("2", 120, 140), ("3", 210, 140),
    ("4", 30, 200), ("5", 120, 200), ("6", 210, 200),
    ("7", 30, 260), ("8", 120, 260), ("9", 210, 260),
    ("*", 30, 320), ("0", 120, 320), ("#", 210, 320)
]

# Създаване на правоъгълници за бутоните
button_rects = {}
for text, x, y in buttons:
    button_rects[text] = pygame.Rect(x, y, 80, 50)

# Бутони за набиране и изтриване
call_btn = pygame.Rect(30, 390, 120, 45)
backspace_btn = pygame.Rect(170, 390, 120, 45)

def draw_phone_screen():
    screen.fill(BLACK)
    
    # 1. Поле за набиране на номера
    pygame.draw.rect(screen, GRAY, (20, 30, 280, 50), border_radius=8)
    num_surface = font.render(phone_number if phone_number else "Въведи номер...", True, WHITE if phone_number else LIGHT_GRAY)
    screen.blit(num_surface, (35, 43))
    
    # 2. Статус на обаждането
    status_surface = font_small.render(call_status, True, GREEN if "Звъни" in call_status else WHITE)
    screen.blit(status_surface, (20, 95))
    
    # 3. Рисуване на цифровата клавиатура
    for text, x, y in buttons:
        rect = button_rects[text]
        pygame.draw.rect(screen, GRAY, rect, border_radius=8)
        txt_surface = font.render(text, True, WHITE)
        screen.blit(txt_surface, (x + 32, y + 10))
        
    # 4. Зелен бутон за обаждане
    pygame.draw.rect(screen, GREEN, call_btn, border_radius=8)
    call_txt = font_small.render("📞 Обади се", True, WHITE)
    screen.blit(call_txt, (call_btn.x + 20, call_btn.y + 13))
    
    # 5. Червен бутон за изтриване (Backspace)
    pygame.draw.rect(screen, RED, backspace_btn, border_radius=8)
    bs_txt = font_small.render("Изтрий", True, WHITE)
    screen.blit(bs_txt, (backspace_btn.x + 35, backspace_btn.y + 13))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            
            # Проверка коя цифра е натисната
            for text, rect in button_rects.items():
                if rect.collidepoint(pos):
                    if len(phone_number) < 12:
                        phone_number += text
                        
            # Натискане на бутон за обаждане
            if call_btn.collidepoint(pos):
                if phone_number:
                    call_status = f"Звъни на {phone_number}..."
                else:
                    call_status = "Моля, въведи номер!"
                    
            # Натискане на бутон за изтриване
            elif backspace_btn.collidepoint(pos):
                phone_number = phone_number[:-1]
                call_status = "Готов за набиране"
                
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.unicode.isdigit() or event.unicode in ('*', '#'):
                if len(phone_number) < 12:
                    phone_number += event.unicode
            elif event.key == pygame.K_BACKSPACE:
                phone_number = phone_number[:-1]

    draw_phone_screen()
    pygame.display.flip()
    pygame.time.Clock().tick(30)

pygame.quit()
sys.exit()
