from kicad_database import *

def test_class_funct():
    # create kicad database class
    kicad_DB = kicad_database()
    kicad_DB.set_database_path(DEFAULT_DB_PATH)
  
    (database_exist,status_msg) = kicad_DB.init_kicad_database(DEFAULT_DB_PATH)
    print(status_msg)

    kicad_DB.reset_field_params()
    
    #standard 100nF 0603
   
    kicad_DB.fld_symbol = "Device:C"
    kicad_DB.fld_value = "100nF"
    kicad_DB.fld_footprint = "Capacitor_SMD:C_0603_1608Metric"
    kicad_DB.fld_datasheet = "https://mm.digikey.com/Volume0/opasdata/d220001/medias/docus/609/CL10B104KB8NNNC_Spec.pdf"
    kicad_DB.fld_manufacturer = "Samsung Electro-Mechanics"
    kicad_DB.fld_mpn = "CL10B104KB8NNNC"
    kicad_DB.fld_digikey_PN = "1276-1000-1-ND"
    kicad_DB.fld_tolerance = "±10%"
    kicad_DB.fld_rating = "50V"
    kicad_DB.fld_package = "0603"
    kicad_DB.fld_description = "100nF 0603 50V"
    
    (MPN_exist,_) = kicad_DB.does_MPN_exist(table=TBL_NAME_CAPACITOR,MPN_str = kicad_DB.fld_mpn)

    if(MPN_exist):
        print("MPN exists:",kicad_DB.fld_mpn) 
        
    else:
        print(":todo")
        kicad_DB.push_mfuncts_2_table(TBL_NAME_CAPACITOR)

    
    kicad_DB.reset_field_params()    

    #standard 1uF 0805
    kicad_DB.fld_symbol = "Device:C"
    kicad_DB.fld_value = "1uF"
    kicad_DB.fld_footprint = "Capacitor_SMD:C_0805_2012Metric"
    kicad_DB.fld_datasheet = "https://mm.digikey.com/Volume0/opasdata/d220001/medias/docus/609/CL10B104KB8NNNC_Spec.pdf"
    kicad_DB.fld_manufacturer = "Samsung Electro-Mechanics"
    kicad_DB.fld_mpn = "CL21B105KBFNNNG"
    kicad_DB.fld_digikey_PN = "1276-1029-1-ND"
    kicad_DB.fld_mouser_PN = EMPTY_STR
    kicad_DB.fld_LCSC_PN = EMPTY_STR
    kicad_DB.fld_misc_distributor = EMPTY_STR
    kicad_DB.fld_misc_PN = EMPTY_STR
    kicad_DB.fld_misc_link = EMPTY_STR
    kicad_DB.fld_tolerance = "±10%"
    kicad_DB.fld_rating = "50V"
    kicad_DB.fld_package = "0805"
    kicad_DB.fld_description = "1uF 0805 50V"
    kicad_DB.fld_notes = "Test Working"

    (MPN_exist,_) = kicad_DB.does_MPN_exist(table=TBL_NAME_CAPACITOR,MPN_str = kicad_DB.fld_mpn)


    if(MPN_exist):
        print("MPN exists:",kicad_DB.fld_mpn) 
        
    else:
        print(":todo")
        kicad_DB.push_mfuncts_2_table(TBL_NAME_CAPACITOR)


    csv_path_list = kicad_DB.get_csv_path_list(CSV_TABLE_DIR)
    capacitor_csv_path = csv_path_list[0]
    (capacitor_tname, _) = kicad_DB.get_table_name_from_path(csv_path=capacitor_csv_path,
                                    table_list=KICAD_TABLE_NAME_LIST)
    
    
    (status_bool,status_msg)= kicad_DB.import_csv_2_sql_db(csv_path=capacitor_csv_path,field_name_list=KICAD_FIELD_NAME_LST,table_name=capacitor_tname)
    print(status_msg)

  
    

if(__name__ == '__main__'):
    test_class_funct()