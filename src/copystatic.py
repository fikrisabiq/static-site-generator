import shutil
import os

def copy_directory_recursive(source_path, dest_path):
    if not os.path.exists(dest_path):
        os.mkdir(dest_path)

    for item in os.listdir(source_path):
        from_item = os.path.join(source_path, item)
        to_item = os.path.join(dest_path, item)

        if os.path.isfile(from_item):
            print(f"Copying file: {from_item} -> {to_item}")
            shutil.copy(from_item, to_item)
        elif os.path.isdir(from_item):
            print(f"Creating directory: {to_item}")
            copy_directory_recursive(from_item, to_item)
