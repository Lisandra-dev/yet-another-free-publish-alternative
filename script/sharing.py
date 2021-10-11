import re
import sys
import os
from dotenv import dotenv_values
from pathlib import Path
from pathlib import PurePath
import shutil
from datetime import datetime
import frontmatter
import yaml
import argparse
import glob

sys.stdin.reconfigure(encoding="utf-8")
sys.stdout.reconfigure(encoding="utf-8")

BASEDIR = os.path.abspath(os.path.dirname(__file__))
if "script" in BASEDIR:
    BASEDIR = PurePath(BASEDIR).parents[0]
env = dotenv_values(Path(f"{BASEDIR}/.env"))
path = Path(f"{BASEDIR}/.git")  # GIT SHARED
post = Path(f"{BASEDIR}/_notes")
img = Path(f"{BASEDIR}/assets/img/")

# Seems to have problem with dotenv with pyto on IOS 15
try:
    vault = Path(env["vault"])
    web = env["blog"]
except KeyError:
    with open(Path(f"{BASEDIR}/.env")) as f:
        vault = Path("".join(f.readlines(1)).replace("vault=", ""))
        web = "".join(f.readlines(2)).replace("blog=", "")


def check_folder(folder_key):
    path = f"{BASEDIR}/_{folder_key}"
    if os.path.isdir(path):
        return path
    else:
        return post


def retro(filepath, opt=0):
    notes = []
    if opt == 0:
        metadata = frontmatter.load(filepath)
    else:
        metadata = frontmatter.loads("".join(filepath))
    file = metadata.content.split("\n")
    for n in file:
        notes.append(n)
    return notes


def remove_frontmatter(meta):
    meta.pop("date", None)
    meta.pop("title", None)
    meta.pop("created", None)
    meta.pop("update", None)
    meta.pop("link", None)
    return meta


def diff_file(file, folder, update=0):
    file_name = os.path.basename(file)
    if check_file(file_name, folder) == "EXIST":
        if update == 1:  # Update : False / Don't check
            return False
        notes_path = Path(f"{folder}/{file_name}")
        retro_old = retro(notes_path)
        meta_old = frontmatter.load(notes_path)
        meta_old = remove_frontmatter(meta_old.metadata)

        temp = file_convert(file, folder)
        front_temp = frontmatter.loads("".join(temp))
        meta_new = remove_frontmatter(front_temp.metadata)
        new_version = retro(temp, 1)
        if new_version == retro_old and sorted(meta_old.keys()) == sorted(
            meta_new.keys()
        ):
            return False
        else:
            return True
    else:
        return True  # Si le fichier existe pas, il peut pas être identique


# PATH WORKING #
def delete_file(filepath, folder):
    path = Path(folder)
    for file in os.listdir(path):
        filepath = os.path.basename(filepath)
        filecheck = os.path.basename(file)
        if filecheck == filepath:
            os.remove(Path(f"{path}/{file}"))
            return True
    return False


def delete_not_exist():
    # for file in poste : if file not in vault : delete file
    vault_file = []
    important_folder=["_includes", "_layout", "_site", "assets", "script"]
    for filename in glob.iglob(f"{vault}**/**", recursive=True):
        vault_file.append(os.path.basename(filename))
    for file in glob.iglob(f"{BASEDIR}/_*/**"):
        if not any(folder in file for folder in important_folder) and os.path.basename(file) not in vault_file:
            os.remove(Path(file))


def check_file(filepath, folder):
    post_file = []
    folder = Path(folder)
    for file in glob.iglob(f"{folder}/**"):
        post_file.append(os.path.basename(file))
    if filepath in post_file:
        return "EXIST"
    else:
        return "NE"


def dest(filepath, folder):
    file_name = os.path.basename(filepath)
    dest = Path(f"{folder}/{file_name}")
    return str(dest)


