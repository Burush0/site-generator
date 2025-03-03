import os, shutil
from textnode import TextNode, TextType
from copystatic import move_files
from generate_site import generate_page

public_dir = "./public"
static_dir = "./static"

src_path = "./content/index.md"
template_path = "./template.html"
dest_path = "./public/index.html"

def main():
    print("Deleting public directory...")
    if os.path.exists(public_dir):
        shutil.rmtree(public_dir)
    
    print("Copying static files to public directory...")
    move_files(static_dir, public_dir)

    generate_page(src_path, template_path, dest_path)

main()