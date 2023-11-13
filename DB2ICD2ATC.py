import pandas as pd
import os
from dotenv import load_dotenv
import re

load_dotenv() # load .env file

death_BD2ICD_path=os.environ.get("death_BD2ICD_path")
disease_BD2ICD_path=os.environ.get("disease_BD2ICD_path")


# Step 1: disease burden to icd9

# read the specific columns of IHME's excel file about the matches of DB and icd9 as Dataframe (2 tables, death and disease)
def load_death_BD2ICD(path=death_BD2ICD_path)->pd.DataFrame:
    '''Read BD-to-ICD excel file of deaths'''
    
    dtypes = {
        "Cause": "object", 
        "ICD9": "object"
    }
    # Assign skiprows=1 to skip the first row which is not the column name of table but only explanatory information.
    df = pd.read_excel(path, dtype=dtypes, usecols=list(dtypes), skiprows=1)
    return df


def load_disease_BD2ICD(path=disease_BD2ICD_path)->pd.DataFrame:
    '''Read BD-to-ICD excel file of diseases'''

    dtypes = {
        "Cause": "object", 
        "ICD9": "object"
    }
    # Assign skiprows=1 to skip the first row which is not the column name of table but only explanatory information.
    df = pd.read_excel(path, dtype=dtypes, usecols=list(dtypes), skiprows=1)

    return df

# convert each value of icd9 columns into a list
def convert_icd9_to_list(icd_df):
    for i in icd_df.index:
        icd_value = icd_df.at[i, "ICD9"]
        # icd9非缺失值
        if not pd.isna(icd_value):

            # 转换为列表
            icds = icd_value.split(", ")
            # 用re识别整数部分和范围
            print(icds)

            # 调用helper function，将atc-4及概率分布写入新的一列
            # To-do:



            # icd_df.at[i, column_name_of_atc] = str(icd9_to_atc4(icd9, ICD2ATC_df))
        # 跳过缺失值的处理
    return

def standarize_icd(icds:list)->list:
    '''A helper function of convert_icd9_to_list to standarize icd codes.'''
    

    for icd in icds:
        # check if it's a range
        if "-" in icd:
            lower, upper = icd.split[0], icd.split[1]
            # check if the range is less than 1 (e.g. 001.1-001.9)
            # check and extract digit part
            if not lower.isdigit():
                a = 1

                # get values between lower digit and upper digit
                # get prefix
            # transfer str into int
            # remove zeros in the front (if exist)
            else:
                lower, upper = int(lower), int(upper)
            # get values between upper and lower

                # add prefix to each value (if exists)
    return

def match_range(icd_range:str)->list:
    '''
    input: icd characters including '-' which denotes a range exists
    return:upper, lower, prefix

    >>> import re
    >>> icd_range = "001.1-001.9"
    >>> print(match_range(icd_range))
    ('', '1', '1')
    >>> icd_range = "v22.2-v24.7"
    >>> results = match_range(icd_range)
    >>> print(results)
    ('v', '22', '24')
    '''
    # zeros (if exist) in the front of digits are filtered by this pattern
    pattern = "([a-zA-Z]*)0*([1-9]+)\.?\d*\-[a-zA-Z]*0*([1-9]+)\.?\d*"
    results = re.match(pattern,  icd_range).groups()

    return results


# for each element of list, use regular expression to match integer part and scope 

# Step 2: icd9 to atc4
# measure_id-2-measure_name = {"1": "Deaths", "2": DALYs (Disability-Adjusted Life Years), and more ?} 
# to specify whether its death or disease base on measure_id or measure_name (reference: the explanation of measure_name  on IHME's website, MEASURE_METRIC_DEFINITIONS in codebook folder)
# for each icd9 list, loop over its element and look up atc4 codes, probability accordingly
# sum probabilies of duplicate atc4 codes
# write unique atc4 codes and probability to a new column of each disease burden

# Step 3: use such relationships
# load disease burden data from IHME and look up their atc4 codes
# write atc4 codes and probabilities

# Question: Normalization atc4 probabilities of each disease burden? How to handle missing values when doing this?


# run doctest
if __name__ == "__main__":
    import doctest
    doctest.testmod()