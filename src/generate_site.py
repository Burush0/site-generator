import os

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


def generate_page(from_path, template_path, dest_path):
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

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as file:
        file.write(template)
    file.close()
    #with open(from_path) as f:
    #    src_content = f
    #print(src_content)

md = """
# Hello world

Some more markdown because why not
He he

And some more

## and another heading2
"""

extract_title(md)