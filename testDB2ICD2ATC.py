import DB2ICD2ATC as DIA

# test




def test_icd2atc():
    death_BD2ICD = DIA.load_death_BD2ICD()
    new_death_df = DIA.icd2atc(death_BD2ICD)
    print(new_death_df)

test_icd2atc()