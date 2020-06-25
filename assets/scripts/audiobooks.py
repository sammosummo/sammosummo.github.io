import goodreads_api_client as gr
import json
import urllib.request
import yaml
from tqdm import tqdm
from bs4 import BeautifulSoup


def audible(url):
    """Add book details from Audible.com webpage.

    """
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, features="html.parser")
    jsn = soup.find_all("script", type="application/ld+json")[1]
    data = json.loads(jsn.contents[0])[0]
    m = data["duration"].lstrip("PT").split("H")[1].split("M")[0]
    dic = {
        "audible_popularity": int(data["aggregateRating"]["ratingCount"]),
        "audible_score": float(data["aggregateRating"]["ratingValue"]),
        "year": int(data["datePublished"].split("-")[0]),
        "month": int(data["datePublished"].split("-")[1]),
        "day": int(data["datePublished"].split("-")[2]),
        "hours": int(data["duration"].lstrip("PT").split("H")[0]),
        "minutes": int(m) if m else 0,
        "image": data["image"],
        "title": data["name"].replace("'", "’"),
        "authors": [a["name"] for a in data["author"]],
        "narrators": [r["name"] for r in data["readBy"]],
        "audible": True,
    }
    return dic


def goodreads(grid):
    """Add book details from Goodreads API.

    """
    # print(f"scraping goodreads data from {grid}")
    key = "cQudYNjfcBYXcVj9w9zA"
    client = gr.Client(developer_key=key)
    result = client.Book.show(grid)
    dic = {}

    if result["series_works"]:

        series = result["series_works"]["series_work"]
        series = [series] if not isinstance(series, list) else series
        dic["series"] = [s["series"]["title"].replace("'", "’") for s in series]
        dic["position_in_series"] = [s["user_position"] for s in series]

    dic["goodreads_score"] = float(result["average_rating"])
    dic["goodreads_popularity"] = int(result["ratings_count"])
    # print(f"goodreads data {dic}")
    return dic


def updated(book):
    """Returns an audiobook with details from audible and goodreads.

    """
    if "title" not in book:

        book = {**audible(book["audible_url"]), **book}

    if "goodreads_score" not in book:

        book = {**goodreads(book["goodreads_id"]), **book}

    book["overall_score"] = (book["book"] + book["performance"]) / 2

    return book


def main():
    f = "../../_data/audiobooks.yaml"
    books = yaml.load(open(f), Loader=yaml.FullLoader)
    books = [updated(book) for book in tqdm(books)]
    yaml.dump(books, open(f, "w"))


if __name__ == "__main__":

    main()
