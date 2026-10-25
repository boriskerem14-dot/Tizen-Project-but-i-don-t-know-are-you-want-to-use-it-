import pygame
import sys
import datetime
import os

# Инициализация на Pygame и Mixer за аудио
pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 320, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tizen Alarm - MP3 Ringtones")

# Цветове
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 200, 100)
RED = (220, 50, 50)
GRAY = (60, 60, 60)
BLUE = (0, 120, 215)

font = pygame.font.SysFont("Arial", 20, bold=True)
font_small = pygame.font.SysFont("Arial", 14)

# Настройки на алармата (по подразбиране: след малко или зададен час)
alarm_hour = datetime.datetime.now().hour
alarm_minute = datetime.datetime.now().minute + 1 # Пример: след 1 минута
if alarm_minute >= 60:
    alarm_minute = 0
    alarm_hour = (alarm_hour + 1) % 24

alarm_active = False
ringtone_playing = False

# Списък с налични MP3 рингтонове (от твоите файлове)
ringtones = [
    {"name": "Boss Battle", "file": "boss_battle.mp3"},
    {"name": "Castle Theme", "file": "castle_theme.mp3"},
    {"name": "File Select", "file": "file_select.mp3"},
    {"name": "Final Battle", "file": "final_battle.mp3"}
]
selected_ringtone_idx = 0

# Бутони за интерфейса
toggle_btn = pygame.Rect(30, 260, 260, 45)
next_ringtone_btn = pygame.Rect(30, 320, 260, 40)
stop_btn = pygame.Rect(30, 380, 260, 45)

def draw_screen(current_time_str):
    screen.fill(BLACK)
    
    # Заглавие
    title = font.render("⏰ Tizen Alarm Clock", True, GREEN)
    screen.blit(title, (50, 20))
    
    # Текущ час
    curr_lbl = font_small.render(f"Текущ час: {current_time_str}", True, WHITE)
    screen.blit(curr_lbl, (30, 70))
    
    # Зададен час на алармата
    alarm_str = f"{alarm_hour:02d}:{alarm_minute:02d}"
    alarm_box_color = RED if alarm_active else GRAY
    pygame.draw.rect(screen, alarm_box_color, (30, 100, 260, 60), border_radius=10)
    
    alarm_lbl = font.render(f"Аларма: {alarm_str}", True, WHITE)
    screen.blit(alarm_lbl, (70, 115))
    
    status_text = "Статус: Включена" if alarm_active else "Статус: Изключена"
    status_lbl = font_small.render(status_text, True, GREEN if alarm_active else WHITE)
    screen.blit(status_lbl, (30, 175))
    
    # Избран рингтон
    current_ringtone = ringtones[selected_ringtone_idx]["name"]
    ring_lbl = font_small.render(f"🎶 Рингтон: {current_ringtone}", True, BLUE)
    screen.blit(ring_lbl, (30, 210))
    
    # Бутон за Вкл/Изкл на алармата
    pygame.draw.rect(screen, GREEN if not alarm_active else RED, toggle_btn, border_radius=8)
    toggle_txt = font.render("Включи / Изключи алармата", True, WHITE)
    screen.blit(toggle_txt, (toggle_btn.x + 15, toggle_btn.y + 12))
    
    # Бутон за смяна на рингтон
    pygame.draw.rect(screen, GRAY, next_ringtone_btn, border_radius=8)
    ring_btn_txt = font_small.render("Смени рингтона (следващ)", True, WHITE)
    screen.blit(ring_btn_txt, (next_ringtone_btn.x + 40, next_ringtone_btn.y + 12))
    
    # Бутон за спиране при звънене
    pygame.draw.rect(screen, RED, stop_btn, border_radius=8)
    stop_txt = font.render("Спри алармата / Музиката", True, WHITE)
    screen.blit(stop_txt, (stop_btn.x + 30, stop_btn.y + 12))

clock = pygame.time.Clock()
running = True

while running:
    now = datetime.datetime.now()
    time_str = now.strftime("%H:%M:%S")
    
    # Проверка дали е време за аларма
    if alarm_active and not ringtone_playing:
        if now.hour == alarm_hour and now.minute == alarm_minute and now.second == 0:
            ringtone_playing = True
            file_to_play = ringtones[selected_ringtone_idx]["file"]
            if os.path.exists(file_to_play):
                pygame.mixer.music.load(file_to_play)
                pygame.mixer.music.play(-1) # -1 означава повтаряне (loop) без спиране
            else:
                print(f"[Грешка] Файлът {file_to_play} не е намерен в паката!")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            if toggle_btn.collidepoint(pos):
                alarm_active = not alarm_active
            elif next_ringtone_btn.collidepoint(pos):
                selected_ringtone_idx = (selected_ringtone_idx + 1) % len(ringtones)
            elif stop_btn.collidepoint(pos):
                alarm_active = False
                ringtone_playing = False
                pygame.mixer.music.stop()
                
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_UP:
                # Увеличаване на часа с клавиш Стрелка нагоре
                alarm_hour = (alarm_hour + 1) % 24
            elif event.key == pygame.K_DOWN:
                # Намаляване на часа с клавиш Стрелка надолу
                alarm_minute = (alarm_minute + 5) % 60

    draw_screen(now.strftime("%H:%M"))
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
