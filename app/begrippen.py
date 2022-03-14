from enum import Enum
from fastapi import HTTPException

import os
import csv
import json

class Category(str, Enum):
    INTELLECTUELE_EIGENDOM_CREATIVE_COMMONS_LICENTIES = 'INTELLECTUELE_EIGENDOM_CREATIVE_COMMONS_LICENTIES'
    INTELLECTUELE_EIGENDOM_DATABANKWET = 'INTELLECTUELE_EIGENDOM_DATABANKWET'
    INTELLECTUELE_EIGENDOM_RIGHTS_STATEMENTS = 'INTELLECTUELE_EIGENDOM_RIGHTS_STATEMENTS'
    INTELLECTUELE_EIGENDOM_SOFTWARE_LICENTIES = 'INTELLECTUELE_EIGENDOM_SOFTWARE_LICENTIES'
    INTELLECTUELE_EIGENDOM_WET_OP_DE_NABURIGE_RECHTEN = 'INTELLECTUELE_EIGENDOM_WET_OP_DE_NABURIGE_RECHTEN'
    OPENBAARHEID_ARCHIEFWET_1995 = 'OPENBAARHEID_ARCHIEFWET_1995'
    OPENBAARHEID_ARCHIEFWET_2021 = 'OPENBAARHEID_ARCHIEFWET_2021'
    OPENBAARHEID_WET_OPEN_OVERHEID = 'OPENBAARHEID_WET_OPEN_OVERHEID'
    PERSOONSGEGEVENS_AVG = 'PERSOONSGEGEVENS_AVG'
    TRIGGERS = 'TRIGGERS'
    VOORKEURSFORMATEN = 'VOORKEURSFORMATEN'

class Concepts:
    def __init__(self, csv_folder:str, json_folder:str): 
        self.json_folder = json_folder
        self.csv_folder = csv_folder       
    # Function to convert a CSV to JSON
    # Takes the file paths as arguments
    def __make_json(self):        
        for objItem in os.listdir(self.csv_folder):
            csvFile = os.path.join(self.csv_folder, objItem)
            if os.path.isfile(csvFile):
                # create a dictionary
                data = []                
                # Open a csv reader called DictReader                
                with open(csvFile, encoding='latin-1') as csvf:
                    csvReader = csv.DictReader(csvf, delimiter= ';')                    
                    # Convert each row into a dictionary
                    # and add it to data
                    for rows in csvReader:
                        # Assuming a column named 'No' to
                        # be the primary key
                        #key = rows[0]
                        data.append(rows)
                        
                # Open a json writer, and use the json.dumps()
                # function to dump data
                jsonFile = os.path.join(self.json_folder, objItem.replace('.csv', '.json'))
                with open(jsonFile, 'w') as jsonf:
                    jsonf.write(json.dumps(data, indent=4))
    
    def load_data(self):
        try:
            self.__make_json() 
        except Exception as err:
            #traceback.print_exc()
            raise HTTPException(status_code=400, detail="Get 'begrippenlijst' error: {0}".format(err)) 
    
    def get_concepts_list(self, category: Category):
        json_object = None
        for objItem in os.listdir(self.json_folder):
            jsonFile = os.path.join(self.json_folder, objItem)
            selectedFile = '{}.json'.format(category.lower());
            if os.path.isfile(jsonFile) and selectedFile == objItem:
                with open(jsonFile, "rb") as f:
                    json_object = json.load(f)
                    break;                    
        return json_object    
    