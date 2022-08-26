import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
from twilio.rest import Client


def twillio_send_message(body):
    account = "ACCOUNT_HERE_ID"
    token = "TOKEN_HERE"
    client = Client(account, token)
    message = client.messages.create(to="TO PHONE HERE", from_="FROM PHONE HERE",
                                     body=str(body))


def test_req(url, retry=5):
    headers = Headers(os="mac", headers=True).generate()
    try:
        response = requests.get(url=url, headers=headers)
        print(f"[+] {url} {response.status_code}")
    except Exception as ex:
        if retry:
            print(f"[INFO] retry ({retry}) => {url}")
            return test_req(url, retry=(retry - 1))
        else:
            raise
    else:
        return response


def links_from_pages():
    global readstos
    count_page = int(input('Введите количество страниц которые я соберу: '))
    count = 1
    for a in range(1, count_page + 1):
        r = test_req(
            url=f'http://theeroticreview.com/reviews/newreviewsList.asp?Valid=1&mp=0&SortBy=3&searchreview=1&svcEscort=1&gDistance=0&page={a}')
        soup = BeautifulSoup(r.text, "lxml")
        page_on_links = soup.find("div", class_="ter-table").find_all("a")
        pages_links = []
        for page_link in page_on_links:
            ready_link = page_link.get("href")
            readstos = f"https://theeroticreview.com{ready_link}"
            pages_links.append(readstos)
        for elem in pages_links:
            with open('links_urls.txt', "a+") as fz:
                fz.write(elem + str('\n'))
        count = count + 1
        if a % 100 == 0:
            twillio_send_message(body=f"Вообщем собрал уже {count} и остановился на {readstos} PS: Parsing Аккаунтов Эскорт ( Разработка БелыйБелыйПони )")


if __name__ == "__main__":
    links_from_pages()