def frontmatter_check(filename, folder):
    metadata = open(Path(f"{folder}/{filename}"), "r", encoding="utf-8")
    meta = frontmatter.load(metadata)
    update = frontmatter.dumps(meta)
    folder_key = folder.replace(f"{BASEDIR}/", "")
    metadata.close()
    final = open(Path(f"{folder}/{filename}"), "w", encoding="utf-8")
    now = datetime.now().strftime("%d-%m-%Y")
    if not "current" in meta.keys() or meta["current"] != False:
        meta["date"] = now
        update = frontmatter.dumps(meta)
        meta = frontmatter.loads(update)
    if not "title" in meta.keys():
        meta["title"] = filename.replace(".md", "")
        update = frontmatter.dumps(meta)
    if not "link" in meta.keys():
        filename = filename.replace(".md", "")
        filename = filename.replace(" ", "-")
        clip = f"{web}{folder_key}/{filename}"
        meta["link"] = clip
        update = frontmatter.dumps(meta)
    final.write(update)
    final.close()
    return


def update_frontmatter(file, folder, share=0):
    metadata = open(file, "r", encoding="utf8")
    meta = frontmatter.load(metadata)
    metadata.close()
    folder_key = folder.replace(f"{BASEDIR}/_", "")
    if "tag" in meta.keys():
        tag = meta["tag"]
    elif "tags" in meta.keys():
        tag = meta["tags"]
    else:
        tag = ""
    meta.metadata.pop("tag", None)
    meta.metadata.pop("tags", None)
    with open(file, "w", encoding="utf-8") as f:
        filename = os.path.basename(file)
        filename = filename.replace(".md", "")
        filename = filename.replace(" ", "-")
        clip = f"{web}{folder_key}/{filename}"
        meta["link"] = clip
        update = frontmatter.dumps(meta, sort_keys=False)
        meta = frontmatter.loads(update)
        if share == 1 and ("share" not in meta.keys() or meta["share"] == "false"):
            meta["share"] = "true"
            update = frontmatter.dumps(meta, sort_keys=False)
            meta = frontmatter.loads(update)
        if tag != "":
            meta["tag"] = tag
        update = frontmatter.dumps(meta, sort_keys=False)
        if re.search(r"\\U\w+", update):
            emojiz = re.search(r"\\U\w+", update)
            emojiz = emojiz.group().strip()
            convert_emojiz = (
                emojiz.encode("ascii")
                .decode("unicode-escape")
                .encode("utf-16", "surrogatepass")
                .decode("utf-16")
            )
            update = re.sub(r'"\\U\w+"', convert_emojiz, update)
        f.write(update)
    return


# ADMONITION CURSED THINGS
def admonition_logo(type, line):
    admonition = {
        "note": "🖊️",
        "seealso": "🖊️",
        "abstract": "📝",
        "summary": "📝",
        "tldr": "📝",
        "info": "ℹ️",
        "todo": "ℹ️",
        "tip": "🔥",
        "hint": "🔥",
        "important": "🔥",
        "success": "✨",
        "check": "✨",
        "done": "✨",
        "question": "❓",
        "help": "❓",
        "faq": "❓",
        "warning": "⚠️",
        "caution": "⚠️",
        "attention": "⚠️",
        "failure": "❌",
        "fail": "❌",
        "missing": "❌",
        "danger": "⚡",
        "error": "⚡",
        "bug": "🐛",
        "example": "📌",
        "exemple": "📌",
        "quote": "📋",
        "cite": "📋",
    }
    if type in admonition.keys():
        logo = admonition[type]
    else:
        logo = "[" + type.title() + "]"
    if line == "":
        title = "**" + logo + "**{: .title}"
    else:
        title = "**" + logo + " " + line + "**{: .title}\n"
    return title


def admonition_trad_content(line, type):

    title = line
    if "collapse:" in line:
        title = ""
    elif "icon:" in line:
        title = ""
    elif "color:" in line:
        title = ""
    elif len(line) == 1:
        title = "$~$  \n"
    elif "title:" in line:
        title = admonition_logo(type, line.replace("title:", "").strip())
    return title


