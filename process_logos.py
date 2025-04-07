from PIL import Image, ImageOps
import os

# settings
input_folder = "input_logos"
output_folder = "output_logos"
target_size = 800
padding_percent = 0.1

# Per-logo settings 
# boost = scale adjustment (1.0 = normal)
# offset = vertical shift in pixels (positive = move down, negative = move up)
logo_settings = {
    "usm":      {"boost": 1.0, "offset": 0},
    "teknion":  {"boost": 1.9, "offset": -20},
    "falk":     {"boost": 1.5, "offset": 40},
    "global": {"boost": 0.85, "offset": 0},
    "humanscale": {"boost": 1.0, "offset": -30},
    "kimball": {"boost": 1.1, "offset": 0},
}

os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(input_folder):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        name, _ = os.path.splitext(filename)
        settings = logo_settings.get(name.lower(), {"boost": 1.0, "offset": 0})
        boost = settings["boost"]
        offset = settings["offset"]

        image_path = os.path.join(input_folder, filename)
        img = Image.open(image_path).convert("RGBA")

        #1: Auto-crop transparent pixels only
        bbox = img.getbbox()
        if bbox:
            img = img.crop(bbox)

        # 2: Convert to grayscale
        img_gray = ImageOps.grayscale(img)

        #3: Convert to black logo
        img_black = img_gray.point(lambda x: 0 if x < 240 else 255, mode='L')

        #4: Place on white background 
        bg = Image.new("L", img_black.size, 255)
        alpha = img.getchannel('A') if img.mode in ('RGBA', 'LA') else None
        if alpha:
            bg.paste(img_black, mask=alpha)
        else:
            bg.paste(img_black)

        bg = bg.convert("RGB")

        # 5: Proportional resize with boost
        w, h = bg.size
        max_logo_size = int(target_size * (1 - padding_percent) * boost)

        if w > h:
            new_w = max_logo_size
            new_h = int(h * (max_logo_size / w))
        else:
            new_h = max_logo_size
            new_w = int(w * (max_logo_size / h))

        resized_logo = bg.resize((new_w, new_h), Image.LANCZOS)

        #6: Center + Vertical Offset
        square_bg = Image.new("RGB", (target_size, target_size), "white")
        x_offset = (target_size - new_w) // 2
        y_offset = ((target_size - new_h) // 2) + offset
        square_bg.paste(resized_logo, (x_offset, y_offset))

        # Save 
        output_path = os.path.join(output_folder, f"{name}.png")
        square_bg.save(output_path)
        print(f"Saved: {output_path} with boost={boost} and offset={offset}")

print("Logos processed with individual boost & vertical offset!")
