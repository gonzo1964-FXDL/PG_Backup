
import pg8000
import time
import datetime
import os
import commands
import subprocess
#
cReaTor = ""
cLeaNer = ""
vieWer = ""
ziPPer = ""
pObject = ""


#pswPath = ""
fileObject ="/ctmpg/.PG/"

today = datetime.date.today()
Today = today.strftime("%y%m%d")
toDay = today.strftime("%y%m")

old_day = datetime.timedelta(days=5)
minus_90 = today - old_day
minus_90 = minus_90.strftime("%y%m%d")

old_day3 = datetime.timedelta(days=3)
minus_3 = today - old_day3
minus_3 = minus_3.strftime("%y%m%d")

old_day1 = datetime.timedelta(days=1)
minus_1 = today - old_day1
minus_1 = minus_1.strftime("%y%m%d")

minus_2 = today - old_day1
ioaLogDelDate = minus_2.strftime("%Y%m%d")


programmUser = os.environ['USER']
#
""" python bin/db_oo.py 

        open
        
        handle password 
        restore mysql
        restore pg
        ioalog
        runinfshout
        what to do if less space on FS
        
        insert "/netfs/CTLM/TOOLS/jobosr_scripts/bin/pg_audit.sh" repalce C1P-PRD-STAT-ALL - PC1PAUDIT - MUCCT1P
        
        insert "/ctmdata/Java/progs/ioalog/execute.csh "   C1T-PRD-STAT-DBA - PC1T1TIOALOG - MUCCT1T
    


"""
#
class DataBase(object): 
    #Die Klasse "DataBase" ist die Basisklasse.

    #def database(self):
    #    print "Initialise Methode - die dann jeweils mit den neuen methoden fuer jede DB ueberschrieben werden kann."
        
        def __init__(self, database_User, database_Name, database_Port, database_Type, database_Host):
            self.database_User = database_User
            self.database_Name = database_Name
            self.database_Port = database_Port
            self.database_Type = database_Type
            self.database_Host = database_Host
            self.dump_Output="/netfs/CTLM/database/"
            self.pswPath = "/ctmpg/.PG/"
            self.ctmpg_SU = "postgres"
            
        def checkSpace(self):

            print "................... check if there is enough space on the FS"
             
            disk = os.statvfs("/netfs/CTLM/database")

            totalBytes = float(disk.f_bsize*disk.f_blocks)
                #print "total space: %d Bytes = %.2f KBytes = %.2f MBytes = %.2f GBytes" % (totalBytes, totalBytes/1024, totalBytes/1024/1024, totalBytes/1024/1024/1024)
            totalUsedSpace = float(disk.f_bsize*(disk.f_blocks-disk.f_bfree))
                #print "used space: %d Bytes = %.2f KBytes = %.2f MBytes = %.2f GBytes" % (totalUsedSpace, totalUsedSpace/1024, totalUsedSpace/1024/1024, totalUsedSpace/1024/1024/1024)
            totalAvailSpace = float(disk.f_bsize*disk.f_bfree)
                #print "available space: %d Bytes = %.2f KBytes = %.2f MBytes = %.2f GBytes" % (totalAvailSpace, totalAvailSpace/1024, totalAvailSpace/1024/1024, totalAvailSpace/1024/1024/1024)
            totalAvailSpaceNonRoot = float(disk.f_bsize*disk.f_bavail) 
                #print "available space for non-super user: %d Bytes = %.2f KBytes = %.2f MBytes = %.2f GBytes " % (totalAvailSpaceNonRoot, totalAvailSpaceNonRoot/1024, totalAvailSpaceNonRoot/1024/1024, totalAvailSpaceNonRoot/1024/1024/1024) 
            avaiLable= totalAvailSpaceNonRoot/1024/1024/1024