def admonition_trad(file_data):
    code_index = 0
    code_dict = {}
    start_list = []
    end_list = []
    for i in range(0, len(file_data)):
        if re.search("[`?!]{3}( ?)ad-(.*)", file_data[i]):
            start = i
            start_list.append(start)
        elif re.match("```", file_data[i]) or re.match("--- admonition", file_data[i]):
            end = i
            end_list.append(end)
    for i, j in zip(start_list, end_list):
        code = {code_index: (i, j)}
        code_index = code_index + 1
        code_dict.update(code)
    for ad, ln in code_dict.items():
        ad_start = ln[0]
        ad_end = ln[1]
        type = re.search("[`!?]{3}( ?)ad-\w+", file_data[ad_start])
        type = re.sub("[`!?]{3}( ?)ad-", "", type.group())
        adm = "b"
        title = ""
        if re.search("[!?]{3} ad-(\w+) (.*)", file_data[ad_start]):
            title = re.search("[!?]{3} ad-(\w+) (.*)", file_data[ad_start])
            adm = "MT"
            title = title.group(2)
        first_block = re.search("ad-(\w+)", file_data[ad_start])
        first_block = "!!!" + first_block.group()
        file_data[ad_start] = re.sub(
            "[`!?]{3}( ?)ad-(.*)", first_block, file_data[ad_start]
        )
        file_data[ad_end] = "  "
        for i in range(ad_start, ad_end):
            file_data[i] = admonition_trad_content(file_data[i], type)
        if adm == "MT":
            if len(title) > 0:
                title_admo = admonition_logo(type, title)
                file_data.insert(ad_start + 1, title_admo)
            else:
                title_admo = admonition_logo(type, "")
                file_data.insert(ad_start + 1, title_admo)
        else:
            converted = [file_data[i] for i in range(ad_start, ad_end)]
            if not any(re.search(".*title.*", line) for line in converted):
                title_admo = admonition_logo(type, "")
                file_data.insert(ad_start + 1, title_admo)
    return file_data


# IMAGES
def get_image(image):
    image = os.path.basename(image)
    for sub, dirs, files in os.walk(vault):
        for file in files:
            filepath = sub + os.sep + file
            if image in file:
                return filepath


def move_img(line):
    img_flags = re.search("[\|\+\-](.*)[]{1,2})]", line)
    if img_flags and not re.search("\-\d+", line):
        img_flags = img_flags.group(0)
        img_flags = img_flags.replace("|", "")
        img_flags = img_flags.replace("]", "")
        img_flags = img_flags.replace(")", "")
        img_flags.replace("(", "")
    else:
        img_flags = ""
    final_text = re.search("(\[{2}|\().*\.(png|jpg|jpeg|gif)", line)
    final_text = final_text.group(0)
    final_text = final_text.replace("(", "")
    final_text = final_text.replace("%20", " ")
    final_text = final_text.replace("[", "")
    final_text = final_text.replace("]", "")
    final_text = final_text.replace(")", "")
    image_path = get_image(final_text)
    final_text = os.path.basename(final_text)
    img_flags = img_flags.replace(final_text, "")
    img_flags = img_flags.replace("(", "")
    if image_path:
        shutil.copyfile(image_path, f"{img}/{final_text}")
        final_text = f"../assets/img/{final_text}"
        final_text = f"![{img_flags}]({final_text})"
        final_text = re.sub(
            "!?(\[{1,2}|\().*\.(png|jpg|jpeg|gif)(.*)(\]{2}|\))", final_text, line
        )
    else:
        final_text = line
    return final_text


def excalidraw_convert(line):
    if ".excalidraw" in line:
        # take the png img from excalidraw
        line = line.replace(".excalidraw", ".excalidraw.png")
        line = line.replace(".md", "")
    return line


def convert_no_embed(line):
    final_text = line
    if re.match("\!\[{2}", line) and not re.match("(.*)\.(png|jpg|jpeg|gif)", line):
        final_text = line.replace("!", "")  # remove "!"
        final_text = re.sub("#\^(.*)", "]]", final_text)  # Link to block doesn't work
    return final_text


def convert_to_wikilink(line):
    final_text = line
    if (
        not re.search("\[\[", final_text)
        and re.search("\[(.*)]\((.*)\)", final_text)
        and not re.search("https", final_text)
    ):  # link : [name](file#title) (and not convert external_link)
        title = re.search("\[(.*)]", final_text)
        title = title.group(1)
        link = re.search("\((.*)\)", final_text)
        link = link.group(1)
        link = link.replace("%20", " ")
        wiki = f"[[{link.replace('.md', '')}|{title}]] "
        final_text = re.sub("\[(.*)]\((.*)\)", wiki, final_text)

    return final_text


