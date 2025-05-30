from django.contrib.auth.hashers import check_password
from email import encoders
from email.mime.base import MIMEBase
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from decimal import Decimal
import threading
import time
from django.http import JsonResponse
from invoice.models.article import Article
from invoice.models.company import Company
from invoice.models.customer import Customer
from invoice.models.document import Document
from invoice.models.facturalineas import Facturalineas


def json_suzdal(response_data):
    response = JsonResponse(response_data)

    # Set CORS headers
    response['Access-Control-Allow-Origin'] = '*'
    response['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS, PUT, DELETE'
    response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With'
    return response



def user_auth(request, data):
    if data is None:
        company_id = str(request.POST.get('company_id')).strip()
        cif        = str(request.POST.get('cif')).strip()
        email      = str(request.POST.get('email')).strip()
        uid        = str(request.POST.get('uid')).strip()
        password   = str(request.POST.get('password')).strip()
    else:
        company_id = str(data['credentials']['company_id']).strip()
        cif        = str(data['credentials']['cif']).strip()
        email      = str(data['credentials']['email']).strip()
        uid        = str(data['credentials']['uid']).strip()
        password   = str(data['credentials']['password']).strip()

    try:
        company = Company.objects.filter(id=company_id).values('id', 'razon', 'cif', 'person_name', 'email', 'emailcompany', 'uid', 'password', 'tlf', 'tlf2', 'country', 'city', 'zipcode', 'province', 'address', 'price').first()
        
        if company['uid'] == uid and check_password(password, company['password']):
            company['password'] = None
            company['uid'] = None
            return [True, company]
        else: 
            return [None, None]
    except Exception as e:
        
        return [None, None]
    


def update_company_data(request):
    company_id = request.POST.get('company_id')
    try:
        c = Company.objects.get(id=company_id)
        c.razon        = str(request.POST.get('razon')).strip()
        c.person_name  = str(request.POST.get('person_name')).strip()
        c.emailcompany = str(request.POST.get('emailcompany')).strip()
        c.country      = str(request.POST.get('country')).strip()
        c.province     = str(request.POST.get('province')).strip()
        c.zipcode      = str(request.POST.get('zipcode')).strip()
        c.city         = str(request.POST.get('city')).strip()
        c.address      = str(request.POST.get('address')).strip()
        c.tlf          = str(request.POST.get('tlf')).strip()
        c.tlf2         = str(request.POST.get('tlf2')).strip()
        c.price        = str(request.POST.get('price')).strip().replace(',', '.')
        c.save()                                                                                                    
        c = Company.objects.filter(id=company_id).values('id', 'razon', 'cif', 'person_name', 'email', 'emailcompany', 'tlf', 'tlf2', 'country', 'city', 'zipcode', 'province', 'address', 'price').first()
        return [True, c]
    except Exception as e:
        return None


def create_new_article(request):
    description = str(request.POST.get('description')).strip()
    price       = str(request.POST.get('price')).replace(',', '.')
    iva         = str(request.POST.get('iva')).replace(',', '.')   
    ivatype     = str(request.POST.get('ivatype')).strip()
    company_id  = int(request.POST.get('company_id'))
    article     = None
    try:
        article  = Article.objects.create(description=description, company_id=company_id, price=price, ivatype=ivatype, iva=iva)
        document = Document.objects.filter(company_id=company_id, description= 'articulo_numero').values('value').first() 
        article.artcode = document['value']
        article.save()
        if article.id > 0:
            return True
        else:
            return None
    except Exception as e:
        if article is not None:
            article.delete()
        return None
    


def create_new_customer(request):
    company_id    = int(request.POST.get('company_id'))
    cif_nif       = str(request.POST.get('cif_nif')).strip()
    razon         = str(request.POST.get('razon')).strip()
    person_name   = str(request.POST.get('person_name')).strip()
    emailcustomer = str(request.POST.get('emailcustomer')).strip()
    phone         = str(request.POST.get('phone')).strip()
    country       = str(request.POST.get('country')).strip()
    province      = str(request.POST.get('province')).strip()
    zipcode       = str(request.POST.get('zipcode')).strip()
    city          = str(request.POST.get('city')).strip()
    address       = str(request.POST.get('address')).strip()
    customer      = None
    try:
        customer = Customer.objects.create(cif_nif=cif_nif, company_id=company_id, razon=razon, person_name=person_name, emailcustomer=emailcustomer, phone=phone, country=country, province=province, zipcode=zipcode, city=city, address=address)
        document = Document.objects.filter(company_id=company_id, description= 'cliente_numero').values('value').first()
        customer.clientcode = document['value']
        customer.save()
        if customer.id > 0:
            return True
        else:
            return None
    except Exception as e:
        customer.delete()
        return None
    

def upgrade_existing_customer(request, id):
    company_id    = int(request.POST.get('company_id'))
    try:
        customer               = Customer.objects.get(id=id, company_id=company_id)
        customer.cif_nif       = str(request.POST.get('cif_nif')).strip()
        customer.razon         = str(request.POST.get('razon')).strip()
        customer.person_name   = str(request.POST.get('person_name')).strip()
        customer.emailcustomer = str(request.POST.get('emailcustomer')).strip()
        customer.phone         = str(request.POST.get('phone')).strip()
        customer.country       = str(request.POST.get('country')).strip()
        customer.province      = str(request.POST.get('province')).strip()
        customer.zipcode       = str(request.POST.get('zipcode')).strip()
        customer.city          = str(request.POST.get('city')).strip()
        customer.address       = str(request.POST.get('address')).strip()
        customer.save()
        if customer.id > 0:
            return True
        else:
            return None
    except Exception as e:
        return None
    


def update_old_article(request, id):
    company_id  = int(request.POST.get('company_id'))
    try:
        article  = Article.objects.get(id=id, company_id=company_id)   
        article.description = str(request.POST.get('description')).strip()
        article.price       = str(request.POST.get('price')).replace(',', '.')
        article.iva         = str(request.POST.get('iva')).replace(',', '.')   
        article.ivatype     = str(request.POST.get('ivatype')).strip()
        article.save()
        if article.id > 0:
            return True
        else:
            return None
    except Exception as e:
        return None
    


def factura_new_article(description, company_id, precio1, ivaType, ivaPorcent):
    if ivaType == '0EXENTO':
        ivaType = 'exento'
    else:
        ivaType = 'norm'
 
    try:
        article  = Article.objects.create(description=description, company_id=company_id, price=precio1, ivatype=ivaType, iva=ivaPorcent)
        document = Document.objects.filter(company_id=company_id, description= 'articulo_numero').values('value').first() 
        article.artcode = document['value']
        article.save()
        if article.id > 0:
            return [True, article]
        else:
            return [None, None]
    except Exception as e:
        if article is not None:
            article.delete()
        return [None, None]
    


def factura_new_lines(lineas_factura):
    for linea in lineas_factura:
        tipo_iva_string = 'norm'
        if linea['iva_type'] == '0EXENTO':
            tipo_iva_string = 'exento'
        try:
            linea_factura = Facturalineas.objects.create(invoice_id=linea['invoice_id'], company_id=linea['company_id'], serie=linea['serie'])
            linea_factura.article_id   = linea['article_id']
            linea_factura.article_num  = linea['article_num']
            linea_factura.article_name = linea['article_name']
            
            linea_factura.cantidad      = linea['cantidad']
            linea_factura.precio        = linea['precio']
            linea_factura.importe_bruto = linea_factura.cantidad *  linea_factura.precio

            linea_factura.descuento             = linea['descuento']
            linea_factura.descuento_val         = linea_factura.descuento / 100 * linea_factura.importe_bruto
            linea_factura.importe_con_descuento = linea_factura.importe_bruto -  linea_factura.descuento_val

            linea_factura.iva_porcent   = linea['iva_porcent']
            linea_factura.iva_valor     = linea_factura.iva_porcent / 100 * linea_factura.importe_con_descuento
            linea_factura.importe_res   = linea_factura.importe_con_descuento + linea_factura.iva_valor 

            linea_factura.iva_type      = tipo_iva_string
            linea_factura.save()
        except Exception as e:
            pass



def enviar_correo(url_email, invoice_name, user_email):
    try:
        # Crea la estructura del mensaje
        msg = MIMEMultipart()
        msg['From'] = "simplefactura2024@gmail.com"
        msg['To'] = user_email
        msg['Subject'] = invoice_name
        html_message = f'''<div style="background-color:#395fce;color:white;font-family:Roboto, RobotoDraft, Helvetica, Arial, sans-serif; border-radius:17px;">
                                <div style="padding:11px;">
                                    <h2>{invoice_name}</h2><br><a style="color:white;" href="https://factura-simple-on.web.app/" target="_blank">Factura Simple App</a><br>
                                </div>
                        <div>'''

        # Cuerpo del mensaje
        msg.attach(MIMEText(html_message, 'html'))  # Usa 'html' si deseas enviar contenido HTML

        if os.path.isfile(url_email):
            with open(url_email, 'rb') as archivo:
               parte_adjunto = MIMEBase('application', 'octet-stream')
               parte_adjunto.set_payload(archivo.read())
            encoders.encode_base64(parte_adjunto)
            filename = os.path.basename(url_email)
            parte_adjunto.add_header('Content-Disposition',f'attachment; filename={filename}',)
            msg.attach(parte_adjunto)

        # Configuración del servidor SMTP (Gmail en este caso)
        servidor = smtplib.SMTP('smtp.gmail.com', 587)
        servidor.starttls()  # Activa la seguridad TLS
        servidor.login("simplefactura2024@gmail.com", "qgij ftlb pijq xulp")  # Autenticación

        # Envía el correo
        servidor.sendmail("simplefactura2024@gmail.com", user_email, msg.as_string())
        servidor.quit()  # Cierra la conexión

    except Exception as e:
        pass


# Function to start the thread
def start_deletion_thread(folder_path):
    deletion_thread = threading.Thread(target=delete_files_after_delay, args=(folder_path,))
    deletion_thread.daemon = True
    deletion_thread.start()

# Function to delete all files in the folder after waiting for 22 minutes
def delete_files_after_delay(folder_path):
    # Wait for 1 minutes
    time.sleep(2 * 60)  # 1 minutes converted to seconds
    # Iterate over files in the directory
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename) 
        # Check if it's a file (not a sub-directory)
        if os.path.isfile(file_path):
            os.remove(file_path)