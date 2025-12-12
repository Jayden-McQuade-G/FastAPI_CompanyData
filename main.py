from typing import Union
from fastapi import FastAPI

import os
import json
import pandas as pd

def path_to_api(path, data):
    for root, dirs, files in os.walk(path):
        metric = os.path.basename(root)              # Data type e.g "balance_sheet"
        for file in files:
            duns = file.replace(".csv", "")   

            file_path = os.path.join(root, file)     # File path to csv data at hand
            df = pd.read_csv(file_path)              # csv into pandas dataframe 

            df = df.replace({pd.NA: None, pd.NaT: None, float('nan'): None, "": None})                  
            
            df_dict = df.to_dict(orient = "records")  # df to dict

            if duns not in data:                      # create dun + add first metric and data
                data[duns] = {metric: df_dict}
            else:
                data[duns][metric] = df_dict          # add other metrics and data
    return data


app = FastAPI()
data = {}            
path_to_api("CompanyData", data)
 

@app.get("/")
def read_root():
    return "Welcome to Company Data API -- See '/docs' for available queries"

@app.get("/all/", summary = "Read All Data (Returns all data - Lacks Optimisation = slow)")
def read_all_data():
    return data

@app.get("/companies/", summary = "Read Companies (Returns list of DUN codes)")
def read_companies():
    return list(data.keys())

@app.get("/companies/{duns}", summary = "Read Companies Docs (Returns list of company docs)")
def read_companies_docs(duns):
    return list(data[duns].keys())

@app.get("/companies/{duns}/{metric}", summary = "Read Companies Docs Data (Returns data from a company doc)")
def read_companies_docs_data(duns, metric):
    print(data[duns][metric])
    return data[duns][metric]


