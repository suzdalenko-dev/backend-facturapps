from invoice.models.company import Company
from invoice.models.customer import Customer
from invoice.models.document import Document
from invoice.models.factura import Factura
from invoice.utils.time_suzdal import current_date, wr_invoice_in_thread, wr_invoice_to_file
from mysite import settings
from ..utils.util_suzdal import json_suzdal, user_auth
import json, os
from datetime import datetime

# http://127.0.0.1:8000/static/1/2024/09/07/data_2024-09-07_14-02-51.json
def invoice_actions(request, action, id):
        if request.body:
            try:
                data = json.loads(request.body.decode('utf-8'))
            except json.JSONDecodeError:
                return json_suzdal({'status': 'error', 'message': 'Cuerpo de la solicitud no es JSON válido'})
        else:
            return json_suzdal({'status': 'error', 'message': 'Cuerpo de la solicitud vacío'})
        
        auth_status, company = user_auth(request, data)
        if auth_status is None or company is None:
            return json_suzdal({'login': False, 'status':'error', 'message':'Usuario no esta logeado'})
            
        try:
            wr_invoice_in_thread(data)
        except Exception as e:
            pass

        ejercicio    = str(datetime.now().strftime('%Y')).strip()
        tipo_factura = str(data['factura']['selectTypeInvoice']).strip()
        

        try:
            customer = Customer.objects.get(id=data['cliente']['clientIdDeveloper'], clientcode=data['cliente']['clientNumber'], company_id=company['id'])
            factura  = Factura.objects.create(company_id=company['id'], tipo_factura=tipo_factura, ejercicio=ejercicio)
            document = Document.objects.filter(company_id=company['id'], description=tipo_factura, ejercicio=ejercicio).values('value').first() 
            factura.numero                = document['value']
            factura.serie_fact            = f"{tipo_factura}/{ejercicio}/{factura.numero}"
            factura.serie_fact_unique     = f"{tipo_factura}/{ejercicio}/{factura.numero}/{company['id']}"
            factura.fecha_expedicion      = current_date()
            factura.customer_id           = customer.id
            factura.receptor_cif          = customer.cif_nif
            factura.receptor_company_name = customer.razon
            factura.receptor_person_name  = customer.person_name


            factura.save()
            if factura.id > 0:
                pass
            else:
                return json_suzdal({'status':'error', 'message':'Fallo al crear factura'})
        except Exception as e:
            if factura is not None:
                factura.delete()
            return json_suzdal({'status':'error', 'message':str(e)})
        

        lineas    = data.get('lineas', [])
        mano_obra = data.get('manoObra', {})
        factura   = data.get('factura', {})
             
              
        rdata = {
            'status': 'ok',
            'message': 'Factura creada '
        }
         
    
        return json_suzdal(rdata)
       