def transluction_note(line):
    # If file (not image) start with "![[" : transluction with rmn-transclude (exclude
    # image from that)
    # Note : Doesn't support partial transluction for the moment ; remove title
    final_text = line
    if (
        re.search("\!\[", line)
        and not re.search("(png|jpg|jpeg|gif)", line)
        and not re.search("https", line)
    ):
        final_text = line.replace("!", "")  # remove "!"
        final_text = re.sub("#(.*)", "]]", final_text)
        final_text = re.sub("\\|(.*)", "]]", final_text)  # remove Alternative title
        final_text = re.sub("]]", "::rmn-transclude]]", final_text)
    return final_text


def clipboard(filepath, folder):
    filename = os.path.basename(filepath)
    filename = filename.replace(".md", "")
    filename = filename.replace(" ", "-")
    folder_key = folder.replace(f"{BASEDIR}/_")
    clip = f"{web}{folder_key}/{filename}"
    if sys.platform == "ios":
        try:
            import pasteboard  # work with pyto

            pasteboard.set_string(clip)
        except ImportError:
            try:
                import clipboard  # work with pytonista

                clipboard.set(clip)
            except ImportError:
                print(
                    "Please, report issue with your OS and configuration to check if it possible to use another clipboard manager"
                )
    else:
        try:
            # trying to use Pyperclip
            import pyperclip

            pyperclip.copy(clip)
        except ImportError:
            print(
                "Please, report issue with your OS and configuration to check if it possible to use another clipboard manager"
            )


def file_write(file, contents, folder):
    file_name = os.path.basename(file)
    if contents == "":
        return False
    else:
        path = Path(f"{folder}/{file_name}")
        if not os.path.exists(path):
            new_notes = open(path, "w", encoding="utf-8")
            for line in contents:
                new_notes.write(line)
            new_notes.close()
            frontmatter_check(file_name, folder)
            return True
        else:
            meta = frontmatter.load(file)
            if not meta["share"] or meta["share"] == False:
                delete_file(file, folder)
            return False


