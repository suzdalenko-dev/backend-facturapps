from datetime import datetime
import json
import os
from xhtml2pdf import pisa

from invoice.models.factura import Factura
from invoice.utils.time_suzdal import second_suzdal
from mysite import settings
from ..utils.util_suzdal import factura_new_article, factura_new_lines, json_suzdal, user_auth

def pdf_work(request, action, id):
    auth_status, company = user_auth(request, None)
    if auth_status is None or company is None:
        return json_suzdal({'login': False, 'status':'error', 'message':'Usuario no esta logeado'})
    
    facturaObj = Factura.objects.get(id=id, company_id=company['id'])
    print(facturaObj.id)

    current_time = datetime.now()
    year  = str(current_time.strftime('%Y'))
    month = str(current_time.strftime('%m'))
    folder_path = os.path.join(settings.STATICFILES_DIRS[0], str(company['id']), year, month)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    seconds = second_suzdal()
    file_name = f"factura_{facturaObj.serie_fact}_{seconds}.pdf"
    file_path = os.path.join(folder_path, file_name)

    with open('static/f.html', 'r') as file:
        html = file.read()
    print(html)

    with open(file_path, "wb") as pdf_file:
        # Convertir el HTML a PDF y guardarlo en el archivo
        pisa_status = pisa.CreatePDF(html, dest=pdf_file)

    file_path = file_path.split('static')
    print(file_path[1])

    rdata = {
            'status': 'ok',
            'message': 'PDF creado',
            'url':'static'+file_path[1],
            'id':id
    }
         
    
    return json_suzdal(rdata)