# Insert proportion of population column to IHME csv files according to sex_name and age_name columns
# Given sex_id, age_id, and year, look up proportion of population in China.

import pandas as pd
from tqdm import tqdm
import os
from dotenv import load_dotenv

load_dotenv() # load .env file

# To-do:
# 1. Load China's population data by year.
# 2. Get sex_id, age_id, and year from columns of IHME csv files.
# 3. Look up and calculate proportion of population from population data.
# 4. Insert proportion of population to a new column in IHME csv files.

popDataPath = os.environ.get("popDataPath")

def loadPop(path=popDataPath):
    '''
    Load multiple sheets of population data.
    Return: dict
        keys of dict: 
            "allAge", percentage of male and female by year
            "male", percentage of male by age and year
            "female", percentage of female by age and year
            "both", percentage of both sex by age and year
    '''

    # Read all sheets directly into an ordered dictionary
    pop = pd.read_excel(path, sheet_name=None)
    return pop

def testLoadPop():
    pop = loadPop()
    for key, value in pop.items():
        print(key)
        print(value)