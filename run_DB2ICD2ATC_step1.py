# run step 1 of DB2ICD2ATC.py

import os
import DB2ICD2ATC as DIA
from dotenv import load_dotenv

load_dotenv() # load .env file
death_ATC = os.environ.get("death_ATC")
disease_ATC = os.environ.get("disease_ATC")

def run():
    '''
    About saved result file:
    If ICD9 column is empty, then ATC-4 is also empty.
    Else if all codes in ICD9 column have no ATC-4 matched, then ATC-4 is an empty dict (i.e. "{}").
    Else if part of codes in ICD9 column are matched with ATC-4, then only those matched results will be written to file.
    Moreover, probabilities of duplicate ATC-4 will be summed up afer mergence.
    '''
    death_BD2ICD = DIA.load_death_BD2ICD()
    disease_BD2ICD = DIA.load_disease_BD2ICD()
    new_death_df = DIA.icd2atc(death_BD2ICD)
    # save
    new_death_df.to_excel(death_ATC)
    new_disease_df = DIA.icd2atc(disease_BD2ICD)
    # save
    new_disease_df.to_excel(disease_ATC)
    return

run()