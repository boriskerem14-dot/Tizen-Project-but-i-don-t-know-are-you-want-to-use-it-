import pygame
import sys
import os

# Инициализиране на Pygame
pygame.init()

# Параметри на екрана на iPhone 2G
WIDTH, HEIGHT = 320, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tizen / Apple Boot Simulator - iPhone 2G")

# Цветове
BLACK = (0, 0, 0)
WHITE = (200, 200, 200)

# Зареждане на генерираното лого или рисуване директно
logo_path = "apple_boot_logo.png"
if os.path.exists(logo_path):
    logo_img = pygame.image.load(logo_path)
    # Центриране на логото
    logo_rect = logo_img.get_rect(center=(WIDTH // 2, HEIGHT // 2))
else:
    logo_img = None

clock = pygame.time.Clock()
running = True
alpha = 0  # За ефект на плавно светване (fade-in)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # Запълване на екрана с черно (фон при зареждане)
    screen.fill(BLACK)

    # Показване на логото с плавно появяване
    if logo_img:
        # Може да се добави alpha ефект или директно рисуване
        screen.blit(logo_img, logo_rect)
    else:
        # Резервен вариант: рисуване на елемент
        pygame.draw.ellipse(screen, WHITE, (130, 200, 60, 70))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
