import os
import DB2ICD2ATC as DIA
from dotenv import load_dotenv

load_dotenv() # load .env file

IHME_test_data_folder = os.environ.get("IHME_test_data_folder")
IHME_test_save_folder = os.environ.get("IHME_test_save_folder")

def run():
    DIA.load_and_update_IHME()
    return

def test():
    '''test with a small sample'''
    DIA.load_and_update_IHME(folder_path=IHME_test_data_folder, save_folder=IHME_test_save_folder)

run()