from invoice.models.article import Article
from invoice.models.company import Company
from invoice.models.customer import Customer
from invoice.models.document import Document
from invoice.models.factura import Factura
from invoice.utils.time_suzdal import current_date, wr_invoice_in_thread, wr_invoice_to_file
from mysite import settings
from ..utils.util_suzdal import factura_new_article, json_suzdal, user_auth
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

        desglose     = data['desglose']
        ejercicio    = str(datetime.now().strftime('%Y')).strip()
        tipo_factura = str(data['factura']['selectTypeInvoice']).strip()
        lineas       = data['lineas']
        if len(lineas) == 0:
             return json_suzdal({'status':'error', 'message':'Factura sin lineas'})

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
            factura.receptor_pais         = customer.country
            factura.receptor_zip_code     = customer.zipcode
            factura.receptor_city         = customer.city
            factura.receptor_address      = customer.address

            factura.emisor_cif            = company['cif']
            factura.emisor_company_name   = company['razon']
            factura.emisor_person_name    = company['person_name']
            factura.emisor_pais           = company['country']
            factura.emisor_zip_code       = company['zipcode']
            factura.emisor_provice        = company['province']
            factura.emisor_city           = company['city']
            factura.emisor_address        = company['address']

            

            # Base Imponible = Precio del artículo × Cantidad de artículos
            for linea in lineas:
                print("---------------------------------------------------------------------------------")
                description = str(linea.get('description', 'none')).strip()
                idArticle1  = str(linea.get('idArticle1', '')).strip()
                precio1     = float(linea.get('precio1', 0))
                cantidad1   = float(linea.get('cantidad1', 0))
                descPorc    = float(linea.get('descPorc', 0))
                ivaPorcent  = float(linea.get('ivaPorcent', 0))
                ivaType     = str(linea.get('ivaType', '0'))

                if idArticle1.isdigit():  # Comprobar si es un número válido
                    articulo_current = Article.objects.filter(id=idArticle1, company_id=company['id']).first()
                else:
                    art_created, articulo_current = factura_new_article(description, company['id'], precio1, ivaType, ivaPorcent)
                    if art_created is None or articulo_current is None:
                        return json_suzdal({'status':'error', 'message':'Error al crear arículo nuevo'})

                importe_inicio        = cantidad1 * precio1
                valor_descuento       = descPorc / 100 * importe_inicio
                importe_con_descuento = importe_inicio - valor_descuento
                valor_iva             = ivaPorcent / 100 * importe_con_descuento
                importe_final         = importe_con_descuento + valor_iva

                print(str(importe_inicio)+" "+str(valor_descuento)+" "+str(importe_con_descuento)+" "+str(valor_iva)+" importe_final="+str(importe_final))
                for d in desglose:
                    if str(d['iva']) == ivaType:
                        d['valor'] += valor_iva

            # ahora el calculo de mano de obra
            canridadManoObra = data['manoObra']['canridadManoObra']
            precioManoObra   = data['manoObra']['precioManoObra']
            descManoObr      = data['manoObra']['descManoObr']
            valorIvaManoObra = data['manoObra']['valorIvaManoObra']
            tipoIvaManoObra  = data['manoObra']['tipoIvaManoObra']


            factura.save()
            
            print(desglose)
            
            if factura.id > 0:
                pass
            else:
                return json_suzdal({'status':'error', 'message':'Fallo al crear factura'})
        except Exception as e:
            if factura is not None:
                factura.delete()
            print('suzdal '+str(e))    
            return json_suzdal({'status':'error', 'message':str(e)})
        

        lineas    = data.get('lineas', [])
        mano_obra = data.get('manoObra', {})
        factura   = data.get('factura', {})
        print(factura)    
              
        rdata = {
            'status': 'ok',
            'message': 'Factura creada '
        }
         
    
        return json_suzdal(rdata)
       