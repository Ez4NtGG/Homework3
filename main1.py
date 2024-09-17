import os
import shutil
from concurrent.futures import ThreadPoolExecutor
import sys

def copy_file(src_file, dest_dir):
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    shutil.copy2(src_file, dest_dir)

def process_directory(src_dir, dest_dir):
    for entry in os.listdir(src_dir):
        path = os.path.join(src_dir, entry)
        if os.path.isdir(path):
            # Рекурсивний виклик для обробки підкаталогів
            process_directory(path, dest_dir)
        else:
            # Отримуємо розширення файлу
            file_extension = os.path.splitext(entry)[1][1:]  # усуваємо крапку
            if file_extension:  # Якщо є розширення
                dest_sub_dir = os.path.join(dest_dir, file_extension)
                with ThreadPoolExecutor() as executor:
                    executor.submit(copy_file, path, dest_sub_dir)

def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py <source_directory> [destination_directory]")
        return

    source_directory = sys.argv[1]
    destination_directory = sys.argv[2] if len(sys.argv) > 2 else "dist"

    process_directory(source_directory, destination_directory)

if __name__ == "__main__":
    main()