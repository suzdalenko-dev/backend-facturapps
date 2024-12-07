from invoice.utils.util_suzdal import json_suzdal
import requests


def parse_work(request, id):

    url = "https://example.com"
    response = requests.get(url)

    return json_suzdal({'id': response.text })