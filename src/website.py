import os
import shutil
import re
from markdown_to_html import markdown_to_html_node


def static_to_public(static_directory, public_directory):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # src/
    PROJECT_ROOT = os.path.dirname(BASE_DIR)               # project root
    public_path = os.path.join(PROJECT_ROOT, public_directory)
    static_path = os.path.join(PROJECT_ROOT, static_directory)
    if os.path.isdir(public_path):
        print("public path exist")
        shutil.rmtree(public_path)
        os.mkdir(public_path)
        directories = os.listdir(static_path)
        for i in directories:
            if os.path.isfile(f"{static_path}/{i}"):
                shutil.copy(f"{static_path}/{i}", public_path)
            else:
                new_public = os.path.join(f"{public_path}/{i}")
                new_static = os.path.join(f"{static_path}/{i}")
                os.mkdir(new_public)
                static_to_public(new_static, new_public)
    else:
        print("public path doesn't exist")

def extract_title(markdown):
    match = re.search(r'^#(?!#)\s+(.+)$', markdown, re.MULTILINE)
    if match:
        title = match.group(1)
        return title
    else:
        raise Exception("No title")
    

def generate_page(from_path, template_path, dest_path):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # src/
    PROJECT_ROOT = os.path.dirname(BASE_DIR)               # project root
    from_path_abs = os.path.join(PROJECT_ROOT, from_path)
    template_path_abs = os.path.join(PROJECT_ROOT, template_path)
    dest_path_abs = os.path.join(PROJECT_ROOT, dest_path)


    print("Generating page from from_path to dest_path using template_path")
    with open(from_path_abs, encoding="utf-8") as f:
        read_markdown = f.read()
    with open(template_path_abs, encoding="utf-8") as f:
        read_template = f.read()
    html_node = markdown_to_html_node(read_markdown)
    html_file = html_node.to_html()
    title = extract_title(read_markdown)
    read_template.replace("{{ Title }}", title)
    read_template.replace("{{ Content }}", html_file)
    

    if os.path.isdir(dest_path_abs):
        with open("demofile.txt", "w") as f:
            f.write(read_template)
    
    else:
        os.makedirs(dest_path_abs)
        with open("demofile.txt", "w") as f:
            f.write(read_template)


    


                


