import json
import sys
from datetime import datetime
import datetime
import os

class DataStorage:
    
    def __init__(self):
        
        self.dic = {}                                                                        //initialising dictionary
        
    def Create(self):                                                                       //create key function
        key = input("Enter key")
        value = input("Enter json value")
        while len(key)>32:                                                                   //key condition
            print("Error : Number of characters in key exceed the maximum number of characters allowed i.e 32")
            key = input("Enter key again")
        while sys.getsizeof(value)>16000:                                                   //value condition
            print("Error : Size of value exceeds the maximum size allowed i.e 16 KB")
            value = input("Enter json value again")
        now = datetime.datetime.now()                                                       //to get current time
        now_plus_5 = now + datetime.timedelta(minutes = 5)                                  //adding 5 mins 
        now_plus_5 = now_plus_5.strftime("%m/%d/%Y %H:%M:%S")
        value = value[:-1] + "," + '"Time_Valid":"' + str(now_plus_5) + '"' + value[-1]
        value = json.loads(value)                                                          //converting json string to dictionary
        
        if key not in self.dic:
            self.dic[key] = value
            obj = json.dumps(self.dic,indent = len(self.dic))                              //converting to json object
            with open('datafile.json','w') as f:
                file_stats = os.stat('datafile.json')
                if (file_stats.st_size / (1024 * 1024)) > 1024:                            //datastorage size condition
                    print("Error: Datastorage has reached its maximum potential no more data can be added now")
                else:
                    f.write(obj)                                                           //writing json object in datastorage
                    print("Key added to the datastorage")
        else:
            print("Error : Key already present in the data store")                         //key already present condition
    
    def Read(self):                                                                        //Read key function
        key = input("Enter Key")
        with open('datafile.json') as f:                                                   //opening datastorage file
            data = json.load(f)
        if key in data:                                                                    //checking key if exists
            time = data[key]['Time_Valid']
        else:
            print("Error : Key doesn't exists in database")
            return
        time_valid = datetime.datetime.strptime(time,"%m/%d/%Y %H:%M:%S")
        current_time = datetime.datetime.now()
        current_time = current_time.strftime("%m/%d/%Y %H:%M:%S")
        current_time = datetime.datetime.strptime(current_time,"%m/%d/%Y %H:%M:%S")
        
        if current_time > time_valid :                                                      //checking time if key can be read or deleted
            print("Error : Time Over value can't be read or deleted now")
            return
        else:
            obj = json.dumps(data[key],indent = len(data[key]))
            return obj
        
        
    def Delete(self):                                                                      //Delete key function
        key = input("Enter Key")
        with open('datafile.json') as f:
            data = json.load(f)
        if key in data:
            time = data[key]['Time_Valid']
        else:
            print("Error : Key doesn't exists in database")
        time_valid = datetime.datetime.strptime(time,"%m/%d/%Y %H:%M:%S")
        current_time = datetime.datetime.now()
        current_time = current_time.strftime("%m/%d/%Y %H:%M:%S")
        current_time = datetime.datetime.strptime(current_time,"%m/%d/%Y %H:%M:%S")
        
        if current_time > time_valid :                                                     //checking time if key can be read or deleted
            print("Error : Time Over value can't be read or deleted now")
        else:
            del self.dic[key]
            obj = json.dumps(self.dic,indent = len(self.dic))
            with open('datafile.json','w') as f:
                f.write(obj)
            print("Key has been successfully deleted from the database")
               