def file_convert(file, folder, option=0):
    final = []
    path_folder = folder.replace(f"{BASEDIR}/", "")
    if not path_folder in file:
        data = open(file, "r", encoding="utf-8")
        meta = frontmatter.load(file)
        lines = data.readlines()
        data.close()
        if option == 1:
            if "share" not in meta.keys() or meta["share"] is False:
                meta["share"] = True
                update = frontmatter.dumps(meta)
                meta = frontmatter.loads(update)
                update_frontmatter(file, folder, 1)
            else:
                update_frontmatter(file, folder, 0)
        else:
            update_frontmatter(file, folder, 0)
            if "share" not in meta.keys() or meta["share"] is False:
                return final
        lines = admonition_trad(lines)
        for ln in lines:
            final_text = ln.replace("  \n", "\n")
            final_text = final_text.replace("\n", "  \n")
            final_text = convert_to_wikilink(final_text)
            final_text = excalidraw_convert(final_text)
            if re.search("\^\w+", final_text) and not re.search(
                "\[\^\w+\]", final_text
            ):
                final_text = re.sub("\^\w+", "", final_text)  # remove block id
            if "embed" in meta.keys() and meta["embed"] == False:
                final_text = convert_to_wikilink(final_text)
                final_text = convert_no_embed(final_text)
            else:
                final_text = transluction_note(final_text)
            final_text = re.sub("\%{2}(.*)\%{2}", "", final_text)
            final_text = re.sub("^\%{2}(.*)", "", final_text)
            final_text = re.sub("(.*)\%{2}$", "", final_text)
            if re.search(r"\\U\w+", final_text):
                emojiz = re.search(r"\\U\w+", final_text)
                emojiz = emojiz.group().strip().replace('"', "")
                convert_emojiz = (
                    emojiz.encode("ascii")
                    .decode("unicode-escape")
                    .encode("utf-16", "surrogatepass")
                    .decode("utf-16")
                )
                final_text = re.sub(r"\\U\w+", convert_emojiz, final_text)
            if final_text.strip().endswith("%%") or final_text.strip().startswith("%%"):
                final_text = ""
            elif re.search("[!?]{3}ad-\w+", final_text):
                final_text = final_text.replace("  \n", "\n")
            if re.search("#\w+", final_text) and not re.search("`#\w+`", final_text):
                token = re.findall("#\w+", final_text)
                token = list(set(token))
                for i in range(0, len(token)):
                    IAL = (
                        "**"
                        + token[i].replace("#", " ")
                        + "**{: "
                        + token[i]
                        + "}{: .hash}"
                    )
                    final_text = final_text.replace(token[i], IAL, 1)
            elif re.search("\{\: (id=|class=|\.).*\}", final_text):
                IAL = re.search("\{\: (id=|class=|\.).*\}", final_text)
                contentIAL = re.search("(.*)\{", final_text)
                if contentIAL:
                    contentIAL = contentIAL.group().replace("{", "")
                    IAL = IAL.group()
                    IAL = IAL.replace("id=", "#")
                    IAL = IAL.replace("class=", ".")
                    if re.search("[\*\_]", contentIAL):  # markdown found
                        syntax = re.search("(\*\*|\*|_)", contentIAL)
                        new = re.sub("(\*\*|\*|_)", "", contentIAL)  # clear md syntax
                        new = syntax.group() + new + syntax.group() + IAL
                    else:
                        new = "**" + contentIAL.rstrip() + "**" + IAL
                    final_text = re.sub(
                        "(.*)\{\: (id=|class=|\.).*\}(\*\*|\*|_)( ?)", new, final_text
                    )
                if re.search("==(.*)==", final_text):
                    final_text = re.sub("==", "[[", final_text, 1)
                    final_text = re.sub("( ?)==", "::highlight]]", final_text, 2)
                    final_text = re.sub("\{\: (id=|class=|\.).*\}", "", final_text)
            elif re.search("==(.*)==", final_text):
                final_text = re.sub("==", "[[", final_text, 1)
                final_text = re.sub("( ?)==", "::highlight]] ", final_text, 2)
            elif re.search(
                "(\[{2}|\().*\.(png|jpg|jpeg|gif)", final_text
            ):  # CONVERT IMAGE
                final_text = move_img(final_text)
            elif re.fullmatch(
                "\\\\", final_text.strip()
            ):  # New line when using "\" in obsidian file
                final_text = "  \n"
            elif re.search("(\[{2}|\[).*", final_text):
                # Escape pipe for link name
                final_text = final_text.replace("|", "\|")
                # Remove block ID (because it doesn't work)
                final_text = re.sub("#\^(.*)]]", "]]", final_text)
                final_text = final_text + "  "
            final.append(final_text)
        return final

    else:
        return final


def search_share(option=0, stop_share=1):
    filespush = []
    check = False
    folder = "_notes"
    for sub, dirs, files in os.walk(vault):
        for file in files:
            filepath = sub + os.sep + file
            if filepath.endswith(".md") and "excalidraw" not in filepath:
                try:
                    yaml_front = frontmatter.load(filepath)
                    if "folder" in yaml_front.keys():
                        folder = yaml_front["folder"]
                        folder = check_folder(folder)
                    else:
                        folder = check_folder("_notes")
                    if "share" in yaml_front.keys() and yaml_front["share"] is True:
                        if option == 1:
                            if "update" in yaml_front and yaml_front["update"] is False:
                                update = 1
                            else:
                                update = 0
                            if diff_file(filepath, folder, update):
                                delete_file(filepath, folder)
                                contents = file_convert(filepath, folder)
                                check = file_write(filepath, contents, folder)
                            else:
                                check = False
                        if option == 2:
                            delete_file(filepath, folder)
                            contents = file_convert(filepath, folder)
                            check = file_write(filepath, contents, folder)
                        destination = dest(filepath, folder)
                        if check:
                            filespush.append(destination)
                    else:
                        if stop_share == 1:
                            delete_file(filepath, folder)
                except (
                    yaml.scanner.ScannerError,
                    yaml.constructor.ConstructorError,
                ) as e:
                    pass

    return filespush, folder


def git_push(COMMIT):
    try:
        import git

        repo = git.Repo(Path(f"{BASEDIR}/.git"))
        repo.git.add(".")
        repo.git.commit("-m", f"{COMMIT}")
        origin = repo.remote("origin")
        origin.push()
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {COMMIT} successfully 🎉")
    except ImportError:
        print(
            f"[{datetime.now().strftime('%H:%M:%S')}] Please, use another way to push your change 😶"
        )


