"""Download my zotero library and convert it to YAML.

"""
import re

from string import ascii_lowercase

from pyzotero import zotero
from unidecode import unidecode


def get_ids():
    """Read file containing ID and API key.

    """
    return [l.strip() for l in open("../../_data/zotero.txt").readlines()]


def download_refs():
    """Download my enitre zotero library.

    """
    library_id, api_key = get_ids()
    zot = zotero.Zotero(library_id, "user", api_key)
    results = zot.everything(zot.top())
    keys = []
    with open("../../_data/refs.yaml", "w") as fw:
        for item in results:
            dic = item["data"]
            authors = []
            _cite = []
            for author in dic["creators"]:
                if author["creatorType"] == "author":
                    if "lastName" in author:
                        _cite.append(author["lastName"])
                        name = author["lastName"] + ","
                        for n in author["firstName"].split():
                            if n not in ("Jr", "Jr.", "Jnr", "Jnr."):
                                n = n[0] + "."
                            name += f" {n}"
                    else:
                        _cite.append(author["name"])
                        name = author["name"]
                    authors.append(name)
            if len(authors) > 1:
                authors[-1] = f"& {authors[-1]}"
            authors = ", ".join(authors)
            date = re.split(" |,|-|/", dic["date"])
            for d in date:
                try:
                    if int(d) > 100:
                        date = str(int(d))
                except ValueError:
                    pass
            for s in ascii_lowercase:
                key = unidecode(authors.split(" ")[0].rstrip(",")) + date + s
                if key not in keys:
                    keys.append(key)
                    fw.write(f"{key}:\n")
                    break
            fw.write(f'   authors: "{authors}"\n')
            fw.write(f'   year: "{date}"\n')
            title = dic["title"].replace('"', "''")
            if dic["itemType"] != "book":
                fw.write(f'   title: "{title}"\n')
            else:
                fw.write(f'   book: "{title}"\n')
            if "publicationTitle" in dic:
                if "arXiv" in dic["publicationTitle"]:
                    arXiv = dic["publicationTitle"].split(":")[1].split()[0]
                    fw.write(f'   arXiv: "{arXiv}"\n')
                    del dic["publicationTitle"]
            _keys = {
                "publicationTitle": "journal",
                "volume": "volume",
                "issue": "issue",
                "bookTitle": "book",
                "publisher": "publisher",
                "edition": "edition",
                "DOI": "doi",
            }
            for k, v in _keys.items():
                if k in dic:
                    if dic[k] != "":
                        fw.write(f'   {v}: "{dic[k]}"\n')
            if "pages" in dic:
                if dic["pages"] != "":
                    pages = re.split("-|–", dic["pages"])
                    fw.write(f'   first_page: "{pages[0]}"\n')
                    if len(pages) > 1:
                        fw.write(f'   last_page: "{pages[1]}"\n')
            editors = []
            for editor in dic["creators"]:
                if editor["creatorType"] == "editor":
                    if "lastName" in editor:
                        name = ""
                        for n in editor["firstName"].split():
                            name += f"{n[0]}. "
                        name += editor["lastName"]
                    else:
                        name = editor["name"]
                    editors.append(name)
            if len(editors) > 1:
                editors[-1] = f"& {editors[-1]} (Eds.)"
            elif len(editors) == 1:
                editors[0] = f"{editors[0]} (Ed.)"
            editors = ", ".join(editors)
            if editors != "":
                fw.write(f'   editors: "In {editors}"\n')
            if len(_cite) == 1:
                citep = f"({_cite[0]}, {date})"
                citet = f"{_cite[0]} ({date})"
            elif len(_cite) == 2:
                citep = f"({_cite[0]} & {_cite[1]}, {date})"
                citet = f"{_cite[0]} and {_cite[1]} ({date})"
            else:
                citep = f"({_cite[0]} <i>et al.</i>, {date})"
                citet = f"{_cite[0]} <i>et al.</i> ({date})"
            fw.write(f'   citep: "[{citep}](#{key})"\n')
            fw.write(f'   citenp: "[{citep[1:-1]}](#{key})"\n')
            fw.write(f'   citet: "[{citet}](#{key})"\n')
            fw.write("\n")


if __name__ == "__main__":
    download_refs()
