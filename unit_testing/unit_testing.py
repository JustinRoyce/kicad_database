##
#
#
import os
import sys
import shutil

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
    print(status_msg)
    return status_bool

##
# validates if kicad database structure
#
def test_db_validation(kicad_db_class:Kicad_Database):
    pass

def test_main():
    print("")
    print("****** START ******")
    print("working!!!")

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
        print("Connection Set")
    else:
        print("SQL Connection Failed")
        print(conn_msg)
        return 0

    # get database information

    kicad_db.get_datebase_pragma_info(kicad_db.get_SQL_connect())

    #test_db_validation(kicad_db_class=kicad_db)

    #return 0


if "__main__" == __name__:
    test_main()
