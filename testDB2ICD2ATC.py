import DB2ICD2ATC as DIA

# test


# disease_BD2ICD = load_disease_BD2ICD()
# print(disease_BD2ICD)

def test_convert_icd9_to_list():
    death_BD2ICD = DIA.load_death_BD2ICD()
    # print(death_BD2ICD)
    DIA.convert_icd9_to_list(death_BD2ICD)
    return

test_convert_icd9_to_list()