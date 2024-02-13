"""
kicad db linker creates kicad database linker file
for kicad to use ODBC server
"""
import os
import json
import csv
import pandas as pd
from kicad_database import KICAD_TABLE_NAME_LIST,KICAD_FIELD_NAME_LST

DB_EMPTY_STR = ""
DB_LINKER_FILE_EXT = ".kicad_dbl"
DB_DEFAULT_VERSION = 0
DB_DEFAULT_TIMEOUT = 2
DB_DEFAULT_TYPE = "odbc"
DB_DEFAULT_DSN = "kicad_db"
DB_JSON_TRUE = True
DB_JSON_FALSE = False

SCRIPT_DIRECTORY = os.path.dirname(__file__)
(DATABASE_DIR, _) = os.path.split(SCRIPT_DIRECTORY)
KICAD_LINKER_FOLDER = "kicad_db_linker"
KICAD_LINKER_FOLDER_PATH = os.path.join(DATABASE_DIR,KICAD_LINKER_FOLDER)
KICAD_LINKER_NAME = "master_database"+ DB_LINKER_FILE_EXT
KICAD_LINKER_PATH  = os.path.join(KICAD_LINKER_FOLDER_PATH,KICAD_LINKER_NAME)
FIELD_PARAMS_CSV_PATH  = os.path.join(SCRIPT_DIRECTORY,"field_params.csv")

### db json tags ###
DB_JSON_TAG_META = "meta"
DB_JSON_META_VERSION = "version"
DB_JSON_META_FILENAME = "filename"

DB_JSON_TAG_NAME = "name"
DB_JSON_TAG_DESCR = "description"

DB_JSON_TAG_SRC = "source"
DB_JSON_SRC_TYPE = "type"
DB_JSON_SRC_DSN = "dsn"
DB_JSON_SRC_USR = "username"
DB_JSON_SRC_PSWD = "password"
DB_JSON_SRC_TOUT = "timeout_seconds"
DB_JSON_SRC_CONN_STR = "connection_string"

DB_JSON_TAG_LIB = "libraries"
DB_JSON_LIB_NAME = "name"
DB_JSON_LIB_TABLE = "table"
DB_JSON_LIB_KEY = "key"
DB_JSON_LIB_SYM = "symbols"
DB_JSON_LIB_FP = "footprints"
DB_JSON_LIB_FIELDS = "fields"

DB_JSON_FLDS_COL = "column"
DB_JSON_FLDS_NAME = "name"
DB_JSON_FLDS_VOA = "visible_on_add"
DB_JSON_FLDS_VIC = "visible_in_chooser"
DB_JSON_FLDS_SHOW = "show_name"

DB_JSON_TAG_PROP = "properties"
DB_JSON_PROP_DESC = "description"
DB_JSON_PROP_FTPF = "footprint_filters"
DB_JSON_PROP_KEYWORDS = "keywords"
DB_JSON_PROP_EXCL_BOM = "exclude_from_bom"
DB_JSON_PROP_EXCL_BRD = "exclude_from_board"

DB_DEFAULT_KEY = "Part_ID"
DB_DEFAULT_SYMBOLS = "Symbols"
DB_DEFAULT_FOOTPRINTS = "Footprints"

DB_PROP_PARAM_DESCR = "Description"
DB_PROP_PARAM_FTPF = "Footprint Filters"
DB_PROP_PARAM_KEYWORD = "Keywords"
DB_PROP_PARAM_EXCL_BOM = "No BOM"
DB_PROP_PARAM_EXCL_BRD = "Schematic Only"


f_params_csv_headers  = ["table",	
                     "column",	
                     "name",	
                     "visible_on_add",	
                     "visible_in_chooser",	
                     "show_name"]


PROPERTIES_FIELD_DICT = {DB_JSON_PROP_DESC:DB_PROP_PARAM_DESCR,
        DB_JSON_PROP_FTPF:DB_PROP_PARAM_FTPF,
        DB_JSON_PROP_KEYWORDS:DB_PROP_PARAM_KEYWORD,
        DB_JSON_PROP_EXCL_BOM:DB_PROP_PARAM_EXCL_BOM,
        DB_JSON_PROP_EXCL_BRD:DB_PROP_PARAM_EXCL_BRD
        }


