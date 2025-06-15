BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "django_migrations" (
	"id"	integer NOT NULL,
	"app"	varchar(255) NOT NULL,
	"name"	varchar(255) NOT NULL,
	"applied"	datetime NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "invoice_article" (
	"id"	integer NOT NULL,
	"company_id"	bigint,
	"artcode"	bigint unsigned NOT NULL CHECK("artcode" >= 0),
	"description"	varchar(254),
	"price"	decimal,
	"iva"	decimal,
	"ivatype"	varchar(11),
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "invoice_company" (
	"id"	integer NOT NULL,
	"razon"	varchar(111),
	"person_name"	varchar(111),
	"cif"	varchar(33) UNIQUE,
	"emailcompany"	varchar(111),
	"password"	varchar(222),
	"tlf"	varchar(33),
	"tlf2"	varchar(33),
	"numvisit"	bigint NOT NULL,
	"regtime"	varchar(33),
	"lastvisit"	varchar(33),
	"uid"	varchar(111),
	"country"	varchar(33),
	"province"	varchar(33),
	"zipcode"	varchar(22),
	"city"	varchar(33),
	"address"	varchar(111),
	"price"	decimal NOT NULL,
	"email"	varchar(111) UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "invoice_country" (
	"id"	integer NOT NULL,
	"description"	varchar(33) UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "invoice_customer" (
	"id"	integer NOT NULL,
	"company_id"	bigint,
	"clientcode"	bigint unsigned NOT NULL CHECK("clientcode" >= 0),
	"cif_nif"	varchar(33),
	"razon"	varchar(255),
	"person_name"	varchar(255),
	"emailcustomer"	varchar(111),
	"phone"	varchar(33),
	"country"	varchar(111) NOT NULL,
	"province"	varchar(111),
	"zipcode"	varchar(11),
	"city"	varchar(111),
	"address"	varchar(255),
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "invoice_document" (
	"id"	integer NOT NULL,
	"description"	varchar(41),
	"value"	integer unsigned NOT NULL CHECK("value" >= 0),
	"ejercicio"	varchar(7),
	"company_id"	bigint,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "invoice_factura" (
	"id"	integer NOT NULL,
	"company_id"	bigint,
	"ejercicio"	varchar(7),
	"serie_fact"	varchar(22),
	"numero"	bigint,
	"serie_fact_unique"	varchar(22) UNIQUE,
	"customer_id"	bigint,
	"customer_num"	bigint,
	"receptor_company_name"	varchar(222),
	"fecha_expedicion"	varchar(33),
	"vencimiento"	varchar(33),
	"ivas_desglose"	varchar(1000),
	"importe_ivas"	decimal NOT NULL,
	"subtotal"	decimal NOT NULL,
	"total"	decimal NOT NULL,
	"total2"	decimal NOT NULL,
	"observacion"	varchar(254),
	"apunta_factura"	varchar(40),
	"name_factura"	varchar(40),
	"tipo_factura"	varchar(3),
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "invoice_facturalineas" (
	"id"	integer NOT NULL,
	"invoice_id"	bigint,
	"company_id"	bigint,
	"serie"	varchar(22),
	"article_id"	bigint,
	"article_num"	bigint,
	"article_name"	varchar(254),
	"cantidad"	decimal,
	"precio"	decimal,
	"importe_bruto"	decimal,
	"descuento"	decimal,
	"descuento_val"	decimal,
	"importe_con_descuento"	decimal,
	"iva_porcent"	decimal,
	"iva_valor"	decimal,
	"importe_res"	decimal,
	"iva_type"	varchar(11),
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "invoice_vehicledata" (
	"id"	integer NOT NULL,
	"invoice_id"	bigint,
	"company_id"	bigint,
	"customer_id"	bigint,
	"matricula"	varchar(22),
	"other_data"	varchar(254),
	PRIMARY KEY("id" AUTOINCREMENT)
);
INSERT INTO "django_migrations" VALUES (1,'invoice','0001_initial','2025-05-03 16:33:41.441133');
INSERT INTO "django_migrations" VALUES (2,'invoice','0002_alter_factura_tipo_factura','2025-05-03 16:33:41.503355');
INSERT INTO "django_migrations" VALUES (3,'invoice','0003_factura_name_factura_alter_factura_apunta_factura_and_more','2025-05-03 16:33:41.556636');
INSERT INTO "django_migrations" VALUES (4,'invoice','0004_alter_company_email','2025-05-03 16:43:36.768644');
INSERT INTO "django_migrations" VALUES (5,'invoice','0005_alter_company_password','2025-05-03 16:47:48.524491');
INSERT INTO "django_migrations" VALUES (6,'invoice','0006_alter_company_email','2025-05-03 16:52:08.795215');
INSERT INTO "invoice_article" VALUES (2,6,1,'Desarrollo App Personalizada',1000,21,'norm');
INSERT INTO "invoice_article" VALUES (3,6,2,'Informe Power BI',3000,21,'norm');
INSERT INTO "invoice_article" VALUES (4,6,3,'Configuracion Servidor',30,21,'norm');
INSERT INTO "invoice_article" VALUES (5,6,4,'Desarrollo API personalizada',1000,21,'norm');
INSERT INTO "invoice_article" VALUES (6,9,1,'Desarrollo Portal Empleado',1000,21,'norm');
INSERT INTO "invoice_article" VALUES (7,7,1,'Portal del Empleado',1000,21,'norm');
INSERT INTO "invoice_article" VALUES (8,7,2,'Aplicación de Fichaje Horario Laboral',2100,21,'norm');
INSERT INTO "invoice_article" VALUES (9,7,3,'Mejora de la presencia de la web general',1310.41,21,'norm');
INSERT INTO "invoice_company" VALUES (3,NULL,NULL,'A123456789',NULL,'pbkdf2_sha256$870000$1TZGUFJo7gsd9nUVZVXbdp$4hspTk9qFa4Ncz+9isyDEbPlyWhYuy3yrn29L/jWv60=','123123',NULL,4,'2025-05-03 18:52:40','2025-05-03 19:00:52','1746291160',NULL,NULL,NULL,NULL,NULL,0,'suz@gmail.com');
INSERT INTO "invoice_company" VALUES (4,'123','123','CIFa','123','pbkdf2_sha256$870000$fvbLPKMpmKGiezx2MoN1wP$Yox3vuhPhVa+omFt0/5RN8DmPMYRcItiHiJIB7VA2w0=','1234554545','123',13,'2025-05-03 19:21:23','2025-05-04 13:26:06','1746292883','123','123','123','123','123',123,'s@gmail.com');
INSERT INTO "invoice_company" VALUES (5,'Suzdalenko Alexey','Suzdalenko Alexey','sdfsdfsdfsdf','Suzdalenko Alexey','pbkdf2_sha256$870000$nVytUvGewTavOpdGaZ43Pn$fzanZZeeUJ1EJ+YcBrbCwkCmwZlDDE82eRBzSsk5/VM=','657666135','942564160',3,'2025-05-04 22:02:12','2025-05-04 22:09:00','1746388932','España','Cantabria','039684','Santander','Calle Alcala 11',40,'x420x@gmail.com');
INSERT INTO "invoice_company" VALUES (6,'Factura App SLNE','Suzdalenko Alexey','A123456','alexey.suzdalenko@gmail.com','pbkdf2_sha256$320000$nfLl3BSFgAkdlk8DhoMbI0$GFJKVhN6DvcGfGohVxZEzAG7p2JtvFZ0JFdOqrmRJtI=','+34657666135','+34657666135',8,'2025-05-05 10:22:50','2025-05-09 17:01:07','1746440570','España','Cantabria','39694','Santa Maria de Cayon','El Traguezo 66',22,'alexey.suzdalenko@gmail.com');
INSERT INTO "invoice_company" VALUES (7,'Desarrollo Suzdalenko','Alexey Suzdalenko','X4207693G','alexey@gmail.com','pbkdf2_sha256$320000$x7eBVJbSODFazWXQebkvPL$oUL5ls/kr7tS9zYTBDTV0Y7MReS3kxV2+ROV11qK2wc=','+34657666135','942 56 41 60',10,'2025-05-31 14:24:07','2025-06-15 19:31:13','1748701447','España','Cantabria','39694','Santa Maria de Cayon','El Traguezo 66',22.5,'alexey@gmail.com');
INSERT INTO "invoice_company" VALUES (8,NULL,NULL,'X420234342',NULL,'pbkdf2_sha256$320000$iwtW5ECnQejVQNH1kf6PpP$Ba4av9LjPuo99dJ7rcROkhLEMH9mxMa2lxq6mc2VNHM=','345345',NULL,2,'2025-06-15 14:23:47','2025-06-15 14:23:56','1749997427',NULL,NULL,NULL,NULL,NULL,0,'a@gmail.com');
INSERT INTO "invoice_company" VALUES (9,'Desarrollador Web','Alexey Suzdalenko','CIF123456','a1@gmail.com','pbkdf2_sha256$320000$KtT2EN86WID3H2TpqiTQ1r$H9zaUPVfkxGsWZVLJnPda9vl/XZWaWADI54B2w5jYwo=','+34657666135','942 56 41 60',2,'2025-06-15 14:43:58','2025-06-15 14:44:03','1749998638','España','Cantabria','101010','Santander','calle Alcala 11',22,'a1@gmail.com');
INSERT INTO "invoice_company" VALUES (10,NULL,NULL,'A1234561',NULL,'pbkdf2_sha256$320000$uHibG0jf8Zs2GK864UgRid$HPU4Cioq6a9U1ryv0boMaNkKtOnbglfKzDUB0fmmvUo=','1111111111111111',NULL,2,'2025-06-15 17:46:09','2025-06-15 17:46:16','1750009569',NULL,NULL,NULL,NULL,NULL,0,'alexey@gmail1.com');
INSERT INTO "invoice_customer" VALUES (1,6,1,'IES Peñacastillo','IES Peñacastillo','IES Peñacastillo','IES@gmail.com','942 32 16 50','España','Cantabria','39011','Peñacastillo','C. Eduardo García');
INSERT INTO "invoice_customer" VALUES (2,6,2,'A12345678','Banco Santander','Pedro Romeral','banco@santander.com','942567143','España','Cantabria','39001','Santander','Calle Alcala 11');
INSERT INTO "invoice_customer" VALUES (3,9,1,'A919292994','Nestle','Roman Nestle','contact@nestle.com','9412343434','España','Cantabria','12312312','Santa Maria de Cayon','La Penilla 11');
INSERT INTO "invoice_customer" VALUES (4,7,1,'A08005449','Nestle S.A.','Peter Aronovi Nestle','contacto@nestle.com','942 11 22 44','España','Cantabria','39690','La Penilla','Calle Alcala 11');
INSERT INTO "invoice_customer" VALUES (5,7,2,'A39000013','Banco Santander S.A.','Héctor Grisi','santander_reclamaciones@gruposantander.es','915 123 123','España','Cantabria','39001','Santander','Paseo de Pereda 9-12');
INSERT INTO "invoice_customer" VALUES (6,7,3,'A39004700','PLASTICOS ESPAÑOLES SA','Armando Álvarez','fiscal@armandoalvarez.com','942 84 61 00','España','Cantabria','39300','Torrelavega','Calle Pablo Garnica 20');
INSERT INTO "invoice_document" VALUES (1,'articulo_numero',1,NULL,4);
INSERT INTO "invoice_document" VALUES (2,'articulo_numero',4,NULL,6);
INSERT INTO "invoice_document" VALUES (3,'cliente_numero',2,NULL,6);
INSERT INTO "invoice_document" VALUES (4,'O',2,'2025',6);
INSERT INTO "invoice_document" VALUES (5,'cliente_numero',1,NULL,9);
INSERT INTO "invoice_document" VALUES (6,'O',1,'2025',9);
INSERT INTO "invoice_document" VALUES (7,'articulo_numero',1,NULL,9);
INSERT INTO "invoice_document" VALUES (8,'articulo_numero',3,NULL,7);
INSERT INTO "invoice_document" VALUES (9,'cliente_numero',3,NULL,7);
INSERT INTO "invoice_document" VALUES (10,'O',2,'2025',7);
INSERT INTO "invoice_factura" VALUES (1,6,'2025','O-2025-1',1,'O-2025-1-6',1,1,'IES Peñacastillo','2025-05-05','2025-05-16','[{"iva": 21, "valor_iva": 886.2, "base_imponible": 4220.0, "total_con_iva": 11156.2, "recec": 5.2}, {"iva": 10, "valor_iva": 0, "base_imponible": 0, "total_con_iva": 0, "recec": 1.4}, {"iva": 4, "valor_iva": 0, "base_imponible": 0, "total_con_iva": 0, "recec": 0}, {"iva": 0, "valor_iva": 0, "base_imponible": 0, "total_con_iva": 0, "recec": 0}, {"iva": "0EXENTO", "valor_iva": 0, "base_imponible": 0, "total_con_iva": 0, "recec": 0}]',886.2,4220,5106.2,5106.2,'El trabajo ejecutado antes de tiempo','','FACTURA','O');
INSERT INTO "invoice_factura" VALUES (2,6,'2025','O-2025-2',2,'O-2025-2-6',1,1,'IES Peñacastillo','2025-05-09','2025-05-20','[{"iva": 21, "valor_iva": 472.5, "base_imponible": 2250.0, "total_con_iva": 7598.8, "recec": 5.2}, {"iva": 10, "valor_iva": 0, "base_imponible": 0, "total_con_iva": 0, "recec": 1.4}, {"iva": 4, "valor_iva": 0, "base_imponible": 0, "total_con_iva": 0, "recec": 0}, {"iva": 0, "valor_iva": 0, "base_imponible": 0, "total_con_iva": 0, "recec": 0}, {"iva": "0EXENTO", "valor_iva": 0, "base_imponible": 0, "total_con_iva": 0, "recec": 0}]',472.5,2250,2722.5,2722.5,'Sin','','FACTURA','O');
INSERT INTO "invoice_factura" VALUES (3,9,'2025','O-2025-1',1,'O-2025-1-9',3,1,'Nestle','2025-06-15','2025-06-26','[{"iva": 21, "valor_iva": 394.79999999999995, "base_imponible": 1880.0, "total_con_iva": 3484.8, "recec": 5.2}, {"iva": 10, "valor_iva": 0, "base_imponible": 0, "total_con_iva": 0, "recec": 1.4}, {"iva": 4, "valor_iva": 0, "base_imponible": 0, "total_con_iva": 0, "recec": 0}, {"iva": 0, "valor_iva": 0, "base_imponible": 0, "total_con_iva": 0, "recec": 0}, {"iva": "0EXENTO", "valor_iva": 0, "base_imponible": 0, "total_con_iva": 0, "recec": 0}]',394.8,1880,2274.8,2274.8,'Trabajo terminado','','FACTURA','O');
INSERT INTO "invoice_factura" VALUES (4,7,'2025','O-2025-1',1,'O-2025-1-7',6,3,'PLASTICOS ESPAÑOLES SA','2025-06-15','2025-06-26','[{"iva": 21, "valor_iva": 690.9, "base_imponible": 3290.0, "total_con_iva": 9704.2, "recec": 5.2}, {"iva": 10, "valor_iva": 0, "base_imponible": 0, "total_con_iva": 0, "recec": 1.4}, {"iva": 4, "valor_iva": 0, "base_imponible": 0, "total_con_iva": 0, "recec": 0}, {"iva": 0, "valor_iva": 0, "base_imponible": 0, "total_con_iva": 0, "recec": 0}, {"iva": "0EXENTO", "valor_iva": 0, "base_imponible": 0, "total_con_iva": 0, "recec": 0}]',690.9,3290,3980.9,3980.9,'Trabajo terminado antes de tiempo','','FACTURA','O');
INSERT INTO "invoice_factura" VALUES (5,7,'2025','O-2025-2',2,'O-2025-2-7',5,2,'Banco Santander S.A.','2025-06-15','2025-06-26','[{"iva": 21, "valor_iva": 275.1861, "base_imponible": 1310.41, "total_con_iva": 1585.5961000000002, "recec": 5.2}, {"iva": 10, "valor_iva": 0, "base_imponible": 0, "total_con_iva": 0, "recec": 1.4}, {"iva": 4, "valor_iva": 0, "base_imponible": 0, "total_con_iva": 0, "recec": 0}, {"iva": 0, "valor_iva": 0, "base_imponible": 0, "total_con_iva": 0, "recec": 0}, {"iva": "0EXENTO", "valor_iva": 0, "base_imponible": 0, "total_con_iva": 0, "recec": 0}]',275.19,1310.41,1585.6,1585.6,'Sin observaciones','','FACTURA','O');
INSERT INTO "invoice_facturalineas" VALUES (1,1,6,'O-2025-1-6',2,1,'Desarrollo App Personalizada',1,1000,1000,0,0,1000,21,210,1210,'norm');
INSERT INTO "invoice_facturalineas" VALUES (2,1,6,'O-2025-1-6',3,2,'Informe Power BI',1,3000,3000,0,0,3000,21,630,3630,'norm');
INSERT INTO "invoice_facturalineas" VALUES (3,1,6,'O-2025-1-6',0,0,'Mano de obra',10,22,220,0,0,220,21,46.2,266.2,'norm');
INSERT INTO "invoice_facturalineas" VALUES (4,2,6,'O-2025-2-6',2,1,'Desarrollo App Personalizada',2,1000,2000,0,0,2000,21,420,2420,'norm');
INSERT INTO "invoice_facturalineas" VALUES (5,2,6,'O-2025-2-6',4,3,'Configuracion Servidor',1,30,30,0,0,30,21,6.3,36.3,'norm');
INSERT INTO "invoice_facturalineas" VALUES (6,2,6,'O-2025-2-6',0,0,'Mano de obra',10,22,220,0,0,220,21,46.2,266.2,'norm');
INSERT INTO "invoice_facturalineas" VALUES (7,3,9,'O-2025-1-9',6,1,'Desarrollo Portal Empleado',1,1000,1000,0,0,1000,21,210,1210,'norm');
INSERT INTO "invoice_facturalineas" VALUES (8,3,9,'O-2025-1-9',0,0,'Mano de obra',40,22,880,0,0,880,21,184.8,1064.8,'norm');
INSERT INTO "invoice_facturalineas" VALUES (9,4,7,'O-2025-1-7',8,2,'Aplicación de Fichaje Horario Laboral',1,2100,2100,10,210,1890,21,396.9,2286.9,'norm');
INSERT INTO "invoice_facturalineas" VALUES (10,4,7,'O-2025-1-7',7,1,'Portal del Empleado',1,1000,1000,5,50,950,21,199.5,1149.5,'norm');
INSERT INTO "invoice_facturalineas" VALUES (11,4,7,'O-2025-1-7',0,0,'Mano de obra',20,22.5,450,0,0,450,21,94.5,544.5,'norm');
INSERT INTO "invoice_facturalineas" VALUES (12,5,7,'O-2025-2-7',9,3,'Mejora de la presencia de la web general',1,1310.41,1310.41,0,0,1310.41,21,275.19,1585.6,'norm');
CREATE INDEX IF NOT EXISTS "invoice_art_company_5faba9_idx" ON "invoice_article" (
	"company_id"
);
CREATE INDEX IF NOT EXISTS "invoice_art_descrip_b92c4f_idx" ON "invoice_article" (
	"description"
);
CREATE INDEX IF NOT EXISTS "invoice_art_id_c82ff4_idx" ON "invoice_article" (
	"id"
);
CREATE INDEX IF NOT EXISTS "invoice_com_id_3a34d1_idx" ON "invoice_company" (
	"id"
);
CREATE INDEX IF NOT EXISTS "invoice_cou_id_4994ef_idx" ON "invoice_country" (
	"id"
);
CREATE INDEX IF NOT EXISTS "invoice_cus_cif_nif_720b7b_idx" ON "invoice_customer" (
	"cif_nif"
);
CREATE INDEX IF NOT EXISTS "invoice_cus_company_746230_idx" ON "invoice_customer" (
	"company_id"
);
CREATE INDEX IF NOT EXISTS "invoice_cus_id_a48e3c_idx" ON "invoice_customer" (
	"id"
);
CREATE INDEX IF NOT EXISTS "invoice_doc_company_677429_idx" ON "invoice_document" (
	"company_id"
);
CREATE INDEX IF NOT EXISTS "invoice_doc_descrip_02ae73_idx" ON "invoice_document" (
	"description"
);
CREATE INDEX IF NOT EXISTS "invoice_doc_ejercic_b75178_idx" ON "invoice_document" (
	"ejercicio"
);
CREATE INDEX IF NOT EXISTS "invoice_fac_company_4740b3_idx" ON "invoice_factura" (
	"company_id"
);
CREATE INDEX IF NOT EXISTS "invoice_fac_company_a58809_idx" ON "invoice_facturalineas" (
	"company_id"
);
CREATE INDEX IF NOT EXISTS "invoice_fac_id_636928_idx" ON "invoice_factura" (
	"id"
);
CREATE INDEX IF NOT EXISTS "invoice_fac_invoice_c8e056_idx" ON "invoice_facturalineas" (
	"invoice_id"
);
CREATE INDEX IF NOT EXISTS "invoice_veh_invoice_367b29_idx" ON "invoice_vehicledata" (
	"invoice_id"
);
COMMIT;
