
from bs4 import BeautifulSoup



def parse_search_html(html_content: bytes) -> list[dict[str, str]]:
    soup = BeautifulSoup(html_content, "html.parser")
    num_characters = int(soup.select_one("div.whitespace-nowrap b").get_text())

    characters = []
    for tr in soup.select("tbody tr"):
        tds = tr.select("td")

        characters.append(
            {
                "name": tds[0].select_one("a").get_text(strip=True),
                "link": f'https://poe.ninja{tds[0].select_one("a").get("href")}',
                "ascendancy": tds[1].select_one("img").get("alt"),
                "level": tds[1].get_text(" ", strip=True),
                "life": tds[2].get_text(strip=True),
                "es": tds[3].get_text(strip=True),
                "ehp": tds[4].get_text(strip=True),
                "dps": tds[5].get_text(strip=True),
                "skill": tds[5].select("img")[0].get("alt"),
            }
        )

    return characters, num_characters