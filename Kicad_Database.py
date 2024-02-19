##
# Class to create Kicad Database that is a wrapper for sqlite functions
# to modify kicad databases

import sqlite3
from sqlite3 import Error
import os
import pandas as pd
import time
import numpy as np
import glob2
from termcolor import colored, cprint
from inspect import currentframe, getframeinfo
import pathlib 

""" CREATE  FILE PATHS """

KICAD_DB_CODE_PATH = __file__
SCRIPT_DIRECTORY = os.path.dirname(__file__)
(DB_ROOT_DIR, _) = os.path.split(SCRIPT_DIRECTORY)

DATABASE_FOLDER = "kicad_database" 
DATABASE_NAME  = "master_component_db.sqlite3"
DATABASE_DIR_PATH = os.path.join(DB_ROOT_DIR,DATABASE_FOLDER)
DEFAULT_DB_PATH = os.path.join(DATABASE_DIR_PATH,DATABASE_NAME)

TEST_CSV_NAME = "test_db_csv.csv"
TEST_CSV_PATH = os.path.join(SCRIPT_DIRECTORY,TEST_CSV_NAME)

CSV_TABLES_DIRNAME = "kicad_db_csv_tables"
CSV_TABLE_DIR = os.path.join(DB_ROOT_DIR,CSV_TABLES_DIRNAME)


### START CONSTANT VARIABLE ###
EMPTY_STR = ""
STATUS_MSG_VALID = "OK"
CSV_FILE_EXTENSION = "csv"
KICAD_DB_EXTENSION = "sqlite3"

TBL_NAME_RESISTOR  = "Resistors"
TBL_NAME_CAPACITOR = "Capacitors"
TBL_NAME_INDUCTOR  = "Inductors"
TBL_NAME_DIODE     = "Diodes"
TBL_NAME_TRANSISTOR = "Transistors"
TBL_NAME_CONNECTOR = "Connectors"
TBL_NAME_IC = "Integrated_Circuits"
TBL_NAME_FUSE = "Fuses"
TBL_NAME_RELAY = "Relays"
TBL_NAME_OSCILLATOR = "Oscillators"
TBL_NAME_SWITCH = "Switches"
TBL_NAME_MISC = "Misc"

PART_ID_PREFIX_RESISTOR  = "RES"
PART_ID_PREFIX_CAPACITOR = "CAP"
PART_ID_PREFIX_INDUCTOR  = "IND"
PART_ID_PREFIX_DIODE     = "DIO"
PART_ID_PREFIX_TRANSISTOR = "TRAN"
PART_ID_PREFIX_CONNECTOR = "CONN"
PART_ID_PREFIX_IC = "IC"
PART_ID_PREFIX_FUSE = "FUS"
PART_ID_PREFIX_RELAY = "REL"
PART_ID_PREFIX_OSCILLATOR = "OSC"
PART_ID_PREFIX_SWITCH = "SW"
PART_ID_PREFIX_MISC = "MISC"

PART_ID_PREFIX_DICT = {
    TBL_NAME_RESISTOR:PART_ID_PREFIX_RESISTOR,
    TBL_NAME_CAPACITOR:PART_ID_PREFIX_CAPACITOR,
    TBL_NAME_INDUCTOR:PART_ID_PREFIX_INDUCTOR,
    TBL_NAME_DIODE:PART_ID_PREFIX_DIODE,
    TBL_NAME_TRANSISTOR:PART_ID_PREFIX_TRANSISTOR,
    TBL_NAME_CONNECTOR:PART_ID_PREFIX_CONNECTOR,
    TBL_NAME_IC:PART_ID_PREFIX_IC,
    TBL_NAME_FUSE:PART_ID_PREFIX_FUSE,
    TBL_NAME_RELAY:PART_ID_PREFIX_RELAY,
    TBL_NAME_OSCILLATOR:PART_ID_PREFIX_OSCILLATOR,
    TBL_NAME_SWITCH:PART_ID_PREFIX_SWITCH,
    TBL_NAME_MISC:PART_ID_PREFIX_MISC
}


#reference designators
TBL_RD_RESISTOR  = "R" 
TBL_RD_CAPACITOR = "C"
TBL_RD_INDUCTOR  = "L"
TBL_RD_DIODE     = "D, LED"
TBL_RD_TRANSISTOR = "Q"
TBL_RD_CONNECTOR = "CONN,P,J"
TBL_RD_IC = "U"
TBL_RD_FUSE = "F"
TBL_RD_RELAY = "R"
TBL_RD_OSCILLATOR = "XTAL,Y"
TBL_RD_SWITCH = "SW"
TBL_RD_MISC = "???"

SQLITE_EXTENSION_LIST = [".sqlite", 
".sqlite3", 
".db", 
".db3", 
".s3db", 
".sl3"]


KICAD_TABLE_NAME_LIST = [
    TBL_NAME_RESISTOR,
    TBL_NAME_CAPACITOR,
    TBL_NAME_INDUCTOR,
    TBL_NAME_DIODE,
    TBL_NAME_TRANSISTOR,
    TBL_NAME_CONNECTOR,
    TBL_NAME_IC,
    TBL_NAME_FUSE,
    TBL_NAME_RELAY,
    TBL_NAME_OSCILLATOR,
    TBL_NAME_SWITCH,
    TBL_NAME_MISC
]

