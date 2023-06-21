import glob
import os
import re
import textwrap
from copy import copy
from typing import Callable, Type

import markdown

import kick

DOC_STRING_REGEX = re.compile(r"\[\[(?P<what>[^\]]*)]]")
DISPLAY_REGEX = re.compile(r"{{(?P<item>[^}]*)}}")
SHOW_ALL_REGEX = re.compile(r"|\[(?P<item>[^|]*)]|")
H3_REGEX = re.compile(r"(?P<text>[a-zA-Z0-9_-]*)<br>\n-----------")
CODEBLOCK_REGEX = re.compile(r"`(?P<code>[^`]*)`")


HEADER = """
<head>
    <link rel="stylesheet" href="styles.css">
</head>"""
RAW_DOCS_DIR = "raw_docs"
FINAL_DOCS_DIR = "docs"
IGNORE_FORMAT_TEXT = "!IGNORE-FORMAT"


def convert_file(fp: str) -> None:
    before_fp = fp
    after_fp = fp.replace(RAW_DOCS_DIR, FINAL_DOCS_DIR)

    with open(before_fp, "r", encoding="utf-8") as f:
        text = f.read()

    if text.splitlines()[0] != IGNORE_FORMAT_TEXT:
        for find in SHOW_ALL_REGEX.findall(text):
            after = "{{x}}".replace("x", find) + f"\n[[{find}]]"
            text = text.replace(f"|[{find}]|", after)

        # Docstring
        for find in DOC_STRING_REGEX.findall(text):
            try:
                item = eval(f"kick.{find}")
                doc = item.__doc__
            except Exception as e:
                pass
            else:
                doc = textwrap.dedent(copy(doc))

                if doc and doc.splitlines()[1].strip() == "|coro|":
                    temp = doc.splitlines()
                    temp.pop(0)
                    temp.pop(0)
                    doc = "\n".join(temp)
                ret = []

                for line in doc.splitlines():
                    if line.startswith("    "):
                        line = f'<span style="margin-left: 30px">{line}</span>'
                    line += "<br>"
                    ret.append(line)

                text = text.replace(f"[[{find}]]", "\n".join(ret))

        for find in DISPLAY_REGEX.findall(text):
            try:
                item = eval(f"kick.{find}")
            except Exception as e:
                pass
            else:
                doc = copy(getattr(item, "__doc__", ""))
                class_ = ""

                if doc and doc.splitlines()[1].strip() == "|coro|":
                    prefix = "async def "
                    temp = doc.splitlines()
                    temp.pop(0)
                    temp.pop(0)
                    doc = "\n".join(temp)
                elif getattr(item, "__is_decorator__", False) is True:
                    prefix = "@"
                    class_ = "at"
                elif isinstance(item, Type):
                    prefix = "class "
                elif isinstance(item, Callable):
                    prefix = "def "
                else:
                    prefix = ""

                if prefix and not class_:
                    class_ = prefix.split(" ")[0]

                after = f"""
                <span class="h4" id="{find}">
                    <span class="{class_}">
                        {prefix}
                    </span>
                    {find}
                </span>"""
                text = text.replace("{{x}}".replace("x", find), textwrap.dedent(after))

        for find in H3_REGEX.findall(text):
            item = f"{find}<br>\n-----------"
            text = text.replace(item, f'<span class="h4">{find}</span>')

        # Codeblock hyperlinks
        for find in CODEBLOCK_REGEX.findall(text):
            after = f'<a href="#{find}" class="hidden">`{find}`</a>'
            text = text.replace(f"`{find}`", after)

    # Convert to HTML
    text = markdown.markdown(text)

    html = f"{HEADER}{text}"

    with open(after_fp, "w", encoding="utf-8") as f:
        f.write(html)


files = glob.glob(f"{RAW_DOCS_DIR}/*.md")

for file in files:
    print(f"Starting on {file}...")
    convert_file(file)
    print(f"Finished {file}")
