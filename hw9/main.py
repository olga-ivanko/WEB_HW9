import requests
from bs4 import BeautifulSoup

url = "https://quotes.toscrape.com/"
domain_q = "https://quotes.toscrape.com"
domain_a = "https://quotes.toscrape.com/author"


def find_next_url(soup, domain_q):
    try:
        next_url = soup.find("li", class_="next").a["href"]
        print(next_url)
        if next_url:
            next_to_parse = domain_q + next_url
            return next_to_parse
    except AttributeError:
        return None


def parse_url(url, soup):
    quotes = soup.find_all("div", class_="quote")

    for q in quotes:
        tags_list = []
        quote = q.find("span", class_="text").text
        author = q.find("small", class_="author").text
        tags = q.find_all("a", class_="tag")

        author_url = domain_a + q.a["href"]

        for t in tags:
            tags_list.append(t.text)

        print(quote, author, author_url, tags_list)

    next_to_parse = find_next_url(soup, domain_q)
    if next_to_parse:
        print(next_to_parse)
        next_response = requests.get(next_to_parse)
        next_soup = BeautifulSoup(next_response.text, features="html.parser")
        parse_url(next_to_parse, next_soup)
    return None


if __name__ == "__main__":
    response = requests.get(url)
    soup = BeautifulSoup(response.text, features="html.parser")
    parse_url(url, soup)
