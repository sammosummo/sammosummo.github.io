"""Add cited references to the front matter of each markdown page.

"""
import os
import re
import sys

import yaml


def get_frontmatter(f):
    """Return front matter from a markdown file in dictionary format.

    """
    with open(f) as fp:
        s = fp.read().partition("---")[2].partition("---")[0]
        d = yaml.safe_load(s)
    return d


def find_cites(f):
    """Return keys to cited papers.

    """
    with open(f) as fp:
        lst = re.findall(r"{{(.+?)}}", fp.read())
    refs = []
    for l in lst:
        if "site.data.refs" in l:
            refs.append(l.split(".")[3])
    return sorted(set(refs))


def replace_frontmatter(f, d):
    """Replace the front matter with new front matter.

    """
    with open(f) as fp:
        s = fp.read().partition("---\n")[2].partition("---\n")[2]
    with open(f, "w") as fw:
        fw.write("---\n")
        yaml.safe_dump(d, fw)
        fw.write(f"---\n{s}")


def add_refs():
    """Add all references.

    """
    posts = [p for p in os.listdir("../../_posts") if ".md" in p]
    for p in posts:
        f = f"../../_posts/{p}"
        d = get_frontmatter(f)
        r = find_cites(f)
        if r:
            d["include_references"] = True
            d["references"] = r
        replace_frontmatter(f, d)


if __name__ == "__main__":
    add_refs()
