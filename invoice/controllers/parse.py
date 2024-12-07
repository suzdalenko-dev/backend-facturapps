from invoice.utils.util_suzdal import json_suzdal


def parse_work(request, id):
    return json_suzdal({'id': id,})