def convert_one(ori, delopt, git):
    file_name = os.path.basename(ori).upper()
    yaml_front = frontmatter.load(ori)
    priv = "_notes"
    if "folder" in yaml_front.keys():
        priv = yaml_front["folder"]
        priv=check_folder(priv)
    if delopt is False:
        print(
            f"[{datetime.now().strftime('%H:%M:%S')}] STARTING CONVERT [{file_name}] OPTIONS :\n- UPDATE "
        )
        delete_file(ori, priv)
    else:
        print(
            f"[{datetime.now().strftime('%H:%M:%S')}] STARTING CONVERT [{file_name}] OPTIONS :\n- PRESERVE"
        )
    contents = file_convert(ori, priv, 1)
    check = file_write(ori, contents, priv)
    if check and not git:
        COMMIT = f"Pushed {file_name.lower()} to blog"
        git_push(COMMIT)
        clipboard(ori, priv)
    elif check and git:
        print(
            f"[{datetime.now().strftime('%H:%M:%S')}] 🎉 Successfully converted {file_name.lower()}"
        )
    else:
        print(
            f"[{datetime.now().strftime('%H:%M:%S')}] {file_name.lower()} already converted 😶"
        )


def convert_all(delopt=False, git=False, force=False, stop_share=0):
    if git:
        git_info = "NO PUSH"
    else:
        git_info = "PUSH"

    if delopt:  # preserve
        print(
            f"[{datetime.now().strftime('%H:%M:%S')}] STARTING CONVERT [ALL] OPTIONS :\n- {git_info}\n- PRESERVE FILES"
        )
        new_files, priv = search_share(0, stop_share)
    elif force:
        print(
            f"[{datetime.now().strftime('%H:%M:%S')}] STARTING CONVERT [ALL] OPTIONS :\n- {git_info}\n- FORCE UPDATE"
        )
        new_files, priv = search_share(2, stop_share)
    else:
        print(
            f"[{datetime.now().strftime('%H:%M:%S')}] STARTING CONVERT [ALL] OPTIONS :\n- {git_info}\n- UPDATE MODIFIED FILES"
        )
        new_files, priv = search_share(1, stop_share)
    commit = "Add to blog:\n"
    if len(new_files) > 0:
        for md in new_files:
            commit = commit + "\n - " + md
        if git is False:
            if len(new_files) == 1:
                md = "".join(new_files)
                commit = md
                clipboard(md, priv)
            commit = f"Add to blog: \n {commit}"
            git_push(commit)
        else:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] 🎉 {commit}")
    else:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] File already exists 😶")


def blog():
    parser = argparse.ArgumentParser(
        description="Create file in _notes, move image in assets, convert to relative path, add share support, and push to git"
    )
    group_f = parser.add_mutually_exclusive_group()
    group_f.add_argument(
        "--preserve",
        "--p",
        "--P",
        help="Don't delete file if already exist",
        action="store_true",
    )
    group_f.add_argument(
        "--update",
        "--u",
        "--U",
        help="force update : delete all file and reform.",
        action="store_true",
    )
    parser.add_argument(
        "--filepath",
        "--f",
        "--F",
        help="Filepath of the file you want to convert",
        action="store",
        required=False,
    )
    parser.add_argument(
        "--git", "--g", "--G", help="No commit and no push to git", action="store_true"
    )
    parser.add_argument(
        "--keep",
        "--k",
        help="Keep deleted file from vault and removed shared file",
        action="store_true",
    )
    args = parser.parse_args()
    ori = args.filepath
    delopt = False
    if args.preserve:
        delopt = True
    force = args.update
    ng = args.git
    if not args.keep:
        delete_not_exist()
        stop_share = 1
    else:
        stop_share = 0
    if ori:
        if os.path.exists(ori):  # Share ONE
            convert_one(ori, delopt, ng)
        else:
            print(f"Error : {ori} doesn't exist.")
            return
    else:
        convert_all(delopt, ng, force, stop_share)


if __name__ == "__main__":
    blog()
