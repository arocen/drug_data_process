import pandas as pd
import os
from dotenv import load_dotenv
import re
import icd9_to_atc4 as i2a

load_dotenv() # load .env file

death_BD2ICD_path=os.environ.get("death_BD2ICD_path")
disease_BD2ICD_path=os.environ.get("disease_BD2ICD_path")
ICD2ATC_path = os.environ.get("ICD2ATC_path")

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
def icd2atc(icd_df:pd.DataFrame, column_name_of_atc="ATC-4")->pd.DataFrame:
    '''
    Reads str value of each row, converts it to list and standarizes it.
    Finally look up and write atc codes and probability distributions according to icd codes.
    '''
    # load icd to atc excel
    icd2atc_df = i2a.read_ICD2ATC()
    

    for i in icd_df.index:
        icd_value = icd_df.at[i, "ICD9"]

        # check value of icd9 is not missing
        if not pd.isna(icd_value):

            # convert str to list
            icds = icd_value.split(", ")

            # standarize icd codes with helper function
            standarized = standarize_icd(icds)
            
            
            # 调用helper function，将atc-4及概率分布写入新的一列
            atc_dict = get_atc(standarized, icd2atc_df)

            icd_df.at[i, column_name_of_atc] = str(atc_dict)

        # skip handling of missing values of icd9
    return icd_df

def standarize_icd(icds:list[str])->list[str]:
    '''
    A helper function of convert_icd9_to_list(), standarizes icd codes.
    

    >>> icds = ["v023.5-v026.6"]
    >>> print(standarize_icd(icds))
    ['v23', 'v24', 'v25', 'v26']

    >>> print(standarize_icd(["055.1-055.8"]))
    ['55']

    >>> new_icds = ["A035.2-A036.5", "M008.2"]
    >>> print(standarize_icd(new_icds))
    ['A35', 'A36', 'M8']

    >>> new_icds2 = ["040.2", "070", "V050.1-V052.3"]
    >>> print(standarize_icd(new_icds2))
    ['40', '70', 'V50', 'V51', 'V52']
    '''
    
    standarized = []
    for icd in icds:
        # check if it's a range
        if "-" in icd:
            result = match_range(icd)

            # check if pattern is matched
            if result:
                # unpack tuple
                (prefix, lower, upper) = match_range(icd)
            else:
                continue

            # check if the range is less than 1 (e.g. 001.1-001.9)
            if lower == upper:
                standarized.append(prefix + lower)
            else:
                # transfer str into int and get values from lower to lower
                values = range(int(lower), int(upper) + 1)
                for value in values:
                    # convert int back to str, add prefix to each value (if exists)
                    standarized.append(prefix + str(value))
        else:
            # remove zeros in the front and decimal numbers
            standarized.append(rm_zeros_and_decimals(icd))
                
    return standarized

def match_range(icd_range:str)->list:
    '''
    A helper function of standarize_icd().
    Input: icd characters including '-' which denotes a range exists.
    Return: a tuple of prefix, lower, and upper. 
        If prefix does not exist, return value of prefix is an empty string.

        
    >>> import re
    >>> icd_range = "001.1-001.9"
    >>> print(match_range(icd_range))
    ('', '1', '1')

    >>> icd_range = "v22.2-v24.7"
    >>> results = match_range(icd_range)
    >>> print(results)
    ('v', '22', '24')

    >>> icd_range = "040.1-042.7"
    >>> results = match_range(icd_range)
    >>> print(results)
    ('', '40', '42')
    '''
    # zeros (if exist) in the front of digits are filtered by this pattern
    pattern = "^([a-zA-Z]*)0*(\d+)(?:\.\d+)?\-[a-zA-Z]*0*(\d+)(?:\.\d+)?$"
    results = re.match(pattern,  icd_range)
    if results:
        return results.groups()
    # 'NoneType' object has no attribute 'groups'
    else:
        return None




    

def rm_zeros_and_decimals(icd9_code:str)->str:
    '''
    A helper function of standarize_icd(). Remove zeros in the front and decimal numbers of icd9 codes.
    Return: standarized single icd9 code.

    >>> icd = "v007.6"
    >>> print(rm_zeros_and_decimals(icd))
    v7
    >>> icd_new = "040"
    >>> print(rm_zeros_and_decimals(icd_new))
    40
    '''
    pattern = "^([a-zA-Z]*)0*(\d+)(?:\.\d+)?$"
    results = re.match(pattern,  icd9_code).groups()
    (prefix, numbers) = results
    return prefix + numbers


def get_atc(icd_list:list, icd2atc_df:pd.DataFrame)->dict:
    '''
    Input: a list of standarized icd codes.
    Return: a dictionary whose keys are atc codes, values are probabilities.
    '''
    results = pd.DataFrame()
    for icd in icd_list:

        # look up atc4 distribution
        atc4_distr = i2a.icd9_to_atc4(icd, icd2atc_df)
        # print(atc4_distr)

        # convert dict to DataFrame
        distr_df = pd.DataFrame.from_dict(atc4_distr)

        # check if look up result is empty
        if not distr_df.empty:

            
            print(distr_df)
            # merge dictionaries and sum up probabilities of dupicate atc codes
            results = pd.concat([results, distr_df]).groupby(['ATC']).sum().reset_index()
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