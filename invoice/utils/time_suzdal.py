from datetime import datetime, timedelta
import json
import os
import threading
import time

from mysite import settings

def time_suzdal():
    current_time = datetime.now()
    formatted_time = str(current_time.strftime('%Y-%m-%d %H:%M:%S'))
    return formatted_time


def current_date():
    current_time = datetime.now()
    formatted_time = str(current_time.strftime('%d/%m/%Y'))
    return formatted_time


def second_suzdal():
    current_time_seconds = int(time.time())
    return current_time_seconds

def creating_invoice_time():
    current_time = datetime.now()
    formatted_time = str(current_time.strftime('%Y-%m-%d_%H-%M-%S'))
    return formatted_time


def wr_invoice_in_thread(data, factura_serie, cif_customer):
    thread = threading.Thread(target=wr_invoice_to_file, args=(data, factura_serie, cif_customer))
    thread.daemon = True
    thread.start()



def wr_invoice_to_file(data, factura_serie, cif_customer):
    company_id   = data['credentials']['company_id']
    current_time = datetime.now()
    year  = str(current_time.strftime('%Y'))
    folder_path = os.path.join(settings.BASE_DIR, 'media', str(company_id), year)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
  
    file_name = f"{factura_serie}_{cif_customer}.json"
    file_path = os.path.join(folder_path, file_name)
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)


def get_time_11days():
    current_date = datetime.now()
    new_date = current_date + timedelta(days=11)
    new_date_formatted = new_date.strftime('%d/%m/%Y')
    return new_date_formatted