"""
kicad database linker file class
"""
class kicad_db_linker():
    def __init__(self):
        self.db_linker_path = ""
        self.field_param_df = None

        self.meta_version = 0
        self.meta_basename = ""
        self.db_name = ""
        self.db_description = ""
        self.source_type = DB_DEFAULT_TYPE
        self.source_dsn = DB_DEFAULT_DSN
        self.source_username = DB_EMPTY_STR
        self.source_password = DB_EMPTY_STR
        self.source_timeout = DB_DEFAULT_TIMEOUT
        self.source_conn_str = DB_EMPTY_STR
        self.db_key = DB_DEFAULT_KEY

    def set_db_linker_path(self,db_linker_path):
        self.db_linker_path = db_linker_path

    def set_field_param_df(self,field_params_csv_path):
        self.field_param_df = pd.read_csv(field_params_csv_path)

    def remove_str_brackets(self,bracket_str):
        new_str = bracket_str[1:-1].strip()
        return new_str
    
    def indent_str(self, raw_str ,indent_spacing):
        CHAR_SPACE = " "
        CHAR_NEWLINE = "\n"
        INDENT_TEXT = CHAR_SPACE*indent_spacing

        new_str = INDENT_TEXT 

        for raw_char in raw_str:
            if(raw_char != CHAR_NEWLINE):
                new_str = new_str + raw_char
            else:
                new_str = new_str + raw_char + INDENT_TEXT
        
        return new_str

    def bool_str_to_bool(self,bool_str):
        
        if(bool_str == True):
            json_bool = bool(True)
        else:
            json_bool = bool(False)

        return json_bool

    """
    @brief Create Meta String
    <p>
    "meta": {
        "version": 0,
        "filename": "master_db_linker.kicad_db
    }
    </p>
    """
    def create_meta_str(self):
        basename = os.path.basename(self.db_linker_path)
        meta_dict ={"meta":{DB_JSON_META_VERSION:self.meta_version,DB_JSON_META_FILENAME:basename}}
        meta_str = json.dumps(meta_dict, indent=2)
        meta_str = self.remove_str_brackets(meta_str)
        meta_str = self.indent_str(meta_str,indent_spacing=4)
        meta_str = meta_str + ","
        return meta_str
    
    """
    @brief Create Name String
    <p>
    "name": "My Database Library"
    </p>
    """
    def create_db_name_str(self):
        name_dict = {DB_JSON_TAG_NAME:self.db_name}
        name_str = json.dumps(name_dict, indent=0)
        name_str = self.remove_str_brackets(name_str)
        name_str = self.indent_str(name_str,indent_spacing=4)
        name_str = name_str + ","
        return name_str
    
    """
    @brief Create Description String
    <p>
    "description": "A database of components"
    </p>
    """
    def create_descr_str(self):
        descr_dict = {DB_JSON_TAG_DESCR:self.db_description}
        descr_str = json.dumps(descr_dict, indent=4)
        descr_str = self.remove_str_brackets(descr_str)
        descr_str = self.indent_str(descr_str,indent_spacing=4)
        descr_str = descr_str + ","    
        return descr_str
    
    """
    @brief Create Source String
    <p>
    "source": {
        "type": "odbc",
        "dsn": "",
        "username": "",
        "password": "",
        "timeout_seconds": 2,
        "connection_string": ""
    }
    </p>
    """
    def create_source_str(self):
        source_dict = {DB_JSON_TAG_SRC:
                        {DB_JSON_SRC_TYPE:self.source_type,
                        DB_JSON_SRC_DSN:self.source_dsn,
                        DB_JSON_SRC_USR:self.source_username,
                        DB_JSON_SRC_PSWD:self.source_password,
                        DB_JSON_SRC_TOUT:self.source_timeout,
                        DB_JSON_SRC_CONN_STR:self.source_conn_str
                        }
                    }
        
        source_str = json.dumps(source_dict, indent=2)
        source_str = self.remove_str_brackets(source_str)
        source_str = self.indent_str(source_str,indent_spacing=4)
        source_str = source_str + ","
        return source_str   
    """
    @brief Create Properties String
    <p>
    "properties": {
                "description": "Description",
                "footprint_filters": "Footprint Filters",
                "keywords": "Keywords",
                "exclude_from_bom": "No BOM",
                "exclude_from_board": "Schematic Only"
            }
    </p>
    """
    def create_properties_str(self):

        prop_field_dict = {DB_JSON_PROP_DESC:DB_PROP_PARAM_DESCR,
                    DB_JSON_PROP_FTPF:DB_PROP_PARAM_FTPF,
                    DB_JSON_PROP_KEYWORDS:DB_PROP_PARAM_KEYWORD,
                    DB_JSON_PROP_EXCL_BOM:DB_PROP_PARAM_EXCL_BOM,
                    DB_JSON_PROP_EXCL_BRD:DB_PROP_PARAM_EXCL_BRD
                    }
        
        prop_dict = {DB_JSON_TAG_PROP:prop_field_dict}

        prop_str = json.dumps(prop_dict, indent=2)
        prop_str = self.remove_str_brackets(prop_str)
        prop_str = self.indent_str(prop_str,indent_spacing=4)
        return prop_str         
        
    def get_field_param_tuple_values(self,table,column):

        fp_df = self.field_param_df
        x_df = (fp_df["table"] == table) & (fp_df["column"] == column)  
        indx_num = fp_df[x_df].index[0]

        name_value = fp_df[DB_JSON_FLDS_NAME][indx_num]
        voa_value = fp_df[DB_JSON_FLDS_VOA][indx_num]
        vic_value = fp_df[DB_JSON_FLDS_VIC][indx_num]
        show_name = fp_df[DB_JSON_FLDS_SHOW][indx_num]

        field_tuple = (name_value,voa_value,vic_value,show_name) 
        return field_tuple

    
    """
    @brief Create Libraries String
    <p>
    "libraries": [
        {
            "name": "Resistors",
            "table": "Resistors",
            "key": "Part ID",
            "symbols": "Symbols",
            "footprints": "Footprints",
            "fields": [
                {
                    "column": "MPN",
                    "name": "MPN",
                    "visible_on_add": false,
                    "visible_in_chooser": true,
                    "show_name": true,
                    "inherit_properties": true
                },
                {
                    "column": "Value",
                    "name": "Value",
                    "visible_on_add": true,
                    "visible_in_chooser": true,
                    "show_name": false
                }
            ],
            "properties": {
                "description": "Description",
                "footprint_filters": "Footprint Filters",
                "keywords": "Keywords",
                "exclude_from_bom": "No BOM",
                "exclude_from_board": "Schematic Only"
            }
        }
    """
    def create_libraries_str(self,table_list,fields_list):
        lib_json_list = []
        field_json_list = []

        for table in table_list:
            for indx,field in enumerate(fields_list):

                (name_value,voa_value_str,vic_value_str,show_name_str) = self.get_field_param_tuple_values(table,field)
            
                voa_value_bool = self.bool_str_to_bool(voa_value_str) 
                vic_value_bool = self.bool_str_to_bool(vic_value_str)
                show_name_bool = self.bool_str_to_bool(show_name_str)
                # filter Part_ID, Symbols, Footprints,and Description from
                # field parameter JSON tags 
                filter_logic = (field != DB_DEFAULT_SYMBOLS) and \
                               (field != DB_DEFAULT_FOOTPRINTS) and \
                               (field != DB_DEFAULT_KEY)and \
                               (field != DB_JSON_TAG_DESCR)
                               
                if(filter_logic):

                    field_item_dict = {DB_JSON_FLDS_COL:fields_list[indx],
                                DB_JSON_FLDS_NAME:name_value,
                                DB_JSON_FLDS_VOA:voa_value_bool,
                                DB_JSON_FLDS_VIC:vic_value_bool,
                                DB_JSON_FLDS_SHOW:show_name_bool}
                    
                    field_json_list.append(field_item_dict)

        

            table_dict = { DB_JSON_LIB_NAME:table,
                        DB_JSON_LIB_TABLE:table,
                        DB_JSON_LIB_KEY:self.db_key,
                        DB_JSON_LIB_SYM:DB_DEFAULT_SYMBOLS,
                        DB_JSON_LIB_FP:DB_DEFAULT_FOOTPRINTS,
                        DB_JSON_LIB_FIELDS:field_json_list,
                        DB_JSON_TAG_PROP:PROPERTIES_FIELD_DICT

                        
                    }
            
            field_json_list = []
            

            lib_json_list.append(table_dict)
            
        lib_dict = {DB_JSON_TAG_LIB:lib_json_list} 
        
        lib_str = json.dumps(lib_dict,indent=4)
        lib_str = self.remove_str_brackets(lib_str)
        lib_str = self.indent_str(lib_str,indent_spacing=4)
        lib_str = lib_str + ","

        return lib_str
    
    def field_param_default_filter(self, table, field):

        column = field
        field_name = field 
        visible_on_add = False
        visible_in_chooser = False
        show_name = False


        # allows show value
        if(field == "Value"):
            visible_on_add = True
            visible_in_chooser = True

        jellybean_bool = (table == "Resistors") or \
                         (table == "Capacitors") or \
                         (table == "Inductors") 
        
        if(jellybean_bool):
            if(field == "Tolerance"):
                visible_on_add = True
                visible_in_chooser = True
            if(field == "Rating"):
                visible_on_add = True
                visible_in_chooser = True  
            if(field == "Package"):  
                visible_on_add = True
                visible_in_chooser = True    
        
        if(table == "Diodes"):
            if(field == "Package"):
                visible_on_add = True
                visible_in_chooser = True    
        
        row_list = [table,column,field_name,visible_on_add,visible_in_chooser,show_name]    

        return row_list   



    def create_field_param_csv(self,csv_path):


        with open(csv_path, 'w', newline='') as outcsv:
            writer = csv.writer(outcsv)
            writer.writerow(f_params_csv_headers)
            row_list = []
            for table in KICAD_TABLE_NAME_LIST:
                for field in KICAD_FIELD_NAME_LST:

                    row_list = self.field_param_default_filter(table, field)
                    writer.writerow(row_list)

    def create_kicad_json_str(self,tag_list):
        file_str = "{\n"

        for tag in tag_list:
            file_str = file_str + tag + "\n"
        
        file_str = file_str + "\n}"

        return file_str
    
    def populate_list(self,list_value,num_of_items):
        new_list = []
        for n in range(num_of_items):
            new_list.append(list_value)

        return new_list
        
    
 
    
    