#            print avaiLable

            if avaiLable < 40:
                print "available space : = %.2f GBytes " % (avaiLable)
            
        def createFS(self):
        
            self.cleanFS()
            self.checkSpace()
            print "............. create FS"  
            self.dump_Output_Create = ""+ self.dump_Output + "/"+ self.database_Type + "/" + self.database_Host + "/" + Today + ""
            cReaTor = "mkdir "+ self.dump_Output_Create + ""
            print cReaTor
            rc = os.system(cReaTor)            
            #vieWer = "ls "+ self.dump_Output_Create + "/*"""
            #rc = os.system(vieWer)  
            #print rc
    
            
        def dumpDB_MySQL(self):    
            
            self.createFS()
            
            print "....................................... START MySQL dump ............. start dump specific db .......->"  + self.database_Host + ""

            self.dump_Output_MySQL = ""+ self.dump_Output + "/"+ self.database_Type + "/" + self.database_Host + "/" + Today + "" 
            
            print 'DB_USER : ' , self.database_User
            print 'DB_NAME : ' , self.database_Name
            print 'DB_PORT : ' , self.database_Port
            print 'DB_TYPE : ' , self.database_Type
            print 'DB_HOST : ' , self.database_Host
            print 'DB_OUT : ' , self.dump_Output_MySQL
            print 'Today    :', today
            print 'Today    :', Today
            print 'Today -90   :', minus_90
            print 'FileObject    :', fileObject 
            
            dUmPer = "mysqlshow -u "+ self.database_User + " -h " + self.database_Host + " --port " + self.database_Port + " | sed 's/|/ /g' | sed '1,4d' | sed -e '' | sed -e 's/^  //' | sed -e '$d'"
            print dUmPer  
            process = subprocess.Popen(dUmPer,stdout=subprocess.PIPE,shell=True)
            for i in iter(process.stdout.readline,''):
                i = i.strip()
                dUmPer = "mysqldump --single-transaction -u "+ self.database_User + " -h " + self.database_Host + " --port " + self.database_Port + " " + i + " --result-file="+ self.dump_Output_MySQL +"/"+ i +".sql"
                print "-------------------->" + dUmPer
                ziPPer = "gzip "+ self.dump_Output_MySQL +"/"+ i +".sql"
                os.system(dUmPer)
                os.system(ziPPer)
        
        def dumpDB_PG(self):

            self.createFS()
            print "....................................... START PostgreSQL dump ............. start dump specific/all db .......->"  + self.database_Host + ""

            self.dump_Output_PostgreSQL = ""+ self.dump_Output + "/"+ self.database_Type + "/" + self.database_Host + "/" + Today + ""            
            
            print 'DB_USER : ' , self.database_User
            print 'DB_NAME : ' , self.database_Name
            print 'DB_PORT : ' , self.database_Port
            print 'DB_TYPE : ' , self.database_Type
            print 'DB_HOST : ' , self.database_Host
            print 'DB_OUT : ' , self.dump_Output_PostgreSQL
 
            print "get password for " + self.database_User + " and from file " + fileObject + "/"+ self.database_User +"" 
            ## if host = wtv or wpv dump die ganzen databases
            #""" how to ge tpassword later ???
            # ueberprufe ob password file existiert !! oder nutzte csv oder xml !! 
            #"""
            self.pswPath = ""+ self.pswPath +"/."+ self.database_Name + ""
            print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
            print self.pswPath
            fobj_in = open(self.pswPath, "r")

            for line in fobj_in:
                pObject = line.rstrip()
                os.putenv('PGPASSWORD', line.rstrip())    
            print pObject
            print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"            
            
            if "wpv01" in self.database_Host or "wtv01" in self.database_Host:
                print "................................................ ctmadm host"
                print " dump all databases wtv = TST wpv = PRD"

                self.dump_Str = " -f "+ self.dump_Output_PostgreSQL +""
                print self.dump_Str
	# removed 15022017			
    #            self.do_TableSpace_Dump(self.dump_Str)
 
            else:
                dUmPer = "pg_dump " + self.database_Name + " -U "+ self.database_User + " -h " + self.database_Host + " -p " + self.database_Port + " -f "+ self.dump_Output_PostgreSQL +"/"+ self.database_Name +".sql"
                print dUmPer
                os.system(dUmPer)


            if "ct" in self.database_User:
                self.dump_ioalog_Str = "-c -Ft -f "+ self.dump_Output_PostgreSQL +""
                print self.dump_ioalog_Str
                        #pg_dump ct1tst800 -U ct1ts t800 -h mucctlatv02 -p 5438 -c -Ft -f $HOME/dump/mucct1t.ct1tst800_`date +'%Y%m%d'`.tar
	# removed 15022017
    #            self.do_ioalog_copy(self.dump_ioalog_Str, pObject)

            ziPPer = "gzip "+ self.dump_Output_PostgreSQL +"/"+ self.database_Name +".sql"
            print ziPPer
            os.system(ziPPer)
                
                
                

        def cleanFS(self):
            print "............. cleanup filesystem of dump file"
            #self.dump_Output = "/netfs/CTMADM/"+ self.database_Type + "/" + self.database_Host + "/" + minus_90 + ""
            self.dump_Output_Clean = ""+ self.dump_Output + "/"+ self.database_Type + "/" + self.database_Host + "/" + minus_3 + ""
            cLeaNer = "rm -irf "+ self.dump_Output_Clean + ""
            print cLeaNer            
            os.system(cLeaNer)


        def cleanDB_Table(self):
            print "............. cleanup old data from specific tables .. only WPV01"            
            print "connect to database"
            print "run query to checke for data"
            print "delete query "

            
        def do_TableSpace_Dump(self, dump_Str):

            """ just to query the postgres database"""
            #! password to be changed
            pObject = "ctmpgrepository"
            os.putenv('PGPASSWORD', pObject)
            #
            print "......................................................................... do_TableSpace_Dump"
            #print pObject
            print self.dump_Str
            print self.dump_Output_PostgreSQL
            credentials = { 'user'    : self.database_User,
                            'password': pObject, 
                            'database': self.database_Name,
                            'host'    : self.database_Host}
  
            myconnection = pg8000.connect(**credentials) 
            cursor = myconnection.cursor()

            try:
                cursor = myconnection.cursor()
                print "connect OK"
            except:
                print "Can't connect to Server"
                exit(0)

            cur = myconnection.cursor()
            # build query
            cursor.execute("SELECT datname FROM pg_database order by datname ")
            result = cursor.fetchall()
            cursor.close()
            
            print self.database_Host
            print self.dump_Str
            
            for data in result:
 
