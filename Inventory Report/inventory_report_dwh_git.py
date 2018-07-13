# -*- coding: utf-8 -*-
"""
Created on Wed Jul 11 12:46:16 2018

@author: Frontier
"""

import pandas as pd
import numpy as np
from datetime import datetime
import os

todate = datetime.utcnow()

dwh_directory = r'.\Python CSVs\DWH Tables'

inventory_report_directory = r'.\Python CSVs\Inventory Reports'
if not os.path.exists(inventory_report_directory):
    os.makedirs(inventory_report_directory)

cars = pd.read_csv(dwh_directory + r'\db_cars.csv')  
models = pd.read_csv(dwh_directory + r'\db_cars_models.csv')
manufacturers = pd.read_csv(dwh_directory + r'\db_cars_manufacturers.csv')

cars = cars[cars.deleted_at.isnull()]
models = models.merge(manufacturers, how = 'left', on = 'car_manufacturer_id')

cars = cars.merge(models, how = 'left', on = 'car_model_id')
cars.internal_car_id = 'MX-' + cars.internal_car_id.astype(str)
cars['Precio sin IVA'] = np.nan

columns_1 = ['internal_car_id',
             'car_selling_status',
             'car_legal_status',
             'car_physical_status',
             'car_vin', 
             'purchase_channel',
             'car_purchased_date',
             'car_purchase_price_car', 
             'Precio sin IVA', 
             'car_purchase_location',
             'car_handedover_from_seller',
             'car_current_location',
             'client_subtype',
             'car_manufacturer_name',
             'car_model_name',
             'year_manufactured',
             'car_trim',
             'car_color']

cars_dwh = cars
cars_dwh.loc[cars.client_subtype.isnull(), 'client_subtype'] = ' '
cars_dwh.client_subtype = cars_dwh.client_subtype.str.lower()

cars_dwh.loc[cars_dwh.client_subtype == 'person', 'Precio sin IVA'] = \
                cars_dwh.loc[cars_dwh.client_subtype == 'person', 'car_purchase_price_car']
cars_dwh.loc[cars_dwh.client_subtype != 'person',
             'Precio sin IVA'] = \
             cars_dwh.loc[cars_dwh.client_subtype != 'person',
                         'car_purchase_price_car']/1.16


cars_dwh = cars.loc[:, cars.columns[cars.columns.isin(columns_1)]]
cars_dwh = cars_dwh[columns_1]

cars_dwh.loc[cars_dwh.car_vin.isnull(),'car_vin'] = 'Faltante'
cars_dwh.loc[cars_dwh.car_purchase_location.isnull(),'car_purchase_location'] = 'Faltante'
cars_dwh.car_vin = cars_dwh.car_vin.str.replace('\(.*\)', '').str.strip()
cars_dwh.car_color = cars_dwh.car_color.str.replace('*.\(', '').str.replace('\)*.', '')

inventory_cars_dwh = cars_dwh[(cars_dwh.car_selling_status.isin(['AVAILABLE',
                                                                 'RESERVED',
                                                                 'NOTAVAILABLE',
                                                                 'PENDINGCLEARANCE',
                                                                 'ONCONSIGNMENT'])) &\
                             (-cars_dwh.car_legal_status.isnull()) &
#                             (-cars_dwh.car_legal_status.isin(['OWNER'])) &
                             (-cars_dwh.purchase_channel.isnull()) &
                             (-cars_dwh.car_current_location.isnull()) &
                             (cars_dwh.car_current_location.str.contains('Buyer') == False) &
                             (cars_dwh.car_current_location.str.contains('B2B') == False) &
                             (cars_dwh.car_physical_status.isin(['INTRANSIT',
                                                                 'ATOURLOCATION']))]

def list0(x):
    try:
        return datetime.strptime(x.split()[0], "%Y-%m-%d")
    except:
        return pd.NaT

inventory_cars_dwh.car_handedover_from_seller = inventory_cars_dwh.car_handedover_from_seller.apply(list0).replace('nan','')

inventory_cars_dwh['Dias en inventario'] = inventory_cars_dwh.\
                                            car_handedover_from_seller.\
                                            apply(lambda x: (todate - x).days)
inventory_cars_dwh['Dias en inventario buckets'] = \
                            pd.cut(inventory_cars_dwh['Dias en inventario'], np.arange(0,33,3))
inventory_cars_dwh['Dias en inventario buckets'] = \
        inventory_cars_dwh['Dias en inventario buckets'].cat.add_categories(['30 +'])
inventory_cars_dwh['Dias en inventario buckets'] =\
         inventory_cars_dwh['Dias en inventario buckets'].fillna('30 +')
inventory_cars_dwh['Dias en inventario buckets'] =\
         inventory_cars_dwh['Dias en inventario buckets'].astype(str)

strange_cars_dwh = cars_dwh[(cars_dwh.car_purchase_price_car < 2) |
                             (cars_dwh.car_selling_status.isnull())]

#inventory_cars_dwh = inventory_cars_dwh.iloc[:, 3:]
inventory_cars_dwh = inventory_cars_dwh.rename(columns = {'car_selling_status': 'Estatus de venta',
                                                          'car_legal_status': 'Estadus legal',
                                                          'car_physical_status': 'Estatus físico',
                                                          'internal_car_id':'ID', 
                                                          'car_vin':'NIV', 
                                                          'purchase_channel':'Tipo de compra',	
                                                          'car_purchased_date': 'Fecha de compra',
                                                          'car_purchase_price_car':'Precio con IVA',	
                                                          'car_purchase_location':'Origen de compra', 
                                                          'car_handedover_from_seller': 'Fecha de ingreso',
                                                          'car_current_location':'Ubicacion Actual',
                                                          'client_subtype': 'Persona compra',
                                                          'car_manufacturer_name': 'Marca',
                                                          'car_model_name': 'Modelo',
                                                          'year_manufactured': 'Año',
                                                          'car_trim': 'Versión',
                                                          'car_color': 'Color'})

inventory_cars_dwh = inventory_cars_dwh.sort_values('ID')

for i in inventory_cars_dwh:
    inventory_cars_dwh.loc[inventory_cars_dwh[i].isnull(), i] = ' '

writer = pd.ExcelWriter(inventory_report_directory + r'\inventory_dwh_' +
                         str(todate).split()[0] + 
                         '.xlsx')
inventory_cars_dwh.to_excel(writer,
                           startrow = 0,
                           startcol = 0,
                           index = False,
                           sheet_name = 'Inventory')
strange_cars_dwh.to_excel(writer,
                        startrow = 0,
                        startcol = 0,
                        index = False,
                        sheet_name = 'Strange Cars')
writer.save()
writer.close()

inventory_cars_dwh.car_selling_status.value_counts().sum()



