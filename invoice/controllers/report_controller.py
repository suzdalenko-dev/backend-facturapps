import os
import openpyxl
from invoice.models.article import Article
from invoice.models.company import Company
from invoice.utils.time_suzdal import creating_invoice_minutes
from invoice.utils.util_suzdal import json_suzdal, user_auth
from mysite import settings


def default_report(request):
    companys = Company.objects.values('razon', 'numvisit', 'regtime', 'lastvisit', 'country', 'province')
    response = list(companys)

    return json_suzdal({'res':response, })


def entity_report(request, current_entity):
    auth_status, company = user_auth(request, None)
    if auth_status is None or company is None:
        return json_suzdal({'login': False, 'status':'error', 'message':'Usuario no esta logeado'})

    workbook = openpyxl.Workbook()
    sheet = workbook.active

    res_data = [['App', 'Factura Simple', 'Suzdalenko Alexey']]
    if current_entity == 'facturas':
        pass
    if current_entity == 'clientes':
        pass
    if current_entity == 'articulos':
        res_data = Article.objects.filter(company_id=company['id']).values_list('artcode', 'description', 'price', 'iva', 'ivatype')
        res_data = list(res_data)
        res_data.insert(0, ['Código Artículo', 'Descripción', 'Precio Unidad €', 'IVA %', 'Tipo IVA'])
        
    print(res_data)

    for row in res_data:
        sheet.append(row)

    folder_path = os.path.join(settings.BASE_DIR, 'media', str(company['id']), 'reports')
    if not os.path.exists(folder_path): os.makedirs(folder_path)
    file_name = f"{current_entity}-{creating_invoice_minutes()}.xlsx"
    file_path = os.path.join(folder_path, file_name)
    workbook.save(file_path)

    
    
    print("Excel file created with list data!")


    return json_suzdal({'res': current_entity, })