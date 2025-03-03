import os, shutil, sys
from textnode import TextNode, TextType
from copystatic import move_files
from generate_site import generate_pages_recursive

public_dir = "./docs"
static_dir = "./static"
content_dir = "./content"
template_path = "./template.html"


def main():
    try:
        basepath = sys.argv[1]
    except:
        basepath = "/"
    print("Deleting public directory...")
    if os.path.exists(public_dir):
        shutil.rmtree(public_dir)
    
    print("Copying static files to public directory...")
    move_files(static_dir, public_dir)

    generate_pages_recursive(content_dir, template_path, public_dir, basepath)

main()