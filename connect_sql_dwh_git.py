# -*- coding: utf-8 -*-
"""
Created on Mon Jul  9 17:03:29 2018

@author: Frontier
"""

import pyodbc
import sys
import pandas as pd
import os


dwh_directory = r'./Python CSVs/DWH Tables'

def get_dwh_tables(connection_parameters_dir):
    connection_parameters = open(connection_parameters_dir + '\connection_parameters.txt')
    connection_parameters = connection_parameters.readlines()
    
    cnxn = pyodbc.connect(Driver = connection_parameters[0].split('= ')[1][:-1],
                          Server   = connection_parameters[1].split('= ')[1][:-1],
                          Database = connection_parameters[2].split('= ')[1][:-1], 
                          UID = connection_parameters[3].split('= ')[1][:-1],
                          PWD = connection_parameters[4].split('= ')[1])
    
    cursor = cnxn.cursor()
    
    cars = pd.read_sql('SELECT * FROM dbo.Cars', cnxn)
    car_manufacturers = pd.read_sql('SELECT * FROM dbo.CarManufacturers', cnxn)
    car_models = pd.read_sql("SELECT * FROM dbo.CarModel", cnxn)
    bids = pd.read_sql("SELECT * FROM dbo.Bids", cnxn)
    dealers = pd.read_sql("SELECT * FROM dbo.Dealers", cnxn)
    inspections = pd.read_sql("SELECT * FROM dbo.Inspections", cnxn)
    bid_types = pd.read_sql("SELECT * FROM dbo.BidType", cnxn)
    auctions = pd.read_sql("SELECT * FROM dbo.Auctions", cnxn)
    auction_winners = pd.read_sql("SELECT * FROM dbo.AuctionWinners", cnxn)
    inspection_centers = pd.read_sql("SELECT * FROM dbo.InspectionCenter", cnxn)
    
    if not os.path.exists(dwh_directory):
        os.makedirs(dwh_directory)
    
    cars.to_csv(dwh_directory + r'/db_cars.csv', index = False)
    car_manufacturers.to_csv(dwh_directory + '\db_cars_manufacturers.csv', index = False)
    car_models.to_csv(dwh_directory + '\db_cars_models.csv', index = False)
    bids.to_csv(dwh_directory + '\db_bids.csv', index = False)
    dealers.to_csv(dwh_directory + '\db_dealers.csv', index = False)
    inspections.to_csv(dwh_directory + '\db_inspections.csv', index = False)
    bid_types.to_csv(dwh_directory + '\db_bid_types.csv', index = False)
    auctions.to_csv(dwh_directory + '\db_auctions.csv', index = False)
    auction_winners.to_csv(dwh_directory + '\db_auction_winners.csv', index = False)
    inspection_centers.to_csv(dwh_directory + '\db_inspection_centers.csv', index = False)
    
    cnxn.close()
    
    return

if __name__ == "__main__":
    connection_parameters_dir = sys.argv[1]
    get_dwh_tables(connection_parameters_dir)
    