KICAD_TABLE_RD_LIST = [
    TBL_RD_RESISTOR,
    TBL_RD_CAPACITOR,
    TBL_RD_INDUCTOR,
    TBL_RD_DIODE,
    TBL_RD_TRANSISTOR,
    TBL_RD_CONNECTOR,
    TBL_RD_IC,
    TBL_RD_FUSE,
    TBL_RD_RELAY,
    TBL_RD_OSCILLATOR,
    TBL_RD_SWITCH,
    TBL_RD_MISC
]

MAX_STR_NUM_LEN = 5

# sqlite3 datatypes
FIELD_DATATYPE_NULL = "NULL"
FIELD_DATATYPE_TEXT = "TEXT"
FIELD_DATATYPE_INTEGER = "INTEGER"
FIELD_DATATYPE_REAL = "REAL"
FIELD_DATATYPE_BLOB = "BLOB"

# kicad field names
KICAD_FIELD_PART_ID = "Part_ID"
KICAD_FIELD_DESCR = "Description"
KICAD_FIELD_MPN = "MPN"
KICAD_FIELD_SYMBOL = "Symbols"
KICAD_FIELD_FOOTPRINT = "Footprints"
KICAD_FIELD_MANUFACT = "Manufacturer"
KICAD_FIELD_DIGIKEY_PN = "Digikey_PN"
KICAD_FIELD_MOUSER_PN = "Mouser_PN"
KICAD_FIELD_LCSC_PN = "LCSC_PN"
KICAD_FIELD_MISC_DISTR = "Misc_Distributor"
KICAD_FIELD_MISC_PN = "Misc_PN"
KICAD_FIELD_MISC_LINK = "Misc_Link"
KICAD_FIELD_MISC_TOL = "Tolerance"
KICAD_FIELD_MISC_RATING = "Rating"
KICAD_FIELD_PACKAGE = "Package"
KICAD_FIELD_NOTES = "Notes"

KICAD_FIELD_NAME_COUNT = 17
KICAD_FIELD_KEY = "Part_ID"

KICAD_FIELD_NAME_LST = [
    "Part_ID",
    "Value",
    "Description",
    "MPN",
    "Symbols",
    "Footprints",
    "Datasheet",
    "Manufacturer",
    "Digikey_PN",
    "Mouser_PN",
    "LCSC_PN",
    "Misc_Distributor",
    "Misc_PN",
    "Misc_Link",
    "Tolerance",
    "Rating",
    "Package",
    "Notes"
]

""" END  CONSTANT VARIABLE """

