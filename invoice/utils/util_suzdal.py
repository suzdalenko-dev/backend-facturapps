from django.http import JsonResponse
from invoice.models.company import Company
from copy import deepcopy


def json_suzdal(response_data):
    response = JsonResponse(response_data)

    # Set CORS headers
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS, PUT, DELETE'
    response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With'
    return response



def user_auth(request):
    company_id = str(request.POST.get('company_id')).strip()
    cif        = str(request.POST.get('cif')).strip()
    email      = str(request.POST.get('email')).strip()
    uid        = str(request.POST.get('uid')).strip()
    password   = str(request.POST.get('password')).strip()

    try:
        company = Company.objects.filter(id=company_id).values('id', 'description', 'cif', 'email', 'emailcliente', 'uid', 'password', 'tlf', 'tlf2', 'country', 'city', 'zipcode', 'province', 'address', 'price').first()
        if company['cif'] == cif and company['email'] == email and company['uid'] == uid and company['password'] == password:
            return [True, company]
        else: 
            return [None, None]
        
    except Exception as e:
        return [None, None]
    


def update_company_data(request):
    company_id = request.POST.get('company_id')
    try:
        c = Company.objects.get(id=company_id)
        c.description  = str(request.POST.get('description')).strip()
        c.emailcliente = str(request.POST.get('emailcliente')).strip()
        c.country      = str(request.POST.get('country')).strip()
        c.province     = str(request.POST.get('province')).strip()
        c.zipcode      = str(request.POST.get('zipcode')).strip()
        c.city         = str(request.POST.get('city')).strip()
        c.address      = str(request.POST.get('address')).strip()
        c.tlf          = str(request.POST.get('tlf')).strip()
        c.tlf2         = str(request.POST.get('tlf2')).strip()
        c.price        = str(request.POST.get('price')).strip()
        c.save()
        c = Company.objects.filter(id=company_id).values('id', 'description', 'cif', 'email', 'emailcliente', 'uid', 'password', 'tlf', 'tlf2', 'country', 'city', 'zipcode', 'province', 'address', 'price').first()
        return [True, c]
    except Exception as e:
        print(str(e))
        return [None, None]

