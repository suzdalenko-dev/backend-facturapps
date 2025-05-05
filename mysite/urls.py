from django.contrib import admin
from django.urls import path

from invoice.controllers import login_controller, registrer_controller, invoice_controller, default_controller, pdf_controller, report_controller, parse

urlpatterns = [
   path('register/', registrer_controller.try_register ),
   path('login/', login_controller.try_login),
   path('invoice/<str:action>/<int:id>', invoice_controller.invoice_actions),
   path('default/<str:action>/<str:entity>/<int:id>', default_controller.default_actions),
   path('pdf/<str:action>/<int:id>', pdf_controller.pdf_work ),
   path('report/users/', report_controller.default_report ),
   path('reports/get/<str:current_entity>', report_controller.entity_report ),
   
   
   path('parse/<str:id>', parse.parse_work),
]
