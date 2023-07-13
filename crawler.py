import requests
import loader
from bs4 import BeautifulSoup
import urllib3

# ssl warning 제거
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# xpath
xpath = {
    "number": "td:nth-child(1)",
    "title": "td:nth-child(2) > div:nth-child(1) > a",
    "date": "td:nth-child(4)",
    "personnel": "td:nth-child(5)",
    "lecturer": "td:nth-child(7)",
}


# csrf token 추출
def _get_csrf_token(session: requests.Session, login_url):
    response = session.get(login_url, verify=False)
    html = BeautifulSoup(response.content, "html.parser")
    csrf_token = html.find("input", {"name": "csrfToken"}).get("value")

    return csrf_token


# 로그인
def login(session: requests.Session):
    session.get(loader.get_env("main_url"), verify=False)

    login_url = loader.get_env("login_url")
    login_data = {
        "username": loader.get_env("email"),
        "password": loader.get_env("password"),
    }
    response = session.post(login_url, data=login_data, verify=False)
    response.raise_for_status()


def crawl_target(session: requests.Session):
    response = session.get(loader.get_env("crawling_url"), verify=False)
    html = BeautifulSoup(response.content, "html.parser")
    try:
        source = html.select("#listFrm > table > tbody > tr")[0]
    except IndexError:
        crawl_target(session)

    result = {}
    for key in xpath.keys():
        result[key] = (
            source.select_one(xpath[key])
            .get_text(strip=True)
            .replace("\t", "")
            .replace("\n", "")
            .replace("\xa0", " ")
            .replace("\r&nbsp", " ")
            .replace("\r", "")
        )

    return result
