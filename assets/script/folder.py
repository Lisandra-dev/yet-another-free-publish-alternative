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
    print(f'🎉 All files are updated and created ! You can now use {folder} !')
main(sys.argv[1])
