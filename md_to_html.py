import os
import sys
import re
import subprocess

def convert_md_to_html(md_file_path, html_dir):
    print("la terminacion es: " + md_file_path[-7:])
    if md_file_path[-7:] in ('.png.md', '.jpg.md', '.pdf.md'):
        subprocess.run([
            'cp',
            os.path.join("/home/jonetxe13/Desktop/obsidian/", os.path.basename(md_file_path[:-3])),
            os.path.join(html_dir, os.path.basename(md_file_path[:-3]))
        ])
        return
    if not os.path.isfile(md_file_path):
        return
    html_file_path = os.path.join(
        html_dir,
        os.path.splitext(os.path.basename(md_file_path))[0] + '.html'
    )
    with open(md_file_path, 'r') as file:
        content = file.read()
        print(md_file_path)
        print("el file path termina en .jpg.md ", md_file_path[-7:] == '.jpg.md')

        def replace_link(match):
            link_target = match.group(1)
            if link_target.endswith(('.jpg', '.png', '.gif')):
                return '<img src="{}" style="max-width:550px;">'.format(link_target)
            else:
                html_file = os.path.splitext(link_target)[0] + '.html'
                return '<a href="{}">{}</a>'.format(html_file, link_target)

        content = re.sub(r'\[\[(.*?)\]\]', replace_link, content)

    with open(md_file_path + ".tmp", 'w') as file:
        file.write(content)
    subprocess.run([
        'pandoc',
        '--template=simple.latex',
        md_file_path + ".tmp",
        '-o',
        html_file_path
    ])
    os.remove(md_file_path + ".tmp")

def process_directory(directory, html_dir):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".md"):
                md_file_path = os.path.join(root, file)
                with open(md_file_path, 'r') as file:
                    content = file.read()
                md_links = re.findall(r'\[\[(.*?)\]\]', content)
                md_file_paths = [os.path.join(os.path.dirname(md_file_path), link + '.md') for link in md_links]
                convert_md_to_html(md_file_path, html_dir)
                for linked_md_file_path in md_file_paths:
                    convert_md_to_html(linked_md_file_path, html_dir)

def process_file(md_file_path, html_dir):
    with open(md_file_path, 'r') as file:
        content = file.read()
    md_links = re.findall(r'\[\[(.*)\]\]', content)
    md_file_paths = [os.path.join("/home/jonetxe13/Desktop/obsidian/", link + '.md') for link in md_links]
    convert_md_to_html(md_file_path, html_dir)
    for linked_md_file_path in md_file_paths:
        # print(linked_md_file_path)
        convert_md_to_html(linked_md_file_path, html_dir)

def main():

    html_dir = os.path.expanduser('~/Desktop/html_dir/SO')
    if len(sys.argv) > 1:
        md_file_path = sys.argv[1]
        html_dir = os.path.join(html_dir, os.path.splitext(os.path.basename(md_file_path))[0])
        os.makedirs(html_dir, exist_ok=True)
        process_file(md_file_path, html_dir)
    else:
        process_directory("/home/jonetxe13/Desktop/obsidian/Universidad/Asignaturas/2/", html_dir)
        process_directory("/home/jonetxe13/Desktop/obsidian/", html_dir)

if __name__ == "__main__":
    main()