#                dUmPer =  "pg_dump -U postgres "+ data[0] +" " + self.dump_Str + "/" + data[0] +".sql"
                dUmPer =  "pg_dump -U postgres "+ data[0] +" -h " + self.database_Host + " " + self.dump_Str + "/" + data[0] +".sql"
                ziPPer = "gzip "+ self.dump_Output_PostgreSQL +"/"+ data[0] +".sql"
            #    mover = "mkdir /netfs/CTLM/prog/python/temp/  /netfs/CTLM/prog/python/temp/" + data[0] +".sql"
                print dUmPer
                os.system(dUmPer)
                print ziPPer
                os.system(ziPPer)

 
        def do_ioalog_copy(self, dump_ioalog_Str, pObject): 
 
            # remove jobs in control-m and in /netfs/CTLM/prog/Java/ioalog
 
            """ dump ioalog form server and restore to ctmpg"""
 
            print "............................................................................... do_ioalog_copy"
            print 'DB_USER : ' , self.database_User
            print 'DB_NAME : ' , self.database_Name
            print 'DB_PORT : ' , self.database_Port
            print 'DB_TYPE : ' , self.database_Type
            print 'DB_HOST : ' , self.database_Host
            print 'DB_OUT : ' , self.dump_Output    
            print self.dump_ioalog_Str
            print self.dump_Output_PostgreSQL
            print pObject
            # dump database
            dUmPer =  "pg_dump " + self.database_Name + " -U " + self.database_User + " -p " + self.database_Port + " -h " + self.database_Host + " " + self.dump_ioalog_Str + "/"+ self.database_Name +".tar"
                        #pg_dump ct2tst800 -U ct2tst800 -p 5432 -h mucctlatv02 -c -Ft -f /netfs/CTLM/database//PostgreSQL/mucctlatv02/160308/ct2tst800.tar
            
            print dUmPer
            os.system(dUmPer)
            # drop database in ctmpg
            ctmpg_Port = "5432"         # change to read from config ?
            print ctmpg_Port
            ctmpg_Host = "mucctlwpv01"
            
            if "atv0" in self.database_Host:
                ctmpg_Host = "mucctlwtv01"

            droP_dataBase = "psql -U " + self.database_User + " -p " + ctmpg_Port + " -h " + ctmpg_Host + " -d " + self.database_Name +"_schema -c \"drop database " + self.database_Name + "\"" ""
            print droP_dataBase
            os.system(droP_dataBase)
                    # create datebase in cmtpg
            creaTe_dataBase = "psql -U " + self.database_User + " -p " + ctmpg_Port + " -h " + ctmpg_Host + " -d " + self.database_Name +"_schema -c \" create database " + self.database_Name + " with template template0 owner " + self.database_User + "\"" ""
            print creaTe_dataBase
            os.system(creaTe_dataBase)
 
             #create schema           
            #print pObject 
            #! password to be changed
            pObject_SU = "ctmpgrepository"
            os.putenv('PGPASSWORD', pObject_SU)           
            #print pObject_SU
  
            restore_to_schema = "pg_restore -d " + self.database_Name + " -U " + self.ctmpg_SU + " -p " + ctmpg_Port + " -h " + ctmpg_Host + " -C " + self.dump_Output_PostgreSQL + "/"+ self.database_Name +".tar"
            print restore_to_schema
            os.system(restore_to_schema)

            #copy DB to tablespace:

            copy_dataBase = "psql -U " + self.ctmpg_SU + " -p " + ctmpg_Port + " -h " + ctmpg_Host + " -c \"create database " + self.database_Name +"_"+ minus_1 + " WITH TEMPLATE " + self.database_Name +   " OWNER " + self.database_User + " TABLESPACE " + self.database_Name + " \"" 
          
            print copy_dataBase
            os.system(copy_dataBase)
            #delete old data in table cmr_ioalog
            #csh /ctmdata/Java/progs/ioalog/delete.sql ct1tst800 
            # to get all dates in table
 #           select distinct logdate from cmr_ioalog; 
 #            delete all except minus_1
            print self.database_User
            print ctmpg_Port
            print ctmpg_Host
            print self.database_Name
            print minus_1
            print pObject
            print toDay
            print ioaLogDelDate
            os.putenv('PGPASSWORD', pObject)           
            
            selDate = "psql -U " + self.database_User + " -p " + ctmpg_Port + " -h " + ctmpg_Host + " -d " + self.database_Name +"_"+ minus_1 + " -c \"select distinct logdate from cmr_ioalog; \"" 
            process = subprocess.Popen(selDate,stdout=subprocess.PIPE,shell=True)
            os.system(selDate)
            #for j in iter(process.stdout.readline,''):
            #    j = j.strip()      
            #    print "DATE............................................"+ j 
            #
            selIoaLog = "psql -U " + self.database_User + " -p " + ctmpg_Port + " -h " + ctmpg_Host + " -d " + self.database_Name +"_"+ minus_1 + " -c \"SELECT table_name from information_schema.tables where table_name like 'cmr_ioalog_%' ; \"" 
            print selIoaLog
            process = subprocess.Popen(selIoaLog,stdout=subprocess.PIPE,shell=True)
            for i in iter(process.stdout.readline,''):
                i = i.strip()
                i_Last = i[-1:]
                if i_Last.isdigit():
                    delDate = "psql -U " + self.database_User + " -p " + ctmpg_Port + " -h " + ctmpg_Host + " -d " + self.database_Name +"_"+ minus_1 + " -c \"delete from cmr_ioalog_"+ i_Last +" where logdate != '"+ ioaLogDelDate +"' ; \""
                    print delDate
                    os.system(delDate)
                    
                selIoaLog = "psql -U " + self.database_User + " -p " + ctmpg_Port + " -h " + ctmpg_Host + " -d " + self.database_Name +"_"+ minus_1 + " -c \"select count(*) from cmr_ioalog ; \""
            print selIoaLog
            os.system(selIoaLog)  
            print selDate
            os.system(selDate)        

                    
        def do_runinshout(self): 
 
            print "do_runinshout"
 
            # replace "/netfs/CTLM/TOOLS/jobosr_scripts/bin/create_runinf_STATS.sh"
            
            
            #1. query EMAPRD
            
            #2. iterate for all AJF and query data
            
