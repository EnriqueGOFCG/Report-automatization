# -*- coding: utf-8 -*-
"""
Created on Fri Jul 13 12:33:03 2018

@author: Frontier
"""

import pandas as pd
import os
from datetime import datetime, timedelta, date

todate = date.today()

exp_directory = r'.\Python CSVs\Export Tables'
car_task_directory = r'.\Python CSVs\Daily Car Task Reports'

cars = pd.read_csv(exp_directory + r'\MX_daily_cars.csv')
car_tasks = pd.read_csv(exp_directory + r'\MX_daily_car_tasks.csv')
inspections = pd.read_csv(exp_directory + r'\MX_daily_inspections.csv')
inspection_details = pd.read_csv(exp_directory + r'\MX_daily_inspections_details.csv')
responsables = pd.read_csv(exp_directory + r'\Concepto-Responsable.csv', 
                           encoding = 'ISO-8859-1')
zonas = pd.read_csv(exp_directory + r'\IP-Zonas.csv',
                    encoding = 'ISO-8859-1')

cars_exp = cars[(-cars.legalStatus.isnull()) &
                (-((cars.legalStatus == 'OWNER') & 
                  (cars.physicalStatus == 'ATOWNER')))]

columns = ['internalId',
           'vin',
           'purchaseChannel',
           'purchaseLocation']

cars_exp = cars_exp[columns]
cars_exp.purchaseLocation = cars_exp.purchaseLocation.str.replace('IP - ', 'IP ')
cars_exp = cars_exp.merge(zonas, on = 'purchaseLocation', how = 'left' )

car_tasks = car_tasks.merge(responsables, on = 'type', how = 'left')

car_tasks.createdAt = car_tasks.createdAt.apply(lambda x: pd.to_datetime(x.split()[0]))
car_tasks = car_tasks[car_tasks.createdAt < date.today()]

car_tasks = car_tasks.merge(cars_exp, 
                            left_on = 'carId', 
                            right_on = 'internalId', 
                            how = 'left')

car_tasks = car_tasks[-(car_tasks.vin.isnull()) &
                      (car_tasks.status == 'OPEN')]
car_tasks = car_tasks.reindex_axis(sorted(car_tasks.columns), axis=1)

car_tasks['Mes Día'] = car_tasks.createdAt.apply(lambda x: str(x).split()[0][5:])

car_tasks = car_tasks[['id',
                       'carId',
                       'vin', 
                       'make', 
                       'model', 
                       'year', 
                       'licensePlate', 
                       'createdAt', 
                       'priority',
                       'description', 
                       'dueDate',
                       'responsible', 
                       'status', 
                       'subject',  
                       'type', 
                       'purchaseChannel',
                       'Mes Día',
                       'Responsable', 
                       'purchaseLocation', 
                       'Zona'
                       ]]

operaciones = car_tasks.groupby(['Responsable','Mes Día'], as_index = False).agg({'purchaseLocation': 'count'})
operaciones = operaciones.pivot(index = 'Responsable', 
                                columns = 'Mes Día', 
                                values = 'purchaseLocation')
operaciones = operaciones.reindex_axis(sorted(operaciones.columns),
                                       axis=1)
for i in operaciones.index:
    operaciones.loc[i, 'Grand Total'] = operaciones.loc[i, :].sum()
for i in operaciones:
    operaciones.loc['Total', i] = operaciones.loc[:, i].sum()

puntos_de_compra = car_tasks[car_tasks.Responsable.str.contains('oordinador')]
puntos_de_compra = puntos_de_compra.groupby(['Zona','Mes Día'], as_index = False).agg({'purchaseLocation': 'count'})
puntos_de_compra = puntos_de_compra.pivot(index = 'Zona', 
                                          columns = 'Mes Día', 
                                          values = 'purchaseLocation')
puntos_de_compra = puntos_de_compra.reindex_axis(sorted(puntos_de_compra.columns),
                                                 axis=1)

for i in puntos_de_compra.index:
    puntos_de_compra.loc[i, 'Grand Total'] = puntos_de_compra.loc[i, :].sum()
for i in puntos_de_compra:
    puntos_de_compra.loc['Total', i] = puntos_de_compra.loc[:, i].sum()

writer = pd.ExcelWriter(car_task_directory + r'\car_task_' +
                         str(todate) + 
                         '.xlsx')

operaciones.to_excel(writer,
                     startrow = 0,
                     startcol = 0,
                     index = True,
                     sheet_name = 'Operaciones')

puntos_de_compra.to_excel(writer,
                          startrow = 0,
                          startcol = 0,
                          index = True,
                          sheet_name = 'Puntos de Compra')

car_tasks.to_excel(writer,
                   startrow = 0,
                   startcol = 0,
                   index = False,
                   sheet_name = 'Daily car tasks')

responsables.to_excel(writer,
                      startrow = 0,
                      startcol = 0,
                      index = False,
                      sheet_name = 'Responsables')

zonas.to_excel(writer,
               startrow = 0,
               startcol = 0,
               index = False,
               sheet_name = 'Zonas')

writer.save()
writer.close()



