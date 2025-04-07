from PIL import Image
import os

# input/output folders
input_folder = "output_logos"
output_folder = "output_webp_logos"

# create output folder if it doesnt exist
os.makedirs(output_folder, exist_ok=True)

# Loop through all image files in the input folder
for filename in os.listdir(input_folder):
    if filename.lower().endswith((".png", ".jpg", ".jpeg")):
        input_path = os.path.join(input_folder, filename)
        output_name = os.path.splitext(filename)[0] + ".webp"
        output_path = os.path.join(output_folder, output_name)

        # Open and convert to RGB 
        img = Image.open(input_path).convert("RGB")
        img.save(output_path, format="WEBP", quality=90)  #quality affects webp size

        print(f"Converted: {filename} → {output_name}")

print("All images converted to WebP format.")
