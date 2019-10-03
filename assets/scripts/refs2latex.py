import yaml


def main():

    lines = ""
    with open("../../_data/my_papers.yaml") as f:

        data = yaml.load(f, Loader=yaml.FullLoader)
        data = sorted(data["my_papers"], key=lambda i: i["sort"])[::-1]

        for paper in data:

            line = "%"
            authors = paper["authors"].replace("</b>", "}").replace("<b>", r"\textbf{")
            authors = r"\item " + authors.replace("&", r"\&")
            line += authors
            line += f" ({paper['year']}). {paper['title']} "
            line += paper["editor"] if "editor" in paper else ""

            # this is a book
            if "book" in paper:
                line += r" \emph{" + paper["book"] + "}"
                if "collection" in paper and "volume" in paper:
                    line += f" ({paper['collection']} vol.~{paper['volume']}, pp.~{paper['first_page']}--{paper['last_page']})."
                elif "book" in paper and "volume" in paper:
                    line += f" (vol.~{paper['volume']}, pp.~{paper['first_page']}--{paper['last_page']})."
                elif "book" in paper and "first_page" in paper:
                    line += f" (pp.~{paper['first_page']}--{paper['last_page']})."
                else:
                    line += "."
                line += f" {paper['city']}, {paper['state']}: {paper['publisher']}."

            # this is an article
            else:
                line += r"\emph{" + paper["journal"] + "}"
                if "volume" in paper:
                    line += ", \emph{" + paper["volume"] + "}"
                if "issue" in paper:
                    line += f"({paper['issue']})"
                if "first_page" in paper:
                    line += f", {paper['first_page']}"
                if "last_page" in paper:
                    line += f"--{paper['last_page']}."
                else:
                    line += "."

            # hyperlinks
            if "doi" in paper:
                line += (
                    " DOI:~\href{"
                    + f"https://doi.org/{paper['doi']}"
                    + "}{"
                    + paper["doi"]
                    + "}."
                )
            if "pmid" in paper:
                line += (
                    " PMID:~\href{"
                    + f"https://www.ncbi.nlm.nih.gov/pubmed/?term={paper['pmid']}"
                    + "}{"
                    + paper["pmid"]
                    + "}."
                )

            """
            {% if paper.journal %}
    {% if paper.volume or paper.first_page %}
      <i>{{ paper.journal }}</i>,
      {% if paper.volume %}
        {% if paper.issue %}
          {% if paper.first_page %}
            <i>{{ paper.volume }}</i>({{ paper.issue }}),
          {% else %}
            <i>{{ paper.volume }}</i>({{ paper.issue }}).
          {% endif %}
        {% else %}
          {% if paper.first_page %}
            <i>{{ paper.volume }}</i>,
          {% else %}
            <i>{{ paper.volume }}</i>.
          {% endif %}
        {% endif %}
      {% endif %}
      {% if paper.first_page %}
        {% if paper.last_page %}
          {{ paper.first_page }}–{{paper.last_page }}.   
        {% else %}
          {{ paper.first_page }}.
        {% endif %}
      {% endif %}
    {% else %}
      <i>{{ paper.journal }}</i>.
    {% endif %}
  {% endif %}
  {% if paper.doi %}
    DOI: <a href="https://doi.org/{{ paper.doi }}">{{ paper.doi }}</a>.
  {% endif %}
  {% if paper.pmid %}
    PMID: <a href="https://www.ncbi.nlm.nih.gov/pubmed/?term={{ paper.pmid }}">{{ paper.pmid }}</a>.
  {% endif %}
            
            """

            print(line)


if __name__ == "__main__":

    main()
