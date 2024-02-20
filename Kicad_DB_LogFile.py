"""
Logfile formate

<date time(YYYY-MM-DD THH:MM:SS) >;TABLE <table>;<field>;LOGSTATE  

"""
import os
import datetime


LOG_STATE_CREATED = "CREATED: "
LOG_STATE_MOD = "MODIFIED: " 
LOG_STATE_DELETE = "DELETED: "

class Kicad_DB_LogFile():
    def __init__(self):
        pass

    def make_str_log_time(self):
        now = datetime.datetime.now()
        log_str = now.strftime("%Y-%m-%d T%H:%M:%S; ")
        return log_str

if('__main__' == __name__ ):
    logfile = Kicad_DB_LogFile()
    dt_str = logfile.make_str_log_time()
    print(dt_str) 
    pass