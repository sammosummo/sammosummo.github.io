"""Convert .nbib files to .yaml files.

"""
import copy
import pickle
import os
import re
from pubmed_lookup import PubMedLookup
from pubmed_lookup import Publication


nbibs = [os.path.join("_nbibs", f) for f in os.listdir("_nbibs") if ".nbib" in f]
papers = []
paper = {}

for f in nbibs:
    print(f"reading {f}")
    with open(f) as fp:
        for l in fp:
            l = l.rstrip()
            if l == "":
                # blank line, new paper
                if "id" in paper:
                    # save old paper
                    papers.append(copy.copy(paper))
                # blank paper
                paper = {}
            elif l[4] == "-":
                name, data = l.split("-", 1)
                name = name.rstrip()
                data = data.strip()
                if name == "ID":
                    # non-pubmed record
                    paper["id"] = data
                    authors_from_pubmed = None
                elif name == "PMID":
                     # pubmed record
                     paper["id"] = data
                     paper["pmid"] = data
                     _f = os.path.join("_nbibs", f"{data}.pkl")
                     if os.path.exists(_f):
                         # already saved the author list
                         with open(_f, "rb") as fp2:
                             authors_from_pubmed = pickle.load(fp2)
                     else:
                         # getting the author list with special chars
                         print(f"looking up {data}")
                         url = f"http://www.ncbi.nlm.nih.gov/pubmed/{data}"
                         lookup = PubMedLookup(url, '')
                         publication = Publication(lookup)
                         authors = [a.split() for a in publication._author_list]
                         x = lambda a: all((a == a.upper(),"ENIGMA" not in a, "CNV" not in a))
                         y = lambda a: ", " + ". ".join(a) + "." if x(a) else a
                         authors = [[y(a) for a in b] for b in authors]
                         authors = [" ".join(a).replace(" ,", ",") for a in authors]
                         print("authors ->", authors)
                         with open(_f, "wb") as fp2:
                             pickle.dump(authors, fp2)
                         authors_from_pubmed = copy.copy(authors)
                     paper["authors"] = authors_from_pubmed
                elif name == "VI":
                     paper["volume"] = data
                elif name == "IP":
                    paper["issue"] = data
                elif name == "DP":
                    paper["year"] = data.split()[0]
                    paper["sort"] = "%s" % paper["year"]
                    try:
                        paper["month"] = data.split()[1]
                        month_number = dict(zip([
                            'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                            'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec',
                        ], range(12)))[paper["month"]]
                        paper["sort"] = "%s-%02d" % (
                            paper["year"], month_number + 1
                        )
                        paper["month"] = str(paper["month"])
                    except IndexError:
                        pass
                elif name == "TI":
                    new_name = "title"
                    paper[new_name] = data
                elif name == "AB":
                    new_name = "abstract"
                    paper[new_name] = data
                elif name == "FAU" and authors_from_pubmed is None:
                    if "authors" not in paper:
                        paper["authors"] = []
                    surname, fns = data.split(",", 1)
                    fns = fns.strip()
                    fns = fns.split(" ") if " " in fns else [fns]
                    fns = " ".join(f"{n[0].upper()}." for n in fns)
                    author = f"{surname}, {fns}"
                    paper["authors"].append(author)
                elif name == "JT":
                    data = re.sub(r"\([^)]*\)", "", data)
                    words = data.split()
                    ignore = ("on", "in", "of", "the", "and")
                    words = [w.title() if w not in ignore else w for w in words]
                    words = " ".join(words)
                    words = words.replace(".", ":")
                    paper["journal"] = words
                elif "[doi]" in data and "doi" not in paper:
                    paper["doi"] = data.split()[0]
                elif name == "PG":
                    paper["first_page"] = data
                    if "-" in data:
                        f, l = data.split("-")
                        if len(l) < len(f):
                            d = len(f) - len(l)
                            l = f[:d] + l
                        paper["first_page"], paper["last_page"] = (f, l)
                elif name == "ED":
                    paper["editor"] = data
                elif name == "CI":
                    paper["city"] = data
                elif name == "CC":
                    paper["state"] = data
                elif name == "CY":
                    paper["publisher"] = data
            else:
                if name in ("TI", "AB"):
                    paper[new_name] += (" " + l.strip())                    
papers.append(paper)

for paper in papers:
    authors = copy.copy(paper["authors"])
    if len(authors) > 1:
        authors[-1] = f"& {authors[-1]}"
    if len(authors) > 2:
        authors = ", ".join(authors)
    else:
        authors = " ".join(authors)
    authors = authors.replace("Mathias, S.", "<b>Mathias, S.</b>")
    authors = authors.replace("<b>Mathias, S.</b> R.", "<b>Mathias, S. R.</b>")
    paper["authors"] = authors
    if "pmid" in paper:
        if paper["pmid"] == "24389264":
            paper["doi"] = "10.2741/S417"
    if "doi" in paper:
        paper["doi_link"] = "https://www.doi.org/" + paper["doi"]
    if "pmid" in paper:
        paper["pmid_link"] = "https://www.ncbi.nlm.nih.gov/pubmed/" + paper["pmid"]
    if paper["journal"] == "Frontiers in Bioscience":
        paper["journal"] = "Frontiers in Bioscience (Scholar Edition)"
    paper["journal"] = paper["journal"].replace(
        " : Cb", ""
    ).replace(
        " : the", ""
    ).replace(
        " Journal of the Association of European Psychiatrists", ""
    ).replace(
        " : Official Publication of the American College of", ""
    ).replace(
        " Official Journal of the Society For", ""
    )
    paper["title"] = paper["title"][0] + paper["title"][1:].lower()
    paper["title"] = paper["title"].replace(
        "african", "African"
    ).replace(
        "american", "American"
    ).replace(
        "qtl", "QTL"
    ).replace(
        "enigma", "ENIGMA"
    ).replace(
        "mri ", "MRI "
    ).replace(
        ": a", ": A"
    )

with open("_data/my_papers.yaml", "w") as fw:
    fw.write("my_papers:\n")
    for paper in papers:
        if "Correction:" not in paper["title"]:
            for k, v in paper.items():
                v = v.replace('"', "'")
                s = f"""{k}: "{v}"\n"""
                if k == "id":
                    s = "\n - " + s
                else:
                    s = "   " + s
                fw.write(s)
