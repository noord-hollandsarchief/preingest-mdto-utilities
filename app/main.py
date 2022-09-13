import os
import base64
import uvicorn
import subprocess
import oletools.oleid
import oletools.olevba
import oletools.oleobj
import fitz

from uuid import UUID, uuid4
from fastapi import FastAPI, HTTPException
from voorkeursformaten import PreferenceFormat
from fixity import Fixity
from begrippen import Category, Concepts
from quicksand.quicksand import quicksand

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to the Preingest extended utilities REST-API."}

@app.post("/fixity/md5/{base64_encoded_full_path}")
async def run_fixity_md5(base64_encoded_full_path :str):    
    calculate = Fixity('md5')
    decodedBytes = base64.b64decode(base64_encoded_full_path)
    file = str(decodedBytes, "utf-8")
    result = calculate.calculate_fixity(file)
    return result

@app.post("/fixity/sha1/{base64_encoded_full_path}")
async def run_fixity_sha1(base64_encoded_full_path:str):
    calculate = Fixity('sha1')
    decodedBytes = base64.b64decode(base64_encoded_full_path)
    file = str(decodedBytes, "utf-8")
    result = calculate.calculate_fixity(file)
    return result

@app.post("/fixity/sha224/{base64_encoded_full_path}")
async def run_fixity_sha224(base64_encoded_full_path:str):
    calculate = Fixity('sha256')
    decodedBytes = base64.b64decode(base64_encoded_full_path)
    file = str(decodedBytes, "utf-8")
    result = calculate.calculate_fixity(file)
    return result

@app.post("/fixity/sha256/{base64_encoded_full_path}")
async def run_fixity_sha256(base64_encoded_full_path:str):
    calculate = Fixity('sha256')
    decodedBytes = base64.b64decode(base64_encoded_full_path)
    file = str(decodedBytes, "utf-8")
    result = calculate.calculate_fixity(file)
    return result

@app.post("/fixity/sha384/{base64_encoded_full_path}")
async def run_fixity_sha384(base64_encoded_full_path:str):
    calculate = Fixity('sha384')
    decodedBytes = base64.b64decode(base64_encoded_full_path)
    file = str(decodedBytes, "utf-8")
    result = calculate.calculate_fixity(file)
    return result

@app.post("/fixity/sha512/{base64_encoded_full_path}")
async def run_fixity_sha512(base64_encoded_full_path:str):
    calculate = Fixity('sha512')
    decodedBytes = base64.b64decode(base64_encoded_full_path)
    file = str(decodedBytes, "utf-8")
    result = calculate.calculate_fixity(file)
    return result

@app.post("/fixity/sha3_224/{base64_encoded_full_path}")
async def run_fixity_sha3_224(base64_encoded_full_path:str):
    calculate = Fixity('sha3_224')
    decodedBytes = base64.b64decode(base64_encoded_full_path)
    file = str(decodedBytes, "utf-8")
    result = calculate.calculate_fixity(file)
    return result

@app.post("/fixity/sha3_256/{base64_encoded_full_path}")
async def run_fixity_sha3_256(base64_encoded_full_path):
    calculate = Fixity('sha3_256')
    decodedBytes = base64.b64decode(base64_encoded_full_path)
    file = str(decodedBytes, "utf-8")
    result = calculate.calculate_fixity(file)
    return result

@app.post("/fixity/sha3_384/{base64_encoded_full_path}")
async def run_fixity_sha3_384(base64_encoded_full_path:str):
    calculate = Fixity('sha3_384')
    decodedBytes = base64.b64decode(base64_encoded_full_path)
    file = str(decodedBytes, "utf-8")
    result = calculate.calculate_fixity(file)
    return result

@app.post("/fixity/sha3_512/{base64_encoded_full_path}")
async def run_fixity_sha3_512(base64_encoded_full_path:str):
    calculate = Fixity('sha3_512')
    decodedBytes = base64.b64decode(base64_encoded_full_path)
    file = str(decodedBytes, "utf-8")
    result = calculate.calculate_fixity(file)
    return result