#                save to csv ? or write direct to MySQL ? or wirte to ctmpg ?
            
            #3. load data from #2. into MySQL
 
            """ load data do runinshout"""
 
 

    #end database
#end class DataBase

#print programmUser  
#print os.environ['USER'] 
#
#   ...................................................... objects
## find method to get these variables defined with values -- xml, csv, ??
""" ......    MYSQL - WTV01 """
database_Host="mucctlwtv01"        
database_User="dbdump"        
database_Port="10306"        
database_Type="MySQL"        
database_Name="statsdb"        
objekt_MySQL_TST = DataBase(database_User, database_Name, database_Port, database_Type, database_Host)
# call method
objekt_MySQL_TST.dumpDB_MySQL()
#
""" ......    MYSQL - WPV01 """
database_Host="mucctlwpv01"        
database_User="dbdump"        
database_Port="3306"        
database_Type="MySQL"        
database_Name="statsdb"        
objekt_MySQL_PRD = DataBase(database_User, database_Name, database_Port, database_Type, database_Host)
# call method
objekt_MySQL_PRD.dumpDB_MySQL()
#
""" ......    PG WTV01 """
    #PG - psql -U postgres -h mucctlwtv01 -p 5432 -d postgres : setenv PGPASSWORD ctmpgrepository
