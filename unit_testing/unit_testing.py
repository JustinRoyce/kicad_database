##
# UNIT TESTING FOR DATABASE 
#
import os
import sys
import shutil
from termcolor import colored, cprint
from rich.console import Console
from rich.table import Table

##
# TERMINAL COLOR VARIABLES
#
TERMC_DEFAULT = "green"
TERMC_ERROR = "red"
TERMC_WARNING = "yellow"
TERMC_SUCCESS = "green"
TERMC_INFO = "black"

###############################
# SET ROOT DIRECTORY FOR
# PYTHON INTERPRETER
###############################
UNIT_TESTING_DIR = os.path.dirname(__file__)
os.chdir(UNIT_TESTING_DIR)
os.chdir("..")
ROOT_DIR = os.getcwd()
sys.path.insert(1, ROOT_DIR)
################################

TESTING_BAY_DIR= os.path.join(UNIT_TESTING_DIR,"testing_bay")
TEST_DB_NAME = "test_database.sqlite3"
TEST_DB_PATH = os.path.join(TESTING_BAY_DIR,TEST_DB_NAME)

from Kicad_Database import Kicad_Database

##
# @brief remove all files in testing bay directory
#
def test_clean_bay_dir():
    for root, dirs, files in os.walk(TESTING_BAY_DIR):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))


##
# creates new kicad database
#
def test_db_creation(kicad_db_class:Kicad_Database,db_path:str):
    status_bool, status_msg = kicad_db_class.create_new_kicad_table(db_path = db_path)
    if(status_bool):
        cprint(status_msg,TERMC_INFO)
    else:
        cprint(status_msg,TERMC_ERROR)

    
    return status_bool


###
# print database info
#
def print_database_info(kicad_db):


     
    # print database information
    pragma_info = kicad_db.get_datebase_pragma_info(kicad_db.get_SQL_connect())
    database_msg = colored("DATA PATH: ",TERMC_DEFAULT)
    database_path = colored(pragma_info[0][2],TERMC_INFO)
    print(database_msg + database_path) 

    table_list = kicad_db.get_tables_list()
    table_msg = colored("AVAILABLE TABLES: ",TERMC_DEFAULT)
    table_str= colored(table_list,TERMC_INFO)
    print(table_msg + table_str )
    table_count_dict = {}
    for table in table_list:
        table_count = kicad_db.get_SQL_row_count(table_name = table)
        table_count_dict[table] = table_count

    console = Console()

    table = Table(show_header=True, header_style="Green")
    table.add_column("Table")
    table.add_column("Number of Line Items")
    
    for key in table_count_dict:
        table.add_row(key,str(table_count_dict[key]))
    
    console.print(table)

def test_part_id_format(kicad_db):
    cprint("*** Testing Number to String Function with Leading Zeros ***", TERMC_DEFAULT)
    base = 9.456
    for i_val in range(0,9):
        expon = pow(10,i_val)
        test_num = int(base*expon)   
        str_num = kicad_db.int2num_str(test_num)
        print("")
        cprint("\t*** test {} ***".format(str(i_val + 1 )),TERMC_DEFAULT)
        print("\ttest number = " + str(test_num) + " has " +str(len(str(test_num))) + " digits")
        print("\toutput number = " + str_num )





##
# validates if kicad database structure
#
def test_db_validation(kicad_db_class:Kicad_Database):

    pass


def test_main():
    print("")
    cprint("****** TESTING STARTED ******",TERMC_DEFAULT)
    

    kicad_db = Kicad_Database()
    # clear directory of all file and folders
    test_clean_bay_dir()
   
    # create new database 
    db_creation_bool = test_db_creation(kicad_db_class=kicad_db,db_path=TEST_DB_PATH)

    #create sql connection and set with kicad class 
    sql_conn, conn_msg = kicad_db.create_connection(db_path=TEST_DB_PATH)
    
    if(sql_conn):
        #set conn
        kicad_db.set_SQL_connect(sql_conn)
        kicad_db.set_database_path(TEST_DB_PATH)
        cprint("Database Connection is Set",TERMC_SUCCESS)
    else:
        cprint("SQL Connection Failed",TERMC_ERROR)
        print(conn_msg)
        return 0

    # get database information
    print("")
    cprint("**** DATABASE INFO: *****",TERMC_DEFAULT)
    print_database_info(kicad_db=kicad_db)

    test_part_id_format(kicad_db)

    #test_db_validation(kicad_db_class=kicad_db)

    #return 0


if "__main__" == __name__:
    test_main()
