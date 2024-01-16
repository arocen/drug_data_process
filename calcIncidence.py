# Functions helpful for calculating adverse probability distributions of IHME data

import pandas as pd
from dotenv import load_dotenv

load_dotenv()

def calcIncidencePerICD10(df:pd.dataframe):
    # TODO: update the algorithm if data from other source is available
    '''
    Calculate incidence per icd code.
    
    - df: dataframe about patients discharged from hosiptal per ICD-10 code. Processed from 中国卫生年鉴.

    Return 2 df with 2 columns. One is range of ICD10, another is percentage of patients discharged from hosiptal.
    '''

    return df["ICD10", "疾病构成(%)"]

def calcIncidencePerICD10FromExcel(file:str, sheet:str='sheet1'):
    '''Calculate incidence from Excel instead of dataframe.'''
    df = pd.read_excel(file, sheet)
    return calcIncidencePerICD10(df)

