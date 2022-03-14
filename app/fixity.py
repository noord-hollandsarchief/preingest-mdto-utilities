from fastapi import HTTPException

import os
import hashlib

class Fixity: 
    def __init__(self, algorithm : str):
        self.algorithm = algorithm

    def __calculate_md5(self, file_name: str):
        if not os.path.exists(file_name):
            raise HTTPException(status_code=404, detail="Item not found: {}".format(file_name))    
        with open(file_name, "rb") as f:
            file_hash = hashlib.md5()
            while chunk := f.read(8192):
                file_hash.update(chunk)
        return {"hash" : file_hash.name, "value" : file_hash.hexdigest()}
        
    def __calculate_sha1(self, file_name: str):
        if not os.path.exists(file_name):
            raise HTTPException(status_code=404, detail="Item not found: {}".format(file_name))
        with open(file_name, "rb") as f:
            file_hash = hashlib.sha1()
            while chunk := f.read(8192):
                file_hash.update(chunk)
        return {"hash" : file_hash.name, "value" : file_hash.hexdigest()}

    def __calculate_sha224(self, file_name: str):
        if not os.path.exists(file_name):
            raise HTTPException(status_code=404, detail="Item not found: {}".format(file_name))    
        with open(file_name, "rb") as f:
            file_hash = hashlib.sha224()
            while chunk := f.read(8192):
                file_hash.update(chunk)
        return {"hash" : file_hash.name, "value" : file_hash.hexdigest()}
 
    def __calculate_sha256(self, file_name: str):
        if not os.path.exists(file_name):
            raise HTTPException(status_code=404, detail="Item not found: {}".format(file_name))    
        with open(file_name, "rb") as f:
            file_hash = hashlib.sha256()
            while chunk := f.read(8192):
                file_hash.update(chunk)
        return {"hash" : file_hash.name, "value" : file_hash.hexdigest()}
       
    def __calculate_sha384(self, file_name: str):
        if not os.path.exists(file_name):
            raise HTTPException(status_code=404, detail="Item not found: {}".format(file_name))    
        with open(file_name, "rb") as f:
            file_hash = hashlib.sha384()
            while chunk := f.read(8192):
                file_hash.update(chunk)
        return {"hash" : file_hash.name, "value" : file_hash.hexdigest()}
    
    def __calculate_sha512(self, file_name: str):
        if not os.path.exists(file_name):
            raise HTTPException(status_code=404, detail="Item not found: {}".format(file_name))    
        with open(file_name, "rb") as f:
            file_hash = hashlib.sha512()
            while chunk := f.read(8192):
                file_hash.update(chunk)
        return {"hash" : file_hash.name, "value" : file_hash.hexdigest()}

    def __calculate_sha3_224(self, file_name: str):
        if not os.path.exists(file_name):
            raise HTTPException(status_code=404, detail="Item not found: {}".format(file_name))    
        with open(file_name, "rb") as f:
            file_hash = hashlib.sha3_224()
            while chunk := f.read(8192):
                file_hash.update(chunk)
        return {"hash" : file_hash.name, "value" : file_hash.hexdigest()}
 
    def __calculate_sha3_256(self, file_name: str):
        if not os.path.exists(file_name):
            raise HTTPException(status_code=404, detail="Item not found: {}".format(file_name))    
        with open(file_name, "rb") as f:
            file_hash = hashlib.sha3_256()
            while chunk := f.read(8192):
                file_hash.update(chunk)
        return {"hash" : file_hash.name, "value" : file_hash.hexdigest()}
       
    def __calculate_sha3_384(self, file_name: str):
        if not os.path.exists(file_name):
            raise HTTPException(status_code=404, detail="Item not found: {}".format(file_name))    
        with open(file_name, "rb") as f:
            file_hash = hashlib.sha3_384()
            while chunk := f.read(8192):
                file_hash.update(chunk)
        return {"hash" : file_hash.name, "value" : file_hash.hexdigest()}
    
    def __calculate_sha3_512(self, file_name: str):
        if not os.path.exists(file_name):
            raise HTTPException(status_code=404, detail="Item not found: {}".format(file_name))    
        with open(file_name, "rb") as f:
            file_hash = hashlib.sha3_512()
            while chunk := f.read(8192):
                file_hash.update(chunk)
        return {"hash" : file_hash.name, "value" : file_hash.hexdigest()}
    
    def calculate_fixity(self, file_name:str):
        try:
            if self.algorithm == 'md5':
                return self.__calculate_md5(file_name)
            if self.algorithm == 'sha1':
                return self.__calculate_sha1(file_name) 
            if self.algorithm == 'sha224':
                return self.__calculate_sha224(file_name)
            if self.algorithm == 'sha384':
                return self.__calculate_sha384(file_name)
            if self.algorithm == 'sha256':
                return self.__calculate_sha256(file_name)
            if self.algorithm == 'sha512':
                return self.__calculate_sha512(file_name)
            if self.algorithm == 'sha3_224':
                return self.__calculate_sha3_224(file_name)
            if self.algorithm == 'sha3_256':
                return self.__calculate_sha3_256(file_name)
            if self.algorithm == 'sha3_384':
                return self.__calculate_sha3_384(file_name)
            if self.algorithm == 'sha3_512':
                return self.__calculate_sha3_512(file_name)
            
            raise HTTPException(status_code=404, detail="Algorithm not found: {}".format(self.algorithm))   
        except Exception as err:
            #traceback.print_exc()
            raise HTTPException(status_code=400, detail="Run fixity calculation error: {0}".format(err)) 
        
         
        
