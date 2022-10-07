import logging
_logger = logging.getLogger(__name__)
import os
import tarfile
import shutil
import hashlib
import base64
import gzip
import pytz
import requests
from datetime import datetime, timedelta
from io import BytesIO
import pathlib
from pathlib import Path

def mandar_mail(self,asunto="Correo Facturacion en Línea",para_mail="info@sistecem.com",mensaje="Mensaje de Prueba",
                desde_mail="miguelbelmontejimenez@gmail.com"):
    mail_pool = self.env['mail.mail']
    values = {'subject': asunto,
              'email_from': desde_mail,
              'email_to': para_mail,
              'body_html': mensaje,
    }
    # values.update({'res_id': 'obj.id'})  # [optional] here is the record id, where you want to post that email after sending
    # values.update({'model': ''Object Name})  # [optional] here is the object(like 'project.project')  to whose record id you want to post that email after sending
    msg_id = mail_pool.create(values)
    if msg_id:
        msg_id.send()
        _logger.info("Mail enviado a : "+para_mail)
    else:
        _logger.error("No se pudo enviar mail : " + para_mail)

def give_current_path(directory):
    path= ''
    for record in (os.path.dirname(os.path.abspath(__file__))).split(os.sep):
        path+= record + '/'
    return path.replace('models/',directory)

def formatear_fecha(fecha):
    formateada = str(fecha - timedelta(hours=4, minutes=0)).replace(" ", "T")
    # formateada = str(fecha - timedelta)
    return formateada

def clean_folder(path):
    # path = 'C:/Program Files/odoo14/server/odoo/addons/codigodecontrolbolivia/static/factura/paquete_factura'
    for the_file in os.listdir(path):
        file_path = os.path.join(path, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            # elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)

def compute_currency_inicial(self,text):
    try:
        if text == 'DOLAR':
            currency = self.env['res.currency'].search([('currency_unit_label', '=', 'Dollars')])
        elif text == 'PESO ARGENTINO':
            currency = self.env['res.currency'].search([('name', '=', 'ARS')])
        else:
            textTitle=text.lower().title()
            currency = self.env['res.currency'].search(['|','|','|',
                                                        ['currency_unit_label', '=', text],
                                                        ['currency_unit_label', '=', text + "s"],
                                                        ['currency_unit_label', '=', textTitle],
                                                        ['currency_unit_label', '=', textTitle+"s"]])
        if currency:
            _logger.info("Emparejó Catálogo con Moneda "+currency.name)
            return int(currency.id)
    except:
        return None

def fastest_object_to_dict(obj):
    if not hasattr(obj, '__keylist__'):
        return obj
    data = {}
    fields = obj.__keylist__
    for field in fields:
        val = getattr(obj, field)
        if isinstance(val, list):  # tuple not used
            data[field] = []
            for item in val:
                data[field].append(fastest_object_to_dict(item))
        else:
            data[field] = fastest_object_to_dict(val)
    return data

def convert_cadena(path):
    with open(path, "rb") as file:
        converted_string = base64.b64encode(file.read())
    # print(converted_string)

    # with open('encode.bin', "wb") as file:
    #     file.write(converted_string)
    return converted_string


def SHA256(path):
    h = hashlib.sha256()
    with open(path, 'rb', buffering=0) as f:
        for b in iter(lambda: f.read(128 * 1024), b''):
            h.update(b)
    return h.hexdigest()


def compress_GZ(xml):
    # xml_path = 'C:/Program Files/Odoo14/server/addons/codigodecontrolbolivia/static/factura/template_invoice.xml'
    # xml = 'C:/Program Files/odoo14/server/odoo/addons/codigodecontrolbolivia/static/factura/prueba2.xml'

    # with open(xml_path, 'rb') as f_in:
    #     with gzip.open(xml_path + '.gz', 'wb') as f_out:
    #         shutil.copyfileobj(f_in, f_out)

    # print("abro el xml "+xml)
    with open(xml, 'rb') as f_in:
        # with gzip.open(xml + '.gz', 'wb') as f_out:
        with gzip.open(xml + '.zip', 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)



def gzip_encode(data):
    """data -> gzip encoded data

    Encode data using the gzip content encoding as described in RFC 1952
    """
    if not gzip:
        raise NotImplementedError
    f = BytesIO()
    gzf = gzip.GzipFile(mode="wb", fileobj=f, compresslevel=1)
    gzf.write(data)
    gzf.close()
    encoded = f.getvalue()
    f.close()
    return encoded

def compress_encoded(s_in):
    s_out = gzip.compress(s_in)
    return s_out

def compress_TAR_GZ(folder_path):
    # ruta = "C://Program Files/odoo14/server/odoo/addons/codigodecontrolbolivia/static/factura"

    for obj in os.scandir(folder_path):
        if obj.is_dir():
            with tarfile.open(f"{obj.path}.tar.gz", "w:gz") as file:
                file.add(obj.path, arcname=obj.name, recursive=True)

def date_time():
    tz = pytz.timezone('America/Caracas')
    return str(datetime.now(tz))[:-9].replace(" ", "T")


def compress_tardir(path, file_name):
    # path = "C://Program Files/odoo14/server/odoo/addons/codigodecontrolbolivia/static/factura/factura/"
    # filename = "C://Program Files/odoo14/server/odoo/addons/codigodecontrolbolivia/static/factura/client_invoice1111.tar.gz"
    file_name = path+file_name+'.tar.gz'
    # print(file_name)
    # open file in write mode
    file_obj = tarfile.open(file_name, "w:gz")

    # Add other files to tar file
    archivos = os.listdir(path)
    cantidad =0
    for item in archivos:
        file_obj.add(path + item, arcname=item)
        # file_obj.add(xml1, arcname='name1.xml')
        # print(item)
        cantidad=cantidad+1
    file_obj.close()
    # print(cantidad-1)
    return (cantidad-1)