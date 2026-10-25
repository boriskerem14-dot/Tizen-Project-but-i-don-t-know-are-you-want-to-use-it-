import pygame
import sys

# Инициализация
pygame.init()

WIDTH, HEIGHT = 320, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tizen Contacts - Social Sync")

# Цветове
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 200, 100)
BLUE = (0, 120, 215)
GRAY = (50, 50, 50)
LIGHT_GRAY = (80, 80, 80)
POPUP_BG = (30, 30, 30)

# Шрифтове
font = pygame.font.SysFont("Arial", 18, bold=True)
font_small = pygame.font.SysFont("Arial", 14)

# Примерни контакти от социални мрежи
contacts = [
    {"name": "Skittle (Borko)", "phone": "+359881234567", "source": "Viber"},
    {"name": "Lumo (Proton)", "phone": "+359899876543", "source": "Telegram"},
    {"name": "Developer Friend", "phone": "+359877112233", "source": "Discord"},
    {"name": "Classmate Ani", "phone": "+359885554433", "source": "Viber"}
]

# Състояние на приложението
selected_contact = None  # Кой контакт е натиснат за меню
action_status = "Избери контакт..."

# Бутони за изскачащото меню (когато е избран контакт)
call_option_btn = pygame.Rect(60, 220, 200, 45)
sms_option_btn = pygame.Rect(60, 280, 200, 45)
close_popup_btn = pygame.Rect(60, 340, 200, 40)

def draw_screen():
    screen.fill(BLACK)
    
    # Заглавие
    title = font.render("👥 Социални Контакти", True, GREEN)
    screen.blit(title, (20, 15))
    
    # Статус лента долу
    status_surf = font_small.render(action_status, True, WHITE)
    screen.blit(status_surf, (20, 450))
    
    # Рисуване на списъка с контакти
    y_offset = 60
    global contact_rects
    contact_rects = []
    
    for i, c in enumerate(contacts):
        rect = pygame.Rect(15, y_offset, 290, 65)
        contact_rects.append((rect, c))
        
        # Фон на картата на контакта
        pygame.draw.rect(screen, GRAY, rect, border_radius=8)
        
        # Име на контакта
        name_surf = font.render(c["name"], True, WHITE)
        screen.blit(name_surf, (rect.x + 15, rect.y + 10))
        
        # Телефон и източник (социална мрежа)
        info_surf = font_small.render(f"{c['phone']} • {c['source']}", True, LIGHT_GRAY)
        screen.blit(info_surf, (rect.x + 15, rect.y + 35))
        
        y_offset += 75

    # Ако е избран контакт, показваме изскачащо меню (Popup)
    if selected_contact:
        # Затемняващ фон
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))

# Меню кутия
        popup_box = pygame.Rect(40, 140, 240, 260)
        pygame.draw.rect(screen, POPUP_BG, popup_box, border_radius=12)
        pygame.draw.rect(screen, BLUE, popup_box, 2, border_radius=12)
        
        # Име на избрания контакт в менюто
        sel_title = font.render(selected_contact["name"], True, WHITE)
        screen.blit(sel_title, (popup_box.x + 20, popup_box.y + 20))
        
        # Бутон Обаждане
        pygame.draw.rect(screen, GREEN, call_option_btn, border_radius=8)
        screen.blit(font.render("📞 Обаждане", True, WHITE), (call_option_btn.x + 40, call_option_btn.y + 12))
        
        # Бутон SMS
        pygame.draw.rect(screen, BLUE, sms_option_btn, border_radius=8)
        screen.blit(font.render("💬 Изпрати SMS", True, WHITE), (sms_option_btn.x + 30, sms_option_btn.y + 12))
        
        # Бутон за затваряне на менюто
        pygame.draw.rect(screen, GRAY, close_popup_btn, border_radius=8)
        screen.blit(font_small.render("Отказ", True, WHITE), (close_popup_btn.x + 80, close_popup_btn.y + 11))

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            
            if selected_contact:
                # Ако менюто е отворено, проверяваме бутоните му
                if call_option_btn.collidepoint(pos):
                    action_status = f"Звъни на {selected_contact['phone']}..."
                    selected_contact = None  # Затваряне на менюто
                elif sms_option_btn.collidepoint(pos):
                    action_status = f"Писане на SMS до {selected_contact['phone']}"
                    selected_contact = None
                elif close_popup_btn.collidepoint(pos):
                    selected_contact = None
            else:
                # Проверяваме кой контакт е кликнат в списъка
                for rect, contact in contact_rects:
                    if rect.collidepoint(pos):
                        selected_contact = contact
                        action_status = f"Избран: {contact['name']}"
                        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if selected_contact:
                    selected_contact = None
                else:
                    running = False

    draw_screen()
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