database_Host="mucctlwtv01"        
database_User="postgres"        
database_Port="5432"        
database_Type="PostgreSQL"        
database_Name="postgres" 
objekt_PG_wtv = DataBase(database_User, database_Name, database_Port, database_Type, database_Host)
objekt_PG_wtv.dumpDB_PG()
#
""" ......    PG WPV01 """
    #PG - psql -U postgres -h mucctlwpv01 -p 5432 -d postgres : setenv PGPASSWORD ctmpgrepository
database_Host="mucctlwpv01"        
database_User="postgres"        
database_Port="5432"        
database_Type="PostgreSQL"        
database_Name="postgres" 
objekt_PG_wpv = DataBase(database_User, database_Name, database_Port, database_Type, database_Host)
objekt_PG_wpv.dumpDB_PG()
#
""" ......    PG ct4dev """
    #PG - psql -U ct4dev -h mucctlatv02 -p 5434 -d ct4dev800 : setenv PGPASSWORD ct4dev800
database_Host="mucctlatv02"        
database_User="ct4dev"        
database_Port="5434"        
database_Type="PostgreSQL"        
database_Name="ct4dev800" 
objekt_PG_4d = DataBase(database_User, database_Name, database_Port, database_Type, database_Host)
	#stop execution 22-nov-2016
	#	objekt_PG_4d.dumpDB_PG()
#
""" ......    PG ct1tst """
    #PG - psql -U ct1tst900 -h mucctlatv02 -p 5438 -d ct1tst900 : setenv PGPASSWORD ct1tst900
database_Host="mucctlatv02"        
database_User="ct1tst900"        
database_Port="5438"        
database_Type="PostgreSQL"        
database_Name="ct1tst900" 
objekt_PG_1t = DataBase(database_User, database_Name, database_Port, database_Type, database_Host)
objekt_PG_1t.dumpDB_PG()
#
""" ......    PG ct2tst """
credentials = {'database_Host' : 'mucctlatv02',
               'database_User' : 'ct2tst800',  
               'database_Port' : '5432',
               'database_Type'   : 'PostgreSQL',
               'database_Name' : 'ct2tst800'}
"""
print credentials
print credentials.values()

    print credentials['database_Host']
    print credentials['database_User']
    print credentials['database_Type']
    print credentials['database_Port']
    print credentials['database_Name']
"""
objekt_PG_2t = DataBase(credentials['database_User'], credentials['database_Name'], credentials['database_Port'], credentials['database_Type'], credentials['database_Host'] )
	#stop execution 22-nov-2016
	#objekt_PG_2t.dumpDB_PG()
#
""" ......    PG ct3tst """
    #PG - psql -U ct3tst900 -h mucctlatv02 -p 5433 -d ct3tst900 : setenv PGPASSWORD ct3tst900
database_Host="mucctlatv02"        
database_User="ct3tst900"        
database_Port="5433"        
database_Type="PostgreSQL"        
database_Name="ct3tst900" 
objekt_PG_3t = DataBase(database_User, database_Name, database_Port, database_Type, database_Host)
objekt_PG_3t.dumpDB_PG()
#
""" ......    PG ct4tst """
    #psql -U ct4tst900 -h mucctlatv02 -p 5436 -d ct4tst900 : setenv PGPASSWORD ct4tst900
database_Host="mucctlatv02"        
database_User="ct4tst900"        
database_Port="5436"        
database_Type="PostgreSQL"        
database_Name="ct4tst900" 
objekt_PG_4t = DataBase(database_User, database_Name, database_Port, database_Type, database_Host)
objekt_PG_4t.dumpDB_PG()
#
""" ......    PG ct5tst """
    #psql -U ct5tst900 -h mucctlatv02 -p 5435 -d ct5tst900 : setenv PGPASSWORD ct5tst900
