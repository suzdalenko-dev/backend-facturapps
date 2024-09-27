from invoice.models.company import Company
from invoice.utils.util_suzdal import json_suzdal


def default_report(request):
    companys = Company.objects.values('razon', 'numvisit', 'regtime', 'lastvisit', 'country', 'province')
    response = list(companys)

    return json_suzdal({'res':response, })