@app.get("/voorkeursformatenlijst")
async def get_preference_list():     
    json_folder = os.path.join(os.getcwd(), '/app/json')   
    pref = PreferenceFormat(json_folder=json_folder);    
    result = pref.get_preference_list()
    return result

@app.get("/begrippenlijst/{category}")
async def get_concept_list(category: Category):     
    json_folder = os.path.join(os.getcwd(), '/app/json')
    csv_folder = os.path.join(os.getcwd(), '/app/csv')    
    concept = Concepts(csv_folder=csv_folder, json_folder=json_folder)
    concept.load_data()      
    return concept.get_concepts_list(category=category)
    
@app.get("/bucket/show")
async def show_bucket():
    if not os.path.isfile('/root/.aws/bucket'):
        raise HTTPException(status_code=400, detail='Could not find the file "bucket" in folder "/root/.aws/"!')     
    with open('/root/.aws/bucket', 'r') as file:
        out = None
        try:
            bucket = file.read().rstrip()
            command = ['aws', 's3', 'ls', '--recursive', 's3://{}'.format(bucket)] 
            out = subprocess.check_output(command)
        except Exception as err:
            raise HTTPException(status_code=400, detail="Shell execution error: {0}".format(err))         
    return { "result" : out }

@app.delete("/bucket/clear")
async def clear_bucket():
    if not os.path.isfile('/root/.aws/bucket'):
            raise HTTPException(status_code=400, detail='Could not find the file "bucket" in folder "/root/.aws/"!')     
    with open('/root/.aws/bucket', 'r') as file:
        out = None
        try:
            bucket = file.read().rstrip()
            command = ['aws', 's3', 'rm', '--recursive', 's3://{}/opex'.format(bucket)] 
            out = subprocess.check_output(command)
        except Exception as err:
            raise HTTPException(status_code=400, detail="Shell execution error: {0}".format(err))         
    return { "result" : out }

@app.put("/bucket/upload/{base64_encoded_full_path_folder}")
async def upload_2_bucket(base64_encoded_full_path_folder:str):
    if not os.path.isfile('/root/.aws/bucket'):
            raise HTTPException(status_code=400, detail='Could not find the file "bucket" in folder "/root/.aws/"!')     
    with open('/root/.aws/bucket', 'r') as file:
        out = None
        try:
            decodedBytes = base64.b64decode(base64_encoded_full_path_folder)
            folder = str(decodedBytes, "utf-8")
            bucket = file.read().rstrip()
            command = ['aws', 's3', 'cp', '--recursive', '{}'.format(folder), 's3://{}/opex'.format(bucket)] 
            out = subprocess.check_output(command)
        except Exception as err:
            raise HTTPException(status_code=400, detail="Shell execution error: {0}".format(err))         
    return { "result" : out }

@app.post("/archive/expand/{target_folder_name}/{base64_encoded_full_path_archive}")
async def expand_archive(base64_encoded_full_path_archive:str, target_folder_name:UUID):  
    decodedBytes = base64.b64decode(base64_encoded_full_path_archive)
    target_archive = str(decodedBytes, "utf-8")    
    if not os.path.isfile(target_archive):
        raise HTTPException(status_code=400, detail='Archive file "{}" not found'.format(target_archive))     
    out = []
    files = []
    path='/data/{}'.format(str(target_folder_name))
    try: 
        if(not os.path.exists(path)):
            os.mkdir(path)         
        command = ['tar', '-oxvf', '{}'.format(target_archive), '-C', '/data/{}'.format(str(target_folder_name))] 
        subprocess.check_output(command)
        # r=root, d=directories, f = files
        for r, d, f in os.walk(path):
            for file in f:
                    files.append(os.path.join(r, file))                    
        out = out + files            
    except Exception as err:
            raise HTTPException(status_code=400, detail="Shell execution error: {0}".format(err))         
    
    return { "result" : out }  

