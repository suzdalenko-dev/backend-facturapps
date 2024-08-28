from invoice.models.company import Company
from ..utils.util_suzdal import json_suzdal

def invoice_actions(request, action, id):
    
        rdata = {
            'id': "company.id",
            'uid': action,
            'status': id,
        }

        res = json_suzdal(rdata)
        return res