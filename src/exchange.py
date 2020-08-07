import requests


def get_rate_for_date(date):
    req_url = 'https://api.exchangeratesapi.io/' + date
    payload = {"symbols": "CAD", "base": "USD"}
    resp = requests.get(req_url, params=payload)
    resp.raise_for_status()
    return resp.json()["rates"]["CAD"]


