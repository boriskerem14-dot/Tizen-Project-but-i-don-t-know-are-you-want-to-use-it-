from PIL import Image, ImageDraw

def generate_boot_logo():
    # Резолюция на екран на iPhone 2G (320x480 пиксела)
    width, height = 320, 480
    
    # Създаване на черен фон (стандартният цвят при зареждане на iOS)
    img = Image.new("RGB", (width, height), color=(0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Рисуване на стилизирано силуетно лого в центъра (напр. Apple форма или маркер)
    apple_body = [130, 200, 190, 270]
    draw.ellipse(apple_body, fill=(200, 200, 200))
    
    # Записване като PNG за предварителен преглед
    img.save("apple_boot_logo.png")
    
    # Конвертиране в суров файлов формат (RAW / RGB565), използван от iBoot
    raw_file = "apple_boot_logo.raw"
    with open(raw_file, "wb") as f:
        for y in range(height):
            for x in range(width):
                r, g, b = img.getpixel((x, y))
                # Преобразуване от 24-bit RGB към 16-bit RGB565
                rgb565 = ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)
                f.write(rgb565.to_bytes(2, byteorder='little'))
                
    print(f"[Успех] Логото е генерирано като {raw_file} и apple_boot_logo.png!")

if __name__ == "__main__":
    generate_boot_logo()
