"""
configuration file class for kicad database 

"""
import configparser
import os
import glob2
from pathlib import Path
from termcolor import colored

SCRIPT_DIR = os.path.dirname(__file__)
DEFAULT_CONFIG_NAME = "config.ini"
DEFAULT_CONFIG_PATH = os.path.join(SCRIPT_DIR,DEFAULT_CONFIG_NAME)

INI_SECTION_PATHS = "PATHS"
INI_EXTENSION = "ini"
INI_PATHS_VAR_DB = "DB_PATH"
INI_PATHS_VAR_CF = "CONFIG_FILE_PATH"
INI_PATHS_VAR_CSV = "CSV_IMPORT_DIR_PATH"
INI_PATHS_VAR_DB_EXPORT = "DB_EXPORT_PATH"

class Kicad_DB_Config_File():
    def __init__(self) -> None:
        self.path_DB = ""
        self.path_DB_export = ""
        self.path_CSV_import_dir = ""
        self.path_config_file = ""
        pass

    def set_config_file_path(self,config_file_path):
        #if(config_file_path) 
        path = Path(config_file_path)

        is_file = path.is_file()
        if(is_file == False):
            return False
        
        if(config_file_path[-3:]!= INI_EXTENSION):
            return False

        
        self.path_config_file = config_file_path

        return True


    def get_all_paths(self):

        config = configparser.ConfigParser()
        config.read(self.path_config_file)
         
        try:
            config_file_path = config[INI_SECTION_PATHS][INI_PATHS_VAR_CF]
        except KeyError as e:
            status_msg = "ERROR: Missing " + str(e) + " variable"
            return status_msg    
     
        try:
            database_path = config[INI_SECTION_PATHS][INI_PATHS_VAR_DB]
        except KeyError as e:
            status_msg = "ERROR: Missing " + str(e) + " variable"
            return status_msg    

        try:
            database_export_path = config[INI_SECTION_PATHS][INI_PATHS_VAR_DB_EXPORT]
        except KeyError as e:
            status_msg = "ERROR: Missing " + str(e) + " variable"
            return status_msg  

        try:
            csv_export_path = config[INI_SECTION_PATHS][INI_PATHS_VAR_CSV]
        except KeyError as e:
            status_msg = "Missing " + str(e) + " variable"
            return status_msg     
            
        self.path_config_file = config_file_path 
        self.path_DB = database_path
        self.path_DB_export = database_export_path
        self.path_CSV_import_dir = csv_export_path

        status_msg = "All Config Files Varibles Are Set"

        return status_msg
    
    def print_paths(self):
        print(colored("\nCONFIG FILE PATH:\n",'green')+self.path_config_file+'\n')
        print(colored("DATABASE PATH:\n",'green')+self.path_DB+'\n')
        print(colored("DATABASE EXPORT PATH:\n",'green')+self.path_DB_export +'\n')
        print(colored("CSV IMPORT DIRECTORY PATH:\n",'green')+self.path_CSV_import_dir +'\n')

    
    def get_path_config_file(self):
        return self.path_config_file
    
    def get_path_database(self):
        return self.path_DB
    
    def get_path_db_export(self):
        return self.path_DB_export
    
    def get_path_CSV_import_dir(self):
        return self.path_CSV_import_dir
        
if(__name__=="__main__"):

    db_gui_config = Kicad_DB_Config_File()
    db_gui_config.set_config_file_path(config_file_path=DEFAULT_CONFIG_PATH)
    db_gui_config.get_all_paths()
    db_gui_config.print_paths()
    