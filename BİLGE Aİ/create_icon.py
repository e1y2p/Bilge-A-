from PIL import Image, ImageDraw, ImageFont
import os

# İkon boyutları
sizes = [16, 32, 48, 64, 128, 256]
base_dir = os.path.dirname(os.path.abspath(__file__))

# .ico dosyası için farklı boyutlar
icon_images = []

for size in sizes:
    # Şeffaf arka plan
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Mavi gradyan arka plan (yuvarlak)
    margin = size // 10
    draw.ellipse([margin, margin, size-margin, size-margin], 
                 fill=(60, 120, 200, 255), outline=(100, 160, 240, 255), width=2)
    
    # B harfi
    try:
        font_size = int(size * 0.6)
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        font = ImageFont.load_default()
    
    # B harfi çizimi
    text = "B"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (size - text_width) // 2
    y = (size - text_height) // 2
    
    draw.text((x, y), text, font=font, fill=(255, 255, 255, 255))
    
    # .ico için listeye ekle
    icon_images.append(img)
    
    # PNG olarak da kaydet
    img.save(os.path.join(base_dir, "Icon", f"bilge_{size}x{size}.png"))

# .ico dosyası oluştur (çok boyutlu)
icon_path = os.path.join(base_dir, "Icon", "bilge.ico")
icon_images[0].save(icon_path, format="ICO", sizes=[(img.width, img.height) for img in icon_images])

print("İkonlar oluşturuldu!")
print(f".ico dosyası: {icon_path}")
