from fastapi import HTTPException
from begrippen import Category

import os
import json

class PreferenceFormat:    
    def __init__(self, json_folder:str):
        self.json_file = json_folder
            
    def get_preference_list(self, file = Category.VOORKEURSFORMATEN) :
        json_object = None
        target_file = os.path.join(self.json_file, '{}.json'.format(file.lower()))
        if not os.path.exists(target_file):
            raise HTTPException(status_code=404, detail="Item not found: {}".format(self.json_file))
        try:
            with open(target_file, "rb") as f:
                json_object = json.load(f)                
        except Exception as err:
            #traceback.print_exc()
            raise HTTPException(status_code=400, detail="Get 'voorkeursformatenlijst' error: {0}".format(err))           
        return json_object