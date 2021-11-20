# This script will help you to create a new folder ("category") for your blog.
# First in need to import the config yaml

import argparse
import os
import sys
from pathlib import Path

import yaml

basedir = Path(__file__).parent.parent.parent
file = basedir / "_config.yml"
file = file.resolve()


def update_config(folder):
    with open(file, "r", encoding="utf-8") as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            exit()
    collections_add = {folder: {"output": True, "permalink": f"/{folder}/:title"}}
    scope_add = [
        {
            "scope": {
                "path": "",
                "type": f"{folder}",
            },
            "values": {"layout": "post", "content-type": "notes"},
        }
    ]
    config["defaults"] = config["defaults"] + scope_add
    config["collections"].update(collections_add)
    with open(file, "w", encoding="utf-8") as stream:
        try:
            yaml.dump(config, stream, sort_keys=False, allow_unicode=True)
        except yaml.YAMLError as exc:
            print(exc)
            exit()


def create_page(folder):
    page = basedir / "private.md"
    target = basedir / f"{folder}.md"

    with open(page, "r", encoding="utf-8") as doc:
        content = "".join(doc.readlines())

    content = content.replace("private", folder)
    content = content.replace("Private", folder)

    with open(target, "w", encoding="utf-8") as doc:
        doc.write(content)

    try:
        os.mkdir(basedir / f"_{folder}")
        with open(basedir/'404.md', 'r') as f: #prevent search crash
            f.write('---\nlayout: post\npermalink: /404.html\ncategory: false\nflux: false\n---\n**Page not found :(**\n')
    except FileExistsError:
        print("The folder already exists")
        pass

def update_search(folder):
    file = basedir / 'search.json'
    content = f'}},\n  {{% endfor %}}\n    {{% for note in site.{folder}}} %\n    {{\n\n      "title"    : "{{{{note.title | strip_html | escape}}}} }}",\n      "url"      : "{{{{note.url}}}}",\n      "content"  : {{{{note.content | newline_to_br | strip_newlines | replace: \'<br/>\', \'\' | strip | strip_html | strip | jsonify }}}}\n\n    }}\n\t{{% unless forloop.last %}},{{% endunless %}}\n  {{% endfor %}}\n  \n]'
    f = open(file, "r", encoding="utf-8")
    data = f.readlines()
    f.close()
    data = ''.join(data)
    data = data.replace('}\n\t{% unless forloop.last %},{% endunless %}\n  {% '
                    'endfor %}\n  \n]', content)
    f = open(file, "w", encoding="utf-8")
    f.write(data)

def update_content(folder):
    contents = basedir / '_includes' / 'content.html'
    f = open(contents, 'r', encoding='utf-8')
    result_folder = '{%-' + f"assign result_{folder} = site.Roleplay | where: 'title',internal_link" + '-%}'
    data = f.readlines()
    f.close()
    for i in range(0, len(data)):
        if "{%- assign result_pages = site.pages | where: 'title',internal_link -%}" in data[i]:
            add_list_index = i
        elif 'internal_urls = internal_urls' in data[i]:
            assign_folder = data[i].strip() + f'|append: result_{folder}[0].url |'
            add_assign_first = i
        elif 'assign internal_urls_alt' in data[i]:
            assign_alt_folder = data[i].strip() + f'|append: result_{folder}[0].url |'
            add_assign_alt = i
    data[add_assign_alt] = assign_alt_folder
    data[add_assign_first] = assign_folder
    data.insert(add_list_index, result_folder)
    data = ''.join(data)
    f = open(contents, 'w', encoding='utf-8')
    f.write(data)
    f.close()


def main(folder):
    parser = argparse.ArgumentParser(
        description="Create all file needed for using a new collection (or folder) in the blog."
    )
    parser.add_argument("Name", help="The folder name")
    args = parser.parse_args()
    update_config(folder)
    print("The config file has been updated with the new folder")
    print(f"Creating the main page {folder}.md and folder with hidden file for push.")
    create_page(folder)
    update_search(folder)
    print(f"The search module is now updated with {folder}.")
    update_content(folder)
    print(f'Internal links are now parsed with the content of {folder}')
    print(f'🎉 All files are updated and created ! You can now use {folder} !')
main(sys.argv[1])
