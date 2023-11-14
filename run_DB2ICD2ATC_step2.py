import os
import DB2ICD2ATC as DIA

def run():
    DIA.load_and_update_IHME()
    return

run()