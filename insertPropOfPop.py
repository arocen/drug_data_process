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
IHME_save_folder = os.environ.get("IHME_save_folder")

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

    # Read all sheets directly into an ordered dictionary, skip first row
    pop = pd.read_excel(path, sheet_name=None, skiprows=[0])
    return pop

def testLoadPop():
    pop = loadPop()
    for key, value in pop.items():
        print(key)
        print(value)
    print(pop["both"].at[1, 2014])

def load_and_update_IHME(folder_path=IHME_save_folder, save_folder=IHME_save_folder):
    '''load IHME csv files in path as a list of DataFrame'''
    csv_files = sorted([f for f in os.listdir(folder_path) if f.endswith(".csv")])

    # use tqdm to add a process bar
    for filename in tqdm(csv_files):
        path = os.path.join(folder_path, filename)
        save_path = os.path.join(save_folder, "updated_" + filename)
        df = pd.read_csv(path)
        insertProp(...)
        df.to_csv(save_path)
    return

def insertProp():
    '''Insert proportion of population to each row of IHME dataframe.'''

    return

def lookUpProp(pop:dict[str, pd.DataFrame], year:int, sex_id:int, age_id:int)->float:
    '''
    Given year, sex_id, and age_id, look up proportion of population (percentage).

    >>> lookUpProp(2015, 3, 15)
    7.58
    '''
    table_name = chooseTable(sex_id, age_id)

    return pop

def chooseTable(sex_id, age_id)->str:
    '''Return table name where percentage will be looked up.'''
    # All ages
    if age_id == 22:
        return "allAge"
    
    # Not all ages
    else:
        # Male
        if sex_id == 1:
            return "male"
        elif sex_id == 2:
            return "female"
        else:
            return "both"

def getRowIndices(lookupDict:dict, table_name:str, sex_id:int, age_id:int)->list[int]|None:
    '''Get row indices according to table name, sex_id, and age_id.'''

    allAgeIndices = {1: [0, ], 2: [1, ], 3: [0, 1]}    # keys: sex_id
    if table_name == "allAge":
        return allAgeIndices[sex_id]
        
    else:
        return  getIndicesExceptAllAge(lookupDict, age_id)
    

def getIndicesExceptAllAge(lookupDict:dict, age_id:int)->list[int]|None:
    '''If table name is "male", "female", or "both", get row indices according to age_id.'''
    try:
        return lookupDict[age_id]
    except:
        # Can not find key in lookupDict
        return None
    

def initializeIndicesDict()->dict[int, list[int]]:
    '''Inialize row indices dict for table "male", "female", or "both".'''
    
    # age_id in range(6, 21)
    singleGroup = dict()
    for i in range(6, 21):
        singleGroup[i] = [i - 5, ]
    
    loopkupDict = {1: [0, ],
                21: [16, 17, 18, 19],
                23: [1, 2],
                24: [range(3, 10)],
                25: [range(10, 14)],
                26: [range(14, 20)],
                30: [16, ],
                31: [17, ],
                32: [18, ],
                37: [range(4, 20)],
                39: [0, 1, 2],
                41: [range(10, 15)],
                157: [range(5, 20)],
                158: [range(4)],
                159: [2, 3, 4],
                160: [17, 18, 19],
                169: [range(2, 11)],
                172: [1, 2],
                188: [1, 2, 3],
                197: [range(3, 8)],
                206: [range(5, 10)],
                228: [range(11, 20)],
                230: [range(12, 16)],
                232: [13, 14],
                234: [range(15, 20)],
                235: [19, ],
                243: [15, 16],
                284: [range(4, 11)],
                285: [range(11, 18)],
                286: [range(12, 18)],
                287: [range(13, 18)],
                288: [range(14, 18)],
                289: [range(15, 18)],
                420: [range(0, 14)]
                }
    # Merge 2 dict
    loopkupDict.update(singleGroup)

    return loopkupDict


# testLoadPop()