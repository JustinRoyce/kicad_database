# Kicad Database Information
```
TO PREVIEW INFORMATION AS MARKDOWN IN VSCODE TYPE CTRL + K , THEN V
```

The project is designed to used to access and modify kicad component information via a custom database. This database information will link to kicad schematic. 

Author: Justin Royce 2024

---

# CODE REQUIREMENTS

- query SQL using fields with respect to tables 

- exports cvs files from Database



# FILE STRUCTURE FOR DATABASE PROGRAM

**KEY**
<div> 
    <img alt="folder icon" src="media/folder.svg" width="20"/> 
        folders are <b>bold</b> 
<div>
<div>
    <img alt="folder icon" src="media/file.svg" width="20"/> 
    files are <i>italics</i>
</div> 
<br>
The data structure for the program is as follows:

<div>
    <img alt="folder icon" src="media/folder.svg" width="20"/>
    <b>kicad_database (root directory)</b>
</div>

<div style="position:relative; left:20px;">
    <img alt="folder icon" src="media/folder.svg" width="20"/> 
    <b>export</b> 
    folder contains export information
</div>

<div style="position:relative; left:20px;">
    <img alt="folder icon" src="media/folder.svg" width="20"/> 
    <b>kicad_db_gui_code</b>
</div>    



---
## Kicad Database Format

The kicad database consists of the following tables:

- Capacitors (C)
- Connectors (J,P,USB)
- Diodes (D,LED)
- Fuse (F)
- Inductors (L)
- Integrated_Circuits (U)
- Misc (Any component that does not fall into the other tables)
- Oscillator (Y or XTAL)
- Relay (K)
- Resistors (R)
- Switch (SW)
- Transistors (Q)


The table fields include the following:

- Part_ID - part ID is key of database
- Symbol - kicad symbol
- Value - value like 100nF, 10K 
- Footprint - kicad footprint
- Datasheet - datasheet of component
- Manufacturer - manufacturer of component
- MPN - Manufacturer Part Number
- Digikey_PN - Digikey Part Number
- Mouser_PN - Mouser Part Number
- LCSC_PN - LCSC Part Number
- Misc_Distributor - misc. distributor name like "Amazon.ca"
- Misc_PN - part number that is not Digikey, Mouser, and LCSC
- Misc_Link - misc comnponent link 
- Tolerance - plus and minus 
- Rating - voltage or power rating of the component
- Package - package size in imperial unless specified. ie: 0603 is 0.06 inch x 0.03 inch  
- Description - Description size
- Notes - Notes associated with components

---
## SETTING UP ODBC FOR LINUX

Open Database Connectivity (ODBC) is an open standard Application Programming Interface (API) for accessing a database. Kicad uses ODBC to link parts with database field
parameters like MPN, Package, and etc.  

### STEP #1: Run Apt Package Manager Commands
```
sudo apt update
sudo apt install odbcinst 
sudo apt install libsqliteodbc
```
### STEP #2: Add file information to /etc/odbcinst.ini:

```
[kicad_db]
Description=electronic parts database
Driver=/usr/lib/x86_64-linux-gnu/odbc/libsqlite3odbc.so
Database=/home/royce/projects/masters/design/proj_kicad/master_lib/database/master_component_db.sqlite3
Timeout=2000
```

### STEP #3: Test if database is accessable:

run the command in the terminal:

```
isql kicad_db
```

if you are proprompted with the database is connected, the ODBC kicad database is functioning. 


