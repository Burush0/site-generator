import os
from pathlib import Path
from markdown_html import markdown_to_html_node

md_path = "../content/index.md"

def extract_title(markdown):
    lines = markdown.split("\n")
    result = ""
    for idx, line in enumerate(lines):
        if line == "":
            continue
        if line.startswith("# "):
            result = lines[idx]
            result = result.strip("#")
            result = result.strip()
            break
    if result == "":
        raise Exception("No h1 header")
    return result


def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as file:
        markdown = file.read()
    file.close()
    
    with open(template_path, "r") as file:
        template = file.read()
    file.close()
    
    content = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", content)

    template = template.replace('href="/', f'href="{basepath}')
    template = template.replace('src="/', f'src="{basepath}')

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as file:
        file.write(template)
    file.close()

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for file in os.listdir(dir_path_content):
        src_filepath = os.path.join(dir_path_content, file)
        dest_filepath = os.path.join(dest_dir_path, file)
        if os.path.isfile(src_filepath):
            dest_filepath = Path(dest_filepath).with_suffix(".html")
            generate_page(src_filepath, template_path, dest_filepath, basepath)
        else:
            generate_pages_recursive(src_filepath, template_path, dest_filepath, basepath)
