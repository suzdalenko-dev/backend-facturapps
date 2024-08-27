from django.http import JsonResponse
from invoice.models.company import Company
from ..utils.json_suzdal import json_suzdal


def try_register(request):
    try:

        cif      = request.POST.get('cif').strip()
        email    = request.POST.get('email').strip()
        tlf      = request.POST.get('tlf').strip()
        password = request.POST.get('password').strip()

        company, created = Company.objects.get_or_create(cif=cif, email=email, password=password)
        company.tlf = tlf
        company.numvisit += 1

        print(company)
        print(created)
        # company.tlf = tlf
        # company.save()

        rdata = {
            'id': cif,
            'status': email
        }

        res = json_suzdal(rdata)

        return res
    
    except Exception as e:
            return json_suzdal({'message': str(e),'status': 'error'})


