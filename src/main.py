import os
import shutil
import sys

from htmlnode import extract_title, markdown_to_html_node
from pathlib import Path

def main():
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    print(f"basepath: {basepath}")

    src_dir = "static"
    tgt_dir = "docs"
    if os.path.exists(tgt_dir):
        shutil.rmtree(tgt_dir)
    copy_dir(src_dir, tgt_dir)

    generate_pages_recursive(basepath, "content", "template.html", tgt_dir)

def generate_pages_recursive(basepath, dir_path_content, template_path, dest_dir_path):
    for f in os.listdir(dir_path_content):
        p = os.path.join(dir_path_content, f)
        if os.path.isfile(p):
            df = os.path.splitext(f)[0] + ".html"
            generate_page(basepath, p, template_path, os.path.join(dest_dir_path, df))
        else:
            generate_pages_recursive(basepath, p, template_path, os.path.join(dest_dir_path, f))

def generate_page(basepath, from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    contents_string = ""
    with open(from_path, mode='r') as file:
        contents_string = file.read().strip()

    template_html = ""
    with open(template_path, mode='r') as file:
        template_html = file.read().strip()

    contents_html = markdown_to_html_node(contents_string).to_html()
    title = extract_title(contents_string)

    html = template_html.replace("{{ Title }}", title).replace("{{ Content }}", contents_html)
    html = html.replace('href="/', f"href=\"{basepath}").replace('src="/', f"src=\"{basepath}")
    Path(os.path.dirname(dest_path)).mkdir(parents=True, exist_ok=True)
    with open(dest_path, 'w') as file:
        file.write(html)


def copy_dir(src_dir, tgt_dir):
    print(f"copying contents of dir: {src_dir} -> {tgt_dir}")
    if not os.path.exists(tgt_dir):
        os.mkdir(tgt_dir)

    fs = os.listdir(src_dir)
    for f in fs:
        sf = os.path.join(src_dir, f)
        tf = os.path.join(tgt_dir, f)
        if os.path.isfile(sf):
            print(f"copying file: {sf} -> {tf}")
            shutil.copy(sf, tf)
        else:
            copy_dir(sf, tf)

main()
