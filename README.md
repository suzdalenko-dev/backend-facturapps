###### Puedes usar el siguiente comando para revertir las migraciones de estas aplicaciones:
python manage.py migrate auth zero
python manage.py migrate admin zero
python manage.py migrate contenttypes zero
python manage.py migrate sessions zero
###### 
###### Si aún no tienes una aplicación donde quieras poner tu modelo de usuario, crea una nueva. Supongamos que la llamas invoice_app
###### python manage.py startapp invoice
###### 
######