if(__name__ == '__main__'):
    db_linker = kicad_db_linker()
    db_linker.set_db_linker_path(KICAD_LINKER_PATH)
    db_linker.create_field_param_csv(FIELD_PARAMS_CSV_PATH)

    db_linker.db_name = "Master_Kicad_Database"
    db_linker.db_description = "Master Custom Database"
    meta_str = db_linker.create_meta_str()
    name_str = db_linker.create_db_name_str()
    descr_str = db_linker.create_descr_str()
    src_str = db_linker.create_source_str()
  
    db_linker.set_field_param_df(field_params_csv_path=FIELD_PARAMS_CSV_PATH)
   
    fp_df = db_linker.field_param_df.head()

    lib_str = db_linker.create_libraries_str(table_list=KICAD_TABLE_NAME_LIST,
                                   fields_list=KICAD_FIELD_NAME_LST)
                                   

    tag_list =[meta_str,name_str,descr_str,src_str,lib_str]
    db_linker_body = "{\n"
    for tag in tag_list:
        db_linker_body = db_linker_body +tag +"\n"

    db_linker_body = db_linker_body.strip()
    db_linker_body = db_linker_body[:-1]
    db_linker_body = db_linker_body + "\n}"

    f = open(KICAD_LINKER_PATH, "w")
    f.write(db_linker_body)
    f.close()

    
    


