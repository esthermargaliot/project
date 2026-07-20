from bs4 import BeautifulSoup


def fill_html(html, mapped):
    soup = BeautifulSoup(html, "html.parser")



    for input_tag in soup.find_all("input"):
        input_id = input_tag.get("id")

        if input_id and input_id in mapped:
            input_tag["value"] = str(mapped[input_id])


    return str(soup)
