from invoice.models.article import Article
from invoice.models.company import Company
from invoice.models.customer import Customer
from invoice.models.document import Document
from invoice.models.factura import Factura
from invoice.utils.time_suzdal import current_date, wr_invoice_in_thread, wr_invoice_to_file
from mysite import settings
from ..utils.util_suzdal import factura_new_article, factura_new_lines, json_suzdal, user_auth
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
            factura.serie_fact            = f"{tipo_factura}-{ejercicio}-{factura.numero}"
            factura.serie_fact_unique     = f"{tipo_factura}-{ejercicio}-{factura.numero}-{company['id']}"
            factura.fecha_expedicion      = current_date()
            
            factura.customer_id           = customer.id
            factura.customer_num          = customer.clientcode
            factura.receptor_company_name = customer.razon

            SUBTOTAL_FACTURA = 0
            IMP_IVAS_FACTURA = 0
            TOTAL_FACTURA    = 0
            LINEAS_FACTURA   = []

            # Base Imponible = Precio del artículo × Cantidad de artículos
            for linea in lineas:
                print("---------------------------------------------------------------------------------")
                description = str(linea.get('description', 'none')).strip()
                idArticle1  = str(linea.get('idArticle1', '')).strip()
                precio1     = float(linea.get('precio1', 0))
                cantidad1   = float(linea.get('cantidad1', 0))
                descPorc    = float(linea.get('descPorc', 0))
                ivaPorcent  = float(linea.get('ivaPorcent', 0))
                ivaTypeStr     = str(linea.get('ivaType', '0'))

                if idArticle1.isdigit():  # Comprobar si es un número válido
                    articulo_current = Article.objects.filter(id=idArticle1, company_id=company['id']).first()
                else:
                    art_created, articulo_current = factura_new_article(description, company['id'], precio1, ivaTypeStr, ivaPorcent)
                    if art_created is None or articulo_current is None:
                        return json_suzdal({'status':'error', 'message':'Error al crear arículo nuevo'})

                importe_inicio        = cantidad1 * precio1
                valor_descuento       = descPorc / 100 * importe_inicio
                importe_con_descuento = importe_inicio - valor_descuento
                SUBTOTAL_FACTURA     += importe_con_descuento
                valor_iva             = ivaPorcent / 100 * importe_con_descuento
                IMP_IVAS_FACTURA      += valor_iva
                importe_final         = importe_con_descuento + valor_iva
                TOTAL_FACTURA        += importe_final

                print(str(importe_inicio)+" "+str(valor_descuento)+" "+str(importe_con_descuento)+" "+str(valor_iva)+" importe_final="+str(importe_final))
                for d in desglose:
                    if str(d['iva']) == ivaTypeStr:
                        d['base_imponible'] += importe_con_descuento
                        d['valor_iva'] += valor_iva
                        d['total_con_iva'] += d['base_imponible'] + d['valor_iva']
                
                linea_factura = {'invoice_id':0, 'serie': '', 'company_id':company['id'], 'article_id':articulo_current.id, 'article_num':articulo_current.artcode, 'article_name':articulo_current.description, 'cantidad':cantidad1, 'precio':precio1, 'descuento':descPorc, 'iva_porcent':ivaPorcent, 'iva_type':ivaTypeStr}
                LINEAS_FACTURA.append(linea_factura)

            # ahora el calculo de mano de obra
            canridadManoObra = float(data['manoObra']['canridadManoObra'])
            precioManoObra   = float(data['manoObra']['precioManoObra'])
            descManoObr      = float(data['manoObra']['descManoObr'])
            valorIvaManoObra = float(data['manoObra']['valorIvaManoObra'])
            tipoIvaManoObra  = str(data['manoObra']['tipoIvaManoObra'])

            # cuando existe mano de obra
            if canridadManoObra > 0 and precioManoObra > 0:
                importe_inicio_mo        = canridadManoObra * precioManoObra
                valor_descuento_mo       = descManoObr / 100 * importe_inicio_mo
                importe_con_descuento_mo = importe_inicio_mo - valor_descuento_mo
                SUBTOTAL_FACTURA        += importe_con_descuento_mo
                valor_iva_mo             = valorIvaManoObra / 100 * importe_con_descuento_mo
                IMP_IVAS_FACTURA         += valor_iva_mo
                importe_final_mo         = importe_con_descuento_mo + valor_iva_mo
                TOTAL_FACTURA           += importe_final_mo

                for d in desglose:
                    if str(d['iva']) == tipoIvaManoObra:
                        d['valor'] += valor_iva_mo

            factura.ivas_desglose = json.dumps(desglose)
            factura.subtotal      = SUBTOTAL_FACTURA
            factura.importe_ivas  = IMP_IVAS_FACTURA
            factura.total         = TOTAL_FACTURA
            factura.total2        = SUBTOTAL_FACTURA + IMP_IVAS_FACTURA
            factura.save()
            
            # pongo a las lineas de iva ID de la factura
            for linea_fac in LINEAS_FACTURA:
                linea_fac['invoice_id'] = factura.id
                linea_fac['serie']      = factura.serie_fact_unique

            linea_creada = factura_new_lines(LINEAS_FACTURA)
            # if linea_creada == 0: x = 11 / 0

            print(desglose)
            print(len(factura.ivas_desglose))
            
            if factura.id > 0:
                pass
            else:
                return json_suzdal({'status':'error', 'message':'Fallo al crear factura'})
        except Exception as e:
            if factura is not None:
                factura.delete()
            print('suzdal '+str(e))    
            return json_suzdal({'status':'error', 'message':str(e)})
        

        factura   = data.get('factura', {})
        print(factura)    
              
        rdata = {
            'status': 'ok',
            'message': 'Factura creada '
        }
         
    
        return json_suzdal(rdata)
       