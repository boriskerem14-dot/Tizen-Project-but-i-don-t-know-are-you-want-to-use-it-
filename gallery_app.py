import pygame
import sys
import os

# Инициализация
pygame.init()

WIDTH, HEIGHT = 320, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tizen Gallery - Slideshow")

# Цветове
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (50, 50, 50)
BLUE = (0, 120, 215)
GREEN = (0, 200, 100)

font = pygame.font.SysFont("Arial", 16)
font_large = pygame.font.SysFont("Arial", 20, bold=True)

# Зареждане на снимки
def load_photos():
    photos = []
    for file in os.listdir("."):
        if file.lower().endswith(('.png', '.jpg', '.jpeg')):
            photos.append(file)
    return photos

photos = load_photos()
selected_photo_idx = None
slideshow_active = False

# Таймер за смяна на кадрите в слайдшоуто (в милисекунди, напр. 3000ms = 3 секунди)
SLIDESHOW_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SLIDESHOW_EVENT, 3000)

# Бутони
back_btn = pygame.Rect(20, 430, 130, 35)
slideshow_btn = pygame.Rect(170, 430, 130, 35)
thumb_rects = []

def draw_gallery():
    screen.fill(BLACK)
    
    # Заглавие
    title_text = "🖼️ Слайдшоу" if slideshow_active else "🖼️ Tizen Галерия"
    title = font_large.render(title_text, True, WHITE)
    screen.blit(title, (20, 15))
    
    global thumb_rects
    thumb_rects = []

    if selected_photo_idx is not None:
        # Режим на цял екран или слайдшоу за избраната снимка
        photo_name = photos[selected_photo_idx]
        try:
            img = pygame.image.load(photo_name)
            img = pygame.transform.scale(img, (320, 350))
            screen.blit(img, (0, 60))
        except:
            err_txt = font.render("Грешка при зареждане", True, (255, 0, 0))
            screen.blit(err_txt, (20, 200))
            
        # Бутон за връщане
        pygame.draw.rect(screen, BLUE, back_btn, border_radius=6)
        screen.blit(font.render("⬅ Назад", True, WHITE), (back_btn.x + 35, back_btn.y + 8))
        
        # Бутон за Вкл/Изкл на слайдшоуто
        btn_color = GREEN if slideshow_active else GRAY
        pygame.draw.rect(screen, btn_color, slideshow_btn, border_radius=6)
        slideshow_txt = "Спри шоу" if slideshow_active else "▶ Слайдшоу"
        screen.blit(font.render(slideshow_txt, True, WHITE), (slideshow_btn.x + 20, slideshow_btn.y + 8))
        
    else:
        # Режим на мрежа с миниатюри
        if not photos:
            no_img = font.render("Няма снимки в папката!", True, (200, 200, 200))
            screen.blit(no_img, (20, 200))
            return
            
        cols = 3
        size = 90
        margin = 12
        start_x = 16
        start_y = 60
        
        for idx, photo in enumerate(photos):
            row = idx // cols
            col = idx % cols
            
            x = start_x + col * (size + margin)
            y = start_y + row * (size + margin)
            
            rect = pygame.Rect(x, y, size, size)
            thumb_rects.append((rect, idx))
            
            pygame.draw.rect(screen, GRAY, rect, border_radius=6)
            
            try:
                thumb = pygame.image.load(photo)
                thumb = pygame.transform.scale(thumb, (size, size))
                screen.blit(thumb, (x, y))
            except:
                pass
                
            pygame.draw.rect(screen, WHITE, rect, 1, border_radius=6)
            
        # Бутон за директно стартиране на слайдшоу от главното меню
        if photos:
            pygame.draw.rect(screen, GREEN, (20, 430, 280, 35), border_radius=6)
            screen.blit(font.render("▶ Пусни цялото слайдшоу", True, WHITE), (60, 438))

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        # Автоматична смяна на снимка при задействане на таймера
        elif event.type == SLIDESHOW_EVENT and slideshow_active:
            if photos:
                selected_photo_idx = (selected_photo_idx + 1) % len(photos)
                
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            
            if selected_photo_idx is not None:
                if back_btn.collidepoint(pos):
                    selected_photo_idx = None
                    slideshow_active = False
                elif slideshow_btn.collidepoint(pos):
                    slideshow_active = not slideshow_active
            else:
# Проверка за клик върху миниатюра
                for rect, idx in thumb_rects:
                    if rect.collidepoint(pos):
                        selected_photo_idx = idx
                        slideshow_active = False
                        
                # Бутон за директно стартиране на слайдшоу
                start_all_btn = pygame.Rect(20, 430, 280, 35)
                if start_all_btn.collidepoint(pos) and photos:
                    selected_photo_idx = 0
                    slideshow_active = True
                    
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if selected_photo_idx is not None:
                    selected_photo_idx = None
                    slideshow_active = False
                else:
                    running = False

    draw_gallery()
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
