from invoice.models.company import Company
from ..utils.util_suzdal import json_suzdal, user_auth


def default_actions(request, action, entity, id):
    if user_auth(request) == False:
        return json_suzdal({'login': False})

    if action == 'get' and entity == 'factura':
        
        rdata = {
            'action': action,
            'entity': entity,
            'id': id,
        }
    
    
    return json_suzdal({'action': action,'entity': entity,'id': id,})
  