import os, shutil
from textnode import TextNode, TextType
from copystatic import move_files
from generate_site import generate_pages_recursive

public_dir = "./public"
static_dir = "./static"
content_dir = "./content"
template_path = "./template.html"



def main():
    print("Deleting public directory...")
    if os.path.exists(public_dir):
        shutil.rmtree(public_dir)
    
    print("Copying static files to public directory...")
    move_files(static_dir, public_dir)

    generate_pages_recursive(content_dir, template_path, public_dir)

main()