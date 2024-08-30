from django.http import JsonResponse
from invoice.models.company import Company


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
        company = Company.objects.filter(id=company_id).values('cif', 'email', 'uid', 'password', 'id').first()
        if company['cif'] == cif and company['email'] == email and company['uid'] == uid and company['password'] == password:
            return [True, company]
        else: 
            return [None, None]

    except Exception as e:
        return [None, None]