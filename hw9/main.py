import requests
from bs4 import BeautifulSoup
import json
from data_upload import load_data_in_db

url = "https://quotes.toscrape.com/"
domain = "https://quotes.toscrape.com"

response = requests.get(url)
soup = BeautifulSoup(response.text, features="html.parser")


quotes_data = []
authors_data = []


def find_next_url(soup, domain):
    try:
        next_url = soup.find("li", class_="next").a["href"]
        # print(next_url)
        if next_url:
            next_to_parse = domain + next_url
            return next_to_parse
    except AttributeError:
        return None


def parse_author_url(url):
    author_response = requests.get(url)
    author_soup = BeautifulSoup(author_response.text, features="html.parser")

    author_details = author_soup.find("div", class_="author-details")
    name = author_details.find("h3", class_="author-title").text

    new_author = {
        "fullname": author_details.find("h3", class_="author-title").text,
        "born_date": author_details.find("span", class_="author-born-date").text,
        "born_location": author_details.find(
            "span", class_="author-born-location"
        ).text,
        "description": author_details.find(
            "div", class_="author-description"
        ).text.strip(),
    }

    if not new_author in authors_data:
        authors_data.append(new_author)
    return name


def parse_url(url, soup):
    print(f"Processing: {url}")
    quotes = soup.find_all("div", class_="quote")

    for q in quotes:
        author = q.find("small", class_="author").text.strip()
        author_url = domain + q.a["href"]
        parse_author_url(author_url)

        tags = q.find_all("a", class_="tag")
        tags_list = []
        for t in tags:
            tags_list.append(t.text)

        new_quote = {
            "tags": tags_list,
            "author": author,
            "quote": q.find("span", class_="text").text.strip(),
        }
        quotes_data.append(new_quote)

    next_to_parse = find_next_url(soup, domain)

    if next_to_parse:
        # print(next_to_parse)
        next_response = requests.get(next_to_parse)
        next_soup = BeautifulSoup(next_response.text, features="html.parser")
        parse_url(next_to_parse, next_soup)

    return "all done"


def authors_to_json():
    with open("authors.json", "w", encoding="utf-8") as file:
        json.dump(authors_data, file, indent=2)

    return "Authors are sucessfully saved to file authors.json"


def quotes_to_json():
    with open("quotes.json", "w", encoding="utf-8") as file:
        json.dump(quotes_data, file, indent=2)
    return "Quotes are sucessfully saved to file quotes.json"


def main():
    print(parse_url(url, soup))
    print(authors_to_json())
    print(quotes_to_json())
    print(load_data_in_db())


if __name__ == "__main__":
    main()
