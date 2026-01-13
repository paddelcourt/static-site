import os
import shutil
import re
from markdown_to_html import markdown_to_html_node


def static_to_public(static_directory, public_directory):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))  
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
    read_template = read_template.replace("{{ Title }}", title)
    read_template = read_template.replace("{{ Content }}", html_file)

    dest_dir = os.path.dirname(dest_path_abs)
    if not os.path.isdir(dest_dir):
        os.makedirs(dest_dir)

    with open(dest_path_abs, "w") as f:
        f.write(read_template)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))  
    PROJECT_ROOT = os.path.dirname(BASE_DIR)               # project root
    dir_path_abs = os.path.join(PROJECT_ROOT, dir_path_content)
    template_path_abs = os.path.join(PROJECT_ROOT, template_path)
    dest_path_abs = os.path.join(PROJECT_ROOT, dest_dir_path)
    if os.path.isdir(dir_path_abs):
        dir_path_list = os.listdir(dir_path_abs)
        print("directory path exist")
        for i in dir_path_list:
            new_dir = os.path.join(f"{dir_path_abs}", f"{i}")
            if i.endswith(".md"):
                print(template_path_abs)
                file_name = os.path.splitext(i)[0]
                dest_html_file_path = os.path.join(f"{dest_path_abs}",f"{file_name}.html")
                return generate_page(new_dir, template_path_abs, dest_html_file_path)
            else:
                
                new_dest_path = os.path.join(f"{dest_path_abs}", f"{i}")
                print(new_dir)
                generate_pages_recursive(new_dir, template_path_abs, new_dest_path)
    else:
        print("directory path doesn't exist")





                


