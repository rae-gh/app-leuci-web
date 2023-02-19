
from pathlib import Path
import os
from os import listdir
from os.path import isfile, join
from django.conf import settings
import datetime    
import logging 

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class AdminClass(object):
    def __init__(self):
        self.data_dir = str(Path(__file__).resolve().parent.parent )+ "/data/"
        self.data_dic = {}
        self.log_file = str(BASE_DIR) + '/leucilog_'+str(settings.DEBUG) +'.log'
        

    def delete_logs(self):
        open(self.log_file, 'w').close()        
        msg = "INFO: log file was cleared at "+str(datetime.datetime.now())+' hours'        
        logging.info(msg)
        return msg

    def show_logs(self, formatted=False, all=False):
        lines = []
        with open(self.log_file, "r") as f:
            lns = f.readlines()

        if all:
            lines = lns
        else:
            for ln in lns:
                if "INFO:" in ln or "ERROR:" in ln:
                    lines.append(ln)
        if not formatted:
            return lines
        line_formed = ""
        for line in lines:
            line_formed += line
        return line_formed
        
        
    def delete_data(self):
        onlyfiles = [f for f in listdir(self.data_dir) if isfile(join(self.data_dir, f))]
        onlyfiles.sort()
        form_str = "Deleting all files...\n"
        
        for file in onlyfiles:
            if file != "readme.md":
                fullpath = self.data_dir + file
                os.remove(fullpath)
                form_str += "Deleted " + file + "\n"
        return form_str
                
        

    def show_data(self, formatted=False):
        
        onlyfiles = [f for f in listdir(self.data_dir) if isfile(join(self.data_dir, f))]
        onlyfiles.sort()

        form_str = "filename\t\tsize (kB)\n"
        form_str += "----------\t\t--------\n"

        for file in onlyfiles:
            if file != "readme.md":
                fullpath = self.data_dir + file
                sz = os.path.getsize(fullpath)
                self.data_dic[file] = (int)(sz/1000)
                form_str += file
                if len(file) <= 8 and "1" in file: 
                    form_str += "\t"
                if len(file) <= 9: 
                    form_str += "\t"
                form_str += "\t" + str((int)(sz/1000)) + "\n"
        
        if not formatted:
            return self.data_dic
        else:
            form_str = form_str.strip()
            return form_str
        

            

        
        



        