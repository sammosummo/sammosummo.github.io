"""Run this script before committing.

"""
from code2yaml import code2yaml
from make_my_bib import make_my_bib
from zotero import download_refs
from add_refs import add_refs


if __name__ == "__main__":

    code2yaml()
    make_my_bib()
    download_refs()
    add_refs()
