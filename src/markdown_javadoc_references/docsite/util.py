import requests


def read_url(url: str) -> str:
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.text


def check_url(url: str) -> requests.Response:
    resp = requests.head(url)
    return resp
