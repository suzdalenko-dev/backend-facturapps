from datetime import datetime
import os
import openpyxl
from invoice.models.article import Article
from invoice.models.company import Company
from invoice.models.customer import Customer
from invoice.models.factura import Factura
from invoice.utils.time_suzdal import creating_invoice_minutes, creating_invoice_time
from invoice.utils.util_suzdal import delete_files_after_delay, json_suzdal, start_deletion_thread, user_auth
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
        default_from = str(request.POST.get('default_from', '2022-01-01')).strip(); default_to = str(request.POST.get('default_to', '2222-01-01')).strip()
        sql = f"""SELECT f.*, c.clientcode, c.cif_nif, c.razon
                 FROM invoice_factura f 
                 JOIN invoice_customer c ON f.customer_id = c.id
                 WHERE f.company_id = %s AND f.fecha_expedicion >= '{default_from}' AND f.fecha_expedicion <= '{default_to}' ORDER BY id DESC"""
        print(sql)
        res_data = Factura.objects.raw(sql, [company['id']])
        res_data = [
            [factura.fecha_expedicion, factura.serie_fact, factura.ejercicio, factura.name_factura, factura.subtotal, factura.importe_ivas, factura.total, factura.observacion, factura.apunta_factura, 
             factura.clientcode, factura.cif_nif, factura.razon]
            for factura in res_data
        ]
        res_data.insert(0, ['Fecha expedición', 'Número', 'Ejercicio', 'Tipo factura', 'Importe lineas', 'Importe IVA', 'Importe total', 'Observación', 'Apunta a factura', 'Cliente número', 'CIF NIF', 'Razon social - nombre'])

    if current_entity == 'clientes':
        res_data = Customer.objects.filter(company_id=company['id']).values_list('clientcode', 'cif_nif', 'razon', 'emailcustomer', 'phone', 'country', 'province', 'zipcode', 'city', 'address').order_by('-id')
        res_data = list(res_data)
        res_data.insert(0, ['Código cliente', 'CIF NIF', 'Razón social - nombre', 'Email', 'Teléfono', 'País', 'Provincia', 'Código postal', 'Cuidad', 'Dirección'])
    if current_entity == 'articulos':
        res_data = Article.objects.filter(company_id=company['id']).values_list('artcode', 'description', 'price', 'iva', 'ivatype').order_by('-id')
        res_data = list(res_data)
        res_data.insert(0, ['Código artículo', 'Descripción', 'Precio unidad €', 'IVA %', 'Tipo IVA'])
        
    for row in res_data:
        sheet.append(row)

    current_time = datetime.now()
    year  = str(current_time.strftime('%Y'))
    folder_path = os.path.join(settings.BASE_DIR, 'media', year, str(company['id']), 'reports')
    if not os.path.exists(folder_path): os.makedirs(folder_path)
    file_name = f"{current_entity}-{creating_invoice_minutes()}.xlsx"
    file_path = os.path.join(folder_path, file_name)
    workbook.save(file_path)

    file_path = file_path.split('media')
    start_deletion_thread(folder_path)

    return json_suzdal({'url':'media'+file_path[1], 'status':'ok', 'company':company})