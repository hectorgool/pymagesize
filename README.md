Aquí tienes una versión actualizada del script que incluye un argumento opcional `-z`. Si este argumento se proporciona, el script comprimirá el directorio de salida en un archivo `.zip`.

```python
import os
import sys
import shutil
from datetime import datetime
from PIL import Image

def get_timestamped_directory():
    # Obtiene la fecha y hora actual
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # Crea un nombre de directorio basado en la fecha y hora
    return f"images_{timestamp}"

def resize_image(image_path, my_image_width, output_directory):
    # Abre la imagen
    img = Image.open(image_path)
    
    # Calcula la altura manteniendo la proporción
    aspect_ratio = img.height / img.width
    my_image_heigth = int(my_image_width * aspect_ratio)
    
    # Redimensiona la imagen
    resized_img = img.resize((my_image_width, my_image_heigth), Image.ANTIALIAS)
    
    # Crea el nuevo nombre del archivo
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    new_image_name = f"{base_name}_{my_image_width}x{my_image_heigth}.png"
    new_image_path = os.path.join(output_directory, new_image_name)
    
    # Guarda la nueva imagen en el directorio de salida
    resized_img.save(new_image_path)
    print(f"Imagen guardada como: {new_image_path}")

def process_directory(directory_path, my_image_width, output_directory):
    # Recorre todos los archivos en el directorio
    for filename in os.listdir(directory_path):
        if filename.endswith(".png"):
            file_path = os.path.join(directory_path, filename)
            resize_image(file_path, my_image_width, output_directory)

def compress_directory(directory_path):
    zip_filename = f"{directory_path}.zip"
    shutil.make_archive(directory_path, 'zip', directory_path)
    print(f"Directorio comprimido en: {zip_filename}")

if __name__ == "__main__":
    # Verifica que se hayan pasado los argumentos correctos
    if len(sys.argv) < 3:
        print("Uso: python script.py <nombre_imagen_o_directorio> <ancho_en_pixeles> [-z]")
        sys.exit(1)
    
    path = sys.argv[1]
    my_image_width = int(sys.argv[2])
    compress = '-z' in sys.argv
    
    # Crea el directorio de salida con el timestamp
    output_directory = get_timestamped_directory()
    os.makedirs(output_directory, exist_ok=True)
    
    if os.path.isfile(path):
        # Si el primer argumento es un archivo, procesa solo esa imagen
        resize_image(path, my_image_width, output_directory)
    elif os.path.isdir(path):
        # Si el primer argumento es un directorio, procesa todas las imágenes PNG en el directorio
        process_directory(path, my_image_width, output_directory)
    else:
        print("El primer argumento debe ser un archivo PNG o un directorio.")
        sys.exit(1)
    
    # Si el argumento -z está presente, comprime el directorio de salida
    if compress:
        compress_directory(output_directory)
```

### Explicación de la Actualización:

1. **Argumento `-z`**:
   - El script ahora verifica si el argumento `-z` está presente en los argumentos de la línea de comandos.
   - Si está presente, el directorio de salida será comprimido en un archivo `.zip` utilizando la función `compress_directory`.

2. **Función `compress_directory(directory_path)`**:
   - Utiliza `shutil.make_archive` para comprimir el directorio de salida en un archivo `.zip`.

3. **Instrucciones de Uso**:
   - Para redimensionar imágenes sin comprimir el directorio:
     ```bash
     python resize_images.py mi_imagen.png 800
     ```
   - Para redimensionar imágenes y comprimir el directorio de salida:
     ```bash
     python resize_images.py mi_imagen.png 800 -z
     ```

El directorio de salida será comprimido en un archivo `.zip` con el mismo nombre del directorio, pero con la extensión `.zip`, y se guardará en la misma ubicación.