@app.post("/archive/compress/{base64_encoded_full_path}")
async def compress_folder(base64_encoded_full_path:str):    
    decodedBytes = base64.b64decode(base64_encoded_full_path)
    target_folder = str(decodedBytes, "utf-8")
    archive_name = '{}.tar'.format(str(uuid4()))
    
    if not os.path.isdir(target_folder):
        raise HTTPException(status_code=400, detail='Folder "{}" not found'.format(target_folder)) 
    
    out = None
    try:    
        archive_structure = target_folder.split('/')
        archive_structure.pop()         
        parent_folder = '/'.join(archive_structure)     
        command = ['tar', '-czvf', os.path.join(parent_folder, archive_name), '{}'.format(target_folder)]         
        subprocess.check_output(command)
        out = os.path.join(parent_folder, archive_name)
    except Exception as err:
            raise HTTPException(status_code=400, detail="Shell execution error: {0}".format(err))         
    
    return { "result" : out } 

@app.post("/utilities/scan_for_macros/{base64_encoded_full_path_file}")
async def scan_for_macros(base64_encoded_full_path_file:str):
    decodedBytes = base64.b64decode(base64_encoded_full_path_file)
    target_file = str(decodedBytes, "utf-8")
    if not os.path.isfile(target_file):
        raise HTTPException(status_code=400, detail='File "{}" not found'.format(target_file)) 
    vba = None
    vba_output = {}    
    try:
        oid = oletools.oleid.OleID(target_file)
        vba = oletools.olevba.VBA_Parser(target_file)
        ole = oletools.oleobj.find_ole(target_file, None)
                 
        indicators_list = oid.check()
        indicators = []
        for i in indicators_list:
            indicator = { "id" : i.id, "name" : i.name, "value" : repr(i.value), "description" : i.description }
            indicators.append(indicator)
            if i.id == 'ext_rels':
                vba_output["embeddedLinks"] = "false" if eval(repr(i.value)) == 0 else "true"                
            #print('Indicator id=%s name="%s" type=%s value=%s' % (i.id, i.name, i.type, repr(i.value)))
            #print('description:', i.description)        
        vba_output["vbaMacros"] = "true" if vba.detect_vba_macros() else "false"
        vba_output["xmlMacros"] = "true" if vba.detect_xlm_macros() else "false"
        vba_output["vbaEncrypted"] = "true" if vba.detect_is_encrypted() else "false"
        vba_output["embeddedFiles"] = "true" if not ole is None else "false"
        
        vba_output["indicators"] = indicators
        
    except Exception as err:        
            raise HTTPException(status_code=400, detail="OLETools execution error: {0}".format(err))  
    finally:
        if not vba is None:
            vba.close()        
    
    return { "result" : vba_output } 

@app.post("/utilities/scan_for_suspicion/{base64_encoded_full_path_file}")
async def scan_for_suspicion(base64_encoded_full_path_file:str):
    decodedBytes = base64.b64decode(base64_encoded_full_path_file)
    target_file = str(decodedBytes, "utf-8")
    if not os.path.isfile(target_file):
        raise HTTPException(status_code=400, detail='File "{}" not found'.format(target_file)) 
    
    result = None
    try:
        qs2 = quicksand(target_file)
        qs2.process()
        result = qs2.results 
               
    except Exception as err:  
        raise HTTPException(status_code=400, detail="QuickSand execution error: {0}".format(err))  
    
    return { "scan" : result }

@app.post("/utilities/find_embedded_files/{base64_encoded_full_path_file}")
async def find_embedded_files(base64_encoded_full_path_file:str):
    result = None  
    decodedBytes = base64.b64decode(base64_encoded_full_path_file)
    target_file = str(decodedBytes, "utf-8")
    if not os.path.isfile(target_file):
        raise HTTPException(status_code=400, detail='File "{}" not found'.format(target_file)) 
    
    embedded = {}
    ef_list = []
    try:
        doc = fitz.open(target_file)
        embedded["count"] = doc.embfile_count()
        
        for i in range(doc.embfile_count()):  # number of embedded files
            info = doc.embfile_info(i)  # get one info dict
            ef = { "name" : info["name"], 
                  #"file" : info["file"], 
                  #"description" : info["desc"], 
                  "length" : info["length"], 
                  "size" : info["size"] }
            ef_list.append(ef)
            
        embedded["files"] = ef_list        
        result = embedded
           
    except Exception as err:  
        raise HTTPException(status_code=400, detail="PyMuPdf execution error: {0}".format(err))  
    
    return { "embedded" : result }    

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)