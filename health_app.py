import pygame
import sys

# Инициализация
pygame.init()
WIDTH, HEIGHT = 320, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Samsung Health - Tizen Edition")

# Цветове
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 200, 100)
BLUE = (0, 120, 215)
GRAY = (100, 100, 100)
BUTTON_BG = (40, 40, 40)

# Шрифтове
font = pygame.font.SysFont("Arial", 16)
font_large = pygame.font.SysFont("Arial", 22, bold=True)

# Здравни данни по подразбиране
health_data = {
    "steps": 4230,
    "calories": 310,
    "water": 4,          # чаши
    "exercises": 1       # брой записани тренировки
}

# Дефиниране на бутоните като правоъгълници (x, y, широчина, височина)
water_button = pygame.Rect(20, 190, 130, 40)
exercise_button = pygame.Rect(165, 190, 135, 40)

def draw_health_dashboard():
    screen.fill(BLACK)
    
    # Заглавие
    title = font_large.render("Samsung Health", True, GREEN)
    screen.blit(title, (20, 20))
    
    # Статистика
    steps_text = font.render(f"🏃 Крачки: {health_data['steps']} / 10000", True, WHITE)
    cal_text = font.render(f"🔥 Калории: {health_data['calories']} kcal", True, WHITE)
    water_text = font.render(f"💧 Вода: {health_data['water']} чаши", True, BLUE)
    ex_text = font.render(f"🏋️ Упражнения: {health_data['exercises']} записани", True, WHITE)
    
    screen.blit(steps_text, (20, 65))
    screen.blit(cal_text, (20, 95))
    screen.blit(water_text, (20, 125))
    screen.blit(ex_text, (20, 155))
    
    # Рисуване на бутон 1: Добавяне на вода
    pygame.draw.rect(screen, BUTTON_BG, water_button, border_radius=8)
    pygame.draw.rect(screen, BLUE, water_button, 2, border_radius=8)
    w_text = font.render("+ Вода (💧)", True, WHITE)
    screen.blit(w_text, (water_button.x + 18, water_button.y + 10))
    
    # Рисуване на бутон 2: Запис на упражнение
    pygame.draw.rect(screen, BUTTON_BG, exercise_button, border_radius=8)
    pygame.draw.rect(screen, GREEN, exercise_button, 2, border_radius=8)
    e_text = font.render("+ Тренировка", True, WHITE)
    screen.blit(e_text, (exercise_button.x + 12, exercise_button.y + 10))
    
    # Навигационен съвет долу
    hint = font.render("Натисни ESC за изход", True, GRAY)
    screen.blit(hint, (20, 440))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Проверяваме дали координатите на клика/докосването попадат в бутоните
            if water_button.collidepoint(event.pos):
                health_data['water'] += 1
            elif exercise_button.collidepoint(event.pos):
                health_data['exercises'] += 1
                health_data['calories'] += 150  # Добавяме калории при тренировка
                
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    draw_health_dashboard()
    pygame.display.flip()
    pygame.time.Clock().tick(30)

pygame.quit()
sys.exit()