##
# Class to create Kicad Database that is a wrapper for sqlite functions
# to modify kicad databases
class Kicad_Database:
    def __init__(self):

        self.database_path = EMPTY_STR
        self.SQL_connect = None
        self.curr_table = EMPTY_STR #current table
        self.field_query = EMPTY_STR

        self.fld_part_id = EMPTY_STR
        self.fld_value = EMPTY_STR
        self.fld_description = EMPTY_STR
        self.fld_mpn = EMPTY_STR
        self.fld_symbol = EMPTY_STR
        self.fld_footprint = EMPTY_STR
        self.fld_datasheet = EMPTY_STR
        self.fld_manufacturer = EMPTY_STR
        self.fld_digikey_PN = EMPTY_STR
        self.fld_mouser_PN = EMPTY_STR
        self.fld_LCSC_PN = EMPTY_STR
        self.fld_misc_distributor = EMPTY_STR
        self.fld_misc_PN = EMPTY_STR
        self.fld_misc_link = EMPTY_STR
        self.fld_tolerance = EMPTY_STR
        self.fld_rating = EMPTY_STR
        self.fld_package = EMPTY_STR
        self.fld_notes = EMPTY_STR

        self.fld_mfunct_lst = []

    
    ## 
    # @brief add double quotes to string    
    def add_str_quotes(self, raw_str):
        quote_str = "\"" + raw_str + "\""
        return quote_str


    ##
    # @brief confirms if the file is a SQL extension 
    # @return true if file path extension is sqlite3 
    #
    def is_sql_extension(self, file_path):
        is_sql_ext = False
        file_ext = pathlib.Path(file_path).suffix
        for sql_ext in SQLITE_EXTENSION_LIST:
            if(file_ext == sql_ext):
                is_sql_ext = True
                break
        
        return is_sql_ext


    def int2num_str(self,integer,tailing_zeros = 7):
        # calculate number of zeros

        if(integer >= 100000):
            num_of_digits = 7
        elif(integer <= 999999 and integer >= 100000): 
            num_of_digits = 6
        elif(integer <= 99999 and integer >= 10000): 
            num_of_digits = 5
        elif(integer <= 9999 and integer >= 1000): 
            num_of_digits = 4
        elif(integer <= 999 and integer >= 100): 
            num_of_digits = 3
        elif(integer <= 99 and integer >= 10): 
            num_of_digits = 2
        elif(integer <= 9 and integer >= 0):
            num_of_digits = 1
        else: 
            num_of_digits = 7

        num_of_zeros = tailing_zeros - num_of_digits
        str_num = "" 
        
        for _ in range(num_of_zeros):
            str_num = str_num + '0'

        int_str_value = str(integer)
        int_str_len = len(int_str_value)
        if(int_str_len > tailing_zeros):
            i_loc = int_str_len-tailing_zeros
            int_str_value = int_str_value[i_loc:]

        str_num = str_num + int_str_value
        
        return str_num


    def create_part_id (self, table, number):
        
        # TODO: add functionally  
        pass 



    ## 
    #@brief updates field list of member functions
    def update_fld_lst(self):
        self.fld_mfunct_lst = [
            self.fld_part_id,
            self.fld_value,
            self.fld_description,
            self.fld_mpn,
            self.fld_symbol,
            self.fld_footprint,
            self.fld_datasheet,
            self.fld_manufacturer,
            self.fld_digikey_PN,
            self.fld_mouser_PN,
            self.fld_LCSC_PN,
            self.fld_misc_distributor,
            self.fld_misc_PN,
            self.fld_misc_link,
            self.fld_tolerance,
            self.fld_rating,
            self.fld_package,
            self.fld_notes]

    ##
    #@brief set database path before running any other functions 
    def set_database_path(self, db_path):
        self.database_path = db_path
        return None
    
    ##
    # @brief set SQL connect class as member function of class
    def set_SQL_connect(self,SQL_connect):
        self.SQL_connect = SQL_connect
        return None
    
    def get_SQL_connect(self):
        return self.SQL_connect
    
    ##
    #@brief: resets all field parameter to NULL string 
    def reset_field_params(self):

        self.fld_part_id = EMPTY_STR
        self.fld_symbol = EMPTY_STR
        self.fld_value = EMPTY_STR
        self.fld_footprint = EMPTY_STR
        self.fld_datasheet = EMPTY_STR
        self.fld_manufacturer = EMPTY_STR
        self.fld_mpn = EMPTY_STR
        self.fld_digikey_PN = EMPTY_STR
        self.fld_mouser_PN = EMPTY_STR
        self.fld_LCSC_PN = EMPTY_STR
        self.fld_misc_distributor = EMPTY_STR
        self.fld_misc_PN = EMPTY_STR
        self.fld_misc_link = EMPTY_STR
        self.fld_tolerance = EMPTY_STR
        self.fld_rating = EMPTY_STR
        self.fld_package = EMPTY_STR
        self.fld_description = EMPTY_STR
        self.fld_notes = EMPTY_STR
        return None
    ##
    # @brief get database field list
    def get_DB_field_list(self):
        return KICAD_FIELD_NAME_LST
    
    ##
    # @brief get database table list
    def get_DB_table_list(self):
        return KICAD_TABLE_NAME_LIST

    
    ##
    # @brief open connection to database
    def open_DB_connection(self):
        conn, status_msg = self.create_connection(db_fpath=self.database_path)
        connect_bool = False
        if(status_msg == STATUS_MSG_VALID):
            connect_bool = True
            self.SQL_connect = conn
        
        return (connect_bool,status_msg)
    

    ##
    # close DB connection 
    def close_DB_connection(self):

        connect_bool = False
        print(type(self.SQL_connect))
        if(type(self.SQL_connect) == (sqlite3.Connection)):
            self.SQL_connect.close()
            connect_bool = True

        return connect_bool
    

    ##
    # get tables list 

    def get_tables_list(self):

        sql_conn = self.get_SQL_connect()
        sql_query = """SELECT name FROM sqlite_master 
        WHERE type='table';"""
    
        # Creating cursor object using connection object
        cursor = sql_conn.cursor()
        
        # executing our sql query
        cursor.execute(sql_query)
        
        # printing all tables list
        truple_list = cursor.fetchall()
        table_list = []
        for truple in truple_list:
            if(truple):
                table_list.append(truple[0])
        return table_list
        
    ##
    # get SQL row count
    #
    def get_SQL_row_count(self,table_name):

        sql_conn = self.get_SQL_connect()
        b_table_exist, _ = self.does_table_exist(table_name=table_name)
        
        if (b_table_exist):
        
            sql_query = "SELECT COUNT(*) FROM " + table_name + " ;"
        
            # Creating cursor object using connection object
            cursor = sql_conn.cursor()
            
            # executing our sql query
            cursor.execute(sql_query)
            
            # printing all tables list
            result = cursor.fetchone()
            row_count= result[0]
            cursor.close()

            return row_count
        else:
            return -1

            

    
    ##
    # @brief set field member functions with member function list
    def set_field_mfunct_wt_list(self, mfunct_list):
        mfunct_list_len = len(mfunct_list)
        if(mfunct_list_len == KICAD_FIELD_NAME_COUNT):
            self.fld_part_id = mfunct_list[0]
            self.fld_value = mfunct_list[1]
            self.fld_description = mfunct_list[2]
            self.fld_mpn = mfunct_list[3]
            self.fld_symbol = mfunct_list[4]
            self.fld_footprint = mfunct_list[5]
            self.fld_datasheet = mfunct_list[6]
            self.fld_manufacturer = mfunct_list[7]
            self.fld_digikey_PN = mfunct_list[8]
            self.fld_mouser_PN = mfunct_list[9]
            self.fld_LCSC_PN = mfunct_list[10]
            self.fld_misc_distributor = mfunct_list[11]
            self.fld_misc_PN = mfunct_list[12]
            self.fld_misc_link = mfunct_list[13]
            self.fld_tolerance = mfunct_list[14]
            self.fld_rating = mfunct_list[15]
            self.fld_package = mfunct_list[16]
            self.fld_notes = mfunct_list[17]
            
            status_msg = STATUS_MSG_VALID
            return_tuple = (True,status_msg)
        
        else:
                        
            status_msg = "Invalid Length:" + str(mfunct_list_len) + \
                        " vs " + str(KICAD_FIELD_NAME_COUNT) 
            return_tuple = (False,status_msg)
        
        return return_tuple 

    ##
    # @brief Create field list with member function
    def create_f_list_wt_mfunct(self):
        mfunct_list = []
        self.fld_part_id = self.add_str_quotes(self.fld_mpn)

        mfunct_list.append(self.fld_part_id)  
        mfunct_list.append(self.fld_value)
        mfunct_list.append(self.fld_description) 
        mfunct_list.append(self.fld_mpn) 
        mfunct_list.append(self.fld_symbol)   
        mfunct_list.append(self.fld_footprint) 
        mfunct_list.append(self.fld_datasheet) 
        mfunct_list.append(self.fld_manufacturer) 
        mfunct_list.append(self.fld_digikey_PN) 
        mfunct_list.append(self.fld_mouser_PN) 
        mfunct_list.append(self.fld_LCSC_PN) 
        mfunct_list.append(self.fld_misc_distributor) 
        mfunct_list.append(self.fld_misc_PN) 
        mfunct_list.append(self.fld_misc_link)
        mfunct_list.append(self.fld_tolerance) 
        mfunct_list.append(self.fld_rating) 
        mfunct_list.append(self.fld_package) 
        mfunct_list.append(self.fld_notes)

        return mfunct_list
    
    ##
    # @brief returns csv path list from directory path
    # @param csv_dir directory path of csv file
    def get_csv_path_list(self,csv_dir):
        csv_glob_filter = "*.csv"
        csv_glob_regex = os.path.join(csv_dir,csv_glob_filter)    
        csv_path_list = glob2.glob(csv_glob_regex)
        csv_path_list.sort()
        return csv_path_list
    
    
    def get_table_name_from_path(self,csv_path,table_list=KICAD_TABLE_NAME_LIST):

        status_bool = False
        table_name = ""
        # get base name and remove .csv
        base_name = os.path.basename(csv_path)
        base_name = base_name[:-4]
        
        if base_name in table_list:
            status_bool = True
            table_name = base_name
        
        return_tuple = (table_name,status_bool)
        return return_tuple

    def vs_debug_linker_str(self,script_path,line_number):
        linker_str = "vscode://file/" + script_path +":" + str(line_number)      
        return linker_str
    
    def get_vs_dlinker_str(self,cf):
        
        filename = getframeinfo(cf).filename
        line_number = cf.f_lineno
        linker_str = "vscode://file/" + filename +":" + str(line_number)

        vs_dlinker = colored("SEE LINK FOR DETAILS: ","yellow") + colored(linker_str,"blue")  
        return vs_dlinker    

    ##
    # @brief turns a python list into tuple
    # ["cat","bat","rat"] ==> "("cat","bat","rat")"
    def create_lst_2_tuple_str(self,lst):
        tuple_str = "("
        for item in lst:

            tuple_str = tuple_str + str(item) + ","
        
        tuple_str = tuple_str.strip()
        tuple_str = tuple_str[:-1]
        
        tuple_str = tuple_str + ")"

        return tuple_str

    ##
    # @brief create update SQL str
    #
    def create_update_sql_str(self,table_name,field_list,df):
        

        sql_str = "UPDATE " + table_name + "\nSET "
        index = 0
        for field in KICAD_FIELD_NAME_LST:
            
            if(field == KICAD_FIELD_KEY):
                db_key = field_list[index]
            else:
                
                field_str = field + " = \'" + field_list[index] 
                sql_str = sql_str + field_str +"\',"
            
            index = index + 1

        sql_str = sql_str[:-1] + "\n"
        sql_str = sql_str + "WHERE " + KICAD_FIELD_KEY + " = \'" + db_key + "\';"

        return sql_str

    ##
    # @brief prints kicad table names
    #
    def print_kicad_table_names(self):
        cprint("\nKICAD TABLE NAMES LIST:","cyan")
        for index, kicad_table in enumerate(KICAD_TABLE_NAME_LIST):
            print("(" + str(index+1)+ "): " + kicad_table)
        return None
    
    ##
    # @brief prints kicad fields names
    #
    def print_kicad_fields_names(self):
        cprint("\nKICAD FIELDS NAMES LIST:","cyan")
        for index, kicad_field in enumerate(KICAD_FIELD_NAME_LST):
            print("(" + str(index+1)+ "): " + kicad_field)
        return None    
    
    ## 
    # @brief create a database connection to the SQLite database <br> 
    # specified by db_file
    # @param db_fpath is the database file path
    # @return: Connection tuple (connect class, status msg)
    #
    def create_connection(self, db_path:str):
        
        try:
            conn = sqlite3.connect(db_path)
            status_msg = STATUS_MSG_VALID
            connect_tuple = (conn,status_msg)
            
        except Error as e:
            conn = None
            status_msg = "Connection Error:"+ str(e)
            connect_tuple = (conn,status_msg)
            return connect_tuple    

        return connect_tuple 

    ##
    # @brief  run sql execute command
    # @param execute_str  command string to execute sql command 
    def run_sql_execute(self,execute_str):
        conn = self.SQL_connect
        try:
            cur = conn.cursor()
            cur.execute(execute_str)
            conn.commit()
            cur.close()
        except sqlite3.Error as err:
            status_msg = "SQL ERROR: " + err
            return_tuple = (False,status_msg)
            return return_tuple
        
        status_msg = STATUS_MSG_VALID
        return_tuple = (True,status_msg)
        return return_tuple
    

    ##
    # #brief get pragma information
    #
    def get_datebase_pragma_info(self,sql_conn):
    
        cur = sql_conn.cursor()
        cur.execute("PRAGMA database_list")
        rows = cur.fetchall()
        pragma_info_list = []
        for row in rows:
            pragma_info_list.append(row)
        return pragma_info_list

    ##
    # @brief confirms if table exists
    # @return true if table exists and false if no table exists as well as
    # status message
    def does_table_exist(self,table_name):

        conn = self.SQL_connect

        sql_str = "SELECT name FROM sqlite_master WHERE type='table' AND  name= \'" + table_name + "\'"
        cur = conn.cursor()
        tables_list = cur.execute(sql_str).fetchall()
        cur.close()
        
        b_table_exists = False
        # if empty no table exists
        if(tables_list == []):
            b_table_exists = False
            status_msg = "EMPTY TABLE"
        else:
            b_table_exists = True
            status_msg = STATUS_MSG_VALID
        
        return (b_table_exists,status_msg)
    
    ##
    # @brief delete sql table 
    # @param table_name is table name to be deleted
    # @return status tuple where: (table deleted boolean, status message)
    #
    def delete_sql_table(self, table_name):
        
        conn = self.SQL_connect
        sql_str = "DROP TABLE IF EXISTS " + table_name + ";"
        cur = conn.cursor()
        cur.execute(sql_str)
        cur.close()
        conn.close()
        status_msg = STATUS_MSG_VALID
        status_turple = (True, status_msg)
        return status_turple
    
    ##
    # does field/ record exist 
    #

    def does_record_exist(self,table,column, value):
        conn = self.SQL_connect

        exe_str  = "SELECT 1 FROM " + table + " WHERE " + column + "="+ value +";"
        

        pass

    ##
    # @brief does MPN exist
    # @param table to be accessed
    # @param MPN_str string exists True is returned
    # @return status tuple where: (table deleted boolean, status message)
    #
    def does_MPN_exist(self,table,MPN_str):

        conn = self.SQL_connect

        
        sql_str = "SELECT " + KICAD_FIELD_MPN.strip() + " FROM " + table
        
        try:
            df = pd.read_sql(sql_str, conn)
        except sqlite3.OperationalError as e:
            status_msg = "SQL OPERATION ERROR:" + e 
            return_tuple = (False, status_msg)
            return return_tuple
    
        MPN_exists = False
        status_msg = STATUS_MSG_VALID
        # check if list is empty
        if df.empty:
            MPN_exists = False
        else:
            MPN_exists = (df.eq(MPN_str)).any().bool()

        return_tuple = (MPN_exists,status_msg)
        
        
        return return_tuple

    ##
    # @brief uses field list to create sql values str used in param varible of sql
    # cursor execute wrapper function
    # ie: [cat, bat, rat] ==> 'VALUES(?,?,?)'
    #
    def create_sql_params_str(self,field_list):
        value_str = "VALUES("
        for field in field_list:
            value_str = value_str + "?" + ","
        value_str = value_str[:-1]
        value_str = value_str + ")"

        return value_str

    ##
    # @brief creates sql value string from list <br>
    # ie: [Part_ID, value, symbol,...] ==> (245,'100uF','Device:C',...) 
    # @param field_value_list list of field values 
    #
    def create_sql_values_str(self,field_value_list):
        
        value_str = "("

        for field in field_value_list:
            field_type = type(field)

            if field_type != "str":
                field = str(field)

            value_str = value_str + "\'"+ field + "\'" + ","    

        value_str = value_str[:-1]
        value_str = value_str + ")"

        return value_str
    
    ##
    # @brief populates a single data type in a list depending on the size of the field list
    # @param data_type data type of the sql table field
    # @param field_list field list of a table
    # @return
    def populate_datatype_list(self, field_list, data_type=FIELD_DATATYPE_TEXT):
        list_size = len(field_list)
        data_type_list = []
        for _ in range(list_size):
            data_type_list.append(data_type)
        return data_type_list



    ##
    # @brief create SQL table in database
    # @param table_name is the new table name
    # @param field_list is a list of fields(column headers) for the SQL database
    # @param datatype_list is the datatype for each field
    def create_sql_table(self,sql_conn,table_name,field_list,datatype_list):
    
        field_type_lst = []
        for index,field in enumerate(field_list):
            field_type_str = field + " " + datatype_list[index]
            field_type_lst.append(field_type_str)

        sql_str = "CREATE TABLE " + table_name + " "    
        tuple_str = self.create_lst_2_tuple_str(field_type_lst)    
        sql_str = sql_str + tuple_str + ";"

        
        # valid connection
        if(sql_conn == None):
            return (False, status_msg)
        
        try: 
            cur = sql_conn.cursor()
            cur.execute(sql_str)
            cur.close()
            status_msg = STATUS_MSG_VALID
            return_tuple = (True,status_msg)
        except sqlite3.Error as error:
            status_msg = "SQL Error: " + error 
            return_tuple = (False,status_msg)

        return return_tuple
    

    def populate_tables_n_fields(self,sql_conn):

        field_list = KICAD_FIELD_NAME_LST
        datatype_list = self.populate_datatype_list(field_list=field_list,data_type=FIELD_DATATYPE_TEXT)
        for table_name in KICAD_TABLE_NAME_LIST:

            status_bool,status_msg = self.create_sql_table(sql_conn,table_name,field_list,datatype_list)
            if(status_bool == False):
                return (status_bool,status_msg)
        
        status_bool = True
        status_msg = "KICAD TEMPLETE TABLES AND FIELDS WERE CREATED FOR DATABASE"
        return status_bool,status_msg



    ##
    # @Todo create new kicad table
    #
    def create_new_kicad_table(self,db_path):
        status_tuple = None

        # check if file exists
        is_file = os.path.isfile(db_path)
        if(is_file):
            status_bool = False
            status_msg = "FILE ALREADY EXISTS: " + db_path
            return (status_bool,status_msg)

        # check for valid SQL file extension
       
        is_sql_ext = self.is_sql_extension(db_path)
        if(is_sql_ext == False):
            status_bool = False
            status_msg = "INVALID SQL EXTENSION: " + db_path
            return (status_bool,status_msg)
        
        #create new blank kicad database
        f = open(db_path, "w")
        f.write("")
        f.close()

        #populate tables and field
        
        (conn,status_msg)  = self.create_connection(db_path=db_path)
        if(conn == None):
            return (False,status_msg)
        
        
        (status_bool,status_msg) = self.populate_tables_n_fields(sql_conn=conn)

        if(status_bool == False):
            return (status_bool,status_msg)
        
        conn.close()

        status_bool = True
        status_msg = "CREATED KICAD DATABASE: " + db_path

        status_tuple = (status_bool, status_msg)
        return status_tuple

    ##
    # @brief Add SQL fields to table SQL command
    # @param table_name name of table
    # @param field_lst list of SQL fields 
    #
    def add_fields2table_cmd(self,table_name,field_lst):
        fields_names = EMPTY_STR
        for field in field_lst:
            fields_names = fields_names + field + " " + FIELD_DATATYPE_TEXT + ","   

        field_names = fields_names[:-1]
        
        exe_cmd = "CREATE TABLE " + table_name  \
        + " (" + field_names +")"

        return exe_cmd

    ##
    # @brief creates a kicad database with field parameters if database does not exists
    # @returns  true or false if database is initialized
    #
    def init_kicad_database(self,db_path):
     
        is_file = os.path.isfile(db_path) 
        if(is_file == True):
            status_msg = colored("DATABASE EXISTS:\n","yellow") + db_path + "\n"
            return_tuple = (False, status_msg)
            return return_tuple
        
        conn = self.SQL_connect
        cur = conn.cursor()

        for table_name in KICAD_TABLE_NAME_LIST:
            table_name_exe = self.add_fields2table_cmd(table_name,KICAD_FIELD_NAME_LST)
            cur.execute(table_name_exe)

        status_msg = colored("DATABASE CREATED:\n","yellow") + db_path + "\n"
        return_tuple = (True, status_msg)

        return return_tuple
    
    ##
    # @brief create csv templates in csv folder path
    # @param csv_path 
    #
    def create_CSV_template(self,csv_path):    
        n = len(KICAD_FIELD_NAME_LST)
        BLANK_LIST = [[]] * n
        name_dict = dict(zip(KICAD_FIELD_NAME_LST, BLANK_LIST))
        df = pd.DataFrame(name_dict)      
        del df[df.columns[0]]
        df.to_csv(path_or_buf=csv_path, index=False)
        
    ##
    # @brief  extract database dataframe from SQL
    # @param table table name 
    # @param db_path database path 
    def get_db_df_from_sql(self,table,db_path):
        db_df = None
        conn = self.SQL_connect
        query_str = "SELECT * from " + table
        
        try:
            db_df = pd.read_sql_query(query_str,con=conn)
        except sqlite3.OperationalError as e:
            status_msg = "SQL OPERATIONAL ERROR: " + e
        
        return_tuple = (db_df, status_msg)
        return return_tuple
    

    ##
    # @brief create kicad csv table templetes
    # @param csv_dir is the csv directory that templates will be created
    def create_csv_tables(self, csv_dir):

        for tables in KICAD_TABLE_NAME_LIST: 
                
            csv_name = tables + ".csv"
            
            csv_path = os.path.join(csv_dir,csv_name)
            file_exists = os.path.exists(csv_path)
        
            if(file_exists):
                print("\nFile already exists:")
                print(csv_path, flush=True)
            else:
                self.create_CSV_template(csv_path)
                print("\n File created:\n%s"%csv_path,flush=True)

    ##
    # @brief  check if csv contains database fields from a python list
    # @param csv_path path of csv path 
    # @param field_list list of field list
    def does_csv_contain_fields(self,csv_path, field_list=KICAD_FIELD_NAME_LST):

        
        # check if file exists
        csv_path_exists = os.path.exists(csv_path)
        if (csv_path_exists == False):
            return_tuple = (False,"NO PATH EXISTS:" + csv_path)
            return return_tuple
       
        # check if dataframe is not empty 
        try:
            csv_df = pd.read_csv(csv_path)
        except pd.errors.EmptyDataError:
            return_tuple = (False,"FILE CONTAINS NO DATA:"+ csv_path)
            return return_tuple
        
        # check if fields match default fields
        csv_fields = [colName for colName in csv_df]
        
        for field in field_list:
            if (field in csv_fields):
                return_tuple = (True,"OK")
            else:
                return_tuple = (False,"FIELD IS MISSING:" + field)
                return return_tuple

        return return_tuple    
   
    ##
    # @brief push member function to table
    # @return status tuple with following format: <br>
    # <br>
    # (status_bool, status msg)<br>
    # status_bool = True if data pushed,otherwise it is False<br>
    # status_msg = status message of the pushing table 
    def push_mfuncts_2_table(self,table):
        
        mpn_value = self.fld_mpn

        if(mpn_value == EMPTY_STR):
            status_msg = "Empty String"
            return_tuple = (False,status_msg)
            return return_tuple
        
        is_MPN_exist = self.does_MPN_exist(table=table,MPN_str=mpn_value)

        if(is_MPN_exist == True):
            status_msg = "MPN Already Exists"
            return_tuple = (False,status_msg)
            return return_tuple
        
        self.fld_part_id = self.add_str_quotes(self.fld_mpn)

        # add member function to table
        conn = self.SQL_connect

        sql_field_str = self.create_lst_2_tuple_str(KICAD_FIELD_NAME_LST)
        self.update_fld_lst()

        value_tuple_str = self.create_sql_values_str(self.fld_mfunct_lst)
        sql_str = "INSERT INTO " + table + sql_field_str + " VALUES" + value_tuple_str 
        
        cur = conn.cursor()
        cur.execute(sql_str)
        conn.commit()        
        status_msg = "Data Pushed to \'" + table + "\' Table" 
        return_tuple = (True, status_msg)
        
        return return_tuple
    
    
    def modified_table(self, table, mfn_field, field_list):
        return_tuple = self.does_MPN_exist(table=table,MPN_str = mfn_field)
        (MPN_exist,status_msg) = return_tuple 
        if(MPN_exist):
            print("MPN exists:",mfn_field) 
            
            update_str = self.create_update_sql_str(table_name=table,field_list=field_list)
            return_tuple = self.run_sql_execute(db_fpath=self.database_path,
                                 execute_str=update_str)
        
        return return_tuple
    
    
    def upload_df_2_sql_db(self,table_name,df, field_name_list = KICAD_FIELD_NAME_LST):
        status_msg = ""
        status_bool = False
        column_len = df.shape[0]
        log_msg = colored("\n*** LOG MESSAGES ***\n","green")
        
        for indx in range(column_len):

            csv_row_df = df.iloc[indx]
            
            # does MPN exist 
            if("MPN" in csv_row_df):
                mpn_str = csv_row_df["MPN"]
                (MPN_in_table, status_msg)  = self.does_MPN_exist(table=table_name,MPN_str=mpn_str)
                
                
                if(status_msg != STATUS_MSG_VALID):
                    status_bool = False
                    return_tuple = (status_bool,status_msg)
                    return return_tuple
            else:
                status_msg = "NO MPN AVAILABLE" + "\n" 
                status_bool = False
                return_tuple = (status_bool,status_msg)
                return return_tuple

            # collect dataframe data into list
            fld_value_list = []
            
            for field_name in field_name_list:

                if(field_name in csv_row_df):
                    field_value = str(csv_row_df[field_name])
                    fld_value_list.append(str(field_value))
                else:
                    if(field_name == KICAD_FIELD_KEY):
                        key_value = self.add_str_quotes(mpn_str)
                        fld_value_list.append(key_value)

                    else:    
                        status_msg = status_msg + "INVALID CSV COLUMN VALUE:" + field_name + "\n" 
                        status_bool = False  

            
            # create connection for database            
            if(MPN_in_table == False):
                #if MPN exist in table, create column
                try:
                    conn = self.SQL_connect
                
                    sql_field_str = self.create_lst_2_tuple_str(lst=field_name_list)
                    value_tuple_str = self.create_sql_values_str(field_value_list=fld_value_list,df = df)
                    sql_str = "INSERT INTO " + table_name + sql_field_str + " VALUES" + value_tuple_str + "\n"
                    cur = conn.cursor()
                    cur.execute(sql_str)
                    log_msg = log_msg + "MPN ITEM: \'" + str(mpn_str) + "\' CREATED FOR \"" + table_name +"\" TABLE\n"
                
                except Exception as e:
                    cf = currentframe()
                    error_line_num = cf.f_lineno + 1
                    status_msg = mpn_str + colored("\nERROR:","red") + str(e) + "\n" + self.get_vs_dlinker_str(cf)  + "\n"
                    return_tuple = (False,status_msg)
                    return return_tuple
                
                
            
            else:
                #if MPN DOES NOT exist in table, modified (update)column
                try:
                    
                    conn = self.SQL_connect
                
                    update_str = self.create_update_sql_str(table_name=table_name,field_list=field_name_list,df=df)
                    print(update_str)
                    return_tuple = self.run_sql_execute(db_fpath=self.database_path,
                                 execute_str=update_str)

                    log_msg = log_msg + "MPN ITEM: \'" + str(mpn_str) + "\' MODIFIED FOR \"" + table_name +"\" TABLE\n"

                
                except Exception as e:

                    cf = currentframe()
                    error_line_num = cf.f_lineno + 1
                    status_msg = mpn_str +"\nERROR:" + str(e) + "\n" + self.get_vs_dlinker_str(cf) 
                    return_tuple = (False,status_msg)
                    return return_tuple

                conn.close()

        return_tuple = (status_msg,log_msg)
        return return_tuple    


    ##
    #@brief lists all tables in database
    def list_tables_in_db(self,db_path):
        table_list = []
        try: 
            sqliteConnection = sqlite3.connect(db_path)
            sql_query = """SELECT tbl_name FROM "main".sqlite_master;"""
           
            cursor = sqliteConnection.cursor()
            cursor.execute(sql_query)
            table_raw_list = cursor.fetchall()
            '''
            format of table_raw_list
            [('Resistors',), ('Capacitors',), ('Inductors',)...]
            
            '''
            for raw_tuple in table_raw_list:
               table_value = raw_tuple[0]
               table_list.append(table_value)
            
            table_list.sort()

        except sqlite3.Error as error:
                print("Failed to execute the above query", error)
        
        finally:
            if(sqliteConnection):
                sqliteConnection.close()
        return table_list


    ##
    # @brief confirms if file is valid kicad database
    def is_valid_kicad_db(self,database_path):
        is_valid_bool = False
        
        # valid if file exist
        is_file_bool = os.path.isfile(database_path)
        if(is_file_bool == False):
            status_msg = "Invalid File Path: " + database_path
            return (is_valid_bool,status_msg)

        # validate file extension
        pathlib_path = pathlib.Path(database_path)
        pathlib_suffix = pathlib_path.suffix
        pathlib_ext = pathlib_suffix[1:]
        if(pathlib_ext != KICAD_DB_EXTENSION ):
            status_msg = "Invalid File Extension: " + pathlib_ext
            return (is_valid_bool,status_msg)

        # is valid sql database
        connection = None 
        try: 
            connection = sqlite3.connect(database_path)
            crsr = connection.cursor()

        except:

            status_msg = "Invalid SQL File: " + database_path
            return (is_valid_bool,status_msg)

        connection.close()

        # list tables
        table_list = self.list_tables_in_db(database_path)
        tables_exists_bool,status_msg = self.does_all_tables_exist(table_list)

        if(tables_exists_bool == False):
            status_msg = "Invalid File Extension: " + pathlib_ext
            return (is_valid_bool,status_msg)

        # list missing field

        is_valid_bool = True
        status_msg = "Kicad Database is Valid"
        return (is_valid_bool, status_msg)

    def get_df_from_csv(self, csv_path):
        
        csv_df = pd.DataFrame()
        # do path exist?
        does_path_exist = os.path.exists(csv_path)
        if(does_path_exist == False):
            status_msg = "INVALID CSV PATH:" + csv_path +  "\n"
            return_tuple = (csv_df,status_msg)
            return return_tuple

        # is csv file extension valid?
        csv_path_len = len(csv_path)
        csv_path_f_ext = csv_path[csv_path_len -3:]
        if csv_path_f_ext != CSV_FILE_EXTENSION:
            status_msg = "INVALID CSV FILE EXTENSION:" + csv_path_f_ext + "\n"
            return_tuple = (csv_df,status_msg)
            return return_tuple

        # get df from csv
        try:
            #note use na_filter=False to remove empty string 
            csv_df = pd.read_csv(csv_path,dtype=str,na_filter=False)
        
        except pd.errors as e:
            status_msg = "PANDAS ERROR:" + e + "\n"
            return_tuple = (csv_df,status_msg)
            return return_tuple
                
        # dataframe ok
        status_msg = STATUS_MSG_VALID
        return_tuple = (csv_df,status_msg)
        return return_tuple
    
    ##
    # @brief doe all table exist in list of tables
    #
    def does_all_tables_exist(self, table_list):
        table_exist_bool = True
        status_msg = "Missing Table(s):"  
        for table_name in KICAD_TABLE_NAME_LIST:
            if not table_name in table_list:
                table_exist_bool = False
                status_msg = status_msg + " " + table_name 

        if(table_exist_bool == True):
            status_msg = "All Tables Exists" 
            return (table_exist_bool,status_msg)
        else:
            return (table_exist_bool,status_msg)

    def import_csv_2_sql_db(self, csv_path, table_name,field_name_list = KICAD_FIELD_NAME_LST,DB_KEY = KICAD_FIELD_KEY):
        log_msg = ""
        
        # does table exist
        (status_bool,status_msg) = self.does_table_exist(table_name=table_name)
        if(status_bool == False):
            return_tuple = (status_bool,status_msg)

        #does csv contain fields
        (status_bool,status_msg) = self.does_csv_contain_fields(csv_path=csv_path,field_list=field_name_list) 
        if(status_bool == False):
            return_tuple = (status_bool,status_msg)

        #create df from csv file
        (csv_df, status_msg)= self.get_df_from_csv(csv_path=csv_path)
        
        if(csv_df.empty ==True):
            status_msg = "DATAFRAME IS EMPTY!!!"
            return_tuple = (False,status_msg )
            return return_tuple

        (status_bool,status_msg) = self.upload_df_2_sql_db(df=csv_df,
                                                           field_name_list=field_name_list,
                                                           table_name=table_name)
        
        return_tuple = (status_bool,status_msg)
        return return_tuple
        
    
        

    

