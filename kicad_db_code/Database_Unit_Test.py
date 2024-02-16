from Kicad_Database import *
from termcolor import colored
def utest_connection(db_path):
    Kicad_DB = Kicad_Database()

    colored_txt = colored("Testing Database Connectivity ...","yellow") 
    print(colored_txt)

    (conn,status_msg) = Kicad_DB.create_connection(db_path=db_path)

    Kicad_DB.set_SQL_connect(conn)
    if(status_msg == STATUS_MSG_VALID):
        
        print_msg = colored("DATABASE: ","yellow") + Kicad_DB.database_path + colored(" EXISTS!!!","yellow")
        print(print_msg)
    else:
        print_msg = colored("DATABASE: ","red") + Kicad_DB.database_path + colored(" DOES NOT EXISTS!!!","red")
        print(print_msg)

    colored_txt = colored("Closing Database ...","yellow") 
    print(colored_txt)

    is_DB_closed = Kicad_DB.close_DB_connection()
    if(is_DB_closed == True):
        colored_txt = colored("Database is Closed","green")
        print(colored_txt)
    else:
        colored_txt = colored("Database is NOT Closed","red")
        print(colored_txt)
    

    


if "__main__" == __name__ :

    db_path = KICAD_DB_CODE_PATH
    #db_path = "/hjsadhash"
    
    utest_connection(db_path)
