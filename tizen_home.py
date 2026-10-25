import pygame
import sys
import datetime
import urllib.request
import json
import os

# Инициализиране на Pygame
pygame.init()

# Параметри на екрана на iPhone 2G (320x480)
WIDTH, HEIGHT = 320, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tizen OS - Home Screen & Wallpaper Simulator")

# Цветове
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)
BLUE = (0, 120, 215)

# Шрифтове
font_large = pygame.font.SysFont("Arial", 54, bold=True)
font_medium = pygame.font.SysFont("Arial", 22)
font_small = pygame.font.SysFont("Arial", 16)

clock = pygame.time.Clock()

# Зареждане на тапета wallpaper.png, ако съществува
wallpaper_path = "wallpaper.png"
if os.path.exists(wallpaper_path):
    wallpaper_img = pygame.image.load(wallpaper_path)
    wallpaper_img = pygame.transform.scale(wallpaper_img, (WIDTH, HEIGHT))
else:
    wallpaper_img = None

def get_weather():
    try:
        url = "https://wttr.in/?format=j1"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=2) as response:
            data = json.loads(response.read().decode())
            temp = data['current_condition'][0]['temp_C']
            return f"{temp}°C"
    except:
        return "22°C"

current_temp = get_weather()

# Състояние на екрана: False = часовник/джаджи, True = само тапет (Home екран)
show_wallpaper = False

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            # Симулиране на Home бутона с клавиш 'h' или 'SPACE'
            elif event.key == pygame.K_h or event.key == pygame.K_SPACE:
                show_wallpaper = not show_wallpaper

    # Вземане на текущ час и дата
    now = datetime.datetime.now()
    time_str = now.strftime("%H:%M")
    date_str = now.strftime("%A, %d %B")

    # Рендиране според състоянието
    if show_wallpaper and wallpaper_img:
        # Показване само на тапета при натиснат Home бутон
        screen.blit(wallpaper_img, (0, 0))
        
        # Малък надпис долу за улеснение в симулатора
        hint_surface = font_small.render("Home Screen (Натисни H за назад)", True, WHITE)
        screen.blit(hint_surface, (10, HEIGHT - 30))
    else:
        # Стандартен екран с час, дата и време
        screen.fill(BLACK)

        if wallpaper_img:
            # Може да се сложи полупрозрачен тапет за фон
            screen.blit(wallpaper_img, (0, 0))
            # Тъмен филтър за четимост на текста
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(150)
            overlay.fill(BLACK)
            screen.blit(overlay, (0, 0))

        # 1. Час
        time_surface = font_large.render(time_str, True, WHITE)
        time_rect = time_surface.get_rect(center=(WIDTH // 2, 100))
        screen.blit(time_surface, time_rect)

        # 2. Дата
        date_surface = font_medium.render(date_str, True, GRAY)
        date_rect = date_surface.get_rect(center=(WIDTH // 2, 160))
        screen.blit(date_surface, date_rect)

        # 3. Температура
        weather_surface = font_medium.render(f"📍 Навън: {current_temp}", True, BLUE)
        weather_rect = weather_surface.get_rect(center=(WIDTH // 2, 220))
        screen.blit(weather_surface, weather_rect)
        
        hint_surface = font_small.render("Натисни H за Wallpaper", True, GRAY)
        screen.blit(hint_surface, (60, HEIGHT - 30))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
