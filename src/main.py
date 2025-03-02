import os, shutil
from textnode import TextNode, TextType
from copystatic import move_files

public_dir = "./public"
static_dir = "./static"

def main():
    print("Deleting public directory...")
    if os.path.exists(public_dir):
        shutil.rmtree(public_dir)
    
    print("Copying static files to public directory...")
    move_files(static_dir, public_dir)

main()