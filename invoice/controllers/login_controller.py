from invoice.models.company import Company
from django.contrib.auth.hashers import check_password
from ..utils.util_suzdal import json_suzdal
from ..utils.time_suzdal import time_suzdal


def try_login(request):
    try:
        email    = request.POST.get('email').strip()
        password = request.POST.get('password').strip()

        company = Company.objects.get(email=email)
        if not check_password(password, company.password):
            return json_suzdal({'message': 'Usuario no encotrado..', 'status': 'error'})
      
        company.lastvisit = time_suzdal()
        company.numvisit += 1
        company.save()

        rdata = {
            'company_id': company.id,
            'uid': company.uid,
            'status': 'ok',
        }

        res = json_suzdal(rdata)
        return res
    
    except Exception as e:
            return json_suzdal({'message': 'Usuario no encotrado...','status': 'error'})