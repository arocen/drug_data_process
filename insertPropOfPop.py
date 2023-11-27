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

def getRowIndices(table_name, sex_id, age_id)->list[int]:
    '''Get row indices according to table name, sex_id, and age_id.'''
    if table_name == "allAge":
        if sex_id == 1:
            return [0, ]
        elif sex_id == 2:
            return [1, ]
        else:
            return [0, 1]
        
    elif table_name == "male":
        ...

        return

def ageGroupId2RowIndices(age_id)->list[int]:
    '''If table name is "male", "female", or "both", get row indices according to age_id.'''

    if age_id in [1, range(6, 22)]:

        # Under 5 age
        if age_id == 1:
            return [0, ]
        
        # Above 80
        elif age_id == 21:
            return [16, 17, 18, 19]
        
        # Other age groups
        else:
            return [age_id - 5, ]
    
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
                197: [range(3, 8)]


                    }
    # # 5-14 years
    # elif age_id == 23:
    #     return [1, 2]
    
    # # 15-49 years
    # elif age_id == 24:
    #     return [range(3, 10)]
    
    # # 50-69 years
    # elif age_id == 25:
    #     return [range(10, 14)]
    
    # # 70+ years
    # elif age_id == 26:
    #     return [range(14, 20)]
    
    # # 80-84, 85-89, 90-94
    # elif age_id in [30, 31, 32]:
    #     return [age_id - 14, ]
    
    # # 20 plus
    # elif age_id == 37:
    #     return [range(4, 20)]
    
    # # 0-14
    # elif age_id == 39:
    #     return [0, 1, 2]
    
    # # 50 to 74 years
    # elif age_id == 41:
    #     return [range(10, 15)]
    
    # # 25 plus
    # elif age_id == 157:
    #     return [range(5, 20)]
    
    # # <20 years
    # elif age_id == 158:
    #     return [range(4)]
    
    # # 10 to 24
    # elif age_id == 159:
    #     return [2, 3, 4]
    
    # # 85 plus
    # elif age_id == 160:
    #     return [17, 18, 19]
    
    # # 10 to 54
    # elif age_id == 169:
    #     return [range(2, 11)]
    
    # # 0 to 9
    # elif age_id == 172:
    #     return [1, 2]
    
    # # 5 to 19
    # elif age_id == 188:
    #     return [1, 2, 3]
    
    # # 15 to 39
    # elif age_id == 197:
    #     return [range(3, 8)]
    
    # 


testLoadPop()