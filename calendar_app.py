import pygame
import sys
import datetime
import calendar

# Инициализация
pygame.init()

WIDTH, HEIGHT = 320, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tizen Calendar & Events")

# Цветове
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 200, 100)
BLUE = (0, 120, 215)
GRAY = (50, 50, 50)
LIGHT_GRAY = (80, 80, 80)

# Шрифтове
font = pygame.font.SysFont("Arial", 16, bold=True)
font_small = pygame.font.SysFont("Arial", 14)

# Текуща дата
now = datetime.datetime.now()
curr_year = now.year
curr_month = now.month
selected_day = now.day

# Речник със събития
events = {
    (curr_year, curr_month, 15): ["Рожден ден на приятел"],
    (curr_year, curr_month, 20): ["Проект за Tizen OS"]
}

# Бутони за смяна на месец
prev_btn = pygame.Rect(20, 15, 40, 30)
next_btn = pygame.Rect(260, 15, 40, 30)

# Бутон за добавяне на събитие на избрания ден
add_event_btn = pygame.Rect(20, 430, 280, 35)

def draw_calendar():
    screen.fill(BLACK)
    
    # Заглавие (Месец и Година)
    month_name = calendar.month_name[curr_month]
    title_surf = font.render(f"{month_name} {curr_year}", True, GREEN)
    screen.blit(title_surf, (85, 20))
    
    # Бутони за навигация < >
    pygame.draw.rect(screen, GRAY, prev_btn, border_radius=6)
    screen.blit(font.render("<", True, WHITE), (prev_btn.x + 14, prev_btn.y + 5))
    
    pygame.draw.rect(screen, GRAY, next_btn, border_radius=6)
    screen.blit(font.render(">", True, WHITE), (next_btn.x + 14, next_btn.y + 5))
    
    # Дни от седмицата
    days_of_week = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Нд"]
    for i, day in enumerate(days_of_week):
        d_surf = font_small.render(day, True, LIGHT_GRAY)
        screen.blit(d_surf, (25 + (i * 40), 65))
        
    # Календарна мрежа
    cal_matrix = calendar.monthcalendar(curr_year, curr_month)
    
    global day_rects
    day_rects = []
    
    start_y = 95
    for row_idx, week in enumerate(cal_matrix):
        for col_idx, day in enumerate(week):
            if day == 0:
                continue
            
            dx = 20 + (col_idx * 40)
            dy = start_y + (row_idx * 35)
            d_rect = pygame.Rect(dx, dy, 32, 30)
            day_rects.append((d_rect, day))
            
            bg_color = BLUE if day == selected_day else GRAY
            if (curr_year, curr_month, day) in events:
                bg_color = (0, 150, 100)
                
            pygame.draw.rect(screen, bg_color, d_rect, border_radius=6)
            
            day_surf = font_small.render(str(day), True, WHITE)
            screen.blit(day_surf, (dx + 8, dy + 6))

# Секция със събития
    event_box_y = 300
    pygame.draw.rect(screen, GRAY, (20, event_box_y, 280, 120), border_radius=8)
    
    sel_title = font.render(f"Събития за {selected_day} {month_name}:", True, WHITE)
    screen.blit(sel_title, (30, event_box_y + 10))
    
    day_events = events.get((curr_year, curr_month, selected_day), [])
    if day_events:
        for idx, ev in enumerate(day_events[:3]):
            ev_surf = font_small.render(f"- {ev}", True, WHITE)
            screen.blit(ev_surf, (30, event_box_y + 40 + (idx * 20)))
    else:
        no_ev = font_small.render("Няма събития за този ден.", True, LIGHT_GRAY)
        screen.blit(no_ev, (30, event_box_y + 45))
        
    # Бутон за добавяне на събитие
    pygame.draw.rect(screen, BLUE, add_event_btn, border_radius=6)
    add_txt = font_small.render("+ Добави събитие (симулация)", True, WHITE)
    screen.blit(add_txt, (add_event_btn.x + 40, add_event_btn.y + 9))

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            
            # Смяна на месец назад
            if prev_btn.collidepoint(pos):
                curr_month -= 1
                if curr_month < 1:
                    curr_month = 12
                    curr_year -= 1
            # Смяна на месец напред
            elif next_btn.collidepoint(pos):
                curr_month += 1
                if curr_month > 12:
                    curr_month = 1
                    curr_year += 1
                    
            # Добавяне на ново симулирано събитие
            elif add_event_btn.collidepoint(pos):
                key = (curr_year, curr_month, selected_day)
                if key not in events:
                    events[key] = []
                events[key].append(f"Нова задача за {selected_day}")
                
            else:
                # Избор на ден от календара
                for d_rect, day in day_rects:
                    if d_rect.collidepoint(pos):
                        selected_day = day
                    
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    draw_calendar()
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
