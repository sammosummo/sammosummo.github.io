"""Create the bibliography file my_papers.yml.

"""

from Bio import Entrez
import re


def main():
    """Grab all my publications and format them into a YAML bibliography.

    """
    print("searching pubmed for my papers")
    Entrez.email = "your.email@example.com"
    handle = Entrez.esearch(
        db="pubmed", sort="date", retmax="200", retmode="xml", term="mathias sr[author]"
    )
    pmids = Entrez.read(handle)["IdList"]
    print(f"found {len(pmids)} with my full name")
    extras = ["28480992", "28385874", "27744290"]
    pmids += extras
    print(f"added {len(extras)} more without my full name")
    print(f"getting details of {len(pmids)} papers")
    pmids = ",".join(pmids)
    handle = Entrez.efetch(db="pubmed", retmode="xml", id=pmids)
    papers = Entrez.read(handle)["PubmedArticle"]
    data = []

    for paper in papers:

        article = paper["MedlineCitation"]["Article"]
        journal = article["Journal"]
        date = journal["JournalIssue"]["PubDate"]
        year = date["Year"]
        month = "00" if "Month" not in date else date["Month"]
        if len(month) == 3:
            month = dict(
                zip(
                    [
                        "Jan",
                        "Feb",
                        "Mar",
                        "Apr",
                        "May",
                        "Jun",
                        "Jul",
                        "Aug",
                        "Sep",
                        "Oct",
                        "Nov",
                        "Dec",
                    ],
                    range(1, 13),
                )
            )[month]
        sort = year + "%02d" % int(month)
        ids = paper["PubmedData"]["ArticleIdList"]

        authors = []
        for _a in article["AuthorList"]:
            if "LastName" in _a:
                a = _a["LastName"] + ", " + ". ".join(_a["Initials"]) + "."
            else:
                a = _a["CollectiveName"].rstrip()
            authors.append(a)
        if len(authors) > 1:
            authors[-1] = "& " + authors[-1]

        jt = journal["Title"].title().replace("Of The", "of the").replace("And", "and")
        jt = jt.replace("Of", "of").replace(" (New York, N.Y. : 1991)", "")
        jt = jt.split(" : ")[0]
        jt = jt.replace(". ", ": ").replace("In ", "in ").replace(": Cb", "")
        jt = jt.replace("Jama", "JAMA")

        ji = journal["JournalIssue"]
        volume = None if "Volume" not in ji else ji["Volume"]
        issue = None if "Issue" not in ji else ji["Issue"]

        title = article["ArticleTitle"]
        rtn = re.split("([:] *)", title)
        title = "".join([i.capitalize() for i in rtn])
        keep = ["BP1-BP2", "African", "American", "Americans", "MRI", "QTL", "ENIGMA"]
        title = " ".join(s.upper() if s.upper() in keep else s for s in title.split())

        k = "Pagination"
        first_page = None if k not in article else article[k]["MedlinePgn"]
        if first_page:
            first_page, *last_page = first_page.split("-")

        dic = {
            "authors": ", ".join(authors),
            "title": title if title[-1] != "." else title[:-1],
            "journal": jt,
            "year": year,
            "sort": sort,
            "pmid": str(paper["MedlineCitation"]["PMID"]),
            "doi": [str(i) for i in ids if str(i)[:3] == "10."][0].lower(),
        }
        dic["id"] = dic["pmid"]

        if volume:
            dic["volume"] = volume
        if issue:
            dic["issue"] = issue
        if first_page:
            dic["first_page"] = first_page
        if last_page:
            dic["last_page"] = last_page[0]

        if int(year) >= 2010 and "Correction:" not in title:

            data.append(dic)

    with open("../../_data/my_papers.yaml", "w") as fw:

        fw.write("my_papers:\n")

        for paper in data:

            fw.write(f"""\n - id: "{paper['id']}"\n""")
            del paper["id"]
            [fw.write(f"""   {k}: "{v}"\n""") for k, v in paper.items()]

        s = "".join(open("../../_data/my_papers_manual.yaml").readlines()[1:])
        fw.write(s)


if __name__ == "__main__":
    main()
