from datetime import datetime
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



def wr_invoice_in_thread(data):
    thread = threading.Thread(target=wr_invoice_to_file, args=(data,))
    thread.daemon = True
    thread.start()



def wr_invoice_to_file(data):
    company_id   = data['credentials']['company_id']
    current_time = datetime.now()
    year  = current_time.strftime('%Y')
    month = current_time.strftime('%m')
    day   = current_time.strftime('%d')
    folder_path = os.path.join(settings.STATICFILES_DIRS[0], company_id, year, month)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    # file_name = f"data_{current_time.strftime('%Y-%m-%d_%H-%M-%S')}.json"
    file_name = f"data_{current_time.strftime('%Y-%m')}.json"
    file_path = os.path.join(folder_path, file_name)
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)
