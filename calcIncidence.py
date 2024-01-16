# Functions helpful for calculating adverse probability distributions of IHME data

import pandas as pd
from dotenv import load_dotenv

load_dotenv()

def calcIncidencePerICD10(df:pd.dataframe):
    '''
    Calculate incidence per icd code.
    
    - df: dataframe about patients discharged from hosiptal per ICD-10 code. Processed from 中国卫生年鉴.
    '''


    return result_df

def calcIncidencePerICD10FromExcel(file:str, sheet:str='sheet1'):
    '''Calculate incidence from Excel instead of dataframe.'''
    df = pd.read_excel(file, sheet)
    return calcIncidencePerICD10(df)