database_Host="mucctlatv02"        
database_User="ct5tst900"        
database_Port="5435"        
database_Type="PostgreSQL"        
database_Name="ct5tst900" 
objekt_PG_5t = DataBase(database_User, database_Name, database_Port, database_Type, database_Host)
objekt_PG_5t.dumpDB_PG()
#
""" ......    PG ct6tst """
    #psql -U ct6tst900 -h mucctlatv02 -p 5437 -d ct6tst900 : setenv PGPASSWORD ct6tst900
database_Host="mucctlatv02"        
database_User="ct6tst900"        
database_Port="5437"        
database_Type="PostgreSQL"        
database_Name="ct6tst900" 
objekt_PG_5t = DataBase(database_User, database_Name, database_Port, database_Type, database_Host)
objekt_PG_5t.dumpDB_PG()
#
#remove EMA 800
#	""" ......    PG emaprd """
#		#PG - mucctlapv01:5432:ema800prd:emaprd:emaprd800
#	database_Host="mucctlapv01"        
#	database_User="emaprd"   
#	database_Port="5432"        
#	database_Type="PostgreSQL"        
#	database_Name="ema800prd" 
#	objekt_PG_emaprd = DataBase(database_User, database_Name, database_Port, database_Type, database_Host)
#	objekt_PG_emaprd.dumpDB_PG()
#
""" ......    PG emaprd-V900 """
    #PG - mucctlapv01:5434:emaprd900:emaprd900:emaprd900
database_Host="mucctlapv01"        
database_User="emaprd900"   
database_Port="5434"        
database_Type="PostgreSQL"        
database_Name="emaprd900" 
objekt_PG_emaprd = DataBase(database_User, database_Name, database_Port, database_Type, database_Host)
objekt_PG_emaprd.dumpDB_PG()
#
#
""" ......    PG ct5prd-V900 """
    #PG - mucctlapv05:5432:ct5prd900:ct5prd900:ct5prd900
database_Host="mucctlapv05"        
database_User="ct5prd900"   
database_Port="5432"        
database_Type="PostgreSQL"        
database_Name="ct5prd900" 
objekt_PG_emaprd = DataBase(database_User, database_Name, database_Port, database_Type, database_Host)
objekt_PG_emaprd.dumpDB_PG()
#
""" ......    PG ct1prd-V900 """
    #PG - mucctlapv02:5432:ct1prd900:ct1prd900:ct1prd900
database_Host="mucctlapv02"        
database_User="ct1prd900"   
database_Port="5432"        
database_Type="PostgreSQL"        
database_Name="ct1prd900" 
objekt_PG_emaprd = DataBase(database_User, database_Name, database_Port, database_Type, database_Host)
objekt_PG_emaprd.dumpDB_PG()
#
#
""" ......    PG ct4prd-V900 """
    #PG - mucctlapv04:5432:ct4prd900:ct4prd900:ct4prd900
database_Host="mucctlapv04"        
database_User="ct4prd900"   
database_Port="5432"        
database_Type="PostgreSQL"        
database_Name="ct4prd900" 
objekt_PG_emaprd = DataBase(database_User, database_Name, database_Port, database_Type, database_Host)
objekt_PG_emaprd.dumpDB_PG()
#
""" ......    PG ct3prd-V900 """
    #PG - mucctlapv03:5432:ct3prd900:ct3prd900:ct3prd900
database_Host="mucctlapv03"
database_User="ct3prd900"   
database_Port="5432"        
database_Type="PostgreSQL"        
database_Name="ct3prd900" 
objekt_PG_emaprd = DataBase(database_User, database_Name, database_Port, database_Type, database_Host)
objekt_PG_emaprd.dumpDB_PG()
#
#
""" ......    PG ct4cfs-V900 """
    #PG - mucctlapv07:5432:ct4cfs0:ct4cfs900:ct4cfs900
database_Host="mucctlapv07"
database_User="ct4cfs900"   
database_Port="5432"        
database_Type="PostgreSQL"        
database_Name="ct4cfs900" 
objekt_PG_emaprd = DataBase(database_User, database_Name, database_Port, database_Type, database_Host)
objekt_PG_emaprd.dumpDB_PG()
#