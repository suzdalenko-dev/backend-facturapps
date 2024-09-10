from datetime import datetime
import json
import os
from xhtml2pdf import pisa

from invoice.models.customer import Customer
from invoice.models.factura import Factura
from invoice.utils.time_suzdal import second_suzdal
from mysite import settings
from ..utils.util_suzdal import factura_new_article, factura_new_lines, json_suzdal, user_auth

def pdf_work(request, action, id):
    try:
        auth_status, company = user_auth(request, None)
        if auth_status is None or company is None:
            return json_suzdal({'login': False, 'status':'error', 'message':'Usuario no esta logeado'})
    
        facturaObj  = Factura.objects.get(id=id, company_id=company['id'])
        customerObj = Customer.objects.get(id=facturaObj.customer_id, company_id=company['id'])

        current_time = datetime.now()
        year  = str(current_time.strftime('%Y'))
        month = str(current_time.strftime('%m'))
        folder_path = f"static/{str(company['id'])}/{year}/{month}/"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        seconds = second_suzdal()
        file_name = f"factura_{facturaObj.serie_fact}.pdf" # file_name = f"factura_{facturaObj.serie_fact}_{seconds}.pdf"
        file_path = folder_path+file_name

        with open('static/f.html', 'r') as file:
            html = file.read()
    
        html = html.replace('@numero_factura@', str(facturaObj.serie_fact))
        html = html.replace('@fecha_factura@', str(facturaObj.fecha_expedicion))
        html = html.replace('@fecha_vencimiento@', str(facturaObj.vencimiento))
        tipo_factura = ''
        if facturaObj.tipo_factura == 'R': tipo_factura = 'RECTIFICATIVA'
        if facturaObj.tipo_factura == 'A': tipo_factura = 'ABONO'
        html = html.replace('@tipo_factura@', tipo_factura)
        html = html.replace('@razon@', company['razon'])
        html = html.replace('@person_name@', company['person_name'])
        html = html.replace('@province@', company['province'])
        html = html.replace('@city@', company['city'])
        html = html.replace('@zipcode@', company['zipcode'])
        html = html.replace('@address@', company['address'])
        html = html.replace('@cif@', company['cif'])
        html = html.replace('@tlf@', company['tlf'])
        
        html = html.replace('@customer_num@', str(facturaObj.customer_num))
        html = html.replace('@razon_cl@', customerObj.razon)
        html = html.replace('@person_name_cl@', customerObj.person_name)
        html = html.replace('@province_cl@', customerObj.province)
        html = html.replace('@city_cl@', customerObj.city)
        html = html.replace('@zipcode_cl@', customerObj.zipcode)
        html = html.replace('@address_cl@', customerObj.address)
        html = html.replace('@cif_nif@', customerObj.cif_nif)
        html = html.replace('@phone@', customerObj.phone)
        html = html.replace('@country@', customerObj.country)
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
    
    except Exception as e:
        return json_suzdal({'message': str(e), 'status': 'error'})