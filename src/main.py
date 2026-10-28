import os
import shutil
import sys

from copystatic import copy_directory_recursive
from page import generate_pages_recursive

dir_path_static = "./static"
dir_path_docs = "./docs"

def main():
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    print(f"Building site to {dir_path_docs} with basepath: {basepath}")
    print("Deleting docs directory")

    if os.path.exists(dir_path_docs):
        shutil.rmtree(dir_path_docs)

    print("Copying static files to docs directory...")
    copy_directory_recursive(dir_path_static, dir_path_docs)
    generate_pages_recursive("content", "template.html", dir_path_docs, basepath)

if __name__ == "__main__":
    main()
