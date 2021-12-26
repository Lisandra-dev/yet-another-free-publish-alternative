
[![GitHub license](https://img.shields.io/github/license/Mara-Li/yet-another-free-publish-alternative)](https://github.com/Mara-Li/yet-another-free-publish-alternative/blob/master/LICENSE)
[![GitHub forks](https://img.shields.io/github/forks/Mara-Li/yet-another-free-publish-alternative)](https://github.com/Mara-Li/yet-another-free-publish-alternative/network) ![GitHub top language](https://img.shields.io/github/languages/top/mara-li/yet-another-free-publish-alternative)
![PyPI](https://img.shields.io/pypi/v/YAFPA?label=YAFPA)
<p align="center"><a href="https://github.com/Mara-Li/YAFPA-python">Powerfull this template with YAFPA</a></p>

---
# Notenote.link

[![Netlify Status](https://api.netlify.com/api/v1/badges/7b37d412-1240-44dd-8539-a7001465b57a/deploy-status)](https://app.netlify.com/sites/owlly-house/deploys)

## What is this?
A digital garden using a custom version of `simply-jekyll`, optimised for integration with [Obsidian](https://obsidian.md). It is more oriented on note-taking and aims to help you build a nice knowledge base that can scale with time. 

[**DEMO**](https://master--owlly-house.netlify.app/)

If you want to see a more refined example, you can check my notes (in french) at [owlly-house](https://www.owlly-house.netlify.app/). 

Issues are welcome, including feedback ! Don't hesitate to ask if you can't find a solution. 💫

![screenshot](/assets/img/screenshot.png)

## What is different?

- Markdown is fully-compatible with Obsidian (including Latex delimiters!)
- There are now only notes (no blog posts).
- There are cosmetic changes (ADHD-friendly code highlighting, larger font, larger page)
- Code is now correctly indented
- Wikilinks, but also alt-text wikilinks (with transclusion!) are usable.

## How do I use this?

You can click on this link and let the deploy-to-netlify-for-free-script do the rest !

[![Deploy to Netlify](https://www.netlify.com/img/deploy/button.svg)](https://app.netlify.com/start/deploy?repository=https://github.com/Mara-Li/yet-another-free-publish-alternative)

Follow the [How to setup this site](https://notenote.link/notes/how-to-setup-this-site) guide, written by [raghuveerdotnet](https://github.com/raghuveerdotnet) and then adapted for this fork.

If you want to use it with Github Pages, it is possible, [please read this](https://github.com/Maxence-L/notenote.link/issues/5#issuecomment-762508069).

## How can I participate?

Open an issue to share feedback or propose features. Star the repo if you like it! 🌟

## How do I customize this for my needs?

Things to modify to make it yours:

- The favicon and profile are here: [assets/site/](assets/site)
- You can change the header in [assets/site/](assets/site) (don't forget the name) and/or [change this line](https://github.com/Mara-Li/yet-another-free-publish-alternative/blob/9d8ae99d867be79a45b5bfbf687e03b95bf8ebd2/assets/css/style.css#L301)
- The main stuff is in [\_config.yml](_config.yml):
    ```yaml
    title: My obsidian notebook
    name: Obsidian Notebook
    user_description: My linked notebook
    tagline: My linked notebook
    notes_url: "https://yourlink.netlify.app"
    profile_pic: /assets/site/profile.gif
    favicon: /assets/site/favicon.png
    logo: /assets/site/LOGO_SEO.png
    copyright_name: MIT
    baseurl: "/" # the subpath of your site, e.g. /blog
    url: "https://owlly-house.netlify.app/" # the base hostname & protocol for your site, e.g. http://example.com
    encoding: utf-8
    ```
- You may want to change the copyright in [\_includes/footer.html](_includes/footer.html):
   ```html
   <p id="copyright-notice">Licence MIT</p>
   ```
On command-line, you can run `bundle exec jekyll serve` then go to `localhost:4000` to check the result.

## Sidenav
You can style the sidenav for your need. 
- Folder name had `.folder_name` class
- Category name had `.category_name` class.
You can use `::marker` to style the marker before each summary.

# Python script

Having files written in Markdown on Obsidian, I created a python script in order to semi-automatically share selected file, not all file, in my blog. 
To install it use `pip install YAFPA`

[You can have more information here](https://pypi.org/project/YAFPA/) and you can work on the script [here](https://github.com/Mara-Li/YAFPA-python).

You need to have python 3.8 on your computer, and `pip` need to be in your PATH.

## Environment
The first time you use the script, it will ask you three things :
- Your vault path (absolute path !)
- The path of the blog (absolute too !)
- The link of your blog, as `https://my-awesome-blog.netlify.app/`

The script will be in `$HOME/.YAFPA-env` so you can edit it with VIM/notepad/your hands…
You can also edit it with `yafpa --config`

Here is a blank sheet to help you if you want to manually write / edit it :
```
vault=
blog_path=
blog=
share=
```
With :
- `vault`: Vault Absolute Path
- `blog_path` : Blog repository absolute path
- `blog` : Blog link
- `share` : your wanted share key ; by default : `share`


## Usage
`usage: yafpa [-h] [--preserve | --update] [--filepath FILEPATH] [--git] [--keep] [--config]`

Create file in folder, move image in assets, convert to relative path, add share support, and push to git

optional arguments:
  - `-h, --help`: show this help message and exit
  - `--preserve, --p, --P` : Don't delete file if already exist
  - `--update, --u, --U` : force update : delete all file and reform.
  - `--filepath FILEPATH, --f FILEPATH, --F FILEPATH `: Filepath of the file you want to convert
  - `--git, --g, --G` : No commit and no push to git
  - `--keep, --k` : Keep deleted file from vault and removed shared file
  - `--config, --c` : Edit the config file

# Frontmatter and metadata
## Script
The script work with the frontmatter :
- `share: true` : Share the file
- `embed: false` : remove the transluction (convert to normal wikilinks)
- `update: false` : Don't update the file at all. 
- `current: false` : Don't update the date
- `folder` : Use another folder than `_notes` alternatively you can use the `category` key
- `category` : Choose a folder and a category for the file as : `folder/category`
    - `folder` is optional ; as default : `_notes`
    -  `category` can be `false` to prevent apparence in the feed
NB : if `category` and `folder` is used at the same time, `folder` will be used as the folder. 


## Blog frontmatter options
- `flux: false` : remove the file from the feed
- `description` : Add a description of the file in the feed. 
- `category: false` : Remove the file from the category feed ; Category is a classement for your file. 

## Exemple of frontmatter :
```yml
category: Roleplay/Application
date: 21-12-2021
share: true
tag: RP/Darkness-Haunted/Application/PC
title: (Darkness Haunted) Alwyn Kallendris
```
The file will be added in the `Roleplay` folder ; and the `Application` will now show the file in the sidebar, the Roleplay page and the collections page. 

### Folder options
The metadata key `folder` allow to use another folder than `_note`.

There are two ways to create the files needed to use this option: 
- You can use the little python script in `assets/script`, with : `python3 assets/script/folder.py folder_name`
- You can use the long way, modify the `_config.md` file and creating folder and main page. 

Here is the steps for the long way :
1. Create a new folder with the name you want, prefixed with `_` (as `_notes` or `_private`)
2. Add to the `_config.yml` : 
   1. collection : 
```yml
  private:
     output: true
     permalink: /folder_name/:title
   ```
   2. defaults
```yml
   - scope: 
       path: ""
       type: folder_name
    values: 
      layout: post
      content-type: notes
  ```
3. Duplicate the `private.md` and rename it with the folder name you want. 
   1. In this new file, change the line `{%- if page.permalink == "/private/" -%}` for `{%- if page.permalink == "/folder_name/" -%}` 
   2. Change the `permalink` key with `permalink: /folder_name/` 
   3. change `{% assign mydocs = site.folder_name | group_by: 'category' %}`

And there is it !

Note : Git don't push empty folder. So, don't forget to create an empty file.
(The python script will do it for you.)

**Notes about Private folder** : the private folder doesn't have a page, and doesn't appear in the feed or in search. The only way to access it is with the link (adding `/private` at the end) 

# Custom CSS

You can add custom css in [custom css](assets/css/custom.css). It will be read when you use hashtag to stylize your text according to [ContextualTypography](https://github.com/mgmeyers/obsidian-contextual-typography) and/or [CodeMirror Options](https://github.com/nothingislost/obsidian-codemirror-options).

To add custom tag to customize your text, you need to edit the `custom.css` file with :
```css
#tag_name {
    css_value : css;
    . . . 
}
```
The script will read the file and change `#tag_name` to `{: .tag_name}`. 

# Customize the script
## Custom Admonition
The file [`custom_admonition`](https://github.com/Mara-Li/yet-another-free-publish-alternative/blob/master/assets/script/custom_admonition.yml) allow you to create custom admonition for the script.
The template is :
```yml
- admonition_type: #Admonition plugin, same name
    - logo #emoji, ASCII...
    - admonition_title #As in admonition plugin
```

A reference of logo used in the original script :
- Note, seelaso : 🖊️
- Abstract, summary, tldr: 📝
- info, todo: ℹ️
- tip, hint, important: 🔥
- success, check, done: ✨
- question, help, faq: ❓
- warning, caution, attention: ⚠️
- failure, fail, missing: ❌
- danger, error: ⚡
- bug: 🐛
- example, exemple: 📌
- quote, cite: 🗨️

## Exclude folder
Sometimes, you want to exclude folder for privacy, or just because you move a file in your archive, and forgot about the share state !
So, you can exclude folder with [`exclude_folder`](https://github.com/Mara-Li/yet-another-free-publish-alternative/blob/master/assets/script/exclude_folder.yml).

The template is :
```yml
- folder_name
- folder_name2
```
(yes, it is just a list

⚠ File in excluded folder are deleted in the blog.

# Obsidian 
→ Please use Wikilinks with "short links" (I BEG YOU)
You can integrate the script within obsidian using the nice plugin [Obsidian ShellCommands](https://github.com/Taitava/obsidian-shellcommands).

You could create two commands :
1. `share all` : `yafpa`
2. `share one` : `yafpa --f {{file_path:absolute}}`

You can use :
- [Customizable Sidebar](https://github.com/phibr0/obsidian-customizable-sidebar)
- [Obsidian Customizable Menu](https://github.com/kzhovn/obsidian-customizable-menu)
To have a button to share your file directly in Obsidian !

#### Template frontmatter
→ The • indicate that this value is optional
```yaml
title: My files•
date: 12-11-2021•
embed: true•
update: true•
current: true•
folder: notes•
flux: true•
share: false 
category: Notes
description: my awesome file
```
You can use MetaEdit / Supercharged links to quickly update the front matter. 
