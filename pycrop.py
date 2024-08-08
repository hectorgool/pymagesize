# import os
# import sys
# from PIL import Image
# from datetime import datetime

# def crop_image(image_path, crop_size):
#     img = Image.open(image_path)
#     width, height = img.size

#     if width < crop_size or height < crop_size:
#         print(f"\nAdvertencia: La imagen '{image_path}' mide menos de {crop_size}x{crop_size} píxeles y no se recortará.")
#         return None

#     left = (width - crop_size) / 2
#     top = (height - crop_size) / 2
#     right = (width + crop_size) / 2
#     bottom = (height + crop_size) / 2

#     img_cropped = img.crop((left, top, right, bottom))
#     return img_cropped

# def process_image(image_path, crop_size, output_dir):
#     img_cropped = crop_image(image_path, crop_size)
#     if img_cropped is None:
#         return  # Skip saving if the image was not cropped
    
#     base_name = os.path.basename(image_path)
#     name, ext = os.path.splitext(base_name)
#     new_name = f"{name}_crop_{crop_size}x{crop_size}{ext}"
#     output_path = os.path.join(output_dir, new_name)
#     img_cropped.save(output_path)
#     print(f"Imagen guardada: {output_path}")

# def process_directory(directory, crop_size, output_dir):
#     for filename in os.listdir(directory):
#         if filename.endswith('.png'):
#             process_image(os.path.join(directory, filename), crop_size, output_dir)

# def main():
#     if len(sys.argv) < 2:
#         print(f"\nUso: python {sys.argv[0]} <imagen|directorio> [tamaño_crop]")
#         sys.exit(1)

#     path = sys.argv[1]
#     crop_size = int(sys.argv[2]) if len(sys.argv) > 2 else 2000

#     if not os.path.exists(path):
#         print(f"Error: {path} no existe.")
#         sys.exit(1)

#     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#     output_dir = f"images_{timestamp}"
#     os.makedirs(output_dir, exist_ok=True)

#     if os.path.isfile(path):
#         process_image(path, crop_size, output_dir)
#     elif os.path.isdir(path):
#         process_directory(path, crop_size, output_dir)
#     else:
#         print(f"Error: {path} no es un archivo ni un directorio válido.")
#         sys.exit(1)

# if __name__ == "__main__":
#     main()

import os
import sys
import datetime
from PIL import Image
import zipfile

def process_image(image_path, my_image_width):
    with Image.open(image_path) as img:
        # Calcular el recorte centrado
        width, height = img.size
        min_dim = min(width, height)
        crop_dim = min(min_dim, my_image_width)
        
        left = (width - crop_dim) // 2
        top = (height - crop_dim) // 2
        right = (width + crop_dim) // 2
        bottom = (height + crop_dim) // 2
        
        img_cropped = img.crop((left, top, right, bottom))
        img_cropped = img_cropped.resize((my_image_width, my_image_width), Image.LANCZOS)
        
        # Generar nombre para la imagen recortada
        base_name, ext = os.path.splitext(os.path.basename(image_path))
        new_name = f"{base_name}_crop_{my_image_width}.png"
        
        return img_cropped, new_name

def save_image(img, new_name, output_dir):
    output_path = os.path.join(output_dir, new_name)
    img.save(output_path)

def process_directory(directory_path, my_image_width, output_dir):
    for filename in os.listdir(directory_path):
        if filename.lower().endswith('.png'):
            image_path = os.path.join(directory_path, filename)
            img_cropped, new_name = process_image(image_path, my_image_width)
            save_image(img_cropped, new_name, output_dir)

def create_zip_file(output_dir):
    zip_filename = f"{output_dir}.zip"
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(output_dir):
            for file in files:
                zipf.write(os.path.join(root, file), 
                           os.path.relpath(os.path.join(root, file), 
                           os.path.join(output_dir, '..')))

def main():
    if len(sys.argv) < 3:
        print("Uso: python script.py <ruta_imagen_o_directorio> <my_image_width> [z]")
        sys.exit(1)
    
    path = sys.argv[1]
    my_image_width = int(sys.argv[2])
    
    # Crear nombre para el directorio de salida
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    output_dir = f"images_{timestamp}"
    os.makedirs(output_dir, exist_ok=True)
    
    # Procesar imagen o directorio
    if os.path.isfile(path):
        img_cropped, new_name = process_image(path, my_image_width)
        save_image(img_cropped, new_name, output_dir)
    elif os.path.isdir(path):
        process_directory(path, my_image_width, output_dir)
    else:
        print(f"{path} no es un archivo o directorio válido.")
        sys.exit(1)
    
    # Crear archivo ZIP si se proporciona el argumento 'z'
    if len(sys.argv) == 4 and sys.argv[3] == 'z':
        create_zip_file(output_dir)

if __name__ == "__main__":
    main()
