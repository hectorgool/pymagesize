A continuación, te proporciono un script en Python que cumple con los requisitos especificados. El script utiliza las bibliotecas `PIL` (Pillow) para manejar la manipulación de imágenes y `os` y `sys` para manejar los argumentos de la línea de comandos y operaciones con archivos.

```python
import os
import sys
from PIL import Image
from datetime import datetime

def crop_image(image_path, crop_size):
    img = Image.open(image_path)
    width, height = img.size

    left = (width - crop_size) / 2
    top = (height - crop_size) / 2
    right = (width + crop_size) / 2
    bottom = (height + crop_size) / 2

    img_cropped = img.crop((left, top, right, bottom))
    return img_cropped

def process_image(image_path, crop_size, output_dir):
    img_cropped = crop_image(image_path, crop_size)
    base_name = os.path.basename(image_path)
    name, ext = os.path.splitext(base_name)
    new_name = f"{name}_crop_{crop_size}x{crop_size}{ext}"
    output_path = os.path.join(output_dir, new_name)
    img_cropped.save(output_path)
    print(f"Imagen guardada: {output_path}")

def process_directory(directory, crop_size, output_dir):
    for filename in os.listdir(directory):
        if filename.endswith('.png'):
            process_image(os.path.join(directory, filename), crop_size, output_dir)

def main():
    if len(sys.argv) < 2:
        print("Uso: python script.py <imagen|directorio> [tamaño_crop]")
        sys.exit(1)

    path = sys.argv[1]
    crop_size = int(sys.argv[2]) if len(sys.argv) > 2 else 2000

    if not os.path.exists(path):
        print(f"Error: {path} no existe.")
        sys.exit(1)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = f"images_{timestamp}"
    os.makedirs(output_dir, exist_ok=True)

    if os.path.isfile(path):
        process_image(path, crop_size, output_dir)
    elif os.path.isdir(path):
        process_directory(path, crop_size, output_dir)
    else:
        print(f"Error: {path} no es un archivo ni un directorio válido.")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

### ¿Cómo usar el script?

1. **Guardar el script** en un archivo llamado `crop_images.py`.

2. **Ejecutar el script** desde la línea de comandos. Aquí algunos ejemplos:

   - Para procesar una sola imagen con el tamaño por defecto de 2000x2000 píxeles:
     ```bash
     python crop_images.py mi_imagen.png
     ```

   - Para procesar una sola imagen y especificar un tamaño de crop personalizado, por ejemplo, 1500x1500 píxeles:
     ```bash
     python crop_images.py mi_imagen.png 1500
     ```

   - Para procesar todas las imágenes `.png` dentro de un directorio, con el tamaño de crop por defecto:
     ```bash
     python crop_images.py mi_directorio
     ```

   - Para procesar todas las imágenes `.png` dentro de un directorio con un tamaño de crop personalizado:
     ```bash
     python crop_images.py mi_directorio 1500
     ```

3. **Resultado**: Las imágenes recortadas se guardarán en un nuevo directorio llamado `images_YYYYMMDD_HHMMSS` en la misma ubicación donde se ejecuta el script.




La línea `if __name__ == "__main__":` es una construcción común en Python que se utiliza para determinar si un script se está ejecutando directamente o si está siendo importado como un módulo en otro script. Vamos a desglosarlo:

### Desglose

- **`__name__`:**  
  En Python, `__name__` es una variable especial que se establece dependiendo de cómo se ejecute el archivo Python.

  - Si el archivo se ejecuta directamente como un script (por ejemplo, ejecutando `python script.py` desde la línea de comandos), entonces `__name__` se establece como `"__main__"`.
  - Si el archivo se importa como un módulo en otro script (por ejemplo, `import script`), entonces `__name__` toma el nombre del archivo (sin la extensión `.py`).

- **`if __name__ == "__main__":`:**  
  Esta línea verifica si `__name__` es igual a `"__main__"`, lo que significa que el script se está ejecutando directamente. Si es así, se ejecuta el bloque de código dentro de este `if`.

- **`main()`:**  
  Esta línea simplemente llama a la función `main()`, que normalmente contiene la lógica principal del programa.

### Ejemplo
Considera el siguiente script `script.py`:

```python
def main():
    print("El script se está ejecutando directamente.")

def funcion_adicional():
    print("Esta es una función adicional.")

if __name__ == "__main__":
    main()
```

- **Si ejecutas este script directamente:**

  ```bash
  python script.py
  ```

  El resultado será:
  ```
  El script se está ejecutando directamente.
  ```

- **Si importas este script en otro archivo:**

  ```python
  import script

  script.funcion_adicional()
  ```

  El resultado será:
  ```
  Esta es una función adicional.
  ```

En este caso, `main()` no se ejecutará automáticamente porque `__name__` no será `"__main__"`, sino `"script"`.

### ¿Por qué se usa?
Esta estructura permite que el código sea reutilizable. Si alguien importa el script como un módulo en otro programa, no se ejecutará el código dentro del bloque `if __name__ == "__main__":`, a menos que lo llamen explícitamente. Esto es útil para organizar el código y para separar la funcionalidad principal del script de las funciones que pueden ser reutilizadas en otros contextos.