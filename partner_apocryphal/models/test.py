

import zipfile
import csv
import urllib.request 
urllib.request.urlretrieve("https://servicioscf.afip.gob.ar/Facturacion/facturasApocrifas/DownloadFile.aspx", "invoices.zip")
with zipfile.ZipFile("invoices.zip", 'r') as zip_ref:
    zip_ref.extractall(".")
# f = open("FacturasApocrifas.txt", "r")
# for x in f:
#   print(x)
import csv
count=0
with open('FacturasApocrifas.txt', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        count+=1
        print('cuit[%r]=>%r', count, row[0])
