import pygame
import sys
import os

# Инициализация
pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 320, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tizen Bixby Assistant")

# Цветове
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 113, 206)      # Samsung / Bixby Blue
GRAY = (50, 50, 50)
LIGHT_GRAY = (90, 90, 90)
GREEN = (0, 200, 100)

font = pygame.font.SysFont("Arial", 16, bold=True)
font_small = pygame.font.SysFont("Arial", 14)

bixby_status = "Hi, how can I help you today?"

# Бутони за трите специфични командни фрази
cmd_btn_1 = pygame.Rect(20, 160, 280, 45) # Turn on color filter
cmd_btn_2 = pygame.Rect(20, 220, 280, 45) # I'm bored
cmd_btn_3 = pygame.Rect(20, 280, 280, 45) # Read today's schedule
mic_btn = pygame.Rect(110, 360, 100, 50)  # Гласов микрофон бутон

def speak(text):
    global bixby_status
    bixby_status = text
    print(f"[Bixby Voice]: {text}")
    # Използваме espeak за реален гласов изход
    try:
        os.system(f'espeak "{text}" &')
    except Exception as e:
        print(f"Грешка при гласово озвучаване: {e}")

def draw_bixby():
    screen.fill(BLACK)
    
    # Заглавие
    title = font.render("Bixby Assistant", True, BLUE)
    screen.blit(title, (90, 25))
    
    # Диалогов прозорец с отговора на Bixby
    pygame.draw.rect(screen, GRAY, (20, 65, 280, 75), border_radius=10)
    b_text = font_small.render(bixby_status, True, WHITE)
    screen.blit(b_text, (30, 85))
    
    # Бутон 1: Turn on color filter
    pygame.draw.rect(screen, GRAY, cmd_btn_1, border_radius=8)
    screen.blit(font_small.render("Turn on color filter", True, WHITE), (cmd_btn_1.x + 20, cmd_btn_1.y + 14))
    
    # Бутон 2: I'm bored
    pygame.draw.rect(screen, GRAY, cmd_btn_2, border_radius=8)
    screen.blit(font_small.render("I'm bored", True, WHITE), (cmd_btn_2.x + 20, cmd_btn_2.y + 14))
    
    # Бутон 3: Read today's schedule
    pygame.draw.rect(screen, GRAY, cmd_btn_3, border_radius=8)
    screen.blit(font_small.render("Read today's schedule", True, WHITE), (cmd_btn_3.x + 20, cmd_btn_3.y + 14))
    
    # Интерактивен бутон за микрофон
    pygame.draw.rect(screen, BLUE, mic_btn, border_radius=25)
    screen.blit(font.render("🎤 Speak", True, WHITE), (mic_btn.x + 18, mic_btn.y + 15))

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            
            if cmd_btn_1.collidepoint(pos):
                speak("Turning on color filter mode.")
                # Тук в бъдеще ще се върже системната функция за филтър на екрана
            elif cmd_btn_2.collidepoint(pos):
                speak("You are bored? Let's play a retro Mario ringtone or open a game.")
            elif cmd_btn_3.collidepoint(pos):
                speak("Today's schedule: Coding Tizen OS and testing apps at 4 PM.")
            elif mic_btn.collidepoint(pos):
                speak("Listening for your voice command...")
                
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    draw_bixby()
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
