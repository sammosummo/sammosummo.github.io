import json
import urllib
import yaml
import re
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm


def get_audioboook_details(url):
    """Return dictionary containing audiobook details from audible.

    """
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, features="html.parser")
    jsn = soup.find_all("script", type="application/ld+json")[1]
    data = json.loads(jsn.contents[0])[0]
    m = data["duration"].lstrip("PT").split("H")[1].split("M")[0]
    if "abridged" not in data:
        data["abridged"] = "false"
    return {
        "abridged": data["abridged"] == "true",
        "audible_popularity": int(data["aggregateRating"]["ratingCount"]),
        "audible_score": float(data["aggregateRating"]["ratingValue"]),
        "year": int(data["datePublished"].split("-")[0]),
        "month": int(data["datePublished"].split("-")[1]),
        "day": int(data["datePublished"].split("-")[2]),
        "hours": int(data["duration"].lstrip("PT").split("H")[0]),
        "minutes": int(m) if m else 0,
        "image": data["image"],
        "title": data["name"],
        "author": data["author"][0]["name"],
        "narrator": [r["name"] for r in data["readBy"]],
    }


def get_series(url):
    """Return dictionary with series name, if there is one.

    """
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, features="html.parser")
    try:
        series = soup.find("div", class_="authorsandseries").find_all("a")[1:]
        series = [re.sub(r"\([^()]*\)", "", s.contents[0]).rstrip() for s in series][0]
        return {"series": series}
    except:
        return {}


def simple(x):
    """Simplify a string.

    """
    return "".join(e for e in re.sub(r"\[[^()]*\]", "", str(x)) if e.isalnum()).lower()


def audiobooks():

    df = pd.read_csv("../../_data/awards.csv", encoding="latin")
    df["Year"] = df.Year.apply(simple)
    df["Title"] = df.Title.apply(simple)
    df["Recipient"] = df.Recipient.apply(simple)
    df["lookup"] = df.Title + df.Recipient

    f = "../../_data/audiobooks.yaml"
    books = yaml.load(open(f), Loader=yaml.FullLoader)
    data = []

    for book in tqdm(books):

        dic = get_audioboook_details(book["audible"])
        dic.update(get_series(book["librarything"]))
        dic.update(book)
        data.append(dic)

    yaml.dump(data, open(f, "w"))


if __name__ == "__main__":

    audiobooks()
