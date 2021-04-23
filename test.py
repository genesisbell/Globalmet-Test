# -*- coding: utf-8 -*-
import requests
import datetime
import pytz
import csv

import os
from os.path import join, dirname

from dotenv import load_dotenv

#Variables env
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

response = requests.get("http://globalmet.mx/estaciones/conditions/78/", headers={
    "Authorization" : os.environ.get('AUTHORIZATION')
})

data = response.json()
data = data.pop('current_observation')

#Fecha
format = "%Y-%m-%dT%H:%M:%S"
date = datetime.datetime.strptime(data['fecha_medicion'][:-1], format)
utc_tz = pytz.timezone('UTC')
local_tz = pytz.timezone('America/Hermosillo')

#Temperatura
temp_c = data['temp_c']
temp_f = (temp_c * 9/5) + 32

#Viento
wind_kph = data['wind_kph']
wind_mph = wind_kph / 1.609
wind_dir = data['wind_dir']

#Precipitación
precip_today_metric = data['precip_today_metric']
precip_today_inches = precip_today_metric / 25.4

#Humedad
relative_humidity = data['relative_humidity']
eto = data['eto']

datos = [
    {'Nombre' : 'Fecha', 'Dato': date},
    {'Nombre' : 'Temperatura C', 'Dato': temp_c},
    {'Nombre' : 'Temperatura F', 'Dato': temp_f},
    {'Nombre' : 'Viento en Kph', 'Dato': wind_kph},
    {'Nombre' : 'Viento en Mph', 'Dato': wind_mph},
    {'Nombre' : 'Direccion del viento', 'Dato': wind_dir},
    {'Nombre' : 'Precipitacion acumulada en mm', 'Dato': precip_today_metric},
    {'Nombre' : 'Precipitacion acumulada en pulg', 'Dato': precip_today_inches},
    {'Nombre' : 'Humedad relativa', 'Dato': relative_humidity},
    {'Nombre' : 'Evapotranspiracion', 'Dato': eto},
]

#Archivo csv
write_file = 'datos.csv'
csv_columns = ['Nombre', 'Dato']
with open (write_file, 'w',) as f:
    writer = csv.DictWriter(f, lineterminator = '\n', fieldnames=csv_columns)
    writer.writerow({'Nombre': 'Nombre', 'Dato': 'Dato'})
    for row in datos:
        writer.writerow(row)

#Valores en pantalla
print "\n\t\t\t\t*******************"
print "\t\t\t\tObservacion actual:"
print "\t\t\t\t*******************\n"
print "Fecha: \t\t\t\t\t%s" % utc_tz.localize(date).astimezone(local_tz)
print "Temperatura C: \t\t\t\t%s C" % temp_c
print "Temperatura F: \t\t\t\t%s F" % temp_f
print "Viento en Kph: \t\t\t\t%s Kph" % wind_kph
print "Viento en Mph: \t\t\t\t%s Mph" % wind_mph
print "Direccion del viento: \t\t\t%s " % wind_dir
print "Precipitacion acumulada en mm: \t\t%s mm" % precip_today_metric
print "Precipitacion acumulada en pulg: \t%s in" % precip_today_inches
print "Humedad relativa: \t\t\t%s " % relative_humidity
print "Evapotranspiracion: \t\t\t%s " % eto