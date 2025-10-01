import requests


def read_url(url):
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.text


def check_url(url):
    resp = requests.head(url)
    return resp.ok
