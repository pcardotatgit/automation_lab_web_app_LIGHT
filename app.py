# a_core_header.py***
# -*- coding: UTF-8 -*-
#!/usr/bin/env python
'''
Copyright (c) 2024 Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms oftool
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
    
what is this script doing ?

    this is the core of the application. This is the flask script that start the web server and exposes every APIs

'''
# a_core_imports.py***
from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
from flask_request_params import bind_request_params
import os
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from tabledef import *
import sqlite3
import sys
from crayons import *
from werkzeug.utils import secure_filename
import struct
import csv
from datetime import datetime, timedelta
import socket
import webbrowser
import threading
import time
import glob
import pandas as pd
from pandas import DataFrame
import random
import signal
import requests
import json
import hashlib
from pathlib import Path
from inspect import currentframe
import subprocess
import shutil
from json_to_dtree_graph import go_analyse_json
import operator
import base64
import env as env

# a_core_global_definitions.py***
# GLOBAL VARIABLE DEFINITION

engine = create_engine('sqlite:///users.db', echo=True)

# Get the current date/time
dateTime = datetime.now()

PAGE_DESTINATION=""
temp=''
method="config.txt"  # for futur use :  must be either config.txt or ../key  or database  or vault or environment variable
Umbrella_Investigate_Token='Bearer 31801821-b9a1-4ad3-82d9-dfe2c93ffake'
UMBRELLA_ENFORCEMENT_KEY = "12345678-b9a1-4ad3-82d9-dfe2c93ffffz"
CSE_CLIENT_ID = "defg26458064a05f1faz"
CSE_API_KEY = "12345678-4f95-43d5-908d-7a7d41ad385z"
CSE_AUTHORIZATION ="Basic ZGVmZzI2NDU4MDY0YTA1ZjFmYXo6MTIzNDU2NzgtNGY5NS00M2Q1LTkwOGQtN2E3ZDQxYWQzODV6"
THREATGRID_API_KEY = "Bearer Zjttqveo7g1doaszbc0n6qfzzz"
CTR_CLIENT_ID = "client-bbaad7e2-e5ff-413f-1234-0e21bc871zzz"
CTR_API_KEY = "ZezA_VszEcMTCzzzU0Wr5mQypXoxbjFNKDnLa0Mkw_O_ZZ4TND9mZZ"
CTR_TOKEN="Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkhqVW4yNlBPUGZlWFFxeDEtcEc3TFU1MnBNRTRVMVlySWlJa29fUTJMV0kifQ.eyJodHRwczovL3NjaGVtYXMuY2lzY28uY29tL2lyb2gvaWRlbnRpdHkvY2xhaW1zL3VzZXIvZW1haWwiOiJwY2FyZG90QGNpc2NvLmNvbSIsImh0dHBzOi8vc2NoZW1hcy5jaXNjby5jb20vaXJvaC9pZGVudGl0eS9jbGFpbXMvdXNlci9zY29wZXMiOlsiaW50ZWdyYXRpb24iLCJwcml2YXRlLWludGVsIiwiYWRtaW4iLCJwcm9maWxlIiwiaW5zcGVjdCIsInNzZSIsInJlZ2lzdHJ5IiwidXNlcnMiLCJjYXNlYm9vayIsIm9yYml0YWwiLCJlbnJpY2giLCJvYXV0aCIsImNvbGxlY3QiLCJyZXNwb25zZSIsInVpLXNldHRpbmdzIiwidGVsZW1ldHJ5OndyaXRlIiwib3BlbmlkIiwibm90aWZpY2F0aW9uIiwiZ2xvYmFsLWludGVsOnJlYWQiLCJhbyJdLCJodHRwczovL3NjaGVtYXMuY2lzY28uY29tL2lyb2gvaWRlbnRpdHkvY2xhaW1zL3VzZXIvaWRwL2lkIjoiaWRiLWFtcCIsImh0dHBzOi8vc2NoZW1hcy5jaXNjby5jb20vaXJvaC9pZGVudGl0eS9jbGFpbXMvdXNlci9uaWNrIjoiUGF0cmljayBDYXJkb3QiLCJlbWFpbCI6InBjYXJkb3RAY2lzY28uY29tIiwiYXVkIjoiY2xpZW50LWJiYWViN2UyLWU1YmItNDEzZi04NDY5LTBlMjFiYzg3MTJiYyIsImh0dHBzOi8vc2NoZW1hcy5jaXNjby5jb20vaXJvaC9pZGVudGl0eS9jbGFpbXMvdXNlci9yb2xlIjoiYWRtaW4iLCJzdWIiOiJiYjRjMDdkMy0zYjhjLTQxYTYtYjBlYS1hODZlNWY5NWQ3YTAiLCJpc3MiOiJJUk9IIEF1dGgiLCJodHRwczovL3NjaGVtYXMuY2lzY28uY29tL2lyb2gvaWRlbnRpdHkvY2xhaW1zL3Njb3BlcyI6WyJwcml2YXRlLWludGVsIiwiZW5yaWNoOnJlYWQiLCJjYXNlYm9vayIsImluc3BlY3Q6cmVhZCIsInJlc3BvbnNlIiwiZ2xvYmFsLWludGVsOnJlYWQiXSwiZXhwIjoxNjAxNDU5MTczLCJodHRwczovL3NjaGVtYXMuY2lzY28uY29tL2lyb2gvaWRlbnRpdHkvY2xhaW1zL29hdXRoL2NsaWVudC9uYW1lIjoicGF0cmlja19jdHJfYXBpX2tleSIsImh0dHBzOi8vc2NoZW1hcy5jaXNjby5jb20vaXJvaC9pZGVudGl0eS9jbGFpbXMvb2F1dGgvdXNlci9pZCI6ImJiNGMwN2QzLTNiOGMtNDFhNi1iMGVhLWE4NmU1Zjk1ZDdhMCIsImh0dHBzOi8vc2NoZW1hcy5jaXNjby5jb20vaXJvaC9pZGVudGl0eS9jbGFpbXMvb3JnL2lkIjoiNDE2MDM4MjYtNjA4ZS00YTRlLThiNjItYjE3ZjkwNjRmOWJkIiwiaHR0cHM6Ly9zY2hlbWFzLmNpc2NvLmNvbS9pcm9oL2lkZW50aXR5L2NsYWltcy9vYXV0aC9ncmFudCI6ImNsaWVudC1jcmVkcyIsImh0dHBzOi8vc2NoZW1hcy5jaXNjby5jb20vaXJvaC9pZGVudGl0eS9jbGFpbXMvb3JnL25hbWUiOiJDaXNjbyAtIHBjYXJkb3QiLCJqdGkiOiJ0b2tlbi05MDExZWJiNS0wZWQxLTQ3N2UtYTRhNS0yODc4N2Y3NjEwYmUiLCJuYmYiOjE2MDE0NTg1MTMsImh0dHBzOi8vc2NoZW1hcy5jaXNjby5jb20vaXJvaC9pZGVudGl0eS9jbGFpbXMvb2F1dGgvc2NvcGVzIjpbInByaXZhdGUtaW50ZWwiLCJlbnJpY2g6cmVhZCIsImNhc2Vib29rIiwiaW5zcGVjdDpyZWFkIiwicmVzcG9uc2UiLCJnbG9iYWwtaW50ZWw6cmVhZCJdLCJodHRwczovL3NjaGVtYXMuY2lzY28uY29tL2lyb2gvaWRlbnRpdHkvY2xhaW1zL3VzZXIvbmFtZSI6IlBhdHJpY2sgQ2FyZG90IiwiaHR0cHM6Ly9zY2hlbWFzLmNpc2NvLmNvbS9pcm9oL2lkZW50aXR5L2NsYWltcy91c2VyL2lkIjoiYmI0YzA3ZDMtM2I4Yy00MWE2LWIwZWEtYTg2ZTVmOTVkN2EwIiwiaHR0cHM6Ly9zY2hlbWFzLmNpc2NvLmNvbS9pcm9oL2lkZW50aXR5L2NsYWltcy9vYXV0aC9jbGllbnQvaWQiOiJjbGllbnQtYmJhZWI3ZTItZTViYi00MTNmLTg0NjktMGUyMWJjODcxMmJjIiwiaHR0cHM6Ly9zY2hlbWFzLmNpc2NvLmNvbS9pcm9oL2lkZW50aXR5L2NsYWltcy92ZXJzaW9uIjoidjEuMzkuMC1hNTBkMDllZWRmMWNkYzUwODBjYyIsImlhdCI6MTYwMTQ1ODU3MywiaHR0cHM6Ly9zY2hlbWFzLmNpc2NvLmNvbS9pcm9oL2lkZW50aXR5L2NsYWltcy9vYXV0aC9raW5kIjoiYWNjZXNzLXRva2VuIn0.pjQUsxKLn7kONHYJFaI7K5U4w3hs7n-3zLrwk13GBilgfaSQX10uSPAyWZ8nCQplx0gJ20Q9L7Z2XWeoI3VZKBYmWaJ8VvlQBNmie6klugGK54o1ysnf-YtgErgB5eo7lslu8nCMuCgxobXcCv5J4_hF0R9934UCGBH4NqqbogmPJe0lupsdyeXj9X1hf0Yx1fMDIJsaCU0QTTxzmZPj2wP_ywdyGFud4DagqGfFBUeOA6SaGh_iBtgcTF9No6VZLviLPde2UDrt4FcrTWmtlKF-BHvpusZZu1EAGs4ZpLwl9-QIouPOCdIou-umfMtEF_VLS71bjfiot4zUuojWQA"
UMBRELLA_TOKEN="eyJhbGciOiJSUzI1NiIsImtpZCI6IjIwMTktMDEtMDEiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJ1bWJyZWxsYS1hdXRoei9hdXRoc3ZjIiwic3ViIjoib3JnLzE5NTMxMTUvdXNlci83ODg3OTk3IiwiZXhwIjoxNzYwNjQ5NDcyLCJuYmYiOjE3NjA2NDU4NzIsImlhdCI6MTc2MDY0NTg3Miwic2NvcGUiOiJyb2xlOnJvb3QtYWRtaW4iLCJhdXRoel9kb25lIjpmYWxzZX0.P9Lmb4nvcjjLhltk8aSjdT2vG1ITybsjAFaNgVprRZ-5lpQMkIG3Sbnc94GhEp2RKduFO2q3kgS9VUayjfqpZnRRFrFVvld5AnhAcA_m0PHz0Kdbq-OwjRmv7K4CuvCwxgJ1L03jKZY1zJQmU7QEjEMlT44d0ZODQAr19aRoMFRR8yCKOyaZZHOuJ5f8ghdeunVtXVhEEJtDKSw1aEORJQEsCCtR888qbjFd38BCy0ZpAI16JpL3r3RJQMbduVz1nNUi8dKnIrqcSqBCkWPMyutri0epQSgMLqOmVkA_Ts0oTlCl0eCmB4B5ac4mYdZ8tkNH7Ay5eJ3w_cWD_y9BYQ"
use_simulator=1 # if = 1 then we query localhost:4000 instead of real host,  0 = query real hosts



# here under FUNCTIONS ===========================   
 
# def_get_line***
def get_line():
    env.level+='-'
    '''
        give the line number in the script wher is called this function
    '''
    print()
    print(env.level,white('def get_line() : >',bold=True))
    loguer(env.level+' def get_line() : >')
    print()     
    currentfram=currentframe()
    result='stop at line # : '+ str(currentfram.f_back.f_lineno)
    env.level=env.level[:-1]
    return result




# def_delete_files_in_temp***
def delete_files_in_temp():
    env.level+='-'
    print()
    print(env.level,white('def delete_files_in_temp() : >',bold=True))
    loguer(env.level+' def delete_files_in_temp() : >')
    print()
    file_list=glob.glob("./temp/*.txt")
    for fichier in file_list:
        fichier=fichier.replace('\\','/')        
        if os.path.exists(fichier):
            print(' ok delete ',fichier)
            os.remove(fichier)    
    env.level=env.level[:-1]
    return 1




# def_clean_result_dir***
def clean_result_dir(dirPath):
    env.level+='-'
    print()
    print(env.level,white('def clean_result_dir() : >',bold=True))
    loguer(env.level+' def clean_result_dir() : >')
    print()
    files =[file for file in os.listdir(dirPath)]
    for file in files:
        print("file to delete : ",file)
        os.remove(dirPath+"/"+file)
    env.level=env.level[:-1]
    return 1



# def_list_files_in_temp***
def list_files_in_temp():
    env.level+='-'
    print()
    print(env.level,white('def list_files_in_temp() : >',bold=True))
    loguer(env.level+' def list_files_in_temp() : >')
    print()
    file_list0=glob.glob("./temp/*.txt")
    file_list=[]
    for fichier in file_list0:
        fichier2=fichier.split('\\')[1]
        #file_list.append(fichier.replace('\\','/'))
        file_list.append(fichier2)
    env.level=env.level[:-1]
    return(file_list)
     



# def_current_date_and_time***
def current_date_and_time():  
    env.level+='-'
    print()
    print(env.level,white('def current_date_and_time() : >',bold=True))
    loguer(env.level+' def current_date_and_time() : >')
    print() 
    '''
        current time + nb days in the YYYYmmddHMSformat
    '''
    current_time = datetime.utcnow()
    timestampStr = current_time.strftime("%Y%m%d%H%M%S")
    env.level=env.level[:-1]
    return(timestampStr)




# def_open_browser_tab***
def open_browser_tab(host, port):
    env.level+='-'
    '''
        open web browser on login page
    '''
    print()
    print(env.level,white('def open_browser_tab() : >',bold=True))
    loguer(env.level+' def open_browser_tab() : >')
    print()
    url = 'http://%s:%s/' % (host, port)

    def _open_tab(url):
        time.sleep(1.5)
        webbrowser.open_new_tab(url)

    thread = threading.Thread(target=_open_tab, args=(url,))
    thread.daemon = True
    thread.start() 
    env.level=env.level[:-1]
    return 1   



# def_current_date_and_time_for_json_data***
def current_date_and_time_for_json_data():  
    env.level+='-'
    print()
    print(env.level,white('def current_date_and_time_for_json_data() : >',bold=True))
    loguer(env.level+' def current_date_and_time_for_json_data() : >')
    print() 
    '''
        current time + nb days in the YYYYmmddHMSformat
    '''
    current_time = datetime.utcnow()
    timestampStr = current_time.strftime("%Y-%m-%dT%H:%M:%S.000Z")  
    env.level=env.level[:-1]    
    return(timestampStr)
    



#  def_loguer***
def loguer(log):
    '''
    MODIFIED : 2025-06-19T15:52:21.000Z

    description : log when a function or a route is called with start date
    '''
    time = datetime.now().isoformat()
    #print(time)
    log=log+' at '+ time
    with open(f'./debug/log.txt','a+') as file:
          file.write(log+'\n')
    return 1
    



#  def_format_log***
def format_log():
    '''
    MODIFIED : 2025-07-19T15:44:48.000Z

    description : read log file and create a formated file
    
    how to call it :
    '''
    route="/format_log"
    env.level+='-'
    print('\n'+env.level,white('def format_log() in analyse_application_logs.py : >\n',bold=True))
    loguer(env.level+' def format_log() in analyse_application_logs.py : >')
    # ===================================================================    
    with open('./port.txt') as file:
        port=file.read()    
    with open('./debug/log.txt') as file:
        text_content=file.read()
    lines=text_content.split('\n')
    with open('./debug/parsed.txt','w') as file:
        for line in lines:
            if line != '' and '[-' in line:
                # print('\n line :\n',cyan(line+'\n',bold=True))               
                if "app.py" in line or "() : >" in line:
                    script=line.split('()')[0]
                    # print('\n script :',yellow(script+'\n',bold=True))
                    script=script.split(' ')[2]
                    # print('\n script :',yellow(script+'\n',bold=True))
                    line=line.replace('[','')
                    line=line.replace('- r','-; r')
                    line=line.replace('- d','-; d')            
                    line=line.replace(': >:','<<:')                     
                    if 'route' in line:
                        url=f";<<url:http://localhost:{port}/code_edit?code=route_def_{script}.py&type=route"
                    else:
                        url=f";<<url:http://localhost:{port}/code_edit?code=def_{script}.py&type=function"
                    # print('\n url :',green(url+'\n',bold=True))
                elif '???' in line:
                    line=line.replace('- var','-; ')
                    line=line.replace(' ???','')
                    url=';'
                else:
                    script=line.split('()')[0]
                    # print('\n script :',yellow(script+'\n',bold=True))
                    script=script.split(' ')[2]      
                    # print('\n script :',yellow(script+'\n',bold=True))
                    subdir=line.split('.py : >')[0]
                    # print('\n subdir 1 :',yellow(subdir+'\n',bold=True))
                    subdir=subdir.split('in ')[1]
                    # print('\n subdir 2 :',yellow(subdir+'\n',bold=True))
                    line=line.replace('[','')
                    line=line.replace('- r','-; r')
                    line=line.replace('- d','-; d')            
                    line=line.replace(': >','<<:')                     
                    if 'route' in line:
                        url=f";<<url:http://localhost:{port}/code_edit_B?code=route_{script}.py&subdir={subdir}"
                    else:
                        url=f";<<url:http://localhost:{port}/code_edit_B?code=def_{script}.py&subdir={subdir}"       
                    # print('\n url :',green(url+'\n',bold=True))
                file.write('-'+line+url+';;;\n')
    # ===================================================================
    env.level=env.level[:-1]
    return 1
    


#  def_copy_dir***
def copy_dir(src_directory,dst_directory,file_types):
    '''
    MODIFIED : 2025-09-28T06:44:45.000Z

    description : copy a director to another directory
    
    how to call it : copy_dir(src_directory,dst_directory,file_types) 
        file_types : ex : *.*  or *.txt
    '''
    route="/copy_dir"
    env.level+='-'
    print('\n'+env.level,white('def copy_dir() in app.py : >\n',bold=True))
    loguer(env.level+' def copy_dir() in app.py : >')
    # ===================================================================    
    print('dst_directory in backup folder',yellow(dst_directory,bold=True))
    print('Directory to backup ;',yellow(src_directory,bold=True))
    if './' not in dst_directory:
        dst_directory='./'+dst_directory
    os.mkdir(dst_directory)
    file_list0=glob.glob("./"+src_directory+"/"+file_types)
    file_list=[]
    for fichier in file_list0:
        fichier2=fichier.split('\\')[1]
        fichier2=fichier2.strip()
        print(fichier2)
        if './' not in src_directory:
            src='./'+src_directory+'/'+fichier2
        else:
            src=src_directory+'/'+fichier2
        print('src :',cyan(src,bold=True))        
        dst=dst_directory+'/'+fichier2
        print('dst :',red(dst,bold=True))        
        if fichier2!='':
            shutil.copyfile(src, dst)
    # ===================================================================
    loguer(env.level+' def END OF copy_dir() in app.py : >')    
    env.level=env.level[:-1]
    return 1
    


#  def_create_connection***
def create_connection(db_file):
    '''
    MODIFIED : 2025-09-23T16:05:16.000Z
    description : create create connection to database
    
    how to call it : conn=create_connection(database)
    '''
    route="/create_connection"
    env.level+='-'
    print('\n'+env.level,white('def create_connection() in app.py : >\n',bold=True))
    loguer(env.level+' def create_connection() in app.py : >')
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    env.level=env.level[:-1]
    return conn  


#  def_create_db_and_table***
def create_db_and_table(db_name,table):
    '''
    MODIFIED : 2025-09-23T16:08:36.000Z
    description : create database and one table
    
    how to call it : create_db_and_table(db_name,table)
    '''
    route="/create_db_and_table"
    env.level+='-'
    print('\n'+env.level,white('def create_db_and_table() in app.py : >\n',bold=True))
    loguer(env.level+' def create_db_and_table() in app.py : >')
    # ===================================================================    
    print("\ndb_name : ",db_name)   
    print("table_name : ",table) 
    with open('./sqlite_databases_code/'+db_name+'/db_details.txt') as file:
        db_details_dict=json.loads(file.read())
    print('\ndb_details_dict : \n',yellow(db_details_dict,bold=True))    
    len_columns=len(db_details_dict['columns'])-1  
    #with sqlite3.connect(':memory:') as conn:
    with sqlite3.connect('./z_bases/'+db_name+'.db') as conn:
        c=conn.cursor()
        print(f"--- table : {table} creation")
        sql_create='CREATE TABLE IF NOT EXISTS '+table +'(`index` int PRIMARY KEY,'
        i=0
        for col in db_details_dict['columns']:
            if i<len_columns:
                sql_create=sql_create+col+' text ,'
            else:
                sql_create=sql_create+col+' text)'
            i+=1
        print('sql_create : \n',cyan(sql_create,bold=True))
        c.execute(sql_create)
        print(green(f"--- OK {table} table created",bold=True))
    # ===================================================================
    #loguer(env.level+' def END OF create_db_and_table() in app.py : >')    
    env.level=env.level[:-1]
    return() 
    


#  def_create_rte_for_create_db***
def create_rte_for_create_db(name):
    '''
    MODIFIED : 2025-10-29

    description : create a new files structure for management of a new database
    
    how to call it : result=create_rte_for_create_db(name)
    '''
    route="/create_rte_for_create_db"
    env.level+='-'
    print('\n'+env.level,white('def create_rte_for_create_db() in app.py : >\n',bold=True))
    loguer(env.level+' def create_rte_for_create_db() in app.py : >')
    # ===================================================================    
    db=name
    db_name=name.replace('./zbases/','')
    db_name=db_name.replace('.db','')
    name=name+'_create_db'
    filename='./code_app_routes/route_def_'+name+'.py'
    filename2='/route_def_'+name+'.py'
    description='Flask Route for the '+name+' Database Create DB action'
    print()
    print(' filename :\n',yellow(filename,bold=True))
    print()
    print()
    print(' filename2 :\n',yellow(filename2,bold=True))
    print()
    print(' description :\n',yellow(description,bold=True))
    print()
    print(magenta('--> CALL  A SUB FUNCTION :',bold=True))
    # check if file already exits
    with open('./code_architecture/app_functions.txt') as file:
        text_content2=file.read()    
    fichier_route = Path('./code_app_routes/route_def_'+name+'.py')    
    if fichier_route.is_file() or filename in text_content2:
        print(filename+' already exists ! Choose another name')
        message1="ALREADY EXIST"
        image="../static/images/nok.png" 
        message2="Choose another name"
        message3="/home"
        message4="Back Home"          
        PAGE_DESTINATION="operation_done"
        page_name="z_operation_done.html"
        loguer(env.level+' route END OF example_name() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]
        return 0
    else:
        print(yellow(f'     {filename} does NOT exists. Let s create it',bold=True))
        route='/'+db+"_create_db"
        title="FLASK APP GENERATOR"
        with open('./sqlite_databases_code/'+db+'/db_details.txt') as file:
            db_details_dict=json.loads(file.read())
        print('db_details_dict : \n',yellow(db_details_dict,bold=True))        
        len_columns=len(db_details_dict['columns'])-1
        menu='''
                    <li><a href="/">Back to main page</a></li>
                    <li><a href="/logout">log Out</a></li>
                    <li><a href="javascript:popup_window('/page_info?page=route_def_bases.py&route='''+route+'''','page_info',700,600);">:</a></li>
        '''       
        output='''<!DOCTYPE HTML>
<!-- description-->
<html>
    <head>
        <title>'''+title+'''</title>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no" />
        <link rel="stylesheet" href="../static/assets/css/main.css" />
    <script>
        function popup_window( url, id, width, height )
        {
            //extract the url parameters if any, and pass them to the called html
            var tempvar=document.location.toString(); // fetch the URL string
            var passedparams = tempvar.lastIndexOf("?");
            if(passedparams > -1)
                url += tempvar.substring(passedparams);
            popup = window.open( url, id, 'toolbar=no,scrollbars=yes,location=yes,statusbar=yes,menubar=no,resizable=yes,width=' + width + ',height=' + height + '' );
            popup.focus();
        }
    </script>
    </head>
    <body class="is-preload">
        <!-- Nav -->
            <nav id="nav">
                <ul>
                '''+menu+'''
                </ul>
            </nav>
        <!-- Portfolio -->
			<article id="top" class="wrapper style1">
				<div class="container">
					<div class="row">
						<div class="col-4 col-5-large col-12-medium">
							<span class="image fit"><img src="../static/images/ok.png" alt="" /></span>
						</div>
						<div class="col-8 col-7-large col-12-medium">
							<header>
								<h1><strong> Database :'''+db+''', was created</strong></h1>
							</header>
							<p>The SQLITE had been created in ./z_bases</p>
                            <a href="/'''+db+'''_dashboard" class="button small scrolly">Go to Dashboard for '''+db+''' DB </a>
						</div>						
					</div>				
				</div>
			</article>
        <!-- Scripts -->
            <script src="../static/assets/js/jquery.min.js"></script>
            <script src="../static/assets/js/jquery.scrolly.min.js"></script>
            <script src="../static/assets/js/init.js"></script>
            <script src="../static/assets/js/browser.min.js"></script>
            <script src="../static/assets/js/breakpoints.min.js"></script>
            <script src="../static/assets/js/util.js"></script>
            <script src="../static/assets/js/main.js"></script>
    </body>
</html>
'''
        text_content='''#  def_'''+db+'''_create_db***
@app.route('/'''+db+'''_create_db', methods=['GET'])
def '''+db+'''_create_db():
    \'\'\'
    '''+description+'''
    \'\'\'
    route="/'''+db+'''_create_db"
    env.level+=\'-\'
    print(\'\\n\'+env.level,white(\'route '''+db+'''_create_db() in ***app.py*** : >\\n\',bold=True))
    loguer(env.level+\' route '''+db+'''_create_db() in ***app.py*** : >\')
    if not session.get(\'logged_in\'):
        return render_template(\'login.html\')
    else:
        with open(\'./sqlite_databases_code/'''+db+'''/db_details.txt\') as file:
            db_details_dict=json.loads(file.read())
        print(\'db_details_dict : \\n\',yellow(db_details_dict,bold=True))
        file=open('./sqlite_databases_code/'''+db+'''/init/'''+db+'''.csv','w')
        ligne_out=\'\'
        len_columns=len(db_details_dict[\'columns\'])-1
        i=0        
        for col in db_details_dict[\'columns\']:
            if i<len_columns:
                ligne_out=ligne_out+col+\','
            else:
                ligne_out=ligne_out+col
            i+=1
        file.write(ligne_out+\'\\n\')
        for i in range (0,10):
            ligne_out=\'''' 
        i=0
        for col in db_details_dict['columns']:
            if i<len_columns:
                text_content=text_content+col+"'+str(i)+','+'"
            else:
                text_content=text_content=text_content+col+"'+str(i)"
            i+=1        
        text_content=text_content+'''           
            file.write(ligne_out+\'\\n\')
        file.close()  
        create_db_and_table(db_details_dict[\'db_name\'],db_details_dict[\'table_name\'])
        html_output=\'\'\''''+output+'''\'\'\'
        loguer(env.level+\' route END OF '''+db+'''_create_db() in ***app.py*** : >\')
        # ===================================================================
        env.level=env.level[:-1]    
        return html_output
'''        
        filename='./code_app_routes/route_def_'+db+'_create_db.py'
        with open(filename,"w") as fichier:
            fichier.write(text_content)     
        with open('./code_architecture/app_routes.txt',"a+") as fichier:
            filename2=filename2.replace('/','')
            fichier.write(filename2+'\n')  
        result=1
    # ===================================================================
    loguer(env.level+' def END OF create_rte_for_create_db() in app.py : >')    
    env.level=env.level[:-1]
    return result
    


#  def_create_rte_for_db_clear_function***
def create_rte_for_db_clear_function(name):
    '''
    MODIFIED : 2025-10-29

    description : Ingest demo data into the database
    
    how to call it : result=create_rte_for_db_clear_function(name)
    '''
    route="/create_rte_for_db_clear_function"
    env.level+='-'
    print('\n'+env.level,white('def create_rte_for_db_clear_function() in app.py : >\n',bold=True))
    loguer(env.level+' def create_rte_for_db_clear_function() in app.py : >')
    # ===================================================================    
    db=name
    db_name=name.replace('./zbases/','')
    db_name=db_name.replace('.db','')
    name=name+'_db_clear'
    filename='./code_app_routes/route_def_'+name+'.py'
    filename2='/route_def_'+name+'.py'
    description='Flask Route for the '+name+' Database Clearing / reset function'
    print()
    print(' filename :\n',yellow(filename,bold=True))
    print()
    print(' filename2 :\n',yellow(filename2,bold=True))
    print()
    print(' description :\n',yellow(description,bold=True))
    print()
    print(magenta('--> CALL  A SUB FUNCTION :',bold=True))
    # check if file already exits
    with open('./code_architecture/app_routes.txt') as file:
        text_content2=file.read()    
    fichier_route = Path('./code_app_routes/route_def_'+name+'.py')    
    if fichier_route.is_file() or filename in text_content2:
        print(filename+' already exists ! Choose another name')
        message1="ALREADY EXIST"
        image="../static/images/nok.png" 
        message2="Choose another name"
        message3="/home"
        message4="Back Home"          
        PAGE_DESTINATION="operation_done"
        page_name="z_operation_done.html"
        loguer(env.level+' route END OF example_name() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]
        return 0
    else:
        print(yellow(f'     {filename} does NOT exists. Let s create it',bold=True))
        route="/"+db+"_db_clear"
        title="FLASK APP GENERATOR"
        with open('./sqlite_databases_code/'+db+'/db_details.txt') as file:
            db_details_dict=json.loads(file.read())
        print('db_details_dict : \n',yellow(db_details_dict,bold=True))       
        
        menu='''
                    <li><a href="/">Back to main page</a></li>
                    <li><a href="/logout">log Out</a></li>
                    <li><a href="javascript:popup_window('/page_info?page=route_def_'''+db+'''_db_clear.py&route='''+route+'''','page_info',700,600);">:</a></li>
        '''       
        output='''<!DOCTYPE HTML>
<!-- description-->
<html>
    <head>
        <title>'''+title+'''</title>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no" />
        <link rel="stylesheet" href="../static/assets/css/main.css" />
    <script>
        function popup_window( url, id, width, height )
        {
            //extract the url parameters if any, and pass them to the called html
            var tempvar=document.location.toString(); // fetch the URL string
            var passedparams = tempvar.lastIndexOf("?");
            if(passedparams > -1)
                url += tempvar.substring(passedparams);
            popup = window.open( url, id, 'toolbar=no,scrollbars=yes,location=yes,statusbar=yes,menubar=no,resizable=yes,width=' + width + ',height=' + height + '' );
            popup.focus();
        }
    </script>
    </head>
    <body class="is-preload">
        <!-- Nav -->
            <nav id="nav">
                <ul>
                '''+menu+'''
                </ul>
            </nav>
        <!-- Portfolio -->
			<article id="top" class="wrapper style1">
				<div class="container">
					<div class="row">
						<div class="col-4 col-5-large col-12-medium">
							<span class="image fit"><img src="../static/images/ok.png" alt="" /></span>
						</div>
						<div class="col-8 col-7-large col-12-medium">
							<header>
								<h1><strong>Database Content Deleted</strong></h1>
							</header>
							<p>Data in Database : '''+db+''' had been cleaned</p>
                            <a href="/'''+db+'''_dashboard" class="button small scrolly">Go to Dashboard for '''+db+''' DB </a>
						</div>						
					</div>				
				</div>
			</article>
        <!-- Scripts -->
            <script src="../static/assets/js/jquery.min.js"></script>
            <script src="../static/assets/js/jquery.scrolly.min.js"></script>
            <script src="../static/assets/js/init.js"></script>
            <script src="../static/assets/js/browser.min.js"></script>
            <script src="../static/assets/js/breakpoints.min.js"></script>
            <script src="../static/assets/js/util.js"></script>
            <script src="../static/assets/js/main.js"></script>
    </body>
</html>
'''
        text_content='''#  def_'''+db+'''_db_clear***
@app.route('/'''+db+'''_db_clear', methods=['GET'])
def '''+db+'''_db_clear():
    \'\'\'
    '''+description+'''
    \'\'\'
    route="/'''+db+'''_db_clear"
    env.level+=\'-\'
    print(\'\\n\'+env.level,white(\'route '''+db+'''_db_clear() in ***app.py*** : >\\n\',bold=True))
    loguer(env.level+\' route '''+db+'''_db_clear() in ***app.py*** : >\')
    if not session.get(\'logged_in\'):
        return render_template(\'login.html\')
    else:
        with open(\'./sqlite_databases_code/'''+db+'''/db_details.txt\') as file:
            db_details_dict=json.loads(file.read())
        print(\'db_details_dict : \\n\',yellow(db_details_dict,bold=True))
        database = os.getcwd()+\'/z_bases/'''+db+'''.db\'
        database=database.replace("\\\\","/")
        print(\'database is :\',database)
        print(\'table is :\', db_details_dict["table_name"])
        conn=create_connection(database) # open connection to database
        if conn:
            # connection to database is OK
            c=conn.cursor()
            print(f\'- Deleting table : {db_details_dict["table_name"]} =>\')
            sql_request="drop table "+db_details_dict["table_name"]
            c.execute(sql_request)
            conn.commit()
            print(\'-- OK DONE : Deleted table : \'+db_details_dict["table_name"])
            create_db_and_table(db_details_dict["db_name"],db_details_dict["table_name"])
            print(f\'-- OK table {db_details_dict["table_name"]} reseted\')     
'''        

        text_content=text_content+'''
        html_output=\'\'\''''+output+'''\'\'\'
        loguer(env.level+\' route END OF '''+db+'''_db_clear() in ***app.py*** : >\')
        # ===================================================================
        env.level=env.level[:-1]    
        return html_output
'''        
        filename='./code_app_routes/route_def_'+db+'_db_clear.py'
        with open(filename,"w") as fichier:
            fichier.write(text_content)     
        with open('./code_architecture/app_routes.txt',"a+") as fichier:
            filename2=filename2.replace('/','')
            fichier.write(filename2+'\n')  
        result=1
    # ===================================================================
    loguer(env.level+' def END OF create_rte_for_db_clear_function() in app.py : >')    
    env.level=env.level[:-1]
    return result
    


#  def_create_rte_for_db_demo_data***
def create_rte_for_db_demo_data(name):
    '''
    MODIFIED : 2025-10-29

    description : Ingest demo data into the database
    
    how to call it : result=create_rte_for_db_demo_data(name)
    '''
    route="/create_rte_for_db_demo_data"
    env.level+='-'
    print('\n'+env.level,white('def create_rte_for_db_demo_data() in app.py : >\n',bold=True))
    loguer(env.level+' def create_rte_for_db_demo_data() in app.py : >')
    # ===================================================================    
    db=name
    db_name=name.replace('./zbases/','')
    db_name=db_name.replace('.db','')
    name=name+'_ingest_demo_data'
    filename='./code_app_routes/route_def_'+name+'.py'
    filename2='/route_def_'+name+'.py'
    description='Flask Route for the '+name+' Database Ingest demo data'
    print()
    print(' filename :\n',yellow(filename,bold=True))
    print()
    print(' filename2 :\n',yellow(filename2,bold=True))
    print()
    print(' description :\n',yellow(description,bold=True))
    print()
    print(magenta('--> CALL  A SUB FUNCTION :',bold=True))
    # check if file already exits
    with open('./code_architecture/app_routes.txt') as file:
        text_content2=file.read()    
    fichier_route = Path('./code_app_routes/route_def_'+name+'.py')    
    if fichier_route.is_file() or filename in text_content2:
        print(filename+' already exists ! Choose another name')
        message1="ALREADY EXIST"
        image="../static/images/nok.png" 
        message2="Choose another name"
        message3="/home"
        message4="Back Home"          
        PAGE_DESTINATION="operation_done"
        page_name="z_operation_done.html"
        loguer(env.level+' route END OF example_name() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]
        return 0
    else:
        print(yellow(f'     {filename} does NOT exists. Let s create it',bold=True))
        route='/'+name+"_ingest_demo_data"
        title="FLASK APP GENERATOR"
        with open('./sqlite_databases_code/'+db_name+'/db_details.txt') as file:
            db_details_dict=json.loads(file.read())
        print('db_details_dict : \n',yellow(db_details_dict,bold=True))       
        
        menu='''
                    <li><a href="/">Back to main page</a></li>
                    <li><a href="/logout">log Out</a></li>
                    <li><a href="javascript:popup_window('/page_info?page=route_def_'''+db+'''.py&route='''+route+'''','page_info',700,600);">:</a></li>
        '''       
        output='''<!DOCTYPE HTML>
<!-- description-->
<html>
    <head>
        <title>'''+title+'''</title>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no" />
        <link rel="stylesheet" href="../static/assets/css/main.css" />
    <script>
        function popup_window( url, id, width, height )
        {
            //extract the url parameters if any, and pass them to the called html
            var tempvar=document.location.toString(); // fetch the URL string
            var passedparams = tempvar.lastIndexOf("?");
            if(passedparams > -1)
                url += tempvar.substring(passedparams);
            popup = window.open( url, id, 'toolbar=no,scrollbars=yes,location=yes,statusbar=yes,menubar=no,resizable=yes,width=' + width + ',height=' + height + '' );
            popup.focus();
        }
    </script>
    </head>
    <body class="is-preload">
        <!-- Nav -->
            <nav id="nav">
                <ul>
                '''+menu+'''
                </ul>
            </nav>
        <!-- Portfolio -->
			<article id="top" class="wrapper style1">
				<div class="container">
					<div class="row">
						<div class="col-4 col-5-large col-12-medium">
							<span class="image fit"><img src="../static/images/ok.png" alt="" /></span>
						</div>
						<div class="col-8 col-7-large col-12-medium">
							<header>
								<h1><strong>Demo Data ingested</strong></h1>
							</header>
							<p>Demo Data ingested into Database :'''+db+'''</p>
                            <a href="/'''+db+'''_dashboard" class="button small scrolly">Go to Dashboard for '''+db+''' DB </a>
						</div>						
					</div>				
				</div>
			</article>
        <!-- Scripts -->
            <script src="../static/assets/js/jquery.min.js"></script>
            <script src="../static/assets/js/jquery.scrolly.min.js"></script>
            <script src="../static/assets/js/init.js"></script>
            <script src="../static/assets/js/browser.min.js"></script>
            <script src="../static/assets/js/breakpoints.min.js"></script>
            <script src="../static/assets/js/util.js"></script>
            <script src="../static/assets/js/main.js"></script>
    </body>
</html>
'''
        text_content='''#  def_'''+db+'''_ingest_demo_data***
@app.route('/'''+db+'''_ingest_demo_data', methods=['GET'])
def '''+db+'''_ingest_demo_data():
    \'\'\'
    '''+description+'''
    \'\'\'
    route="/'''+db+'''_ingest_demo_data"
    env.level+=\'-\'
    print(\'\\n\'+env.level,white(\'route '''+db+'''_ingest_demo_data() in ***app.py*** : >\\n\',bold=True))
    loguer(env.level+\' route '''+db+'''_ingest_demo_data() in ***app.py*** : >\')
    if not session.get(\'logged_in\'):
        return render_template(\'login.html\')
    else:
        with open(\'./sqlite_databases_code/'''+db+'''/db_details.txt\') as file:
            db_details_dict=json.loads(file.read())
        print(\'db_details_dict : \\n\',yellow(db_details_dict,bold=True))
        database = os.getcwd()+\'/z_bases/'''+db+'''.db\'
        database=database.replace("\\\\","/")
        print(\'database is :\',database)
        lines=[]    
        file=\'./sqlite_databases_code/'''+db+'''/init/'''+db+'''.csv\'
        with open (file) as csvfile:
            reader = csv.reader(csvfile, delimiter=\',\')
            lines = list(reader)
            indexA=0
            print(\''''+db_details_dict['table_name']+''' table =>\\n\')
            conn=create_connection(database) # open connection to database            
            for row in lines:
                if conn:
                    # connection to database is OK
                    c=conn.cursor()
                    # let\'s go to every lines one by one and let\'s extract url, targeted brand
                    sqlite_data=[indexA]
                    sqlite_data=(indexA,'''
        len_columns=len(db_details_dict['columns'])-1
        i=0        
        for col in db_details_dict['columns']:
            if i<len_columns:
                text_content=text_content+'row['+str(i)+'] ,'
            else:
                text_content=text_content+'row['+str(i)+'])\n                    sql_add="INSERT OR IGNORE into '
                text_content=text_content+db_details_dict['table_name']+' (`index`,'
            i+=1   
        len_columns=len(db_details_dict['columns'])-1
        i=0        
        for col in db_details_dict['columns']:
            if i<len_columns:
                text_content=text_content+col+','
            else:
                text_content=text_content+col+') VALUES (?,'
            i+=1        
        i=0        
        for col in db_details_dict['columns']:
            if i<len_columns:
                text_content=text_content+'?,'
            else:
                text_content=text_content+'?)"'
            i+=1             
        text_content=text_content+'''
                    print('\\nsql_add :',cyan(sql_add,bold=True))
                c.execute(sql_add, sqlite_data)
                print(green("==> OK Done : demo data ingested",bold=True))
                indexA+=1
                conn.commit()        
'''        

        text_content=text_content+'''
        html_output=\'\'\''''+output+'''\'\'\'
        loguer(env.level+\' route END OF '''+db+'''_ingest_demo_data() in ***app.py*** : >\')
        # ===================================================================
        env.level=env.level[:-1]    
        return html_output
'''        
        filename='./code_app_routes/route_def_'+db+'_ingest_demo_data.py'
        with open(filename,"w") as fichier:
            fichier.write(text_content)     
        with open('./code_architecture/app_routes.txt',"a+") as fichier:
            filename2=filename2.replace('/','')
            fichier.write(filename2+'\n')  
        result=1
    # ===================================================================
    loguer(env.level+' def END OF create_rte_for_db_demo_data() in app.py : >')    
    env.level=env.level[:-1]
    return result
    


#  def_create_rte_for_db_read_function***
def create_rte_for_db_read_function(name):
    '''
    MODIFIED : 2025-09-30

    description : Read SQLITE DB Content and display result into a select box
    
    how to call it : create_rte_for_db_read_function(db_name)
    '''
    route="/create_rte_for_db_read_function"
    env.level+='-'
    print('\n'+env.level,white('def create_rte_for_db_read_function() in app.py : >\n',bold=True))
    loguer(env.level+' def create_rte_for_db_read_function() in app.py : >')
    # ===================================================================    
    db=name
    db_name=name.replace('./zbases/','')
    db_name=db_name.replace('.db','')
    name=name+'_db_read'
    filename='./code_app_routes/route_def_'+name+'.py'
    filename2='/route_def_'+name+'.py'
    description='Flask Route for the '+name+' Database Read DB content function'
    print()
    print(' filename :\n',yellow(filename,bold=True))
    print()
    print(' filename2 :\n',yellow(filename2,bold=True))
    print()
    print(' description :\n',yellow(description,bold=True))
    print()
    print(magenta('--> CALL  A SUB FUNCTION :',bold=True))
    # check if file already exits
    with open('./code_architecture/app_routes.txt') as file:
        text_content2=file.read()    
    fichier_route = Path('./code_app_routes/route_def_'+name+'.py')    
    if fichier_route.is_file() or filename in text_content2:
        print(filename+' already exists ! Choose another name')
        message1="ALREADY EXIST"
        image="../static/images/nok.png" 
        message2="Choose another name"
        message3="/home"
        message4="Back Home"          
        PAGE_DESTINATION="operation_done"
        page_name="z_operation_done.html"
        loguer(env.level+' route END OF example_name() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]
        return 0
    else:
        print(yellow(f'     {filename} does NOT exists. Let s create it',bold=True))
        route="/"+db+"_db_read"
        title="FLASK APP GENERATOR"
        with open('./sqlite_databases_code/'+db+'/db_details.txt') as file:
            db_details_dict=json.loads(file.read())
        print('db_details_dict : \n',yellow(db_details_dict,bold=True))       
        
        menu='''
                    <li><a href="/">Back to main page</a></li>
                    <li><a href="/'''+db+'''_dashboard">Back to Database Page</a></li>
                    <li><a href="/logout">log Out</a></li>
                    <li><a href="javascript:popup_window('/page_info?page=route_def_'''+db+'''_db_read.py&route='''+route+'''','page_info',700,600);">:</a></li>
        '''       
        output='''<!DOCTYPE HTML>
<!-- description-->
<html>
    <head>
        <title>'''+title+'''</title>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no" />
        <link rel="stylesheet" href="../static/assets/css/main.css" />
    <script>
        function popup_window( url, id, width, height )
        {
            //extract the url parameters if any, and pass them to the called html
            var tempvar=document.location.toString(); // fetch the URL string
            var passedparams = tempvar.lastIndexOf("?");
            if(passedparams > -1)
                url += tempvar.substring(passedparams);
            popup = window.open( url, id, 'toolbar=no,scrollbars=yes,location=yes,statusbar=yes,menubar=no,resizable=yes,width=' + width + ',height=' + height + '' );
            popup.focus();
        }
    </script>
    </head>
    <body class="is-preload">
        <!-- Nav -->
            <nav id="nav">
                <ul>
                '''+menu+'''
                </ul>
            </nav>
			<article id="indic_list" class="wrapper style4">
				<div class="container medium">
					<header>
						<h2>Database Content</h2>
                        <p>Select a Row</p>
						<p>Or refine Search by keyword (in any columns)</p>
					</header>
					<div class="row">
						<div class="col-12">
							<form method="get" action="/db_row_details">
                            	<input type="hidden" name="database" value="'''+db+'''">
                            	<input type="hidden" name="table" value="'''+db_details_dict['table_name']+'''"> 
                                <input type="hidden" name="columns" value="\'\'\'+columns+\'\'\'">                                
								<div class="row">
									<div class="col-12">
										<select id="row" name="row">
                                            \'\'\'+select_options+\'\'\'           
                                        </select>
									</div>      
									<div class="col-12">
										<ul class="actions">
                                            <li><input type="submit" value="Select this row" class="button small scrolly" /></li>
										</ul>
									</div>                                    
								</div>
							</form>
						</div>    
                        <form method="get" action="/'''+db+'''_db_read">
                            <div class="row">                        
                                <div class="col-6 col-12-small">
                                    <h3>Search Keyword :</h3>
                                </div>                                
                                <div class="col-6 col-12-small">
                                    <input type="text"  id="keyword" name="keyword" placeholder="keyword" />
                               </div>  
                                <div class="col-12">      
                                    <ul class="actions">
                                        <input type="submit" value="Search" class="button small scrolly" />
                                    </ul>
                                </div> 
                        </form>
					</div>
					<footer>
						<ul id="copyright">
							
						</ul>
					</footer>
				</div>
			</article>
        <!-- Scripts -->
            <script src="../static/assets/js/jquery.min.js"></script>
            <script src="../static/assets/js/jquery.scrolly.min.js"></script>
            <script src="../static/assets/js/init.js"></script>
            <script src="../static/assets/js/browser.min.js"></script>
            <script src="../static/assets/js/breakpoints.min.js"></script>
            <script src="../static/assets/js/util.js"></script>
            <script src="../static/assets/js/main.js"></script>
    </body>
</html>
'''
        text_content='''#  def_'''+db+'''_db_read***
@app.route('/'''+db+'''_db_read', methods=['GET'])
def '''+db+'''_db_read():
    \'\'\'
    '''+description+'''
    \'\'\'
    route="/'''+db+'''_db_read"
    env.level+=\'-\'
    print(\'\\n\'+env.level,white(\'route '''+db+'''_db_read() in ***app.py*** : >\\n\',bold=True))
    loguer(env.level+\' route '''+db+'''_db_read() in ***app.py*** : >\')
    if not session.get(\'logged_in\'):
        return render_template(\'login.html\')
    else:
        keyword=\'\'
        keyword=request.args.get("keyword")
        print("\\nkeyword : ",keyword)      
        with open(\'./sqlite_databases_code/'''+db+'''/db_details.txt\') as file:
            db_details_dict=json.loads(file.read())
        print(\'db_details_dict : \\n\',yellow(db_details_dict,bold=True))
        database = os.getcwd()+\'/z_bases/'''+db+'''.db\'
        database=database.replace("\\\\","/")
        print(\'database is :\',database)
        # sqlite:///:memory: (or, sqlite://)
        # sqlite:///relative/path/to/file.db
        # sqlite:////absolute/path/to/file.db
        db_name = "'''+db+'''.db"
        table_name = db_details_dict["table_name"]
        engine = sqlalchemy.create_engine("sqlite:///z_bases/%s" % db_name, execution_options={"sqlite_raw_colnames": True})
        df = pd.read_sql_table(table_name, engine)
        out_df = df[[\'index',\''''        
        len_columns=len(db_details_dict['columns'])-1
        i=0
        for col in db_details_dict['columns']:
            print(col)
            if i<len_columns:
                text_content=text_content+col+"','"
            else:
                text_content=text_content+col+"']]"
            i+=1
        text_content=text_content+'''
        #save result to csv file
        out_df.to_csv(r\'./result/'''+db+'''.csv\')
        df = DataFrame(out_df)
        #print (df)
        select_options=\'\'
        res = df.values.tolist()
        for item in res:
            if keyword:
                if keyword in item:
                    select_options=select_options+\'<option value="\'+str(item[0])+\'">\'+item[1]+\'</option>\'
            else:
                select_options=select_options+\'<option value="\'+str(item[0])+\'">\'+item[1]+\'</option>\'     
        print(\'=========================================\')
        columns="'''        
        i=0
        for col in db_details_dict['columns']:
            print(col)
            if i<len_columns:
                text_content=text_content+col+","
            else:
                text_content=text_content+col
            i+=1
        text_content=text_content+'''"                
        print(\'DONE\')        
        html_output=\'\'\''''+output+'''\'\'\'
        loguer(env.level+\' route END OF '''+db+'''_db_read() in ***app.py*** : >\')
        # ===================================================================
        env.level=env.level[:-1]    
        return html_output
'''        
        filename='./code_app_routes/route_def_'+db+'_db_read.py'
        with open(filename,"w") as fichier:
            fichier.write(text_content)     
        with open('./code_architecture/app_routes.txt',"a+") as fichier:
            filename2=filename2.replace('/','')
            fichier.write(filename2+'\n')  
        result=1
    # ===================================================================
    loguer(env.level+' def END OF create_rte_for_db_read_function() in app.py : >')    
    env.level=env.level[:-1]
    return result
    


#  def_create_rte_for_db_add_entry_function***
def create_rte_for_db_add_entry_function(name):
    '''
    MODIFIED : 2025-10-09

    description : create route for db add a new entry into database
    
    how to call it : create_rte_for_db_add_entry_function(name)
        name : de name
    ''' 
    route="/create_rte_for_db_add_entry_function"
    env.level+='-'
    print('\n'+env.level,white('def create_rte_for_db_add_entry_function() in app.py : >\n',bold=True))
    loguer(env.level+' def create_rte_for_db_add_entry_function() in app.py : >')
    # ===================================================================    
    db=name
    db_name=name.replace('./zbases/','')
    db_name=db_name.replace('.db','')
    name=name+'_db_add_entry'
    filename='./code_app_routes/route_def_'+name+'.py'
    filename2='/route_def_'+name+'.py'
    description='Flask Route for the '+name+' Database Update an entry'
    print()
    print(' filename :\n',yellow(filename,bold=True))
    print(' filename2 :\n',yellow(filename2,bold=True))
    print()
    print(magenta('--> CALL  A SUB FUNCTION :',bold=True))
    # check if file already exits
    with open('./code_architecture/app_routes.txt') as file:
        text_content2=file.read()    
    fichier_route = Path('./code_app_routes/route_def_'+name+'.py')    
    if fichier_route.is_file() or filename in text_content2:
        print(red('ERROR !!',bold=True))
        print(filename+' already exists ! Choose another name')
        message1="ALREADY EXIST"
        image="../static/images/nok.png" 
        message2="Choose another name"
        message3="/home"
        message4="Back Home"        
        PAGE_DESTINATION="operation_done"
        page_name="z_operation_done.html"
        loguer(env.level+' route END OF example_name() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]
        return 0
    else:
        print(yellow(f'     {filename} does NOT exists. Let s create it',bold=True))
        route="/"+db+"_db_add_entry"
        title="FLASK APP GENERATOR"
        with open('./sqlite_databases_code/'+db+'/db_details.txt') as file:
            db_details_dict=json.loads(file.read())
        print('db_details_dict : \n',yellow(db_details_dict,bold=True))       
        # STEP 1 create the formular
        text_content='''#  def_'''+db+'''_db_add_entry***
@app.route('/'''+db+'''_db_add_entry', methods=['GET'])
def '''+db+'''_db_add_entry():
    \'\'\'
    '''+description+'''
    \'\'\'
    route="/'''+db+'''_db_add_entry"
    env.level+=\'-\'
    print(\'\\n\'+env.level,white(\'route '''+db+'''_db_add_entry() in ***app.py*** : >\\n\',bold=True))
    loguer(env.level+\' route '''+db+'''_db_add_entry() in ***app.py*** : >\')
    if not session.get(\'logged_in\'):
        return render_template(\'login.html\')
    else:
        db_name = "'''+db+'''.db"
        column_list=[\''''
        len_columns=len(db_details_dict['columns'])-1
        i=0
        for col in db_details_dict['columns']:
            print(col)
            if i<len_columns:
                text_content=text_content+col+"','"
            else:
                text_content=text_content+col
            i=i+1
        text_content=text_content+'''\']
        print(\'\\ncolumn_list :\',cyan(column_list,bold=True))
        index=sqlite_db_get_last_index(\''''+db+'''\')
        index+=1        
        print(\'index : \',index)
        PAGE_DESTINATION="z_sqlite_db_add_entry"
        page_name="z_sqlite_db_add_entry.html"
        db_name=db_name.split(\'.\')[0]
        loguer(env.level+\' route END OF example_name() in ***app.py*** : >\')
        # ===================================================================
        env.level=env.level[:-1]
        return render_template(\'main_index.html\',route=route,USERNAME=session[\'user\'],PAGE_DESTINATION=PAGE_DESTINATION,page_name=page_name,column_list=column_list,index=index,db_name=db_name)
 
'''        
        filename='./code_app_routes/route_def_'+db+'_db_add_entry.py'
        with open(filename,"w") as fichier:
            fichier.write(text_content)     
        with open('./code_architecture/app_routes.txt',"a+") as fichier:
            filename2=filename2.replace('/','')
            fichier.write(filename2+'\n')  
        # STEP 2 create the add entry in sqlite data base route           
        text_content='''#  def_'''+db+'''_db_add_entry_ok***
@app.route('/'''+db+'''_db_add_entry_ok', methods=['GET'])
def '''+db+'''_db_add_entry_ok():
    \'\'\'
    '''+description+'''
    \'\'\'
    route="/'''+db+'''_db_add_entry_ok"
    env.level+=\'-\'
    print(\'\\n\'+env.level,white(\'route '''+db+'''_db_add_entry_ok() in ***app.py*** : >\\n\',bold=True))
    loguer(env.level+\' route '''+db+'''_db_add_entry_ok() in ***app.py*** : >\')
    if not session.get(\'logged_in\'):
        return render_template(\'login.html\')
    else:\n'''
        for col in db_details_dict['columns']:
            print(col)
            text_content=text_content+'        '+col+'=request.args.get("'+col+'")\n        print("\\n'+col+': ",'+col+')\n'
        text_content=text_content+'''
        db_name=request.args.get("db_name")
        print(\'db_name :\',db_name)     
        with open(\'./sqlite_databases_code/\'+db_name+\'/db_details.txt\') as file:
            db_details_dict=json.loads(file.read())
        print(\'db_details_dict : \\n\',yellow(db_details_dict,bold=True)) 
        database = os.getcwd()+\'/z_bases/\'+db_name+\'.db\'
        database=database.replace("\\\\","/")
        table=db_details_dict[\'table_name\']
        print(\'database is :\',database) 
        print(\'table is :\',table)          
        # Get last index value in SQLITE DB
        new_index=sqlite_db_get_last_index(db_name)+1        
        print(\'new_index is :\',new_index)  
        sqlite_data=(new_index,'''
        len_columns=len(db_details_dict['columns'])-1
        i=0
        for col in db_details_dict['columns']:
            print(col)
            if i<len_columns:
                text_content=text_content+col+","
            else:
                text_content=text_content+col+")"
            i+=1        
        text_content=text_content+'''
        sql_add=f"INSERT OR IGNORE into {table} (`index`,'''
        i=0
        for col in db_details_dict['columns']:
            print(col)
            if i<len_columns:
                text_content=text_content+col+","
            else:
                text_content=text_content+col+")"
            i+=1           
        text_content=text_content+' VALUES (?,'
        i=0
        for col in db_details_dict['columns']:
            print(col)
            if i<len_columns:
                text_content=text_content+"?,"
            else:
                text_content=text_content+'?)"'
            i+=1         
        text_content=text_content+'''
        print(\'sqlite_data :\',sqlite_data)     
        print(\'sql_add :\',sql_add)          
        con = sqlite3.connect(database)       
        try:
            cur = con.cursor()
            cur.execute(sql_add,sqlite_data)
            con.commit()
            print(green(\'OK DONE ENTRY DELETED\',bold=True))
            image="../static/images/ok.png" 
            message1="Entry Added"
            message2="Entry was added to DB"
            message3=f"/{db_name}_dashboard"
            message4=f"{db_name}_dasbhoard"        
            PAGE_DESTINATION="operation_done"
            page_name="operation_done.html"            
            loguer(env.level+\' route END OF machin_db_add_entry_ok() in ***app.py*** : >\')    
            env.level=env.level[:-1]        
            return render_template(\'main_index.html\',route=route,USERNAME=session[\'user\'],PAGE_DESTINATION=PAGE_DESTINATION,message1=message1,message2=message2,message3=message3,message4=message4,image=image,page_name=page_name) 
        except:
            print(red(\'Error\',bold=True))
            image="../static/images/nok.png" 
            message1="Error"
            message2="An error occured"
            message3=f"/{db_name}_dashboard"
            message4=f"{db_name}_dasbhoard"        
            PAGE_DESTINATION="operation_done"
            page_name="operation_done.html"            
            loguer(env.level+\' route END OF machin_db_add_entry_ok() in ***app.py*** : >\')    
            env.level=env.level[:-1]        
            return render_template(\'main_index.html\',route=route,USERNAME=session[\'user\'],PAGE_DESTINATION=PAGE_DESTINATION,message1=message1,message2=message2,message3=message3,message4=message4,image=image,page_name=page_name)

'''        
        filename='./code_app_routes/route_def_'+db+'_db_add_entry_ok.py'
        with open(filename,"w") as fichier:
            fichier.write(text_content)     
        filename2='route_def_'+db+'_db_add_entry_ok.py'    
        with open('./code_architecture/app_routes.txt',"a+") as fichier:
            filename2=filename2.replace('/','')
            fichier.write(filename2+'\n')              
        result=1
    
    # ===================================================================
    loguer(env.level+' def END OF create_rte_for_db_add_entry_function() in app.py : >')    
    env.level=env.level[:-1]
    return result
    


#  def_create_rte_for_db_delete_entry_function***
def create_rte_for_db_delete_entry_function(name):
    '''
    MODIFIED : 2025-10-02

    description : create route for db delete entry
    
    how to call it : create_rte_for_db_delete_entry_function(name)
        name = db name
    '''
    route="/create_rte_for_db_delete_entry_function"
    env.level+='-'
    print('\n'+env.level,white('def create_rte_for_db_delete_entry_function() in app.py : >\n',bold=True))
    loguer(env.level+' def create_rte_for_db_delete_entry_function() in app.py : >')
    # ===================================================================    
    db=name
    db_name=name.replace('./zbases/','')
    db_name=db_name.replace('.db','')
    name=name+'_db_delete_entry'
    filename='./code_app_routes/route_def_'+name+'.py'
    filename2='/route_def_'+name+'.py'
    description='Flask Route for the '+name+' Database delete entry'
    print()
    print(' filename :\n',yellow(filename,bold=True))
    print()
    print(' filename2 :\n',yellow(filename2,bold=True))
    print()
    print(magenta('--> CALL  A SUB FUNCTION :',bold=True))
    # check if file already exits
    with open('./code_architecture/app_routes.txt') as file:
        text_content2=file.read()    
    fichier_route = Path('./code_app_routes/route_def_'+name+'.py')    
    if fichier_route.is_file() or filename in text_content2:
        print(filename+' already exists ! Choose another name')
        message1="ALREADY EXIST"
        image="../static/images/nok.png" 
        message2="Choose another name"
        message3="/home"
        message4="Back Home"          
        PAGE_DESTINATION="operation_done"
        page_name="z_operation_done.html"
        loguer(env.level+' route END OF example_name() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]
        return 0
    else:
        print(yellow(f'     {filename} does NOT exists. Let s create it',bold=True))
        route="/"+db+"_db_delete_entry"
        title="FLASK APP GENERATOR"
        with open('./sqlite_databases_code/'+db+'/db_details.txt') as file:
            db_details_dict=json.loads(file.read())
        print('db_details_dict : \n',yellow(db_details_dict,bold=True))       
        
        text_content='''#  def_'''+db+'''_db_delete_entry***
@app.route('/'''+db+'''_db_delete_entry', methods=['GET'])
def '''+db+'''_db_delete_entry():
    \'\'\'
    '''+description+'''
    \'\'\'
    route="/'''+db+'''_db_delete_entry"
    env.level+=\'-\'
    print(\'\\n\'+env.level,white(\'route '''+db+'''_db_delete_entry() in ***app.py*** : >\\n\',bold=True))
    loguer(env.level+\' route '''+db+'''_db_delete_entry() in ***app.py*** : >\')
    if not session.get(\'logged_in\'):
        return render_template(\'login.html\')
    else:
        row=request.args.get("row")
        print("\\nrow : ",row)
        result=sqlite_db_delete_entry(\''''+db+'''\',row)         
        message1="OK done - Entry DELETED"
        image="../static/images/ok.png" 
        message2="entry had been deleted"
        message3="/'''+db+'''_dashboard"
        message4="'''+db+''' Dashboard"
        PAGE_DESTINATION="operation_done"
        page_name="operation_done.html"
        loguer(env.level+\' route END OF example_name() in ***app.py*** : >\')
        # ===================================================================
        env.level=env.level[:-1]
        return render_template(\'main_index.html\',route=route,USERNAME=session[\'user\'],PAGE_DESTINATION=PAGE_DESTINATION,message1=message1,message2=message2,message3=message3,message4=message4,image=image,page_name=page_name)
 
'''        
        filename='./code_app_routes/route_def_'+db+'_db_delete_entry.py'
        with open(filename,"w") as fichier:
            fichier.write(text_content)     
        with open('./code_architecture/app_routes.txt',"a+") as fichier:
            filename2=filename2.replace('/','')
            fichier.write(filename2+'\n')  
        result=1
    
    # ===================================================================
    loguer(env.level+' def END OF create_rte_for_db_delete_entry_function() in app.py : >')    
    env.level=env.level[:-1]
    return result
    


#  def_create_rte_for_db_update_entry_function***
def create_rte_for_db_update_entry_function(name):
    '''
    MODIFIED : 2025-09-30T15:23:41.000Z

    description : create route for db update entry
    
    how to call it :
    '''
    route="/create_rte_for_db_update_entry_function"
    env.level+='-'
    print('\n'+env.level,white('def create_rte_for_db_update_entry_function() in app.py : >\n',bold=True))
    loguer(env.level+' def create_rte_for_db_update_entry_function() in app.py : >')
    # ===================================================================    
    db=name
    db_name=name.replace('./zbases/','')
    db_name=db_name.replace('.db','')
    name=name+'_db_update_entry'
    filename='./code_app_routes/route_def_'+name+'.py'
    filename2='/route_def_'+name+'.py'
    description='Flask Route for the '+name+' Database Update an entry'
    print()
    print(' filename :\n',yellow(filename,bold=True))
    print()
    print(' filename2 :\n',yellow(filename2,bold=True))
    print()
    print(magenta('--> CALL  A SUB FUNCTION :',bold=True))
    # check if file already exits
    with open('./code_architecture/app_routes.txt') as file:
        text_content2=file.read()    
    fichier_route = Path('./code_app_routes/route_def_'+name+'.py')    
    if fichier_route.is_file() or filename in text_content2:
        print(filename+' already exists ! Choose another name')
        message1="ALREADY EXIST"
        image="../static/images/nok.png" 
        message2="Choose another name"
        message3="/home"
        message4="Back Home"          
        PAGE_DESTINATION="operation_done"
        page_name="z_operation_done.html"
        loguer(env.level+' route END OF example_name() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]
        return 0
    else:
        print(yellow(f'     {filename} does NOT exists. Let s create it',bold=True))
        route="/"+db+"_db_update_entry"
        title="FLASK APP GENERATOR"
        with open('./sqlite_databases_code/'+db+'/db_details.txt') as file:
            db_details_dict=json.loads(file.read())
        print('db_details_dict : \n',yellow(db_details_dict,bold=True))       
        
        text_content='''#  def_'''+db+'''_db_update_entry***
@app.route('/'''+db+'''_db_update_entry', methods=['GET'])
def '''+db+'''_db_update_entry():
    \'\'\'
    '''+description+'''
    \'\'\'
    route="/'''+db+'''_db_update_entry"
    env.level+=\'-\'
    print(\'\\n\'+env.level,white(\'route '''+db+'''_db_update_entry() in ***app.py*** : >\\n\',bold=True))
    loguer(env.level+\' route '''+db+'''_db_update_entry() in ***app.py*** : >\')
    if not session.get(\'logged_in\'):
        return render_template(\'login.html\')
    else:
        row=request.args.get("row")
        print("\\nrow : ",row)'''
        len_columns=len(db_details_dict['columns'])-1
        i=0
        for col in db_details_dict['columns']:
            print(col)
            if i<len_columns:
                text_content=text_content+'''\n        '''+col+'''=request.args.get(\''''+col+'''\')\n        print('\\n'''+col+''' : \','''+col+''')'''  
        text_content=text_content+'''
        with open(\'./sqlite_databases_code/'''+db+'''/db_details.txt\') as file:
            db_details_dict=json.loads(file.read())
        print(\'db_details_dict : \\n\',yellow(db_details_dict,bold=True))        
        db_name = "'''+db+'''.db"
        table_name = db_details_dict["table_name"]
        where_clause='`index` = '+row
        sql_fields=[\'index\',\''''
        i=0
        for col in db_details_dict['columns']:
            print(col)
            if i<len_columns:
                text_content=text_content+col+"','"
            else:
                text_content=text_content+col+"']"
            i+=1
        text_content=text_content+'''\n        sql_data_list=[int(row),'''
        i=0
        for col in db_details_dict['columns']:
            print(col)
            if i<len_columns:
                text_content=text_content+col+","
            else:
                text_content=text_content+col+"]"
            i+=1        
        
        text_content=text_content+'''
        result=sqlite_db_update_entry(db_name,table_name,where_clause,sql_fields,sql_data_list)        
        message1="OK done"
        image="../static/images/ok.png" 
        message2="entry had been updated"
        message3="/'''+db+'''_dashboard"
        message4="'''+db+''' Dashboard"
        PAGE_DESTINATION="operation_done"
        page_name="operation_done.html"
        loguer(env.level+\' route END OF example_name() in ***app.py*** : >\')
        # ===================================================================
        env.level=env.level[:-1]
        return render_template(\'main_index.html\',route=route,USERNAME=session[\'user\'],PAGE_DESTINATION=PAGE_DESTINATION,message1=message1,message2=message2,message3=message3,message4=message4,image=image,page_name=page_name)
 
'''        
        filename='./code_app_routes/route_def_'+db+'_db_update_entry.py'
        with open(filename,"w") as fichier:
            fichier.write(text_content)     
        with open('./code_architecture/app_routes.txt',"a+") as fichier:
            filename2=filename2.replace('/','')
            fichier.write(filename2+'\n')  
        result=1
    
    # ===================================================================
    loguer(env.level+' def END OF create_rte_for_db_update_entry_function() in app.py : >')    
    env.level=env.level[:-1]
    return result
    


#  def_create_rte_for_db_dashboard***
def create_rte_for_db_dashboard(name):
    '''
    MODIFIED : 2025-09-29
    description : create a new files structure for management of a new database
    
    how to call it : result=create_rte_for_db_dashboard(name)
    '''
    route="/create_rte_for_db_dashboard"
    env.level+='-'
    print('\n'+env.level,white('def create_rte_for_db_dashboard() in app.py : >\n',bold=True))
    loguer(env.level+' def create_rte_for_db_dashboard() in app.py : >')
    # ===================================================================    
    db=name
    name=name+'_dashboard'
    filename='./code_app_routes/route_def_'+name+'.py'
    filename2='/route_def_'+name+'.py'
    description='Flask Route for the '+name+' Database dashoard'
    print()
    print(' filename :\n',yellow(filename,bold=True))
    print()
    print()
    print(' filename2 :\n',yellow(filename2,bold=True))
    print()
    print(' description :\n',yellow(description,bold=True))
    print()
    print(magenta('--> CALL  A SUB FUNCTION :',bold=True))
    # check if file already exits
    with open('./code_architecture/app_routes.txt') as file:
        text_content2=file.read()
    fichier_route = Path('./code_app_routes/route_def_'+name+'.py')    
    if fichier_route.is_file() or filename in text_content2:
        print(filename+' already exists ! Choose another name')
        image="../static/images/nok.png"
        message2="Flask Route for this DB already exist"
        message3="/Message 3"
        message4="Message 4 in button"
        PAGE_DESTINATION="operation_done"
        page_name="z_operation_done.html"
        loguer(env.level+' route END OF example_name() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]
        return 0
    else:
        print(yellow(f'     {filename} does NOT exists. Let s create it',bold=True))
        route='/'+db+"_dashboard"
        title="FLASK APP GENERATOR"
        portfolio='''
                        <div class="col-4 col-6-medium col-12-small">
                            <article class="box style2">
                                <a href="/'''+db+'''_create_db" class="image featured"><img src="../static/images/database0.png" alt="" /></a>
                                <h3><a href="/'''+db+'''_create_db">Create Database</a></h3>
                                <p>Create the '''+db+''' Database</p>
                            </article>
                        </div>
                        <div class="col-4 col-6-medium col-12-small">
                            <article class="box style2">
                                <a href="/'''+db+'''_ingest_demo_data" class="image featured"><img src="../static/images/database0.png" alt="" /></a>
                                <h3><a href="/'''+db+'''_ingest_demo_data">Ingest Demo Data</a></h3>
                                <p>Ingest Demo Data into DB</p>
                            </article>
                        </div>
                        <div class="col-4 col-6-medium col-12-small">
                            <article class="box style2">
                                <a href="/'''+db+'''_db_read" class="image featured"><img src="../static/images/database0.png" alt="" /></a>
                                <h3><a href="/'''+db+'''_db_read">Read Database content</a></h3>
                                <p>Read DB an Create a CSV result</p>
                            </article>
                        </div>
                        <div class="col-4 col-6-medium col-12-small">
                            <article class="box style2">
                                <a href="/'''+db+'''_db_clear" class="image featured"><img src="../static/images/database0.png" alt="" /></a>
                                <h3><a href="/'''+db+'''_db_clear">Clear Database</a></h3>
                                <p>Delete Database content</p>
                            </article>
                        </div>
                        <div class="col-4 col-6-medium col-12-small">
                            <article class="box style2">
                                <a href="/'''+db+'''_db_ingest_csv" class="image featured"><img src="../static/images/database0.png" alt="" /></a>
                                <h3><a href="/'''+db+'''_db_ingest_csv">Ingest a CSV file</a></h3>
                                <p>Ingest a CSV file</p>
                            </article>
                        </div>
                        <div class="col-4 col-6-medium col-12-small">
                            <article class="box style2">
                                <a href="/'''+db+'''_db_add_entry" class="image featured"><img src="../static/images/database0.png" alt="" /></a>
                                <h3><a href="/'''+db+'''_db_add_entry">Add Entry</a></h3>
                                <p>Add an Entry to Database</p>
                            </article>
                        </div>
            '''
        menu='''
                    <li><a href="/">Back to main page</a></li>
                    <li><a href="/logout">log Out</a></li>
                    <li><a href="javascript:popup_window('/page_info?page=route_def_'''+db+'''_dashboard.py&route='''+route+'''','page_info',700,600);">:</a></li>
        '''
        output='''<!DOCTYPE HTML>
<!-- description-->
<html>
    <head>
        <title>'''+title+'''</title>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no" />
        <link rel="stylesheet" href="../static/assets/css/main.css" />
    <script>
        function popup_window( url, id, width, height )
        {
            //extract the url parameters if any, and pass them to the called html
            var tempvar=document.location.toString(); // fetch the URL string
            var passedparams = tempvar.lastIndexOf("?");
            if(passedparams > -1)
                url += tempvar.substring(passedparams);
            popup = window.open( url, id, 'toolbar=no,scrollbars=yes,location=yes,statusbar=yes,menubar=no,resizable=yes,width=' + width + ',height=' + height + '' );
            popup.focus();
        }
    </script>
    </head>
    <body class="is-preload">
        <!-- Nav -->
            <nav id="nav">
                <ul>
                '''+menu+'''
                </ul>
            </nav>
        <!-- Portfolio -->
            <article id="portfolio" class="wrapper style3">
                <div class="container">
                    <header>
                        <h2>'''+db+''' Database</h2>
                    </header>
                    <div class="row">'''
        output=output+portfolio
        output=output+'''
                    </div>
                </div>
            </article>
        <!-- Scripts -->
            <script src="../static/assets/js/jquery.min.js"></script>
            <script src="../static/assets/js/jquery.scrolly.min.js"></script>
            <script src="../static/assets/js/init.js"></script>
            <script src="../static/assets/js/browser.min.js"></script>
            <script src="../static/assets/js/breakpoints.min.js"></script>
            <script src="../static/assets/js/util.js"></script>
            <script src="../static/assets/js/main.js"></script>
    </body>
</html>
'''
        text_content='''#  def_'''+db+'''_dashboard***
@app.route('/'''+db+'''_dashboard', methods=['GET'])
def '''+db+'''_dashboard():
    \'\'\'
    '''+description+'''
    \'\'\'
    route="/'''+db+'''_dashboard"
    env.level+=\'-\'
    print(\'\\n\'+env.level,white(\'route '''+db+'''_dashboard() in ***app.py*** : >\\n\',bold=True))
    loguer(env.level+\' route '''+db+'''_dashboard() in ***app.py*** : >\')
    if not session.get(\'logged_in\'):
        return render_template(\'login.html\')
    else:
        html_output=\'\'\''''+output+'''\'\'\'
        loguer(env.level+\' route END OF '''+db+'''_dashboard() in ***app.py*** : >\')
        # ===================================================================
        env.level=env.level[:-1]
        return html_output
        '''
        filename='./code_app_routes/route_def_'+db+'_dashboard.py'
        with open(filename,"w") as fichier:
            fichier.write(text_content)
        with open('./code_architecture/app_routes.txt',"a+") as fichier:
            filename2=filename2.replace('/','')
            fichier.write(filename2+'\n')
        result=1
    # ===================================================================
    loguer(env.level+' def END OF create_rte_for_db_dashboard() in app.py : >')    
    env.level=env.level[:-1]
    return result
    


#  def_sqlite_db_add_entry***
def sqlite_db_add_entry(database,sql_request,sql_data_list):
    '''
    TO DEBUG !!
    MODIFIED : 2025-10-09T15:09:17.000Z
    description : add a new entry in sqlite database
    
    how to call it : result=sqlite_db_add_entry(database,sql_request,sql_data_list)
    '''
    route="/sqlite_db_add_entry"
    env.level+='-'
    print('\n'+env.level,white('def sqlite_db_add_entry() in app.py : >\n',bold=True))
    loguer(env.level+' def sqlite_db_add_entry() in app.py : >')
    # ===================================================================    
    print('database :',database)
    print('sql_request :',sql_request)     
    print('sql_data_list :',sql_data_list)
    con = sqlite3.connect(database)
    try:
        cur = con.cursor()
        cur.execute(sql_add,sqlite_data)
        con.commit()
        print(green('OK DONE ENTRY ADDED INTEO DATABASE',bold=True))
        loguer(env.level+' route END OF machin_db_add_entry_ok() in ***app.py*** : >')
        env.level=env.level[:-1]
        return 1
    except:
        print(red('Error : could not add entry into database',bold=True))
        loguer(env.level+' route END OF machin_db_add_entry_ok() in ***app.py*** : >')
        env.level=env.level[:-1]
        return 0


#  def_sqlite_db_delete_entry***
def sqlite_db_delete_entry(db_name,row):
    '''
    MODIFIED : 2025-10-01T16:57:57.000Z

    description : delete a row from the sqllite Database
    
    how to call it : result = sqlite_db_delete_entry(db_name,row)
    '''
    route="/sqlite_db_delete_entry"
    env.level+='-'
    print('\n'+env.level,white('def sqlite_db_delete_entry() in app.py : >\n',bold=True))
    loguer(env.level+' def sqlite_db_delete_entry() in app.py : >')
    # ===================================================================    
    print()
    print('db_name :',db_name)     
    with open('./sqlite_databases_code/'+db_name+'/db_details.txt') as file:
        db_details_dict=json.loads(file.read())
    print('db_details_dict : \n',yellow(db_details_dict,bold=True)) 
    database = os.getcwd()+'/z_bases/'+db_name+'.db'
    database=database.replace("\\","/")
    table=db_details_dict['table_name']
    print('database is :',database) 
    print('table is :',table)   
    print('row to delete is :',row)     
    sql=f"DELETE FROM {table} where `index` = "+row
    print('\nsql request :',yellow(sql,bold=True))
    con = sqlite3.connect(database)       
    try:
        cur = con.cursor()
        cur.execute(sql)
        con.commit()
        print(green('OK DONE ENTRY DELETED',bold=True))
        loguer(env.level+' def END OF sqlite_db_delete_entry() in app.py : >')    
        env.level=env.level[:-1]        
        return 1
    except:
        print(red('Error',bold=True))
        loguer(env.level+' def END OF sqlite_db_delete_entry() in app.py : >')    
        env.level=env.level[:-1]                
        return 0



#  def_sqlite_db_get_last_index***
def sqlite_db_get_last_index(db_name):
    '''
    MODIFIED : 2025-10-02T08:49:29.000Z
    description : retrieve highest index value of entries into a database
    
    how to call it : last_index=sqlite_db_get_last_index(db_name)
    
        db_name : database name ( without .db extension )
    '''
    route="/sqlite_db_get_last_index"
    env.level+='-'
    print('\n'+env.level,white('def sqlite_db_get_last_index() in app.py : >\n',bold=True))
    loguer(env.level+' def sqlite_db_get_last_index() in app.py : >')
    # ===================================================================    
    with open('./sqlite_databases_code/'+db_name+'/db_details.txt') as file:
        db_details_dict=json.loads(file.read())
    print('db_details_dict : \n',yellow(db_details_dict,bold=True))
    database = os.getcwd()+'/z_bases/'+db_name+'.db'
    database=database.replace("\\","/")
    print('database is :',database)
    if '.db' not in db_name:
        db_name = db_name+".db"
    table_name = db_details_dict["table_name"]
    print('table_name is :',table_name)    
    index=0
    with sqlite3.connect(database) as conn:
        cursor=conn.cursor()
        sql_request = f"SELECT * from {table_name}"
        print('\nsql_request : ',sql_request)
        try:
            cursor.execute(sql_request)
            for resultat in cursor:
                #print(resultat)
                if resultat[0]> index:
                    index=resultat[0]
        except:
            sys.exit("couldn't read database")
    # ===================================================================
    loguer(env.level+' def END OF sqlite_db_get_last_index() in app.py : >')    
    env.level=env.level[:-1]
    return index
    


#  def_sqlite_db_select_entry***
def sqlite_db_select_entry(database,table,where_clause):
    '''
    MODIFIED : 2025-09-26T08:40:02.000Z
    description : Search an entry in the selected SQLITE database
    
    how to call it :     resultats = sqlite_db_select_entry(database,table,where_clause) 
    '''
    route="/sqlite_db_select_entry"
    env.level+='-'
    print('\n'+env.level,white('def sqlite_db_select_entry() in app.py : >\n',bold=True))
    loguer(env.level+' def sqlite_db_select_entry() in app.py : >')
    # ===================================================================    
    database = os.getcwd()+'/z_bases/'+database+'.db'
    database=database.replace("\\","/")
    #database = './z_bases/'+database+'.db'
    print('database is :',database)    
    liste=[]
    columns=[]
    with sqlite3.connect(database) as conn:
        cursor=conn.cursor()           
        sql_request = f"SELECT * from {table} {where_clause}"
        print('\nsql_request : ',cyan(sql_request+'\n',bold=True))
        try:
            cursor.execute(sql_request)
            for resultat in cursor:
                print('entry found : ',resultat)
                liste.append(resultat)
        except:
            print(red('Error reading database',bold=True))
            sys.exit("couldn't read database")
    # ===================================================================
    print(' Result liste in sqlite_db_select_entry() : ',cyan(liste,bold=True))
    loguer(env.level+' def END OF sqlite_db_select_entry() in app.py : >')    
    env.level=env.level[:-1]
    return(liste) 
   

#  def_sqlite_db_update_entry***
def sqlite_db_update_entry(database,table,where_clause,sql_fields,sql_data_list):
    '''
    MODIFIED : 2025-10-01
    description : Update a row into the sqllite Database
    
    how to call it :     resultats = sqlite_db_update_entry(database,table,where_clause,sql_fields,sql_data_list) 
        database : DB name
        table : table name
        where_clause : where clause for selecting a row ex : where index = 2
        sql_fields : columns field list
        sql_data_list : data list of new data to ingest into the row
    '''
    route="/sqlite_db_update_entry"
    env.level+='-'
    print('\n'+env.level,white('def sqlite_db_update_entry() in app.py : >\n',bold=True))
    loguer(env.level+' def sqlite_db_update_entry() in app.py : >')
    # ===================================================================    
    if '.db' not in database:
        database = os.getcwd()+'/z_bases/'+database+'.db'
    else:
        database = os.getcwd()+'/z_bases/'+database
    database=database.replace("\\","/")
    #database = './z_bases/'+database+'.db'
    print('database is :',database)    
    with sqlite3.connect(database) as conn:
        cursor=conn.cursor()
        print('sql_data_list :',cyan(sql_data_list,bold=True))             
        sql_data=('')
        sql_data=sql_data_list
        sql_request = f"UPDATE {table} SET "
        i=0
        len_sql_data_list=len(sql_data_list)
        for item in sql_fields:
            if sql_data_list[i]==None:
                sql_data_list[i]=""
            if i<len_sql_data_list-1:
                if i==0:
                    sql_request =sql_request +"`"+item+"` = "+str(sql_data_list[i])+" , "
                else:
                    sql_request =sql_request + item +" = '"+sql_data_list[i]+"' , "
            else:
                sql_request =sql_request + item +" = '"+sql_data_list[i]+"'"
            i+=1
        if where_clause!='':
            if 'where' not in sql_request:
                sql_request=sql_request+' where '+where_clause
            else:
                sql_request=sql_request+' '+where_clause           
        print('sql_request :',cyan(sql_request,bold=True))
        cursor.execute(sql_request)
        result=1
    # ===================================================================
    loguer(env.level+' def END OF sqlite_db_update_entry() in app.py : >')    
    env.level=env.level[:-1]
    return(result) 
   

#  def_create_rte_for_db_ingest_cvs***
def create_rte_for_db_ingest_cvs(name):
    '''
    MODIFIED : 2025-10-09T19:46:56.000Z

    description : create route for csv file ingestion in Database
    
    how to call it : create_rte_for_db_ingest_cvs(db_name)
    '''
    route="/create_rte_for_db_ingest_cvs"
    env.level+='-'
    print('\n'+env.level,white('def create_rte_for_db_ingest_cvs() in app.py : >\n',bold=True))
    loguer(env.level+' def create_rte_for_db_ingest_cvs() in app.py : >')
    # ===================================================================    
    db=name
    db_name=name.replace('./zbases/','')
    db_name=db_name.replace('.db','')
    name=name+'_db_ingest_csv'
    filename='./code_app_routes/route_def_'+name+'.py'
    filename2='/route_def_'+name+'.py'
    description='Flask Route for the '+name+' Database Update an entry'
    print()
    print(' filename :\n',yellow(filename,bold=True))
    print()
    print(' filename2 :\n',yellow(filename2,bold=True))
    print()
    print(magenta('--> CALL  A SUB FUNCTION :',bold=True))
    # check if file already exits
    with open('./code_architecture/app_routes.txt') as file:
        text_content2=file.read()    
    fichier_route = Path('./code_app_routes/route_def_'+name+'.py')    
    if fichier_route.is_file() or filename in text_content2:
        print(filename+' already exists ! Choose another name')
        message1="ALREADY EXIST"
        image="../static/images/nok.png" 
        message2="Choose another name"
        message3="/home"
        message4="Back Home"          
        PAGE_DESTINATION="operation_done"
        page_name="z_operation_done.html"
        loguer(env.level+' route END OF example_name() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]
        return 0
    else:
        print(yellow(f'     {filename} does NOT exists. Let s create it',bold=True))
        route="/"+db+"_db_ingest_csv"
        title="FLASK APP GENERATOR"
        with open('./sqlite_databases_code/'+db+'/db_details.txt') as file:
            db_details_dict=json.loads(file.read())
        print('db_details_dict : \n',yellow(db_details_dict,bold=True))       
        
        text_content='''#  def_'''+db+'''_db_ingest_csv***
@app.route('/'''+db+'''_db_ingest_csv', methods=['GET'])
def '''+db+'''_db_ingest_csv():
    \'\'\'
    '''+description+'''
    \'\'\'
    route="/'''+db+'''_db_ingest_csv"
    env.level+=\'-\'
    print(\'\\n\'+env.level,white(\'route '''+db+'''_db_ingest_csv() in ***app.py*** : >\\n\',bold=True))
    loguer(env.level+\' route '''+db+'''_db_ingest_csv() in ***app.py*** : >\')
    if not session.get(\'logged_in\'):
        return render_template(\'login.html\')
    else:
        db_name="'''+db+'''"
        message1="Message 1 :"
        image="../static/images/toolbox.png"
        message2="Message 2 :"
        message3="/Message 3"
        message4="Message 4 in button"
        PAGE_DESTINATION="z_sqlite_ingest_csv"
        page_name="z_sqlite_ingest_csv.html"
        loguer(env.level+\' route END OF '''+db+'''_db_ingest_csv() in ***app.py*** : >\')
        # ===================================================================
        env.level=env.level[:-1]
        return render_template(\'main_index.html\',route=route,USERNAME=session[\'user\'],PAGE_DESTINATION=PAGE_DESTINATION,message1=message1,message2=message2,message3=message3,message4=message4,image=image,page_name=page_name,db_name=db_name) 
'''        
        filename='./code_app_routes/route_def_'+db+'_db_ingest_csv.py'
        with open(filename,"w") as fichier:
            fichier.write(text_content)     
        with open('./code_architecture/app_routes.txt',"a+") as fichier:
            filename2=filename2.replace('/','')
            fichier.write(filename2+'\n')  
        result=1
    # ===================================================================
    loguer(env.level+' def END OF create_rte_for_db_ingest_cvs() in app.py : >')    
    env.level=env.level[:-1]
    return result
    


#  def_sqlite_db_duplicate_entry***
def sqlite_db_duplicate_entry(db_name,row):
    '''
    MODIFIED : 2025-10-29

    description : duplicate selected row from the sqllite Database
    
    how to call it : result = sqlite_db_duplicate_entry(db_name,row)
    '''
    route="/sqlite_db_duplicate_entry"
    env.level+='-'
    print('\n'+env.level,white('def sqlite_db_duplicate_entry() in app.py : >\n',bold=True))
    loguer(env.level+' def sqlite_db_duplicate_entry() in app.py : >')
    # ===================================================================    
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        db_name=request.args.get("db_name")
        print('db_name :',db_name)     
        row=request.args.get("row")
        print('db_name :',row)              
        with open('./sqlite_databases_code/'+db_name+'/db_details.txt') as file:
            db_details_dict=json.loads(file.read())
        print('db_details_dict : \n',yellow(db_details_dict,bold=True)) 
        column_list=db_details_dict['columns']
        database = os.getcwd()+'/z_bases/'+db_name+'.db'
        database=database.replace("\\","/")
        table=db_details_dict['table_name']
        print('database is :',database) 
        print('table is :',table)          
        # read entry in data base
        where_clause='where `index` = '+row
        entry_list=sqlite_db_select_entry(db_name,table,where_clause)
        print("\nentry_list : \n",entry_list)
        items={}
        i=0
        for obj in entry_list[0]:
            if i<len(column_list):
                items[i]={'name':column_list[i],'value':entry_list[0][i+1]}
            i+=1
        print('items : ',cyan(items,bold=True))        
        # Get last index value in SQLITE DB
        new_index=sqlite_db_get_last_index(db_name)+1        
        print('new_index is :',str(new_index)+'\n')         
        sqlite_data=[new_index]      
        i=0
        for obj in items.items():
            print('obj :',cyan(obj,bold=True))
            sqlite_data.append(obj[1]['value'])  
        sql_add=f"INSERT OR IGNORE into {table} (`index`,"
        i=0
        for obj in items.items():
            print('obj :',cyan(obj,bold=True))
            if i<len(column_list)-1:
                sql_add=sql_add+obj[1]['name']+','
            else:
                sql_add=sql_add+obj[1]['name']+') VALUES (?,'
            i+=1       
        i=0
        for obj in items:
            if i<len(column_list)-1:
                sql_add=sql_add+'?,'
            else:
                sql_add=sql_add+'?)'
            i+=1             
        print('sqlite_data :',sqlite_data)     
        print('sql_add :',sql_add)    
        con = sqlite3.connect(database)       
        try:
            cur = con.cursor()
            cur.execute(sql_add,sqlite_data)
            con.commit()
            print(green('OK DONE ENTRY DUPLICATED',bold=True))
            image="../static/images/ok.png" 
            message1="Entry Duplicated"
            message2="Entry was duplicated"
            message3=f"/{db_name}_dashboard"
            message4=f"{db_name}_dasbhoard"        
            PAGE_DESTINATION="operation_done"
            page_name="operation_done.html"            
            env.level=env.level[:-1]        
            return render_template('main_index.html',route=route,USERNAME=session['user'],PAGE_DESTINATION=PAGE_DESTINATION,message1=message1,message2=message2,message3=message3,message4=message4,image=image,page_name=page_name) 
        except:
            print(red('Error',bold=True))
            image="../static/images/nok.png" 
            message1="Error"
            message2="An error occured"
            message3=f"/{db_name}_dashboard"
            message4=f"{db_name}_dasbhoard"        
            PAGE_DESTINATION="operation_done"
            page_name="operation_done.html"            
            env.level=env.level[:-1]        
            return render_template('main_index.html',route=route,USERNAME=session['user'],PAGE_DESTINATION=PAGE_DESTINATION,message1=message1,message2=message2,message3=message3,message4=message4,image=image,page_name=page_name)




#  def_create_rte_for_sqlite_db_duplicate_entry_function***
def create_rte_for_sqlite_db_duplicate_entry_function(name):
    '''
    MODIFIED : 2025-10-02

    description : create route for db delete entry
    
    how to call it : create_rte_for_sqlite_db_duplicate_entry_function(name)
        name = db name
    '''
    route="/create_rte_for_sqlite_db_duplicate_entry_function"
    env.level+='-'
    print('\n'+env.level,white('def create_rte_for_sqlite_db_duplicate_entry_function() in app.py : >\n',bold=True))
    loguer(env.level+' def create_rte_for_sqlite_db_duplicate_entry_function() in app.py : >')
    # ===================================================================    
    db=name
    db_name=name.replace('./zbases/','')
    db_name=db_name.replace('.db','')
    name=name+'_db_duplicate_entry'
    filename='./code_app_routes/route_def_'+name+'.py'
    filename2='/route_def_'+name+'.py'
    description='Flask Route for the '+name+' Database delete entry'
    print()
    print(' filename :\n',yellow(filename,bold=True))
    print()
    print(' filename2 :\n',yellow(filename2,bold=True))
    print()
    print(magenta('--> CALL  A SUB FUNCTION :',bold=True))
    # check if file already exits
    with open('./code_architecture/app_routes.txt') as file:
        text_content2=file.read()    
    fichier_route = Path('./code_app_routes/route_def_'+name+'.py')    
    if fichier_route.is_file() or filename in text_content2:
        print(filename+' already exists ! Choose another name')
        message1="ALREADY EXIST"
        image="../static/images/nok.png" 
        message2="Choose another name"
        message3="/home"
        message4="Back Home"          
        PAGE_DESTINATION="operation_done"
        page_name="z_operation_done.html"
        loguer(env.level+' route END OF example_name() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]
        return 0
    else:
        print(yellow(f'     {filename} does NOT exists. Let s create it',bold=True))
        route="/"+db+"_db_duplicate_entry"
        title="FLASK APP GENERATOR"
        with open('./sqlite_databases_code/'+db+'/db_details.txt') as file:
            db_details_dict=json.loads(file.read())
        print('db_details_dict : \n',yellow(db_details_dict,bold=True))       
        
        text_content='''#  def_'''+db+'''_db_duplicate_entry***
@app.route('/'''+db+'''_db_duplicate_entry', methods=['GET'])
def '''+db+'''_db_duplicate_entry():
    \'\'\'
    '''+description+'''
    \'\'\'
    route="/'''+db+'''_db_duplicate_entry"
    env.level+=\'-\'
    print(\'\\n\'+env.level,white(\'route '''+db+'''_db_duplicate_entry() in ***app.py*** : >\\n\',bold=True))
    loguer(env.level+\' route '''+db+'''_db_duplicate_entry() in ***app.py*** : >\')
    if not session.get(\'logged_in\'):
        return render_template(\'login.html\')
    else:
        row=request.args.get("row")
        print("\\nrow : ",row)
        result=sqlite_db_duplicate_entry(\''''+db+'''\',row)         
        message1="OK done - Entry DUPLICATED"
        image="../static/images/ok.png" 
        message2="entry had been duplicated"
        message3="/'''+db+'''_dashboard"
        message4="'''+db+''' Dashboard"
        PAGE_DESTINATION="operation_done"
        page_name="operation_done.html"
        loguer(env.level+\' route END OF example_name() in ***app.py*** : >\')
        # ===================================================================
        env.level=env.level[:-1]
        return render_template(\'main_index.html\',route=route,USERNAME=session[\'user\'],PAGE_DESTINATION=PAGE_DESTINATION,message1=message1,message2=message2,message3=message3,message4=message4,image=image,page_name=page_name)
 
'''        
        filename='./code_app_routes/route_def_'+db+'_db_duplicate_entry.py'
        with open(filename,"w") as fichier:
            fichier.write(text_content)     
        with open('./code_architecture/app_routes.txt',"a+") as fichier:
            filename2=filename2.replace('/','')
            fichier.write(filename2+'\n')  
        result=1
    
    # ===================================================================
    loguer(env.level+' def END OF create_rte_for_sqlite_db_duplicate_entry_function() in app.py : >')    
    env.level=env.level[:-1]
    return result
    



# here under FUNCTIONS ===========================   
 
# def_parse_config***
def parse_config(text_content):
    env.level+='-'
    print()
    print(env.level,white('def parse_config() in app.py : >',bold=True))
    loguer(env.level+' def parse_config()  in app.py : >')
    print()
    text_lines=text_content.split('\n')
    conf_result=['','','','','']
    for line in text_lines:
        print(green(line,bold=True))
        if 'api_key' in line:
            words=line.split('=')
            if len(words)==2:
                conf_result[0]=line.split('=')[1]
                conf_result[0]=conf_result[0].replace('"','')
                conf_result[0]=conf_result[0].replace("'","")
                conf_result[0]=conf_result[0].strip()
            else:
                conf_result[0]=""
        elif 'network_id' in line:
            words=line.split('=')
            if len(words)==2:
                conf_result[1]=line.split('=')[1]
                conf_result[1]=conf_result[1].replace('"','')
                conf_result[1]=conf_result[1].replace("'","")
                conf_result[1]=conf_result[1].strip()
            else:
                conf_result[1]=""
        elif 'host' in line:
            words=line.split('=')
            if len(words)==2:
                conf_result[2]=line.split('=')[1]
                conf_result[2]=conf_result[2].replace('"','')
                conf_result[2]=conf_result[2].replace("'","")
                conf_result[2]=conf_result[2].strip()
            else:
                conf_result[2]=""
        elif 'orgID' in line:
            words=line.split('=')
            if len(words)==2:
                conf_result[3]=line.split('=')[1]
                conf_result[3]=conf_result[3].replace('"','')
                conf_result[3]=conf_result[3].replace("'","")
                conf_result[3]=conf_result[3].strip()
            else:
                conf_result[3]=""
        elif 'profil_name' in line:
            words=line.split('=')
            if len(words)==2:
                conf_result[4]=line.split('=')[1]
                conf_result[4]=conf_result[4].replace('"','')
                conf_result[4]=conf_result[4].replace("'","")
                conf_result[4]=conf_result[4].strip()
            else:
                conf_result[4]=""
    print(yellow(conf_result))
    env.level=env.level[:-1]
    return conf_result




#  def_replace_variables***
def replace_variables(chaine,config_dict):
    '''
    MODIFIED : 2025-07-18T14:43:59.000Z

    description : replace a variable string which start whith $ by the corresponding config variable which has the same name
    '''
    route="/replace_variables(chaine,config_dict)"
    env.level+='-'
    print()
    print(env.level,white('def replace_variables() in app.py  : >\n',bold=True))
    loguer(env.level+' def replace_variables() in app.py  : > ')
    print()
    global api_key
    global orgID
    global host
    global network_id
    global profil_name
    # ===================================================================    

    for k,v in config_dict.items():
          if v:
              chaine=chaine.replace('$'+k,v)
    print()
    print('chaine :',yellow(chaine,bold=True))
    print()   
    # ===================================================================
    env.level=env.level[:-1]
    return chaine
    



#  def_send_api_call_function***
def send_api_call_function(method,base_url,relative_url,additionnal_get_params,headers,payload,body,params,parameters,api_key):
    '''
    MODIFIED : 2025-11-06
    description : send_the_api call to the destination REST service
    
    how to call it : result,json_txt_result=send_api_call_function(method,base_url,relative_url,additionnal_get_params,headers,payload,body,parameters,api_key)
    '''
    route="/send_api_call_function"
    env.level+='-'
    print()
    print(env.level,white('def send_api_call_function() in app.py  : >\n',bold=True))
    loguer(env.level+' def send_api_call_function() in app.py  : > ')
    print()
    #global api_key
    global orgID
    global host
    global client_id
    global client_password
    global custom1
    global custom2
    global profil_name
    # ===================================================================    
    print('base_url :',cyan(base_url,bold=True))
    print()        
    print('relative_url :',cyan(relative_url,bold=True))
    print()  
    print('method :',cyan(method,bold=True))
    print()       
    print('payload :',cyan(payload,bold=True))
    print()    
    print('headers :',cyan(headers,bold=True))
    print()      
    print('body :',cyan(body,bold=True))
    print()
    print('params :',cyan(params,bold=True))    
    print()
    print('parameters :',cyan(parameters,bold=True))
    print('\napi_key :',cyan(api_key,bold=True))          
    config_dict={}
    if api_key !='' and api_key !='no_key':    
        config_dict['api_key']=api_key  
    config_dict['host']=host 
    '''
    if client_id !='':    
        config_dict['client_id']=client_id 
    if client_password !='':    
        config_dict['client_password']=client_password        
    '''        
    if parameters !='':
        parameter_list=parameters.split("***")    
        for param in parameter_list:
            params=param.split('=')
            config_dict[params[0]]=params[1]
    print('config_dict :\n',yellow(config_dict,bold=True))
    print()      
    saved_token='xxx'
    if '$SAVED_TOKEN' in relative_url:
        relative_url=relative_url.replace('$SAVED_TOKEN',saved_token)      
    if '$SAVED_TOKEN' in payload:
        payload=payload.replace('$SAVED_TOKEN',saved_token)      
    if '$SAVED_TOKEN' in headers:
        headers=headers.replace('$SAVED_TOKEN',saved_token)        
    if '$SAVED_TOKEN' in body:
        body=body.replace('$SAVED_TOKEN',saved_token) 
        
    if '$' in relative_url:
        relative_url=replace_variable(relative_url)
    print('relative_url :',yellow(relative_url,bold=True))
    print()
    if payload!='':
        if '$' in payload:
           payload=replace_variable(payload)  
    else:
        payload={}
    payload=json.loads(payload)         
    if headers!='':
        if '$' in headers:
            headers=replace_variable(headers) 
    else:
        headers=''    
    if body !='':
        if '$' in body:
            body=replace_variable(body)         
    else:
        body={}                  
    api_url = f"{base_url}{relative_url}{additionnal_get_params}"          
    print(magenta('--> API CALL details here under :',bold=True))
    print('api_url : ',yellow(api_url,bold=True))
    print()     
    print('method : ',yellow(method,bold=True))
    print()     
    print('payload :',yellow(payload,bold=True))
    print() 
    print('headers :',yellow(headers,bold=True))
    print()    
    print('body :',yellow(body,bold=True))
    print()     
    print('parameters :',yellow(parameters,bold=True))
    print()
    #if headers!={}:
    headers=json.loads(headers)  
    if body=="{}":
        body=json.loads(body)  
    response = requests.request(method, api_url, headers=headers, data = payload, params=params)
    print('response :',yellow(response,bold=True))
    print('response content :',yellow(response.content,bold=True))
    print()  
    if 'Route NOT FOUND' not in response.content.decode('UTF-8'):
        if response.status_code==401:
            print()
            print(red('INVALID API CREDENTIALS >',bold=True))
            print()      
            # renew the token
            #access_token=get_ctr_token(host_for_token,client_id,client_password)
            #response = requests.request(method, api_url, headers=headers, data = payload)
            result=0
            json_txt_result=''
        elif response.status_code==403:
            print()
            print(red('ACCESS FORBIDEN >',bold=True))
            print()      
            # renew the token
            result=0
            json_txt_result=response.content       
        else:
            result=1
            if '</title>' not in response.text:
                json_txt_result = json.dumps(response.json(),indent=4,sort_keys=True, separators=(',', ': '))
                print()
                print('json_txt_result  : \n',green(json_txt_result,bold=True))       
                with open('./json_results/json_result.json','w') as file:
                    file.write(json_txt_result)
                '''
                items=response.json()
                for item in items: 
                    index+=1
                    if type(item) is dict:
                        print()
                        print(item)
                        print()
                        print(cyan(item["target_ref"],bold=True))      
                '''
            else:
                json_txt_result=response.text
                print('RESULT : ',red(response_txt,bold=True))
    else:
        result=0
        json_txt_result='ERROR  !!!! '
    # ===================================================================
    env.level=env.level[:-1]
    return result,json_txt_result
    



#  def_date_time_for_file_name***
def date_time_for_file_name():
    '''
    MODIFIED : 2025-07-18T14:41:19.000Z

    description : generate date and time suffixe to be added to file names when we save file : format YYYYmmddHMS 
    '''
    route="/date_time_for_file_name"
    env.level+='-'
    print()
    print(env.level,white('def date_time_for_file_name() in app.py : >',bold=True))
    loguer(env.level+' def date_time_for_file_name() in app.py : >')
    print()
    # ===================================================================    
    current_time = datetime.utcnow()
    timestampStr = current_time.strftime("%Y%m%d_%H%M%S")  
    # ===================================================================
    env.level=env.level[:-1]
    return(timestampStr)
    

#  def_select_profile_function***
def select_profile_function(authentication_profile):
    '''
    MODIFIED : 2025-10-26T17:23:59.000Z

    description : retrieve API credentials from profile
    
    how to call it :
    '''
    route="/select_profile_function"
    env.level+='-'
    print('\n'+env.level,white('def select_profile_function() in app.py : >\n',bold=True))
    loguer(env.level+' def select_profile_function() in app.py : >')
    global client_id
    global client_password
    global host
    global host_for_token
    global profil_name
    # ===================================================================    
    database="account_keys"
    print("\ndatabase : ",database)
    table="account_keys"
    print("\ntable : ",table)
    where_clause=f'where `name` = "{authentication_profile}"'
    entry_list=sqlite_db_select_entry(database,table,where_clause)
    print("\nentry_list : \n",entry_list)    
    type=entry_list[0][2]
    if type=='basic':
        client_id=entry_list[0][3]
        client_password=entry_list[0][4]
        api_key="no_key"
    elif type=='api_key':
        client_id=""
        client_password=""   
        api_key=entry_list[0][4]   
    elif type=='token':
        client_id=""
        client_password=""   
        api_key=entry_list[0][4]           
    else:
        client_id=""
        client_password=""   
        api_key=entry_list[0][4]                
    # ===================================================================
    env.level=env.level[:-1]
    return client_id,client_password,api_key
    


#  def_variables_sqlite_update_value***
def variables_sqlite_update_value(name,value):
    '''
    MODIFIED : 2025-11-05

    description : Update the value of the selected variable name in variables DB
    
    how to call it : result = variables_sqlite_update_value(name,value)
        name : name to search an update in the rows
        value : new value
    '''
    route="/variables_sqlite_update_value"
    env.level+='-'
    print('\n'+env.level,white('def variables_sqlite_update_value() in app.py : >\n',bold=True))
    loguer(env.level+' def variables_sqlite_update_value() in app.py : >')
    global client_id
    global client_password
    global host
    global host_for_token
    global profil_name
    # ===================================================================    
    database="variables.db"
    #database = './z_bases/'+database+'.db'
    result=0
    value=value.replace("'"," ")
    print('database is :',database) 
    print(cyan(f'\n new value : {value} for variable : {name} \n',bold=True))
    #print('\n value = ',red(value,bold=True))   
    with sqlite3.connect('./z_bases/'+database) as conn:
        cursor=conn.cursor()
        sql_request = f"UPDATE 'variables' SET value = '{value}' where name = '{name}'"      
        print('sql_request :',cyan(sql_request,bold=True))
        cursor.execute(sql_request)
        result=1
    # ===================================================================
    loguer(env.level+' def END OF variables_sqlite_update_value() in app.py : >')    
    env.level=env.level[:-1]
    return result
    


#  def_parse_result_of_cse_get_computers***
def parse_result_of_cse_get_computers(api_call_result,hostname):
    '''
    MODIFIED : 2025-11-01T13:14:17.000Z

    description : Parse the result of the CSE Get Computers API call and output the GUID of the selected hostname
    
    how to call it :
    '''
    route="/parse_result_of_cse_get_computers"
    env.level+='-'
    print('\n'+env.level,white('def parse_result_of_cse_get_computers() in app.py : >\n',bold=True))
    loguer(env.level+' def parse_result_of_cse_get_computers() in app.py : >')
    # ===================================================================    
    print('\n api_call_result  : \n',cyan(api_call_result,bold=True))
    print('\nhostname  : ',cyan(hostname,bold=True))
    json_input_data=json.loads(api_call_result)
    computer_list_items = json_input_data["data"]
    print('\n computer_list_items  : ',cyan(computer_list_items,bold=True))    
    print(type(computer_list_items))
    print(len(computer_list_items))
    guid="xxxxxxxx"
    for item in computer_list_items:
        if item["hostname"]==hostname:
            print('\n',yellow(item["hostname"],bold=True))
            print(yellow(item["connector_guid"],bold=True))
            guid=item["connector_guid"]
    # ===================================================================  
    env.level=env.level[:-1]
    return guid


#  def_workflow_sqlite_update_step***
def workflow_sqlite_update_step(index,new_step):
    '''
    MODIFIED : 2025-11-01T16:03:53.000Z

    description : update step field of row in workflow database
    
    how to call it :
    '''
    route="/workflow_sqlite_update_step"
    env.level+='-'
    print('\n'+env.level,white('def workflow_sqlite_update_step() in app.py : >\n',bold=True))
    loguer(env.level+' def workflow_sqlite_update_step() in app.py : >')
    global client_id
    global client_password
    global host
    global host_for_token
    global profil_name
    # ===================================================================    
    database="workflows.db"
    #database = './z_bases/'+database+'.db'
    result=0
    print('database is :',database) 
    #print('\n value = ',red(value,bold=True))   
    with sqlite3.connect('./z_bases/'+database) as conn:
        cursor=conn.cursor()
        sql_request = f"UPDATE 'workflows' SET step = '{new_step}' where `index` = {index}"      
        print('sql_request :',cyan(sql_request,bold=True))
        cursor.execute(sql_request)
        result=1
    # ===================================================================
    loguer(env.level+' def END OF workflow_sqlite_update_step() in app.py : >')    
    env.level=env.level[:-1]
    return result
    


#  def_renumber_steps***
def renumber_steps(step):
    '''
    MODIFIED : 2025-11-01T18:18:23.000Z

    description : renumber steps from step number given as input
    
    how to call it :
    '''
    route="/renumber_steps"
    env.level+='-'
    print('\n'+env.level,white('def renumber_steps() in app.py : >\n',bold=True))
    loguer(env.level+' def renumber_steps() in app.py : >')
    if not session.get('logged_in'):
        return render_template('login.html')
    else:  
        print('step :',step,type(step))
        db_name = "workflows.db"
        column_list=['workflow_name','step','step_name','input','output','comment']
        print('\ncolumn_list :',cyan(column_list,bold=True))
        # step list
        table_name = "workflows"
        engine = sqlalchemy.create_engine("sqlite:///z_bases/%s" % db_name, execution_options={"sqlite_raw_colnames": True})
        df = pd.read_sql_table(table_name, engine)
        out_df = df[['index','workflow_name','step','step_name','input','output','comment']]
        df = DataFrame(out_df)
        #print (df)
        res = df.values.tolist()
        steps_dict={}
        step_index=0
        for item in res:
            print(item)    
            row_step_number=item[2].split(' ')[1]
            row_step_number=int(row_step_number)
            if row_step_number>=step:
                row_step_number=row_step_number+1
                if row_step_number==1:
                    new_step_number='Step 01'
                elif row_step_number==2:
                    new_step_number='Step 02'    
                elif row_step_number==3:
                    new_step_number='Step 03' 
                elif row_step_number==4:
                    new_step_number='Step 04' 
                elif row_step_number==5:
                    new_step_number='Step 05' 
                elif row_step_number==6:
                    new_step_number='Step 06' 
                elif row_step_number==7:
                    new_step_number='Step 07' 
                elif row_step_number==8:
                    new_step_number='Step 08'     
                elif row_step_number==9:
                    new_step_number='Step 09'             
                else:        
                    new_step_number='Step '+str(row_step_number)            
                steps_dict[step_index]={
                    'new_step':new_step_number,
                    'index':str(item[0])
                }    
            step_index+=1
        print('STEPS TO UPDATE : ',cyan(steps_dict,bold=True))
        for item in steps_dict.items():
            print(" item : ",item)
            #print(" item['index'] : ",item[1]['index'])
            #print("item['new_step'] : ",item[1]['new_step'])
            result=workflow_sqlite_update_step(item[1]['index'],item[1]['new_step'])            
        result=1
        # ===================================================================
        env.level=env.level[:-1]
        return result
    


#  def_renumber_steps_delete***
def renumber_steps_delete(step):
    '''
    MODIFIED : 2025-11-01T18:18:23.000Z

    description : renumber steps from step number given as input
    
    how to call it :
    '''
    route="/renumber_steps_delete"
    env.level+='-'
    print('\n'+env.level,white('def renumber_steps_delete() in app.py : >\n',bold=True))
    loguer(env.level+' def renumber_steps_delete() in app.py : >')
    if not session.get('logged_in'):
        return render_template('login.html')
    else:  
        step=step.split(' ')[1]
        step=int(step)        
        print('step :',step,type(step))        
        db_name = "workflows.db"
        column_list=['workflow_name','step','step_name','input','output','comment']
        print('\ncolumn_list :',cyan(column_list,bold=True))
        # step list
        table_name = "workflows"
        engine = sqlalchemy.create_engine("sqlite:///z_bases/%s" % db_name, execution_options={"sqlite_raw_colnames": True})
        df = pd.read_sql_table(table_name, engine)
        out_df = df[['index','workflow_name','step','step_name','input','output','comment']]
        df = DataFrame(out_df)
        #print (df)
        res = df.values.tolist()
        steps_dict={}
        step_index=0
        for item in res:
            print(item)    
            row_step_number=item[2].split(' ')[1]
            row_step_number=int(row_step_number)
            if row_step_number>step:
                if row_step_number>0:
                    row_step_number=row_step_number-1
                    if row_step_number==1:
                        new_step_number='Step 01'
                    elif row_step_number==2:
                        new_step_number='Step 02'    
                    elif row_step_number==3:
                        new_step_number='Step 03' 
                    elif row_step_number==4:
                        new_step_number='Step 04' 
                    elif row_step_number==5:
                        new_step_number='Step 05' 
                    elif row_step_number==6:
                        new_step_number='Step 06' 
                    elif row_step_number==7:
                        new_step_number='Step 07' 
                    elif row_step_number==8:
                        new_step_number='Step 08'     
                    elif row_step_number==9:
                        new_step_number='Step 09'             
                    else:        
                        new_step_number='Step '+str(row_step_number)            
                    steps_dict[step_index]={
                        'new_step':new_step_number,
                        'index':str(item[0])
                    }    
                step_index+=1
        print('STEPS TO UPDATE : ',cyan(steps_dict,bold=True))
        for item in steps_dict.items():
            print(" item : ",item)
            #print(" item['index'] : ",item[1]['index'])
            #print("item['new_step'] : ",item[1]['new_step'])
            result=workflow_sqlite_update_step(item[1]['index'],item[1]['new_step'])            
        result=1
        # ===================================================================
        env.level=env.level[:-1]
        return result
    


#  def_cse_id_of_event_type_name***
def cse_id_of_event_type_name(event_name):
    '''
    MODIFIED : 2025-11-03T09:54:03.000Z

    description : Send CSE Get event type id API call and parse ID of the event type name give as input
    
    how to call it :
    '''
    route="/cse_id_of_event_type_name"
    env.level+='-'
    print('\n'+env.level,white('def cse_id_of_event_type_name() in app.py : >\n',bold=True))
    loguer(env.level+' def cse_id_of_event_type_name() in app.py : >')
    # ===================================================================    
    api_call_name="Secure Endpoint Get Event Types"
    # GET variable from calling web page
    row=request.args.get("row")
    print("\nrow : ",row)
    database="api_calls"
    print("\ndatabase : ",database)
    table="api_calls"
    print("\ntable : ",table)
    where_clause=f' where name = "{api_call_name}"'
    entry_list=sqlite_db_select_entry(database,table,where_clause)
    print("\nentry_list : \n",entry_list)
    result,json_txt_result=select_api_call_and_send_it(api_call_name)
    result_dict=json.loads(json_txt_result)
    #print(cyan(result_dict,bold=True))
    all_events=result_dict['data']
    event_id="xxxxxx"
    for item in all_events:
        print('\n',yellow(item,bold=True))
        if item['name']==event_name:
            event_id=str(item['id'])
    print('event_id : ',green(event_id,bold=True))
    # ===================================================================
    loguer(env.level+' def END OF cse_id_of_event_type_name() in app.py : >')    
    env.level=env.level[:-1]
    return event_id
    


#  def_renumber_steps_minus_one***
def renumber_steps_minus_one(step):
    '''
    MODIFIED : 2025-11-01T18:18:23.000Z

    description : renumber steps from step number given as input
    
    how to call it :
    '''
    route="/renumber_steps_minus_one"
    env.level+='-'
    print('\n'+env.level,white('def renumber_steps_minus_one() in app.py : >\n',bold=True))
    loguer(env.level+' def renumber_steps_minus_one() in app.py : >')
    if not session.get('logged_in'):
        return render_template('login.html')
    else:      
        print('step :',step,type(step))  
        sys.exit()
        db_name = "workflows.db"
        column_list=['workflow_name','step','step_name','input','output','comment']
        print('\ncolumn_list :',cyan(column_list,bold=True))
        # step list
        table_name = "workflows"
        engine = sqlalchemy.create_engine("sqlite:///z_bases/%s" % db_name, execution_options={"sqlite_raw_colnames": True})
        df = pd.read_sql_table(table_name, engine)
        out_df = df[['index','workflow_name','step','step_name','input','output','comment']]
        df = DataFrame(out_df)
        #print (df)
        res = df.values.tolist()
        steps_dict={}
        step_index=0
        if step!=1:        
            for item in res:
                print(item)    
                row_step_number=item[2].split(' ')[1]
                row_step_number=int(row_step_number)
                if row_step_number<=step:
                    if row_step_number>0:
                        row_step_number=row_step_number-1
                    if row_step_number==1:
                        new_step_number='Step 01'
                    elif row_step_number==2:
                        new_step_number='Step 02'    
                    elif row_step_number==3:
                        new_step_number='Step 03' 
                    elif row_step_number==4:
                        new_step_number='Step 04' 
                    elif row_step_number==5:
                        new_step_number='Step 05' 
                    elif row_step_number==6:
                        new_step_number='Step 06' 
                    elif row_step_number==7:
                        new_step_number='Step 07' 
                    elif row_step_number==8:
                        new_step_number='Step 08'     
                    elif row_step_number==9:
                        new_step_number='Step 09'             
                    else:        
                        new_step_number='Step '+str(row_step_number)            
                    steps_dict[step_index]={
                        'new_step':new_step_number,
                        'index':str(item[0])
                    }
                step_index+=1
        else:
            for item in res:
                print(item)    
                row_step_number=item[2].split(' ')[1]
                row_step_number=int(row_step_number)
                if row_step_number>=step:
                    row_step_number=row_step_number+1
                    if row_step_number==1:
                        new_step_number='Step 01'
                    elif row_step_number==2:
                        new_step_number='Step 02'    
                    elif row_step_number==3:
                        new_step_number='Step 03' 
                    elif row_step_number==4:
                        new_step_number='Step 04' 
                    elif row_step_number==5:
                        new_step_number='Step 05' 
                    elif row_step_number==6:
                        new_step_number='Step 06' 
                    elif row_step_number==7:
                        new_step_number='Step 07' 
                    elif row_step_number==8:
                        new_step_number='Step 08'     
                    elif row_step_number==9:
                        new_step_number='Step 09'             
                    else:        
                        new_step_number='Step '+str(row_step_number)            
                    steps_dict[step_index]={
                        'new_step':new_step_number,
                        'index':str(item[0])
                    }       
                step_index+=1                    
        print('STEPS TO UPDATE : ',cyan(steps_dict,bold=True))
        for item in steps_dict.items():
            print(" item : ",item)
            #print(" item['index'] : ",item[1]['index'])
            #print("item['new_step'] : ",item[1]['new_step'])
            result=workflow_sqlite_update_step(item[1]['index'],item[1]['new_step'])            
        result=1
        # ===================================================================
        env.level=env.level[:-1]
        return result
    


#  def_replace_variable***
def replace_variable(objet):
    '''
    MODIFIED : 2025-11-03T22:47:34.000Z

    description : replace every variables in the object by their values
    
    how to call it :
    '''
    route="/replace_variable"
    env.level+='-'
    print('\n'+env.level,white('def replace_variable() in app.py : >\n',bold=True))
    loguer(env.level+' def replace_variable() in app.py : >')
    # ===================================================================    
    # Variables
    db_name = "variables.db"
    table_name = "variables"
    engine = sqlalchemy.create_engine("sqlite:///z_bases/%s" % db_name, execution_options={"sqlite_raw_colnames": True})
    df = pd.read_sql_table(table_name, engine)
    out_df = df[['index','name','environment_name','value','description','comment','used_by']]
    df = DataFrame(out_df)
    #print (df)
    res = df.values.tolist()
    variables_dict={}
    for item in res:
        #print(item)
        objet=objet.replace('$'+item[1],item[3])
    # ===================================================================
    loguer(env.level+' def END OF replace_variable() in app.py : >')    
    env.level=env.level[:-1]
    return objet
    


#  def_cse_check_for_events_in_host***
def cse_check_for_events_in_host(events,guid,event_id_list):
    '''
    MODIFIED : 2025-11-04T16:11:33.000Z

    description : check if events name are in the last CSE event for the selected host
    
    how to call it :
    '''
    route="/cse_check_for_events_in_host"
    env.level+='-'
    print('\n'+env.level,white('def cse_check_for_events_in_host() in app.py : >\n',bold=True))
    loguer(env.level+' def cse_check_for_events_in_host() in app.py : >')
    # ===================================================================    
    print('event_id_list : ',cyan(event_id_list,bold=True))
    print('guid : ',cyan(guid,bold=True))
    print()
    events_in_json=json.loads(events)
    #print('events_in_json : \n',yellow(events_in_json,bold=True))
    data=events_in_json['data']
    #print('data : \n',cyan(data,bold=True))
    host_events={}
    index=0
    for event in data:
        print('\nevent_type_id : \n',yellow(event["event_type_id"],bold=True))
        print('\nconnector_guid : \n',yellow(event["connector_guid"],bold=True))
        if event["connector_guid"]==guid and str(event["event_type_id"]) in event_id_list:
            print(red('OK'))
            host_events[index]=event
            index+=1
    step_output="nb_of_events_on_victim_machine"
    variables_sqlite_update_value(step_output,str(index))
    #print(cyan(host_events,bold=True))
    # ===================================================================
    loguer(env.level+' def END OF cse_check_for_events_in_host() in app.py : >')    
    env.level=env.level[:-1]
    return host_events
    


#  def_variable_value***
def variable_value(name):
    '''
    MODIFIED : 2025-11-04T17:00:20.000Z

    description : return value of the variable in the Database
    
    how to call it : value=variable_value(variable_name)
    '''
    route="/variable_value"
    env.level+='-'
    print('\n'+env.level,white('def variable_value() in app.py : >\n',bold=True))
    loguer(env.level+' def variable_value() in app.py : >')

    # ===================================================================    
    database="variables"        
    table="variables"              
    where_clause=f'where name = "{name}"'
    entry_list=sqlite_db_select_entry(database,table,where_clause)
    value=entry_list[0][3]
    # ===================================================================
    env.level=env.level[:-1]
    return value
    


#  def_get_sha256_from_cse_event***
def get_sha256_from_cse_event(events_in_host):
    '''
    MODIFIED : 2025-11-05T10:43:08.000Z

    description : Extract malicious sha256 value from last events list in computer
    
    how to call it :
    '''
    route="/get_sha256_from_cse_event"
    env.level+='-'
    print('\n'+env.level,white('def get_sha256_from_cse_event() in app.py : >\n',bold=True))
    loguer(env.level+' def get_sha256_from_cse_event() in app.py : >')
    # ===================================================================    
    event_dict=json.loads(events_in_host)
    filename=''
    sha256=''
    for event in event_dict.items():
        #print("\nevent : ",red(event,bold=True))
        filename=event[1]["file"]["file_name"]
        sha256=event[1]["file"]["identity"]["sha256"]
    print("\nfilename : ",cyan(filename,bold=True)) 
    print("\nsha256 : ",cyan(sha256,bold=True))
    # ===================================================================
    loguer(env.level+' def END OF get_sha256_from_cse_event() in app.py : >')    
    env.level=env.level[:-1]
    return sha256,filename
    


#  def_parse_result_of_ma_search_submission***
def parse_result_of_ma_search_submission(result):
    '''
    MODIFIED : 2025-11-05T13:52:27.000Z

    description : parse the result of malware analytics API call and extract sha256 of malicious file, submision id
    
    how to call it :
    '''
    route="/parse_result_of_ma_search_submission"
    env.level+='-'
    print('\n'+env.level,white('def parse_result_of_ma_search_submission() in app.py : >\n',bold=True))
    loguer(env.level+' def parse_result_of_ma_search_submission() in app.py : >')
    # ===================================================================    
    json_dict=json.loads(result)['data']['items']
    #print("\njson_dict : ",cyan(json_dict,bold=True)) 
    Malware_Analytics_sample_ID='xxxxxxxx'
    for item in json_dict:
        for item2 in item.items():
            if 'item' in item2:
                #print("\nitem2 : ",cyan(item2,bold=True))
                #print("\ntype",cyan(type(item2 ),bold=True))
                Malware_Analytics_sample_ID=str(item2[1]['sample'])
                #print("\nsample : ",red(item2[1]['sample'],bold=True))
                print('==========================================')
    print("\nMalware_Analytics_sample_ID : ",cyan(Malware_Analytics_sample_ID,bold=True)) 
    # ===================================================================
    loguer(env.level+' def END OF parse_result_of_ma_search_submission() in app.py : >')    
    env.level=env.level[:-1]
    return Malware_Analytics_sample_ID
    


#  def_parse_umbrella_result_for_token***
def parse_umbrella_result_for_token(result):
    '''
    MODIFIED : 2025-11-05T14:33:53.000Z

    description : parse the result of the Umbrella API V2 Token request and return the token
    
    how to call it :
    '''
    route="/parse_umbrella_result_for_token"
    env.level+='-'
    print('\n'+env.level,white('def parse_umbrella_result_for_token() in app.py : >\n',bold=True))
    loguer(env.level+' def parse_umbrella_result_for_token() in app.py : >')
    # ===================================================================    
    if 'access_token' in result:
        json_data=json.loads(result)
        token=json_data['access_token']
    else:
        token='ERROR ! no token in result'
    # ===================================================================
    loguer(env.level+' def END OF parse_umbrella_result_for_token() in app.py : >')    
    env.level=env.level[:-1]
    return token
    


#  def_parse_result_of_ma_get_domains***
def parse_result_of_ma_get_domains(result):
    '''
    MODIFIED : 2025-11-05T16:40:37.000Z

    description : parse the result of Malware Analytics API call and return domain name and domain IP address
    
    how to call it :
    '''
    route="/parse_result_of_ma_get_domains"
    env.level+='-'
    print('\n'+env.level,white('def parse_result_of_ma_get_domains() in app.py : >\n',bold=True))
    loguer(env.level+' def parse_result_of_ma_get_domains() in app.py : >')
    # ===================================================================    
    json_result=json.loads(result)
    for item in json_result.items():
        if 'data' in item[0]:
            #print("\nitem : ",cyan(item,bold=True))
            #print("\ntype",cyan(type(item),bold=True))   
            domain=item[1]["items"][0]["domain"]
            domain_ip=item[1]["items"][0]["data"]["answers"][0]
            print("\ndomain :",red(domain,bold=True))
            print("\ndomain_ip :",red(domain_ip,bold=True))            
    # ===================================================================
    loguer(env.level+' def END OF parse_result_of_ma_get_domains() in app.py : >')    
    env.level=env.level[:-1]
    return domain,domain_ip
    


#  def_parse_result_of_dns_activity***
def parse_result_of_dns_activity(result,domain):
    '''
    MODIFIED : 2025-11-05T17:14:38.000Z

    description : parse the result of the Umbrella get dns activity and return the list of IP addresses of host which connect to the domain
    
    how to call it :
    '''
    route="/parse_result_of_dns_activity"
    env.level+='-'
    print('\n'+env.level,white('def parse_result_of_dns_activity() in app.py : >\n',bold=True))
    loguer(env.level+' def parse_result_of_dns_activity() in app.py : >')
    # ===================================================================    
    ip_list=[]
    json_result=json.loads(result)['data']
    for item in json_result:
        #print("\nitem : ",cyan(item['domain'],bold=True))
        #print("\ntype",cyan(type(item),bold=True))   
        if item['domain']== domain:
            #print(red(item['internalip'],bold=True))
            #print('==================')
            ip_list.append(item['internalip'])
    print("\nip_list",red(ip_list,bold=True))
    # ===================================================================
    loguer(env.level+' def END OF parse_result_of_dns_activity() in app.py : >')    
    env.level=env.level[:-1]
    return ip_list
    


#  def_send_api_call_for_oauth_token***
def send_api_call_for_oauth_token(base_url,relative_url,client_id,client_password,headers,body_payload):
    '''
    MODIFIED : 2025-11-05T18:45:25.000Z

    description : Send API call for asking for a token based on Oauth2
    
    how to call it : result,response_txt=send_api_call_for_oauth_token(base_url,relative_url,client_id,client_password,headers,body_payload)
    '''
    route="/end_api_call_for_oauth_token"
    env.level+='-'
    print('\n'+env.level,white('def end_api_call_for_oauth_token() in app.py : >\n',bold=True))
    loguer(env.level+' def end_api_call_for_oauth_token() in app.py : >')
    # ===================================================================    
    print('\nbase_url :',cyan(base_url,bold=True))   
    print('\nrelative_url :',cyan(relative_url,bold=True))
    print('\nmethod :',cyan('POST',bold=True))     
    print('\nbody_payload :',cyan(body_payload,bold=True)) 
    print('\nheaders :',cyan(headers,bold=True))      
    if headers!='':
        if '$' in headers:
            headers=replace_variables(headers,config_dict) 
    else:
        headers=''    
    api_url = f"{base_url}{relative_url}"          
    print(magenta('\n--> API CALL :',bold=True))
    print('\napi_url : ',yellow(api_url,bold=True))    
    response = requests.post(api_url, headers=headers, auth=(client_id, client_password), data=body_payload)
    print('response code:',yellow(response,bold=True))
    print('response :',yellow(response.content,bold=True))
    print()     
    if response.status_code==401:
        print()
        print(red('INVALID API KEY >',bold=True))
        print()      
        # renew the token
        # access_token=get_ctr_token(host_for_token,client_id,client_password)
        # response = requests.request(method, api_url, headers=headers, data = payload)
        result=0
        json_txt_result=''
    else:
        result=1
        if '</title>' not in response.text:
            json_txt_result = json.dumps(response.json(),indent=4,sort_keys=True, separators=(',', ': '))
            print()
            print('json_txt_result  : \n',green(json_txt_result,bold=True))       
            with open('./json_results/json_result.json','w') as file:
                file.write(json_txt_result)
            '''
            items=response.json()
            for item in items: 
                index+=1
                if type(item) is dict:
                    print()
                    print(item)
                    print()
                    print(cyan(item["target_ref"],bold=True))      
            '''
        else:
            json_txt_result=response.text
    # ===================================================================
    env.level=env.level[:-1]
    return result,json_txt_result
    

#  def_parse_xdr_result_for_token***
def parse_xdr_result_for_token(result):
    '''
    MODIFIED : 2025-11-05T14:33:53.000Z

    description : parse the result of the Umbrella API V2 Token request and return the token
    
    how to call it :
    '''
    route="/parse_xdr_result_for_token"
    env.level+='-'
    print('\n'+env.level,white('def parse_xdr_result_for_token() in app.py : >\n',bold=True))
    loguer(env.level+' def parse_xdr_result_for_token() in app.py : >')
    # ===================================================================    
    if 'access_token' in result:
        json_data=json.loads(result)
        token=json_data['access_token']
    else:
        token='ERROR ! no token in result'
    # ===================================================================
    loguer(env.level+' def END OF parse_xdr_result_for_token() in app.py : >')    
    env.level=env.level[:-1]
    return token
    


#  def_set_observable_type_to_domain***
def set_observable_type_to_domain():
    '''
    MODIFIED : 2025-11-06T14:57:08.000Z

    description : set_observable_type_variable_to_domain
    
    how to call it :
    '''
    route="/set_observable_type_to_domain"
    env.level+='-'
    print('\n'+env.level,white('def set_observable_type_to_domain() in app.py : >\n',bold=True))
    loguer(env.level+' def set_observable_type_to_domain() in app.py : >')
    # ===================================================================    
    variables_sqlite_update_value('observable_type','domain')
    # ===================================================================
    env.level=env.level[:-1]
    return 1
    


#  def_update_variables_from_json_inputs***
def update_variables_from_json_inputs(inputs):
    '''
    MODIFIED : 2025-11-06T15:19:39.000Z

    description : Update Variable from a JSON Input definition
    
    how to call it :
    '''
    route="/update_variables_from_json_inputs"
    env.level+='-'
    print('\n'+env.level,white('def update_variables_from_json_inputs() in app.py : >\n',bold=True))
    loguer(env.level+' def update_variables_from_json_inputs() in app.py : >')
    # ===================================================================    
    json_dict=json.loads(inputs)
    print('json_dict : ',cyan(json_dict,bold=True))
    for item,v in json_dict.items():
        print(item)
        if '$' in v:    
            word=v.replace('$','')
            print(f'\n OK We replace this name : {word} by its value in Database\n')            
            v=replace_this_variable_by_its_value(word)
        print(v)        
        print("========================")
        variables_sqlite_update_value(item,v)
    # ===================================================================
    env.level=env.level[:-1]
    return 1
    


#  def_replace_this_variable_by_its_value***
def replace_this_variable_by_its_value(objet):
    '''
    MODIFIED : 2025-11-03T22:47:34.000Z

    description : replace every variables in the object by their values
    
    how to call it :
    '''
    route="/replace_this_variable_by_its_value"
    env.level+='-'
    print('\n'+env.level,white('def replace_this_variable_by_its_value() in app.py : >\n',bold=True))
    loguer(env.level+' def replace_this_variable_by_its_value() in app.py : >')
    # ===================================================================    
    # Variables
    db_name = "variables.db"
    table_name = "variables"
    engine = sqlalchemy.create_engine("sqlite:///z_bases/%s" % db_name, execution_options={"sqlite_raw_colnames": True})
    df = pd.read_sql_table(table_name, engine)
    out_df = df[['index','name','environment_name','value','description','comment','used_by']]
    df = DataFrame(out_df)
    #print (df)
    res = df.values.tolist()
    variables_dict={}
    for item in res:
        print(cyan(item[1],bold=True))
        if objet==item[1]:
            print(green('OK Match => '+item[3],bold=True))
            objet=item[3]
            break
    # ===================================================================
    loguer(env.level+' def END OF replace_this_variable_by_its_value() in app.py : >')    
    env.level=env.level[:-1]
    return objet
    


#  def_sqlite_db_duplicate_workflow_entry***
def sqlite_db_duplicate_workflow_entry(db_name,row):
    '''
    MODIFIED : 2025-10-29

    description : duplicate selected row from the sqllite Database
    
    how to call it : result = sqlite_db_duplicate_workflow_entry(db_name,row)
    '''
    route="/sqlite_db_duplicate_workflow_entry"
    env.level+='-'
    print('\n'+env.level,white('def sqlite_db_duplicate_workflow_entry() in app.py : >\n',bold=True))
    loguer(env.level+' def sqlite_db_duplicate_workflow_entry() in app.py : >')
    # ===================================================================    
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        db_name=request.args.get("db_name")
        print('db_name :',db_name)     
        row=request.args.get("row")
        print('db_name :',row)              
        with open('./sqlite_databases_code/'+db_name+'/db_details.txt') as file:
            db_details_dict=json.loads(file.read())
        print('db_details_dict : \n',yellow(db_details_dict,bold=True)) 
        column_list=db_details_dict['columns']
        database = os.getcwd()+'/z_bases/'+db_name+'.db'
        database=database.replace("\\","/")
        table=db_details_dict['table_name']
        print('database is :',database) 
        print('table is :',table)          
        # read entry in data base
        where_clause='where `index` = '+row
        entry_list=sqlite_db_select_entry(db_name,table,where_clause)
        print("\nentry_list : \n",entry_list)   
        # calculate new step
        where_clause=''
        full_list=sqlite_db_select_entry(db_name,table,where_clause)
        #print("\nfull_list : \n",full_list) 
        last_step=''
        for item in full_list:
            #print(item[2])
            if item[2]>last_step:
                last_step=item[2]
        print("\nLast step is : \n",last_step) 
        step_index=int(last_step.split(' ')[1])
        step_index+=1
        if step_index=='1':
            step_index='01'
        elif step_index=='2':
            step_index='02'    
        elif step_index=='3':
            step_index='03' 
        elif step_index=='4':
            step_index='04' 
        elif step_index=='5':
            step_index='05' 
        elif step_index=='6':
            step_index='06' 
        elif step_index=='7':
            step_index='07' 
        elif step_index=='8':
            step_index='08'     
        elif step_index=='9':
            step_index='09'             
        else:
            step_index=str(step_index)
                
        new_step_index='Step '+str(step_index)
        print('New step index : ',cyan(new_step_index,bold=True))
        items={}
        i=0
        for obj in entry_list[0]:
            if i<len(column_list):
                if i==1:
                    items[i]={'name':column_list[i],'value':new_step_index}
                else:
                    items[i]={'name':column_list[i],'value':entry_list[0][i+1]}
            i+=1
        print('items : ',cyan(items,bold=True))        
        # Get last index value in SQLITE DB
        new_index=sqlite_db_get_last_index(db_name)+1        
        print('new_index is :',str(new_index)+'\n')         
        sqlite_data=[new_index]      
        i=0
        for obj in items.items():
            print('obj :',cyan(obj,bold=True))
            sqlite_data.append(obj[1]['value'])  
        sql_add=f"INSERT OR IGNORE into {table} (`index`,"
        i=0
        for obj in items.items():
            print('obj :',cyan(obj,bold=True))
            if i<len(column_list)-1:
                sql_add=sql_add+obj[1]['name']+','
            else:
                sql_add=sql_add+obj[1]['name']+') VALUES (?,'
            i+=1       
        i=0
        for obj in items:
            if i<len(column_list)-1:
                sql_add=sql_add+'?,'
            else:
                sql_add=sql_add+'?)'
            i+=1             
        print('sqlite_data :',sqlite_data)     
        print('sql_add :',sql_add)    
        con = sqlite3.connect(database)       
        try:
            cur = con.cursor()
            cur.execute(sql_add,sqlite_data)
            con.commit()
            print(green('OK DONE ENTRY DUPLICATED',bold=True))
            image="../static/images/ok.png" 
            message1="Entry Duplicated"
            message2="Entry was duplicated"
            message3=f"/{db_name}_dashboard"
            message4=f"{db_name}_dasbhoard"        
            PAGE_DESTINATION="operation_done"
            page_name="operation_done.html"            
            env.level=env.level[:-1]        
            return render_template('main_index.html',route=route,USERNAME=session['user'],PAGE_DESTINATION=PAGE_DESTINATION,message1=message1,message2=message2,message3=message3,message4=message4,image=image,page_name=page_name) 
        except:
            print(red('Error',bold=True))
            image="../static/images/nok.png" 
            message1="Error"
            message2="An error occured"
            message3=f"/{db_name}_dashboard"
            message4=f"{db_name}_dasbhoard"        
            PAGE_DESTINATION="operation_done"
            page_name="operation_done.html"            
            env.level=env.level[:-1]        
            return render_template('main_index.html',route=route,USERNAME=session['user'],PAGE_DESTINATION=PAGE_DESTINATION,message1=message1,message2=message2,message3=message3,message4=message4,image=image,page_name=page_name)




#  def_reset_every_databases***
def reset_every_databases():
    '''
    MODIFIED : 2025-11-11T08:06:18.000Z

    description : reset every databases
    
    how to call it : result = reset_every_databases()
    '''
    route="/reset_every_databases"
    env.level+='-'
    print('\n'+env.level,white('def reset_every_databases() in app.py : >\n',bold=True))
    loguer(env.level+' def reset_every_databases() in app.py : >')
    # ===================================================================    
    action_type = 'replace'
    # WORKFLOWS
    print(red('RESET VARIABLES',bold=True))
    with open('./sqlite_databases_code/workflows/db_details.txt') as file:
        db_details_dict=json.loads(file.read())
    print('db_details_dict : \n',yellow(db_details_dict,bold=True))
    database = os.getcwd()+'/z_bases/workflows.db'
    database=database.replace("\\","/")
    print('database is :',database)
    print('table is :', db_details_dict["table_name"])
    conn=create_connection(database) # open connection to database
    if conn:
        # connection to database is OK
        c=conn.cursor()
        print(f'- Deleting table : {db_details_dict["table_name"]} =>')
        sql_request="drop table "+db_details_dict["table_name"]
        c.execute(sql_request)
        conn.commit()
        print('-- OK DONE : Deleted table : '+db_details_dict["table_name"])
        create_db_and_table(db_details_dict["db_name"],db_details_dict["table_name"])
        print(f'-- OK table {db_details_dict["table_name"]} reseted')     
    db_name='workflows'
    with open('./sqlite_databases_code/'+db_name+'/db_details.txt') as file:
        db_details_dict=json.loads(file.read())
    print('db_details_dict : \n',yellow(db_details_dict,bold=True))
    database = os.getcwd()+'/z_bases/'+db_name+'.db'
    database=database.replace("\\","/")
    print('database is :',database)
    print('table is :',db_details_dict['table_name'])
    lines=[]
    file='./DB_backups/workflows_init_20251109.csv'
    with open (file) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        lines = list(reader)
        if action_type=="replace":
            conn=create_connection(database) # open connection to database
            if conn:
                # connection to database is OK
                c=conn.cursor()
                print(f'- Deleting table : {db_details_dict["table_name"]} =>')
                sql_request="drop table "+db_details_dict["table_name"]
                c.execute(sql_request)
                conn.commit()
                print('-- OK DONE : Deleted table : '+db_details_dict["table_name"])
                create_db_and_table(db_details_dict["db_name"],db_details_dict["table_name"])
                print(f'-- OK table {db_details_dict["table_name"]} reseted')                  
            indexA=0
        else:
            indexA=sqlite_db_get_last_index(db_name)+1
        conn=create_connection(database) # open connection to database
        for row in lines:
            if conn:
                # connection to database is OK
                c=conn.cursor()
                # let's go to every lines one by one and let's extract url, targeted brand
                len_columns=len(db_details_dict['columns'])-1
                sqlite_data=[indexA]
                for cel in row:
                    sqlite_data.append(cel)
                print('\nsqlite_data :',cyan(sqlite_data,bold=True))
                sql_add=f"INSERT OR IGNORE into {db_details_dict['table_name']} (`index`,"
                i=0
                for col in db_details_dict['columns']:
                    print(col)
                    if i<len_columns:
                        sql_add=sql_add+col+","
                    else:
                        sql_add=sql_add+col+")"
                    i+=1
                sql_add=sql_add+' VALUES (?,'
                i=0
                for col in db_details_dict['columns']:
                    print(col)
                    if i<len_columns:
                        sql_add=sql_add+"?,"
                    else:
                        sql_add=sql_add+'?)'
                    i+=1
                #sql_add="INSERT OR IGNORE into truc (`index`,premier,deuxieme,troisieme,quatrieme) VALUES (?,?,?,?,?)"
                print('\nsql_add :',cyan(sql_add,bold=True))
            c.execute(sql_add, sqlite_data)
            print(green("==> OK Done : demo data ingested",bold=True))
            indexA+=1
            conn.commit()

    #VARIABLES
    print(red('RESET VARIABLES',bold=True))
    with open('./sqlite_databases_code/variables/db_details.txt') as file:
        db_details_dict=json.loads(file.read())
    print('db_details_dict : \n',yellow(db_details_dict,bold=True))
    file=open('./sqlite_databases_code/variables/init/variables.csv','w')
    ligne_out=''
    len_columns=len(db_details_dict['columns'])-1
    i=0        
    for col in db_details_dict['columns']:
        if i<len_columns:
            ligne_out=ligne_out+col+','
        else:
            ligne_out=ligne_out+col
        i+=1
    file.write(ligne_out+'\n')
    for i in range (0,10):
        ligne_out='name'+str(i)+','+'environment_name'+str(i)+','+'value'+str(i)+','+'description'+str(i)+','+'comment'+str(i)+','+'used_by'+str(i)           
        file.write(ligne_out+'\n')
    file.close()  
    create_db_and_table(db_details_dict['db_name'],db_details_dict['table_name'])
    
    db_name = "variables"
    print("\ndb_name : ",db_name)
    print("\naction_type : ",action_type)        

    result=1
    if result==1:
        with open('./sqlite_databases_code/variables/db_details.txt') as file:
            db_details_dict=json.loads(file.read())
        print('db_details_dict : \n',yellow(db_details_dict,bold=True))
        database = os.getcwd()+'/z_bases/'+db_name+'.db'
        database=database.replace("\\","/")
        print('database is :',database)
        print('table is :',db_details_dict['table_name'])
        lines=[]
        file='./DB_backups/variables_ok_20251109.csv'
        with open (file) as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            lines = list(reader)
            if action_type=="replace":
                conn=create_connection(database) # open connection to database
                if conn:
                    # connection to database is OK
                    c=conn.cursor()
                    print(f'- Deleting table : {db_details_dict["table_name"]} =>')
                    sql_request="drop table "+db_details_dict["table_name"]
                    c.execute(sql_request)
                    conn.commit()
                    print('-- OK DONE : Deleted table : '+db_details_dict["table_name"])
                    create_db_and_table(db_details_dict["db_name"],db_details_dict["table_name"])
                    print(f'-- OK table {db_details_dict["table_name"]} reseted')                  
                indexA=0
            else:
                indexA=sqlite_db_get_last_index(db_name)+1
            conn=create_connection(database) # open connection to database
            for row in lines:
                if conn:
                    # connection to database is OK
                    c=conn.cursor()
                    # let's go to every lines one by one and let's extract url, targeted brand
                    len_columns=len(db_details_dict['columns'])-1
                    sqlite_data=[indexA]
                    for cel in row:
                        sqlite_data.append(cel)
                    print('\nsqlite_data :',cyan(sqlite_data,bold=True))
                    sql_add=f"INSERT OR IGNORE into {db_details_dict['table_name']} (`index`,"
                    i=0
                    for col in db_details_dict['columns']:
                        print(col)
                        if i<len_columns:
                            sql_add=sql_add+col+","
                        else:
                            sql_add=sql_add+col+")"
                        i+=1
                    sql_add=sql_add+' VALUES (?,'
                    i=0
                    for col in db_details_dict['columns']:
                        print(col)
                        if i<len_columns:
                            sql_add=sql_add+"?,"
                        else:
                            sql_add=sql_add+'?)'
                        i+=1
                    #sql_add="INSERT OR IGNORE into truc (`index`,premier,deuxieme,troisieme,quatrieme) VALUES (?,?,?,?,?)"
                    print('\nsql_add :',cyan(sql_add,bold=True))
                c.execute(sql_add, sqlite_data)
                print(green("==> OK Done : demo data ingested",bold=True))
                indexA+=1
                conn.commit()  
    # FUNCTIONS
    with open('./sqlite_databases_code/functions/db_details.txt') as file:
        db_details_dict=json.loads(file.read())
    print('db_details_dict : \n',yellow(db_details_dict,bold=True))
    file=open('./sqlite_databases_code/functions/init/functions.csv','w')
    ligne_out=''
    len_columns=len(db_details_dict['columns'])-1
    i=0        
    for col in db_details_dict['columns']:
        if i<len_columns:
            ligne_out=ligne_out+col+','
        else:
            ligne_out=ligne_out+col
        i+=1
    file.write(ligne_out+'\n')
    for i in range (0,10):
        ligne_out='name'+str(i)+','+'environment_name'+str(i)+','+'description'+str(i)+','+'called_function'+str(i)+','+'input_variables'+str(i)+','+'output_variables'+str(i)+','+'comment'+str(i)           
        file.write(ligne_out+'\n')
    file.close()  
    create_db_and_table(db_details_dict['db_name'],db_details_dict['table_name'])
    
    db_name = "functions"
    print("\ndb_name : ",db_name)
    print("\naction_type : ",action_type)        

    result=1
    if result==1:
        with open('./sqlite_databases_code/functions/db_details.txt') as file:
            db_details_dict=json.loads(file.read())
        print('db_details_dict : \n',yellow(db_details_dict,bold=True))
        database = os.getcwd()+'/z_bases/'+db_name+'.db'
        database=database.replace("\\","/")
        print('database is :',database)
        print('table is :',db_details_dict['table_name'])
        lines=[]
        file='./DB_backups/functions_ok_20251109.csv'
        with open (file) as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            lines = list(reader)
            if action_type=="replace":
                conn=create_connection(database) # open connection to database
                if conn:
                    # connection to database is OK
                    c=conn.cursor()
                    print(f'- Deleting table : {db_details_dict["table_name"]} =>')
                    sql_request="drop table "+db_details_dict["table_name"]
                    c.execute(sql_request)
                    conn.commit()
                    print('-- OK DONE : Deleted table : '+db_details_dict["table_name"])
                    create_db_and_table(db_details_dict["db_name"],db_details_dict["table_name"])
                    print(f'-- OK table {db_details_dict["table_name"]} reseted')                  
                indexA=0
            else:
                indexA=sqlite_db_get_last_index(db_name)+1
            conn=create_connection(database) # open connection to database
            for row in lines:
                if conn:
                    # connection to database is OK
                    c=conn.cursor()
                    # let's go to every lines one by one and let's extract url, targeted brand
                    len_columns=len(db_details_dict['columns'])-1
                    sqlite_data=[indexA]
                    for cel in row:
                        sqlite_data.append(cel)
                    print('\nsqlite_data :',cyan(sqlite_data,bold=True))
                    sql_add=f"INSERT OR IGNORE into {db_details_dict['table_name']} (`index`,"
                    i=0
                    for col in db_details_dict['columns']:
                        print(col)
                        if i<len_columns:
                            sql_add=sql_add+col+","
                        else:
                            sql_add=sql_add+col+")"
                        i+=1
                    sql_add=sql_add+' VALUES (?,'
                    i=0
                    for col in db_details_dict['columns']:
                        print(col)
                        if i<len_columns:
                            sql_add=sql_add+"?,"
                        else:
                            sql_add=sql_add+'?)'
                        i+=1
                    #sql_add="INSERT OR IGNORE into truc (`index`,premier,deuxieme,troisieme,quatrieme) VALUES (?,?,?,?,?)"
                    print('\nsql_add :',cyan(sql_add,bold=True))
                c.execute(sql_add, sqlite_data)
                print(green("==> OK Done : demo data ingested",bold=True))
                indexA+=1
                conn.commit()  
    # ACCOUNT KEYS
    with open('./sqlite_databases_code/account_keys/db_details.txt') as file:
        db_details_dict=json.loads(file.read())
    print('db_details_dict : \n',yellow(db_details_dict,bold=True))
    file=open('./sqlite_databases_code/account_keys/init/account_keys.csv','w')
    ligne_out=''
    len_columns=len(db_details_dict['columns'])-1
    i=0        
    for col in db_details_dict['columns']:
        if i<len_columns:
            ligne_out=ligne_out+col+','
        else:
            ligne_out=ligne_out+col
        i+=1
    file.write(ligne_out+'\n')
    for i in range (0,10):
        ligne_out='name'+str(i)+','+'type'+str(i)+','+'username'+str(i)+','+'password'+str(i)+','+'key'+str(i)+','+'comment'+str(i)           
        file.write(ligne_out+'\n')
    file.close()  
    create_db_and_table(db_details_dict['db_name'],db_details_dict['table_name'])
    
    db_name = "account_keys"
    print("\ndb_name : ",db_name)
    print("\naction_type : ",action_type)        
    result=1
    if result==1:
        with open('./sqlite_databases_code/account_keys/db_details.txt') as file:
            db_details_dict=json.loads(file.read())
        print('db_details_dict : \n',yellow(db_details_dict,bold=True))
        database = os.getcwd()+'/z_bases/'+db_name+'.db'
        database=database.replace("\\","/")
        print('database is :',database)
        print('table is :',db_details_dict['table_name'])
        lines=[]
        file='./DB_backups/account_keys_ok_20251109.csv'
        with open (file) as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            lines = list(reader)
            if action_type=="replace":
                conn=create_connection(database) # open connection to database
                if conn:
                    # connection to database is OK
                    c=conn.cursor()
                    print(f'- Deleting table : {db_details_dict["table_name"]} =>')
                    sql_request="drop table "+db_details_dict["table_name"]
                    c.execute(sql_request)
                    conn.commit()
                    print('-- OK DONE : Deleted table : '+db_details_dict["table_name"])
                    create_db_and_table(db_details_dict["db_name"],db_details_dict["table_name"])
                    print(f'-- OK table {db_details_dict["table_name"]} reseted')                  
                indexA=0
            else:
                indexA=sqlite_db_get_last_index(db_name)+1
            conn=create_connection(database) # open connection to database
            for row in lines:
                if conn:
                    # connection to database is OK
                    c=conn.cursor()
                    # let's go to every lines one by one and let's extract url, targeted brand
                    len_columns=len(db_details_dict['columns'])-1
                    sqlite_data=[indexA]
                    for cel in row:
                        sqlite_data.append(cel)
                    print('\nsqlite_data :',cyan(sqlite_data,bold=True))
                    sql_add=f"INSERT OR IGNORE into {db_details_dict['table_name']} (`index`,"
                    i=0
                    for col in db_details_dict['columns']:
                        print(col)
                        if i<len_columns:
                            sql_add=sql_add+col+","
                        else:
                            sql_add=sql_add+col+")"
                        i+=1
                    sql_add=sql_add+' VALUES (?,'
                    i=0
                    for col in db_details_dict['columns']:
                        print(col)
                        if i<len_columns:
                            sql_add=sql_add+"?,"
                        else:
                            sql_add=sql_add+'?)'
                        i+=1
                    #sql_add="INSERT OR IGNORE into truc (`index`,premier,deuxieme,troisieme,quatrieme) VALUES (?,?,?,?,?)"
                    print('\nsql_add :',cyan(sql_add,bold=True))
                c.execute(sql_add, sqlite_data)
                print(green("==> OK Done : demo data ingested",bold=True))
                indexA+=1
                conn.commit()
    # API_CALLS
    with open('./sqlite_databases_code/api_calls/db_details.txt') as file:
        db_details_dict=json.loads(file.read())
    print('db_details_dict : \n',yellow(db_details_dict,bold=True))
    file=open('./sqlite_databases_code/api_calls/init/api_calls.csv','w')
    ligne_out=''
    len_columns=len(db_details_dict['columns'])-1
    i=0        
    for col in db_details_dict['columns']:
        if i<len_columns:
            ligne_out=ligne_out+col+','
        else:
            ligne_out=ligne_out+col
        i+=1
    file.write(ligne_out+'\n')
    for i in range (0,10):
        ligne_out='name'+str(i)+','+'fqdn'+str(i)+','+'relative_url'+str(i)+','+'documentation'+str(i)+','+'method'+str(i)+','+'description'+str(i)+','+'payload'+str(i)+','+'header'+str(i)+','+'body'+str(i)+','+'query_params'+str(i)+','+'custom_variables'+str(i)+','+'authentication_profile'+str(i)+','+'inputs_variables'+str(i)+','+'output_variables'+str(i)           
        file.write(ligne_out+'\n')
    file.close()  
    create_db_and_table(db_details_dict['db_name'],db_details_dict['table_name'])
    
    db_name = "api_calls"
    print("\ndb_name : ",db_name)
    print("\naction_type : ",action_type)        

    result=1
    if result==1:
        with open('./sqlite_databases_code/'+db_name+'/db_details.txt') as file:
            db_details_dict=json.loads(file.read())
        print('db_details_dict : \n',yellow(db_details_dict,bold=True))
        database = os.getcwd()+'/z_bases/'+db_name+'.db'
        database=database.replace("\\","/")
        print('database is :',database)
        print('table is :',db_details_dict['table_name'])
        lines=[]
        file='./DB_backups/api_calls_ok_20251109.csv'
        with open (file) as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            lines = list(reader)
            if action_type=="replace":
                conn=create_connection(database) # open connection to database
                if conn:
                    # connection to database is OK
                    c=conn.cursor()
                    print(f'- Deleting table : {db_details_dict["table_name"]} =>')
                    sql_request="drop table "+db_details_dict["table_name"]
                    c.execute(sql_request)
                    conn.commit()
                    print('-- OK DONE : Deleted table : '+db_details_dict["table_name"])
                    create_db_and_table(db_details_dict["db_name"],db_details_dict["table_name"])
                    print(f'-- OK table {db_details_dict["table_name"]} reseted')                  
                indexA=0
            else:
                indexA=sqlite_db_get_last_index(db_name)+1
            conn=create_connection(database) # open connection to database
            for row in lines:
                if conn:
                    # connection to database is OK
                    c=conn.cursor()
                    # let's go to every lines one by one and let's extract url, targeted brand
                    len_columns=len(db_details_dict['columns'])-1
                    sqlite_data=[indexA]
                    for cel in row:
                        sqlite_data.append(cel)
                    print('\nsqlite_data :',cyan(sqlite_data,bold=True))
                    sql_add=f"INSERT OR IGNORE into {db_details_dict['table_name']} (`index`,"
                    i=0
                    for col in db_details_dict['columns']:
                        print(col)
                        if i<len_columns:
                            sql_add=sql_add+col+","
                        else:
                            sql_add=sql_add+col+")"
                        i+=1
                    sql_add=sql_add+' VALUES (?,'
                    i=0
                    for col in db_details_dict['columns']:
                        print(col)
                        if i<len_columns:
                            sql_add=sql_add+"?,"
                        else:
                            sql_add=sql_add+'?)'
                        i+=1
                    #sql_add="INSERT OR IGNORE into truc (`index`,premier,deuxieme,troisieme,quatrieme) VALUES (?,?,?,?,?)"
                    print('\nsql_add :',cyan(sql_add,bold=True))
                c.execute(sql_add, sqlite_data)
                print(green("==> OK Done : demo data ingested",bold=True))
                indexA+=1
                conn.commit()    
    
    result=1
    # ===================================================================
    loguer(env.level+' def END OF reset_every_databases() in app.py : >')    
    env.level=env.level[:-1]
    return result
    



# here under the flask routes part ===========================    

app = Flask(__name__)

# def_do_admin_login***
@app.route('/login', methods=['POST'])
def do_admin_login(): 
    env.level+='-'
    print()
    print(env.level,white('route do_admin_login() : >',bold=True))
    loguer(env.level+' route do_admin_login() : >')
    print()
    route="/login"
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])
 
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]) )
    result = query.first()
    if result:
        session['logged_in'] = True
        session['user'] = POST_USERNAME
    else:
        flash('wrong password!')
    env.level=env.level[:-1]
    return index()
  



# def_logout***
@app.route("/logout")
def logout():
    env.level+='-'
    print()
    print(env.level,white('route logout() : >',bold=True))
    loguer(env.level+' route logout() : >')
    print()
    route="/logout"
    session['logged_in'] = False
    env.level=env.level[:-1]
    return index() 
    



# def_stopServer***
@app.route('/stop', methods=['GET'])
def stopServer():
    env.level+='-'
    print()
    print(env.level,white('route stopServer() : >',bold=True))
    loguer(env.level+' route stopServer() : >')
    print()
    route="/stop"
    os.kill(os.getpid(), signal.SIGINT)
    env.level=env.level[:-1]
    return "Flask Server is shutting down..."
    



#  def_list_htmlpage***
@app.route('/list_htmlpage', methods=['GET','POST'])
def list_htmlpage():
    '''
    MODIFIED : 20250724

	list every html pages into the ./templates subfolder
    '''
    env.level+='-'
    # print()
    # print(env.level,white('route list_htmlpage() : >',bold=True))
    #loguer(env.level+' route list_htmlpage() : >')
    # print()
    with open('./result/home_url.txt') as file:
        home_url=file.read()
    html_output='<html><body><a href="'+home_url+'"><b><= back to home</b></a><h4>HTML PAGES :</h4><table border="1"><tbody>';
    files =[file for file in os.listdir('./code_app_html_templates')]
    ii=0
    function_list=[]
    for file in files:
        if '.html' in file:
            # print(' file : ',yellow(file,bold=True)) 
            html_output=html_output+'<tr><td><b><a href="/code_edit?code='+file+'&type=html">'+file+'</a></td><td><a href="/edit_html?filename=../code_app_html_templates/'+file+'">( open in notepad++)</a></td><td><a href="/del_html_file?filename=./code_app_html_templates/'+file+'">(DEL)</a></b></td><td><a href="/rename_file?filename=../code_app_html_templates/'+file+'&scriptdir=code_app_html_templates">(REN)</a></b></td><td><a href="/duplicate_html?filename='+file+'">(duplic)</a></b></td></tr>'
    env.level=env.level[:-1]
    html_output=html_output+'\n</tbody></table><br><a href="/stop">Click here to stop the App  </a></body><html>'
    return html_output
  
  


# def_new_function***
@app.route('/new_function', methods=['GET','POST'])
def new_function():
    '''
    MODIFIED 20250605
    
    display formular for create a new function
    '''
    env.level+='-'
    print()
    print(env.level,white('route new_function() : >',bold=True))
    loguer(env.level+' route new_function() : >')
    print()
    with open('./result/home_url.txt') as file:
        home_url=file.read()
    html_output='''<html><body><a href="'''+home_url+'''"><b><= back to home</b></a><br><br>
    <form action="/new_function_create" method="GET">
    <b>function name : </b><input type="text"  id="function_name" name="name" width="80"/>-- Args :<input type="text"  id="args" name="args" value="()"/><br><br>
    <b>Function description</b><br>
    <textarea id="description" name="description" rows="5" cols="50"></textarea><br><br>
    <center><input type="submit" value="valid"/></center>
    </form>
    </body></html>
    ''';   
    env.level=env.level[:-1]
    return html_output
    
    


#  new_route***
@app.route('/new_route', methods=['GET','POST'])
def new_route():
    '''
    MODIFIED : 20250507
    display formular for create a new route  
    '''
    env.level+='-'
    print()
    print(env.level,white('route new_route() : >',bold=True))
    loguer(env.level+' route new_route() : >')
    print()
    with open('./result/home_url.txt') as file:
        home_url=file.read()
    html_output='''<html><body><a href="'''+home_url+'''"><b><= back to home</b></a><br><br>
    <form action="/new_route_create" method="GET">
    <b>route name : </b><input type="text"  id="route_name" name="name" /><br><br>
    <b>route description</b><br>
    <textarea id="description" name="description" rows="5" cols="50"></textarea><br><br>
    <center><input type="submit" value="valid"/></center>
    </form>
    </body></html>
    ''';   
    env.level=env.level[:-1]
    return html_output 


# def_new_script_route***
@app.route('/new_script_route', methods=['GET','POST'])
def new_script_route():
    '''
    MODIFIED 20250324
    
    display formular for create a new_script_route of an external script
    '''
    env.level+='-'
    print()
    print(env.level,white('route new_script_route() : >',bold=True))
    loguer(env.level+' route new_script_route() : >')
    print()
    scriptdir = request.args.get('scriptdir')
    print()
    print(' scriptdir:\n',yellow(scriptdir,bold=True))
    print()      
    with open('./result/home_url.txt') as file:
        home_url=file.read()
    html_output='''<html><body><a href="'''+home_url+'''"><b><= back to home</b></a><center><h3>new route for [ '''+scriptdir+'''.py ]</h3></center>
    <form action="/new_script_route_create" method="GET">
    <b>route name : </b><input type="text"  id="function_name" name="name" /><br><br>
    <b>route description</b><br>
    <textarea id="description" name="description" rows="5" cols="50"></textarea><br><br>
    <input type="hidden"  id="scriptdir" name="scriptdir" value="'''+scriptdir+'''"/>
    <center><input type="submit" value="create"/></center>
    </form>
    </body></html>
    ''';   
    env.level=env.level[:-1]
    return html_output
    
    


#  def_new_html_page***
@app.route('/new_html_page', methods=['GET'])
def new_html_page():
    '''
    MODIFIED : 20250923
    
    display formular for creating a new html page in the ./templates folder
    '''
    route="/new_html_page"
    env.level+='-'
    print()
    print(env.level,white('route new_html_page() : >',bold=True))
    loguer(env.level+' route new_html_page() : >')
    print()
    with open('./result/home_url.txt') as file:
        home_url=file.read()
    html_output='''<html><body><a href="'''+home_url+'''"><b><= back to home</b></a><br><br>
    <form action="/new_html_page_create" method="GET">
    <b>page name : </b><input type="text"  id="page_name" name="name" /> ( just the name ex ; my_page )<br><br>
    <b>page description</b><br>
    <textarea id="description" name="description" rows="5" cols="50"></textarea><br><br>
    <b>Select a template :</b><br>
    <select name="template">
    <option value="page1">Like Index page</option>
    <option value="page2">Like page for result ( operation done )</option>
    <option value="page3">Like page for item selection</option>
    <option value="page4">Like page complex formular</option>  
    <option value="page5">Like page report in a textarea</option>
    <option value="page6">Like page formular for searching keyword edit box</option>
    <option value="page7">Like page formular for entering paragraph into textarea</option>    
    <option value="page8">Like page result into textarea black</option>  
    <option value="page9">calandar</option>
    <option value="page10">Dark Input field over white background</option>
    <option value="page11">Toggled hints</option>   
    <option value="page12">result page text area on white background & action button</option> 
    <option value="page13">EMPTY PAGE</option> 
    <option value="page14">Result List with Searching field</option> 
    <option value="page15">Search Keyword in wich field</option>     
    </select>
    <center><br><br><input type="submit" value="valid"/></center>
    </form>
    </body></html>
    ''';   
    env.level=env.level[:-1]
    return html_output  
    



# def_save_code***
@app.route('/save_code', methods=['POST'])
def save_code():
    '''
        version 20250825
    '''
    env.level+='-'
    # print()
    # print(env.level,white('route save_code() : >',bold=True))
    #loguer(env.level+' route save_code() : >')
    # print()
    python_code = request.form['code']
    # print()
    # print(' code:\n',yellow(python_code,bold=True))
    # print()
    # print()
    if python_code[0]=="#":
        filename=python_code.split("***")[0]
        python_code=python_code.split(",***subdir=***")[0]        
        if "def_"  in filename:
            filename=filename.replace("#  ","")
            filename=filename.replace("# ","")
            if '.py' not in filename:
                filename=filename+'.py'
            if '@app.route' in python_code:
                with open('./result/current_edited_route.txt','w') as file:
                    file.write('route_'+filename)            
                filename='./code_app_routes/route_'+filename  
            else:
                with open('./result/current_edited_function.txt','w') as file:
                    file.write(filename)            
                filename='./code_app_functions/'+filename      
                
            filename=filename.replace(" ","_")        
            filename=filename.replace("__","_")      
            # print()
            # print(' filename: ',yellow(filename,bold=True))
            # print()
            #filepath='./code_chunks/'+filename
            python_code=python_code.replace('\t','    ')
            lines=python_code.split('\n')
            output_lines=''
            for line in lines:
                line2=line.replace(' ','*')
                print(line2)
                if '                                      ' in line:
                    print(red('found 42',bold=True))
                    line=line.strip()
                    line='                                        '+line        
                elif '                                  ' in line:
                    print(red('found 38',bold=True))
                    line=line.strip()
                    line='                                    '+line         
                elif '                              ' in line:
                    print(red('found 34',bold=True))
                    line=line.strip()
                    line='                                '+line         
                elif '                              ' in line:
                    print(red('found 30',bold=True))
                    line=line.strip()
                    line='                                '+line        
                elif '                          ' in line:
                    print(red('found 26',bold=True))
                    line=line.strip()
                    line='                            '+line        
                elif '                      ' in line:
                    print(red('found 22',bold=True))
                    line=line.strip()
                    line='                        '+line                                   
                elif '                  ' in line:
                    print(red('found 18',bold=True))
                    line=line.strip()
                    line='                    '+line
                elif '              ' in line:
                    print(red('found 14',bold=True))
                    line=line.strip()
                    line='                '+line            
                elif '          ' in line:
                    print(red('found 10',bold=True))
                    line=line.strip()
                    line='            '+line             
                elif '      ' in line:
                    print(red('found 6',bold=True))
                    line=line.strip()
                    line='        '+line            
                else:
                    print(green('perfect',bold=True))
                line2=line.replace(' ','*')  
                print('new line :',cyan(line2,bold=True))
                output_lines=output_lines+line+'\n'
                #a=input('NEXT')
            output_lines=output_lines.replace('\n\n\n','\n\n')     
            output_lines=output_lines.replace('\n\n','\n')             
            with open(filename,"w") as file:
                file.write(output_lines)
    else:
        filename=python_code.split(",***subdir=***")[1]    
        python_code=python_code.split(",***subdir=***")[0]
        # print()
        # print(' python_code: ',yellow(python_code,bold=True))
        # print()         
        #filename=filename.replace("./","")
        # print()
        # print(' filename: ',yellow(filename,bold=True))
        # print() 
        python_code=python_code.replace('\n\n\n','\n\n')     
        python_code=python_code.replace('\n\n','\n')           
        with open(filename,"w") as file:
            file.write(python_code)    
    with open('./result/current_edited_script.txt',"w") as file:
        file.write(filename)     
    route="/save_code"
    PAGE_DESTINATION="code_saved.html"
    page_name="code_saved.html"
    env.level=env.level[:-1]
    return render_template('code_saved.html')
    
    


# def_save_code_B***
@app.route('/save_code_B', methods=['POST'])
def save_code_B():
    '''
        version : 20250825
        save code for script to import
    '''
    env.level+='-'
    # print()
    # print(env.level,white('route save_code_B() : >',bold=True))
    #loguer(env.level+' route save_code_B() : >')
    # print()
    params = request.form['code']
    python_code=params.split(',***subdir=***')[0]
    # print()
    # print(' python_code:\n',yellow(python_code,bold=True))
    # print()
    # print()
    fichier = params.split(',***subdir=***')[1]
    # print()
    # print(' fichier:\n',yellow(fichier,bold=True))
    # print()
    # print()
    python_code=python_code.replace('\t','    ')
    lines=python_code.split('\n')
    output_lines=''
    for line in lines:
        line2=line.replace(' ','*')
        print(line2)
        if line.startswith('                                              '):
            print(red('found 46',bold=True))
            line=line.strip()
            line='                                            '+line          
        elif line.startswith('                                          '):
            print(red('found 42',bold=True))
            line=line.strip()
            line='                                        '+line        
        elif line.startswith('                                      '):
            print(red('found 38',bold=True))
            line=line.strip()
            line='                                    '+line         
        elif line.startswith('                                  '):
            print(red('found 34',bold=True))
            line=line.strip()
            line='                                '+line         
        elif line.startswith('                              '):
            print(red('found 30',bold=True))
            line=line.strip()
            line='                                '+line        
        elif line.startswith('                          '):
            print(red('found 26',bold=True))
            line=line.strip()
            line='                            '+line        
        elif line.startswith('                      '):
            print(red('found 22',bold=True))
            line=line.strip()
            line='                        '+line        
        elif line.startswith('                  '):
            print(red('found 18',bold=True))
            line=line.strip()
            line='                    '+line
        elif line.startswith('              '):
            print(red('found 14',bold=True))
            line=line.strip()
            line='                '+line            
        elif line.startswith('          '):
            print(red('found 10',bold=True))
            line=line.strip()
            line='            '+line             
        elif line.startswith('      '):
            print(red('found 6',bold=True))
            line=line.strip()
            line='        '+line            
        else:
            print(green('perfect',bold=True))
        line2=line.replace(' ','*')  
        print('new line :',cyan(line2,bold=True))
        output_lines=output_lines+line+'\n'
        #a=input('NEXT')
    output_lines=output_lines.replace('\n\n\n','\n\n')     
    output_lines=output_lines.replace('\n\n','\n')         
    with open(fichier,'w') as file:
        file.write(output_lines)
    liste=fichier.split('/')
    current_script=liste[-1]
    with open('./result/current_edited_script.txt',"w") as file:
        file.write(current_script)
    route="/save_code_B"
    PAGE_DESTINATION="code_saved.html"
    page_name="code_saved.html"
    env.level=env.level[:-1]
    return render_template('code_saved.html')
    
    


#  def_new_function_create***
@app.route('/new_function_create', methods=['GET','POST'])
def new_function_create():
    '''
    Modified : 202501001
    
    create the function .py file into the ./code_chunks subfolder if that one doesn t already exist
    '''
    env.level+='-'
    print()
    print(env.level,white('route new_function_create() : >',bold=True))
    loguer(env.level+' route new_function_create() : >')
    print()
    name = request.args.get('name')
    name=name.replace('-','_')
    name=name.replace(' ','_')    
    description = request.args.get('description')
    args = request.args.get('args')       
    filename='./code_app_functions/def_'+name+'.py'
    filename2='/def_'+name+'.py'

    print()
    print(' filename :\n',yellow(filename,bold=True))
    print()
    print()
    print(' filename2 :\n',yellow(filename2,bold=True))
    print()
    print(' description :\n',yellow(description,bold=True))
    print()
    print(magenta('--> CALL  A SUB FUNCTION :',bold=True))
    # check if file already exits
    with open('./code_architecture/app_functions.txt') as file:
        text_content=file.read()
    print(' text_content :\n',yellow(text_content,bold=True))
    with open('./code_architecture/app_routes.txt') as file:
        text_content2=file.read()
    print(' text_content :\n',yellow(text_content,bold=True))    
    print()          
    mot=filename2.replace('/','')
    print(' mot :\n',yellow(mot,bold=True))
    print()    
    if mot in text_content or mot in text_content2:
        print(filename+' already exists ! Choose another name')
        with open('./result/home_url.txt') as file:
            home_url=file.read()        
        html_output='''<html><body><a href="'''+home_url+'''"><b><= back to home</b></a><br><br>
        <center><h3>This function already exists ! choose another name</h3></center>
    <form action="/new_function_create" method="GET">
    <b>function name : </b><input type="text"  id="function_name" name="name" /><br><br>
    <b>Function description</b><br>
    <textarea id="description" name="description" rows="5" cols="50"></textarea><br><br>
    <center><input type="submit" value="valid"/></center>
    </form>        
        </body></html>
        ''';        
    else:
        print(yellow(f'     {filename} does NOT exists. Let s create it',bold=True))
        with open('./code_templates/function_template.py') as file:
            text_content=file.read()
        text_content=text_content.replace('example_name',name)
        version='MODIFIED : '+current_date_and_time_for_json_data()+'\n\n    description : '
        description=version+description
        text_content=text_content.replace('***description***',description) 
        text_content=text_content.replace('***app.py***','app.py')        
        text_content=text_content.replace('(args)',args)         
        with open(filename,"w") as fichier:
            fichier.write(text_content)     
        with open('./code_architecture/app_functions.txt',"a+") as fichier:
            filename2=filename2.replace('/','')
            fichier.write(filename2+'\n')  
        with open('./result/home_url.txt') as file:
            home_url=file.read()
        html_output='''<html><body><a href="'''+home_url+'''"><b><= back to home</b></a><br><br>
        <center><h3>function created</h3></center>
        <center><h3><a href="/code_edit?code='''+filename2+'''&type=function">EDIT in inline editor :'''+filename2+'''</a>. OR .<a href="/edit_html?filename=.'''+filename+'''">( Edit in notepad++ )</a></center>
        </body></html>
        ''';             
    with open('./result/current_edited_script.txt',"w") as file:
        file.write(filename2)        
    env.level=env.level[:-1]
    return html_output   
    
    


# def_new_route_create***
@app.route('/new_route_create', methods=['GET','POST'])
def new_route_create():
    env.level+='-'
    print()
    print(env.level,white('route new_route_create() : >',bold=True))
    loguer(env.level+' route new_route_create() : >')
    print()
    '''
    Modified : 20250923
    
    create the route .py file into the ./code_app_routes subfolder if that one doesn t already exist
    '''    
    name = request.args.get('name')
    name=name.replace('-','_')
    name=name.replace(' ','_')    
    if '/' in name:
        name=name.replace('/','')
    description = request.args.get('description')
    filename='./code_app_routes/route_def_'+name+'.py'
    filename2='/route_def_'+name+'.py'

    print()
    print(' filename :\n',yellow(filename,bold=True))
    print()
    print()
    print(' filename2 :\n',yellow(filename2,bold=True))
    print()
    print(' description :\n',yellow(description,bold=True))
    print()
    print(magenta('--> CALL  A SUB FUNCTION :',bold=True))
    # check if file already exits
    with open('./code_architecture/app_routes.txt') as file:
        text_content2=file.read()    
    fichier_route = Path('./code_app_routes/route_def_'+name+'.py')    
    if fichier_route.is_file() or filename in text_content2:
        print(filename+' already exists ! Choose another name')
        with open('./result/home_url.txt') as file:
            home_url=file.read()        
        html_output='''<html><body><a href="'''+home_url+'''"><b><= back to home</b></a><br><br>
        <center><h3>This route already exists ! choose another name</h3></center>
    <form action="/new_route_create" method="GET">
    <b>route name : </b><input type="text"  id="route_name" name="name" /><br><br>
    <b>route description</b><br>
    <textarea id="description" name="description" rows="5" cols="50"></textarea><br><br>
    <center><input type="submit" value="valid"/></center>
    </form>        
        </body></html>
        ''';        
    else:
        print(yellow(f'     {filename} does NOT exists. Let s create it',bold=True))
        with open('./code_templates/route_template.py') as file:
            text_content=file.read()
        text_content=text_content.replace('example_name',name)
        version='Created : '+current_date_and_time_for_json_data()+'\n\n    description : '
        description=version+description
        text_content=text_content.replace('***description***',description) 
        with open(filename,"w") as fichier:
            fichier.write(text_content)     
        with open('./code_architecture/app_routes.txt',"a+") as fichier:
            filename2=filename2.replace('/','')
            fichier.write(filename2+'\n')  
        with open('./result/home_url.txt') as file:
            home_url=file.read()
        html_output='''<html><body><a href="'''+home_url+'''"><b><= back to home</b></a><br><br>
        <center><h3>route created</h3></center>
        <center><h3><a href="/code_edit?code='''+filename2+'''&type=route">EDIT in inline editor :'''+filename2+'''</a>. OR .<a href="/edit_html?filename=.'''+filename+'''">( Edit in notepad++ )</a></center>
        </body></html>
        ''';             
    env.level=env.level[:-1]
    return html_output  


#  def_new__script_route_create***
@app.route('/new_script_route_create', methods=['GET','POST'])
def new__script_route_create():
    '''
    Modified : 20250324
    
    create a new route for the selected imported script
    '''
    env.level+='-'
    print()
    print(env.level,white('route new__script_route_create() : >',bold=True))
    loguer(env.level+' route new__script_route_create() : >')
    print()
    scriptdir= request.args.get('scriptdir')    
    name = request.args.get('name')
    name=name.replace('-','_')
    name=name.replace(' ','_')    
    description = request.args.get('description')

    filename='./code_app_scripts_to_import/'+scriptdir+'/route_def_'+name+'.py'
    filename2='/route_def_'+name+'.py'

    print()
    print(' filename :\n',yellow(filename,bold=True))
    print()
    print()
    print(' filename2 :\n',yellow(filename2,bold=True))
    print()
    print(' description :\n',yellow(description,bold=True))
    print()
    print()
    print(' scriptdir :\n',yellow(scriptdir,bold=True))
    print()    
    with open('./result/home_url.txt') as file:
        home_url=file.read()
    # check if file already exits 
    fichier_route = Path(filename)    
    if fichier_route.is_file():    
        print(filename+' already exists ! Choose another name')
        html_output='''<html><body><a href="'''+home_url+'''"><b><= back to home</b></a><center><h3>new function for [ '''+scriptdir+'''.py ]</h3></center>
    <form action="/new_script_route_create" method="GET">
    <b>function name : </b><input type="text"  id="function_name" name="name" /><br><br>
    <b>Function description</b><br>
    <textarea id="description" name="description" rows="5" cols="50"></textarea><br><br>
    <input type="hidden"  id="scriptdir" name="scriptdir" value="'''+scriptdir+'''"/>
    <center><input type="submit" value="create"/></center>
    </form>
    </body></html>
    ''';         
    else:
        print(yellow(f'     {filename} does NOT exists. Let s create it',bold=True))
        with open('./code_templates/route_template.py') as file:
            text_content=file.read()
        text_content=text_content.replace('example_name',name)
        version='MODIFIED : '+current_date_and_time_for_json_data()+'\n\n    description : '
        description=version+description
        text_content=text_content.replace('***description***',description) 
        with open(filename,"w") as fichier:
            fichier.write(text_content)     
        with open(f'./code_app_scripts_to_import/{scriptdir}/script_routes.txt',"a+") as fichier:
            filename2=filename2.replace('/','')
            fichier.write(filename2+'\n')  
        html_output='''<html><body><a href="'''+home_url+'''"><b><= back to home</b></a><br><br>
        <center><h3>function created</h3></center>
        <center><h3><a href="/code_edit_B?code='''+filename2+'''&subdir='''+scriptdir+'''">EDIT in inline editor :'''+filename2+'''</a>. OR .<a href="/edit_html?filename=.'''+filename+'''">( Edit in notepad++ )</a></center><hr><br><b><a href="/new_script_function?scriptdir='''+scriptdir+'''">Create a new function for [ '''+scriptdir+'''.py ]</a></b><br><b><a href="/new_script_route?scriptdir='''+scriptdir+'''">Create a new route for [ '''+scriptdir+'''.py ]</a></b>
        </body></html>
        ''';           
    with open('./result/current_edited_script.txt',"w") as file:
        file.write(filename2)          
    env.level=env.level[:-1]
    return html_output   
    
    


# def_page_info***
@app.route('/page_info', methods=['GET'])
def page_info():
    '''
        Modified : 20250708
        
        description : display page_info.html
    '''
    env.level+='-'
    # print()
    # print(env.level,white('route page_info() : >',bold=True))
    #loguer(env.level+' route page_info() : >')
    # print()
    route="/page_info"
    page=request.args.get('page')
    route=request.args.get('route').split('?')[0]
    # print()
    # print('page : ',yellow(page,bold=True))
    # print()
    # print('route : ',yellow(route,bold=True))
    url='/page_info?page='+page+'&route='+route
    with open('./result/home_url.txt','w') as file:
        file.write(url)
    chunk=route+'.py'
    chunk=chunk.replace('/','route_def_')
    # print()
    with open('./result/current_edited_imported_script.txt') as file:
        last_edited_script=file.read()          
    # print()
    # print('last_edited_script : ',yellow(last_edited_script,bold=True))
    # print()          
    env.level=env.level[:-1]
    return render_template('page_info.html',page=page,route=route,chunk=chunk,last_edited_script=last_edited_script)
    


# def_tools***
@app.route('/tools', methods=['GET'])
def tools():
    env.level+='-'
    print()
    print(env.level,white('route tools() : >',bold=True))
    loguer(env.level+' route tools() : >')
    print()
    route="/tools"
    global client_id
    global client_password
    global host
    global host_for_token
    global profil_name
    global access_token
    if not session.get('logged_in'):
        env.level=env.level[:-1]
        return render_template('login.html')
    else:
        print('client_id : ',client_id)
        print('client_password : ',client_password);
        print('host : ',host)
        if "https://private.intel.eu.amp.cisco.com" in host:
            host_for_token="https://visibility.eu.amp.cisco.com"
        elif "https://private.intel.amp.cisco.com" in host:
            host_for_token="https://visibility.amp.cisco.com"
        else:
            host_for_token="https://visibility.apjc.amp.cisco.com"
        print('host_for_token : ',host_for_token)
        print('profil_name : ',profil_name);
        #print("incidents : \n",yellow(result,bold=True))
        message1="Current XDR tenant profile : "+profil_name
        image="../static/images/toolbox.png" 
        message2="XDR Tool Library. Select the tool category you want to invoke"
        message3="/"
        message4="Select a tool Category"
        PAGE_DESTINATION="tools"  
        env.level=env.level[:-1]
        return render_template('main_index.html',route=route,USERNAME=session['user'],PAGE_DESTINATION=PAGE_DESTINATION,image=image,message1=message1,message2=message2,message3=message3,message4=message4)
        



# def_edit_html***
@app.route('/edit_html', methods=['GET'])
def edit_html():
    env.level+='-'
    route="/edit_html"
    print()
    print(env.level,white('route edit_html() : >',bold=True))
    #loguer(env.level+' route edit_html() : >')
    filename=request.args.get('filename')
    print()
    print(yellow(f"- filename : {filename}",bold=True))
    command="start notepad++.exe ./code_app_html_templates/"+filename
    result = os.system(command)
    print()    
    with open('./result/home_url.txt') as file:
        home_url=file.read()   
    env.level=env.level[:-1]
    return render_template('OK.html',home_url=home_url)
   




# def_edit_todo***
@app.route('/edit_todo', methods=['GET'])
def edit_todo():
    env.level+='-'
    route="/edit_todo"
    print()
    print(env.level,white('route edit_todo() : >',bold=True))
    #loguer(env.level+' route edit_todo() : >')
    command="start notepad++.exe ./templates/todo.txt"
    result = os.system(command)
    print()    
    with open('./result/home_url.txt') as file:
        home_url=file.read()   
    env.level=env.level[:-1]
    return render_template('OK.html',home_url=home_url)

        


# def_note***
@app.route('/note', methods=['GET'])
def note():
    env.level+='-'
    route="/note"
    print()
    print(env.level,white('route note() : >',bold=True))
    loguer(env.level+' route note() : >')
    print()
    global client_id
    global client_password
    global host
    global host_for_token
    global profil_name
    if not session.get('logged_in'):
        env.level=env.level[:-1]
        return render_template('login.html')
    else:
        # GET variable from calling web page
        note='note_'+request.args.get('note')
        print()
        print('note : ',yellow(note,bold=True))
        print()
        with open('./templates/'+note) as fichier:
            text_content=fichier.read()
        html_content=text_content.replace("\n","<BR>")
        env.level=env.level[:-1]
        return html_content
        
        


# create_app_py***
@app.route('/create_app_py', methods=['GET'])
def create_app_py():
    env.level+='-'
    route="/create_app_py"
    print()
    print(env.level,white('def create_app_py() : >',bold=True))
    loguer(env.level+' def create_app_py() : >')
    print()
    with open('./app.py') as file:
            text_content=file.read()     
    with open('./code_backup/app_'+current_date_and_time()+'.py','w') as file:
            file.write(text_content)     
    print()
    print(green('   app.py backup = OK',bold=True))
    print()                
    with open('./app_new.py','w') as app:
        print()
        print(green('  Create header',bold=True))
        print()    
        with open('./code_system_main_blocs/a_core_header.py') as file:
            text_content=file.read() 
        app.write(text_content)
        app.write('\n')
        print(green('  - Create header = OK',bold=True))
        print()
        print(green('  Create Import section',bold=True))
        with open('./code_system_main_blocs/a_core_imports.py') as file:
            text_content=file.read() 
        app.write(text_content)
        app.write('\n')   
        print(green('  - Create Import section = OK',bold=True))
        print()
        print(green('  Create Global Variable Definition',bold=True))
        with open('./code_system_main_blocs/a_core_global_definitions.py') as file:
            text_content=file.read() 
        app.write(text_content)
        app.write('\n')
        app.write('\n')     
        print(green('  - Create Global Variable Definition = OK',bold=True))
        print()
        print(green('  Create system functions ',bold=True))      
        line_out='''
# here under FUNCTIONS ===========================   
 
'''
        app.write(line_out)            
        with open('./code_architecture/system_functions.txt') as file:
            text_content=file.read()
        lines=text_content.split('\n')
        for script_name in lines:
            print(script_name)
            if script_name.strip() !="":
                with open(f'./code_system_functions/{script_name}') as file2:
                    text_content2=file2.read() 
                app.write(text_content2)
                app.write('\n\n')
        print(green('  - Create system functions = OK',bold=True))
        print()  
        print(green('  Create application functions',bold=True))
        app.write(line_out)            
        with open('./code_architecture/app_functions.txt') as file:
            text_content=file.read()
        lines=text_content.split('\n')
        for script_name in lines:
            print(script_name)
            if script_name.strip() !="":
                with open(f'./code_app_functions/{script_name}') as file2:
                    text_content2=file2.read() 
                app.write(text_content2)
                app.write('\n\n')
        print(green('  - Create application functions = OK',bold=True))
        print()     
        print(green('  Create system routes ',bold=True))        
        line_out='''
# here under the flask routes part ===========================    

app = Flask(__name__)

'''
        app.write(line_out)
        with open('./code_architecture/system_routes.txt') as file:
            text_content=file.read()
        lines=text_content.split('\n')
        for script_name in lines:
            print(script_name)
            if script_name.strip() !="":
                with open(f'./code_system_routes/{script_name}') as file2:
                    text_content2=file2.read() 
                app.write(text_content2)
                app.write('\n\n')  
                
        print(green('  - Create system routes = OK',bold=True))
        print()     
        print(green('  Create application routes',bold=True))  
        with open('./code_architecture/app_routes.txt') as file:
            text_content=file.read()
        lines=text_content.split('\n')
        for script_name in lines:
            print(script_name)
            if script_name.strip() !="":
                with open(f'./code_app_routes/{script_name}') as file2:
                    text_content2=file2.read() 
                app.write(text_content2)
                app.write('\n\n')           
        print(green('  - Create system routes = OK',bold=True))
        print()     
        print(green('  Create Main Function',bold=True))        
        with open('./code_system_main_blocs/a_core_main.py') as file:
            text_content=file.read() 
        app.write('\n') 
        app.write(text_content)
        app.write('\n')         
        print(green('  - Create Main Function = OK',bold=True))          
    with open('./result/home_url.txt') as file:
        home_url=file.read()            
    html_output='''<html><body><a href="'''+home_url+'''"><b><= back to home</b></a><br><br>
    <center><h2>app_new.py created in the root directory</h2><b>It is actually named : app_new.py</b></center></body></html>''';          
    env.level=env.level[:-1]
    return html_output


# under_construction***
def under_construction():
    env.level+='-'
    print()
    print(env.level,white('route under_construction() : >',bold=True))
    loguer(env.level+' route under_construction() : >')
    print()
    route="/under_construction"
    print()
    print(red('UNDER CONSTRUCTION',bold=True))
    print()
    PAGE_DESTINATION="under_construction"
    page_name="under_contrustion.html"
    env.level=env.level[:-1]
    return render_template('main_index.html',route=route,USERNAME=session['user'],PAGE_DESTINATION=PAGE_DESTINATION,page_name=page_name)
    



#  def_new_html_page_create***
@app.route('/new_html_page_create', methods=['GET'])
def new_html_page_create():
    '''
    MODIFIED : 2025-09-25

    description : Create a new html page into the ./tempates subfolder
    '''
    route="/new_html_page_create"
    env.level+='-'
    print()
    print(env.level,white('route new_html_page_create() : >',bold=True))
    loguer(env.level+' route new_html_page_create() : >')
    print()
    name = request.args.get('name')
    name=name.split('.')[0]
    description = request.args.get('description')
    template = request.args.get('template')
    filename='z_'+name+'.html'
    print()
    print(' filename :\n',yellow(filename,bold=True))
    print()
    print()
    print(' template :\n',yellow(template,bold=True))
    print()
    print(' description :\n',yellow(description,bold=True))
    print()
    print(magenta('--> CALL  A SUB FUNCTION :',bold=True))
    # check if file already exits
    fichier_function = Path('z_'+name+'.html')    
    if fichier_function.is_file():
        print(filename+' already exists ! Choose another name')
        html_output='''<html><body>
        <center><h3>This html page already exists ! choose another name</h3></center>
    <form action="/new_html_page_create" method="GET">
    <b>Page name : </b><input type="text"  id="function_name" name="name" /><br><br>
    <b>Page description</b><br>
    <textarea id="description" name="description" rows="5" cols="50"></textarea><br><br>
    <center><input type="submit" value="valid"/></center>
    </form>        
        </body></html>
        ''';        
    else:
        print(yellow(f'     {filename} does NOT exists. Let s create it',bold=True))
        if template=='page1':
            with open('./code_templates/html_page.html') as file:
                text_content=file.read()
        elif template=='page2':
            with open('./code_templates/html_page2.html') as file:
                text_content=file.read()   
        elif template=='page3':
            with open('./code_templates/html_page3.html') as file:
                text_content=file.read()     
        elif template=='page4':
            with open('./code_templates/html_page4.html') as file:
                text_content=file.read() 
        elif template=='page5':
            with open('./code_templates/html_page5.html') as file:
                text_content=file.read()       
        elif template=='page6':
            with open('./code_templates/html_page6.html') as file:
                text_content=file.read()     
        elif template=='page7':
            with open('./code_templates/html_page7.html') as file:
                text_content=file.read()     
        elif template=='page8':
            with open('./code_templates/html_page8.html') as file:
                text_content=file.read()       
        elif template=='page9':
            with open('./code_templates/html_page9.html') as file:
                text_content=file.read()   
        elif template=='page10':
            with open('./code_templates/html_page10.html') as file:
                text_content=file.read()              
        elif template=='page11':
            with open('./code_templates/html_page11.html') as file:
                text_content=file.read()   
        elif template=='page12':
            with open('./code_templates/html_page12.html') as file:
                text_content=file.read()               
        elif template=='page13':
            with open('./code_templates/html_page13.html') as file:
                text_content=file.read()         
        elif template=='page14':
            with open('./code_templates/html_page14.html') as file:
                text_content=file.read()         
        elif template=='page15':
            with open('./code_templates/html_page15.html') as file:
                text_content=file.read()          
        elif template=='page16':
            with open('./code_templates/html_page1.html') as file:
                text_content=file.read()                    
        text_content=text_content.replace('example_name',name)
        text_content="* "+filename+"***"+text_content
        version='Created : '+current_date_and_time_for_json_data()+'\n\n    description : '
        description=version+description
        text_content=text_content.replace('***description***',description) 
        filename2=filename.replace("./templates/","")
        filename2=filename2.replace(".html","")
        main_index_chunk='''&nbsp;&nbsp;&nbsp;&nbsp;{% if PAGE_DESTINATION == &quot;'''+filename2+'''&quot;%}<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{% extends &quot;'''+filename2+'''.html&quot; %}<br>
&nbsp;&nbsp;&nbsp;&nbsp;{% endif %} '''
        with open("./code_app_html_templates/"+filename,"w") as fichier:
            fichier.write(text_content)     
        with open('./result/home_url.txt') as file:
            home_url=file.read()
        html_output='''<html><body><a href="'''+home_url+'''"><b><= back to home</b></a><br><br>
        <center><h3>function created</h3></center>
        <center><h3><a href="/code_edit?code='''+filename+'''&type=html">EDIT in inline editor :'''+filename+'''</a>. OR .<a href="/edit_html?filename='''+filename+'''">( Edit in notepad++ )</a></center><br><br>'''+main_index_chunk+'''
        </body></html>
        ''';      
        with open('./code_architecture/main_html.txt',"a+") as fichier:
            fichier.write(filename+'\n')        
    env.level=env.level[:-1]
    return html_output  


#  def_list_snippets***
@app.route('/list_snippets', methods=['GET'])
def list_snippets():
    '''
    Created : 2025-03-31T17:42:51.000Z

    list code snippets
    '''
    route="/list_snippets"
    env.level+='-'
    # print()
    # print(env.level,white('route list_snippets() : >',bold=True))
    #loguer(env.level+' route list_snippets() : >')
    # print()
    with open('./result/home_url.txt') as file:
        home_url=file.read()
    html_output='<html><body><a href="'+home_url+'"><b><= back to home</b></a><ul>';
    files =[file for file in os.listdir('./code_snippets')]
    ii=0
    function_list=[]
    for file in files:
        # print(' file : ',yellow(file,bold=True)) 
        html_output=html_output+'<li><b><a href="/read_code_snippet?snippet='+file+'">'+file+'</a></b></li>'
    env.level=env.level[:-1]
    html_output=html_output+'\n</ul><br><a href="/stop">Click here to stop the App  </a></body><html>'
    return html_output
        



# def list_routes***
@app.route('/list_routes', methods=['GET','POST'])
def list_routes():
    '''
        modified : 2025-09-25
        
        description : liste application routes
        
        how_to_call : list_routes()
    '''
    env.level+='-'
    # print()
    # print(env.level,white('route list_routes() : >',bold=True))
    #loguer(env.level+' route list_routes() : >')
    # print()
    with open('./result/home_url.txt') as file:
        home_url=file.read()
    if os.path.exists('./result/keyword.txt'):
        with open('./result/keyword.txt') as file:
            keyword=file.read()  
    else:
        keyword=''
    html_output='<html><body><a href="'+home_url+'"><b><= back to home</b></a><br><br><form action="/search_app_route" method="get"><input type="text" name="keyword" value="'+keyword+'"><input type="submit" value="Search"></form><br><br>';
    with open('./result/current_edited_route.txt') as file:
        last_route=file.read()
    html_output=html_output+'<b><a href="/code_edit?code='+last_route+'&type=route">Last Edited : '+last_route+'</a><br><a href="/new_route">Create a new route</a><br><h4>ROUTES :</h4><table border="1"><tbody>';
    files =[file for file in os.listdir('./code_app_routes')]
    ii=0
    function_list=[]
    scriptdir='code_app_routes'
    for file in files:
        if 'route_' in file and 'a_core_' not in file and file !='back':
            # print(' file : ',yellow(file,bold=True)) 
            html_output=html_output+'<tr><td><b><a href="/code_edit?code='+file+'&type=route">'+file+'</a></td><td><a href="/edit_html?filename=../code_app_routes/'+file+'">( open in notepad++ )</a></td><td><a href="/delete_file?filename=../code_app_routes/'+file+'&scriptdir='+scriptdir+'">(DEL)</a></b></td><td><a href="/rename_file?filename=../code_app_routes/'+file+'&scriptdir='+scriptdir+'">(REN)</a></b></td><td><a href="/move_route_to_system?filename=../code_app_routes/'+file+'&scriptdir=code_system_routes">(mv 2 sys)</a></b></td><td><a href="/copy_route_to_central?filename=./code_app_routes/'+file+'&scriptdir=code_central_routes">(cp 2 central)</a></b></td><td><a href="/duplicate_route?filename='+file+'">(duplic)</a></b></td></tr>'
    env.level=env.level[:-1]
    html_output=html_output+'\n</tbody></table><br><a href="/list_functions">List Functions</a><br><br><a href="/stop">Click here to stop the App  </a></body><html>'
    return html_output
    



# def list_functions***
@app.route('/list_functions', methods=['GET','POST'])
def list_functions():
    '''
        modified : 20250923
        description : list system  functions in ./code_app_functions
    '''
    env.level+='-'
    # print()
    # print(env.level,white('route list_functions() : >',bold=True))
    #loguer(env.level+' route list_functions() : >')
    # print()
    with open('./result/home_url.txt') as file:
        home_url=file.read()
    if os.path.exists('./result/keyword.txt'):
        with open('./result/keyword.txt') as file:
            keyword=file.read()         
    html_output='<html><body><a href="'+home_url+'"><b><= back to home</b></a><br><br><form action="/search_app_function" method="get"><input type="text" name="keyword" value="'+keyword+'"><input type="submit" value="Search"></form><br><br>';
    with open('./result/current_edited_function.txt') as file:
        last_function=file.read()
    html_output=html_output+'<b><a href="/code_edit?code='+last_function+'&type=function">Last Edited : '+last_function+'</a><br><a href="/new_function">Create a new function</a><br><h4>FUNCTIONS :</h4><table border="1"><tbody>';   
    
    files =[file for file in os.listdir('./code_app_functions')]
    ii=0
    scriptdir='code_app_functions'
    function_list=[]
    for file in files:
        # print(' file : ',yellow(file,bold=True)) 
        html_output=html_output+'<tr><td><b><a href="/code_edit?code='+file+'&type=function">'+file+'</a></td><td><a href="/edit_html?filename=../code_app_functions/'+file+'">( open in notepad++ )</b></td><td><a href="/delete_file?filename=../code_app_functions/'+file+'&scriptdir='+scriptdir+'">(DEL)</a></b></td><td><a href="/rename_file?filename=../code_app_functions/'+file+'&scriptdir='+scriptdir+'">(REN)</a></b></td><td><a href="/move_function_to_system?filename=../code_app_functions/'+file+'&scriptdir=code_system_functions">( mv 2 sys )</a></b></td><td><a href="/copy_function_to_central?filename=./code_app_functions/'+file+'&scriptdir=code_central_functions">( cp 2 central )</a></b></td><td><a href="/duplicate_function?filename='+file+'">(duplic)</a></b></td></tr>'
    env.level=env.level[:-1]
    html_output=html_output+'\n</tbody></table><br><a href="/list_routes">List Routes</a><br><br><a href="/stop">Click here to stop the App  </a></body><html>'
    return html_output
    



#  def_read_code_snippet***
@app.route('/read_code_snippet', methods=['GET'])
def read_code_snippet():
    '''
    Created : 2025-03-31T19:45:47.000Z

read and display the content of the code snippet
    '''
    route="/read_code_snippet"
    env.level+='-'
    print()
    print(env.level,white('route read_code_snippet() : >',bold=True))
    loguer(env.level+' route read_code_snippet() : >')
    print()
    global client_id
    global client_password
    global host
    global host_for_token
    global profil_name
    if not session.get('logged_in'):
        return render_template('login.html')
    else:     
        snippet=request.args.get('snippet')
        print()
        print('snippet : ',snippet)
        print()
        with open('./code_snippets/'+snippet) as file:
            txt_content=file.read()    
        lines=txt_content.split('\n')
        html_out=''
        for line in lines:
            line=line.replace(' ','&nbsp;')
            html_out=html_out+line+'<br>'
    return html_out
        



# def_code_edit***
@app.route('/code_edit', methods=['GET','POST'])
def code_edit():
    env.level+='-'
    # print()
    # print(env.level,white('route code_edit() : >',bold=True))
    #loguer(env.level+' route code_edit() : >')
    # print()
    python_code = request.args.get('code')
    the_type = request.args.get('type')    
    if python_code=='route_def_.py':
        python_code='route_def_index.py'
    # print()
    # print(' python_code:\n',yellow(python_code,bold=True))
    # print()  
    # print()
    # print(' the_type :\n',yellow(the_type,bold=True))
    # print() 
    if the_type=='function':
        filename=f'./code_app_functions/{python_code}'  
    elif the_type=='route':
        filename=f'./code_app_routes/{python_code}' 
    else:
        filename=f'./code_app_html_templates/{python_code}'
    filename=filename.replace('/.','/')
    # print()
    # print(' filename :',yellow(filename,bold=True))
    # print()      
    with open(filename) as file:
        code=file.read()
    env.level=env.level[:-1]
    return render_template("./code_editor.html",code=code,fichier=filename,the_type=the_type)



# def_code_edit_B***
@app.route('/code_edit_B', methods=['GET','POST'])
def code_edit_B():
    env.level+='-'
    # print()
    # print(env.level,white('route code_edit_B() : >',bold=True))
    #loguer(env.level+' route code_edit_B() : >')
    # print()
    python_code = request.args.get('code')
    subdir = request.args.get('subdir')    
    if python_code=='route_def_.py':
        python_code='route_def_home.py'
    # print()
    # print(' python_code:\n',yellow(python_code,bold=True))
    # print()  
    # print()
    # print(' subdir :\n',yellow(subdir,bold=True))
    # print() 
    filename=f'./code_app_scripts_to_import/{subdir}/{python_code}'  
    filename=filename.replace('/.','/')
    if os.path.exists(filename):    
        with open(filename) as file:
            code=file.read()
        env.level=env.level[:-1]
        return render_template("./code_editor_B.html",code=code,fichier=filename,subdir=subdir,python_code=python_code)
    else:
        with open('./result/home_url.txt') as file:
            home_url=file.read()    
        html_output='''<html><body><a href="'''+home_url+'''"><b><= back to home</b></a><br><br>
        <center><h3>This file does not exist anymore</h3></center>
        </body></html>
        ''';                
        env.level=env.level[:-1]
        return html_output 
    
    


# def_goto_script_B***
@app.route('/goto_script_B', methods=['GET'])
def goto_script_B():
    '''
        modified : 20250709
        menu for imported scripts
    '''
    env.level+='-'
    # print()
    # print(env.level,white('route goto_script_B() : >',bold=True))
    #loguer(env.level+' route goto_script_B() : >')
    # print()
    scriptdir = request.args.get('script')
    with open('./result/selected_script.txt','w') as file:
        file.write(scriptdir)
    fichier=scriptdir
    with open('./result/current_edited_script.txt') as file:
        last_edited_script=file.read()    
    with open('./result/current_edited_imported_script.txt','w') as file:
        file.write(fichier)
    scriptdir=scriptdir.replace('.py','')
    # print()
    # print(' scriptdir :\n',yellow(scriptdir,bold=True))
    # print()      
    with open('./result/home_url.txt') as file:
        home_url=file.read()
    with open('./result/selected_script_working_dir.txt') as file:
        workingdir=file.read()    
    '''
    with open(scriptdir+'/build_location.txt','w') as file:
        workingdir=file.read()     
    '''      
    #html_output='<html><body><a href="'+home_url+'"><b><= back to home</b></a><br><br><b><a href="/new_script_function?scriptdir='+scriptdir+'">Create a new function for [ '+scriptdir+'.py ]</a></b><br><b><a href="/new_script_route?scriptdir='+scriptdir+'">Create a new route for [ '+scriptdir+'.py ]</a></b><br><br>script working directory is : <br><b>'+workingdir+'</b><a href="/change_script_working_directory"><b>...( modify )</b></a></b><br><br><a href="/compile_script?code='+fichier+'&subdir='+scriptdir+'"><b>Compile Script</b></a></b>';
    html_output='<html><body><a href="'+home_url+'"><b><= back to home</b></a><h2>[ '+scriptdir+'.py ]</h2><b><a href="/new_script_function?scriptdir='+scriptdir+'">Create a new function</a>....<a href="/new_function_from_library_B?script='+fichier+'&scriptdir='+scriptdir+'">Add a new function from library</a></b><br><b><a href="/new_script_route?scriptdir='+scriptdir+'">Create a new route</a>....<a href="/new_route_from_library_B?script='+fichier+'&scriptdir='+scriptdir+'">Add a new route from library</a></b><br><br><a href="/compile_script?code='+fichier+'&subdir='+scriptdir+'"><b>Compile Script</b></a> In working directory : <br><b>'+workingdir+'</b><a href="/change_script_working_directory"><b>-( change )</b></a></b><br><br>'
    html_output=html_output+'<b><a href="/code_edit_B?code='+last_edited_script+'&subdir='+scriptdir+'">Last edited : '+last_edited_script+'</a>.---.<a href="/edit_html?filename=../code_app_scripts_to_import/'+scriptdir+'/'+last_edited_script+'">( open in notepad++ )</a></b>'
    html_output=html_output+'<h3>Edit a core chunks</h3><ul>'
    files =[file for file in os.listdir('./code_app_scripts_to_import/'+scriptdir)]
    ii=0
    #function_list=[]
    html_output=html_output+'<li><b><a href="/code_edit_B?code=a_main.txt&subdir='+scriptdir+'">a_main.txt</a>.---.<a href="/edit_html?filename=../code_app_scripts_to_import/'+scriptdir+'/a_main.txt">( open in notepad++ )</a></b></li><li></li><li><b><a href="/code_edit_B?code=a_header.txt&subdir='+scriptdir+'">a_header.txt</a>.---.<a href="/edit_html?filename=../code_app_scripts_to_import/'+scriptdir+'/a_header.txt">( open in notepad++ )</a></b></li><li><b><a href="/code_edit_B?code=a_imports.txt&subdir='+scriptdir+'">a_imports.txt</a>.---.<a href="/edit_html?filename=../code_app_scripts_to_import/'+scriptdir+'/a_imports.txt">( open in notepad++ )</a></b></li><li><b><a href="/code_edit_B?code=a_global_variables.txt&subdir='+scriptdir+'">a_global_variables.txt</a>.---.<a href="/edit_html?filename=../code_app_scripts_to_import/'+scriptdir+'/a_global_variables.txt">( open in notepad++ )</a></b></li><li><b><a href="/code_edit_B?code=script_functions.txt&subdir='+scriptdir+'">script_functions.txt</a>.---.<a href="/edit_html?filename=../code_app_scripts_to_import/'+scriptdir+'/script_functions.txt">( open in notepad++ )</a></b></li><li><b><a href="/code_edit_B?code=script_routes.txt&subdir='+scriptdir+'">script_routes.txt</a>.---.<a href="/edit_html?filename=../code_app_scripts_to_import/'+scriptdir+'/script_routes.txt">( open in notepad++ )</a></b></li><li><b><a href="/code_edit_B?code=./package_dev/z_init_appli.py&subdir='+scriptdir+'">z_init_appli.py</a>.---.<a href="/edit_html?filename=../code_app_scripts_to_import/'+scriptdir+'/package_dev/z_init_appli.py">( open in notepad++ )</a></b></li><li><b><a href="/code_edit_B?code=./package_dev/requirements.txt&subdir='+scriptdir+'">requirements.txt</a>.---.<a href="/edit_html?filename=../code_app_scripts_to_import/'+scriptdir+'/package_dev/requirements.txt">( open in notepad++ )</a></b></li>'
    '''
    for file in files:
        if 'route_' not in file and 'a_core_' not in file and file !='back' and '.txt' in file:
            print(' file : ',yellow(file,bold=True)) 
            html_output=html_output+'<li><b><a href="/code_edit_B?code='+file+'&subdir='+scriptdir+'">'+file+'</a>.---.<a href="/edit_html?filename=../code_app_scripts_to_import/'+scriptdir+'/'+file+'">( open in notepad++ )</a></b></li>'
    '''
    html_output=html_output+'</ul><h3>Edit a function</h3><table border="1"><tbody>';
    for file in files:
        if 'route_' not in file and file !='back' and '.py' in file:
            # print(' file : ',yellow(file,bold=True)) 
            html_output=html_output+'<tr><td><b><a href="/code_edit_B?code='+file+'&subdir='+scriptdir+'">'+file+'</a></td><td><a href="/edit_html?filename=../code_app_scripts_to_import/'+scriptdir+'/'+file+'">( open in notepad++ )</a></b></td><td><a href="/delete_file?filename=../code_app_scripts_to_import/'+scriptdir+'/'+file+'&scriptdir='+scriptdir+'">( DELETE )</a></b></td><td><a href="/rename_file?filename=../code_app_scripts_to_import/'+scriptdir+'/'+file+'&scriptdir='+scriptdir+'">( RENAME )</a></b></td><td><a href="/copy_function_to_central_B?filename=./code_app_scripts_to_import/'+scriptdir+'/'+file+'&scriptdir='+scriptdir+'">( cp 2 central )</a></b></td></td><td><a href="/duplicate_script?filename='+file+'&scriptdir='+scriptdir+'&type=function">(duplicate)</a></b></td><tr>' 
            
    html_output=html_output+'</tbody></table><h3>Edit a route</h3><table border="1"><tbody>';
    for file in files:
        if 'route_' in file and file !='back' and '.py' in file:
            # print(' file : ',yellow(file,bold=True)) 
            html_output=html_output+'<tr><td><b><a href="/code_edit_B?code='+file+'&subdir='+scriptdir+'">'+file+'</a></b></td><td><a href="/edit_html?filename=../code_app_scripts_to_import/'+scriptdir+'/'+file+'">( open in notepad++ )</a></b></td><td><a href="/delete_file?filename=../code_app_scripts_to_import/'+scriptdir+'/'+file+'&scriptdir='+scriptdir+'">( DELETE )</a></b></td><td><a href="/rename_file?filename=../code_app_scripts_to_import/'+scriptdir+'/'+file+'&scriptdir='+scriptdir+'">( RENAME )</a></b></td><td><a href="/copy_route_to_central_B?filename=./code_app_scripts_to_import/'+scriptdir+'/'+file+'&scriptdir='+scriptdir+'">( cp 2 central )</a></b></td><td><a href="/duplicate_script?filename='+file+'&scriptdir='+scriptdir+'&type=route">(duplicate)</a></b></td><tr>'            
    html_output=html_output+'</tbody></table>';            
    env.level=env.level[:-1]
    return html_output
        



#  def_new_script_to_import***
@app.route('/new_script_to_import', methods=['GET','POST'])
def route_def_new_script_to_import():
    '''
    MODIFIED : 20250507
    display formular for create a new script to import  
    '''
    env.level+='-'
    print()
    print(env.level,white('route new_script_to_import() : >',bold=True))
    loguer(env.level+' route new_script_to_import() : >')
    print()
    with open('./result/home_url.txt') as file:
        home_url=file.read()
    html_output='''<html><body><a href="'''+home_url+'''"><b><= back to home</b></a><br><br>
    <form action="/new_script_to_import_create" method="GET">
    <b>script name : </b><input type="text"  id="script_name" name="name" /><br><br>
    <b>script description</b><br>
    <textarea id="description" name="description" rows="5" cols="50"></textarea><br><br>
    <center><input type="submit" value="valid"/></center>
    </form>
    </body></html>
    ''';   
    env.level=env.level[:-1]
    return html_output 


# def_new_script_to_import_create***
@app.route('/new_script_to_import_create', methods=['GET','POST'])
def new_script_to_import_create():
    env.level+='-'
    print()
    print(env.level,white('route new_script_to_import_create() : >',bold=True))
    loguer(env.level+' route new_script_to_import_create() : >')
    print()
    '''
    Modified : 20251001
    
    create a new external python script to import ase a resource to the main script
    '''    
    filename = request.args.get('name')
    if '.py' not in filename:
        filename=filename+'.py'
    filename=filename.replace('-','_')
    filename=filename.replace(' ','_')        
    description = request.args.get('description')
    print()
    print(' filename :\n',yellow(filename,bold=True))
    print()
    print(' description :\n',yellow(description,bold=True))
    print()
    with open('./code_architecture/imported_scripts.txt') as file:
        text_content=file.read()    
    if filename in text_content:
        print(filename+' already exists ! Choose another name')
        html_output='''<html><body>
        <center><h3>This script already exists ! choose another name</h3></center>
    <form action="/new_script_to_import_create" method="GET">
    <b>script name : </b><input type="text"  id="script_name" name="name" /><br><br>
    <b>script description</b><br>
    <textarea id="description" name="description" rows="5" cols="50"></textarea><br><br>
    <center><input type="submit" value="valid"/></center>
    </form>        
        </body></html>
        ''';        
    else:
        print(yellow(f'     {filename} does NOT exists. Let s create it',bold=True))
        with open('./code_architecture/imported_scripts.txt','a+') as file:
            file.write(filename+'\n')          
        # create a sub durectory
        subdir='./code_app_scripts_to_import/'+filename.replace('.py','')
        os.mkdir(subdir)
        os.mkdir(subdir+'/package_dev') 
        os.mkdir(subdir+'/package_dev/debug')      
        os.mkdir(subdir+'/package_dev/temp')        
        os.mkdir(subdir+'/package_dev/output')
        os.mkdir(subdir+'/package_dev/result')
        os.mkdir(subdir+'/package_prod')    
        os.mkdir(subdir+'/package_prod/debug')
        os.mkdir(subdir+'/package_prod/temp')
        os.mkdir(subdir+'/package_prod/output')      
        os.mkdir(subdir+'/package_prod/result')        
        with open(subdir+'/a_imports.txt','w') as file:
            line_out="import env as env\nfrom crayons import *\nfrom analyse_application_logs import loguer\n"
            file.write(line_out)
        with open(subdir+'/a_global_variables.txt','w') as file:
            file.write('')  
        with open(subdir+'/script_functions.txt','w') as file:
            file.write('')   
        with open(subdir+'/script_routes.txt','w') as file:
            file.write('')              
        with open(subdir+'/a_header.txt','w') as file:
            line_out="# -*- coding: UTF-8 -*-\n#!/usr/bin/env python\n'''\n    description : "
            line_out=line_out+description+"\n'''"
            file.write(line_out)             
        with open(subdir+'/a_main.txt','w') as file:
            line_out='if __name__=="__main__":\n    print(env.level,white("MAIN FUNCTION ( the application starts here ): >",bold=True))\n    with open("./debug/log.txt","w") as file:\n        pass\n    loguer(env.level+" APPLICATION STARTS")'    
            file.write(line_out)     
        with open(subdir+'/build_location.txt','w') as file:
            file.write(subdir+'/package_dev')     
 
        with open(subdir+'/package_dev/result/home_url.txt','w') as file:
            pass 
        with open(subdir+'/package_prod/result/home_url.txt','w') as file:
            pass 
        with open(subdir+'/package_dev/env.py','w') as file:
            file.write('level="["')
        with open(subdir+'/package_prod/env.py','w') as file:
            file.write('level="["')         
            
        with open('./result/home_url.txt') as file:
            home_url=file.read()
            print()
            print('home_url',home_url)
            print()
            
        with open("./analyse_application_logs.py") as file:
            text_content=file.read()
        text_content=text_content.replace("app.py",filename)
        with open(subdir+'/package_dev/analyse_application_logs.py','w') as file:
            file.write(text_content)
        with open(subdir+'/package_prod/analyse_application_logs.py','w') as file:
            file.write(text_content)        
            
        with open("./code_templates/z_init_appli.py") as file:
            text_content=file.read()
        text_content=text_content.replace("app.py",filename)
        with open(subdir+'/package_dev/z_init_appli.py','w') as file:
            file.write(text_content)
        with open(subdir+'/package_prod/z_init_appli.py','w') as file:
            file.write(text_content)     
        with open(subdir+'/package_dev/a.bat','w') as file:
            file.write("python -m venv venv")     
        with open(subdir+'/package_dev/b.bat','w') as file:
            file.write("venv\\scripts\\activate")    
        with open(subdir+'/package_dev/c.bat','w') as file:
            file.write("pip install -r requirements.txt")      
        with open(subdir+'/package_dev/d.bat','w') as file:
            file.write("venv\\scripts\\deactivate")    
        with open(subdir+'/package_dev/e.bat','w') as file:
            file.write("python z_init_appli.py")   
        with open(subdir+'/package_dev/requirements.txt','w') as file:
            file.write("crayons==0.4.0\nrequests==2.32.3")
        with open(subdir+'/package_prod/a.bat','w') as file:
            file.write("python -m venv venv")     
        with open(subdir+'/package_prod/b.bat','w') as file:
            file.write("venv\\scripts\\activate")    
        with open(subdir+'/package_prod/c.bat','w') as file:
            file.write("pip install -r requirements.txt")      
        with open(subdir+'/package_prod/d.bat','w') as file:
            file.write("venv\\scripts\\deactivate")    
        with open(subdir+'/package_prod/e.bat','w') as file:
            file.write("python z_init_appli.py")  
        with open(subdir+'/package_prod/requirements.txt','w') as file:
            file.write("crayons==0.4.0\nrequests==2.32.3")            
        html_output='<html><body><a href="'
        html_output=html_output+home_url
        html_output=html_output+'"><b><= back to home</b></a><br><br>\n<center><h3>script '
        html_output=html_output+filename
        html_output=html_output+' created</h3></center>\n </body></html>'             
    env.level=env.level[:-1]
    return html_output  


# def_list_external_scripts_B***
@app.route('/list_external_scripts', methods=['GET','POST'])
def list_external_scripts():
    '''
        version : 20250929
    '''
    env.level+='-'
    # print()
    # print(env.level,white('route list_external_scripts() : >',bold=True))
    #loguer(env.level+' route list_external_scripts() : >')
    # print()
    with open('./result/home_url.txt') as file:
        home_url=file.read()
    with open('./result/current_edited_imported_script.txt') as file:
        last_edited_script=file.read()  
    html_output='<html><body><a href="'+home_url+'"><b><= back to home</b></a><br><br><a href="/goto_script_B?script='+last_edited_script+'&type=route">Last Edited :'+last_edited_script+'</a><br><a href="/new_script_to_import">Create a new script</a><br><a href="edit_html?filename=../code_architecture/imported_scripts.txt">Edit the list ( notepad++ )</a><br><br><b><u>DELETE A SCRIPT :</u> remove the script name from the list ( link above : ./code_architecture/imported_scripts.txt )  and manually delete the directory structure in ./code_app_scripts_to_import.</b><h3>Select a script</h3><ul>';
    with open('./code_architecture/imported_scripts.txt') as file:
        for line in file:
            # print(' file : ',yellow(line,bold=True)) 
            html_output=html_output+'<li><b><a href="/goto_script_B?script='+line+'&type=route">'+line+'</a></b></li>'
    env.level=env.level[:-1]
    html_output=html_output+'\n</ul></body><html>'
    return html_output
    



# def_goto_script***
@app.route('/goto_script', methods=['GET'])
def goto_script():
    env.level+='-'
    # print()
    # print(env.level,white('route goto_script() : >',bold=True))
    #loguer(env.level+' route goto_script() : >')
    # print()
    scriptdir = request.args.get('script')
    scriptdir=scriptdir.replace('.py','')
    # print()
    # print(' scriptdir :\n',yellow(scriptdir,bold=True))
    # print()    
    with open('./result/home_url.txt') as file:
        home_url=file.read()
    html_output='<html><body><a href="'+home_url+'"><b><= back to home</b></a><br><br><b><a href="/new_script_function_create?scriptdir='+scriptdir+'">Create a new function for [ '+scriptdir+'.py ]</a></b><h3>Edit a score chunks</h3><ul>';
    files =[file for file in os.listdir('./code_app_scripts_to_import/'+scriptdir)]
    ii=0
    function_list=[]
    for file in files:
        if 'route_' not in file and 'a_core_' not in file and file !='back':
            # print(' file : ',yellow(file,bold=True)) 
            html_output=html_output+'<li><b><a href="/code_edit?code=.../code_app_scripts_to_import/'+scriptdir+'/'+file+'&type=function">'+file+'</a>.---.<a href="/edit_html?filename=../code_app_scripts_to_import/'+scriptdir+'/'+file+'">( open in notepad++ )</b></li>'
    html_output=html_output+'<h3>Edit a route</h3>';
    html_output=html_output+'<h3>Edit a function</h3>';
    env.level=env.level[:-1]
    return html_output
        



# def_new_script_function***
@app.route('/new_script_function', methods=['GET','POST'])
def new_script_function():
    '''
    MODIFIED 20250605
    
    display formular for create a new_script_function of an external script
    '''
    env.level+='-'
    print()
    print(env.level,white('route new_script_function() : >',bold=True))
    loguer(env.level+' route new_script_function() : >')
    print()
    scriptdir = request.args.get('scriptdir')
    print()
    print(' scriptdir:\n',yellow(scriptdir,bold=True))
    print()      
    with open('./result/home_url.txt') as file:
        home_url=file.read()
    html_output='''<html><body><a href="'''+home_url+'''"><b><= back to home</b></a><center><h3>new function for [ '''+scriptdir+'''.py ]</h3></center>
    <form action="/new_script_function_create" method="GET">
    <b>function name : </b><input type="text"  id="function_name" name="name" />-- Args :<input type="text"  id="args" name="args" value="()"/><br><br>
    <b>Function description</b><br>
    <textarea id="description" name="description" rows="5" cols="50"></textarea><br><br>
    <input type="hidden"  id="scriptdir" name="scriptdir" value="'''+scriptdir+'''"/>
    <center><input type="submit" value="create"/></center>
    </form>
    </body></html>
    ''';   
    env.level=env.level[:-1]
    return html_output
    
    


#  def_new__script_function_create***
@app.route('/new_script_function_create', methods=['GET','POST'])
def new__script_function_create():
    '''
    Modified : 20251001
    
    create a new function for the selected imported script
    '''
    env.level+='-'
    print()
    print(env.level,white('route new__script_function_create() : >',bold=True))
    loguer(env.level+' route new__script_function_create() : >')
    print()
    scriptdir= request.args.get('scriptdir')    
    name = request.args.get('name')
    name=name.replace('-','_')
    name=name.replace(' ','_')    
    args = request.args.get('args')    
    description = request.args.get('description')

    filename='./code_app_scripts_to_import/'+scriptdir+'/def_'+name+'.py'
    filename2='/def_'+name+'.py'

    print()
    print(' filename :\n',yellow(filename,bold=True))
    print()
    print()
    print(' filename2 :\n',yellow(filename2,bold=True))
    print()
    print(' description :\n',yellow(description,bold=True))
    print()
    print()
    print(' scriptdir :\n',yellow(scriptdir,bold=True))
    print()    
    with open('./result/home_url.txt') as file:
        home_url=file.read()
    # check if file already exits 
    '''
    fichier_function = Path(filename)    
    fichier_function = filename
    '''
    fichier_route = Path(filename)
    if fichier_route.is_file():  
        print(filename+' already exists ! Choose another name')
        html_output='''<html><body><a href="'''+home_url+'''"><b><= back to home</b></a><center><h3>new function for [ '''+scriptdir+'''.py ]</h3></center>
    <form action="/new_script_function_create" method="GET">
    <b>function name : </b><input type="text"  id="function_name" name="name" />-- Args :<input type="text"  id="args" name="args" value="()"/><br><br>
    <b>Function description</b><br>
    <textarea id="description" name="description" rows="5" cols="50"></textarea><br><br>
    <input type="hidden"  id="scriptdir" name="scriptdir" value="'''+scriptdir+'''"/>
    <center><input type="submit" value="create"/></center>
    </form>
    </body></html>
    ''';         
    else:
        print(yellow(f'     {filename} does NOT exists. Let s create it',bold=True))
        with open('./code_templates/function_template.py') as file:
            text_content=file.read()
        text_content=text_content.replace('example_name',name)
        version='MODIFIED : '+current_date_and_time_for_json_data()+'\n\n    description : '
        description=version+description
        text_content=text_content.replace('***description***',description) 
        text_content=text_content.replace('***app.py***',scriptdir+'.py')
        text_content=text_content.replace('(args)',args)        
        with open(filename,"w") as fichier:
            fichier.write(text_content)     
        with open(f'./code_app_scripts_to_import/{scriptdir}/script_functions.txt',"a+") as fichier:
            filename2=filename2.replace('/','')
            fichier.write(filename2+'\n')  
        html_output='''<html><body><a href="'''+home_url+'''"><b><= back to home</b></a><br><br>
        <center><h3>function created</h3></center>
        <center><h3><a href="/code_edit_B?code='''+filename2+'''&subdir='''+scriptdir+'''">EDIT in inline editor :'''+filename2+'''</a>. OR .<a href="/edit_html?filename=.'''+filename+'''">( Edit in notepad++ )</a></center><hr><br><b><a href="/new_script_function?scriptdir='''+scriptdir+'''">Create a new function for [ '''+scriptdir+'''.py ]</a></b><br><b><a href="/new_script_route?scriptdir='''+scriptdir+'''">Create a new route for [ '''+scriptdir+'''.py ]</a></b>
        </body></html>
        ''';       
    with open('./result/current_edited_script.txt',"w") as file:
        file.write(filename2)          
    env.level=env.level[:-1]
    return html_output   
    
    


#  def_list_system_scripts***
@app.route('/list_system_scripts', methods=['GET'])
def list_system_scripts():
    '''
    Created : 2025-08-01

    description : go to the menu for editing system scripts
    '''
    route="/list_system_scripts"
    env.level+='-'
    # print()
    # print(env.level,white('route list_system_scripts() in ***app.py*** : >',bold=True))
    #loguer(env.level+' route list_system_scripts() in ***app.py*** : >')
    # print()
    last_script=''
    with open('./result/home_url.txt') as file:
        home_url=file.read()
    if os.path.exists('./result/keyword.txt'):
        with open('./result/keyword.txt') as file:
            keyword=file.read()         
    html_output='<html><body><a href="'+home_url+'"><b><= back to home</b></a><br><br><form action="/search_system_script" method="get"><input type="text" name="keyword" value="'+keyword+'"><input type="submit" value="Search"></form><br>';        

    html_output=html_output+'<h4>System Route :</h4><table border="1"><tbody>';
    
    
    #html_output=html_output+'<h3>Edit a system route</h3><ul>';
    files =[file for file in os.listdir('./code_system_routes')]    
    for file in files:
        if 'route_' in file and file !='back' and '.py' in file:
            # print(' file : ',yellow(file,bold=True)) 
            html_output=html_output+'<tr><td><b><a href="/edit_html?filename=../code_system_routes/'+file+'">'+file+' ( open in notepad++ )</a></b></td><td><a href="/duplicate_system_route?filename='+file+'">(duplicate in app routes)</a></b></td></tr>'    
    html_output=html_output+'</tbody></table><h4>System Functions :</h4><table border="1"><tbody>';
    files =[file for file in os.listdir('./code_system_functions')]     
    for file in files:
        if 'route_' not in file and file !='back' and '.py' in file:
            # print(' file : ',yellow(file,bold=True)) 
            html_output=html_output+'<tr><td><b><a href="/edit_html?filename=../code_system_functions/'+file+'">'+file+' ( open in notepad++ )</a></b></td><td><a href="/duplicate_system_function?filename='+file+'">(duplicate in app functions)</a></b></td></tr>' 
    html_output=html_output+'</tbody></table><br><a href="/stop">Click here to stop the App  </a></body></html>';            
    env.level=env.level[:-1]
    return html_output


#  def_delete_file***
@app.route('/delete_file', methods=['GET'])
def delete_file():
    '''
    Created : 2025-06-05T09:07:30.000Z

    description : go to delete file confirmation formular
    '''
    route="/delete_file"
    env.level+='-'
    print()
    print(env.level,white('route delete_file() in ***app.py*** : >',bold=True))
    loguer(env.level+' route delete_file() in ***app.py*** : >')
    print()
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        filename=request.args.get('filename')
        filename=filename.replace('../','./')
        print()
        print('filename : ',filename)
        print()
        scriptdir=request.args.get('scriptdir')
        print()
        print('scriptdir : ',scriptdir)
        print()        
        html_output=f'<h3>Do you really want to delete : <br><br>{filename}</h3><br>in directory <b>[ {scriptdir} ]</b><br><hr>';
        html_output=html_output+f'<form action="/ok_delete_file" method="GET"><input type="hidden" name="filename" value="{filename}"><input type="hidden" name="scriptdir" value="{scriptdir}"><input type="submit" value="YES I DO"></form>'
        env.level=env.level[:-1]
        return html_output        



#  def_ok_delete_file***
@app.route('/ok_delete_file', methods=['GET'])
def ok_delete_file():
    '''
    Created : 2025-07-25

    description : Delete script as confirmation had been given
    '''
    route="/ok_delete_file"
    env.level+='-'
    print()
    print(env.level,white('route ok_delete_file() in ***app.py*** : >',bold=True))
    loguer(env.level+' route ok_delete_file() in ***app.py*** : >')
    print()
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        filename=request.args.get('filename')       
        print()
        print('filename path : ',filename)  
        print()          
        scriptdir=request.args.get('scriptdir')
        print()
        print('scriptdir : ',scriptdir)
        print()    
        if os.path.exists(filename):
            print(' ok delete',filename)
            os.remove(filename)            
        if scriptdir=='code_app_routes':
            filename=filename.replace('./code_app_routes/','')        
            print()
            print('filename : ',filename)  
            print()          
            function_file='./code_architecture/app_routes.txt'
        elif scriptdir=='code_app_functions':
            filename=filename.replace('./code_app_functions/','')        
            print()
            print('filename : ',filename)  
            print()           
            function_file='./code_architecture/app_functions.txt'         
        elif scriptdir=='code_app_html_templates':
            filename=filename.replace('./code_app_html_templates/','')        
            print()
            print('filename : ',filename)  
            print()           
            function_file='./code_architecture/main_html.txt'            
        else:
            chemin='./code_app_scripts_to_import/'+scriptdir+'/'
            filename=filename.replace(chemin,'')        
            print()
            print('filename : ',filename)  
            print()          
            if 'route_def' in filename:            
                function_file='./code_app_scripts_to_import/'+scriptdir+'/script_routes.txt'
            else:
                function_file='./code_app_scripts_to_import/'+scriptdir+'/script_functions.txt'            
        print()
        print('architecture file to update : ',function_file)  
        print()
        with open(function_file) as file:
            text_content=file.read()        
        text_content=text_content.replace(filename,'')    
        text_content=text_content.replace('\n\n','\n')
        with open(function_file,'w') as file:      
            file.write(text_content)
        with open('./result/home_url.txt') as file:
            home_url=file.read()            
        html_output='<html><body><b><a href="'+home_url+'"><= back to home</b></a><br><br><h3>Script : '+filename+' Deleted</h3><a href="/stop">Click here to stop the App  </a></body></html>';             
    env.level=env.level[:-1]
    return html_output  
        



#  def_rename_file***
@app.route('/rename_file', methods=['GET'])
def rename_file():
    '''
    Created : 2025-06-05T13:50:52.000Z

    description : got to rename script formular
    '''
    route="/rename_file"
    env.level+='-'
    print()
    print(env.level,white('route rename_file() in ***app.py*** : >',bold=True))
    loguer(env.level+' route rename_file() in ***app.py*** : >')
    print()
    global client_id
    global client_password
    global host
    global host_for_token
    global profil_name
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        filename=request.args.get('filename')
        filename=filename.replace('../','./')
        print()
        print('filename : ',filename)
        print()
        scriptdir=request.args.get('scriptdir')
        print()
        print('scriptdir : ',scriptdir)
        print()        
        html_output=f'<h3>Do you really want to rename : <br><br>{filename}</h3><br>in directory <b>[ {scriptdir} ]</b><br><hr>';
        html_output=html_output+f'<form action="/ok_rename_file" method="GET"><input type="text" name="new_name"><input type="hidden" name="filename" value="{filename}"><input type="hidden" name="scriptdir" value="{scriptdir}"><input type="submit" value="Rename"></form>'
        env.level=env.level[:-1]
        return html_output     


#  def_ok_rename_file***
@app.route('/ok_rename_file', methods=['GET'])
def ok_rename_file():
    '''
    Created : 2025-08-01

    description : Rename the selected script as it was confirmed prior
    '''
    route="/ok_rename_file"
    env.level+='-'
    print()
    print(env.level,white('route ok_rename_file() in ***app.py*** : >',bold=True))
    loguer(env.level+' route ok_rename_file() in ***app.py*** : >')
    print()
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        filepath=request.args.get('filename')       
        print()
        print('filename path : ',filepath)  
        print()          
        scriptdir=request.args.get('scriptdir')
        print()
        print('scriptdir : ',scriptdir)
        print()    
        new_name=request.args.get('new_name')
        if scriptdir=='code_app_html_templates':        
            if 'z_' not in new_name:
                new_name='z_'+new_name       
            if '.html' not in new_name:
                new_name=new_name+'.html'         
        print()
        print('new_name : ',new_name)
        print()     
        if '.py' in new_name:
            new_name=new_name.replace('.py','')           
        if scriptdir=='code_app_routes':
            filename=filepath.replace('./code_app_routes/','')        
            print()
            print('app route filename : ',filename)  
            print()          
            if os.path.exists(filepath):
                print(' ok rewrite this file :',filepath,' to ',new_name+'.py')
                with open(filepath) as file:
                    text_content=file.read()
                mot=filename.replace('.py','')
                mot=mot.replace('route_def_','')
                print()
                print('replace : ',mot, ' by ',new_name)  
                print()                   
                text_content=text_content.replace(mot,new_name)
                new_name2='route_def_'+new_name+'.py'
                new_name3=new_name       
                print('name3 : ',cyan(new_name3+'\n',bold=True))
                with open('./code_app_routes/'+new_name2,'w') as file:
                    file.write(text_content)             
            function_file='./code_architecture/app_routes.txt'
        elif scriptdir=='code_app_functions':
            filename=filepath.replace('./code_app_functions/','')        
            print()
            print('app function filename : ',filename)  
            print()     
            if os.path.exists(filepath):
                print(' ok rewrite this file :',filepath,' to ',new_name+'.py')
                with open(filepath) as file:
                    text_content=file.read()
                mot=filename.replace('.py','')
                mot=mot.replace('def_','')
                print()
                print('replace : ',mot, ' by ',new_name)  
                print()                 
                text_content=text_content.replace(mot,new_name)
                new_name2='def_'+new_name+'.py'
                new_name3=new_name
                with open('./code_app_functions/'+new_name2,'w') as file:
                    file.write(text_content)             
            function_file='./code_architecture/app_functions.txt'         
        elif scriptdir=='code_app_html_templates':
            filename=filepath.replace('./code_app_html_templates/','')    
            print()
            print('html page filename to rename : ',filename)  
            print()     
            if os.path.exists(filepath):
                print(' ok rewrite this file :',filename,' to ',new_name+'.html')
                with open(filepath) as file:
                    text_content=file.read()
                print()
                print('replace : ',filename, ' by ',new_name)  
                print()                 
                text_content=text_content.replace(filename,new_name)
                new_name2=new_name # needed for architecture file update
                with open('./code_app_html_templates/'+new_name,'w') as file:
                    file.write(text_content)             
            function_file='./code_architecture/main_html.txt'    
            mot=filename            
        else:
            chemin='./code_app_scripts_to_import/'+scriptdir+'/'
            filename=filepath.replace(chemin,'')                     
            if 'route_def' in filename:     
                print()
                print('script route filename : ',filename)  
                print()              
                if os.path.exists(filepath):
                    print(' ok rewrite this file :',filepath,' to ',new_name+'.py')
                    with open(filepath) as file:
                        text_content=file.read()
                    mot=filename.replace('.py','')
                    mot=mot.replace('route_def_','')
                    print()
                    print('replace : ',mot, ' by ',new_name)  
                    print()                       
                    text_content=text_content.replace(mot,new_name)
                    new_name2='route_def_'+new_name+'.py'
                    new_name3=new_name                    
                    with open('./code_app_scripts_to_import/'+scriptdir+'/'+new_name2,'w') as file:
                        file.write(text_content)                
                function_file='./code_app_scripts_to_import/'+scriptdir+'/script_routes.txt'
            else:
                print()
                print('script function filename : ',filename)  
                print()             
                if os.path.exists(filepath):
                    print(' ok rewrite this file :',filepath,' to ',new_name+'.py')
                    with open(filepath) as file:
                        text_content=file.read()
                    mot=filename.replace('.py','')
                    mot=mot.replace('def_','')
                    print()
                    print('replace : ',mot, ' by ',new_name)  
                    print()                                           
                    text_content=text_content.replace(mot,new_name)
                    new_name2='def_'+new_name+'.py'
                    new_name3=new_name
                    with open('./code_app_scripts_to_import/'+scriptdir+'/'+new_name2,'w') as file:
                        file.write(text_content)               
                function_file='./code_app_scripts_to_import/'+scriptdir+'/script_functions.txt'                     
        print()
        print('architecture file : ',function_file)  
        print()
        with open(function_file) as file:
            text_content=file.read()        
        text_content=text_content.replace(mot,new_name3)    
        text_content=text_content.replace('\n\n','\n')
        with open(function_file,'w') as file:      
            file.write(text_content)
        if os.path.exists(filepath):
            print(' ok delete',filepath)
            os.remove(filepath)            
        with open('./result/home_url.txt') as file:
            home_url=file.read()            
        html_output='<html><body><b><a href="'+home_url+'"><= back to home</b></a><br><br><h3>Script : '+filename+' Renamed to '+new_name+'.py</h3><a href="/stop">Click here to stop the App  </a></body></html>';             
    env.level=env.level[:-1]
    return html_output  
        



#  def_compile_script***
@app.route('/compile_script', methods=['GET'])
def compile_script():
    '''
    Created : 2025-06-05T21:36:10.000Z

    description : create the selected external script
    '''
    route="/compile_script"
    env.level+='-'
    print()
    print(env.level,white('route compile_script() in ***app.py*** : >',bold=True))
    loguer(env.level+' route compile_script() in ***app.py*** : >')
    print()
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        scriptdir = request.args.get('subdir')
        print()
        print(' scriptdir :\n',yellow(scriptdir,bold=True))
        print()    
        code = request.args.get('code')
        print()
        print(' code :\n',yellow(code,bold=True))
        print()    
        os.system("python compile_script.py 1")
        with open('./result/home_url.txt') as file:
            home_url=file.read()    
        with open('./result/current_edited_imported_script.txt') as file:
            last_edited_script=file.read()             
        html_output='''<html><body><br><a href="'''+home_url+'''"><b><= back to home</b></a><br><br><a href="/goto_script_B?script='''+last_edited_script+'''&type=route">Go To Last edited</a><br>
        <center><h3>Script builted</h3></center>
        </body></html>
        ''';             
    env.level=env.level[:-1]
    return html_output 



#  def_compile_script_B***
@app.route('/compile_script_B', methods=['GET'])
def compile_script_B():
    '''
    Created : 2025-06-06T16:11:31.000Z

    description : create the selected application script
    '''
    route="/compile_script_B"
    env.level+='-'
    print()
    print(env.level,white('route compile_script_B() in ***app.py*** : >',bold=True))
    loguer(env.level+' route compile_script_B() in ***app.py*** : >')
    print()
    global client_id
    global client_password
    global host
    global host_for_token
    global profil_name
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        scriptdir = request.args.get('type')
        print()
        print(' type :\n',yellow(type,bold=True))
        print()    
        code = request.args.get('code')
        print()
        print(' code :\n',yellow(code,bold=True))
        print()    
        os.system("python compile.py 1")
        with open('./result/home_url.txt') as file:
            home_url=file.read()        
        html_output='''<html><body><a href="/code_edit?code='''+code+'''&type='''+type+'''"><b><= back to code</b></a><br><br><a href="'''+home_url+'''"><b><= back to home</b></a><br><br>
        <center><h3>Script builted</h3></center>
        </body></html>
        ''';             
    env.level=env.level[:-1]
    return html_output 
  


#  def_confirm_workingdir_change***
@app.route('/confirm_workingdir_change', methods=['GET'])
def confirm_workingdir_change():
    '''
    Created : 2025-06-07T14:29:14.000Z

    description : write the new directory in ./result/selected_script_working_dir.txt
    '''
    route="/confirm_workingdir_change"
    env.level+='-'
    print()
    print(env.level,white('route confirm_workingdir_change() in ***app.py*** : >',bold=True))
    loguer(env.level+' route confirm_workingdir_change() in ***app.py*** : >')
    print()
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        workingdir=request.args.get('directory')
        print()
        print('workingdir : ',workingdir)        
        with open('./result/selected_script_working_dir.txt','w') as file:
            file.write(workingdir)         
        with open('./result/home_url.txt') as file:
            home_url=file.read()
        html_output='''<html><body><a href="'''+home_url+'''"><b><= back to home</b></a><br><br>
        <center><h3>Script Destination Directory Updated</h3></center>
        </body></html>
        ''';             
    env.level=env.level[:-1]
    return html_output 


#  def_change_script_working_directory***
@app.route('/change_script_working_directory', methods=['GET'])
def change_script_working_directory():
    '''
    Created : 2025-06-07T14:25:35.000Z

    description : change the destination directory where to create the    script
    '''
    route="/change_script_working_directory"
    env.level+='-'
    print()
    print(env.level,white('route change_script_working_directory() in ***app.py*** : >',bold=True))
    loguer(env.level+' route change_script_working_directory() in ***app.py*** : >')
    print()
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        with open('./result/home_url.txt') as file:
            home_url=file.read()
        html_output='''<html><body><a href="'''+home_url+'''"><b><= back to home</b></a><br><br>
        <form action="/confirm_workingdir_change" method="GET">
        <b>Directory Name ( full path in disk ) : </b><input type="text"  id="directory" name="directory" /><br><br>
        <center><input type="submit" value="valid"/></center>
        </form>
        </body></html>
        ''';   
        env.level=env.level[:-1]
        return html_output


#  def_change_listening_port***
@app.route('/change_listening_port', methods=['GET'])
def change_listening_port():
    '''
    Created : 2025-07-20

    description : change the listening port of the application
    '''
    route="/change_listening_port"
    env.level+='-'
    print()
    print(env.level,white('route change_listening_port() in ***app.py*** : >',bold=True))
    loguer(env.level+' route change_listening_port() in ***app.py*** : >')
    print()
    global client_id
    global client_password
    global host
    global host_for_token
    global profil_name
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        with open('./result/home_url.txt') as file:
            home_url=file.read()
        with open('./port.txt') as file:
            port=file.read()
        with open('./server_ip_address.txt') as file:
            ip_address=file.read()              
        html_output='''<html><body><a href="'''+home_url+'''"><b><= back to home</b></a><br><br>
        <form action="/change_listening_port_confirmed" method="GET">
        <b>New Listening port number  : </b><input type="text"  id="new_port" name="new_port" value="'''+port+'''"/><br>
        <b>New Server IP address  : </b><input type="text"  id="new_ip_addr" name="new_ip_addr" value="'''+ip_address+'''"/><br>
        <center><input type="submit" value="valid"/></center>
        </form>
        </body></html>
        ''';   
        env.level=env.level[:-1]
        return html_output


#  def_change_listening_port_confirmed***
@app.route('/change_listening_port_confirmed', methods=['GET'])
def change_listening_port_confirmed():
    '''
    Created : 2025-07-20

    description : Ok change listening port confirmed, lets do it
    '''
    route="/change_listening_port_confirmed"
    env.level+='-'
    print()
    print(env.level,white('route change_listening_port_confirmed() in ***app.py*** : >',bold=True))
    loguer(env.level+' route change_listening_port_confirmed() in ***app.py*** : >')
    print()
    global client_id
    global client_password
    global host
    global host_for_token
    global profil_name
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        new_port=request.args.get('new_port')
        print()
        print('new_port : ',new_port)
        loguer(env.level+'- var Inputs : ???')
        loguer(env.level+'-- var new_port : '+new_port+' ???')
        new_ip_address=request.args.get('new_ip_addr')
        loguer(env.level+'-- var new_ip_address : '+new_ip_address+' ???')
        print()
        print('new_ip_address : ',new_ip_address)        
        with open('./code_system_main_blocs/a_core_main.py') as file:
            text_content=file.read()    
        text_content=text_content.replace('port=5000','port='+new_port)
        with open('./code_system_main_blocs/a_core_main.py','w') as file:
            file.write(text_content) 
        with open('./code_system_html_templates/code_editor.html') as file:
            text_content=file.read()    
        text_content=text_content.replace('5000/save_code',new_port+'/save_code')
        with open('./code_system_html_templates/code_editor.html','w') as file:
            file.write(text_content)
        with open('./code_system_html_templates/code_editor_B.html') as file:
            text_content=file.read()    
        text_content=text_content.replace('5000/save_code',new_port+'/save_code')
        with open('./code_system_html_templates/code_editor_B.html','w') as file:
            file.write(text_content)                             
        with open('./result/home_url.txt') as file:
            home_url=file.read()   
        with open('./port.txt','w') as file:
            file.write(new_port)         
        with open('./server_ip_address.txt','w') as file:
            file.write(new_ip_address)              
        html_output='''<html><body><a href="'''+home_url+'''"><b><= back to home</b></a><br><br>
        <center><h3>Ok Done New port is : '''+new_port+'''</h3></center>
        <b>Listening port had been changed into :<ul>
        <li>./code_system_main_blocs/a_core_main.py</li>
        <li>./code_system_html_templates/code_editor.html</li>
        <li>./code_system_html_templates/code_editor_B.html</li>        
        </ul>
        </b>
        <br><br><a href="/stop">Click here to stop the App  </a>
        </body></html>
        ''';        
    env.level=env.level[:-1]
    return html_output        



#  def_copy_function_to_central***
@app.route('/copy_function_to_central', methods=['GET'])
def copy_function_to_central():
    '''
    Created : 2025-08-23

    description : copy this function  to the central repo and make it re usable
    '''
    route="/copy_function_to_central"
    env.level+='-'
    print()
    print(env.level,white('route copy_function_to_central() in ***app.py*** : >',bold=True))
    loguer(env.level+' route copy_function_to_central() in ***app.py*** : >')
    print()
    global client_id
    global client_password
    global host
    global host_for_token
    global profil_name
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        filepath=request.args.get('filename')       
        print()
        print('filename path : ',filepath)  
        print()          
        scriptdir=request.args.get('scriptdir')
        print()
        print('scriptdir : ',scriptdir)
        print()    
        new_name=filepath.replace('code_app_functions','code_central_functions')
        script_date = datetime.utcnow().strftime("%Y-%m-%d")
        new_name=new_name.replace('.py','_v'+script_date+'.py')        
        print()
        print('new_name : ',new_name)
        print()        
        print(' ok copy this file :',filepath,' to ',new_name+'.py')
        with open(filepath) as file:
            text_content=file.read()        
        lines=text_content.split('\n')
        output_lines=''
        for line in lines:
            print('line :' ,cyan(line,bold=True))
            if "print(env.level,white(" in line or "print('\\n'+env.level,white(" in line:
                print('line :',red(line,bold=True))
                chunks=line.split(') in ')
                line=chunks[0]+") in app.py  : >\\n',bold=True))"
                print('TO line :',green(line,bold=True))
            if "loguer(env.level+" in line:
                print('line :',red(line,bold=True))
                chunks=line.split(') in ')
                line=chunks[0]+") in app.py  : > ')"
                print('TO line :',green(line,bold=True))                 
            output_lines=output_lines+line+'\n'           
        with open(new_name,'w') as file:
            file.write(output_lines)      
        scriptname=filepath.replace('./code_app_functions/','')    
        print()
        print('scriptname : ',scriptname)
        print()         
        function_file='./code_central_functions/central_functions.txt'

        if '.py' in scriptname:
            pass
        else:
            scriptname=scriptname+'.py'
        if os.path.exists(function_file):
            with open(function_file) as file:
                text_content=file.read()        
            if  scriptname not in text_content:            
                with open(function_file,'a+') as file:      
                    file.write(scriptname+'\n')
        else:
            with open(function_file,'w') as file:      
                file.write(scriptname+'\n')  
         
        with open('./result/home_url.txt') as file:
            home_url=file.read()            
        html_output='<html><body><b><a href="'+home_url+'"><= back to home</b></a><br><br><h3>Ok route script had been moved to system</h3><a href="/stop">Click here to stop the App  </a></body></html>';             
    env.level=env.level[:-1]
    return html_output  
  


#  def_copy_route_to_central***
@app.route('/copy_route_to_central', methods=['GET'])
def copy_route_to_central():
    '''
    Created : 2025-06-14

    description : copy this route to the central repo to make it reusable
    '''
    route="/copy_route_to_central"
    env.level+='-'
    print()
    print(env.level,white('route copy_route_to_central() in ***app.py*** : >',bold=True))
    loguer(env.level+' route copy_route_to_central() in ***app.py*** : >')
    print()
    global client_id
    global client_password
    global host
    global host_for_token
    global profil_name
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        filepath=request.args.get('filename')       
        print()
        print('filename path : ',filepath)  
        print()          
        scriptdir=request.args.get('scriptdir')
        print()
        print('scriptdir : ',scriptdir)
        print()    
        new_name=filepath.replace('code_app_routes','code_central_routes')
        script_date = datetime.utcnow().strftime("%Y-%m-%d")
        new_name=new_name.replace('.py','_v'+script_date+'.py')        
        print()
        print('new_name : ',new_name)
        print()        
        print(' ok copy this file :',filepath,' to ',new_name+'.py')
        with open(filepath) as file:
            text_content=file.read()    
        lines=text_content.split('\n')
        output_lines=''
        for line in lines:
            print('line :' ,cyan(line,bold=True))
            if "print(env.level,white(" in line or "print('\\n'+env.level,white(" in line:
                print('line :',red(line,bold=True))
                chunks=line.split(') in ')
                line=chunks[0]+") in app.py  : >\\n',bold=True))"
                print('TO line :',green(line,bold=True))
            if "loguer(env.level+" in line:
                print('line :',red(line,bold=True))
                chunks=line.split(') in ')
                line=chunks[0]+") in app.py  : > ')"
                print('TO line :',green(line,bold=True))                
            output_lines=output_lines+line+'\n'            
        with open(new_name,'w') as file:
            file.write(output_lines)      
        scriptname=filepath.replace('./code_app_routes/','')    
        print()
        print('scriptname : ',scriptname)
        print()         
        function_file='./code_central_routes/central_routes.txt'
        if '.py' in scriptname:
            pass
        else:
            scriptname=scriptname+'.py'
        if os.path.exists(function_file):
            with open(function_file) as file:
                text_content=file.read()        
            if  scriptname not in text_content:            
                with open(function_file,'a+') as file:      
                    file.write(scriptname+'\n')
        else:
            with open(function_file,'w') as file:      
                file.write(scriptname+'\n')                  
         
        with open('./result/home_url.txt') as file:
            home_url=file.read()            
        html_output='<html><body><b><a href="'+home_url+'"><= back to home</b></a><br><br><h3>Ok route script had been moved to system</h3><a href="/stop">Click here to stop the App  </a></body></html>';             
    env.level=env.level[:-1]
    return html_output  
  


#  def_move_function_to_system***
@app.route('/move_function_to_system', methods=['GET'])
def move_function_to_system():
    '''
    Created : 2025-06-10T12:54:39.000Z

    description : move function from ./code_app_functions to ./code_system_functions
    '''
    route="/move_function_to_system"
    env.level+='-'
    print()
    print(env.level,white('route move_function_to_system() in ***app.py*** : >',bold=True))
    loguer(env.level+' route move_function_to_system() in ***app.py*** : >')
    print()
    global client_id
    global client_password
    global host
    global host_for_token
    global profil_name
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        filename=request.args.get('filename')
        filename=filename.replace('../','./')
        print()
        print('filename : ',filename)
        print()
        scriptdir=request.args.get('scriptdir')
        print()
        print('scriptdir : ',scriptdir)
        print()        
        html_output=f'<h3>Do you really want to promote function : <br><br>{filename} to system function </h3><br>in directory <b>[ {scriptdir} ]</b><br><hr>';
        html_output=html_output+f'<form action="/ok_move_function_to_system" method="GET"><input type="text" name="new_name" value="{filename}"><input type="hidden" name="filename" value="{filename}"><input type="hidden" name="scriptdir" value="{scriptdir}"><input type="submit" value="Move"></form>'
        env.level=env.level[:-1]
        return html_output  


#  def_move_route_to_system***
@app.route('/move_route_to_system', methods=['GET'])
def move_route_to_system():
    '''
    Created : 2025-06-10T12:05:09.000Z

    description : move route in app folder to the system folder
    '''
    route="/move_route_to_system"
    env.level+='-'
    print()
    print(env.level,white('route move_route_to_system() in ***app.py*** : >',bold=True))
    loguer(env.level+' route move_route_to_system() in ***app.py*** : >')
    print()
    global client_id
    global client_password
    global host
    global host_for_token
    global profil_name
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        filename=request.args.get('filename')
        filename=filename.replace('../','./')
        print()
        print('filename : ',filename)
        print()
        scriptdir=request.args.get('scriptdir')
        print()
        print('scriptdir : ',scriptdir)
        print()        
        html_output=f'<h3>Do you really want to promote route : <br><br>{filename} to system route </h3><br>in directory <b>[ {scriptdir} ]</b><br><hr>';
        html_output=html_output+f'<form action="/ok_move_route_to_system" method="GET"><input type="text" name="new_name" value="{filename}"><input type="hidden" name="filename" value="{filename}"><input type="hidden" name="scriptdir" value="{scriptdir}"><input type="submit" value="Move"></form>'
        env.level=env.level[:-1]
        return html_output  


#  def_ok_move_function_to_system***
@app.route('/ok_move_function_to_system', methods=['GET'])
def ok_move_function_to_system():
    '''
    Created : 2025-06-10T14:46:18.000Z

    description : move function to system confirmed. Lets do it
    '''
    route="/ok_move_function_to_system"
    env.level+='-'
    print()
    print(env.level,white('route ok_move_function_to_system() in ***app.py*** : >',bold=True))
    loguer(env.level+' route ok_move_function_to_system() in ***app.py*** : >')
    print()
    global client_id
    global client_password
    global host
    global host_for_token
    global profil_name
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        filepath=request.args.get('filename')       
        print()
        print('filename path : ',filepath)  
        print()          
        scriptdir=request.args.get('scriptdir')
        print()
        print('scriptdir : ',scriptdir)
        print()    
        new_name=filepath.replace('code_app_functions','code_system_functions')
        print()
        print('new_name : ',new_name)
        print()        
       
        if os.path.exists(filepath):
            print(' ok move this file :',filepath,' to ',new_name)
            with open(filepath) as file:
                text_content=file.read()            
            with open(new_name,'w') as file:
                file.write(text_content)      
        scriptname=filepath.replace('./code_app_functions/','')    
        print()
        print('scriptname : ',scriptname)
        print()         
        function_file='./code_architecture/app_functions.txt'

        with open(function_file) as file:
            text_content=file.read()        
        text_content=text_content.replace(scriptname+'\n','')    
        with open(function_file,'w') as file:      
            file.write(text_content)

        with open('./code_architecture/system_functions.txt','a+') as file:      
            file.write(scriptname+'\n')
                        
        if os.path.exists(filepath):
            print(' ok delete',filepath)
            os.remove(filepath)            
        with open('./result/home_url.txt') as file:
            home_url=file.read()            
        html_output='<html><body><b><a href="'+home_url+'"><= back to home</b></a><br><br><h3>Ok function script had been moved to system</h3><a href="/stop">Click here to stop the App  </a></body></html>';             
    env.level=env.level[:-1]
    return html_output  
  


#  def_ok_move_route_to_system***
@app.route('/ok_move_route_to_system', methods=['GET'])
def ok_move_route_to_system():
    '''
    Created : 2025-06-10T13:25:33.000Z

    description : move route to system confirmed. Lets do it
    '''
    route="/ok_move_route_to_system"
    env.level+='-'
    print()
    print(env.level,white('route ok_move_route_to_system() in ***app.py*** : >',bold=True))
    loguer(env.level+' route ok_move_route_to_system() in ***app.py*** : >')
    print()
    global client_id
    global client_password
    global host
    global host_for_token
    global profil_name
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        filepath=request.args.get('filename')       
        print()
        print('filename path : ',filepath)  
        print()          
        scriptdir=request.args.get('scriptdir')
        print()
        print('scriptdir : ',scriptdir)
        print()    
        new_name=filepath.replace('code_app_routes','code_system_routes')
        print()
        print('new_name : ',new_name)
        print()        
       
        if os.path.exists(filepath):
            print(' ok move this file :',filepath,' to ',new_name+'.py')
            with open(filepath) as file:
                text_content=file.read()            
            with open(new_name,'w') as file:
                file.write(text_content)      
        scriptname=filepath.replace('./code_app_routes/','')    
        print()
        print('scriptname : ',scriptname)
        print()         
        function_file='./code_architecture/app_routes.txt'

        with open(function_file) as file:
            text_content=file.read()        
        text_content=text_content.replace(scriptname+'\n','')    
        with open(function_file,'w') as file:      
            file.write(text_content)

        with open('./code_architecture/system_routes.txt','a+') as file:      
            file.write(scriptname+'\n')
                        
        if os.path.exists(filepath):
            print(' ok delete',filepath)
            os.remove(filepath)            
        with open('./result/home_url.txt') as file:
            home_url=file.read()            
        html_output='<html><body><b><a href="'+home_url+'"><= back to home</b></a><br><br><h3>Ok route script had been moved to system</h3><a href="/stop">Click here to stop the App  </a></body></html>';             
    env.level=env.level[:-1]
    return html_output  


#  def_copy_function_into_project***
@app.route('/copy_function_into_project', methods=['GET'])
def copy_function_into_project():
    '''
    Created : 2025-08-23

    description : copy function from central library to app functions
    '''
    route="/copy_function_into_project"
    env.level+='-'
    print()
    print(env.level,white('route copy_function_into_project() in ***app.py*** : >',bold=True))
    loguer(env.level+' route copy_function_into_project() in ***app.py*** : >')
    print()
    global client_id
    global client_password
    global host
    global host_for_token
    global profil_name
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        '''
        script_project=request.args.get('scriptdir')+'.py'
        print()
        print('script_project : ',scriptdir)  
        '''
        script=request.args.get('script')
        print()
        print('script to add into project : ',script)
        source_filename='./code_central_functions/'+script
        if '_v20' in script:
            script_destination=script.split('_v')[0]+'.py'
        else:
            script_destination=script
        destination_filename='./code_app_functions/'+script_destination
        print(' ok copy this file :',source_filename,' to ',destination_filename)
        with open(source_filename) as file:
            text_content=file.read()         
        #text_content=text_content.replace('app.py',script_project)
        with open(destination_filename,'w') as file:
            file.write(text_content)             
        function_file='./code_architecture/app_functions.txt'
        if '.py' in script_destination:
            pass
        else:
            script_destination=script_destination+'.py'
        if os.path.exists(function_file):
            with open(function_file) as file:
                text_content=file.read()        
            if  script_destination not in text_content:            
                with open(function_file,'a+') as file:      
                    file.write(script_destination+'\n')
        else:
            with open(function_file,'w') as file:      
                file.write(script_destination+'\n')            
        with open('./result/home_url.txt') as file:
            home_url=file.read()            
        html_output='<html><body><b><a href="'+home_url+'"><= back to home</b></a><br><br><h3>Function Script :<br><br>'+script+'<br><br>Copied into project</h3><a href="/new_function_from_library">Copy / Link another function script </a><br><br><a href="/stop">Click here to stop the App  </a></body></html>';             
    env.level=env.level[:-1]
    return html_output         
  


#  def_copy_function_into_project_B***
@app.route('/copy_function_into_project_B', methods=['GET'])
def copy_function_into_project_B():
    '''
    Created : 2025-08-23

    description : copy function from central library to imported script functions
    '''
    route="/copy_function_into_project_B"
    env.level+='-'
    print()
    print(env.level,white('route copy_function_into_project_B() in ***app.py*** : >',bold=True))
    loguer(env.level+' route copy_function_into_project_B() in ***app.py*** : >')
    print()
    global client_id
    global client_password
    global host
    global host_for_token
    global profil_name
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        script=request.args.get('script')
        print()
        print('script : ',script)
        scriptdir=request.args.get('scriptdir')
        print()
        print('scriptdir : ',scriptdir)       
        if '_v20' in script:
            script_destination=script.split('_v')[0]+'.py'
        else:
            script_destination=script
        source_filename='./code_central_functions/'+script
        destination_filename='./code_app_scripts_to_import/'+scriptdir+'/'+script_destination
        print(' ok copy this file :',source_filename,' to ',destination_filename)
        with open(source_filename) as file:
            text_content=file.read() 
        text_content=text_content.replace('app.py',scriptdir+'.py')
        with open(destination_filename,'w') as file:
            file.write(text_content)             
        function_file='./code_app_scripts_to_import/'+scriptdir+'/script_functions.txt'
        print()
        print('function_file : ',function_file)        
        if '.py' in script_destination:
            pass
        else:
            script_destination=script_destination+'.py'
        if os.path.exists(function_file):
            with open(function_file) as file:
                text_content=file.read()        
            if script_destination not in text_content:            
                with open(function_file,'a+') as file:      
                    file.write(script_destination+'\n')
        else:
            with open(function_file,'w') as file:      
                file.write(script_destination+'\n')      
        with open('./result/home_url.txt') as file:
            home_url=file.read()            
        html_output='<html><body><b><a href="'+home_url+'"><= back to home</b></a><br><br><h3>Function Script :<br><br>'+script+'<br><br>Copied into project</h3><a href="/new_function_from_library_B?script='+script+'&scriptdir='+scriptdir+'">Copy / Link another function script </a><br><br><a href="/stop">Click here to stop the App  </a></body></html>';             
    env.level=env.level[:-1]
    return html_output         
  


#  def_copy_function_to_central_B***
@app.route('/copy_function_to_central_B', methods=['GET'])
def copy_function_to_central_B():
    '''
    Created : 2025-08-22

    description : copy a function script from an imported script to central library
    '''
    route="/copy_function_to_central_B"
    env.level+='-'
    print()
    print(env.level,white('route copy_function_to_central_B() in ***app.py*** : >',bold=True))
    loguer(env.level+' route copy_function_to_central_B() in ***app.py*** : >')
    print()
    global client_id
    global client_password
    global host
    global host_for_token
    global profil_name
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        filepath=request.args.get('filename')       
        print()
        print('filename path : ',filepath)  
        print()          
        scriptdir=request.args.get('scriptdir')
        print()
        print('scriptdir : ',scriptdir)
        print()    
        new_name=filepath.replace('code_app_scripts_to_import/'+scriptdir,'code_central_functions')
        script_date = datetime.utcnow().strftime("%Y-%m-%d")
        new_name=new_name.replace('.py','_v'+script_date+'.py')
        print()
        print('new_name : ',new_name)
        print()        
        print(' ok copy this file :',filepath,' to ',new_name+'.py')
   
        with open(filepath) as file:
            text_content=file.read()
        lines=text_content.split('\n')
        output_lines=''
        for line in lines:
            print('line :' ,cyan(line,bold=True))
            if "print(env.level,white(" in line or "print('\\n'+env.level,white(" in line:
                print('line :',red(line,bold=True))
                chunks=line.split(') in ')
                line=chunks[0]+") in app.py  : >\\n',bold=True))"
                print('TO line :',green(line,bold=True))
            if "loguer(env.level+" in line:
                print('line :',red(line,bold=True))
                chunks=line.split(') in ')
                line=chunks[0]+") in app.py  : > ')"
                print('TO line :',green(line,bold=True))                
            output_lines=output_lines+line+'\n'
        with open(new_name,'w') as file:
            file.write(output_lines)      
        scriptname=filepath.replace('./code_app_scripts_to_import/'+scriptdir+'/','') 
        print()
        print('scriptname : ',scriptname)
        print()         
        function_file='./code_central_functions/central_functions.txt'

        if '.py' in scriptname:
            pass
        else:
            scriptname=scriptname+'.py'
        if os.path.exists(function_file):
            with open(function_file) as file:
                text_content=file.read()        
            if  scriptname not in text_content:            
                with open(function_file,'a+') as file:      
                    file.write(scriptname+'\n')
        else:
            with open(function_file,'w') as file:      
                file.write(scriptname+'\n')  
        
        with open('./result/home_url.txt') as file:
            home_url=file.read()            
        html_output='<html><body><b><a href="'+home_url+'"><= back to home</b></a><br><br><h3>Ok function script had been Copied to cenral library</h3><a href="/stop">Click here to stop the App  </a></body></html>';             
    env.level=env.level[:-1]
    return html_output  
  


#  def_copy_route_into_project***
@app.route('/copy_route_into_project', methods=['GET'])
def copy_route_into_project():
    '''
    Created : 2025-06-14T08:00:50.000Z

    description : copy selected script from library to project app scripts
    '''
    route="/copy_route_into_project"
    env.level+='-'
    print()
    print(env.level,white('route copy_route_into_project() in ***app.py*** : >',bold=True))
    loguer(env.level+' route copy_route_into_project() in ***app.py*** : >')
    print()
    global client_id
    global client_password
    global host
    global host_for_token
    global profil_name
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        script=request.args.get('script')
        print()
        print('script : ',script)
        source_filename='./code_central_routes/'+script
        destination_filename='./code_app_routes/'+script
        print(' ok copy this file :',source_filename,' to ',destination_filename)
        with open(source_filename) as file:
            text_content=file.read()            
        with open(destination_filename,'w') as file:
            file.write(text_content)             
        function_file='./code_architecture/app_routes.txt'
        if '.py' in script:
            pass
        else:
            script=script+'.py'
        if os.path.exists(function_file):
            with open(function_file) as file:
                text_content=file.read()        
            if  script not in text_content:            
                with open(function_file,'a+') as file:      
                    file.write(script+'\n')
        else:
            with open(function_file,'w') as file:      
                file.write(script+'\n')            
        with open('./result/home_url.txt') as file:
            home_url=file.read()            
        html_output='<html><body><b><a href="'+home_url+'"><= back to home</b></a><br><br><h3>Route Script :<br><br>'+script+'<br><br>Copied into project</h3><a href="/new_route_from_library">Copy / Link another route script </a><br><br><a href="/stop">Click here to stop the App  </a></body></html>';             
    env.level=env.level[:-1]
    return html_output         


#  def_copy_route_into_project_B***
@app.route('/copy_route_into_project_B', methods=['GET'])
def copy_route_into_project_B():
    '''
    Created : 2025-06-14T10:27:55.000Z

    description : copy route from central library to imported script
    '''
    route="/copy_route_into_project_B"
    env.level+='-'
    print()
    print(env.level,white('route copy_route_into_project_B() in ***app.py*** : >',bold=True))
    loguer(env.level+' route copy_route_into_project_B() in ***app.py*** : >')
    print()
    global client_id
    global client_password
    global host
    global host_for_token
    global profil_name
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        script=request.args.get('script')
        print()
        print('script : ',script)
        scriptdir=request.args.get('scriptdir')
        print()
        print('scriptdir : ',scriptdir)        
        
        source_filename='./code_central_routes/'+script
        destination_filename='./code_app_scripts_to_import/'+scriptdir+'/'+script
        print(' ok copy this file :',source_filename,' to ',destination_filename)
        with open(source_filename) as file:
            text_content=file.read()            
        with open(destination_filename,'w') as file:
            file.write(text_content)             
        function_file='./code_app_scripts_to_import/'+scriptdir+'/script_routes.txt'
        print()
        print('function_file : ',function_file)        
        if '.py' in script:
            pass
        else:
            script=script+'.py'
        if os.path.exists(function_file):
            with open(function_file) as file:
                text_content=file.read()        
            if  script not in text_content:            
                with open(function_file,'a+') as file:      
                    file.write(script+'\n')
        else:
            with open(function_file,'w') as file:      
                file.write(script+'\n')      
        with open('./result/home_url.txt') as file:
            home_url=file.read()            
        html_output='<html><body><b><a href="'+home_url+'"><= back to home</b></a><br><br><h3>Route Script :<br><br>'+script+'<br><br>Copied into project</h3><a href="/new_route_from_library_B?script='+script+'&scriptdir='+scriptdir+'">Copy / Link another route script </a><br><br><a href="/stop">Click here to stop the App  </a></body></html>';             
    env.level=env.level[:-1]
    return html_output         
  


#  def_copy_route_to_central_B***
@app.route('/copy_route_to_central_B', methods=['GET'])
def copy_route_to_central_B():
    '''
    Created : 2025-06-14T09:27:40.000Z

    description : copy selected route script into central library
    '''
    route="/copy_route_to_central_B"
    env.level+='-'
    print()
    print(env.level,white('route copy_route_to_central_B() in ***app.py*** : >',bold=True))
    loguer(env.level+' route copy_route_to_central_B() in ***app.py*** : >')
    print()
    global client_id
    global client_password
    global host
    global host_for_token
    global profil_name
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        filepath=request.args.get('filename')       
        print()
        print('filename path : ',filepath)  
        print()          
        scriptdir=request.args.get('scriptdir')
        print()
        print('scriptdir : ',scriptdir)
        print()    
        new_name=filepath.replace('code_app_scripts_to_import/'+scriptdir,'code_central_routes')
        print()
        print('new_name : ',new_name)
        print()        
        print(' ok copy this file :',filepath,' to ',new_name+'.py')
   
        with open(filepath) as file:
            text_content=file.read()            
        with open(new_name,'w') as file:
            file.write(text_content)      
        scriptname=filepath.replace('./code_app_scripts_to_import/'+scriptdir+'/','') 
        print()
        print('scriptname : ',scriptname)
        print()         
        function_file='./code_central_routes/central_routes.txt'

        if '.py' in scriptname:
            pass
        else:
            scriptname=scriptname+'.py'
        if os.path.exists(function_file):
            with open(function_file) as file:
                text_content=file.read()        
            if  scriptname not in text_content:            
                with open(function_file,'a+') as file:      
                    file.write(scriptname+'\n')
        else:
            with open(function_file,'w') as file:      
                file.write(scriptname+'\n')  
        
        with open('./result/home_url.txt') as file:
            home_url=file.read()            
        html_output='<html><body><b><a href="'+home_url+'"><= back to home</b></a><br><br><h3>Ok route script had been Copied to cenral library</h3><a href="/stop">Click here to stop the App  </a></body></html>';             
    env.level=env.level[:-1]
    return html_output  
  


#  def_new_function_from_library***
@app.route('/new_function_from_library', methods=['GET'])
def new_function_from_library():
    '''
    Created : 2025-09-13

    description : select a function from central library
    '''
    route="/new_function_from_library"
    env.level+='-'
    print()
    print(env.level,white('route new_function_from_library() in ***app.py*** : >',bold=True))
    loguer(env.level+' route new_function_from_library() in ***app.py*** : >')
    print()
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        with open('./result/home_url.txt') as file:
            home_url=file.read()
        html_output='<html><body><a href="'+home_url+'"><b><= back to home</b></a><br><form action="/search_new_function_from_library" method="get"><input type="text" name="keyword"><input type="submit" value="Search"></form><table border="1"><tbody>';
        files =[file for file in os.listdir('./code_central_functions')]
        function_list=[]
        scriptdir='code_app_functions'
        for file in files:
              if '.txt' not in file:
                print(' file : ',yellow(file,bold=True)) 
                
                html_output=html_output+'<tr><td><b><a href="/code_edit_C?code='+file+'&type=function">'+file+'</a> </td><td><a href="/copy_function_into_project?script='+file+'&scriptdir='+scriptdir+'">COPY to project</a></td><td><a href="/link_function_to_project?script='+file+'">LINK to project</a></b></td></tr>'
        env.level=env.level[:-1]
        html_output=html_output+'</tbody></table><br><br><a href="/stop">Click here to stop the App  </a></body><html>'
        return html_output      
      
  


#  def_new_function_from_library_B***
@app.route('/new_function_from_library_B', methods=['GET'])
def new_function_from_library_B():
    '''
    Created : 2025-08-23

    description : Add a new function from central library to imported script
    '''
    route="/new_function_from_library_B"
    env.level+='-'
    print()
    print(env.level,white('route new_function_from_library_B() in ***app.py*** : >',bold=True))
    loguer(env.level+' route new_function_from_library_B() in ***app.py*** : >')
    print()
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        script=request.args.get('script')
        print()
        print('script : ',script)
        scriptdir=request.args.get('scriptdir')
        print()
        print('scriptdir : ',scriptdir)        
        with open('./result/home_url.txt') as file:
            home_url=file.read()
        html_output='<html><body><a href="'+home_url+'"><b><= back to home</b></a><br><form action="/search_new_function_from_library_B" method="get"><input type="text" name="keyword"><input type="hidden" name="script" value="'+script+'"><input type="hidden" name="scriptdir" value="'+scriptdir+'"><input type="submit" value="Search"></form><br><ul>';
        files =[file for file in os.listdir('./code_central_functions')]
        function_list=[]
        for file in files:
              if '.txt' not in file:
                print(' file : ',yellow(file,bold=True)) 
                html_output=html_output+'<li><b>'+file+' : <a href="/copy_function_into_project_B?script='+file+'&scriptdir='+scriptdir+'">COPY to project</a>.---.<a href="/link_function_to_project_B?script='+file+'&scriptdir='+scriptdir+'">LINK to project</a></b>'
        env.level=env.level[:-1]
        html_output=html_output+'</ul><br><br><a href="/stop">Click here to stop the App  </a></body><html>'
        return html_output      
      
  


#  def_new_route_from_library***
@app.route('/new_route_from_library', methods=['GET'])
def new_route_from_library():
    '''
    Created : 2025-06-14T07:50:53.000Z

    description : select a route from central library
    '''
    route="/new_route_from_library"
    env.level+='-'
    print()
    print(env.level,white('route new_route_from_library() in ***app.py*** : >',bold=True))
    loguer(env.level+' route new_route_from_library() in ***app.py*** : >')
    print()
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        with open('./result/home_url.txt') as file:
            home_url=file.read()
        html_output='<html><body><a href="'+home_url+'"><b><= back to home</b></a><br><br><form action="/search_new_route_from_library" method="get"><input type="text" name="keyword"><input type="submit" value="Search"></form><table border="1"><tbody>';
        files =[file for file in os.listdir('./code_central_routes')]
        function_list=[]
        scriptdir='code_app_routes'
        for file in files:
              if '.txt' not in file:
                print(' file : ',yellow(file,bold=True)) 
                html_output=html_output+'<tr><td><b><a href="/code_edit_C?code='+file+'&type=route">'+file+'</a> </td><td> <a href="/copy_route_into_project?script='+file+'">COPY to project</a></td><td><a href="/link_route_to_project?script='+file+'">LINK to project</a></b></td></tr>'
        env.level=env.level[:-1]
        html_output=html_output+'</tbody></table><br><br><a href="/stop">Click here to stop the App  </a></body><html>'
        return html_output


#  def_new_route_from_library_B***
@app.route('/new_route_from_library_B', methods=['GET'])
def new_route_from_library_B():
    '''
    Created : 2025-06-14T10:21:33.000Z

    description : add a route from central library to imported script routes
    '''
    route="/new_route_from_library_B"
    env.level+='-'
    print()
    print(env.level,white('route new_route_from_library_B() in ***app.py*** : >',bold=True))
    loguer(env.level+' route new_route_from_library_B() in ***app.py*** : >')
    print()
    global client_id
    global client_password
    global host
    global host_for_token
    global profil_name
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        script=request.args.get('script')
        print()
        print('script : ',script)
        scriptdir=request.args.get('scriptdir')
        print()
        print('scriptdir : ',scriptdir)        
        with open('./result/home_url.txt') as file:
            home_url=file.read()
        html_output='<html><body><a href="'+home_url+'"><b><= back to home</b></a><br><form action="/search_new_route_from_library_B" method="get"><input type="text" name="keyword"><input type="hidden" name="script" value="'+script+'"><input type="hidden" name="scriptdir" value="'+scriptdir+'"><input type="submit" value="Search"></form><ul>';
        files =[file for file in os.listdir('./code_central_routes')]
        function_list=[]
        for file in files:
              if '.txt' not in file:
                print(' file : ',yellow(file,bold=True)) 
                html_output=html_output+'<li><b>'+file+' : <a href="/copy_route_into_project_B?script='+file+'&scriptdir='+scriptdir+'">COPY to project</a>.---.<a href="/link_route_to_project_B?script='+file+'&scriptdir='+scriptdir+'">LINK to project</a></b>'
        env.level=env.level[:-1]
        html_output=html_output+'</ul><br><br><a href="/stop">Click here to stop the App  </a></body><html>'
        return html_output      
      
  


#  def_analyse_logs***
@app.route('/analyse_logs', methods=['GET'])
def analyse_logs():
    '''
    Created : 2025-07-19T19:56:25.000Z

    description : read log and create a dtree vie
    '''
    route="/analyse_logs"
    env.level+='-'
    print('\n'+env.level,white('route analyse_logs() in ***app.py*** : >\n',bold=True))
    #loguer(env.level+' route analyse_logs() in ***app.py*** : >')
    global client_id
    global client_password
    global host
    global host_for_token
    global profil_name
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        subprocess.run(["python", "analyse_application_logs.py"])
        with open('./templates/log.html') as file:
            html_output=file.read()
        env.level=env.level[:-1]
        return html_output


#  def_duplicate_function***
@app.route('/duplicate_function', methods=['GET'])
def duplicate_function():
    '''
    Created : 2025-07-24T08:24:03.000Z

    description : duplicate function with same name + _COPY_ 
    '''
    route="/duplicate_function"
    env.level+='-'
    print('\n'+env.level,white('route duplicate_function() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route duplicate_function() in ***app.py*** : >')
    global client_id
    global client_password
    global host
    global host_for_token
    global profil_name
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        filename=request.args.get('filename')
        print('\nfilename : ',filename)       
        mot=filename.replace('.py','')
        mot=mot.replace('def_','')
        filename2=filename.replace('.py','_COPY_.py')
        print('\nmot : ',mot+'\n')
        with open('./code_app_functions/'+filename) as file:
            code=file.read()
            code=code.replace(mot,mot+'_COPY_')    
        new_filename='./code_app_functions/'+filename2
        with open(new_filename,'w') as file:
              file.write(code)            
        with open('./code_architecture/app_functions.txt','a+') as file: 
            file.write(filename2+'\n')
        with open('./result/home_url.txt') as file:
            home_url=file.read()
        html_output='''<html><body><a href="'''+home_url+'''"><b><= back to home</b></a><br><br>
        <center><h3>route copied as '''+filename+'''_COPY_.py</h3></center>
        </body></html>
        ''';       
    '''    
    with open('./result/current_edited_script.txt',"w") as file:
        file.write(filename2)          
    '''
    env.level=env.level[:-1]
    return html_output 

#  def_duplicate_route***
@app.route('/duplicate_route', methods=['GET'])
def duplicate_route():
    '''
    Created : 2025-07-24T08:24:03.000Z

    description : duplicate route with same name + _COPY_ 
    '''
    route="/duplicate_route"
    env.level+='-'
    print('\n'+env.level,white('route duplicate_route() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route duplicate_route() in ***app.py*** : >')
    global client_id
    global client_password
    global host
    global host_for_token
    global profil_name
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        filename=request.args.get('filename')
        print('\nfilename : ',filename)       
        mot=filename.replace('.py','')
        mot=mot.replace('route_def_','')
        filename2=filename.replace('.py','_COPY_.py')
        print('\nmot : ',mot+'\n')
        with open('./code_app_routes/'+filename) as file:
            code=file.read()
            code=code.replace(mot,mot+'_COPY_')    
        new_filename='./code_app_routes/'+filename2
        with open(new_filename,'w') as file:
              file.write(code)            
        with open('./code_architecture/app_routes.txt','a+') as file: 
            file.write(filename2+'\n')
        with open('./result/home_url.txt') as file:
            home_url=file.read()
        html_output='''<html><body><a href="'''+home_url+'''"><b><= back to home</b></a><br><br>
        <center><h3>route copied as '''+filename+'''_COPY_.py</h3></center>
        </body></html>
        ''';       
    '''    
    with open('./result/current_edited_script.txt',"w") as file:
        file.write(filename2)          
    '''
    env.level=env.level[:-1]
    return html_output 

#  def_duplicate_system_function***
@app.route('/duplicate_system_function', methods=['GET'])
def duplicate_system_function():
    '''
    Created : 2025-10-29

    description : duplicate a system function in app functions
    '''
    route="/duplicate_system_function"
    env.level+='-'
    print('\n'+env.level,white('route duplicate_system_function() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route duplicate_system_function() in ***app.py*** : >')
    global client_id
    global client_password
    global host
    global host_for_token
    global profil_name
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        filename=request.args.get('filename')
        print('\nfilename : ',filename)       
        mot=filename.replace('.py','')
        mot=mot.replace('def_','')
        filename2=filename.replace('.py','_COPY_.py')
        print('\nmot : ',mot+'\n')
        with open('./code_system_functions/'+filename) as file:
            code=file.read()
            code=code.replace(mot,mot+'_COPY_')    
        new_filename='./code_app_functions/'+filename2
        with open(new_filename,'w') as file:
              file.write(code)            
        with open('./code_architecture/app_functions.txt','a+') as file: 
            file.write(filename2+'\n')
        with open('./result/home_url.txt') as file:
            home_url=file.read()
        html_output='''<html><body><a href="'''+home_url+'''"><b><= back to home</b></a><br><br>
        <center><h3>function copied as '''+filename+'''_COPY_.py</h3></center>
        </body></html>
        ''';       
    '''    
    with open('./result/current_edited_script.txt',"w") as file:
        file.write(filename2)          
    '''
    env.level=env.level[:-1]
    return html_output 
  

#  def_duplicate_system_route***
@app.route('/duplicate_system_route', methods=['GET'])
def duplicate_system_route():
    '''
    Created : 2025-07-31T07:40:03.000Z

    description : duplicate a system route in app routes
    '''
    route="/duplicate_system_route"
    env.level+='-'
    print('\n'+env.level,white('route duplicate_system_route() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route duplicate_system_route() in ***app.py*** : >')
    global client_id
    global client_password
    global host
    global host_for_token
    global profil_name
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        filename=request.args.get('filename')
        print('\nfilename : ',filename)       
        mot=filename.replace('.py','')
        mot=mot.replace('route_def_','')
        filename2=filename.replace('.py','_COPY_.py')
        print('\nmot : ',mot+'\n')
        with open('./code_system_routes/'+filename) as file:
            code=file.read()
            code=code.replace(mot,mot+'_COPY_')    
        new_filename='./code_app_routes/'+filename2
        with open(new_filename,'w') as file:
              file.write(code)            
        with open('./code_architecture/app_routes.txt','a+') as file: 
            file.write(filename2+'\n')
        with open('./result/home_url.txt') as file:
            home_url=file.read()
        html_output='''<html><body><a href="'''+home_url+'''"><b><= back to home</b></a><br><br>
        <center><h3>route copied as '''+filename+'''_COPY_.py</h3></center>
        </body></html>
        ''';       
    '''    
    with open('./result/current_edited_script.txt',"w") as file:
        file.write(filename2)          
    '''
    env.level=env.level[:-1]
    return html_output 
  

#  def_del_html_file***
@app.route('/del_html_file', methods=['GET'])
def del_html_file():
    '''
    Created : 2025-07-25T06:45:11.000Z

    description : delete an html file from local library
    '''
    route="/del_html_file"
    env.level+='-'
    print('\n'+env.level,white('route del_html_file() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route del_html_file() in ***app.py*** : >')
    global client_id
    global client_password
    global host
    global host_for_token
    global profil_name
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        filename=request.args.get('filename')
        filename=filename.replace('../','./')
        print('\nfilename : ',filename+'\n')    
        scriptdir='code_app_html_templates'
        html_output=f'<h3>Do you really want to delete : <br><br>{filename}</h3><br>in directory <b>./code_app_html_templates</b><br><hr>';
        html_output=html_output+f'<form action="/ok_delete_file" method="GET"><input type="hidden" name="filename" value="{filename}"><input type="hidden" name="scriptdir" value="{scriptdir}"><input type="submit" value="YES I DO"></form>'
        env.level=env.level[:-1]
        return html_output  


#  def_duplicate_script***
@app.route('/duplicate_script', methods=['GET'])
def duplicate_script():
    '''
    Created : 2025-08-22

    description : duplicate a function in an imported script
    '''
    route="/duplicate_script"
    env.level+='-'
    print('\n'+env.level,white('route duplicate_script() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route duplicate_script() in ***app.py*** : >')
    print('\n'+env.level,white('route duplicate_route() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route duplicate_route() in ***app.py*** : >')
    global client_id
    global client_password
    global host
    global host_for_token
    global profil_name
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        type=request.args.get('type')
        print('\ntype : ',type)       
        scriptdir=request.args.get('scriptdir')
        print('\nscriptdir : ',scriptdir)       
        filename=request.args.get('filename')
        print('\nfilename : ',filename)       
        mot=filename.replace('.py','')
        if type=="route":
               mot=mot.replace('route_def_','')
        else:
            mot=mot.replace('def_','')  
        filename2=filename.replace('.py','_COPY_.py')
        print('\nmot : ',mot+'\n')
        with open('./code_app_scripts_to_import/'+scriptdir+'/'+filename) as file:
            code=file.read()
            code=code.replace(mot,mot+'_COPY_')    
        new_filename='./code_app_scripts_to_import/'+scriptdir+'/'+filename2
        with open(new_filename,'w') as file:
              file.write(code)   
        if type=="route":
            with open('./code_architecture/script_routes.txt','a+') as file: 
                file.write(filename2+'\n')
            with open('./code_app_scripts_to_import/'+scriptdir+'/script_routes.txt','a+') as file: 
                file.write(filename2+'\n')                
        else:
            with open('./code_architecture/script_functions.txt','a+') as file: 
                file.write(filename2+'\n')    
            with open('./code_app_scripts_to_import/'+scriptdir+'/script_functions.txt','a+') as file: 
                file.write(filename2+'\n')                                
        with open('./result/home_url.txt') as file:
            home_url=file.read()
        html_output='''<html><body><a href="'''+home_url+'''"><b><= back to home</b></a><br><br>
        <center><h3>route copied as '''+filename+'''_COPY_.py</h3></center>
        </body></html>
        ''';       
    '''    
    with open('./result/current_edited_script.txt',"w") as file:
        file.write(filename2)          
    '''
    env.level=env.level[:-1]
    return html_output 
  

#  def_list_projects***
@app.route('/list_projects', methods=['GET'])
def list_projects():
    '''
    Created : 2025-09-14

    description : list current scripts project in projects library
    '''
    route="/list_projects"
    env.level+='-'
    print('\n'+env.level,white('route list_projects() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route list_projects() in ***app.py*** : >')
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        with open('./result/home_url.txt') as file:
            home_url=file.read()
        html_output='<html><body><a href="'+home_url+'"><b><= back to home</b></a><br>';        

        html_output=html_output+'<h4>Projects :</h4><table border="1"><tbody>';
        with open('./code_projets/projets.txt') as file:
            text_content=file.read()            
        files =text_content.split('\n')  
        for file in files:
            if file!='':
                # print(' file : ',yellow(file,bold=True)) 
                with open('./code_projets/'+file+'.txt') as file2:
                    projet_details=json.loads(file2.read())
                #description=projet_details['description']
                html_output=html_output+'<tr><td><li><b><a href="/project_details?name='+file+'">'+file+'</a></b></li></td><td><li>'+projet_details['description']+'</li></td><td><a href="/project_remove">REMOVE</a></td></tr>'    
        html_output=html_output+'</tbody></table><br><a href="/stop">Click here to stop the App  </a></body></html>';            
        env.level=env.level[:-1]
        return html_output


#  new_project***
@app.route('/new_project', methods=['GET','POST'])
def new_project():
    '''
    MODIFIED : 20250507
    display formular for create a new project 
    '''
    env.level+='-'
    print()
    print(env.level,white('route new_project() : >',bold=True))
    loguer(env.level+' route new_project() : >')
    print()
    with open('./result/home_url.txt') as file:
        home_url=file.read()
    html_output='''<html><body><a href="'''+home_url+'''"><b><= back to home</b></a><br><br>
    <form action="/new_project_create" method="GET">
    <b>route name : </b><input type="text"  id="route_name" name="name" /><br><br>
    <b>package directory location : </b><input type="text"  id="working_dir" name="working_dir" size= "80"/><br><br>
    <b>route description</b><br>
    <textarea id="description" name="description" rows="5" cols="50"></textarea><br><br>
    <center><input type="submit" value="valid"/></center>
    </form>
    </body></html>
    ''';   
    env.level=env.level[:-1]
    return html_output 


#  def_new_project_add_script***
@app.route('/new_project_add_script', methods=['GET'])
def new_project_add_script():
    '''
    Created : 2025-08-01T07:16:51.000Z

    description : select a script from library and add it to project
    '''
    route="/new_project_add_script"
    env.level+='-'
    print('\n'+env.level,white('route new_project_add_script() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route new_project_add_script() in ***app.py*** : >')
    global client_id
    global client_password
    global host
    global host_for_token
    global profil_name
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        with open('./result/home_url.txt') as file:
            home_url=file.read()
        name=request.args.get('name')
        print('\n name : ',name)  
        html_output='<html><body><a href="'+home_url+'"><b><= back to home</b></a><h3>Select a script to add to project:</h3><ul>';
        with open('./code_architecture/imported_scripts.txt') as file:
            for line in file:
                # print(' file : ',yellow(line,bold=True)) 
                html_output=html_output+'<li><b><a href="/new_project_add_script_selected?script='+line+'&project='+name+'">'+line+'</a></b></li>'
        env.level=env.level[:-1]
        html_output=html_output+'\n</ul></body><html>'
        return html_output
           

#  def_new_project_add_script_selected***
@app.route('/new_project_add_script_selected', methods=['GET'])
def new_project_add_script_selected():
    '''
    Created : 2025-08-01T07:33:26.000Z

    description : add selected script to selected project 
    '''
    route="/new_project_add_script_selected"
    env.level+='-'
    print('\n'+env.level,white('route new_project_add_script_selected() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route new_project_add_script_selected() in ***app.py*** : >')
    global client_id
    global client_password
    global host
    global host_for_token
    global profil_name
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        script=request.args.get('script')
        print('\nscript name : ',script)   
        project=request.args.get('project')
        print('\nproject name : ',project)     
        with open('./code_projets/'+project+'.txt') as file:
            project_details=json.loads(file.read()) 
        project_details['script_list'].append(script)        
        with open('./code_projets/'+project+'.txt','w') as file:
            file.write(json.dumps(project_details,sort_keys=True,indent=4, separators=(',', ': ')))            
        with open('./result/home_url.txt') as file:
            home_url=file.read()
        html_output='''<html><body><a href="'''+home_url+'''"><b><= back to home</b></a><br><br>
        <center><h3>Script : '''+script+''' Added to Project : '''+project+'''</h3></center>
        <center><h3><a href="/project_details?name='''+project+'''">Back to project details</a></h3>
        </body></html>
        ''';                  
        env.level=env.level[:-1]
        return html_output 


#  def_new_project_create***
@app.route('/new_project_create', methods=['GET'])
def new_project_create():
    '''
    Created : 2025-07-31T08:27:03.000Z

    description : add the new project into the project files
    '''
    route="/new_project_create"
    env.level+='-'
    print('\n'+env.level,white('route new_project_create() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route new_project_create() in ***app.py*** : >')
    global client_id
    global client_password
    global host
    global host_for_token
    global profil_name
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        name=request.args.get('name')
        name=name.replace('-','_')
        name=name.replace(' ','_')       
        print('\n name : ',name)         
        description=request.args.get('description')
        print('\n description : ',description)         
        working_dir=request.args.get('working_dir')
        print('\n working_dir : ',working_dir)            
        name=name.replace(' ','_')
        script_details={'name': name,'description' : description,"package_dir" : working_dir, "script_list":[] }
        with open('./code_projets/projets.txt','a+') as file:
              file.write(name+'\n')
        with open('./code_projets/'+name+'.txt','w') as file:
              file.write(json.dumps(script_details,sort_keys=True,indent=4, separators=(',', ': ')))     
        with open('./result/home_url.txt') as file:
            home_url=file.read()
        html_output='''<html><body><a href="'''+home_url+'''"><b><= back to home</b></a><br><br>
        <center><h3>OK NEW PROJECT ADDED TO LIST</h3></center>
        </body></html>
        ''';   
        env.level=env.level[:-1]
        return html_output 


#  def_project_details***
@app.route('/project_details', methods=['GET'])
def project_details():
    '''
    Created : 2025-08-01T06:24:48.000Z

    description : display project details
    '''
    route="/project_details"
    env.level+='-'
    print('\n'+env.level,white('route project_details() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route project_details() in ***app.py*** : >')
    global client_id
    global client_password
    global host
    global host_for_token
    global profil_name
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        name=request.args.get('name')
        print('\nproject name : ',name)       
        with open('./result/home_url.txt') as file:
            home_url=file.read()
        with open('./code_projets/'+name+'.txt') as file:
            project_details=json.loads(file.read())
        
        html_output='''<html><body><a href="'''+home_url+'''"><b><= back to home</b></a><br><br>
        <form action="/new_project_update" method="GET">
        <b>Projectname : </b><input type="text"  id="route_name" name="name" value="'''+project_details['name']+'''"/><br><br>
        <b>package directory location : </b><input type="text"  id="working_dir" name="working_dir" size= "80" value="'''+project_details['package_dir']+'''"/><br><br>
        <b>Project description</b><br>
        <textarea id="description" name="description" rows="5" cols="50">'''+project_details['description']+'''</textarea><br>
        </form>'''
        html_output=html_output+'<h4>project scripts :</h4><table border="1"><tbody>';
        for script in project_details['script_list']:
            html_output=html_output+'<tr><td><li><b><a href="/goto_script_B?script='+script+'&type=route">'+script+'</a></b></li></b></td><td><li><b><a href="/remove_script_from_project?script='+script+'&name='+name+'">Remove</a></b></li></td></tr>'
        html_output=html_output+''
        html_output=html_output+'</tbody></table><br><form action="/new_project_add_script" method="get"><input type="hidden" name="name" value="'+name+'"><input type="submit" value="Add a new script to project"><br><br><b><a href="/stop">Click here to stop the App  </a></b></body><html>'''    
        env.level=env.level[:-1]
        return html_output 

#  def_remove_script_from_project***
@app.route('/remove_script_from_project', methods=['GET'])
def remove_script_from_project():
    '''
    Created : 2025-08-01T07:55:41.000Z

    description : remove selected script from project list
    '''
    route="/remove_script_from_project"
    env.level+='-'
    print('\n'+env.level,white('route remove_script_from_project() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route remove_script_from_project() in ***app.py*** : >')
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        script=request.args.get('script')
        print('\nscript name : ',script)   
        project=request.args.get('name')
        print('\nproject name : ',project)     
        with open('./code_projets/'+project+'.txt') as file:
            project_details=json.loads(file.read())            
        project_details['script_list'].remove(script)        
        with open('./code_projets/'+project+'.txt','w') as file:
            file.write(json.dumps(project_details,sort_keys=True,indent=4, separators=(',', ': ')))            
        with open('./result/home_url.txt') as file:
            home_url=file.read()
        html_output='''<html><body><a href="'''+home_url+'''"><b><= back to home</b></a><br><br>
        <center><h3>Script : '''+script+''' Removed Project : '''+project+'''</h3></center>
        <center><h3><a href="/project_details?name='''+project+'''">Back to project details</a></h3>
        </body></html>
        ''';                  
        env.level=env.level[:-1]
        return html_output 


#  def_search_app_function***
@app.route('/search_app_function', methods=['GET'])
def search_app_function():
    '''
    Created : 2025-08-01T06:20:17.000Z

    description : list app functions that have keyword in their names
    '''
    route="/search_app_function"
    env.level+='-'
    print('\n'+env.level,white('route search_app_function() in ***app.py*** : >\n',bold=True))
    #loguer(env.level+' route search_app_function() in ***app.py*** : >')
    global client_id
    global client_password
    global host
    global host_for_token
    global profil_name
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        keyword=request.args.get('keyword')
        print('\nkeyword : ',keyword)     
        with open('./result/home_url.txt') as file:
            home_url=file.read()  
        with open('./result/keyword.txt','w') as file:
            file.write(keyword)              
        html_output='<html><body><a href="'+home_url+'"><b><= back to home</b></a><br><br><form action="/search_app_function" method="get"><input type="text" name="keyword" value="'+keyword+'" ><input type="submit" value="Search"></form><br><br>';
                
        with open('./result/current_edited_function.txt') as file:
            last_function=file.read()
        html_output=html_output+'<b><a href="/code_edit?code='+last_function+'&type=function">Last Edited : '+last_function+'</a><br><a href="/new_function">Create a new function</a><br><h4>FUNCTIONS :</h4><table border="1"><tbody>';   
        
        files =[file for file in os.listdir('./code_app_functions')]
        ii=0
        scriptdir='code_app_functions'
        function_list=[]
        for file in files:
            if 'a_core_' not in file and file !='back' and keyword in file: 
                # print(' file : ',yellow(file,bold=True)) 
                html_output=html_output+'<tr><td><b><a href="/code_edit?code='+file+'&type=function">'+file+'</a></td><td><a href="/edit_html?filename=../code_app_functions/'+file+'">( open in notepad++ )</b></td><td><a href="/delete_file?filename=../code_app_functions/'+file+'&scriptdir='+scriptdir+'">(DEL)</a></b></td><td><a href="/rename_file?filename=../code_app_functions/'+file+'&scriptdir='+scriptdir+'">(REN)</a></b></td><td><a href="/move_function_to_system?filename=../code_app_functions/'+file+'&scriptdir=code_system_functions">( mv 2 sys )</a></b></td><td><a href="/copy_function_to_central?filename=./code_app_functions/'+file+'&scriptdir=code_central_functions">( cp 2 central )</a></b></td><td><a href="/duplicate_function?filename='+file+'">(duplic)</a></b></td></tr>'
        env.level=env.level[:-1]
        html_output=html_output+'\n</tbody></table><br><a href="/list_routes">List Routes</a><br><br><a href="/stop">Click here to stop the App  </a></body><html>'
        return html_output
    

            

#  def_search_app_route***
@app.route('/search_app_route', methods=['GET'])
def search_app_route():
    '''
    Created : 2025-09-28

    description : list application route that have keyword in their namds
    '''
    route="/search_app_route"
    env.level+='-'
    print('\n'+env.level,white('route search_app_route() in ***app.py*** : >\n',bold=True))
    #loguer(env.level+' route search_app_route() in ***app.py*** : >')
    global client_id
    global client_password
    global host
    global host_for_token
    global profil_name
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        keyword=request.args.get('keyword')
        print('\nkeyword : ',keyword)     
        with open('./result/home_url.txt') as file:
            home_url=file.read()     
        with open('./result/keyword.txt','w') as file:
            file.write(keyword)             
        html_output='<html><body><a href="'+home_url+'"><b><= back to home</b></a><br><br><form action="/search_app_route" method="get"><input type="text" name="keyword" value="'+keyword+'"><input type="submit" value="Search"></form><br><br>';
        with open('./result/current_edited_route.txt') as file:
            last_route=file.read()
        html_output=html_output+'<b><a href="/code_edit?code='+last_route+'&type=route">Last Edited : '+last_route+'</a><br><a href="/new_route">Create a new route</a><br><h4>ROUTES :</h4><table border="1"><tbody>';
        files =[file for file in os.listdir('./code_app_routes')]
        ii=0
        function_list=[]
        scriptdir='code_app_routes'
        for file in files:
            if 'route_' in file and 'a_core_' not in file and file !='back' and keyword in file: 
                # print(' file : ',yellow(file,bold=True)) 
                html_output=html_output+'<tr><td><b><a href="/code_edit?code='+file+'&type=route">'+file+'</a></td><td><a href="/edit_html?filename=../code_app_routes/'+file+'">( open in notepad++ )</a></td><td><a href="/delete_file?filename=../code_app_routes/'+file+'&scriptdir='+scriptdir+'">(DEL)</a></b></td><td><a href="/rename_file?filename=../code_app_routes/'+file+'&scriptdir='+scriptdir+'">(REN)</a></b></td><td><a href="/move_route_to_system?filename=../code_app_routes/'+file+'&scriptdir=code_system_routes">(mv 2 sys)</a></b></td><td><a href="/copy_route_to_central?filename=./code_app_routes/'+file+'&scriptdir=code_central_routes">(cp 2 central)</a></b></td><td><a href="/duplicate_route?filename='+file+'">(duplic)</a></b></td></tr>'
        env.level=env.level[:-1]
        html_output=html_output+'\n</tbody></table><br><a href="/list_functions">List Functions</a><br><br><a href="/stop">Click here to stop the App  </a></body><html>'
        return html_output        
        

#  def_search_system_script***
@app.route('/search_system_script', methods=['GET'])
def search_system_script():
    '''
    Created : 2025-10-29

    description : list system scripts that have keyword in their names
    '''
    route="/search_system_script"
    env.level+='-'
    print('\n'+env.level,white('route search_system_script() in ***app.py*** : >\n',bold=True))
    #loguer(env.level+' route search_system_script() in ***app.py*** : >')
    global client_id
    global client_password
    global host
    global host_for_token
    global profil_name
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        keyword=request.args.get('keyword')
        print('\nkeyword : ',keyword)           
        with open('./result/home_url.txt') as file:
            home_url=file.read()
        with open('./result/keyword.txt','w') as file:
            file.write(keyword)             
        html_output='<html><body><a href="'+home_url+'"><b><= back to home</b></a><br><br><form action="/search_system_script" method="get"><input type="text" name="keyword" value="'+keyword+'"><input type="submit" value="Search"></form><br>';        
        html_output=html_output+'<h4>System Route :</h4><table border="1"><tbody>';
        #html_output=html_output+'<h3>Edit a system route</h3><ul>';
        files =[file for file in os.listdir('./code_system_routes')]    
        for file in files:
            if 'route_' in file and file !='back' and '.py' in file and keyword in file:
                # print(' file : ',yellow(file,bold=True)) 
                html_output=html_output+'<tr><td><b><a href="/edit_html?filename=../code_system_routes/'+file+'">'+file+' ( open in notepad++ )</a></b></td><td><a href="/duplicate_system_route?filename='+file+'">(duplicate in app routes)</a></b></td></tr>'    
        html_output=html_output+'</tbody></table><h4>System Functions :</h4><table border="1"><tbody>';
        files =[file for file in os.listdir('./code_system_functions')]     
        for file in files:
            if 'route_' not in file and file !='back' and '.py' in file and keyword in file:
                # print(' file : ',yellow(file,bold=True)) 
                html_output=html_output+'<tr><td><b><a href="/edit_html?filename=../code_system_functions/'+file+'">'+file+' ( open in notepad++ )</a></b></td><td><a href="/duplicate_system_function?filename='+file+'">(duplicate in app functions)</a></b></td></tr>' 
        html_output=html_output+'</tbody></table><br><a href="/stop">Click here to stop the App  </a></body></html>';            
        env.level=env.level[:-1]
        return html_output      


#  def_search_new_function_from_library***
@app.route('/search_new_function_from_library', methods=['GET'])
def search_new_function_from_library():
    '''
    Created : 2025-08-23

    description : select a function from central library
    '''
    route="/search_new_function_from_library"
    env.level+='-'
    print()
    print(env.level,white('route search_new_function_from_library() in ***app.py*** : >',bold=True))
    loguer(env.level+' route search_new_function_from_library() in ***app.py*** : >')
    print()
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        keyword=request.args.get('keyword')
        print('\nkeyword : ',keyword)       
        with open('./result/home_url.txt') as file:
            home_url=file.read()
        html_output='<html><body><a href="'+home_url+'"><b><= back to home</b></a><br><form action="/search_new_function_from_library" method="get"><input type="text" name="keyword"><input type="submit" value="Search"></form><ul>';
        files =[file for file in os.listdir('./code_central_functions')]
        function_list=[]
        scriptdir='code_app_functions'
        for file in files:
                if '.txt' not in file and keyword in file:
                    print(' file : ',yellow(file,bold=True))
                    html_output=html_output+'<li><b>'+file+' : <a href="/copy_function_into_project?script='+file+'">COPY to project</a>.---.<a href="/link_function_to_project?script='+file+'">LINK to project</a></b>'
        env.level=env.level[:-1]
        html_output=html_output+'</ul><br><br><a href="/stop">Click here to stop the App  </a></body><html>'
        return html_output
        
  



#  def_search_new_function_from_library_B***
@app.route('/search_new_function_from_library_B', methods=['GET'])
def search_new_function_from_library_B():
    '''
    Created : 2025-08-23

    description : Add a new function from central library to imported script
    '''
    route="/search_new_function_from_library_B"
    env.level+='-'
    print()
    print(env.level,white('route search_new_function_from_library_B() in ***app.py*** : >',bold=True))
    loguer(env.level+' route search_new_function_from_library_B() in ***app.py*** : >')
    print()
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        keyword=request.args.get('keyword')
        print('\nkeyword : ',keyword)      
        script=request.args.get('script')
        print()
        print('script : ',script)
        scriptdir=request.args.get('scriptdir')
        print()
        print('scriptdir : ',scriptdir)        
        with open('./result/home_url.txt') as file:
            home_url=file.read()
        html_output='<html><body><a href="'+home_url+'"><b><= back to home</b></a><br><form action="/search_search_new_function_from_library_B" method="get"><input type="text" name="keyword"><input type="hidden" name="script" value="'+script+'"><input type="hidden" name="scriptdir" value="'+scriptdir+'"><input type="submit" value="Search"></form><br><ul>';
        files =[file for file in os.listdir('./code_central_functions')]
        function_list=[]
        for file in files:
              if '.txt' not in file and keyword in file:
                print(' file : ',yellow(file,bold=True)) 
                html_output=html_output+'<li><b>'+file+' : <a href="/copy_function_into_project_B?script='+file+'&scriptdir='+scriptdir+'">COPY to project</a>.---.<a href="/link_function_to_project_B?script='+file+'&scriptdir='+scriptdir+'">LINK to project</a></b>'
        env.level=env.level[:-1]
        html_output=html_output+'</ul><br><br><a href="/stop">Click here to stop the App  </a></body><html>'
        return html_output      
      

#  def_application_tree***
@app.route('/application_tree', methods=['GET'])
def application_tree():
    '''
    Created : 2025-09-03
    description : create and display the application function dependency tree structure
    
    how to call it : application_tree()
    '''
    route="/application_tree"
    env.level+='-'
    print('\n'+env.level,white('route application_tree() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route application_tree() in ***app.py*** : >')
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        with open('./result/home_url.txt') as file:
            home_url=file.read()
        functions_list_file=open('./result/function_list.txt','w')
        html_output='<html><body><a href="'+home_url+'"><b><= back to home</b></a><br>';
        html_output=html_output+'<h1>Application tree</h1>';
        html_output=html_output+'<h2>Main loop in app.py</h2>';
        html_output=html_output+'<li><b>Main function : <a href="/edit_html?filename=../code_system_main_blocs/a_core_main.py">if __name__==\'main\'</a> : <a href="/expand?code=a_core_main.py&type=main&parent=app.py"> ( Expand ) </a></li>'
        html_output=html_output+'<h2>List Routes in app.py</h2>';
        files =[file for file in os.listdir('./code_app_routes')]
        function_list=[]
        scriptdir='code_app_routes'
        for file in files:
            if 'route_' in file and 'a_core_' not in file and file !='back':
                # print(' file : ',yellow(file,bold=True))
                file2=file.replace("route_def_","")
                file2=file2.replace(".py","")
                file2=file2.replace("/","")
                html_output=html_output+'<li><b><a href="/code_edit?code='+file+'&type=route">/'+file2+'</a> : <a href="/expand?code='+file+'&type=route&parent=app.py"> ( Expand ) </a></b></li>'
                functions_list_file.write(file2+"(;app.py\n")
        html_output=html_output+'<h2>List Functions in app.py</h2>';
        files =[file for file in os.listdir('./code_app_functions')]
        ii=0
        scriptdir='code_app_functions'
        function_list=[]
        for file in files:
            if 'route_' not in file and 'a_core_' not in file and file !='back':
                # print(' file : ',yellow(file,bold=True))
                html_output=html_output+'<li><b><a href="/code_edit?code='+file+'&type=function">'+file+'</a> : <a href="/expand?code='+file+'&type=function&parent=app.py"> ( Expand ) </a></b></li>'
                file2=file.replace(".py","")
                file2=file2.replace("def_","")
                functions_list_file.write(file2+"(;app.py\n")
        html_output=html_output+'<h2>List External Imported Scripts</h2>';
        with open('./code_architecture/imported_scripts_to_import.txt') as file:
            text_content=file.read()
        print('imported_scripts_to_import.txt : ',cyan(text_content,bold=True))
        lines=text_content.split('\n')
        for line in lines:
            if line!='':
                html_output=html_output+'<li><b><a href="/goto_script_B?script='+line+'&type=route">'+line+'</a></b><ul>'
                scriptdir2=line.replace(".py","")
                file2s =[file2 for file2 in os.listdir('./code_app_scripts_to_import/'+scriptdir2)]
                for file2 in file2s:
                    if 'route_' not in file2 and file2 !='back' and '.py' in file2:
                        html_output=html_output+'<li><b><a href="/code_edit_B?code='+file2+'&subdir='+scriptdir2+'">'+file2+'</a> : <a href="/expand?code='+file2+'&type=script&parent='+line+'"> ( Expand ) </a></b></li>'
                        file3=file2.replace(".py","")
                        file3=file3.replace("def_","")
                        functions_list_file.write(file3+"(;"+line+"\n")
                html_output=html_output+'</ul></li>'
        html_output=html_output+'</body></html>';
        functions_list_file.close()
        env.level=env.level[:-1]
        return html_output


#  def_expand***
@app.route('/expand', methods=['GET'])
def expand():
    '''
    Created : 2025-09-03T07:31:45.000Z
    description : open selected script and list sub functions
    '''
    route="/expand"
    env.level+='-'
    print('\n'+env.level,white('route expand() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route expand() in ***app.py*** : >')
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        script=request.args.get('code')
        print('\nscript : ',script+'\n')
        type=request.args.get('type')
        print('\ntype : ',type+'\n')      
        parent=request.args.get('parent')
        print('\nparent : ',parent+'\n')        
        if type=="route":
            fichier='./code_app_routes/'+script
            type="function"
        elif type=="function":            
            fichier='./code_app_functions/'+script
        elif type=="main":            
            fichier='./code_system_main_blocs/'+script            
        else:
            subdir=parent.replace('.py','')
            fichier='./code_app_scripts_to_import/'+subdir+'/'+script
        with open(fichier) as file:
            python_code=file.read()
        with open('./result/home_url.txt') as file:
            home_url=file.read()
        html_output='<html><body><a href="/application_tree"><b><= back to home</b></a><br><h2>'+script+'</h2><h2>Functions called in this function</h2>';                   
        functions_dict={}
        with open('./result/function_list.txt') as file:
            txt_content=file.read()
        items=txt_content.split('\n')
        for item in items:
            print('item',item)
            if item!='':
                function=item.split(";")[0]
                parent_script=item.split(";")[1]
                functions_dict[function]={'function':function,'parent_script':parent_script}
                function2=function.replace('(','')
                function3='def_'+function2+'.py'
                if functions_dict[function]['parent_script']!="app.py":
                    type="script"
                    parent2=functions_dict[function]['parent_script']
                if function in python_code and function2 not in script:
                    #code_edit_B?code=def_loguer.py&subdir=analyse_application_logs
                    print('\nparent : ',parent+'\n') 
                    print('\nparent_script : ',functions_dict[function]['parent_script']+'\n')
                    if functions_dict[function]['parent_script']=="app.py":
                        parent2="app.py"
                        html_output=html_output+'<li><b><a href="/code_edit?code='+function3+'&type=function">'+function2+'</a> --- [ in '+functions_dict[function]['parent_script']+'  ] --- <a href="/expand?code='+function3+'&type='+type+'&parent='+parent2+'">( Expand )</a></b></li>'
                    else:
                        subdir=functions_dict[function]['parent_script'].replace('.py','')
                        html_output=html_output+'<li><b><a href="/code_edit_B?code='+function3+'&subdir='+subdir+'">'+function2+'</a> --- [ in '+functions_dict[function]['parent_script']+'  ] --- <a href="/expand?code='+function3+'&type='+type+'&parent='+parent2+'">( Expand )</a></b></li>'                         
        html_output=html_output+'</body></html>';
        print('functions_dict : \n',cyan(functions_dict,bold=True))
        env.level=env.level[:-1]
        return (html_output)
        


#  def_backup_application***
@app.route('/backup_application', methods=['GET'])
def backup_application():
    '''
    Created : 2025-09-11T14:57:16.000Z
    description : trigger an application code backup
    '''
    route="/backup_application"
    env.level+='-'
    print('\n'+env.level,white('route backup_application() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route backup_application() in ***app.py*** : >')
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        os.system("python backup_app_system_code.py 1")
        with open('./result/home_url.txt') as file:
            home_url=file.read()
        html_output='''<html><body><br><a href="'''+home_url+'''"><b><= back to home</b></a><br><br>
        <center><h3>APPLICATION CODE BACKUP DONE check ./code_backup </h3></center>
        <center><h3>A directory structure PLUS a zip file had been created</h3></center>
        </body></html>
            ''';
    env.level=env.level[:-1]
    return html_output 
  


# def_code_edit_C***
@app.route('/code_edit_C', methods=['GET','POST'])
def code_edit_C():
    env.level+='-'
    # print()
    # print(env.level,white('route code_edit_C() : >',bold=True))
    #loguer(env.level+' route code_edit_C() : >')
    # print()
    python_code = request.args.get('code')
    the_type = request.args.get('type')    
    if python_code=='route_def_.py':
        python_code='route_def_index.py'
    # print()
    print(' python_code:\n',yellow(python_code,bold=True))
    # print()  
    # print()
    print(' the_type :\n',yellow(the_type,bold=True))
    # print() 
    if the_type=='function':
        filename=f'./code_central_functions/{python_code}'
    elif the_type=='route':
        filename=f'./code_central_routes/{python_code}'
    else:
        filename=f'./code_central_html_templates/{python_code}'
    filename=filename.replace('/.','/')
    # print()
    # print(' filename :',yellow(filename,bold=True))
        # print()
    with open(filename) as file:
        code=file.read()
    env.level=env.level[:-1]
    return render_template("./code_editor.html",code=code,fichier=filename,the_type=the_type)


#  def_project_remove***
@app.route('/project_remove', methods=['GET'])
def project_remove():
    '''
    Created : 2025-09-14T13:27:26.000Z
    description : instruction for removing a project from the project list
    '''
    route="/project_remove"
    env.level+='-'
    print('\n'+env.level,white('route project_remove() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route project_remove() in ***app.py*** : >')
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        with open('./result/home_url.txt') as file:
            home_url=file.read()
        html_output='<html><body><a href="'+home_url+'"><b><= back to home</b></a><h2>For Now for deleting a project in the list :</h2><ul><li>Edit ./code_projets/project.txt and remove the project name</li><li>Delete the project subfolder</li></ul></body></html>';
        env.level=env.level[:-1]
        return html_output


#  def_search_new_route_from_library***
@app.route('/search_new_route_from_library', methods=['GET'])
def search_new_route_from_library():
    '''
    Created : 2025-09-14
    description : select a function from central library
    '''
    route="/search_new_route_from_library"
    env.level+='-'
    print()
    print(env.level,white('route search_new_route_from_library() in ***app.py*** : >',bold=True))
    loguer(env.level+' route search_new_route_from_library() in ***app.py*** : >')
    print()
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        keyword=request.args.get('keyword')
        print('\nkeyword : ',keyword)
        with open('./result/home_url.txt') as file:
            home_url=file.read()
        html_output='<html><body><a href="'+home_url+'"><b><= back to home</b></a><br><form action="/search_new_route_from_library" method="get"><input type="text" name="keyword"><input type="submit" value="Search"></form><ul>';
        files =[file for file in os.listdir('./code_central_routes')]
        function_list=[]
        scriptdir='code_app_routes'
        for file in files:
                if '.txt' not in file and keyword in file:
                    print(' file : ',yellow(file,bold=True))
                    html_output=html_output+'<li><b>'+file+' : <a href="/copy_route_into_project?script='+file+'">COPY to project</a>.---.<a href="/link_route_to_project?script='+file+'">LINK to project</a></b>'
        env.level=env.level[:-1]
        html_output=html_output+'</ul><br><br><a href="/stop">Click here to stop the App  </a></body><html>'
        return html_output
        
  


#  def_search_new_route_from_library_B***
@app.route('/search_new_route_from_library_B', methods=['GET'])
def search_new_route_from_library_B():
    '''
    Created : 2025-09-14

    description : Add a new function from central library to imported script
    '''
    route="/search_new_route_from_library_B"
    env.level+='-'
    print()
    print(env.level,white('route search_new_route_from_library_B() in ***app.py*** : >',bold=True))
    loguer(env.level+' route search_new_route_from_library_B() in ***app.py*** : >')
    print()
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        keyword=request.args.get('keyword')
        print('\nkeyword : ',keyword)      
        script=request.args.get('script')
        print()
        print('script : ',script)
        scriptdir=request.args.get('scriptdir')
        print()
        print('scriptdir : ',scriptdir)        
        with open('./result/home_url.txt') as file:
            home_url=file.read()
        html_output='<html><body><a href="'+home_url+'"><b><= back to home</b></a><br><form action="/search_search_new_route_from_library_B" method="get"><input type="text" name="keyword"><input type="hidden" name="script" value="'+script+'"><input type="hidden" name="scriptdir" value="'+scriptdir+'"><input type="submit" value="Search"></form><br><ul>';
        files =[file for file in os.listdir('./code_central_routes')]
        function_list=[]
        for file in files:
              if '.txt' not in file and keyword in file:
                print(' file : ',yellow(file,bold=True)) 
                html_output=html_output+'<li><b>'+file+' : <a href="/copy_route_into_project_B?script='+file+'&scriptdir='+scriptdir+'">COPY to project</a>.---.<a href="/link_route_to_project_B?script='+file+'&scriptdir='+scriptdir+'">LINK to project</a></b>'
        env.level=env.level[:-1]
        html_output=html_output+'</ul><br><br><a href="/stop">Click here to stop the App  </a></body><html>'
        return html_output      
      

#  def_bases***
@app.route('/bases', methods=['GET'])
def bases():
    '''
    Created : 2025-09-23T05:51:19.000Z
    description : display Databases Access Web Page
    '''
    route="/bases"
    env.level+='-'
    print('\n'+env.level,white('route bases() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route bases() in ***app.py*** : >')
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        route="/bases"
        title="FLASK APP GENERATOR"
        portfolio=''        
        if os.path.exists('./sqlite_databases_code/databases.txt'):     
            with open('./sqlite_databases_code/databases.txt') as file:
                text_content=file.read()
            databases=text_content.split('\n')
            for db in databases:
                if db!='':
                    with open('./sqlite_databases_code/'+db+'/db_description.txt') as file:   
                        description=file.read()
                    portfolio=portfolio+'''
                        <div class="col-4 col-6-medium col-12-small">
                            <article class="box style2">
                                <a href="/'''+db+'''_dashboard" class="image featured"><img src="../static/images/database0.png" alt="" /></a>
                                <h3><a href="/'''+db+'''_dashboard">'''+db+'''</a></h3>
                                <p>'''+description+'''</p>
                            </article>
                        </div>            
'''            
        portfolio=portfolio+'''                        <div class="col-4 col-6-medium col-12-small">
                            <article class="box style2">
                                <a href="/reset_databases" class="image featured"><img src="../static/images/database0.png" alt="" /></a>
                                <h3><a href="/reset_databases">Reset Databases</a></h3>
                                <p>Reset All Databases</p>
                            </article>
                        </div>
'''
        menu='''        
                    <li><a href="/">Back to main page</a></li>
                    <li><a href="/logout">log Out</a></li>
                    <li><a href="javascript:popup_window('/page_info?page=route_def_bases.py&route='''+route+'''','page_info',700,600);">:</a></li>
        '''       
        output='''<!DOCTYPE HTML>
<!-- description-->
<html>
    <head>
        <title>'''+title+'''</title>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no" />
        <link rel="stylesheet" href="../static/assets/css/main.css" />
    <script>
        function popup_window( url, id, width, height )
        {
            //extract the url parameters if any, and pass them to the called html
            var tempvar=document.location.toString(); // fetch the URL string
            var passedparams = tempvar.lastIndexOf("?");
            if(passedparams > -1)
                url += tempvar.substring(passedparams);
            popup = window.open( url, id, 'toolbar=no,scrollbars=yes,location=yes,statusbar=yes,menubar=no,resizable=yes,width=' + width + ',height=' + height + '' );
            popup.focus();
        }
    </script>
    </head>
    <body class="is-preload">
        <!-- Nav -->
            <nav id="nav">
                <ul>
                '''+menu+'''
                </ul>
            </nav>
        <!-- Portfolio -->
            <article id="portfolio" class="wrapper style3">
                <div class="container">
                    <header>
                        <h2>Databases</h2>
                    </header>
                    <div class="row">'''
        output=output+portfolio
        output=output+'''
                    </div>
                </div>
            </article>
        <!-- Scripts -->
            <script src="../static/assets/js/jquery.min.js"></script>
            <script src="../static/assets/js/jquery.scrolly.min.js"></script>
            <script src="../static/assets/js/init.js"></script>
            <script src="../static/assets/js/browser.min.js"></script>
            <script src="../static/assets/js/breakpoints.min.js"></script>
            <script src="../static/assets/js/util.js"></script>
            <script src="../static/assets/js/main.js"></script>
    </body>
</html>
'''
        loguer(env.level+' route END OF bases() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]
        return output


#  def_codegen_get_input_variable***
@app.route('/codegen_get_input_variable', methods=['GET'])
def codegen_get_input_variable():
    '''
    Created : 2025-09-22T07:47:39.000Z

    description : display formular for get input variable code generator
    '''
    route="/codegen_get_input_variable"
    env.level+='-'
    print('\n'+env.level,white('route codegen_get_input_variable() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route codegen_get_input_variable() in ***app.py*** : >')
    global client_id
    global client_password
    global host
    global host_for_token
    global profil_name
    if not session.get('logged_in'):
        return render_template('login.html')
    else:       
        message1="Message 1 :"
        image="../static/images/toolbox.png" 
        message2="Message 2 :"
        message3="/Message 3"
        message4="Message 4 in button"
        PAGE_DESTINATION="z_codegen_get_input_variable"
        page_name="z_codegen_get_input_variable.html"
        loguer(env.level+' route END OF codegen_get_input_variable() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]
        return render_template('main_index.html',route=route,USERNAME=session['user'],PAGE_DESTINATION=PAGE_DESTINATION,message1=message1,message2=message2,message3=message3,message4=message4,image=image,page_name=page_name)
        


#  def_codegen_input_variable_create***
@app.route('/codegen_input_variable_create', methods=['GET'])
def codegen_input_variable_create():
    '''
    Created : 2025-09-22T07:51:41.000Z

    description : create code for input variables
    '''
    route="/codegen_input_variable_create"
    env.level+='-'
    print('\n'+env.level,white('route codegen_input_variable_create() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route codegen_input_variable_create() in ***app.py*** : >')
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        # GET variable from calling web page
        variable=request.args.get('variable')
        print('\nvariable : ',variable)          
        output='''        # GET variable from calling web page
        '''+variable+'''=request.args.get("'''+variable+'''")
        print("\\n'''+variable+''' : ",'''+variable+''') 
        
        # POST variable 
        
        <input type="hidden" name="'''+variable+'''" >
         
        '''+variable+''' = request.form["'''+variable+'''"]
        print()
        print("\\n'''+variable+''' : ",'''+variable+''')  
        '''
        print('output :\n',cyan(output,bold=True))             
        message1="Message 1 :"
        image="../static/images/toolbox.png" 
        message2="Message 2 :"
        message3="/Message 3"
        message4="Message 4 in button"
        PAGE_DESTINATION="z_codegen_input_variable_create"
        page_name="z_codegen_input_variable_create.html"
        loguer(env.level+' route END OF codegen_input_variable_create() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]
        return render_template('main_index.html',route=route,USERNAME=session['user'],PAGE_DESTINATION=PAGE_DESTINATION,message1=message1,message2=message2,message3=message3,message4=message4,image=image,page_name=page_name,output=output)
        


#  def_codegen_sqlidb***
@app.route('/codegen_sqlidb', methods=['GET'])
def codegen_sqlidb():
    '''
    Created : 2025-09-22T07:21:17.000Z

    description : display the SQLITE DB Formular
    '''
    route="/codegen_sqlidb"
    env.level+='-'
    print('\n'+env.level,white('route codegen_sqlidb() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route codegen_sqlidb() in ***app.py*** : >')
    global client_id
    global client_password
    global host
    global host_for_token
    global profil_name
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        PAGE_DESTINATION="z_codegen_sqlidb"
        page_name="z_codegen_sqlidb.html"
        loguer(env.level+' route END OF codegen_sqlidb() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]
        return render_template('main_index.html',route=route,USERNAME=session['user'],PAGE_DESTINATION=PAGE_DESTINATION,page_name=page_name)
        


#  def_codegen_sqlidb_create***
@app.route('/codegen_sqlidb_create', methods=['GET'])
def codegen_sqlidb_create():
    '''
    Created : 2025-10-29
    description : create SQLITE DB Management structure and files and add it to the application
    '''
    route="/codegen_sqlidb_create"
    env.level+='-'
    print('\n'+env.level,white('route codegen_sqlidb_create() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route codegen_sqlidb_create() in ***app.py*** : >')
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        # GET variable from calling web page
        db_name=request.args.get("db_name")
        db_name=db_name.strip().lower()
        print("\ndb_name : ",db_name)
        # GET variable from calling web page
        table_name=request.args.get("table_name")
        print("\ntable_name : ",table_name)
        table_name.strip().lower()
        # GET variable from calling web page
        description=request.args.get("description")
        print("\ndescription : ",description)
        # GET variable from calling web page
        column_names=request.args.get("column_names")
        db_details={}
        db_details['db_name']=db_name
        db_details['table_name']=table_name
        db_details['description']=description
        if ',' in column_names:
            columns=column_names.split(',')
        else:
            columns=column_names.split(';')
        print("\ncolumns : ",columns)
        db_details['columns']=columns
        db_details_text=json.dumps(db_details,sort_keys=True,indent=4, separators=(',', ': '))
        if os.path.exists('./sqlite_databases_code/databases.txt'):
            print(green('OK ./sqlite_databases_code exists ',bold=True))
            if os.path.exists('./sqlite_databases_code/'+db_name+'/db_scripts.txt'):
                pass
            else:
                os.mkdir('./sqlite_databases_code/'+db_name)
                os.mkdir('./sqlite_databases_code/'+db_name+'/init')
                with open('./sqlite_databases_code/'+db_name+'/db_details.txt',"w") as file:
                    file.write(db_details_text)
                with open('./sqlite_databases_code/'+db_name+'/db_description.txt',"w") as file:
                    file.write(description)
                with open('./sqlite_databases_code/databases.txt',"a+") as file:
                    file.write(db_name+'\n')
        else:
            print(red('ERROR ./sqlite_databases_code doesn\'t exists ! Let\'s create it',bold=True))
            os.mkdir('./sqlite_databases_code')
            with open('./sqlite_databases_code/databases.txt',"w") as file:
                pass
            os.mkdir('./z_bases')
            with open('./z_bases/databases.txt',"w") as file:
                pass
            os.mkdir('./sqlite_databases_code/'+db_name)
            os.mkdir('./sqlite_databases_code/'+db_name+'/init')
            with open('./sqlite_databases_code/'+db_name+'/db_details.txt',"w") as file:
                file.write(db_details_text)
            with open('./sqlite_databases_code/'+db_name+'/db_description.txt',"w") as file:
                file.write(description)
            with open('./sqlite_databases_code/databases.txt',"a+") as file:
                file.write(db_name+'\n')
        '''
        if os.path.exists('./z_bases/store_sqllite_DBs.txt'):
            print(green('OK ./z_bases exists ',bold=True))
        else:
            print(red('ERROR ./z_bases doesn\'t exists ! Let\'s create it',bold=True))
            os.mkdir('./z_bases')
            with open('./z_bases/store_sqllite_DBs.txt',"w") as file:
                pass
        '''
        output='''\'\'\'
    create the '''+db_name+'''.csv csv file to be ingested into the DB for testing
\'\'\'
import sys
import sqlite3
from crayons import *
    
def create_csv_demos_data():    
    file=open(\'./init/'''+db_name+'''.csv\',\'w\')
    ligne_out=\''''
        for col in columns:
            output=output+col+','
        output=output[:-1]
        output=output+'''\'
    file.write(ligne_out)
    file.write(\'\\n\')
    for i in range (0,10):
        ligne_out=\''''
        len_columns=len(columns)-1
        i=0
        for col in columns:
            print(col)
            if i<len_columns:
                output=output+col+'''\'+str(i)+\',\'+\''''
            else:
                output=output+col+'''\'+str(i)'''
            i+=1
        output=output+'''
        file.write(ligne_out)
        file.write(\'\\n\')
    file.close()
 
if __name__==\'__main__\':
    create_csv_demos_data()
    print(green(\'DONE '''+db_name+'''.csv for demos data was created\',bold=True))
    '''
        with open('./sqlite_databases_code/'+db_name+'/y1_'+db_name+'_create_csv_demo_file_to_ingest_into_db.py','w') as file:
            file.write(output)
            
        output='''import sys
import csv
from crayons import *
import sqlite3
import os
import json
def create_connection(db_file):
    \'\'\' create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    \'\'\'
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn
   
def create_db_and_table():    
    #with sqlite3.connect(\':memory:\') as conn:
    with sqlite3.connect(\''''+db_name+'''.db\') as conn:
        c=conn.cursor()
        try:
            print("--- table : '''+table_name+''' creation")
            sql_create=f"CREATE TABLE IF NOT EXISTS '''+table_name+''' (`index` int PRIMARY KEY,'''
        len_columns=len(columns)-1
        i=0
        for col in columns:
            print(col)
            if i<len_columns:
                output=output+col+''' text ,'''
            else:
                output=output+col+''' text'''
            i+=1
        output=output+''')"
            c.execute(sql_create)
            print(green("--- OK '''+table_name+''' table created",bold=True))
        except:
            sys.exit(red("couldn\'t create '''+table_name+''' table",bold=True))
    return()    
    
def feed_database():
    database = os.getcwd()+\'/'''+db_name+'''.db\'
    database=database.replace("\\\\","/")
    print(\'database is :\',database)
    lines=[]    
    file=\'./init/'''+db_name+'''.csv\' 
    with open (file) as csvfile:
        reader = csv.reader(csvfile, delimiter=\',\')
        lines = list(reader)
        indexA=0
        print()
        print(\' '''+table_name+''' table =>\')
        print()
        for row in lines:
            #print (\'print the all row  : \' + row)
            print('''
        i=0
        for col in columns:
            print(col)
            if i<len_columns:
                output=output+'''row['''+str(i)+'''] ,'''
            else:
                output=output+'''row['''+str(i)+'''])'''
            i+=1
        output=output+'''
            #print(row)
            conn=create_connection(database) # open connection to database
            if conn:
                # connection to database is OK
                c=conn.cursor()
                # let\'s go to every lines one by one and let\'s extract url, targeted brand
                sqlite_data=(indexA,'''
        i=0
        for col in columns:
            print(col)
            if i<len_columns:
                output=output+'''row['''+str(i)+'''] ,'''
            else:
                output=output+'''row['''+str(i)+'''])\n                sql_add="INSERT OR IGNORE into '''+table_name+''' (`index`,'''
            i+=1
        i=0
        for col in columns:
            print(col)
            if i<len_columns:
                output=output+col+','
            else:
                output=output+col+') VALUES (?,'
            i+=1
        i=0
        for col in columns:
            print(col)
            if i<len_columns:
                output=output+'?,'
            else:
                output=output+'?)"'
            i+=1
        output=output+'''
                print()
                print('sql_add :',cyan(sql_add,bold=True))
                print()
                c.execute(sql_add, sqlite_data)
                print(green("==> OK Done",bold=True))
                indexA+=1
                            conn.commit()
        print()
        print(' ==> OK')
        print()
        
def reset_tables():
    conn=create_connection(\''''+db_name+'''.db\') # open connection to database
    if conn:
        # connection to database is OK
        c=conn.cursor()
        print(\'- Deleting table : '''+table_name+''' =>\')
        sql_request="drop table : '''+table_name+'''"
        c.execute(sql_request)
        conn.commit()
        print(\'-- OK DONE : Deleting table : '''+table_name+'''\')
        create_db_and_table()
        print(green(\'OK '''+table_name+'''.db created\',bold=True))
        print(yellow(\'Now ingest data into DB\',bold=True))
        feed_database()
        print(\'-- OK data ingested\')
        
def create_database_if_not_exits():
    try:
        database = os.getcwd()+\'/'''+db_name+'''.db\'
        database=database.replace("\\\\","/")
        print(\'database is :\',database)
        f = open(database)
        print(green("- OK the database exists",bold=True))
        f.close()
        rep=input(\' Do you want to create the '''+table_name+''' table ( Y/N ) ? : \')
        if rep==\'Y\':
            print(\'-- Ok let\\'s Create table : '''+table_name+'''\')
        create_db_and_table()
        print(green(\'-- Ok Done - '''+table_name+''' table succesfuly created \',bold=True))
        rep=input(\' Do you want to ingest demo data from ./init/'''+db_name+'''.csv ( Y/N ) ? : \')
        if rep==\'Y\':
            print(\'-- Ingest demo data into table : '''+table_name+'''\')
            feed_database()
            print(green(\'-- OK  Demo data succesfuly ingested into table : '''+table_name+'''\',bold=True))
    except IOError:
        print(red("- NOK the database DO NOT exists... let\'s create it",bold=True))
        print(\'Create '''+db_name+'''.db and table : '''+table_name+'''\')
        create_db_and_table()
        print(\'-- OK  Database and table created\')
        print()
        rep=input(\' Ingest demo data from ./init/'''+db_name+'''.csv ( Y/N ) ? : \')
        if rep!=\'N\':
            print(\'-- Ingest demo data into table : '''+table_name+'''\')
            feed_database()
            print(\'-- OK  Demo data ingested into table : '''+table_name+'''\')
        
if __name__ == "__main__":
    create_database_if_not_exits()
            print(\'ALL DONE\')
        '''
        with open('./sqlite_databases_code/'+db_name+'/y2_'+db_name+'_create_db_read_csv_to_db_line_by_line.py','w') as file:
            file.write(output)
        output='''import pandas as pd
import sqlalchemy
from pandas import DataFrame
# sqlite:///:memory: (or, sqlite://)
# sqlite:///relative/path/to/file.db
# sqlite:////absolute/path/to/file.db
db_name = "'''+db_name+'''.db"
table_name = "'''+table_name+'''"
engine = sqlalchemy.create_engine("sqlite:///%s" % db_name, execution_options={"sqlite_raw_colnames": True})
df = pd.read_sql_table(table_name, engine)
out_df = df[[\''''
        i=0
        for col in columns:
            print(col)
            if i<len_columns:
                output=output+col+"','"
            else:
                output=output+col+"']]"
            i+=1
        output=output+'''
#save result to csv file
out_df.to_csv(r\''''+db_name+'''.csv\')
df = DataFrame(out_df)
print (df)
print(\'=========================================\')
print(\'DONE\')
            '''
        with open('./sqlite_databases_code/'+db_name+'/y3_'+db_name+'_read_sqlite_db_and_create_csv.py','w') as file:
            file.write(output)
        output='''import pandas as pd
from sqlalchemy import create_engine
# the csv file is : '''+db_name+'''.csv
# database will be : '''+db_name+'''.db
# the table name is  : '''+table_name+'''
df = pd.read_csv(\''''+db_name+'''s.csv\', sep=\',\')
# sqlite:///:memory: (or, sqlite://)
# sqlite:///relative/path/to/file.db
# sqlite:////absolute/path/to/file.db
engine = create_engine(\'sqlite:///'''+db_name+'''.db\')
df.to_sql(\''''+table_name+'''\', engine) #With this one the table and database must not already exists
#df.to_sql(\''''+table_name+'''\', con=engine, if_exists=\'append\')   #with this one you can append data to an existing database
#df.to_sql(\''''+table_name+'''\', con=engine, if_exists=\'replace\')   #with this one you can truncat an existing database
'''
        with open('./sqlite_databases_code/'+db_name+'/y4_'+db_name+'_ingest_csv_into_sqlite_db_panda.py','w') as file:
            file.write(output)
        output='''from crayons import *
from array import array
def clean_text_file(file):
    print(red(file))
    print()
    line_out=""
    with open( file, \'rb\' ) as file:
        data = array( \'B\', file.read() ) # buffer the file
        list=[147,148]
                for byte in data:
            v = byte # int value
            if v > 140 and v < 160:
                #print(red(f"{v} : {c}"))
                #print(c)
                c = chr(32)
            elif v == 226:
                #print(yellow(f"{v} : {c}"))
                c = chr(32)
                #print(c)
            elif v == 255:
                #print(yellow(f"{v} : {c}"))
                c = chr(46)
                        #print(c)
            elif v not in list:
                c = chr(byte)
            else:
                c = chr(39)
            #print(yellow(f"{v} : {c}"))
            #print(c)
            line_out+=c
    return(line_out)
    
def csv_file_cleaning(fichier):
    text_out=clean_text_file(fichier)
    list_lines=text_out.split(\'\\n\')
    new_file_name=\'./init/'''+db_name+'''.csv\'
    #new_file_name=\'./init/clean_'''+db_name+'''.csv\'
    print(red(new_file_name,bold=True))
    with open(new_file_name,\'w\',encoding=\'utf-8\') as fich:
        for line in list_lines:
            line=line.strip()
            if line!=\'\':
                print(line)
                fich.write(line+\'\\n\')
    print()
    print()    
    print(cyan(\'================ Original CSV file cleaning DONE ==================\',bold=True))
    print()     
    
if __name__ == "__main__":
    csv_file_cleaning(\'./init/'''+db_name+'''.txt\')
        print(\'ALL DONE\')
        '''
        with open('./sqlite_databases_code/'+db_name+'/y5_'+db_name+'_normalize_original_file.py','w') as file:
            file.write(output)
        output='''\'\'\'
    this resource manages interaction with the sqllite database
\'\'\'
import sys
import sqlite3
from crayons import *
from datetime import datetime, timedelta
import time
import json
def date_time():
    \'\'\'
        get current date time in yy-mm-dd-H:M:S:fZ format
    \'\'\'
    current_time = datetime.utcnow()
    current_time = current_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    current_date=current_time.split(\'T\')[0]
    return(current_time,current_date)
def create_connection(db_file):
    \'\'\' create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    \'\'\'
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn    
    
def read_db(database,table,where_clause):
    liste=[]
    with sqlite3.connect(database) as conn:
        cursor=conn.cursor()
        sql_request = f"SELECT * from {table} {where_clause}"
        print()
        print(sql_request)
        print()
        try:
            cursor.execute(sql_request)
            for resultat in cursor:
                #print(resultat)
                liste.append(resultat)
        except:
            sys.exit("couldn\'t read database")
    return(liste) 
    
def update_db_generic(database,table,where_clause,data):
    liste=[]
    with sqlite3.connect(database) as conn:
        cursor=conn.cursor()
        sql_request = f"UPDATE {table} SET "
        for key,value in data.items():
            print(cyan(key))
            print(red(value))
            sql_request =sql_request + key +" = \'"+value+"\',"
        sql_request=sql_request[:-1]
        if where_clause!=\'\':
            sql_request=sql_request+\' where \'+where_clause
        print()
        print(sql_request)
        print()
        try:
            cursor.execute(sql_request)
            print("Execute UPDATE IN DB")
        except:
            sys.exit("couldn\'t execute update on database")
    return(1)  
def update_db2(database,table,where_clause,sql_fields,sql_data_list):
    liste=[]
    with sqlite3.connect(database) as conn:
        cursor=conn.cursor()
        sql_data=(\'\')
        sql_data=sql_data_list
        sql_request = f"UPDATE {table} SET "
        for item in sql_fields:
            sql_request =sql_request + item +" = ? , "
        sql_request=sql_request[:-2]
        if where_clause!=\'\':
            sql_request=sql_request+\' where \'+where_clause
        print()
        print(sql_request)
        print()
        try:
            cursor.execute(sql_request)
            print("Execute UPDATE IN DB")
        except:
            sys.exit("couldn\'t execute update on database")
    return(1)     
def read(database,table):    
    file=open(\'out.txt\',\'w\')
    where=\' where selected = "YES"\'
    where=\'\'
    resultats = read_db(database,table,where)    
    if resultats :
        for resultat in resultats:
            print(resultat)
            ligne_out=resultat[0]+\';\'+resultat[1]+\';\'+resultat[2]+\';\'+resultat[3]+\';\'+resultat[4]
            file.write(ligne_out)
            file.write(\'\\n\')
    else:
        print(\'NO RESULTS\')
    file.close()
def delete_row(db_name,table_name,id):
    con = sqlite3.connect(db_name)
    sql=f"DELETE FROM \'{table_name}\' WHERE `index`=?"
    #print(sql)
    try:
        cur = con.cursor()
        cur.execute(sql, (id,))
        con.commit()
        return 1
    except:
        return 0
def delete_from_db(database,table,where_clause):
    con = sqlite3.connect(database)
    print()
    print(\'database :\','''+db_name+''')     
    print(\'table :\','''+table_name+''')    
    print(\'where clause :\',where_clause)
    
    sql=f"DELETE FROM {table} where {where_clause}"
    print()
    print(yellow(sql,bold=True))
    print()    
    try:
        cur = con.cursor()
        cur.execute(sql)
        con.commit()
        print(green(\'OK DONE\',bold=True))
        return 1
    except:
        print(red(\'Error\',bold=True))
        return 0
        
def drop_table(database,table):
    conn=create_connection(database) # open connection to database
    if conn:
        # connection to database is OK
        c=conn.cursor()
        print(\'- Deleting table : '''+table_name+''' =>\')
        sql_request="drop table '''+table_name+'''"
        c.execute(sql_request)
        conn.commit()
        print(\'-- OK DONE : table : '''+table_name+''' Deleted \')
def reset_table(database,table):
    conn=create_connection(database) # open connection to database
    if conn:
        # connection to database is OK
        c=conn.cursor()
        try:
            print("-- try to create : '''+table_name+''' in case it does not exit")
            sql_create=f"CREATE TABLE IF NOT EXISTS '''+table_name+''' ( `index` int PRIMARY KEY,'''
        i=0
        for col in columns:
            print(col)
            if i<len_columns:
                output=output+col+''' text ,'''
            else:
                output=output+col+''' text)"'''
            i+=1
        output=output+'''
            c.execute(sql_create)
            print("--- OK '''+table_name+''' table created")
        except:
            sys.exit("couldn\'t create '''+db_name+'''.db")
        print(\'- Deleting table : '''+table_name+''' =>\')
        sql_request="drop table '''+table_name+'''"
        c.execute(sql_request)
        conn.commit()
        print(\'-- OK DONE : table : '''+table_name+''' Deleted \')
        try:
            print("-- create table : network_objects")
            sql_create=f"CREATE TABLE IF NOT EXISTS '''+table_name+''' ( `index` int PRIMARY KEY,'''
        i=0
        for col in columns:
            print(col)
            if i<len_columns:
                output=output+col+''' text ,'''
            else:
                output=output+col+''' text)"'''
            i+=1
            output=output+'''
            c.execute(sql_create)
            print("--- OK network_objects table created")
        except:
            sys.exit("couldn\'t create '''+db_name+'''.db")
        
def insert_new_row(row,database,table): # row is a list of items
    print()
    print(cyan("insert a new row into DB",bold=True))
            print(row)
    conn=create_connection(database) # open connection to database
    if conn:
        # connection to database is OK
        # STEP 1 get the number of item in the database in order to calculate the next index
        where=\'\'
        resultats = read_db(database,table,where)
        nb=0
        if resultats :
            for resultat in resultats:
                #print(resultat)
                nb+=1
        else:
            print(\'NO RESULTS\')
        # STEP 2 : add the new item into the database
        indexA=nb+1
        sqlite_data=(indexA,'''
        i=0
        for col in columns:
            print(col)
            if i<len_columns:
                output=output+'''row['''+str(i)+'''] ,'''
            else:
                output=output+'''row['''+str(i)+'''])\n                sql_add="INSERT OR IGNORE into '''+table_name+''' (`index`,'''
            i+=1
        i=0
        for col in columns:
            print(col)
            if i<len_columns:
                output=output+col+','
            else:
                output=output+col+') VALUES (?,'
            i+=1
        i=0
        for col in columns:
            print(col)
            if i<len_columns:
                output=output+'?,'
            else:
                output=output+'?)"'
            i+=1
        output=output+'''
        conn.execute(sql_add, sqlite_data)
        conn.commit()
        print(green("OK DONE",bold=True))
        
def create_database_if_not_exits():
    try:
        database = os.getcwd()+\'/'''+db_name+'''.db\'
        database=database.replace("\\\\","/")
        print(\'database is :\',database)
        f = open(database)
        print(green("- OK the database exists",bold=True))
        f.close()
        rep=input(\' Do you want to create the '''+table_name+''' table ( Y/N ) ? : \')
        if rep==\'Y\':
            print(\'-- Create table : '''+table_name+'''\')
        create_db_and_table()
        print(\'-- Ok Done - '''+table_name+''' table succesfuly created \')
        rep=input(\' Do you want to ingest demo data from ./init/'''+db_name+'''.csv ( Y/N ) ? : \')
        if rep==\'Y\':
            print(\'-- Ingest demo data into table : '''+table_name+'''\')
            feed_database()
            print(\'-- OK  Demo data succesfuly ingested into table : '''+table_name+'''\')
    except IOError:
        print(red("- NOK the database DO NOT exists... let\'s create it",bold=True))
        print(\'Create '''+db_name+'''.db and table : '''+table_name+'''\')
        create_db_and_table()
        print(\'-- OK  Database and table created\')
        print()
        rep=input(\' Ingest demo data from ./init/'''+db_name+'''.csv ( Y/N ) ? : \')
        if rep==\'Y\':
            print(\'-- Ingest demo data into table : '''+table_name+'''\')
            feed_database()
            print(\'-- OK  Demo data ingested into table : '''+table_name+'''\')
        
\'\'\'    
if __name__==\'__main__\':
    database="'''+db_name+'''.db"
    table="'''+table_name+'''"
    #main(database,table)   
    client_name=\'ACME COMPANY\'
    #update_client_db(database,table,client_name)
    id=0
    #delete_row(id)
\'\'\'
        '''
        with open('./sqlite_databases_code/'+db_name+'/y6_'+db_name+'_read_write_sqlite_database.py','w') as file:
            file.write(output)
        output='''\'\'\'
    use functions that are into y6_trace_read_write_sqlite_database.py
    
    and manages Data in sqliteDB
\'\'\'
import sys
import csv
import sqlite3
from crayons import *
from y6_'''+db_name+'''_read_write_sqlite_database import read_db,update_db_generic,delete_row,read,insert_new_row
database="'''+db_name+'''.db"
table="'''+table_name+'''"
def get_rows():
    print()
    print(cyan("Read DB and select item in database to be displayed",bold=True))
    where_clause=" where `index`<10"
    #where_clause=" where `time`=\'time4\'"
    #where_clause=" group by event"
    #print(\'where clause :\',where_clause)
    result=read_db(database,table,where_clause)
    #print(cyan(result))
    for item in result:
        print
        print(yellow(item,bold=True))
        print()
    print(green("Done",bold=True))
    return(result)
def add_row():
    liste=[\'name10\',\'address10\',\'local_contacts10\',\'ftd_list10\',\'description10\',\'version10\']    
    insert_new_row(liste,database,table)
def update_db():
    # data and field are passed thru a dictionnary    
    data_to_set={"device_type":"red_cross","color":"PAT2","c3":"PAT3"}
    where="c2 = \'hitch_hacker-B\' and device_type = \'expand\'"
    update_db_generic(database,table,where,data_to_set)
    
def update_db2():
    # data and field are passed thru 2 lists, one for field ans one for data
    data_list=["red_cross","PAT2","PAT3"]
    field_list=["device_type","color","c3"]
    where="c2 = \'hitch_hacker-B\' and device_type = \'expand\'"
    update_db2(database,table,where,field_list,data_to_set)
def delete_objects():
    where="c2 = \'one_to_many_policy_matrix\' and y = \'-172\'"
    #where="c2 = \'policy-draft-1\' and device_type = \'arrow_green_round\'"
    delete_from_db(database,table,where)
    
if __name__==\'__main__\':
    #get_rows()
    #add_row()
        #update_db()
'''
        with open('./sqlite_databases_code/'+db_name+'/y7_'+db_name+'_example_of_queries.py','w') as file:
            file.write(output)
        #
        # Create sub scripts structure here under
        #
        create_rte_for_db_dashboard(db_name)
        create_rte_for_create_db(db_name)
        create_rte_for_db_demo_data(db_name)
        create_rte_for_db_clear_function(db_name)
        create_rte_for_db_read_function(db_name)
        create_rte_for_db_update_entry_function(db_name)
        create_rte_for_db_delete_entry_function(db_name)
        create_rte_for_db_add_entry_function(db_name)
        create_rte_for_db_ingest_cvs(db_name)
        create_rte_for_sqlite_db_duplicate_entry_function(db_name)
        message1="SQLITE DB CREATED"
        image="../static/images/ok.png"
        message2="SQLITE DB structure and files had been created and added into this application."
        message3="/stop"
        message4="YOU MUST RESTART FLASK !!"
        PAGE_DESTINATION="operation_done"
        page_name="operation_done.html"
        loguer(env.level+' route END OF codegen_sqlidb_create() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]
        return render_template('main_index.html',route=route,USERNAME=session['user'],PAGE_DESTINATION=PAGE_DESTINATION,message1=message1,message2=message2,message3=message3,message4=message4,image=image,page_name=page_name)
        


#  def_create_route_for_db_template***
def create_route_for_db_template(name):
    '''
    MODIFIED : 2025-09-23T09:20:21.000Z
    description : Ingest demo data into the database
    
    how to call it : result=create_route_for_db_template(name)
    '''
    route="/create_route_for_db_template"
    env.level+='-'
    print('\n'+env.level,white('def create_route_for_db_template() in app.py : >\n',bold=True))
    loguer(env.level+' def create_route_for_db_template() in app.py : >')
    # ===================================================================    
    db=name
    db_name=name.replace('./zbases/','')
    db_name=db_name.replace('.db','')
    name=name+'_ingest_demo_data'
    filename='./code_app_routes/route_def_'+name+'.py'
    filename2='/route_def_'+name+'.py'
    description='Flask Route for the '+name+' Database Create DB action'
    print()
    print(' filename :\n',yellow(filename,bold=True))
    print()
    print(' filename2 :\n',yellow(filename2,bold=True))
    print()
    print(' description :\n',yellow(description,bold=True))
    print()
    print(magenta('--> CALL  A SUB FUNCTION :',bold=True))
    # check if file already exits
    with open('./code_architecture/app_routes.txt') as file:
        text_content2=file.read()
    fichier_route = Path('./code_app_routes/route_def_'+name+'.py')    
    if fichier_route.is_file() or filename in text_content2:
        print(filename+' already exists ! Choose another name')
        PAGE_DESTINATION="operation_done"
        page_name="z_operation_done.html"
        loguer(env.level+' route END OF example_name() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]
        return 0
    else:
        print(yellow(f'     {filename} does NOT exists. Let s create it',bold=True))
        route="/"+db+"action"
        title="FLASK APP GENERATOR"
        with open('./sqlite_databases_code/'+db_name+'/db_details.txt') as file:
            db_details_dict=json.loads(file.read())
        print('db_details_dict : \n',yellow(db_details_dict,bold=True))
        
        menu='''
                    <li><a href="/">Back to main page</a></li>
                    <li><a href="/logout">log Out</a></li>
                    <li><a href="javascript:popup_window('/page_info?page=route_def_'''+db+'''action.py&route='''+route+'''','page_info',700,600);">:</a></li>
        '''
        output='''<!DOCTYPE HTML>
<!-- description-->
<html>
    <head>
        <title>'''+title+'''</title>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no" />
        <link rel="stylesheet" href="../static/assets/css/main.css" />
    <script>
        function popup_window( url, id, width, height )
        {
            //extract the url parameters if any, and pass them to the called html
            var tempvar=document.location.toString(); // fetch the URL string
            var passedparams = tempvar.lastIndexOf("?");
            if(passedparams > -1)
                url += tempvar.substring(passedparams);
            popup = window.open( url, id, 'toolbar=no,scrollbars=yes,location=yes,statusbar=yes,menubar=no,resizable=yes,width=' + width + ',height=' + height + '' );
            popup.focus();
        }
    </script>
    </head>
    <body class="is-preload">
        <!-- Nav -->
            <nav id="nav">
                <ul>
                '''+menu+'''
                </ul>
            </nav>
        <!-- Portfolio -->
            <article id="top" class="wrapper style1">
                <div class="container">
                    <div class="row">
                        <div class="col-4 col-5-large col-12-medium">
                            <span class="image fit"><img src="../static/images/ok.png" alt="" /></span>
                        </div>
                        <div class="col-8 col-7-large col-12-medium">
                            <header>
                                <h1><strong>Demo Data ingested</strong></h1>
                            </header>
                            <p>Demo Data ingested into Database :'''+db+'''</p>
                            <a href="/'''+db+'''_dashboard" class="button small scrolly">Go to Dashboard for '''+db+''' DB </a>
                        </div>
                    </div>
                </div>
            </article>
        <!-- Scripts -->
            <script src="../static/assets/js/jquery.min.js"></script>
            <script src="../static/assets/js/jquery.scrolly.min.js"></script>
            <script src="../static/assets/js/init.js"></script>
            <script src="../static/assets/js/browser.min.js"></script>
            <script src="../static/assets/js/breakpoints.min.js"></script>
            <script src="../static/assets/js/util.js"></script>
            <script src="../static/assets/js/main.js"></script>
    </body>
</html>
'''
        text_content='''#  def_'''+db+'''_ingest_demo_data***
@app.route('/'''+db+'''_ingest_demo_data', methods=['GET'])
def '''+db+'''_ingest_demo_data():
    \'\'\'
    '''+description+'''
    \'\'\'
    route="/'''+db+'''_ingest_demo_data"
    env.level+=\'-\'
    print(\'\\n\'+env.level,white(\'route '''+db+'''_ingest_demo_data() in ***app.py*** : >\\n\',bold=True))
    loguer(env.level+\' route '''+db+'''_ingest_demo_data() in ***app.py*** : >\')
    if not session.get(\'logged_in\'):
        return render_template(\'login.html\')
    else:
        with open(\'./sqlite_databases_code/'''+db+'''/db_details.txt\') as file:
            db_details_dict=json.loads(file.read())
        print(\'db_details_dict : \\n\',yellow(db_details_dict,bold=True))
        database = os.getcwd()+\'/z_bases/'''+db+'''.db\'
        database=database.replace("\\\\","/")
        print(\'database is :\',database)
        lines=[]
        file=\'./sqlite_databases_code/'''+db+'''/init/'''+db+'''.csv\'
        with open (file) as csvfile:
            reader = csv.reader(csvfile, delimiter=\',\')
            lines = list(reader)
            indexA=0
            print(\''''+db_details_dict['table_name']+''' table =>\\n\')
            for row in lines:
                conn=create_connection(database) # open connection to database
                if conn:
                    # connection to database is OK
                    c=conn.cursor()
                    # let\'s go to every lines one by one and let\'s extract url, targeted brand
                    sqlite_data=[indexA]
                    len_columns=len(db_details_dict[\'columns\'])-1
                    sqlite_data=(indexA,'''
        len_columns=len(db_details_dict['columns'])-1
        i=0
        for col in db_details_dict['columns']:
            if i<len_columns:
                text_content=text_content+'row['+str(i)+'] ,'
            else:
                text_content=text_content+'row['+str(i)+'])\n                    sql_add="INSERT OR IGNORE into '
                text_content=text_content+db_details_dict['table_name']+' (`index`,'
            i+=1
        len_columns=len(db_details_dict['columns'])-1
        i=0
        for col in db_details_dict['columns']:
            if i<len_columns:
                text_content=text_content+col+','
            else:
                text_content=text_content+col+') VALUES (?,'
            i+=1
        i=0
        for col in db_details_dict['columns']:
            if i<len_columns:
                text_content=text_content+'?,'
            else:
                text_content=text_content+'?)"'
            i+=1
        text_content=text_content+'''
                    print('\\nsql_add :',cyan(sql_add,bold=True))
                c.execute(sql_add, sqlite_data)
                print(green("==> OK Done : demo data ingested",bold=True))
                indexA+=1
                conn.commit()
        '''
        text_content=text_content+'''
        html_output=\'\'\''''+output+'''\'\'\'
        loguer(env.level+\' route END OF '''+db+'''_ingest_demo_data() in ***app.py*** : >\')
        # ===================================================================
        env.level=env.level[:-1]
        return html_output
        '''
        filename='./code_app_routes/route_def_'+db+'_ingest_demo_data.py'
        with open(filename,"w") as fichier:
            fichier.write(text_content)
        with open('./code_architecture/app_routes.txt',"a+") as fichier:
            filename2=filename2.replace('/','')
            fichier.write(filename2+'\n')
        result=1
    # ===================================================================
    loguer(env.level+' def END OF create_route_for_db_template() in app.py : >')    
    env.level=env.level[:-1]
    return result
    


#  def_db_row_details***
@app.route('/db_row_details', methods=['GET'])
def db_row_details():
    '''
    Created : 2025-10-26
    description : 
    '''
    route="/db_row_details"
    env.level+='-'
    print('\n'+env.level,white('route db_row_details() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route db_row_details() in ***app.py*** : >')
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        # GET variable from calling web page
        row=request.args.get("row")
        print("\nrow : ",row)
        database=request.args.get("database")
        print("\ndatabase : ",database)
        table=request.args.get("table")
        print("\ntable : ",table)
        columns=request.args.get("columns")
        print("\ncolumns : ",columns)
        column_list=columns.split(',')
        where_clause='where `index` = '+row
        entry_list=sqlite_db_select_entry(database,table,where_clause)
        print("\nentry_list : \n",entry_list)
        items={}
        i=0
        for obj in entry_list[0]:
            if i<len(column_list):
                items[i]={'name':column_list[i],'value':entry_list[0][i+1]}
            i+=1
        print('items : ',cyan(items,bold=True))
        PAGE_DESTINATION="z_db_display_entry_details"
        page_name="z_db_display_entry_details.html"
        loguer(env.level+' route END OF db_row_details() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]
        return render_template('main_index.html',route=route,USERNAME=session['user'],PAGE_DESTINATION=PAGE_DESTINATION,page_name=page_name,items=items,db_name=database,row=row)
        


#  def_sqlite_ingest_csv***
@app.route('/sqlite_ingest_csv', methods=['GET','POST'])
def sqlite_ingest_csv():
    '''
    Created : 2025-10-10
    description : download a csv file and store it into ./tmp
    '''
    route="/sqlite_ingest_csv"
    env.level+='-'
    print('\n'+env.level,white('route sqlite_ingest_csv() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route sqlite_ingest_csv() in ***app.py*** : >')
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        result=0
        db_name = request.form['db_name']
        print("\ndb_name : ",db_name)
        action_type = request.form['action_type']
        print("\naction_type : ",action_type)        
        # download the CSV file
        if request.method == 'POST':
            if 'file' not in request.files:
                return redirect(request.url)
            file = request.files['file']
            if file.filename == '':
                return redirect(request.url)
            if file:
                filename = file.filename
                print('filename : ',filename+'\n')
                filename='csv_file.csv'
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                result=1
        # Prepare the resulting Next Web Page
        
        if result==1:
            with open('./sqlite_databases_code/'+db_name+'/db_details.txt') as file:
                db_details_dict=json.loads(file.read())
            print('db_details_dict : \n',yellow(db_details_dict,bold=True))
            database = os.getcwd()+'/z_bases/'+db_name+'.db'
            database=database.replace("\\","/")
            print('database is :',database)
            print('table is :',db_details_dict['table_name'])
            lines=[]
            file='./temp/csv_file.csv'
            with open (file) as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                lines = list(reader)
                if action_type=="replace":
                    conn=create_connection(database) # open connection to database
                    if conn:
                        # connection to database is OK
                        c=conn.cursor()
                        print(f'- Deleting table : {db_details_dict["table_name"]} =>')
                        sql_request="drop table "+db_details_dict["table_name"]
                        c.execute(sql_request)
                        conn.commit()
                        print('-- OK DONE : Deleted table : '+db_details_dict["table_name"])
                        create_db_and_table(db_details_dict["db_name"],db_details_dict["table_name"])
                        print(f'-- OK table {db_details_dict["table_name"]} reseted')                  
                    indexA=0
                else:
                    indexA=sqlite_db_get_last_index(db_name)+1
                conn=create_connection(database) # open connection to database
                for row in lines:
                    if conn:
                        # connection to database is OK
                        c=conn.cursor()
                        # let's go to every lines one by one and let's extract url, targeted brand
                        len_columns=len(db_details_dict['columns'])-1
                        sqlite_data=[indexA]
                        for cel in row:
                            sqlite_data.append(cel)
                        print('\nsqlite_data :',cyan(sqlite_data,bold=True))
                        sql_add=f"INSERT OR IGNORE into {db_details_dict['table_name']} (`index`,"
                        i=0
                        for col in db_details_dict['columns']:
                            print(col)
                            if i<len_columns:
                                sql_add=sql_add+col+","
                            else:
                                sql_add=sql_add+col+")"
                            i+=1
                        sql_add=sql_add+' VALUES (?,'
                        i=0
                        for col in db_details_dict['columns']:
                            print(col)
                            if i<len_columns:
                                sql_add=sql_add+"?,"
                            else:
                                sql_add=sql_add+'?)'
                            i+=1
                        #sql_add="INSERT OR IGNORE into truc (`index`,premier,deuxieme,troisieme,quatrieme) VALUES (?,?,?,?,?)"
                        print('\nsql_add :',cyan(sql_add,bold=True))
                    c.execute(sql_add, sqlite_data)
                    print(green("==> OK Done : demo data ingested",bold=True))
                    indexA+=1
                    conn.commit()
            image="../static/images/ok.png"
            message1="Database Updated"
            message2="CSV file is in [ ./temp ]"
            message3=f"/{db_name}_dashboard"
            message4=f"{db_name}_dashboard"
        else:
            image="../static/images/nok.png"
            message1="ERROR"
            message2="File Not downloaded"
            message3="/"
            message4="Home"
        PAGE_DESTINATION="z_sqlite_ingest_csv_result"
        page_name="z_sqlite_ingest_csv_result.html"
        loguer(env.level+' route END OF sqlite_ingest_csv() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]
        return render_template('main_index.html',route=route,USERNAME=session['user'],PAGE_DESTINATION=PAGE_DESTINATION,message1=message1,message2=message2,message3=message3,message4=message4,image=image,page_name=page_name)
        


# def_index***
@app.route('/', methods=['GET'])
def index():
    '''
    Created : 2025-07-19
    description : for displaying the landing page where users land just after login
    '''
    route="/"
    env.level+='-'
    print()
    print(env.level,white('route index() in ***app.py*** : >',bold=True))
    loguer(env.level+' route index() in ***app.py*** : >')
    print()
    global client_id
    global client_password
    global host
    global host_for_token
    global profil_name
    if not session.get('logged_in'):
        env.level=env.level[:-1]
        return render_template('login.html')
    else:
        print()
        print(yellow("- OK Logged In",bold=True))
        print()
        result=1
        if result==1:
            image="../static/images/automation.png"
            message1="Automate Threat Hunting Operations"
            message2=""
            message3="/do_something"
            message4="Do something"
        elif result==2:
            image="../static/images/nok.png"
            message1="message1"
            message2="message2"
            message3="#message3"
            message4="message4"
        else:
            image="../static/images/nok.png"
            message1="message1 to customize in def index()"
            message2="message2 to customize in def index()"
            message3="/do_something"
            message4="message4 to customize in def index()"
        PAGE_DESTINATION="index"
        page_name="index.html"
        env.level=env.level[:-1]
        return render_template('main_index.html',USERNAME=session['user'],PAGE_DESTINATION=PAGE_DESTINATION,image=image,message1=message1,message2=message2,message3=message3,message4=message4,page_name=page_name,route=route)


#  def_nice_gui_1***
@app.route('/nice_gui_1', methods=['GET'])
def nice_gui_1():
    '''
    Created : 2025-07-31T15:38:40.000Z

    description : display the nice gui example 1
    '''
    route="/nice_gui_1"
    env.level+='-'
    print('\n'+env.level,white('route nice_gui_1() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route nice_gui_1() in ***app.py*** : >')
    global client_id
    global client_password
    global host
    global host_for_token
    global profil_name
    if not session.get('logged_in'):
        return render_template('login.html')
    else:            
        message1="Message 1 :"
        image="../static/images/toolbox.png" 
        message2="Message 2 :"
        message3="/Message 3"
        message4="Message 4 in button"
        PAGE_DESTINATION="z_nice_gui_1"
        page_name="z_nice_gui_1.html"
        # ===================================================================
        env.level=env.level[:-1]
        return render_template('main_index.html',route=route,USERNAME=session['user'],PAGE_DESTINATION=PAGE_DESTINATION,message1=message1,message2=message2,message3=message3,message4=message4,image=image,page_name=page_name)
        


#  def_codegen***
@app.route('/codegen', methods=['GET'])
def codegen():
    '''
    Created : 2025-09-22T07:17:49.000Z

    description : display code generator web page
    '''
    route="/codegen"
    env.level+='-'
    print('\n'+env.level,white('route codegen() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route codegen() in ***app.py*** : >')
    global client_id
    global client_password
    global host
    global host_for_token
    global profil_name
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        # ===================================================================       
        message1="Message 1 :"
        image="../static/images/toolbox.png" 
        message2="Message 2 :"
        message3="/Message 3"
        message4="Message 4 in button"
        PAGE_DESTINATION="z_codegen"
        page_name="z_codegen.html"
        loguer(env.level+' route END OF codegen() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]
        return render_template('main_index.html',route=route,USERNAME=session['user'],PAGE_DESTINATION=PAGE_DESTINATION,message1=message1,message2=message2,message3=message3,message4=message4,image=image,page_name=page_name)
        


#  def_codegen_flask_app***
@app.route('/codegen_flask_app', methods=['GET'])
def codegen_flask_app():
    '''
    Created : 2025-09-22T07:21:17.000Z

    description : display the SQLITE DB Formular
    '''
    route="/codegen_flask_app"
    env.level+='-'
    print('\n'+env.level,white('route codegen_flask_app() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route codegen_flask_app() in ***app.py*** : >')
    global client_id
    global client_password
    global host
    global host_for_token
    global profil_name
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        PAGE_DESTINATION="z_codegen_flask_app"
        page_name="z_codegen_flask_app.html"
        loguer(env.level+' route END OF codegen_flask_app() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]
        return render_template('main_index.html',route=route,USERNAME=session['user'],PAGE_DESTINATION=PAGE_DESTINATION,page_name=page_name)
        


#  def_codegen_flask_app_create***
@app.route('/codegen_flask_app_create', methods=['GET'])
def codegen_flask_app_create():
    '''
    Created : 2025-09-29
    description : Create the Flask Application Structure as an imported script
    '''
    route="/codegen_flask_app_create"
    env.level+='-'
    print('\n'+env.level,white('route codegen_flask_app_create() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route codegen_flask_app_create() in ***app.py*** : >')
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        # ===================================================================
        # GET variable from calling web page
        name=request.args.get("name")
        print("\nname : ",name)
        name=name.replace(' ','_')
        description=request.args.get("description")
        print("\ndescription : ",description)
        filename = request.args.get('name')
        port=request.args.get("port")
        print("\nport : ",port) 
        protocol=request.args.get("protocol")
        print("\nprotocol : ",protocol)         
        if '.py' not in filename:
            filename=filename+'.py'
        description = request.args.get('description')
        print()
        print(' filename :\n',yellow(filename,bold=True))
        print()
        print(' description :\n',yellow(description,bold=True))
        print()
        with open('./code_architecture/imported_scripts.txt') as file:
            text_content=file.read()
        name_list=text_content.split('\n')
        good=1
        for item in name_list:
            if filename==item:
                good=0
        if good==0:
            print(filename+' already exists ! Choose another name')
            message1="Name already Exist"
            image="../static/images/nok.png"
            message2="Choose another name"
            message3="/codegen_flask_app"
            message4="Create a Flask App"
            PAGE_DESTINATION="operation_done"
            page_name="operation_done.html"
            loguer(env.level+' route END OF codegen_flask_app_create() in ***app.py*** : >')
            # ===================================================================
            env.level=env.level[:-1]
            return render_template('main_index.html',route=route,USERNAME=session['user'],PAGE_DESTINATION=PAGE_DESTINATION,message1=message1,message2=message2,message3=message3,message4=message4,image=image,page_name=page_name)
                
        else:
            print(yellow(f'     {filename} does NOT exists. Let s create it',bold=True))
            with open('./code_architecture/imported_scripts.txt','a+') as file:
                file.write(filename+'\n')
            # create a sub durectory
            subdir='./code_app_scripts_to_import/'+filename.replace('.py','')
            os.mkdir(subdir)
            os.mkdir(subdir+'/package_dev')
            os.mkdir(subdir+'/package_dev/debug')
            os.mkdir(subdir+'/package_dev/temp')
            os.mkdir(subdir+'/package_dev/output')
            os.mkdir(subdir+'/package_dev/result')
            os.mkdir(subdir+'/package_dev/templates')              
            os.mkdir(subdir+'/package_prod')
            os.mkdir(subdir+'/package_prod/debug')
            os.mkdir(subdir+'/package_prod/temp')
            os.mkdir(subdir+'/package_prod/output')
            os.mkdir(subdir+'/package_prod/result')
            os.mkdir(subdir+'/package_prod/templates')            
            with open(subdir+'/a_imports.txt','w') as file:
                line_out='''from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
import os
import sys
from crayons import *
from werkzeug.utils import secure_filename
import random
from datetime import datetime, timedelta
import socket
import webbrowser
import threading
import time
import glob
import signal
import requests
import json
import hashlib
from pathlib import Path
from inspect import currentframe
import subprocess
import shutil
import env as env
#import sqlalchemy
#from sqlalchemy.orm import sessionmaker
#from tabledef import *
#import sqlite3
#import struct
#import csv
#import pandas as pd
#from pandas import DataFrame
'''                
                file.write(line_out)
            with open(subdir+'/a_global_variables.txt','w') as file:
                file.write('app = Flask(__name__)\n')
            with open(subdir+'/script_functions.txt','w') as file:
                file.write('def_loguer.py\ndef_open_browser_tab.py\n')
            with open(subdir+'/script_routes.txt','w') as file:
                file.write('')
            with open(subdir+'/a_header.txt','w') as file:
                line_out="# -*- coding: UTF-8 -*-\n#!/usr/bin/env python\n'''\n    description : "
                line_out=line_out+description+"\n'''"
                file.write(line_out)
            with open(subdir+'/a_main.txt','w') as file:
                line_out='''
@app.route(\'/\', methods=[\'GET\'])
def index():
    \'\'\'
    version:

    description : index page
    \'\'\'
    route="/index"
    env.level+=\'-\'
    print(\'\\n\'+env.level,white(\'route index() in ***app.py*** : >\\n\',bold=True))
    loguer(env.level+\' route index() in ***app.py*** : >\')
    # ===================================================================
    env.level=env.level[:-1]
    return render_template(\'index.html\')
  
    
if __name__=="__main__":
    print(env.level,white("MAIN FUNCTION ( the application starts here ): >",bold=True))
    with open("./debug/log.txt","w") as file:
        pass
    loguer(env.level+" APPLICATION STARTS")
'''
                if protocol=="http":
                    line_out=line_out+'''    host="127.0.0.1"
    open_browser_tab(host,'''+port+''')
    app.secret_key = os.urandom(12)
    app.run(debug=False,host='0.0.0.0', port='''+port+''')
    '''
                else:
                    line_out=line_out+'''    host="127.0.0.1"
    #open_browser_tab(host,'''+port+''')
    app.secret_key = os.urandom(12)
        app.run(debug=True,host='0.0.0.0',port='''+port+''',ssl_context='adhoc')
    '''    
                file.write(line_out)
            with open(subdir+'/build_location.txt','w') as file:
                file.write(subdir+'/package_dev')
     
            with open(subdir+'/package_dev/result/home_url.txt','w') as file:
                pass
            with open(subdir+'/package_prod/result/home_url.txt','w') as file:
                pass
            with open(subdir+'/package_dev/env.py','w') as file:
                file.write('level="["')
            with open(subdir+'/package_prod/env.py','w') as file:
                file.write('level="["')
                
            with open('./result/home_url.txt') as file:
                home_url=file.read()
                print()
                print('home_url',home_url)
                print()
                
            with open("./analyse_application_logs.py") as file:
                text_content=file.read()
            text_content=text_content.replace("app.py",filename)
            with open(subdir+'/package_dev/analyse_application_logs.py','w') as file:
                file.write(text_content)
            with open(subdir+'/package_prod/analyse_application_logs.py','w') as file:
                file.write(text_content)
                
            with open("./code_templates/z_init_appli.py") as file:
                text_content=file.read()
            text_content=text_content.replace("app.py",filename)
            with open(subdir+'/package_dev/z_init_appli.py','w') as file:
                file.write(text_content)
            with open(subdir+'/package_prod/z_init_appli.py','w') as file:
                file.write(text_content)
            with open(subdir+'/package_dev/a.bat','w') as file:
                file.write("python -m venv venv")
            with open(subdir+'/package_dev/b.bat','w') as file:
                file.write("venv\\scripts\\activate")
            with open(subdir+'/package_dev/c.bat','w') as file:
                file.write("pip install -r requirements.txt")
            with open(subdir+'/package_dev/d.bat','w') as file:
                file.write("venv\\scripts\\deactivate")
            with open(subdir+'/package_dev/e.bat','w') as file:
                file.write("python z_init_appli.py")
            with open(subdir+'/package_dev/requirements.txt','w') as file:
                file.write("crayons==0.4.0\nrequests==2.32.3\nflask\nsqlalchemy\npandas\nijson")
            with open(subdir+'/package_prod/a.bat','w') as file:
                file.write("python -m venv venv")
            with open(subdir+'/package_prod/b.bat','w') as file:
                file.write("venv\\scripts\\activate")
            with open(subdir+'/package_prod/c.bat','w') as file:
                file.write("pip install -r requirements.txt")
            with open(subdir+'/package_prod/d.bat','w') as file:
                file.write("venv\\scripts\\deactivate")
            with open(subdir+'/package_prod/e.bat','w') as file:
                file.write("python z_init_appli.py")
            with open(subdir+'/package_prod/requirements.txt','w') as file:
                file.write("crayons==0.4.0\nrequests==2.32.3\nflask\nsqlalchemy\npandas\nijson")
        file_types='*.*'
        src_directory='./static'
        dst_directory=subdir+'/package_dev/static'        
        copy_dir(src_directory,dst_directory,file_types)
        src_directory='./static/img'
        dst_directory=subdir+'/package_dev/static/img'        
        copy_dir(src_directory,dst_directory,file_types)        
        src_directory='./static/assets'
        dst_directory=subdir+'/package_dev/static/assets'        
        copy_dir(src_directory,dst_directory,file_types) 
        src_directory='./static/assets/css'
        dst_directory=subdir+'/package_dev/static/assets/css'        
        copy_dir(src_directory,dst_directory,file_types)
        src_directory='./static/assets/css/images'
        dst_directory=subdir+'/package_dev/static/assets/css/images'        
        copy_dir(src_directory,dst_directory,file_types)
        src_directory='./static/assets/css/images/ie'
        dst_directory=subdir+'/package_dev/static/assets/css/images/ie'        
        copy_dir(src_directory,dst_directory,file_types)
        src_directory='./static/assets/js'
        dst_directory=subdir+'/package_dev/static/assets/js'        
        copy_dir(src_directory,dst_directory,file_types)
        src_directory='./static/assets/sass'
        dst_directory=subdir+'/package_dev/static/assets/sass'        
        copy_dir(src_directory,dst_directory,file_types)
        src_directory='./static/assets/sass/libs'
        dst_directory=subdir+'/package_dev/static/assets/sass/libs'        
        copy_dir(src_directory,dst_directory,file_types)
        src_directory='./static/assets/webfonts'
        dst_directory=subdir+'/package_dev/static/assets/webfonts'        
        copy_dir(src_directory,dst_directory,file_types)     
        src_directory='./static/images'
        dst_directory=subdir+'/package_dev/static/images'        
        copy_dir(src_directory,dst_directory,file_types)    
        src_directory='./static'
        dst_directory=subdir+'/package_prod/static'        
        copy_dir(src_directory,dst_directory,file_types)
        src_directory='./static/img'
        dst_directory=subdir+'/package_prod/static/img'        
        copy_dir(src_directory,dst_directory,file_types)        
        src_directory='./static/assets'
        dst_directory=subdir+'/package_prod/static/assets'        
        copy_dir(src_directory,dst_directory,file_types) 
        src_directory='./static/assets/css'
        dst_directory=subdir+'/package_prod/static/assets/css'        
        copy_dir(src_directory,dst_directory,file_types)
        src_directory='./static/assets/css/images'
        dst_directory=subdir+'/package_prod/static/assets/css/images'        
        copy_dir(src_directory,dst_directory,file_types)
        src_directory='./static/assets/css/images/ie'
        dst_directory=subdir+'/package_prod/static/assets/css/images/ie'        
        copy_dir(src_directory,dst_directory,file_types)
        src_directory='./static/assets/js'
        dst_directory=subdir+'/package_prod/static/assets/js'        
        copy_dir(src_directory,dst_directory,file_types)
        src_directory='./static/assets/sass'
        dst_directory=subdir+'/package_prod/static/assets/sass'        
        copy_dir(src_directory,dst_directory,file_types)
        src_directory='./static/assets/sass/libs'
        dst_directory=subdir+'/package_prod/static/assets/sass/libs'        
        copy_dir(src_directory,dst_directory,file_types)
        src_directory='./static/assets/webfonts'
        dst_directory=subdir+'/package_prod/static/assets/webfonts'        
        copy_dir(src_directory,dst_directory,file_types)     
        src_directory='./static/images'
        dst_directory=subdir+'/package_prod/static/images'        
        copy_dir(src_directory,dst_directory,file_types)   
        shutil.copyfile('./code_templates/index.html', './'+subdir+'/package_dev/templates/index.html')
        shutil.copyfile('./code_templates/index.html', './'+subdir+'/package_prod/templates/index.html')        
        shutil.copyfile('./code_central_functions/def_loguer_v2025-09-29.py', './'+subdir+'/def_loguer.py')     
        shutil.copyfile('./code_central_functions/def_open_browser_tab_v2025-09-29.py', './'+subdir+'/def_open_browser_tab.py')         
        # ###########################################
        message1="Flask App Created"
        image="../static/images/ok.png"
        message2="Edit the APP in the imported scripts"
        message3="/goto_script_B?script="+name+".py&type=route"
        message4="Edit the Flask APP"
        PAGE_DESTINATION="z_codegen_flask_app_create"
        page_name="z_codegen_flask_app_create.html"
        loguer(env.level+' route END OF codegen_flask_app_create() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]
        return render_template('main_index.html',route=route,USERNAME=session['user'],PAGE_DESTINATION=PAGE_DESTINATION,message1=message1,message2=message2,message3=message3,message4=message4,image=image,page_name=page_name)
        



def t_():
    current_time = datetime.utcnow()
    current_time = current_time.strftime("$%Y%m%dW%H%M%S.%fZ")
    return(current_time)

def b_(t):
    with open('./templates/28b.json','a+') as file:
        file.write(t)
              

@app.route('/test')
def test():
    return render_template('check.html')
 
'''
    HERE UNDER CSE ROUTES
'''
@app.route("/v1/events", methods=['GET'])
def CSE1():
    """Get a list of recent events from Cisco CSE."""
    #?connector_guid[]=7eb09223-b9b3-4508-ac9f-d16fffbdafb0&event_type[]=1107296272&event_type[]=1090519054&limit=10
    #TO DEBUG
    #connector_guid=request.args.get('connector_guid')   
    b_('3')
    token = request.headers.get('Authorization')
    print()
    print(cyan('CSE GET All Events for a specific Computer',bold=True))
    print(cyan('received token :'+token,bold=True))     
    print()
    if token==CSE_AUTHORIZATION:
        return render_template('2.json')       
    else: 
        return '{"ERROR": {"error cause":"invalid Authentication Basic Token :'+token+' "}}'        

@app.route("/v1/computers", methods=['GET'])
def CSE2():
    token = request.headers.get('Authorization')   
    with open('./templates/28b.json','w') as file:
        file.write(t_())    
    b_('1')    
    print()
    print(cyan('CSE GET All Computers',bold=True))
    print(cyan('received token :'+token,bold=True))   
    print()
    #"""Get a list of computers from Cisco CSE."""
    if token==CSE_AUTHORIZATION:
        return render_template('1.json')       
    else: 
        return '{"ERROR": {"error cause":"invalid Authentication Basic Token :'+token+' "}}'    
 
@app.route("/v1/computers/fc2842aa-12a7-4e65-ab73-b4d8053a9d9d", methods=['GET','PUT','PATCH','DELETE'])
def CSE3b():
    token = request.headers.get('Authorization')
    print()
    print(cyan('received token :'+token,bold=True))   
    print()
    if token==CSE_AUTHORIZATION:
        if request.method == 'GET':
            print(cyan("/v1/computers/ ECHO: GET",bold=True))
            prtin()
            return render_template('3.json')
        elif request.method == 'PATCH':
            print(cyan("CSE PATCH Move Computer to new Group",bold=True))
            print()            
            return render_template('7-Move_Computer_to_new_Group.json')
        elif request.method == 'PUT':
            return "ECHO: PUT\n"           
    else: 
        return '{"ERROR": {"error cause":"invalid Authentication Basic Token :'+token+' "}}'  
 
@app.route("/v1/computers/7eb09223-b9b3-4508-ac9f-d16fffbdafb0", methods=['GET','PUT','PATCH','DELETE'])
def CSE3():
    token = request.headers.get('Authorization')
    print()
    print(cyan('received token :'+token,bold=True))   
    print()
    if token==CSE_AUTHORIZATION:
        if request.method == 'GET':
            print(cyan("/v1/computers/ ECHO: GET",bold=True))
            prtin()
            return render_template('3.json')
        elif request.method == 'PATCH':
            print(cyan("APMP PATCH Move Computer to new Group",bold=True))
            print()            
            return render_template('7-Move_Computer_to_new_Group.json')
        elif request.method == 'PUT':
            return "ECHO: PUT\n"           
    else: 
        return '{"ERROR": {"error cause":"invalid Authentication Basic Token :'+token+' "}}' 

@app.route("/v1/computers/7eb09223-b9b3-4508-ac9f-d16fffbdafb0/isolation", methods=['GET','PUT','PATCH','DELETE'])
def CSE4():
    token = request.headers.get('Authorization')
    print()
    print(cyan('received token :'+token,bold=True))   
    print()
    with open('./templates/isolation_status.txt','r') as file2:
        statut=file2.read()        
    if token==CSE_AUTHORIZATION:
        if request.method == 'GET':
            print(cyan("CSE GET Check status for Computer Isolation",bold=True)) 
            print(cyan(f"  current statut isolation is equal to {statut}",bold=True))
            if statut=='1':      
                b_('4')
                return render_template('10-Check_status_for_Computer_Isolation_isolated.json')
            else:
                return render_template('10b-Check_status_for_Computer_Isolation_isolated.json')
        elif request.method == 'PUT':
            print(cyan("CSE PUT : Isolate infected Computer",bold=True)) 
            print()
            if statut=='1': 
                print(cyan("Computer already isolated",bold=True)) 
                return render_template('21-Isolate_infected_Computer_error_409.json')
            else:
                with open('./templates/isolation_status.txt','w') as file2:
                    file2.write('1')              
                return render_template('8-Isolate_infected_Computer.json')    
        elif request.method == 'DELETE':
            print(cyan("CSE DELETE Delete Isolation of infected Computer",bold=True)) 
            print()
            with open('./templates/isolation_status.txt','w') as file2:
                file2.write('0')              
            return render_template('9-Delete_Isolation_of_infected_Computer.json')         
    else: 
        return '{"ERROR": {"error cause":"invalid Authentication Basic Token :'+token+' "}}'
        
@app.route("/v1/computers/fc2842aa-12a7-4e65-ab73-b4d8053a9d9d/isolation", methods=['GET','PUT','PATCH','DELETE'])
def CSE4b():
    token = request.headers.get('Authorization')
    print()
    print(cyan('received token :'+token,bold=True))   
    print()
    with open('./templates/isolation_status.txt','r') as file2:
        statut=file2.read()        
    if token==CSE_AUTHORIZATION:
        if request.method == 'GET':
            print(cyan("CSE GET Check status for Computer Isolation",bold=True)) 
            print(cyan(f"  current statut isolation is equal to {statut}",bold=True))
            if statut=='1':            
                return render_template('10-Check_status_for_Computer_Isolation_isolated.json')
            else:
                return render_template('10b-Check_status_for_Computer_Isolation_isolated.json')
        elif request.method == 'PUT':
            print(cyan("CSE PUT : Isolate infected Computer",bold=True)) 
            print()
            if statut=='1': 
                print(cyan("Computer already isolated",bold=True)) 
                return render_template('21-Isolate_infected_Computer_error_409.json')
            else:
                print(cyan("Computer NOT already isolated",bold=True))
                with open('./templates/isolation_status.txt','w') as file2:
                    file2.write('1')   
                with open('./templates/8-Isolate_infected_Computer.json') as file:
                    text_content=file.read()
                print(text_content)
                return render_template('8-Isolate_infected_Computer.json')    
        elif request.method == 'DELETE':
            print(cyan("CSE DELETE Delete Isolation of infected Computer",bold=True)) 
            print()
            with open('./templates/isolation_status.txt','w') as file2:
                file2.write('0')              
            return render_template('9-Delete_Isolation_of_infected_Computer.json')         
    else: 
        return '{"ERROR": {"error cause":"invalid Authentication Basic Token :'+token+' "}}'


@app.route("/v1/computers/fc2842aa-12a7-4e65-ab73-b4d8053a9d9d/vulnerabilities", methods=['GET'])
def CSE5():
    token = request.headers.get('Authorization')
    print()
    print(cyan("CSE GET All Vulnerabilities for a specific Computer",bold=True))
    print(cyan('received token :'+token,bold=True))   
    print()
    if token==CSE_AUTHORIZATION:
        return render_template('6-All_Vulnerabilities_for_a_specific_Computer.json')  
    else: 
        return '{"ERROR": {"error cause":"invalid Authentication Basic Token :'+token+' "}}'

@app.route("/v1/event_types", methods=['GET'])
def CSE6():
    token = request.headers.get('Authorization')
    print()
    print(cyan('CSE GET Event Types',bold=True))
    print(cyan('received token :'+token,bold=True))     
    print()
    if token==CSE_AUTHORIZATION:
        return render_template('1-get_event_type_id.json')        
    else: 
        return '{"ERROR": {"error cause":"invalid Authentication Basic Token :'+token+' "}}'  
        
        
@app.route("/v1/groups", methods=['GET'])
def CSE7():
    token = request.headers.get('Authorization')
    print()
    print(cyan('CSE GET All Groups',bold=True))
    print(cyan('received token :'+token,bold=True))     
    print()
    if token==CSE_AUTHORIZATION:
        return render_template('3-get_all_groups.json')       
    else: 
        return '{"ERROR": {"error cause":"invalid Authentication Basic Token :'+token+' "}}'      
    
@app.route("/v1/file_lists/simple_custom_detections", methods=['GET'])
def CSE8():
    token = request.headers.get('Authorization')
    print()
    print(cyan('CSE Get All Simple Custom Detections',bold=True))
    print(cyan('received token :'+token,bold=True))     
    print()
    if token==CSE_AUTHORIZATION:
        return render_template('4-get_all_simple_detection.json')      
    else: 
        return '{"ERROR": {"error cause":"invalid Authentication Basic Token :'+token+' "}}'     

@app.route("/v1/file_lists/10050bbc-cc0a-48b9-b8ce-71fbec2fba6c/files/b1380fd95bc5c0729738dcda2696aa0a7c6ee97a93d992931ce717a0df523967", 
methods=['POST'])
def CSE9():
    token = request.headers.get('Authorization')
    print()
    print(cyan('CSE Get All Simple Custom Detections',bold=True))
    print(cyan('received token :'+token,bold=True))     
    print()
    if token==CSE_AUTHORIZATION:
        return render_template('16-add_file_to_block_list.json')      
    else: 
        return '{"ERROR": {"error cause":"invalid Authentication Basic Token :'+token+' "}}'  

        
'''
    HERE UNDER MALWARE ANALYTICS ROUTES
'''
        
@app.route("/api/v2/search/submissions", methods=['GET'])
def TG1():
    sha=request.args['q']
    token = 'Bearer '+request.args['api_key']    
    print()
    print(cyan('ThreatGrid GET Sample Submissions Search',bold=True))
    print(cyan('received token :'+token,bold=True))  
    print(cyan('received sha :'+sha,bold=True))
    print()    
    if token==THREATGRID_API_KEY:
        if sha=='b1380fd95bc5c0729738dcda2696aa0a7c6ee97a93d992931ce717a0df523967':
            b_('4')
            return render_template('5.json')
        else: 
            return '{"ERROR": {"error cause":"this is not the expected sha256 '+sha+'"}}'          
    else: 
        return '{"ERROR": {"error cause":"invalid token :'+token+' "}}'
    
@app.route("/api/v2/samples/feeds/domains", methods=['GET'])
def TG2():
    token = 'Bearer '+request.args['api_key']    
    sample = request.args['sample']  
    print()
    print(cyan('ThreatGrid GET Request Sample Domains',bold=True))
    print(cyan('received token :'+token,bold=True)) 
    print(cyan('received sample :'+sample,bold=True))    
    print()     
    if token==THREATGRID_API_KEY:
        if sample=='4d1e71bf3fa1a98b23fb7cb6e3ab2ad6':
            return render_template('6.json')
        elif sample=='d826d1eec635e7d77c1d9dd7abb0a8e5':
            return render_template('6.json')
        else: 
            return '{"ERROR": {"error cause":"this is not the expected sample_ID : '+sample+'"}}'      
    else: 
        return '{"ERROR": {"error cause":"invalid token **:'+token+'"}}'
        
    
@app.route("/api/v2/iocs/feeds/domains", methods=['GET'])
def TG3():
    token = 'Bearer '+request.args['api_key']       
    print()
    print(cyan('ThreatGrid GET IOC feeds',bold=True))
    print(cyan('received token :'+token,bold=True))     
    print()    
    if token==THREATGRID_API_KEY:
        if 'confidence' in request.args:
            return render_template('27.json')
        else:
            return render_template('1_IOC_Feeds.json')        
    else: 
        return '{"ERROR": {"error cause":"invalid token :'+token+' "}}'

@app.route("/api/v3/feeds/dga-dns_2020-01-08.json", methods=['GET'])
def TG4():
    token = 'Bearer '+request.args['api_key']   
    print()
    print(cyan('ThreatGrid GET Feed in JSON format',bold=True))
    print(cyan('received token :'+token,bold=True))     
    print()     
    if token==THREATGRID_API_KEY:
            return render_template('2-Feed_in_JSON_format.json')        
    else: 
        return '{"ERROR": {"error cause":"invalid token :'+token+' "}}'
        
@app.route("/api/v2/samples/d826d1eec635e7d77c1d9dd7abb0a8e5/analysis.json", methods=['GET'])
def TG5b():
    token = 'Bearer '+request.args['api_key']  
    print()
    print(cyan('ThreatGrid GET Request Sample Analysis Report',bold=True))
    print(cyan('received token :'+token,bold=True))     
    print()     
    if token==THREATGRID_API_KEY:
            return render_template('5-Request_Sample_Analysis_Report.json')        
    else: 
        return '{"ERROR": {"error cause":"invalid token :'+token+' "}}' 
        
@app.route("/api/v2/samples/4d1e71bf3fa1a98b23fb7cb6e3ab2ad6/analysis.json", methods=['GET'])
def TG5():
    token = 'Bearer '+request.args['api_key']  
    print()
    print(cyan('ThreatGrid GET Request Sample Analysis Report',bold=True))
    print(cyan('received token :'+token,bold=True))     
    print()     
    if token==THREATGRID_API_KEY:
            return render_template('5-Request_Sample_Analysis_Report.json')        
    else: 
        return '{"ERROR": {"error cause":"invalid token :'+token+' "}}' 
        
@app.route("/api/v3/feeds/ransomware-dns_2020-01-08.stix", methods=['GET'])
def TG6():
    token = 'Bearer '+request.args['api_key']  
    print()
    print(cyan('ThreatGrid GET Feed in STIX format',bold=True))
    print(cyan('received token :'+token,bold=True))     
    print()    
    if token==THREATGRID_API_KEY:
        return render_template('tg_stix.json')        
    else: 
        return '{"ERROR": {"error cause":"invalid token :'+token+' "}}'
     
        
'''
    HERE UNDER UMBRELLA ROUTES
'''
@app.route("/domains/categorization", methods=['GET','POST'])
def Umbrella1():
    token = request.headers['Authorization']
    print()
    print(cyan('Umbrella GET Get Single Domain Status and Categorization',bold=True))
    print(cyan('received token :'+token,bold=True))   
    print()     
    if token==Umbrella_Investigate_Token:
        return render_template('7.json')
    else: 
        return '{"ERROR": {"error cause":"invalid token :'+token+'"}}'
 
@app.route("/1.0/events", methods=['POST'])
def Umbrella2():
    headers = request.headers
    token = request.args['customerKey']
    print()
    print(cyan('Umbrella POST Enforce on bad Domains in Umbrella',bold=True))
    print()     
    if token==UMBRELLA_ENFORCEMENT_KEY:
        return render_template('14.json')
    else: 
        return '{"ERROR": {"error cause":"invalid token :'+token+'"}}' 
        
@app.route("/1.0/events?customerKey=12345678-b9a1-4ad3-82d9-dfe2c93ffffz", methods=['POST'])
def Umbrella2b():
    headers = request.headers
    token = request.args['customerKey']
    print()
    print(cyan('Umbrella POST Enforce on bad Domains in Umbrella',bold=True))
    print()     
    if token==UMBRELLA_ENFORCEMENT_KEY:
        b_('10')
        return render_template('14.json')
    else: 
        return '{"ERROR": {"error cause":"invalid token :'+token+'"}}' 

@app.route("/1.0/domains", methods=['GET'])
def umbrella3():
    #TO DEBUG
    headers = request.headers
    #token = headers['Authorization']
    token = request.args['customerKey']
    print()
    print(cyan('Umbrella POST Enforce on bad Domains in Umbrella',bold=True))
    print()     
    if token==UMBRELLA_ENFORCEMENT_KEY:
        return render_template('26-Get_all_domains_in_a_custom_Enforcement_List.json')
    else: 
        return '{"ERROR": {"error cause":"invalid token :'+token+'"}}' 
        
        
@app.route("/domains/categorization/retdemos.com", methods=['GET'])
def umbrella4():
    token = request.headers['Authorization']
    print()
    print(cyan('Umbrella GET Get Single Domain Status and Categorization',bold=True))
    print()       
    if token==Umbrella_Investigate_Token:
        return render_template('1-Get_Single_Domain_Status_and_Categorization.json')
    else: 
        return '{"ERROR": {"error cause":"invalid token :'+token+'"}}'    
        
@app.route("/domains/categorization/['retdemos.com']", methods=['GET'])
def umbrella5():
    token = request.headers['Authorization']
    if token==Umbrella_Investigate_Token:
        return render_template('1-Get_Single_Domain_Status_and_Categorization.json')
    else: 
        return '{"ERROR": {"error cause":"invalid token :'+token+'"}}'     

@app.route("/domains/categorization/%5B'retdemos.com',%20'retdemos.com',%20'retdemos.com'%5D", methods=['GET'])
def umbrella5b():
    token = request.headers['Authorization']
    if token==Umbrella_Investigate_Token:
        return render_template('1-Get_Single_Domain_Status_and_Categorization.json')
    else: 
        return '{"ERROR": {"error cause":"invalid token :'+token+'"}}'          

@app.route("/pdns/domain/internetbadguys.com", methods=['GET'])
def umbrella6():
    token = request.headers['Authorization']
    print()
    print(cyan('Umbrella GET Get Historical Data on a Domain',bold=True))
    print()     
    if token==Umbrella_Investigate_Token:
        return render_template('2-Get_Historical_Data_on_a_Domain.json')
    else: 
        return '{"ERROR": {"error cause":"invalid token :'+token+'"}}'   

@app.route("/recommendations/name/internetbadguys.com.json", methods=['GET'])
def umbrella7():
    token = request.headers['Authorization']
    print()
    print(cyan('Umbrella GET Co-Occurences for a Domain',bold=True))
    print()     
    if token==Umbrella_Investigate_Token:
        return render_template('Co-Occurences_for_a_Domain.json')
    else: 
        return '{"ERROR": {"error cause":"invalid token :'+token+'"}}'   

@app.route("/links/name/example.com.json", methods=['GET'])
def umbrella8():
    token = request.headers['Authorization']
    print()
    print(cyan('Umbrella GET Related Domains for a Domain',bold=True))
    print()      
    if token==Umbrella_Investigate_Token:
        return render_template('4-Related_Domains_for_a_Domain.json')
    else: 
        return '{"ERROR": {"error cause":"invalid token :'+token+'"}}'     

@app.route("/security/name/getmalware.com.json", methods=['GET'])
def umbrella9():
    token = request.headers['Authorization']
    print()
    print(cyan('Umbrella GET Get Security Report for domain',bold=True))
    print()      
    if token==Umbrella_Investigate_Token:
        return render_template('5-Get_Security_Report_for_domain.json')
    else: 
        return '{"ERROR": {"error cause":"invalid token :'+token+'"}}'  

@app.route("/domains/risk-score/getmalware.com", methods=['GET'])
def umbrella10():
    token = request.headers['Authorization']
    print()
    print(cyan('Umbrella GET Get Risk Score for domain',bold=True))
    print()       
    if token==Umbrella_Investigate_Token:
        return render_template('6-Get_Risk_Score_for_domain.json')
    else: 
        return '{"ERROR": {"error cause":"invalid token :'+token+'"}}'  

@app.route("/samples/getmalware.com", methods=['GET'])
def umbrella11():
    token = request.headers['Authorization']
    print()
    print(cyan('Umbrella GET Threat Grid Integration',bold=True))
    print()      
    if token==Umbrella_Investigate_Token:
        return render_template('7-Threat_Grid_Integration.json')
    else: 
        return '{"ERROR": {"error cause":"invalid token :'+token+'"}}'      
        
@app.route("/1", methods=['GET']) #TO DEBUG
def umbrella12():
    token = request.headers['Authorization']
    print()
    print(cyan('Umbrella GET Enforce on bad Domains in Umbrella',bold=True))
    print()     
    if token==Umbrella_Investigate_Token:
        return render_template('15.json')
    else: 
        return '{"ERROR": {"error cause":"invalid token :'+token+'"}}'  
        
@app.route('/auth/v2/token', methods = ['POST'])
def umbrella_token():
    print('request',cyan(request.headers,bold=True))
    Authorization=request.headers.get("Authorization")
    Authorization=Authorization.replace("Basic ","")
    Authorization=Authorization.encode('utf-8')
    print('Authorization ',cyan(Authorization,bold=True))    
    print('Authorization type ',cyan(type(Authorization),bold=True)) 
    decoded_Authorization = base64.decodebytes(Authorization)
    print('decoded_Authorization ',cyan(decoded_Authorization,bold=True))    
    decoded_Authorization=decoded_Authorization.decode('utf-8')
    creds=decoded_Authorization.split(":")
    client_id=creds[0]
    client_password=creds[1]
    print('client_id ',cyan(client_id,bold=True))
    print('client_password ',cyan(client_password,bold=True))
 
    #print('request.auth',cyan(request.form['client_credentials'],bold=True))    
    payload=request.form['grant_type']
    print()
    print(cyan('Threat Response POST Auth',bold=True))    
    print(cyan("Received payload : "+payload,bold=True)) 
    print()
    if payload=='client_credentials' and client_id=='7c46bbf9e629475086e8fad219f9999a' and client_password=='1d579c19ed8c474596103239305b418f':
        with open('./templates/umbrella_token.json') as file:
            text_content=file.read()
        response=json.dumps(text_content)
        print(cyan(response,bold=True))
        #print(cyan(type(response),bold=True))  
        return render_template('umbrella_token.json')
    else: 
        return '{"ERROR": {"error cause":"invalid authentication token "}}'

    
@app.route('/v2/activity/dns', methods = ['GET'])
def umbrella_get_dns_activity():
    token = request.headers['Authorization']
    global UMBRELLA_TOKEN
    print('token : \n',cyan(token))
    print('Umbrella token : \n',cyan(UMBRELLA_TOKEN))    
    token = token.replace('Bearer ','')    
    if token!=UMBRELLA_TOKEN:
        print(red('Bad Token'))
        return ({})
    else:  
        return render_template('29_dns_activity.json')    
        
'''
    HERE UNDER XDR THREAT RESPONSES ROUTES
'''
       
@app.route("/iroh/oauth2/token", methods=['POST'])
def CTR1():
    print('request',cyan(request.headers,bold=True))
    Authorization=request.headers.get("Authorization")
    Authorization=Authorization.replace("Basic ","")
    Authorization=Authorization.encode('utf-8')
    print('Authorization ',cyan(Authorization,bold=True))    
    print('Authorization type ',cyan(type(Authorization),bold=True)) 
    decoded_Authorization = base64.decodebytes(Authorization)
    print('decoded_Authorization ',cyan(decoded_Authorization,bold=True))    
    decoded_Authorization=decoded_Authorization.decode('utf-8')
    creds=decoded_Authorization.split(":")
    client_id=creds[0]
    client_password=creds[1]
    print('client_id ',cyan(client_id,bold=True))
    print('client_password ',cyan(client_password,bold=True))
 
    #print('request.auth',cyan(request.form['client_credentials'],bold=True))    
    payload=request.form['grant_type']
    print()
    print(cyan('Threat Response POST Auth',bold=True))    
    print(cyan("Received payload : "+payload,bold=True)) 
    print()
    token = 'OK'
    if payload=='client_credentials' and client_id=='client-bbaad7e2-e5ff-413f-1234-0e21bc871zzz' and client_password=='ZezA_VszEcMTCzzzU0Wr5mQypXoxbjFNKDnLa0Mkw_O_ZZ4TND9mZZ':
        return render_template('9.json')
    else: 
        return '{"ERROR": {"error cause":"invalid authentication token "}}' 
        
@app.route("/iroh/iroh-inspect/inspect", methods=['GET','POST'])
def CTR2():
    token =request.headers['Authorization']
    print()
    print(cyan('Threat Response POST Inspect',bold=True))    
    #print(cyan("Received token : "+token,bold=True)) 
    print()    
    if token==CTR_TOKEN:
        b_('12')
        return render_template('10.json')
    else: 
        return '{"ERROR": {"error cause":"invalid token :'+token+'"}}'         
        
@app.route("/iroh/iroh-enrich/observe/observables", methods=['POST'])
def CTR3():
    token =request.headers['Authorization']
    print()
    print(cyan('Threat Response POST Enrich - Observe',bold=True))         
    data = request.data  # TO DEBUG PATRICK
    #data = request.params['data']
    observable_str=''
    print(cyan("observe_payload: ",bold=True))      
    for item in data:
        observable_str+=chr(item)
    #observable=data[0]
    print(cyan(observable_str,bold=True))
    if token==CTR_TOKEN:
        if observable_str=='[{"value": "b1380fd95bc5c0729738dcda2696aa0a7c6ee97a93d992931ce717a0df523967", "type": "sha256"}]':
            b_('13')
            return render_template('11.json')
        else:
            b_('13b')
            return '{"ERROR": "wrong value for observe_payload "}'
    else: 
        return '{"ERROR": {"error cause":"invalid token :'+token+'"}}'       
        
@app.route("/iroh/iroh-response/respond/observables", methods=['POST'])
def CTR4():
    token =request.headers['Authorization']    
    print('token :\n',green(token,bold=True))    
    print()
    print(cyan('Threat Response POST Response - Observables',bold=True))  
    print()
    print('request_data :',cyan(request.data,bold=True))
    #data=json.loads(request.data)     
    data=request.data.decode("utf-8")
    print('JSON data :',cyan(data,bold=True))   
    words=data.split('&')
    observable_value=words[0].split('=')[1]
    observable_type=words[1].split('=')[1]
    print()
    print('\nobservable_value: ',observable_value)    
    print('\nobservable_type: ',observable_type)   
    if token==CTR_TOKEN:
        if observable_type=='hostname':
            return render_template('response_actions_for_hostnames.json')
        elif observable_type=='ip':
            with open('./templates/response_actions_for_ip.json') as file:
                text_content=file.read()
            text_content=text_content.replace("1.2.3.4",observable_value)
            with open('./templates/response_actions.json','w') as file:
                file.write(text_content)
            return render_template('response_actions.json')
        elif observable_type=='domain':
            return render_template('response_actions_for_domain.json')
        elif observable_type=='sha256':
            return render_template('response_actions_for_sha256.json')
        else:
            return ({})
    else: 
        return '{"ERROR": {"error cause":"invalid token :'+token+'"}}'      

@app.route("/iroh/iroh-response/respond/trigger/21bb0ed7-937c-4fc7-9338-34e05a8d6916/amp-add-sha256-scd", methods=['POST'])
def CTR5():
    token =request.headers['Authorization']
    print()
    print(cyan('Threat Response POST Response - Trigger action',bold=True))  
    print()    
    if token==CTR_TOKEN:
        b_('17')
        return render_template('13.json')
    else: 
        return '{"ERROR": {"error cause":"invalid token :'+token+'"}}'  

@app.route("/iroh/iroh-response/respond/trigger/21bb0ed7-937c-4fc7-9338-34e05a8d6916/amp-remove-sha256-scd", methods=['POST'])
def CTR5b():
    token =request.headers['Authorization']
    print()
    print(cyan('Threat Response POST Response - Trigger action',bold=True))  
    print()    
    if token==CTR_TOKEN:
        b_('17')
        return render_template('13.json')
    else: 
        return '{"ERROR": {"error cause":"invalid token :'+token+'"}}'     
        
        
        
@app.route("/iroh/iroh-enrich/deliberate/observables", methods=['POST'])
def CTRR():
    token =request.headers['Authorization']
    print()
    print(cyan('Threat Response POST Enrich - Deliberate',bold=True))    
    #print(cyan("Received token : "+token,bold=True)) 
    print()      
    if token==CTR_TOKEN:
        return render_template('3-Enrich_-_Deliberate.json')
    else: 
        return '{"ERROR": {"error cause":"invalid token :'+token+'"}}'  
           
@app.route("/v1/disposition", methods=['GET'])
def CTR6():
    print()
    print(cyan('Threat Response POST Enrich - Deliberate',bold=True))    
    #print(cyan("Received token : "+token,bold=True)) 
    print()
    with open('./templates/28b.json','r') as file2:
        T='{'+file2.read()+'}'     
    return T          
        
@app.route("/iroh/iroh-enrich/refer/observables", methods=['POST'])
def CTR7():
    token =request.headers['Authorization']
    print()
    print(cyan('Threat Response POST Refer',bold=True))    
    #print(cyan("Received token : "+token,bold=True)) 
    print()    
    if token==CTR_TOKEN:
        return render_template('5-refer.json')
    else: 
        return '{"ERROR": {"error cause":"invalid token :'+token+'"}}'     

@app.route("/iroh/iroh-response/respond/trigger/22g678f2-ad5e-4374-8708-a8fcc7861f6c/01HP8SN2BIX9I1IR4dI1b4l9q1DQVwziOKo", methods=['POST'])
def CTR8():
    print(cyan("Trigger CSE host isolation workflow",bold=True)) 
    print()
    print('request_data :',cyan(request.data,bold=True))
    #data=json.loads(request.data)     
    data=request.data.decode("utf-8")
    print('JSON data :',cyan(data,bold=True))   
    words=data.split('&')
    observable_value=words[0].split('=')[1]
    observable_type=words[1].split('=')[1]
    print()
    print('\nobservable_value: ',observable_value)    
    print('\nobservable_type: ',observable_type)    
    if observable_value=='Demo_AMP_Threat_Audit' and observable_type=='hostname':
        variables_sqlite_update_value('guid_isolation_status','YES')
        variables_sqlite_update_value('victim_hostname_isolation_status','YES')       
        with open('./templates/isolation_status.txt','r') as file2:
            statut=file2.read()       
        if statut=='1': 
            print(cyan("Computer already isolated",bold=True)) 
            #return render_template('21-Isolate_infected_Computer_error_409.json')
            return ({'status':'YES in CSE'})
        else:
            with open('./templates/isolation_status.txt','w') as file2:
                file2.write('1')              
            return ({'status':'YES in CSE'})               
    else:
        return ('"status": "isolation = NO"')
     
        
@app.route("/iroh/iroh-response/respond/trigger/9c99aefa-64be-4a3d-884e-d4f14e60eebc/01YD3Z1A74H553WXOpHSOD0cJVN1fw1ik0T", methods=['POST'])
def CTR9():
    print(cyan("Trigger ISE host Quarantine workflow",bold=True)) 
    print()
    print('request_data :',cyan(request.data,bold=True))
    #data=json.loads(request.data)     
    data=request.data.decode("utf-8")
    print('JSON data :',cyan(data,bold=True))   
    words=data.split('&')
    observable_value=words[0].split('=')[1]
    observable_type=words[1].split('=')[1]
    print()
    print('\nobservable_value: ',observable_value)    
    print('\nobservable_type: ',observable_type) 
    infected_machine_list=['192.168.128.192', '192.168.128.181', '192.168.128.156']    
    if observable_type=='ip':   
        if observable_value in infected_machine_list and observable_type=='ip':            
            return ('"quarantine"')   
        else:
            return ('"status": "unknown"')            
    else:
        return ('"status": "unknown"')
        
@app.route("/iroh/iroh-response/respond/trigger/4b7a22cb-09a2-4b35-9b62-199bb55329c6/block", methods=['POST'])
def CTR10():
    print(cyan("Trigger adding domain to umbrella blocking list",bold=True)) 
    print()
    '''
    data=json.loads(request.data)     
    observable_value=data['value']
    print()
    print('observable_value: ',observable_value)    
    observable_type=data['type']
    print()
    print('observable_type: ',observable_type)    
    '''
    data=request.data.decode("utf-8")
    print('JSON data :',cyan(data,bold=True))   
    words=data.split('&')
    observable_value=words[0].split('=')[1]
    observable_type=words[1].split('=')[1]
    print()
    print('\nobservable_value: ',observable_value)    
    print('\nobservable_type: ',observable_type)      
    if observable_type=='domain':   
        if observable_value == "retdemos.com":            
            return ({'status':'YES in Umbrella'})   
        else:
            return ('"status": "unknown"')            
    else:
        return ('"status": "isolation = NO"')   

                  
        
@app.route("/iroh/iroh-response/respond/trigger/9c99aefa-8b06-4df8-96f4-a89e3f2556ef/01GWHRNGESXD03H9ZF47jbf3ZzJKez1F0Ej", methods=['POST'])
def CTR11():
    print(cyan("Trigger adding sha256 to Secure Endpoint Simple Custom Detection List\n",bold=True)) 
    data=request.data.decode("utf-8")
    print('JSON data :',cyan(data,bold=True))   
    words=data.split('&')
    observable_value=words[0].split('=')[1]
    observable_type=words[1].split('=')[1]
    print()
    print('\nobservable_value: ',observable_value)    
    print('\nobservable_type: ',observable_type)     
    if observable_type=='sha256':   
        if observable_value == "b1380fd95bc5c0729738dcda2696aa0a7c6ee97a93d992931ce717a0df523967" :   
            print(green('QUARANTINE SHA256',bold=True))
            variables_sqlite_update_value('filename_isolation_status','YES')
            return ({'status':'YES in CSE'})   
        else:
            print(red('ERROR 2',bold=True))
            return ('"status": "isolation = NO"')            
    else:
        print(red('ERROR 1',bold=True))   
        return ('"status": "isolation = NO"')
        
@app.route("/iroh/iroh-response/respond/trigger/9c99aefa-8b06-4df8-96f4-a89e3f2556ef/02DHT5DT6CKL50tVu3sj7WKrOnp6GaYSt3J", methods=['POST'])
def CTR12():
    print(cyan("Trigger adding IP to XDR Feed",bold=True)) 
    #data=json.loads(request.data)     
    data=request.data.decode("utf-8")
    print('JSON data :',cyan(data,bold=True))   
    words=data.split('&')
    observable_value=words[0].split('=')[1]
    observable_type=words[1].split('=')[1]
    print()
    print('\nobservable_value: ',observable_value)    
    print('\nobservable_type: ',observable_type)      
    if observable_type=='ip': 
        '''
        internal_ip_1=variable_value('internal_infected_ip_address_1')
        internal_ip_2=variable_value('internal_infected_ip_address_2')
        internal_ip_3=variable_value('internal_infected_ip_address_3')        
        internal_ip_4=variable_value('infected_machine_internal_ip_address')
        internal_ip_5=variable_value('malicious_domain_ip')
        if observable_value == internal_ip_1:            
            #variables_sqlite_update_value('internal_ip_1_isolation_status',"YES : in XDR Feeds")          
        elif observable_value == internal_ip_2:          
            #variables_sqlite_update_value('internal_ip_2_isolation_status',"YES : in XDR Feeds")          
            return ('YES in XDR Feed')       
        elif observable_value == internal_ip_3:        
            #variables_sqlite_update_value('internal_ip_3_isolation_status',"YES : in XDR Feeds")         
            return ('YES in XDR Feed')     
        elif observable_value == internal_ip_4:          
            #variables_sqlite_update_value('host_ip_isolation_status',"YES : in XDR Feeds")           
            return ('YES in XDR Feed')  
        elif observable_value == internal_ip_5:      
            #variables_sqlite_update_value('malicious_domain_ip_isolation_status',"YES : in XDR Feeds")            
            return ('YES in XDR Feed')              
        else:
            return ({"status": "unknown"}) 
        '''
        return ({'status':'YES in XDR Feed'})               
    else:
        return ('"status": "isolation = NO"')  
        
@app.route("/iroh/iroh-response/respond/trigger/test/test", methods=['POST'])
def CTR13():
    print(cyan("Trigger adding IP to XDR Feed",bold=True)) 
    #data=json.loads(request.data)     
    data=request.data.decode("utf-8")
    print('JSON data :',cyan(data,bold=True))   
    words=data.split('&')
    observable_value=words[0].split('=')[1]
    observable_type=words[1].split('=')[1]
    print()
    print('\nobservable_value: ',observable_value)    
    print('\nobservable_type: ',observable_type)      
    if observable_type=='ip':   
        if observable_value == "192.168.128.156":            
            return ('{"isolation_status": '+observable_value+'" added to XDR Firewall Feed"}')   
        else:
            return ('"status": "unknown"')            
    else:
        return ('"status": "unknown"') 
    
@app.errorhandler(404)
def not_found(error):
    return render_template('error.html'), 404 
    
# # ABOVE CHALLENGE SIMULATOR ROUTES  ########################################################    

#  def_step1***
@app.route('/step1', methods=['GET'])
def step1():
    '''
    Created : 2025-10-25T14:03:52.000Z

    description : STEP 1 Get computers
    '''
    route="/step1"
    env.level+='-'
    print('\n'+env.level,white('route step1() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route step1() in ***app.py*** : >')
    global client_id
    global client_password
    global host
    global host_for_token
    global profil_name
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        image="../static/images/toolbox.png" 
        message2="Message 2 :"
        message3="/Message 3"
        message4="Message 4 in button"
        PAGE_DESTINATION="z_step1"
        page_name="z_step1.html"
        loguer(env.level+' route END OF step1() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]
        return render_template('main_index.html',route=route,USERNAME=session['user'],PAGE_DESTINATION=PAGE_DESTINATION,message1=message1,message2=message2,message3=message3,message4=message4,image=image,page_name=page_name)
        


#  def_product_apis***
@app.route('/product_apis', methods=['GET'])
def product_apis():
    '''
    Created : 2025-10-25T14:17:46.000Z

    description : display a list of product APIs
    '''
    route="/product_apis"
    env.level+='-'
    print('\n'+env.level,white('route product_apis() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route product_apis() in ***app.py*** : >')
    global client_id
    global client_password
    global host
    global host_for_token
    global profil_name
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        # ===================================================================       
        '''
        # GET variable from calling web page
        profil_name='./profiles/'+request.args.get('profil_name')
        print()
        print('profil_name : ',profil_name)        
        # POST variable 
        keyword = request.form['keyword']
        print()
        print('keyword : ',keyword)
        
        # API TOKEN
        with open('ctr_token.txt','r') as file0:
            access_token=file0.read()
            
        action=request.args.get('action')
        print()
        print('action: ',action)
        print()
        if action=="copy":
            do something
            
        #CALL  A SUB FUNCTION
        print()   
        print(magenta('--> CALL  A SUB FUNCTION :',bold=True)) 
        '''        
        # Prepare the resulting Next Web Page
        result=1
        if result==1:        
            image="../static/images/ok.png" 
            message1="Title"
            message2="Connexion to XDR Tenant is Okay !"
            message3="#portfolio"
            message4="Button Message"            
        elif result==2:
            image="../static/images/ok.png" 
            message1="Title"
            message2="Connexion to XDR Tenant is Okay !"
            message3="#portfolio"
            message4="Button Message"              
        else:
            image="../static/images/ok.png" 
            message1="Title"
            message2="Connexion to XDR Tenant is Okay !"
            message3="#portfolio"
            message4="Button Message"              
        message1="Message 1 :"
        image="../static/images/toolbox.png" 
        message2="Message 2 :"
        message3="/Message 3"
        message4="Message 4 in button"
        PAGE_DESTINATION="z_product_apis"
        page_name="z_product_apis.html"
        loguer(env.level+' route END OF product_apis() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]
        return render_template('main_index.html',route=route,USERNAME=session['user'],PAGE_DESTINATION=PAGE_DESTINATION,message1=message1,message2=message2,message3=message3,message4=message4,image=image,page_name=page_name)
        


#  def_cse_get_computer***
@app.route('/cse_get_computer', methods=['GET'])
def cse_get_computer():
    '''
    Created : 2025-10-25T14:03:52.000Z
    description : STEP 1 Get computers
    '''
    route="/cse_get_computer"
    env.level+='-'
    print('\n'+env.level,white('route cse_get_computer() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route cse_get_computer() in ***app.py*** : >')
    global client_id
    global client_password
    global host
    global host_for_token
    global profil_name
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        database="api_calls"
        print("\ndatabase : ",database)
        table="api_calls"
        print("\ntable : ",table)
        name='Secure Endpoint Get Computers'
        where_clause=f'where `name` = "{name}"'
        entry_list=sqlite_db_select_entry(database,table,where_clause)
        print("\nentry_list : \n",entry_list)
        name=entry_list[0][1]
        base_url=entry_list[0][2]
        relative_url=entry_list[0][3]
        api_docummentation=entry_list[0][4]
        method=entry_list[0][5]
        short_description=entry_list[0][6]
        payload=entry_list[0][7]
        header=entry_list[0][8]
        body=entry_list[0][9]
        params=entry_list[0][10]
        parameters=entry_list[0][11]
        authentication_profile=entry_list[0][12]
        inputs=entry_list[0][13]
        outputs=entry_list[0][14]
        image="../static/images/toolbox.png"
        PAGE_DESTINATION="z_cse_get_computer"
        page_name="z_cse_get_computer.html"
        loguer(env.level+' route END OF cse_get_computer() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]
        return render_template('main_index.html',route=route,USERNAME=session['user'],PAGE_DESTINATION=PAGE_DESTINATION,image=image,page_name=page_name,name=name,base_url=base_url,relative_url=relative_url,api_docummentation=api_docummentation,method=method,short_description=short_description,payload=payload,header=header,body=body,params=params,parameters=parameters,authentication_profile=authentication_profile)
        


#  def_cse_apis***
@app.route('/cse_apis', methods=['GET'])
def cse_apis():
    '''
    Created : 2025-10-25T14:25:05.000Z

    description : display Secure Endpoint APIs choices
    '''
    route="/cse_apis"
    env.level+='-'
    print('\n'+env.level,white('route cse_apis() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route cse_apis() in ***app.py*** : >')
    global client_id
    global client_password
    global host
    global host_for_token
    global profil_name
    if not session.get('logged_in'):
        return render_template('login.html')
    else:           
        message1="Message 1 :"
        image="../static/images/toolbox.png" 
        message2="Message 2 :"
        message3="/Message 3"
        message4="Message 4 in button"
        PAGE_DESTINATION="z_cse_apis"
        page_name="z_cse_apis.html"
        loguer(env.level+' route END OF cse_apis() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]
        return render_template('main_index.html',route=route,USERNAME=session['user'],PAGE_DESTINATION=PAGE_DESTINATION,message1=message1,message2=message2,message3=message3,message4=message4,image=image,page_name=page_name)
        


#  def_cse_get_event_type***
@app.route('/cse_get_event_type', methods=['GET'])
def cse_get_event_type():
    '''
    Created : 2025-10-25T17:33:35.000Z
    description : CSE event type API
    '''
    route="/cse_get_event_type"
    env.level+='-'
    print('\n'+env.level,white('route cse_get_event_type() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route cse_get_event_type() in ***app.py*** : >')
    global client_id
    global client_password
    global host
    global host_for_token
    global profil_name
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        database="api_calls"
        print("\ndatabase : ",database)
        table="api_calls"
        print("\ntable : ",table)
        name='Secure Endpoint Get Event Types'
        where_clause=f'where `name` = "{name}"'
        entry_list=sqlite_db_select_entry(database,table,where_clause)
        print("\nentry_list : \n",entry_list)
        name=entry_list[0][1]
        base_url=entry_list[0][2]
        relative_url=entry_list[0][3]
        api_docummentation=entry_list[0][4]
        method=entry_list[0][5]
        short_description=entry_list[0][6]
        payload=entry_list[0][7]
        header=entry_list[0][8]
        body=entry_list[0][9]
        params=entry_list[0][10]
        parameters=entry_list[0][11]
        authentication_profile=entry_list[0][12]
        inputs=entry_list[0][13]
        outputs=entry_list[0][14]
        image="../static/images/toolbox.png"
        PAGE_DESTINATION="z_cse_get_event_type"
        page_name="z_cse_get_event_type.html"
        loguer(env.level+' route END OF cse_get_computer() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]
        return render_template('main_index.html',route=route,USERNAME=session['user'],PAGE_DESTINATION=PAGE_DESTINATION,image=image,page_name=page_name,name=name,base_url=base_url,relative_url=relative_url,api_docummentation=api_docummentation,method=method,short_description=short_description,payload=payload,header=header,body=body,params=params,parameters=parameters,authentication_profile=authentication_profile)
        


#  def_cse_get_events***
@app.route('/cse_get_events', methods=['GET'])
def cse_get_events():
    '''
    Created : 2025-10-25T17:38:08.000Z

    description : CSE get events
    '''
    route="/cse_get_events"
    env.level+='-'
    print('\n'+env.level,white('route cse_get_events() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route cse_get_events() in ***app.py*** : >')
    global client_id
    global client_password
    global host
    global host_for_token
    global profil_name
    if not session.get('logged_in'):
        return render_template('login.html')
    else: 
        message1="Message 1 :"
        image="../static/images/toolbox.png" 
        message2="Message 2 :"
        message3="/Message 3"
        message4="Message 4 in button"
        PAGE_DESTINATION="z_cse_get_events"
        page_name="z_cse_get_events.html"
        loguer(env.level+' route END OF cse_get_events() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]
        return render_template('main_index.html',route=route,USERNAME=session['user'],PAGE_DESTINATION=PAGE_DESTINATION,message1=message1,message2=message2,message3=message3,message4=message4,image=image,page_name=page_name)
        


#  def_cse_isolation***
@app.route('/cse_isolation', methods=['GET'])
def cse_isolation():
    '''
    Created : 2025-10-25T17:42:28.000Z

    description : CSE Isolation API
    '''
    route="/cse_isolation"
    env.level+='-'
    print('\n'+env.level,white('route cse_isolation() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route cse_isolation() in ***app.py*** : >')
    global client_id
    global client_password
    global host
    global host_for_token
    global profil_name
    if not session.get('logged_in'):
        return render_template('login.html')
    else:     
        message1="Message 1 :"
        image="../static/images/toolbox.png" 
        message2="Message 2 :"
        message3="/Message 3"
        message4="Message 4 in button"
        PAGE_DESTINATION="z_cse_isolation"
        page_name="z_cse_isolation.html"
        loguer(env.level+' route END OF cse_isolation() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]
        return render_template('main_index.html',route=route,USERNAME=session['user'],PAGE_DESTINATION=PAGE_DESTINATION,message1=message1,message2=message2,message3=message3,message4=message4,image=image,page_name=page_name)
        


#  def_ma_apis***
@app.route('/ma_apis', methods=['GET'])
def ma_apis():
    '''
    Created : 2025-10-25T19:49:26.000Z

    description : display malware analytics APIs
    '''
    route="/ma_apis"
    env.level+='-'
    print('\n'+env.level,white('route ma_apis() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route ma_apis() in ***app.py*** : >')
    global client_id
    global client_password
    global host
    global host_for_token
    global profil_name
    if not session.get('logged_in'):
        return render_template('login.html')
    else:        
        message1="Message 1 :"
        image="../static/images/toolbox.png" 
        message2="Message 2 :"
        message3="/Message 3"
        message4="Message 4 in button"
        PAGE_DESTINATION="z_ma_apis"
        page_name="z_ma_apis.html"
        loguer(env.level+' route END OF ma_apis() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]
        return render_template('main_index.html',route=route,USERNAME=session['user'],PAGE_DESTINATION=PAGE_DESTINATION,message1=message1,message2=message2,message3=message3,message4=message4,image=image,page_name=page_name)
        


#  def_ma_get_domains***
@app.route('/ma_get_domains', methods=['GET'])
def ma_get_domains():
    '''
    Created : 2025-10-25T19:59:59.000Z

    description : Malware Analytics Get domains attached to a sh256
    '''
    route="/ma_get_domains"
    env.level+='-'
    print('\n'+env.level,white('route ma_get_domains() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route ma_get_domains() in ***app.py*** : >')
    global client_id
    global client_password
    global host
    global host_for_token
    global profil_name
    if not session.get('logged_in'):
        return render_template('login.html')
    else:           
        message1="Message 1 :"
        image="../static/images/toolbox.png" 
        message2="Message 2 :"
        message3="/Message 3"
        message4="Message 4 in button"
        PAGE_DESTINATION="z_ma_get_domains"
        page_name="z_ma_get_domains.html"
        loguer(env.level+' route END OF ma_get_domains() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]
        return render_template('main_index.html',route=route,USERNAME=session['user'],PAGE_DESTINATION=PAGE_DESTINATION,message1=message1,message2=message2,message3=message3,message4=message4,image=image,page_name=page_name)
        


#  def_ma_get_submission***
@app.route('/ma_get_submission', methods=['GET'])
def ma_get_submission():
    '''
    Created : 2025-10-25T20:04:08.000Z

    description : Malware Analytics Get submission
    '''
    route="/ma_get_submission"
    env.level+='-'
    print('\n'+env.level,white('route ma_get_submission() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route ma_get_submission() in ***app.py*** : >')
    global client_id
    global client_password
    global host
    global host_for_token
    global profil_name
    if not session.get('logged_in'):
        return render_template('login.html')
    else:          
        message1="Message 1 :"
        image="../static/images/toolbox.png" 
        message2="Message 2 :"
        message3="/Message 3"
        message4="Message 4 in button"
        PAGE_DESTINATION="z_ma_get_submission"
        page_name="z_ma_get_submission.html"
        loguer(env.level+' route END OF ma_get_submission() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]
        return render_template('main_index.html',route=route,USERNAME=session['user'],PAGE_DESTINATION=PAGE_DESTINATION,message1=message1,message2=message2,message3=message3,message4=message4,image=image,page_name=page_name)
        


#  def_umbrella_apis***
@app.route('/umbrella_apis', methods=['GET'])
def umbrella_apis():
    '''
    Created : 2025-10-25T20:22:39.000Z

    description : display umbrella api choices
    '''
    route="/umbrella_apis"
    env.level+='-'
    print('\n'+env.level,white('route umbrella_apis() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route umbrella_apis() in ***app.py*** : >')
    global client_id
    global client_password
    global host
    global host_for_token
    global profil_name
    if not session.get('logged_in'):
        return render_template('login.html')
    else:          
        message1="Message 1 :"
        image="../static/images/toolbox.png" 
        message2="Message 2 :"
        message3="/Message 3"
        message4="Message 4 in button"
        PAGE_DESTINATION="z_umbrella_apis"
        page_name="z_umbrella_apis.html"
        loguer(env.level+' route END OF umbrella_apis() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]
        return render_template('main_index.html',route=route,USERNAME=session['user'],PAGE_DESTINATION=PAGE_DESTINATION,message1=message1,message2=message2,message3=message3,message4=message4,image=image,page_name=page_name)
        


#  def_umbrella_get_token***
@app.route('/umbrella_get_token', methods=['GET'])
def umbrella_get_token():
    '''
    Created : 2025-10-25T20:36:57.000Z

    description : Umbrella API v2 get token API
    '''
    route="/umbrella_get_token"
    env.level+='-'
    print('\n'+env.level,white('route umbrella_get_token() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route umbrella_get_token() in ***app.py*** : >')
    global client_id
    global client_password
    global host
    global host_for_token
    global profil_name
    if not session.get('logged_in'):
        return render_template('login.html')
    else:         
        message1="Message 1 :"
        image="../static/images/toolbox.png" 
        message2="Message 2 :"
        message3="/Message 3"
        message4="Message 4 in button"
        PAGE_DESTINATION="z_umbrella_get_token"
        page_name="z_umbrella_get_token.html"
        loguer(env.level+' route END OF umbrella_get_token() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]
        return render_template('main_index.html',route=route,USERNAME=session['user'],PAGE_DESTINATION=PAGE_DESTINATION,message1=message1,message2=message2,message3=message3,message4=message4,image=image,page_name=page_name)
        


#  def_umbrella_domain_status***
@app.route('/umbrella_domain_status', methods=['GET'])
def umbrella_domain_status():
    '''
    Created : 2025-10-26T08:19:34.000Z

    description : umbrella API v1 get domain status
    '''
    route="/umbrella_domain_status"
    env.level+='-'
    print('\n'+env.level,white('route umbrella_domain_status() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route umbrella_domain_status() in ***app.py*** : >')
    global client_id
    global client_password
    global host
    global host_for_token
    global profil_name
    if not session.get('logged_in'):
        return render_template('login.html')
    else:    
        message1="Message 1 :"
        image="../static/images/toolbox.png" 
        message2="Message 2 :"
        message3="/Message 3"
        message4="Message 4 in button"
        PAGE_DESTINATION="z_umbrella_domain_status"
        page_name="z_umbrella_domain_status.html"
        loguer(env.level+' route END OF umbrella_domain_status() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]
        return render_template('main_index.html',route=route,USERNAME=session['user'],PAGE_DESTINATION=PAGE_DESTINATION,message1=message1,message2=message2,message3=message3,message4=message4,image=image,page_name=page_name)
        


#  def_umbrella_get_dns_activity***
@app.route('/umbrella_get_dns_activityb', methods=['GET'])
def umbrella_get_dns_activityb():
    '''
    Created : 2025-10-26T08:32:01.000Z

    description : Umbrella API v2 get DNS activity API
    '''
    route="/umbrella_get_dns_activity"
    env.level+='-'
    print('\n'+env.level,white('route umbrella_get_dns_activityb() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route umbrella_get_dns_activityb() in ***app.py*** : >')
    global client_id
    global client_password
    global host
    global host_for_token
    global profil_name
    if not session.get('logged_in'):
        return render_template('login.html')
    else:     
        message1="Message 1 :"
        image="../static/images/toolbox.png" 
        message2="Message 2 :"
        message3="/Message 3"
        message4="Message 4 in button"
        PAGE_DESTINATION="z_umbrella_get_dns_activity"
        page_name="z_umbrella_get_dns_activity.html"
        loguer(env.level+' route END OF umbrella_get_dns_activity() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]
        return render_template('main_index.html',route=route,USERNAME=session['user'],PAGE_DESTINATION=PAGE_DESTINATION,message1=message1,message2=message2,message3=message3,message4=message4,image=image,page_name=page_name)
        


#  def_xdr_apis***
@app.route('/xdr_apis', methods=['GET'])
def xdr_apis():
    '''
    Created : 2025-10-26T08:46:00.000Z

    description : display XDR APIs choice
    '''
    route="/xdr_apis"
    env.level+='-'
    print('\n'+env.level,white('route xdr_apis() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route xdr_apis() in ***app.py*** : >')
    global client_id
    global client_password
    global host
    global host_for_token
    global profil_name
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        message1="Message 1 :"
        image="../static/images/toolbox.png" 
        message2="Message 2 :"
        message3="/Message 3"
        message4="Message 4 in button"
        PAGE_DESTINATION="z_xdr_apis"
        page_name="z_xdr_apis.html"
        loguer(env.level+' route END OF xdr_apis() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]
        return render_template('main_index.html',route=route,USERNAME=session['user'],PAGE_DESTINATION=PAGE_DESTINATION,message1=message1,message2=message2,message3=message3,message4=message4,image=image,page_name=page_name)
        


#  def_cse_get_computer_api***
@app.route('/cse_get_computer_api', methods=['GET','POST'])
def cse_get_computer_api():
    '''
    Created : 2025-10-26T10:01:07.000Z

    description : run the CSE get computer API formular
    '''
    route="/cse_get_computer_api"
    env.level+='-'
    print('\n'+env.level,white('route cse_get_computer_api() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route cse_get_computer_api() in ***app.py*** : >')
    global client_id
    global client_password
    global host
    global host_for_token
    global profil_name
    if not session.get('logged_in'):
        return render_template('login.html')
    else:  
        name = request.form.get("name")
        print("\nname : ",name)
        base_url = request.form.get("base_url")
        print("\nbase_url : ",base_url)
        relative_url = request.form.get("relative_url")
        print("\nrelative_url : ",relative_url)
        api_docummentation = request.form.get("api_docummentation")
        print("\napi_docummentation : ",api_docummentation)  
        short_description = request.form.get("short_description")
        print("\nshort_description : ",short_description)  
        payload = request.form.get("payload")
        print("\npayload : ",payload) 
        method = request.form.get("method")
        print("\nmethod : ",method)  
        header = request.form.get("header")
        print("\nheader : ",header)  
        body = request.form.get("body")
        print("\nbody : ",body)  
        params = request.form.get("params")
        print("\nparams : ",params)  
        parameters = request.form.get("parameters")
        print("\nparameters : ",parameters)  
        authentication_profile = request.form.get("authentication_profile")
        print("\nauthentication_profile : ",authentication_profile)  
        inputs = request.form.get("inputs")
        print("\ninputs : ",inputs)  
        outputs = request.form.get("outputs")
        print("\noutputs : ",outputs)          
        PAGE_DESTINATION="z_cse_get_computer_api"
        page_name="z_cse_get_computer_api.html"
        loguer(env.level+' route END OF cse_get_computer_api() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]
        return render_template('main_index.html',route=route,USERNAME=session['user'],PAGE_DESTINATION=PAGE_DESTINATION,page_name=page_name,name=name,base_url=base_url,relative_url=relative_url,api_docummentation=api_docummentation,short_description=short_description,payload=payload,method=method,header=header,body=body,params=params,parameters=parameters,authentication_profile=authentication_profile,inputs=inputs,outputs=outputs)
        


#  def_account_keys_dashboard***
@app.route('/account_keys_dashboard', methods=['GET'])
def account_keys_dashboard():
    '''
    Flask Route for the account_keys_dashboard Database dashoard
    '''
    route="/account_keys_dashboard"
    env.level+='-'
    print('\n'+env.level,white('route account_keys_dashboard() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route account_keys_dashboard() in ***app.py*** : >')
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        html_output='''<!DOCTYPE HTML>
<!-- description-->
<html>
    <head>
        <title>FLASK APP GENERATOR</title>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no" />
        <link rel="stylesheet" href="../static/assets/css/main.css" />
    <script>
        function popup_window( url, id, width, height )
        {
            //extract the url parameters if any, and pass them to the called html
            var tempvar=document.location.toString(); // fetch the URL string
            var passedparams = tempvar.lastIndexOf("?");
            if(passedparams > -1)
                url += tempvar.substring(passedparams);
            popup = window.open( url, id, 'toolbar=no,scrollbars=yes,location=yes,statusbar=yes,menubar=no,resizable=yes,width=' + width + ',height=' + height + '' );
            popup.focus();
        }
    </script>
    </head>
    <body class="is-preload">
        <!-- Nav -->
            <nav id="nav">
                <ul>
                
                    <li><a href="/">Back to main page</a></li>
                    <li><a href="/logout">log Out</a></li>
                    <li><a href="javascript:popup_window('/page_info?page=route_def_account_keys_dashboard.py&route=/account_keys_dashboard','page_info',700,600);">:</a></li>
        
                </ul>
            </nav>
        <!-- Portfolio -->
            <article id="portfolio" class="wrapper style3">
                <div class="container">
                    <header>
                        <h2>account_keys Database</h2>
                    </header>
                    <div class="row">
                        <div class="col-4 col-6-medium col-12-small">
                            <article class="box style2">
                                <a href="/account_keys_create_db" class="image featured"><img src="../static/images/database0.png" alt="" /></a>
                                <h3><a href="/account_keys_create_db">Create Database</a></h3>
                                <p>Create the account_keys Database</p>
                            </article>
                        </div>
                        <div class="col-4 col-6-medium col-12-small">
                            <article class="box style2">
                                <a href="/account_keys_ingest_demo_data" class="image featured"><img src="../static/images/database0.png" alt="" /></a>
                                <h3><a href="/account_keys_ingest_demo_data">Ingest Demo Data</a></h3>
                                <p>Ingest Demo Data into DB</p>
                            </article>
                        </div>
                        <div class="col-4 col-6-medium col-12-small">
                            <article class="box style2">
                                <a href="/account_keys_db_read" class="image featured"><img src="../static/images/database0.png" alt="" /></a>
                                <h3><a href="/account_keys_db_read">Read Database content</a></h3>
                                <p>Read DB an Create a CSV result</p>
                            </article>
                        </div>
                        <div class="col-4 col-6-medium col-12-small">
                            <article class="box style2">
                                <a href="/account_keys_db_clear" class="image featured"><img src="../static/images/database0.png" alt="" /></a>
                                <h3><a href="/account_keys_db_clear">Clear Database</a></h3>
                                <p>Delete Database content</p>
                            </article>
                        </div>
                        <div class="col-4 col-6-medium col-12-small">
                            <article class="box style2">
                                <a href="/account_keys_db_ingest_csv" class="image featured"><img src="../static/images/database0.png" alt="" /></a>
                                <h3><a href="/account_keys_db_ingest_csv">Ingest a CSV file</a></h3>
                                <p>Ingest a CSV file</p>
                            </article>
                        </div>
                        <div class="col-4 col-6-medium col-12-small">
                            <article class="box style2">
                                <a href="/account_keys_db_add_entry" class="image featured"><img src="../static/images/database0.png" alt="" /></a>
                                <h3><a href="/account_keys_db_add_entry">Add Entry</a></h3>
                                <p>Add an Entry to Database</p>
                            </article>
                        </div>
            
                    </div>
                </div>
            </article>
        <!-- Scripts -->
            <script src="../static/assets/js/jquery.min.js"></script>
            <script src="../static/assets/js/jquery.scrolly.min.js"></script>
            <script src="../static/assets/js/init.js"></script>
            <script src="../static/assets/js/browser.min.js"></script>
            <script src="../static/assets/js/breakpoints.min.js"></script>
            <script src="../static/assets/js/util.js"></script>
            <script src="../static/assets/js/main.js"></script>
    </body>
</html>
'''
        loguer(env.level+' route END OF account_keys_dashboard() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]
        return html_output
        

#  def_account_keys_create_db***
@app.route('/account_keys_create_db', methods=['GET'])
def account_keys_create_db():
    '''
    Flask Route for the account_keys_create_db Database Create DB action
    '''
    route="/account_keys_create_db"
    env.level+='-'
    print('\n'+env.level,white('route account_keys_create_db() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route account_keys_create_db() in ***app.py*** : >')
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        with open('./sqlite_databases_code/account_keys/db_details.txt') as file:
            db_details_dict=json.loads(file.read())
        print('db_details_dict : \n',yellow(db_details_dict,bold=True))
        file=open('./sqlite_databases_code/account_keys/init/account_keys.csv','w')
        ligne_out=''
        len_columns=len(db_details_dict['columns'])-1
        i=0        
        for col in db_details_dict['columns']:
            if i<len_columns:
                ligne_out=ligne_out+col+','
            else:
                ligne_out=ligne_out+col
            i+=1
        file.write(ligne_out+'\n')
        for i in range (0,10):
            ligne_out='name'+str(i)+','+'type'+str(i)+','+'username'+str(i)+','+'password'+str(i)+','+'key'+str(i)+','+'comment'+str(i)           
            file.write(ligne_out+'\n')
        file.close()  
        create_db_and_table(db_details_dict['db_name'],db_details_dict['table_name'])
        html_output='''<!DOCTYPE HTML>
<!-- description-->
<html>
    <head>
        <title>FLASK APP GENERATOR</title>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no" />
        <link rel="stylesheet" href="../static/assets/css/main.css" />
    <script>
        function popup_window( url, id, width, height )
        {
            //extract the url parameters if any, and pass them to the called html
            var tempvar=document.location.toString(); // fetch the URL string
            var passedparams = tempvar.lastIndexOf("?");
            if(passedparams > -1)
                url += tempvar.substring(passedparams);
            popup = window.open( url, id, 'toolbar=no,scrollbars=yes,location=yes,statusbar=yes,menubar=no,resizable=yes,width=' + width + ',height=' + height + '' );
            popup.focus();
        }
    </script>
    </head>
    <body class="is-preload">
        <!-- Nav -->
            <nav id="nav">
                <ul>
                
                    <li><a href="/">Back to main page</a></li>
                    <li><a href="/logout">log Out</a></li>
                    <li><a href="javascript:popup_window('/page_info?page=route_def_bases.py&route=/account_keys_create_db','page_info',700,600);">:</a></li>
        
                </ul>
            </nav>
        <!-- Portfolio -->
			<article id="top" class="wrapper style1">
				<div class="container">
					<div class="row">
						<div class="col-4 col-5-large col-12-medium">
							<span class="image fit"><img src="../static/images/ok.png" alt="" /></span>
						</div>
						<div class="col-8 col-7-large col-12-medium">
							<header>
								<h1><strong> Database :account_keys, was created</strong></h1>
							</header>
							<p>The SQLITE had been created in ./z_bases</p>
                            <a href="/account_keys_dashboard" class="button small scrolly">Go to Dashboard for account_keys DB </a>
						</div>						
					</div>				
				</div>
			</article>
        <!-- Scripts -->
            <script src="../static/assets/js/jquery.min.js"></script>
            <script src="../static/assets/js/jquery.scrolly.min.js"></script>
            <script src="../static/assets/js/init.js"></script>
            <script src="../static/assets/js/browser.min.js"></script>
            <script src="../static/assets/js/breakpoints.min.js"></script>
            <script src="../static/assets/js/util.js"></script>
            <script src="../static/assets/js/main.js"></script>
    </body>
</html>
'''
        loguer(env.level+' route END OF account_keys_create_db() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]    
        return html_output


#  def_account_keys_ingest_demo_data***
@app.route('/account_keys_ingest_demo_data', methods=['GET'])
def account_keys_ingest_demo_data():
    '''
    Flask Route for the account_keys_ingest_demo_data Database Ingest demo data
    '''
    route="/account_keys_ingest_demo_data"
    env.level+='-'
    print('\n'+env.level,white('route account_keys_ingest_demo_data() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route account_keys_ingest_demo_data() in ***app.py*** : >')
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        with open('./sqlite_databases_code/account_keys/db_details.txt') as file:
            db_details_dict=json.loads(file.read())
        print('db_details_dict : \n',yellow(db_details_dict,bold=True))
        database = os.getcwd()+'/z_bases/account_keys.db'
        database=database.replace("\\","/")
        print('database is :',database)
        lines=[]    
        file='./sqlite_databases_code/account_keys/init/account_keys.csv'
        with open (file) as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            lines = list(reader)
            indexA=0
            print('account_keys table =>\n')
            conn=create_connection(database) # open connection to database            
            for row in lines:
                if conn:
                    # connection to database is OK
                    c=conn.cursor()
                    # let's go to every lines one by one and let's extract url, targeted brand
                    sqlite_data=[indexA]
                    sqlite_data=(indexA,row[0] ,row[1] ,row[2] ,row[3] ,row[4] ,row[5])
                    sql_add="INSERT OR IGNORE into account_keys (`index`,name,type,username,password,key,comment) VALUES (?,?,?,?,?,?,?)"
                    print('\nsql_add :',cyan(sql_add,bold=True))
                c.execute(sql_add, sqlite_data)
                print(green("==> OK Done : demo data ingested",bold=True))
                indexA+=1
                conn.commit()        

        html_output='''<!DOCTYPE HTML>
<!-- description-->
<html>
    <head>
        <title>FLASK APP GENERATOR</title>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no" />
        <link rel="stylesheet" href="../static/assets/css/main.css" />
    <script>
        function popup_window( url, id, width, height )
        {
            //extract the url parameters if any, and pass them to the called html
            var tempvar=document.location.toString(); // fetch the URL string
            var passedparams = tempvar.lastIndexOf("?");
            if(passedparams > -1)
                url += tempvar.substring(passedparams);
            popup = window.open( url, id, 'toolbar=no,scrollbars=yes,location=yes,statusbar=yes,menubar=no,resizable=yes,width=' + width + ',height=' + height + '' );
            popup.focus();
        }
    </script>
    </head>
    <body class="is-preload">
        <!-- Nav -->
            <nav id="nav">
                <ul>
                
                    <li><a href="/">Back to main page</a></li>
                    <li><a href="/logout">log Out</a></li>
                    <li><a href="javascript:popup_window('/page_info?page=route_def_account_keys.py&route=/account_keys_ingest_demo_data_ingest_demo_data','page_info',700,600);">:</a></li>
        
                </ul>
            </nav>
        <!-- Portfolio -->
			<article id="top" class="wrapper style1">
				<div class="container">
					<div class="row">
						<div class="col-4 col-5-large col-12-medium">
							<span class="image fit"><img src="../static/images/ok.png" alt="" /></span>
						</div>
						<div class="col-8 col-7-large col-12-medium">
							<header>
								<h1><strong>Demo Data ingested</strong></h1>
							</header>
							<p>Demo Data ingested into Database :account_keys</p>
                            <a href="/account_keys_dashboard" class="button small scrolly">Go to Dashboard for account_keys DB </a>
						</div>						
					</div>				
				</div>
			</article>
        <!-- Scripts -->
            <script src="../static/assets/js/jquery.min.js"></script>
            <script src="../static/assets/js/jquery.scrolly.min.js"></script>
            <script src="../static/assets/js/init.js"></script>
            <script src="../static/assets/js/browser.min.js"></script>
            <script src="../static/assets/js/breakpoints.min.js"></script>
            <script src="../static/assets/js/util.js"></script>
            <script src="../static/assets/js/main.js"></script>
    </body>
</html>
'''
        loguer(env.level+' route END OF account_keys_ingest_demo_data() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]    
        return html_output


#  def_account_keys_db_clear***
@app.route('/account_keys_db_clear', methods=['GET'])
def account_keys_db_clear():
    '''
    Flask Route for the account_keys_db_clear Database Clearing / reset function
    '''
    route="/account_keys_db_clear"
    env.level+='-'
    print('\n'+env.level,white('route account_keys_db_clear() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route account_keys_db_clear() in ***app.py*** : >')
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        with open('./sqlite_databases_code/account_keys/db_details.txt') as file:
            db_details_dict=json.loads(file.read())
        print('db_details_dict : \n',yellow(db_details_dict,bold=True))
        database = os.getcwd()+'/z_bases/account_keys.db'
        database=database.replace("\\","/")
        print('database is :',database)
        print('table is :', db_details_dict["table_name"])
        conn=create_connection(database) # open connection to database
        if conn:
            # connection to database is OK
            c=conn.cursor()
            print(f'- Deleting table : {db_details_dict["table_name"]} =>')
            sql_request="drop table "+db_details_dict["table_name"]
            c.execute(sql_request)
            conn.commit()
            print('-- OK DONE : Deleted table : '+db_details_dict["table_name"])
            create_db_and_table(db_details_dict["db_name"],db_details_dict["table_name"])
            print(f'-- OK table {db_details_dict["table_name"]} reseted')     

        html_output='''<!DOCTYPE HTML>
<!-- description-->
<html>
    <head>
        <title>FLASK APP GENERATOR</title>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no" />
        <link rel="stylesheet" href="../static/assets/css/main.css" />
    <script>
        function popup_window( url, id, width, height )
        {
            //extract the url parameters if any, and pass them to the called html
            var tempvar=document.location.toString(); // fetch the URL string
            var passedparams = tempvar.lastIndexOf("?");
            if(passedparams > -1)
                url += tempvar.substring(passedparams);
            popup = window.open( url, id, 'toolbar=no,scrollbars=yes,location=yes,statusbar=yes,menubar=no,resizable=yes,width=' + width + ',height=' + height + '' );
            popup.focus();
        }
    </script>
    </head>
    <body class="is-preload">
        <!-- Nav -->
            <nav id="nav">
                <ul>
                
                    <li><a href="/">Back to main page</a></li>
                    <li><a href="/logout">log Out</a></li>
                    <li><a href="javascript:popup_window('/page_info?page=route_def_account_keys_db_clear.py&route=/account_keys_db_clear','page_info',700,600);">:</a></li>
        
                </ul>
            </nav>
        <!-- Portfolio -->
			<article id="top" class="wrapper style1">
				<div class="container">
					<div class="row">
						<div class="col-4 col-5-large col-12-medium">
							<span class="image fit"><img src="../static/images/ok.png" alt="" /></span>
						</div>
						<div class="col-8 col-7-large col-12-medium">
							<header>
								<h1><strong>Database Content Deleted</strong></h1>
							</header>
							<p>Data in Database : account_keys had been cleaned</p>
                            <a href="/account_keys_dashboard" class="button small scrolly">Go to Dashboard for account_keys DB </a>
						</div>						
					</div>				
				</div>
			</article>
        <!-- Scripts -->
            <script src="../static/assets/js/jquery.min.js"></script>
            <script src="../static/assets/js/jquery.scrolly.min.js"></script>
            <script src="../static/assets/js/init.js"></script>
            <script src="../static/assets/js/browser.min.js"></script>
            <script src="../static/assets/js/breakpoints.min.js"></script>
            <script src="../static/assets/js/util.js"></script>
            <script src="../static/assets/js/main.js"></script>
    </body>
</html>
'''
        loguer(env.level+' route END OF account_keys_db_clear() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]    
        return html_output


#  def_account_keys_db_read***
@app.route('/account_keys_db_read', methods=['GET'])
def account_keys_db_read():
    '''
    Flask Route for the account_keys_db_read Database Read DB content function
    '''
    route="/account_keys_db_read"
    env.level+='-'
    print('\n'+env.level,white('route account_keys_db_read() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route account_keys_db_read() in ***app.py*** : >')
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        keyword=''
        keyword=request.args.get("keyword")
        print("\nkeyword : ",keyword)      
        with open('./sqlite_databases_code/account_keys/db_details.txt') as file:
            db_details_dict=json.loads(file.read())
        print('db_details_dict : \n',yellow(db_details_dict,bold=True))
        database = os.getcwd()+'/z_bases/account_keys.db'
        database=database.replace("\\","/")
        print('database is :',database)
        # sqlite:///:memory: (or, sqlite://)
        # sqlite:///relative/path/to/file.db
        # sqlite:////absolute/path/to/file.db
        db_name = "account_keys.db"
        table_name = db_details_dict["table_name"]
        engine = sqlalchemy.create_engine("sqlite:///z_bases/%s" % db_name, execution_options={"sqlite_raw_colnames": True})
        df = pd.read_sql_table(table_name, engine)
        out_df = df[['index','name','type','username','password','key','comment']]
        #save result to csv file
        out_df.to_csv(r'./result/account_keys.csv')
        df = DataFrame(out_df)
        #print (df)
        select_options=''
        res = df.values.tolist()
        for item in res:
            if keyword:
                if keyword in item:
                    select_options=select_options+'<option value="'+str(item[0])+'">'+item[1]+'</option>'
            else:
                select_options=select_options+'<option value="'+str(item[0])+'">'+item[1]+'</option>'     
        print('=========================================')
        columns="name,type,username,password,key,comment"                
        print('DONE')        
        html_output='''<!DOCTYPE HTML>
<!-- description-->
<html>
    <head>
        <title>FLASK APP GENERATOR</title>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no" />
        <link rel="stylesheet" href="../static/assets/css/main.css" />
    <script>
        function popup_window( url, id, width, height )
        {
            //extract the url parameters if any, and pass them to the called html
            var tempvar=document.location.toString(); // fetch the URL string
            var passedparams = tempvar.lastIndexOf("?");
            if(passedparams > -1)
                url += tempvar.substring(passedparams);
            popup = window.open( url, id, 'toolbar=no,scrollbars=yes,location=yes,statusbar=yes,menubar=no,resizable=yes,width=' + width + ',height=' + height + '' );
            popup.focus();
        }
    </script>
    </head>
    <body class="is-preload">
        <!-- Nav -->
            <nav id="nav">
                <ul>
                
                    <li><a href="/">Back to main page</a></li>
                    <li><a href="/account_keys_dashboard">Back to Database Page</a></li>
                    <li><a href="/logout">log Out</a></li>
                    <li><a href="javascript:popup_window('/page_info?page=route_def_account_keys_db_read.py&route=/account_keys_db_read','page_info',700,600);">:</a></li>
        
                </ul>
            </nav>
			<article id="indic_list" class="wrapper style4">
				<div class="container medium">
					<header>
						<h2>Database Content</h2>
                        <p>Select a Row</p>
						<p>Or refine Search by keyword (in any columns)</p>
					</header>
					<div class="row">
						<div class="col-12">
							<form method="get" action="/db_row_details">
                            	<input type="hidden" name="database" value="account_keys">
                            	<input type="hidden" name="table" value="account_keys"> 
                                <input type="hidden" name="columns" value="'''+columns+'''">                                
								<div class="row">
									<div class="col-12">
										<select id="row" name="row">
                                            '''+select_options+'''           
                                        </select>
									</div>      
									<div class="col-12">
										<ul class="actions">
                                            <li><input type="submit" value="Select this row" class="button small scrolly" /></li>
										</ul>
									</div>                                    
								</div>
							</form>
						</div>    
                        <form method="get" action="/account_keys_db_read">
                            <div class="row">                        
                                <div class="col-6 col-12-small">
                                    <h3>Search Keyword :</h3>
                                </div>                                
                                <div class="col-6 col-12-small">
                                    <input type="text"  id="keyword" name="keyword" placeholder="keyword" />
                               </div>  
                                <div class="col-12">      
                                    <ul class="actions">
                                        <input type="submit" value="Search" class="button small scrolly" />
                                    </ul>
                                </div> 
                        </form>
					</div>
					<footer>
						<ul id="copyright">
							
						</ul>
					</footer>
				</div>
			</article>
        <!-- Scripts -->
            <script src="../static/assets/js/jquery.min.js"></script>
            <script src="../static/assets/js/jquery.scrolly.min.js"></script>
            <script src="../static/assets/js/init.js"></script>
            <script src="../static/assets/js/browser.min.js"></script>
            <script src="../static/assets/js/breakpoints.min.js"></script>
            <script src="../static/assets/js/util.js"></script>
            <script src="../static/assets/js/main.js"></script>
    </body>
</html>
'''
        loguer(env.level+' route END OF account_keys_db_read() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]    
        return html_output


#  def_account_keys_db_update_entry***
@app.route('/account_keys_db_update_entry', methods=['GET'])
def account_keys_db_update_entry():
    '''
    Flask Route for the account_keys_db_update_entry Database Update an entry
    '''
    route="/account_keys_db_update_entry"
    env.level+='-'
    print('\n'+env.level,white('route account_keys_db_update_entry() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route account_keys_db_update_entry() in ***app.py*** : >')
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        row=request.args.get("row")
        print("\nrow : ",row)
        name=request.args.get('name')
        print('\nname : ',name)
        type=request.args.get('type')
        print('\ntype : ',type)
        username=request.args.get('username')
        print('\nusername : ',username)
        password=request.args.get('password')
        print('\npassword : ',password)
        key=request.args.get('key')
        print('\nkey : ',key)
        comment=request.args.get('comment')
        print('\ncomment : ',comment)
        with open('./sqlite_databases_code/account_keys/db_details.txt') as file:
            db_details_dict=json.loads(file.read())
        print('db_details_dict : \n',yellow(db_details_dict,bold=True))        
        db_name = "account_keys.db"
        table_name = db_details_dict["table_name"]
        where_clause='`index` = '+row
        sql_fields=['index','name','type','username','password','key','comment']
        sql_data_list=[int(row),name,type,username,password,key,comment]
        result=sqlite_db_update_entry(db_name,table_name,where_clause,sql_fields,sql_data_list)        
        message1="OK done"
        image="../static/images/ok.png" 
        message2="entry had been updated"
        message3="/account_keys_dashboard"
        message4="account_keys Dashboard"
        PAGE_DESTINATION="operation_done"
        page_name="operation_done.html"
        loguer(env.level+' route END OF example_name() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]
        return render_template('main_index.html',route=route,USERNAME=session['user'],PAGE_DESTINATION=PAGE_DESTINATION,message1=message1,message2=message2,message3=message3,message4=message4,image=image,page_name=page_name)
 


#  def_account_keys_db_delete_entry***
@app.route('/account_keys_db_delete_entry', methods=['GET'])
def account_keys_db_delete_entry():
    '''
    Flask Route for the account_keys_db_delete_entry Database delete entry
    '''
    route="/account_keys_db_delete_entry"
    env.level+='-'
    print('\n'+env.level,white('route account_keys_db_delete_entry() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route account_keys_db_delete_entry() in ***app.py*** : >')
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        row=request.args.get("row")
        print("\nrow : ",row)
        result=sqlite_db_delete_entry('account_keys',row)         
        message1="OK done - Entry DELETED"
        image="../static/images/ok.png" 
        message2="entry had been deleted"
        message3="/account_keys_dashboard"
        message4="account_keys Dashboard"
        PAGE_DESTINATION="operation_done"
        page_name="operation_done.html"
        loguer(env.level+' route END OF example_name() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]
        return render_template('main_index.html',route=route,USERNAME=session['user'],PAGE_DESTINATION=PAGE_DESTINATION,message1=message1,message2=message2,message3=message3,message4=message4,image=image,page_name=page_name)
 


#  def_account_keys_db_add_entry***
@app.route('/account_keys_db_add_entry', methods=['GET'])
def account_keys_db_add_entry():
    '''
    Flask Route for the account_keys_db_add_entry Database Update an entry
    '''
    route="/account_keys_db_add_entry"
    env.level+='-'
    print('\n'+env.level,white('route account_keys_db_add_entry() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route account_keys_db_add_entry() in ***app.py*** : >')
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        db_name = "account_keys.db"
        column_list=['name','type','username','password','key','comment']
        print('\ncolumn_list :',cyan(column_list,bold=True))
        index=sqlite_db_get_last_index('account_keys')
        index+=1        
        print('index : ',index)
        PAGE_DESTINATION="z_sqlite_db_add_entry"
        page_name="z_sqlite_db_add_entry.html"
        db_name=db_name.split('.')[0]
        loguer(env.level+' route END OF example_name() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]
        return render_template('main_index.html',route=route,USERNAME=session['user'],PAGE_DESTINATION=PAGE_DESTINATION,page_name=page_name,column_list=column_list,index=index,db_name=db_name)
 


#  def_account_keys_db_add_entry_ok***
@app.route('/account_keys_db_add_entry_ok', methods=['GET'])
def account_keys_db_add_entry_ok():
    '''
    Flask Route for the account_keys_db_add_entry Database Update an entry
    '''
    route="/account_keys_db_add_entry_ok"
    env.level+='-'
    print('\n'+env.level,white('route account_keys_db_add_entry_ok() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route account_keys_db_add_entry_ok() in ***app.py*** : >')
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        name=request.args.get("name")
        print("\nname: ",name)
        type=request.args.get("type")
        print("\ntype: ",type)
        username=request.args.get("username")
        print("\nusername: ",username)
        password=request.args.get("password")
        print("\npassword: ",password)
        key=request.args.get("key")
        print("\nkey: ",key)
        comment=request.args.get("comment")
        print("\ncomment: ",comment)

        db_name=request.args.get("db_name")
        print('db_name :',db_name)     
        with open('./sqlite_databases_code/'+db_name+'/db_details.txt') as file:
            db_details_dict=json.loads(file.read())
        print('db_details_dict : \n',yellow(db_details_dict,bold=True)) 
        database = os.getcwd()+'/z_bases/'+db_name+'.db'
        database=database.replace("\\","/")
        table=db_details_dict['table_name']
        print('database is :',database) 
        print('table is :',table)          
        # Get last index value in SQLITE DB
        new_index=sqlite_db_get_last_index(db_name)+1        
        print('new_index is :',new_index)  
        sqlite_data=(new_index,name,type,username,password,key,comment)
        sql_add=f"INSERT OR IGNORE into {table} (`index`,name,type,username,password,key,comment) VALUES (?,?,?,?,?,?,?)"
        print('sqlite_data :',sqlite_data)     
        print('sql_add :',sql_add)          
        con = sqlite3.connect(database)       
        try:
            cur = con.cursor()
            cur.execute(sql_add,sqlite_data)
            con.commit()
            print(green('OK DONE ENTRY DELETED',bold=True))
            image="../static/images/ok.png" 
            message1="Entry Added"
            message2="Entry was added to DB"
            message3=f"/{db_name}_dashboard"
            message4=f"{db_name}_dasbhoard"        
            PAGE_DESTINATION="operation_done"
            page_name="operation_done.html"            
            loguer(env.level+' route END OF machin_db_add_entry_ok() in ***app.py*** : >')    
            env.level=env.level[:-1]        
            return render_template('main_index.html',route=route,USERNAME=session['user'],PAGE_DESTINATION=PAGE_DESTINATION,message1=message1,message2=message2,message3=message3,message4=message4,image=image,page_name=page_name) 
        except:
            print(red('Error',bold=True))
            image="../static/images/nok.png" 
            message1="Error"
            message2="An error occured"
            message3=f"/{db_name}_dashboard"
            message4=f"{db_name}_dasbhoard"        
            PAGE_DESTINATION="operation_done"
            page_name="operation_done.html"            
            loguer(env.level+' route END OF machin_db_add_entry_ok() in ***app.py*** : >')    
            env.level=env.level[:-1]        
            return render_template('main_index.html',route=route,USERNAME=session['user'],PAGE_DESTINATION=PAGE_DESTINATION,message1=message1,message2=message2,message3=message3,message4=message4,image=image,page_name=page_name)



#  def_account_keys_db_ingest_csv***
@app.route('/account_keys_db_ingest_csv', methods=['GET'])
def account_keys_db_ingest_csv():
    '''
    Flask Route for the account_keys_db_ingest_csv Database Update an entry
    '''
    route="/account_keys_db_ingest_csv"
    env.level+='-'
    print('\n'+env.level,white('route account_keys_db_ingest_csv() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route account_keys_db_ingest_csv() in ***app.py*** : >')
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        db_name="account_keys"
        message1="Message 1 :"
        image="../static/images/toolbox.png"
        message2="Message 2 :"
        message3="/Message 3"
        message4="Message 4 in button"
        PAGE_DESTINATION="z_sqlite_ingest_csv"
        page_name="z_sqlite_ingest_csv.html"
        loguer(env.level+' route END OF account_keys_db_ingest_csv() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]
        return render_template('main_index.html',route=route,USERNAME=session['user'],PAGE_DESTINATION=PAGE_DESTINATION,message1=message1,message2=message2,message3=message3,message4=message4,image=image,page_name=page_name,db_name=db_name) 


#  def_send_api_call***
@app.route('/send_api_call', methods=['GET'])
def send_api_call():
    '''
    Created : 2025-11-06
    description : Send the API call to URL Endpoint with the passed data
    '''
    route="/send_api_call"
    env.level+='-'
    print()
    print(env.level,white('route send_api_call() in app.py  : >\n',bold=True))
    loguer(env.level+' route send_api_call() in app.py  : > ')
    print()
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        global use_simulator
        base_url=request.args.get('base_url')
        print('\nbase_url : ',yellow(base_url,bold=True))
        name=request.args.get('name')
        print()
        print('name : ',yellow(name,bold=True))
        relative_url=request.args.get('relative_url')
        print()
        print('relative_url : ',yellow(relative_url,bold=True))
        api_documentation=request.args.get('api_docummentation')
        print()
        print('api_documentation : ',yellow(api_documentation,bold=True))
        method=request.args.get('method')
        print()
        print('method : ',yellow(method,bold=True))
        short_description=request.args.get('short_description')
        print()
        print('short_description : ',yellow(short_description,bold=True))
        payload=request.args.get('payload')
        payload=payload.replace('\n','')
        payload=payload.replace('\r','')
        payload=payload.replace('  ',' ')
        payload=payload.replace('  ',' ')
        payload=payload.replace('  ',' ')
        payload=payload.replace('  ',' ')
        print()
        print('payload : ',yellow(payload,bold=True))
        header=request.args.get('header')
        header=header.replace('\n','')
        header=header.replace('\r','')
        header=header.replace('  ',' ')
        header=header.replace('  ',' ')
        header=header.replace('  ',' ')
        header=header.replace('  ',' ')
        print()
        print('header : ',yellow(header,bold=True))
        body=request.args.get('body')
        body=body.replace('\n','')
        body=body.replace('\r','')
        body=body.replace('  ',' ')
        body=body.replace('  ',' ')
        body=body.replace('  ',' ')
        body=body.replace('  ',' ')
        print()
        print('body : ',yellow(body,bold=True))
        params=request.args.get('params')
        params=params.replace('\n','***')
        params=params.replace('\r','')
        params=params.replace('  ',' ')
        params=params.replace('  ',' ')
        params=params.replace('  ',' ')
        params=params.replace('  ',' ')
        print()
        print('params : ',yellow(params,bold=True))
        
        parameters=request.args.get('parameters')
        parameters=parameters.replace('\n','***')
        parameters=parameters.replace('\r','')
        parameters=parameters.replace('  ',' ')
        parameters=parameters.replace('  ',' ')
        parameters=parameters.replace('  ',' ')
        parameters=parameters.replace('  ',' ')
        print()
        print('parameters : ',yellow(parameters,bold=True))
        authentication_profile=request.args.get('authentication_profile')
        print()
        print('authentication_profile : ',yellow(authentication_profile,bold=True))
        filename='./api_calls_history/'+name+'_'+date_time_for_file_name()+'.txt'  # http://127.0.0.1:4000/code_edit?code=def_date_time_for_file_name.py&type=function
        with open(filename,'w') as file:
            file.write('name=:'+name+'\n')
            file.write('base_url=:'+base_url+'\n')
            file.write('relative_url=:'+relative_url+'\n')
            file.write('api_documentation=:'+api_documentation+'\n')
            file.write('method=:'+method+'\n')
            file.write('short_description=:'+short_description+'\n')
            file.write('payload=:'+payload+'\n')
            file.write('header=:'+header+'\n')
            file.write('body=:'+body+'\n')
            file.write('params=:'+params+'\n')
            file.write('parameters=:'+parameters+'\n')
            file.write('authentication_profile=:'+authentication_profile+'\n')
        with open('./result/last_api_call.txt','w') as file:
            file.write(filename)
        # Select Authentication Profile
        #api_key=''
        if authentication_profile!="saved_token":
            username,password,api_key=select_profile_function(authentication_profile) 
            
            authentication_dict={
                'username':username,
                'password':password,
                'api_key':api_key
            }
            print("\nauthentication_dict : ",yellow(authentication_dict,bold=True))  
        else:
            with open('./profiles/saved_token.txt') as file:
                api_key=file.read()
        if "@" in base_url:
            chunks=base_url.split('@')
            i=0
            new_chunks=[]
            for chunk in chunks:
                if 'https' in chunk or 'HTTPS' in chunk:
                    chunk=chunk.replace('https://','')
                    chunk=chunk.replace('HTTPS://','')
                    protocol='https'
                else:
                    chunk=chunk.replace('http://','')
                    chunk=chunk.replace('HTTP://','')      
                    protocol='http'                    
                print(chunk)    
                if i==0:
                    creds=chunk.split(':')
                    ii=0
                    new_cred_words=[]
                    for cred_word in creds:
                        if '$$' in cred_word:
                            mot=cred_word.replace('$$','')
                            mot=mot.replace('***','')                        
                        print(cyan(mot,bold=True))
                        new_cred_words.append(authentication_dict[mot])
                        ii+=1
                    print(yellow(new_cred_words,bold=True))
                    new_chunks.append(protocol+'://'+new_cred_words[0]+':'+new_cred_words[1]+'@')
                elif i==1:
                   new_chunks.append(chunk)
                i+=1
            if use_simulator==1:
                base_url=new_chunks[0].replace('https:','http:')+'localhost:4000'
            else:
                base_url=new_chunks[0]+new_chunks[1]
        else:
            if use_simulator==1:
                base_url='http://localhost:4000'

        print()
        print('final base_url to use : ',cyan(base_url,bold=True))                      
        additionnal_get_params='' # parameters at the end of the URL ?parm1=xxx?param2=yyy
        if body=='':
            body_json={}
        else:
            body_json=json.loads(body)
        if body_json == {"grant_type": "client_credentials"}:
            header_json=json.loads(header)
            result,response_txt=send_api_call_for_oauth_token(base_url,relative_url,client_id,client_password,header_json,body_json) # http://127.0.0.1:4000/code_edit?code=def_send_api_call_for_oauth_token.py&type=function
        elif payload == {"grant_type": "client_credentials"}:
            header_json=json.loads(header)
            result,response_txt=send_api_call_for_oauth_token(base_url,relative_url,client_id,client_password,header_json,body_json) # http://127.0.0.1:4000/code_edit?code=def_send_api_call_for_oauth_token.py&type=function
        else:
            print("\nOK SEND CALL (x166): ") 
            if api_key==None:
                api_key='xxx'
            print('api_key :',red(api_key,bold=True))       
            result,response_txt=send_api_call_function(method,base_url,relative_url,additionnal_get_params,header,payload,body,params,parameters,api_key) # http://127.0.0.1:4000/code_edit?code=def_send_api_call_function.py&type=function
        # read the first 200 lines of the JSON result
        with open('./json_results/json_result.json') as file:
            lines=file.read().split('\n')
        print('  lines : \n',lines)
        response_txt=''
        ii=0
        for line in lines:
            response_txt=response_txt+line+'\n'
            ii+=1
            if ii>200:
                response_txt=response_txt+'..... Rest of response is not shown... it was too long \n\n=> You can click on the [ Display in Tree Graph ] button  to see the entire content'
                break
        # #########################################################
        if result==1:
            image="../static/images/ok.png"
            message1=response_txt
            message2="Connexion to XDR Tenant is Okay !"
            message3="#portfolio"
            message4="Button Message"
            PAGE_DESTINATION="z_api_call_result"
            page_name="z_api_call_result.html"
            env.level=env.level[:-1]
            return render_template('main_index.html',route=route,USERNAME=session['user'],PAGE_DESTINATION=PAGE_DESTINATION,message1=message1,message2=message2,message3=message3,message4=message4,image=image,page_name=page_name)
        else:
            image="../static/images/nok.png"
            message1="Operation Failed"
            message2="An Error Occured"
            message3="/"
            message4="Home"
            PAGE_DESTINATION="operation_done"
            page_name="operation_done.html"
            loguer(env.level+' route send_api_call() in app.py  : > ')
            env.level=env.level[:-1]
            return render_template('main_index.html',route=route,USERNAME=session['user'],PAGE_DESTINATION=PAGE_DESTINATION,message1=message1,message2=message2,message3=message3,message4=message4,image=image,page_name=page_name)
        



#  def_dtree***
@app.route('/dtree', methods=['GET'])
def dtree():
    '''
    Created : 2025-07-18T14:58:59.000Z

    description : call the dtree function that will create the dtree graph in the template subfolder
    '''
    route="/dtree"
    env.level+='-'
    print()
    print(env.level,white('route dtree() in app.py  : >\n',bold=True))
    loguer(env.level+' route dtree() in app.py  : > ')
    print()
    global api_key
    global orgID
    global host
    global network_id
    global profil_name
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        filename=request.args.get('filename')
        filename=filename.split('***')[0]
        print()
        print('filename : ',filename)  
        html_content=go_analyse_json(filename)
        # ===================================================================
        env.level=env.level[:-1]
        return html_content
        



#  def_cse_get_event_type_api***
@app.route('/cse_get_event_type_api', methods=['GET','POST'])
def cse_get_event_type_api():
    '''
    Created : 2025-10-27T18:50:55.000Z

    description : Secure Endpoint Get every event types in this tenant and output their details
    '''
    route="/cse_get_event_type_api"
    env.level+='-'
    print('\n'+env.level,white('route cse_get_event_type_api() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route cse_get_event_type_api() in ***app.py*** : >')
    global client_id
    global client_password
    global host
    global host_for_token
    global profil_name
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        name = request.form.get("name")
        print("\nname : ",name)
        base_url = request.form.get("base_url")
        print("\nbase_url : ",base_url)
        relative_url = request.form.get("relative_url")
        print("\nrelative_url : ",relative_url)
        api_docummentation = request.form.get("api_docummentation")
        print("\napi_docummentation : ",api_docummentation)  
        short_description = request.form.get("short_description")
        print("\nshort_description : ",short_description)  
        payload = request.form.get("payload")
        print("\npayload : ",payload) 
        method = request.form.get("method")
        print("\nmethod : ",method)  
        header = request.form.get("header")
        print("\nheader : ",header)  
        body = request.form.get("body")
        print("\nbody : ",body)  
        params = request.form.get("params")
        print("\nparams : ",params)  
        parameters = request.form.get("parameters")
        print("\nparameters : ",parameters)  
        authentication_profile = request.form.get("authentication_profile")
        print("\nauthentication_profile : ",authentication_profile)  
        inputs = request.form.get("inputs")
        print("\ninputs : ",inputs)  
        outputs = request.form.get("outputs")
        print("\noutputs : ",outputs) 
        PAGE_DESTINATION="z_cse_get_event_type_api"
        page_name="z_cse_get_event_type_api.html"
        loguer(env.level+' route END OF cse_get_event_type_api() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]
        return render_template('main_index.html',route=route,USERNAME=session['user'],PAGE_DESTINATION=PAGE_DESTINATION,page_name=page_name,name=name,base_url=base_url,relative_url=relative_url,api_docummentation=api_docummentation,short_description=short_description,payload=payload,method=method,header=header,body=body,params=params,parameters=parameters,authentication_profile=authentication_profile,inputs=inputs,outputs=outputs)
        


#  def_generic_api_details***
@app.route('/generic_api_details', methods=['GET'])
def generic_api_details():
    '''
    Created : 2025-10-28T08:25:17.000Z

    description : display API details before sending the API Call
    '''
    route="/generic_api_details"
    env.level+='-'
    print('\n'+env.level,white('route generic_api_details() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route generic_api_details() in ***app.py*** : >')
    global client_id
    global client_password
    global host
    global host_for_token
    global profil_name
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        database="api_calls"
        print("\ndatabase : ",database)
        table="api_calls"
        print("\ntable : ",table)
        #name='Secure Endpoint Get Computers'
        name=request.args.get('name')
        where_clause=f'where `name` = "{name}"'
        entry_list=sqlite_db_select_entry(database,table,where_clause)
        print("\nentry_list : \n",entry_list)
        name=entry_list[0][1]
        base_url=entry_list[0][2]
        relative_url=entry_list[0][3]
        api_docummentation=entry_list[0][4]
        method=entry_list[0][5]
        short_description=entry_list[0][6]
        payload=entry_list[0][7]
        header=entry_list[0][8]
        body=entry_list[0][9]
        params=entry_list[0][10]
        parameters=entry_list[0][11]
        authentication_profile=entry_list[0][12]
        inputs=entry_list[0][13]
        outputs=entry_list[0][14]
        image="../static/images/API.png"
        PAGE_DESTINATION="z_selected_api"
        page_name="z_selected_api.html"
        loguer(env.level+' route END OF cse_get_computer() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]
        return render_template('main_index.html',route=route,USERNAME=session['user'],PAGE_DESTINATION=PAGE_DESTINATION,image=image,page_name=page_name,name=name,base_url=base_url,relative_url=relative_url,api_docummentation=api_docummentation,method=method,short_description=short_description,payload=payload,header=header,body=body,params=params,parameters=parameters,authentication_profile=authentication_profile)
       


#  def_product_api_call***
@app.route('/product_api_call', methods=['GET','POST'])
def product_api_call():
    '''
    Created : 2025-10-26T10:01:07.000Z

    description : run the CSE get computer API formular
    '''
    route="/product_api_call"
    env.level+='-'
    print('\n'+env.level,white('route product_api_call() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route product_api_call() in ***app.py*** : >')
    global client_id
    global client_password
    global host
    global host_for_token
    global profil_name
    if not session.get('logged_in'):
        return render_template('login.html')
    else:  
        name = request.form.get("name")
        print("\nname : ",name)
        base_url = request.form.get("base_url")
        print("\nbase_url : ",base_url)
        relative_url = request.form.get("relative_url")
        print("\nrelative_url : ",relative_url)
        api_docummentation = request.form.get("api_docummentation")
        print("\napi_docummentation : ",api_docummentation)  
        short_description = request.form.get("short_description")
        print("\nshort_description : ",short_description)  
        payload = request.form.get("payload")
        print("\npayload : ",payload) 
        method = request.form.get("method")
        print("\nmethod : ",method)  
        header = request.form.get("header")
        print("\nheader : ",header)  
        body = request.form.get("body")
        print("\nbody : ",body)  
        params = request.form.get("params")
        print("\nparams : ",params)  
        parameters = request.form.get("parameters")
        print("\nparameters : ",parameters)  
        authentication_profile = request.form.get("authentication_profile")
        print("\nauthentication_profile : ",authentication_profile)  
        inputs = request.form.get("inputs")
        print("\ninputs : ",inputs)  
        outputs = request.form.get("outputs")
        print("\noutputs : ",outputs)          
        PAGE_DESTINATION="z_product_api_call"
        page_name="z_product_api_call.html"
        loguer(env.level+' route END OF product_api_call() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]
        return render_template('main_index.html',route=route,USERNAME=session['user'],PAGE_DESTINATION=PAGE_DESTINATION,page_name=page_name,name=name,base_url=base_url,relative_url=relative_url,api_docummentation=api_docummentation,short_description=short_description,payload=payload,method=method,header=header,body=body,params=params,parameters=parameters,authentication_profile=authentication_profile,inputs=inputs,outputs=outputs)
        


#  def_workflows_dashboard***
@app.route('/workflows_dashboard', methods=['GET'])
def workflows_dashboard():
    '''
    Flask Route for the workflows_dashboard Database dashoard
    '''
    route="/workflows_dashboard"
    env.level+='-'
    print('\n'+env.level,white('route workflows_dashboard() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route workflows_dashboard() in ***app.py*** : >')
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        html_output='''<!DOCTYPE HTML>
<!-- description-->
<html>
    <head>
        <title>FLASK APP GENERATOR</title>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no" />
        <link rel="stylesheet" href="../static/assets/css/main.css" />
    <script>
        function popup_window( url, id, width, height )
        {
            //extract the url parameters if any, and pass them to the called html
            var tempvar=document.location.toString(); // fetch the URL string
            var passedparams = tempvar.lastIndexOf("?");
            if(passedparams > -1)
                url += tempvar.substring(passedparams);
            popup = window.open( url, id, 'toolbar=no,scrollbars=yes,location=yes,statusbar=yes,menubar=no,resizable=yes,width=' + width + ',height=' + height + '' );
            popup.focus();
        }
    </script>
    </head>
    <body class="is-preload">
        <!-- Nav -->
            <nav id="nav">
                <ul>
                
                    <li><a href="/">Back to main page</a></li>
                    <li><a href="/logout">log Out</a></li>
                    <li><a href="javascript:popup_window('/page_info?page=route_def_workflows_dashboard.py&route=/workflows_dashboard','page_info',700,600);">:</a></li>
        
                </ul>
            </nav>
        <!-- Portfolio -->
            <article id="portfolio" class="wrapper style3">
                <div class="container">
                    <header>
                        <h2>workflows Database</h2>
                    </header>
                    <div class="row">
                        <div class="col-4 col-6-medium col-12-small">
                            <article class="box style2">
                                <a href="/workflows_create_db" class="image featured"><img src="../static/images/database0.png" alt="" /></a>
                                <h3><a href="/workflows_create_db">Create Database</a></h3>
                                <p>Create the workflows Database</p>
                            </article>
                        </div>
                        <div class="col-4 col-6-medium col-12-small">
                            <article class="box style2">
                                <a href="/workflows_ingest_demo_data" class="image featured"><img src="../static/images/database0.png" alt="" /></a>
                                <h3><a href="/workflows_ingest_demo_data">Ingest Demo Data</a></h3>
                                <p>Ingest Demo Data into DB</p>
                            </article>
                        </div>
                        <div class="col-4 col-6-medium col-12-small">
                            <article class="box style2">
                                <a href="/workflows_db_read_custom" class="image featured"><img src="../static/images/database0.png" alt="" /></a>
                                <h3><a href="/workflows_db_read_custom">Read Database content</a></h3>
                                <p>Read DB content and get access to entries</p>
                            </article>
                        </div> 
                        <div class="col-4 col-6-medium col-12-small">
                            <article class="box style2">
                                <a href="/workflows_db_clear" class="image featured"><img src="../static/images/database0.png" alt="" /></a>
                                <h3><a href="/workflows_db_clear">Clear Database</a></h3>
                                <p>Delete Database content</p>
                            </article>
                        </div>
                        <div class="col-4 col-6-medium col-12-small">
                            <article class="box style2">
                                <a href="/workflows_db_ingest_csv" class="image featured"><img src="../static/images/database0.png" alt="" /></a>
                                <h3><a href="/workflows_db_ingest_csv">Ingest a CSV file</a></h3>
                                <p>Ingest a CSV file</p>
                            </article>
                        </div>
                        <div class="col-4 col-6-medium col-12-small">
                            <article class="box style2">
                                <a href="/workflows_db_add_entry" class="image featured"><img src="../static/images/database0.png" alt="" /></a>
                                <h3><a href="/workflows_db_add_entry">Add Entry</a></h3>
                                <p>Add an Entry to Database</p>
                            </article>
                        </div>          
                        <div class="col-4 col-6-medium col-12-small">
                            <article class="box style2">
                                <a href="/workflows_solution" class="image featured"><img src="../static/images/database0.png" alt="" /></a>
                                <h3><a href="/workflows_solution">Install Solution</a></h3>
                                <p>Install Workflow solution</p>
                            </article>
                        </div>                           
                    </div>
                </div>
            </article>
        <!-- Scripts -->
            <script src="../static/assets/js/jquery.min.js"></script>
            <script src="../static/assets/js/jquery.scrolly.min.js"></script>
            <script src="../static/assets/js/init.js"></script>
            <script src="../static/assets/js/browser.min.js"></script>
            <script src="../static/assets/js/breakpoints.min.js"></script>
            <script src="../static/assets/js/util.js"></script>
            <script src="../static/assets/js/main.js"></script>
    </body>
</html>
'''
        loguer(env.level+' route END OF workflows_dashboard() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]
        return html_output
        

#  def_workflows_create_db***
@app.route('/workflows_create_db', methods=['GET'])
def workflows_create_db():
    '''
    Flask Route for the workflows_create_db Database Create DB action
    '''
    route="/workflows_create_db"
    env.level+='-'
    print('\n'+env.level,white('route workflows_create_db() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route workflows_create_db() in ***app.py*** : >')
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        with open('./sqlite_databases_code/workflows/db_details.txt') as file:
            db_details_dict=json.loads(file.read())
        print('db_details_dict : \n',yellow(db_details_dict,bold=True))
        file=open('./sqlite_databases_code/workflows/init/workflows.csv','w')
        ligne_out=''
        len_columns=len(db_details_dict['columns'])-1
        i=0        
        for col in db_details_dict['columns']:
            if i<len_columns:
                ligne_out=ligne_out+col+','
            else:
                ligne_out=ligne_out+col
            i+=1
        file.write(ligne_out+'\n')
        for i in range (0,10):
            ligne_out='workflow_name'+str(i)+','+'step'+str(i)+','+'step_name'+str(i)+','+'input'+str(i)+','+'output'+str(i)+','+'comment'+str(i)           
            file.write(ligne_out+'\n')
        file.close()  
        create_db_and_table(db_details_dict['db_name'],db_details_dict['table_name'])
        html_output='''<!DOCTYPE HTML>
<!-- description-->
<html>
    <head>
        <title>FLASK APP GENERATOR</title>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no" />
        <link rel="stylesheet" href="../static/assets/css/main.css" />
    <script>
        function popup_window( url, id, width, height )
        {
            //extract the url parameters if any, and pass them to the called html
            var tempvar=document.location.toString(); // fetch the URL string
            var passedparams = tempvar.lastIndexOf("?");
            if(passedparams > -1)
                url += tempvar.substring(passedparams);
            popup = window.open( url, id, 'toolbar=no,scrollbars=yes,location=yes,statusbar=yes,menubar=no,resizable=yes,width=' + width + ',height=' + height + '' );
            popup.focus();
        }
    </script>
    </head>
    <body class="is-preload">
        <!-- Nav -->
            <nav id="nav">
                <ul>
                
                    <li><a href="/">Back to main page</a></li>
                    <li><a href="/logout">log Out</a></li>
                    <li><a href="javascript:popup_window('/page_info?page=route_def_bases.py&route=/workflows_create_db','page_info',700,600);">:</a></li>
        
                </ul>
            </nav>
        <!-- Portfolio -->
			<article id="top" class="wrapper style1">
				<div class="container">
					<div class="row">
						<div class="col-4 col-5-large col-12-medium">
							<span class="image fit"><img src="../static/images/ok.png" alt="" /></span>
						</div>
						<div class="col-8 col-7-large col-12-medium">
							<header>
								<h1><strong> Database :workflows, was created</strong></h1>
							</header>
							<p>The SQLITE had been created in ./z_bases</p>
                            <a href="/workflows_dashboard" class="button small scrolly">Go to Dashboard for workflows DB </a>
						</div>						
					</div>				
				</div>
			</article>
        <!-- Scripts -->
            <script src="../static/assets/js/jquery.min.js"></script>
            <script src="../static/assets/js/jquery.scrolly.min.js"></script>
            <script src="../static/assets/js/init.js"></script>
            <script src="../static/assets/js/browser.min.js"></script>
            <script src="../static/assets/js/breakpoints.min.js"></script>
            <script src="../static/assets/js/util.js"></script>
            <script src="../static/assets/js/main.js"></script>
    </body>
</html>
'''
        loguer(env.level+' route END OF workflows_create_db() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]    
        return html_output


#  def_workflows_ingest_demo_data***
@app.route('/workflows_ingest_demo_data', methods=['GET'])
def workflows_ingest_demo_data():
    '''
    Flask Route for the workflows_ingest_demo_data Database Ingest demo data
    '''
    route="/workflows_ingest_demo_data"
    env.level+='-'
    print('\n'+env.level,white('route workflows_ingest_demo_data() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route workflows_ingest_demo_data() in ***app.py*** : >')
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        with open('./sqlite_databases_code/workflows/db_details.txt') as file:
            db_details_dict=json.loads(file.read())
        print('db_details_dict : \n',yellow(db_details_dict,bold=True))
        database = os.getcwd()+'/z_bases/workflows.db'
        database=database.replace("\\","/")
        print('database is :',database)
        lines=[]    
        file='./sqlite_databases_code/workflows/init/workflows.csv'
        with open (file) as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            lines = list(reader)
            indexA=0
            print('workflows table =>\n')
            conn=create_connection(database) # open connection to database            
            for row in lines:
                if conn:
                    # connection to database is OK
                    c=conn.cursor()
                    # let's go to every lines one by one and let's extract url, targeted brand
                    sqlite_data=[indexA]
                    sqlite_data=(indexA,row[0] ,row[1] ,row[2] ,row[3] ,row[4] ,row[5])
                    sql_add="INSERT OR IGNORE into workflows (`index`,workflow_name,step,step_name,input,output,comment) VALUES (?,?,?,?,?,?,?)"
                    print('\nsql_add :',cyan(sql_add,bold=True))
                c.execute(sql_add, sqlite_data)
                print(green("==> OK Done : demo data ingested",bold=True))
                indexA+=1
                conn.commit()        

        html_output='''<!DOCTYPE HTML>
<!-- description-->
<html>
    <head>
        <title>FLASK APP GENERATOR</title>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no" />
        <link rel="stylesheet" href="../static/assets/css/main.css" />
    <script>
        function popup_window( url, id, width, height )
        {
            //extract the url parameters if any, and pass them to the called html
            var tempvar=document.location.toString(); // fetch the URL string
            var passedparams = tempvar.lastIndexOf("?");
            if(passedparams > -1)
                url += tempvar.substring(passedparams);
            popup = window.open( url, id, 'toolbar=no,scrollbars=yes,location=yes,statusbar=yes,menubar=no,resizable=yes,width=' + width + ',height=' + height + '' );
            popup.focus();
        }
    </script>
    </head>
    <body class="is-preload">
        <!-- Nav -->
            <nav id="nav">
                <ul>
                
                    <li><a href="/">Back to main page</a></li>
                    <li><a href="/logout">log Out</a></li>
                    <li><a href="javascript:popup_window('/page_info?page=route_def_workflows.py&route=/workflows_ingest_demo_data_ingest_demo_data','page_info',700,600);">:</a></li>
        
                </ul>
            </nav>
        <!-- Portfolio -->
			<article id="top" class="wrapper style1">
				<div class="container">
					<div class="row">
						<div class="col-4 col-5-large col-12-medium">
							<span class="image fit"><img src="../static/images/ok.png" alt="" /></span>
						</div>
						<div class="col-8 col-7-large col-12-medium">
							<header>
								<h1><strong>Demo Data ingested</strong></h1>
							</header>
							<p>Demo Data ingested into Database :workflows</p>
                            <a href="/workflows_dashboard" class="button small scrolly">Go to Dashboard for workflows DB </a>
						</div>						
					</div>				
				</div>
			</article>
        <!-- Scripts -->
            <script src="../static/assets/js/jquery.min.js"></script>
            <script src="../static/assets/js/jquery.scrolly.min.js"></script>
            <script src="../static/assets/js/init.js"></script>
            <script src="../static/assets/js/browser.min.js"></script>
            <script src="../static/assets/js/breakpoints.min.js"></script>
            <script src="../static/assets/js/util.js"></script>
            <script src="../static/assets/js/main.js"></script>
    </body>
</html>
'''
        loguer(env.level+' route END OF workflows_ingest_demo_data() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]    
        return html_output


#  def_workflows_db_clear***
@app.route('/workflows_db_clear', methods=['GET'])
def workflows_db_clear():
    '''
    Flask Route for the workflows_db_clear Database Clearing / reset function
    '''
    route="/workflows_db_clear"
    env.level+='-'
    print('\n'+env.level,white('route workflows_db_clear() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route workflows_db_clear() in ***app.py*** : >')
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        with open('./sqlite_databases_code/workflows/db_details.txt') as file:
            db_details_dict=json.loads(file.read())
        print('db_details_dict : \n',yellow(db_details_dict,bold=True))
        database = os.getcwd()+'/z_bases/workflows.db'
        database=database.replace("\\","/")
        print('database is :',database)
        print('table is :', db_details_dict["table_name"])
        conn=create_connection(database) # open connection to database
        if conn:
            # connection to database is OK
            c=conn.cursor()
            print(f'- Deleting table : {db_details_dict["table_name"]} =>')
            sql_request="drop table "+db_details_dict["table_name"]
            c.execute(sql_request)
            conn.commit()
            print('-- OK DONE : Deleted table : '+db_details_dict["table_name"])
            create_db_and_table(db_details_dict["db_name"],db_details_dict["table_name"])
            print(f'-- OK table {db_details_dict["table_name"]} reseted')     

        html_output='''<!DOCTYPE HTML>
<!-- description-->
<html>
    <head>
        <title>FLASK APP GENERATOR</title>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no" />
        <link rel="stylesheet" href="../static/assets/css/main.css" />
    <script>
        function popup_window( url, id, width, height )
        {
            //extract the url parameters if any, and pass them to the called html
            var tempvar=document.location.toString(); // fetch the URL string
            var passedparams = tempvar.lastIndexOf("?");
            if(passedparams > -1)
                url += tempvar.substring(passedparams);
            popup = window.open( url, id, 'toolbar=no,scrollbars=yes,location=yes,statusbar=yes,menubar=no,resizable=yes,width=' + width + ',height=' + height + '' );
            popup.focus();
        }
    </script>
    </head>
    <body class="is-preload">
        <!-- Nav -->
            <nav id="nav">
                <ul>
                
                    <li><a href="/">Back to main page</a></li>
                    <li><a href="/logout">log Out</a></li>
                    <li><a href="javascript:popup_window('/page_info?page=route_def_workflows_db_clear.py&route=/workflows_db_clear','page_info',700,600);">:</a></li>
        
                </ul>
            </nav>
        <!-- Portfolio -->
			<article id="top" class="wrapper style1">
				<div class="container">
					<div class="row">
						<div class="col-4 col-5-large col-12-medium">
							<span class="image fit"><img src="../static/images/ok.png" alt="" /></span>
						</div>
						<div class="col-8 col-7-large col-12-medium">
							<header>
								<h1><strong>Database Content Deleted</strong></h1>
							</header>
							<p>Data in Database : workflows had been cleaned</p>
                            <a href="/workflows_dashboard" class="button small scrolly">Go to Dashboard for workflows DB </a>
						</div>						
					</div>				
				</div>
			</article>
        <!-- Scripts -->
            <script src="../static/assets/js/jquery.min.js"></script>
            <script src="../static/assets/js/jquery.scrolly.min.js"></script>
            <script src="../static/assets/js/init.js"></script>
            <script src="../static/assets/js/browser.min.js"></script>
            <script src="../static/assets/js/breakpoints.min.js"></script>
            <script src="../static/assets/js/util.js"></script>
            <script src="../static/assets/js/main.js"></script>
    </body>
</html>
'''
        loguer(env.level+' route END OF workflows_db_clear() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]    
        return html_output


#  def_workflows_db_read***
@app.route('/workflows_db_read', methods=['GET'])
def workflows_db_read():
    '''
    Flask Route for the workflows_db_read Database Read DB content function
    '''
    route="/workflows_db_read"
    env.level+='-'
    print('\n'+env.level,white('route workflows_db_read() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route workflows_db_read() in ***app.py*** : >')
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        keyword=''
        keyword=request.args.get("keyword")
        print("\nkeyword : ",keyword)
        with open('./sqlite_databases_code/workflows/db_details.txt') as file:
            db_details_dict=json.loads(file.read())
        print('db_details_dict : \n',yellow(db_details_dict,bold=True))
        database = os.getcwd()+'/z_bases/workflows.db'
        database=database.replace("\\","/")
        print('database is :',database)
        # sqlite:///:memory: (or, sqlite://)
        # sqlite:///relative/path/to/file.db
        # sqlite:////absolute/path/to/file.db
        db_name = "workflows.db"
        table_name = db_details_dict["table_name"]
        engine = sqlalchemy.create_engine("sqlite:///z_bases/%s" % db_name, execution_options={"sqlite_raw_colnames": True})
        df = pd.read_sql_table(table_name, engine)
        out_df = df[['index','workflow_name','step','step_name','input','output','comment']]
        #save result to csv file
        out_df.to_csv(r'./result/workflows.csv')
        df = DataFrame(out_df)
        #print (df)
        select_options=''
        res = df.values.tolist()
        element_index=2
        sorted_list=sorted(res, key=lambda x: x[element_index])
                    
        for item in sorted_list:
            if keyword:
                if keyword in item:
                    select_options=select_options+'<option value="'+str(item[2])+'">'+item[2]+'</option>'
            else:
                select_options=select_options+'<option value="'+str(item[2])+'">'+item[2]+'</option>'
        print('=========================================')
        columns="workflow_name,step,step_name,input,output,comment"
        print('DONE')
        html_output='''<!DOCTYPE HTML>
<!-- description-->
<html>
    <head>
        <title>FLASK APP GENERATOR</title>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no" />
        <link rel="stylesheet" href="../static/assets/css/main.css" />
    <script>
        function popup_window( url, id, width, height )
        {
            //extract the url parameters if any, and pass them to the called html
            var tempvar=document.location.toString(); // fetch the URL string
            var passedparams = tempvar.lastIndexOf("?");
            if(passedparams > -1)
                url += tempvar.substring(passedparams);
            popup = window.open( url, id, 'toolbar=no,scrollbars=yes,location=yes,statusbar=yes,menubar=no,resizable=yes,width=' + width + ',height=' + height + '' );
            popup.focus();
        }
    </script>
    </head>
    <body class="is-preload">
        <!-- Nav -->
            <nav id="nav">
                <ul>
                
                    <li><a href="/">Back to main page</a></li>
                    <li><a href="/workflows_dashboard">Back to Database Page</a></li>
                    <li><a href="/logout">log Out</a></li>
                    <li><a href="javascript:popup_window('/page_info?page=route_def_workflows_db_read.py&route=/workflows_db_read','page_info',700,600);">:</a></li>
        
                </ul>
            </nav>
            <article id="indic_list" class="wrapper style4">
                <div class="container medium">
                    <header>
                        <h2>Database Content</h2>
                        <p>Select a Row</p>
                        <p>Or refine Search by keyword (in any columns)</p>
                    </header>
                    <div class="row">
                        <div class="col-12">
                            <form method="get" action="/workflows_step_details">
                                <input type="hidden" name="database" value="workflows">
                                <input type="hidden" name="table" value="workflows">
                                <input type="hidden" name="columns" value="'''+columns+'''">
                                <div class="row">
                                    <div class="col-12">
                                        <select id="step" name="step">
                                        '''+select_options+'''
                                        </select>
                                    </div>
                                    <div class="col-12">
                                        <ul class="actions">
                                        <li><input type="submit" value="Select this row" class="button small scrolly" /></li>
                                        </ul>
                                    </div>
                                </div>
                            </form>
                        </div>
                        <form method="get" action="/workflows_db_read">
                            <div class="row">
                                <div class="col-6 col-12-small">
                                    <h3>Search Keyword :</h3>
                                </div>
                                <div class="col-6 col-12-small">
                                    <input type="text"  id="keyword" name="keyword" placeholder="keyword" />
                                </div>
                                <div class="col-12">
                                    <ul class="actions">
                                        <input type="submit" value="Search" class="button small scrolly" />
                                    </ul>
                                </div>
                        </form>
                    </div>
                    <footer>
                        <ul id="copyright">
                            
                        </ul>
                    </footer>
                </div>
            </article>
        <!-- Scripts -->
            <script src="../static/assets/js/jquery.min.js"></script>
            <script src="../static/assets/js/jquery.scrolly.min.js"></script>
            <script src="../static/assets/js/init.js"></script>
            <script src="../static/assets/js/browser.min.js"></script>
            <script src="../static/assets/js/breakpoints.min.js"></script>
            <script src="../static/assets/js/util.js"></script>
            <script src="../static/assets/js/main.js"></script>
    </body>
</html>
'''
        loguer(env.level+' route END OF workflows_db_read() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]
        return html_output


#  def_workflows_db_update_entry***
@app.route('/workflows_db_update_entry', methods=['GET'])
def workflows_db_update_entry():
    '''
    version 20251105
    Flask Route for the workflows_db_update_entry Database Update an entry
    '''
    route="/workflows_db_update_entry"
    env.level+='-'
    print('\n'+env.level,white('route workflows_db_update_entry() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route workflows_db_update_entry() in ***app.py*** : >')
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        row=request.args.get("row")
        print("\nrow : ",row)
        workflow_name=request.args.get('workflow_name')
        print('\nworkflow_name : ',workflow_name)        
        step=request.args.get('step')
        print('\nstep : ',step)
        if "**" not in step:
            # NEW STEP
            int_step=int(step.split(' ')[1])
            #renumber_steps_minus_one(int_step)
            #renumber_steps(int_step)
        else:
            step=step.replace("**","")
        step_custom=request.args.get('step_custom')
        print('\nstep_custom : ',step_custom)   
        if step_custom!="":
            step=step_custom
        step_prefix=request.args.get('step_prefix')
        print('\nstep_prefix : ',step_prefix)        
        step_name=request.args.get('step_name')
        if step_prefix!='':
            step_name=step_prefix+' <=> '+step_name
        print('\nstep_name : ',step_name)
        custom_input=request.args.get('custom_input')
        print('\ncustom_input : ',custom_input)
        input=request.args.get('input')
        if custom_input!='':
            input=custom_input  
        if input=='':
            input="None"
        print('\ninput : ',input)        
        custom_output=request.args.get('custom_output') 
        print('\ncustom_output : ',custom_output)
        output=request.args.get('output')
        if custom_output!='':
            output=custom_output        
        if output=='':
            output="None"            
        print('\noutput : ',output)
        comment=request.args.get('comment')
        print('\ncomment : ',comment)
        with open('./sqlite_databases_code/workflows/db_details.txt') as file:
            db_details_dict=json.loads(file.read())
        print('db_details_dict : \n',yellow(db_details_dict,bold=True))        
        db_name = "workflows.db"
        table_name = db_details_dict["table_name"]
        where_clause='`index` = '+row
        sql_fields=['index','workflow_name','step','step_name','input','output','comment']
        sql_data_list=[int(row),workflow_name,step,step_name,input,output,comment]
        result=sqlite_db_update_entry(db_name,table_name,where_clause,sql_fields,sql_data_list)        
        message1="OK done"
        image="../static/images/ok.png" 
        message2="entry had been updated"
        message3="/workflows_dashboard"
        message4="workflows Dashboard"
        PAGE_DESTINATION="operation_done"
        page_name="operation_done.html"
        loguer(env.level+' route END OF example_name() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]
        return render_template('main_index.html',route=route,USERNAME=session['user'],PAGE_DESTINATION=PAGE_DESTINATION,message1=message1,message2=message2,message3=message3,message4=message4,image=image,page_name=page_name)
 


#  def_workflows_db_delete_entry***
@app.route('/workflows_db_delete_entry', methods=['GET'])
def workflows_db_delete_entry():
    '''
    Flask Route for the workflows_db_delete_entry Database delete entry
    '''
    route="/workflows_db_delete_entry"
    env.level+='-'
    print('\n'+env.level,white('route workflows_db_delete_entry() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route workflows_db_delete_entry() in ***app.py*** : >')
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        row=request.args.get("row")
        print("\nrow : ",row)        
        # GET variable from calling web page
        step=request.args.get("step")
        print("\nstep : ",step)
        database="workflows"
        print("\ndatabase : ",database)
        table="workflows"
        print("\ntable : ",table)
        where_clause=f'where `index` = "{row}"'
        entry_list=sqlite_db_select_entry(database,table,where_clause)
        print("\nentry_list : \n",entry_list)
        row=str(entry_list[0][0])
        workflow_name=entry_list[0][1]
        step=entry_list[0][2]
        step_name=entry_list[0][3]          
        input=entry_list[0][4]
        output=entry_list[0][5]
        comment=entry_list[0][6]          
        result=renumber_steps_delete(step)       
        result=sqlite_db_delete_entry('workflows',row)            
        db_name = "workflows.db"
        table_name = "workflows"
        engine = sqlalchemy.create_engine("sqlite:///z_bases/%s" % db_name, execution_options={"sqlite_raw_colnames": True})
        df = pd.read_sql_table(table_name, engine)
        out_df = df[['index','workflow_name','step','step_name','input','output','comment']]
        #save result to csv file
        #out_df.to_csv(r'./result/workflows.csv')
        df = DataFrame(out_df)
        #print (df)
        select_options=''
        res = df.values.tolist()
        step_dict={}
        for item in res:
            print(item)    
            step_dict[item[2]]={
                'title':item[2],
                'description':item[3]
            }         
        print('step_dict : ' ,yellow(step_dict,bold=True))
        # sort detection by steps
        sorted_dict = {}
        step_list=[]
        for item,value in step_dict.items():
            print('item:\n',yellow(item,bold=True))   
            print('value:\n',yellow(value,bold=True))
            step_list.append([value['title'],item])
        sorted_step_list = sorted(step_list, key=operator.itemgetter(0),reverse=False)     
        print()
        print('sorted step_list:\n',cyan(sorted_step_list,bold=True))   
        print()     
        for step in sorted_step_list:
            for item,valeur in step_dict.items():
                if item==step[1] and valeur['title']== step[0]:
                    sorted_dict[item] = step_dict[item]
                    break    
        
        print('=========================================')
        columns="workflow_name,step,step_name,input,output,comment"    
        message1="Message 1 :"
        image="../static/images/toolbox.png" 
        message2="Message 2 :"
        message3="/Message 3"
        message4="Message 4 in button"
        PAGE_DESTINATION="z_workflows"
        page_name="z_workflows.html"
        loguer(env.level+' route END OF workflows() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]
        return render_template('main_index.html',route=route,USERNAME=session['user'],PAGE_DESTINATION=PAGE_DESTINATION,page_name=page_name,step_dict=sorted_dict)

#  def_workflows_db_add_entry***
@app.route('/workflows_db_add_entry', methods=['GET'])
def workflows_db_add_entry():
    '''
    Flask Route for the workflows_db_add_entry Database Update an entry
    '''
    route="/workflows_db_add_entry"
    env.level+='-'
    print('\n'+env.level,white('route workflows_db_add_entry() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route workflows_db_add_entry() in ***app.py*** : >')
    if not session.get('logged_in'):
        return render_template('login.html')
    else:        
        db_name = "workflows.db"
        column_list=['workflow_name','step','step_name','input','output','comment']
        print('\ncolumn_list :',cyan(column_list,bold=True))
        index=sqlite_db_get_last_index('workflows')
        index+=1        
        print('index : ',index)
        # step list
        step_list_dict={}
        table_name = "workflows"
        engine = sqlalchemy.create_engine("sqlite:///z_bases/%s" % db_name, execution_options={"sqlite_raw_colnames": True})
        df = pd.read_sql_table(table_name, engine)
        out_df = df[['index','workflow_name','step','step_name','input','output','comment']]
        df = DataFrame(out_df)
        #print (df)
        res = df.values.tolist()
        steps_dict={}
        nb_step=0
        for item in res:
            print(item)    
            steps_dict[item[2]]={
                'title':item[2],
                'index':item[0]
            }  
            nb_step+=1
        print('steps_dict : ' ,yellow(steps_dict,bold=True))
        # sort detection by steps
        sorted_dict = {}
        step_list=[]
        for item,value in steps_dict.items():
            print('item:\n',yellow(item,bold=True))   
            print('value:\n',yellow(value,bold=True))
            step_list.append([value['title'],item])
        sorted_step_list = sorted(step_list, key=operator.itemgetter(0),reverse=False)     
        print()
        print('sorted step_list:\n',cyan(sorted_step_list,bold=True))   
        print()     
        for step in sorted_step_list:
            for item,valeur in steps_dict.items():
                if item==step[1] and valeur['title']== step[0]:
                    sorted_dict[item] = steps_dict[item]
                    break         
        # calculate next step
        next_step=nb_step+1
        if next_step==1:
            str_next_step='Step 01'
        elif next_step==2:
            str_next_step='Step 02'    
        elif next_step==3:
            str_next_step='Step 03' 
        elif next_step==4:
            str_next_step='Step 04' 
        elif next_step==5:
            str_next_step='Step 05' 
        elif next_step==6:
            str_next_step='Step 06' 
        elif next_step==7:
            str_next_step='Step 07' 
        elif next_step==8:
            str_next_step='Step 08'     
        elif next_step==9:
            str_next_step='Step 09'             
        else:
            str_next_step='Step '+str(next_step)        
        # API Calls
        db_name = "api_calls.db"
        table_name = "api_calls"
        engine = sqlalchemy.create_engine("sqlite:///z_bases/%s" % db_name, execution_options={"sqlite_raw_colnames": True})
        df = pd.read_sql_table(table_name, engine)
        out_df = df[['index','name','fqdn','relative_url','documentation','method','description','payload','header','body','query_params','custom_variables','authentication_profile','inputs_variables','output_variables']]
        #save result to csv file
        #out_df.to_csv(r'./result/api_calls.csv')
        df = DataFrame(out_df)
        #print (df)
        #save result to csv file
        #out_df.to_csv(r'./result/workflows.csv')
        df = DataFrame(out_df)
        #print (df)
        res = df.values.tolist()
        function_dict={}
        for item in res:
            print(item)    
            function_dict[item[1]]={
                'title':item[1],
            }                
        # Functions
        db_name = "functions.db"
        table_name = "functions"
        engine = sqlalchemy.create_engine("sqlite:///z_bases/%s" % db_name, execution_options={"sqlite_raw_colnames": True})
        df = pd.read_sql_table(table_name, engine)
        out_df = df[['index','name','environment_name','description','called_function','input_variables','output_variables','comment']]
        df = DataFrame(out_df)
        #print (df)
        res = df.values.tolist()
        for item in res:
            print(item)    
            function_dict[item[1]]={
                'title':item[1],
            }         
        
        # Variables
        db_name = "variables.db"
        table_name = "variables"
        engine = sqlalchemy.create_engine("sqlite:///z_bases/%s" % db_name, execution_options={"sqlite_raw_colnames": True})
        df = pd.read_sql_table(table_name, engine)
        out_df = df[['index','name','environment_name','value','description','comment','used_by']]
        df = DataFrame(out_df)
        #print (df)
        res = df.values.tolist()
        variables_dict={}
        for item in res:
            print(item)    
            variables_dict[item[1]]={
                'title':item[1],
            }       
        sorted_variables_dict = {}
        variables_list=[]
        for item,value in variables_dict.items():
            print('item:\n',yellow(item,bold=True))   
            print('value:\n',yellow(value,bold=True))
            variables_list.append([value['title'],item])
        sorted_variables_list = sorted(variables_list, key=operator.itemgetter(0),reverse=False)     
        print('\nsorted_variables_list:\n',cyan(sorted_variables_list,bold=True))     
        for step in sorted_variables_list:
            for item,valeur in variables_dict.items():
                if item==step[1] and valeur['title']== step[0]:
                    sorted_variables_dict[item] = variables_dict[item]
                    break
            
        PAGE_DESTINATION="z_sqlite_db_add_entry_custom"
        page_name="z_sqlite_db_add_entry_custom.html"
        db_name="workflows"
        loguer(env.level+' route END OF example_name() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]
        return render_template('main_index.html',route=route,USERNAME=session['user'],PAGE_DESTINATION=PAGE_DESTINATION,page_name=page_name,column_list=column_list,index=index,db_name=db_name,steps_dict=sorted_dict,function_dict=function_dict,variables_dict=sorted_variables_dict,str_next_step=str_next_step,next_step=next_step)
 


#  def_workflows_db_add_entry_ok***
@app.route('/workflows_db_add_entry_ok', methods=['GET'])
def workflows_db_add_entry_ok():
    '''
        version : 20251103
        Flask Route for the workflows_db_add_entry Database Update an entry
    '''
    route="/workflows_db_add_entry_ok"
    env.level+='-'
    print('\n'+env.level,white('route workflows_db_add_entry_ok() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route workflows_db_add_entry_ok() in ***app.py*** : >')
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        workflow_name=request.args.get("workflow_name")
        print("\nworkflow_name: ",workflow_name)
        step=request.args.get("step")
        print("\nstep: ",step)        
        if 'Step' not in step:
            if step=='1':
                step='Step 01'
            elif step=='2':
                step='Step 02'    
            elif step=='3':
                step='Step 03' 
            elif step=='4':
                step='Step 04' 
            elif step=='5':
                step='Step 05' 
            elif step=='6':
                step='Step 06' 
            elif step=='7':
                step='Step 07' 
            elif step=='8':
                step='Step 08'     
            elif step=='9':
                step='Step 09'             
            else:
                step='Step '+step
        else:
            insert_in_position=step.split(' ')[1]
            insert_in_position=int(insert_in_position)
            result=renumber_steps(insert_in_position)
        print("\nstep: ",step)
        step_prefix=request.args.get('step_prefix')
        print('\nstep_prefix : ',step_prefix)        
        step_name=request.args.get('step_name')
        if step_prefix!='':
            step_name=step_prefix+' <=> '+step_name
        print("\nstep_name: ",step_name)
        custom_input=request.args.get('custom_input')
        print('\ncustom_input : ',custom_input)        
        input=request.args.get("input")
        if custom_input!='':
            input=custom_input          
        if input=='':
            input="None" 
        print("\ninput: ",input)

        custom_output=request.args.get('custom_output') 
        print('\ncustom_output : ',custom_output)        
        output=request.args.get("output")
        if custom_output!='':
            output=custom_output         
        if output=='':
            output="None" 
        print("\noutput: ",output)
        comment=request.args.get("comment")
        print("\ncomment: ",comment)
        # ##############################
        db_name="workflows"
        print('db_name :',db_name)     
        with open('./sqlite_databases_code/'+db_name+'/db_details.txt') as file:
            db_details_dict=json.loads(file.read())
        print('db_details_dict : \n',yellow(db_details_dict,bold=True)) 
        database = os.getcwd()+'/z_bases/'+db_name+'.db'
        database=database.replace("\\","/")
        table=db_details_dict['table_name']
        print('database is :',database) 
        print('table is :',table)          
        # Get last index value in SQLITE DB
        new_index=sqlite_db_get_last_index(db_name)+1        
        print('new_index is :',new_index)  
        sqlite_data=(new_index,workflow_name,step,step_name,input,output,comment)
        sql_add=f"INSERT OR IGNORE into {table} (`index`,workflow_name,step,step_name,input,output,comment) VALUES (?,?,?,?,?,?,?)"
        print('sqlite_data :',sqlite_data)     
        print('sql_add :',sql_add)          
        con = sqlite3.connect(database)       
        try:
            cur = con.cursor()
            cur.execute(sql_add,sqlite_data)
            con.commit()
            print(green('OK DONE ENTRY ADDED',bold=True))
            db_name = "workflows.db"
            table_name = "workflows"
            engine = sqlalchemy.create_engine("sqlite:///z_bases/%s" % db_name, execution_options={"sqlite_raw_colnames": True})
            df = pd.read_sql_table(table_name, engine)
            out_df = df[['index','workflow_name','step','step_name','input','output','comment']]
            #save result to csv file
            #out_df.to_csv(r'./result/workflows.csv')
            df = DataFrame(out_df)
            #print (df)
            select_options=''
            res = df.values.tolist()
            step_dict={}
            for item in res:
                print(item)    
                step_dict[item[2]]={
                    'title':item[2],
                    'description':item[3]
                }         
            print('step_dict : ' ,yellow(step_dict,bold=True))
            # sort detection by steps
            sorted_dict = {}
            step_list=[]
            for item,value in step_dict.items():
                print('item:\n',yellow(item,bold=True))   
                print('value:\n',yellow(value,bold=True))
                step_list.append([value['title'],item])
            sorted_step_list = sorted(step_list, key=operator.itemgetter(0),reverse=False)     
            print()
            print('sorted step_list:\n',cyan(sorted_step_list,bold=True))   
            print()     
            for step in sorted_step_list:
                for item,valeur in step_dict.items():
                    if item==step[1] and valeur['title']== step[0]:
                        sorted_dict[item] = step_dict[item]
                        break    
            
            print('=========================================')
            columns="workflow_name,step,step_name,input,output,comment"    
            message1="Message 1 :"
            image="../static/images/toolbox.png" 
            message2="Message 2 :"
            message3="/Message 3"
            message4="Message 4 in button"
            PAGE_DESTINATION="z_workflows"
            page_name="z_workflows.html"
            loguer(env.level+' route END OF workflows() in ***app.py*** : >')
            # ===================================================================
            env.level=env.level[:-1]
            return render_template('main_index.html',route=route,USERNAME=session['user'],PAGE_DESTINATION=PAGE_DESTINATION,page_name=page_name,step_dict=sorted_dict)
        except:
            print(red('Error',bold=True))
            image="../static/images/nok.png" 
            message1="Error"
            message2="An error occured"
            message3=f"/{db_name}_dashboard"
            message4=f"{db_name}_dasbhoard"        
            PAGE_DESTINATION="operation_done"
            page_name="operation_done.html"            
            env.level=env.level[:-1]        
            return render_template('main_index.html',route=route,USERNAME=session['user'],PAGE_DESTINATION=PAGE_DESTINATION,message1=message1,message2=message2,message3=message3,message4=message4,image=image,page_name=page_name)
        

#  def_workflows_db_ingest_csv***
@app.route('/workflows_db_ingest_csv', methods=['GET'])
def workflows_db_ingest_csv():
    '''
    Flask Route for the workflows_db_ingest_csv Database Update an entry
    '''
    route="/workflows_db_ingest_csv"
    env.level+='-'
    print('\n'+env.level,white('route workflows_db_ingest_csv() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route workflows_db_ingest_csv() in ***app.py*** : >')
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        db_name="workflows"
        message1="Message 1 :"
        image="../static/images/toolbox.png"
        message2="Message 2 :"
        message3="/Message 3"
        message4="Message 4 in button"
        PAGE_DESTINATION="z_sqlite_ingest_csv"
        page_name="z_sqlite_ingest_csv.html"
        loguer(env.level+' route END OF workflows_db_ingest_csv() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]
        return render_template('main_index.html',route=route,USERNAME=session['user'],PAGE_DESTINATION=PAGE_DESTINATION,message1=message1,message2=message2,message3=message3,message4=message4,image=image,page_name=page_name,db_name=db_name) 


#  def_workflows_db_duplicate_entry***
@app.route('/workflows_db_duplicate_entry', methods=['GET'])
def workflows_db_duplicate_entry():
    '''
    Flask Route for the workflows_db_duplicate_entry Database delete entry
    '''
    route="/workflows_db_duplicate_entry"
    env.level+='-'
    print('\n'+env.level,white('route workflows_db_duplicate_entry() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route workflows_db_duplicate_entry() in ***app.py*** : >')
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        row=request.args.get("row")
        print("\nrow : ",row)        
        result=sqlite_db_duplicate_workflow_entry('workflows',row)         
        last_step=''
        db_name = "workflows"
        table="workflows"
        print('database is :',db_name) 
        print('table is :',table)          
        # read entry in data base
        where_clause=''
        full_list=sqlite_db_select_entry(db_name,table,where_clause)    
        for item in full_list:
            #print(item[2])
            if item[2]>last_step:
                last_step=item[2]
        print("\nLast step is : \n",last_step)         
        message1="OK done - Entry DUPLICATED"
        image="../static/images/ok.png" 
        message2="entry had been duplicated"
        message3="/workflows_step_details?step="+last_step
        message4="Edit New Step"
        PAGE_DESTINATION="operation_done"
        page_name="operation_done.html"
        loguer(env.level+' route END OF example_name() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]
        return render_template('main_index.html',route=route,USERNAME=session['user'],PAGE_DESTINATION=PAGE_DESTINATION,message1=message1,message2=message2,message3=message3,message4=message4,image=image,page_name=page_name)
 


#  def_api_calls_dashboard***
@app.route('/api_calls_dashboard', methods=['GET'])
def api_calls_dashboard():
    '''
    Flask Route for the api_calls_dashboard Database dashoard
    '''
    route="/api_calls_dashboard"
    env.level+='-'
    print('\n'+env.level,white('route api_calls_dashboard() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route api_calls_dashboard() in ***app.py*** : >')
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        html_output='''<!DOCTYPE HTML>
<!-- description-->
<html>
    <head>
        <title>FLASK APP GENERATOR</title>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no" />
        <link rel="stylesheet" href="../static/assets/css/main.css" />
    <script>
        function popup_window( url, id, width, height )
        {
            //extract the url parameters if any, and pass them to the called html
            var tempvar=document.location.toString(); // fetch the URL string
            var passedparams = tempvar.lastIndexOf("?");
            if(passedparams > -1)
                url += tempvar.substring(passedparams);
            popup = window.open( url, id, 'toolbar=no,scrollbars=yes,location=yes,statusbar=yes,menubar=no,resizable=yes,width=' + width + ',height=' + height + '' );
            popup.focus();
        }
    </script>
    </head>
    <body class="is-preload">
        <!-- Nav -->
            <nav id="nav">
                <ul>
                
                    <li><a href="/">Back to main page</a></li>
                    <li><a href="/logout">log Out</a></li>
                    <li><a href="javascript:popup_window('/page_info?page=route_def_api_calls_dashboard.py&route=/api_calls_dashboard','page_info',700,600);">:</a></li>
        
                </ul>
            </nav>
        <!-- Portfolio -->
            <article id="portfolio" class="wrapper style3">
                <div class="container">
                    <header>
                        <h2>api_calls Database</h2>
                    </header>
                    <div class="row">
                        <div class="col-4 col-6-medium col-12-small">
                            <article class="box style2">
                                <a href="/api_calls_create_db" class="image featured"><img src="../static/images/database0.png" alt="" /></a>
                                <h3><a href="/api_calls_create_db">Create Database</a></h3>
                                <p>Create the api_calls Database</p>
                            </article>
                        </div>
                        <div class="col-4 col-6-medium col-12-small">
                            <article class="box style2">
                                <a href="/api_calls_ingest_demo_data" class="image featured"><img src="../static/images/database0.png" alt="" /></a>
                                <h3><a href="/api_calls_ingest_demo_data">Ingest Demo Data</a></h3>
                                <p>Ingest Demo Data into DB</p>
                            </article>
                        </div>
                        <div class="col-4 col-6-medium col-12-small">
                            <article class="box style2">
                                <a href="/api_calls_db_read" class="image featured"><img src="../static/images/database0.png" alt="" /></a>
                                <h3><a href="/api_calls_db_read">Read Database content</a></h3>
                                <p>Read DB an Create a CSV result</p>
                            </article>
                        </div>
                        <div class="col-4 col-6-medium col-12-small">
                            <article class="box style2">
                                <a href="/api_calls_db_clear" class="image featured"><img src="../static/images/database0.png" alt="" /></a>
                                <h3><a href="/api_calls_db_clear">Clear Database</a></h3>
                                <p>Delete Database content</p>
                            </article>
                        </div>
                        <div class="col-4 col-6-medium col-12-small">
                            <article class="box style2">
                                <a href="/api_calls_db_ingest_csv" class="image featured"><img src="../static/images/database0.png" alt="" /></a>
                                <h3><a href="/api_calls_db_ingest_csv">Ingest a CSV file</a></h3>
                                <p>Ingest a CSV file</p>
                            </article>
                        </div>
                        <div class="col-4 col-6-medium col-12-small">
                            <article class="box style2">
                                <a href="/api_calls_db_add_entry" class="image featured"><img src="../static/images/database0.png" alt="" /></a>
                                <h3><a href="/api_calls_db_add_entry">Add Entry</a></h3>
                                <p>Add an Entry to Database</p>
                            </article>
                        </div>
            
                    </div>
                </div>
            </article>
        <!-- Scripts -->
            <script src="../static/assets/js/jquery.min.js"></script>
            <script src="../static/assets/js/jquery.scrolly.min.js"></script>
            <script src="../static/assets/js/init.js"></script>
            <script src="../static/assets/js/browser.min.js"></script>
            <script src="../static/assets/js/breakpoints.min.js"></script>
            <script src="../static/assets/js/util.js"></script>
            <script src="../static/assets/js/main.js"></script>
    </body>
</html>
'''
        loguer(env.level+' route END OF api_calls_dashboard() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]
        return html_output
        

#  def_api_calls_create_db***
@app.route('/api_calls_create_db', methods=['GET'])
def api_calls_create_db():
    '''
    Flask Route for the api_calls_create_db Database Create DB action
    '''
    route="/api_calls_create_db"
    env.level+='-'
    print('\n'+env.level,white('route api_calls_create_db() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route api_calls_create_db() in ***app.py*** : >')
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        with open('./sqlite_databases_code/api_calls/db_details.txt') as file:
            db_details_dict=json.loads(file.read())
        print('db_details_dict : \n',yellow(db_details_dict,bold=True))
        file=open('./sqlite_databases_code/api_calls/init/api_calls.csv','w')
        ligne_out=''
        len_columns=len(db_details_dict['columns'])-1
        i=0        
        for col in db_details_dict['columns']:
            if i<len_columns:
                ligne_out=ligne_out+col+','
            else:
                ligne_out=ligne_out+col
            i+=1
        file.write(ligne_out+'\n')
        for i in range (0,10):
            ligne_out='name'+str(i)+','+'fqdn'+str(i)+','+'relative_url'+str(i)+','+'documentation'+str(i)+','+'method'+str(i)+','+'description'+str(i)+','+'payload'+str(i)+','+'header'+str(i)+','+'body'+str(i)+','+'query_params'+str(i)+','+'custom_variables'+str(i)+','+'authentication_profile'+str(i)+','+'inputs_variables'+str(i)+','+'output_variables'+str(i)           
            file.write(ligne_out+'\n')
        file.close()  
        create_db_and_table(db_details_dict['db_name'],db_details_dict['table_name'])
        html_output='''<!DOCTYPE HTML>
<!-- description-->
<html>
    <head>
        <title>FLASK APP GENERATOR</title>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no" />
        <link rel="stylesheet" href="../static/assets/css/main.css" />
    <script>
        function popup_window( url, id, width, height )
        {
            //extract the url parameters if any, and pass them to the called html
            var tempvar=document.location.toString(); // fetch the URL string
            var passedparams = tempvar.lastIndexOf("?");
            if(passedparams > -1)
                url += tempvar.substring(passedparams);
            popup = window.open( url, id, 'toolbar=no,scrollbars=yes,location=yes,statusbar=yes,menubar=no,resizable=yes,width=' + width + ',height=' + height + '' );
            popup.focus();
        }
    </script>
    </head>
    <body class="is-preload">
        <!-- Nav -->
            <nav id="nav">
                <ul>
                
                    <li><a href="/">Back to main page</a></li>
                    <li><a href="/logout">log Out</a></li>
                    <li><a href="javascript:popup_window('/page_info?page=route_def_bases.py&route=/api_calls_create_db','page_info',700,600);">:</a></li>
        
                </ul>
            </nav>
        <!-- Portfolio -->
			<article id="top" class="wrapper style1">
				<div class="container">
					<div class="row">
						<div class="col-4 col-5-large col-12-medium">
							<span class="image fit"><img src="../static/images/ok.png" alt="" /></span>
						</div>
						<div class="col-8 col-7-large col-12-medium">
							<header>
								<h1><strong> Database :api_calls, was created</strong></h1>
							</header>
							<p>The SQLITE had been created in ./z_bases</p>
                            <a href="/api_calls_dashboard" class="button small scrolly">Go to Dashboard for api_calls DB </a>
						</div>						
					</div>				
				</div>
			</article>
        <!-- Scripts -->
            <script src="../static/assets/js/jquery.min.js"></script>
            <script src="../static/assets/js/jquery.scrolly.min.js"></script>
            <script src="../static/assets/js/init.js"></script>
            <script src="../static/assets/js/browser.min.js"></script>
            <script src="../static/assets/js/breakpoints.min.js"></script>
            <script src="../static/assets/js/util.js"></script>
            <script src="../static/assets/js/main.js"></script>
    </body>
</html>
'''
        loguer(env.level+' route END OF api_calls_create_db() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]    
        return html_output


#  def_api_calls_ingest_demo_data***
@app.route('/api_calls_ingest_demo_data', methods=['GET'])
def api_calls_ingest_demo_data():
    '''
    Flask Route for the api_calls_ingest_demo_data Database Ingest demo data
    '''
    route="/api_calls_ingest_demo_data"
    env.level+='-'
    print('\n'+env.level,white('route api_calls_ingest_demo_data() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route api_calls_ingest_demo_data() in ***app.py*** : >')
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        with open('./sqlite_databases_code/api_calls/db_details.txt') as file:
            db_details_dict=json.loads(file.read())
        print('db_details_dict : \n',yellow(db_details_dict,bold=True))
        database = os.getcwd()+'/z_bases/api_calls.db'
        database=database.replace("\\","/")
        print('database is :',database)
        lines=[]    
        file='./sqlite_databases_code/api_calls/init/api_calls.csv'
        with open (file) as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            lines = list(reader)
            indexA=0
            print('api_calls table =>\n')
            conn=create_connection(database) # open connection to database            
            for row in lines:
                if conn:
                    # connection to database is OK
                    c=conn.cursor()
                    # let's go to every lines one by one and let's extract url, targeted brand
                    sqlite_data=[indexA]
                    sqlite_data=(indexA,row[0] ,row[1] ,row[2] ,row[3] ,row[4] ,row[5] ,row[6] ,row[7] ,row[8] ,row[9] ,row[10] ,row[11] ,row[12] ,row[13])
                    sql_add="INSERT OR IGNORE into api_calls (`index`,name,fqdn,relative_url,documentation,method,description,payload,header,body,query_params,custom_variables,authentication_profile,inputs_variables,output_variables) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
                    print('\nsql_add :',cyan(sql_add,bold=True))
                c.execute(sql_add, sqlite_data)
                print(green("==> OK Done : demo data ingested",bold=True))
                indexA+=1
                conn.commit()        

        html_output='''<!DOCTYPE HTML>
<!-- description-->
<html>
    <head>
        <title>FLASK APP GENERATOR</title>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no" />
        <link rel="stylesheet" href="../static/assets/css/main.css" />
    <script>
        function popup_window( url, id, width, height )
        {
            //extract the url parameters if any, and pass them to the called html
            var tempvar=document.location.toString(); // fetch the URL string
            var passedparams = tempvar.lastIndexOf("?");
            if(passedparams > -1)
                url += tempvar.substring(passedparams);
            popup = window.open( url, id, 'toolbar=no,scrollbars=yes,location=yes,statusbar=yes,menubar=no,resizable=yes,width=' + width + ',height=' + height + '' );
            popup.focus();
        }
    </script>
    </head>
    <body class="is-preload">
        <!-- Nav -->
            <nav id="nav">
                <ul>
                
                    <li><a href="/">Back to main page</a></li>
                    <li><a href="/logout">log Out</a></li>
                    <li><a href="javascript:popup_window('/page_info?page=route_def_api_calls.py&route=/api_calls_ingest_demo_data_ingest_demo_data','page_info',700,600);">:</a></li>
        
                </ul>
            </nav>
        <!-- Portfolio -->
			<article id="top" class="wrapper style1">
				<div class="container">
					<div class="row">
						<div class="col-4 col-5-large col-12-medium">
							<span class="image fit"><img src="../static/images/ok.png" alt="" /></span>
						</div>
						<div class="col-8 col-7-large col-12-medium">
							<header>
								<h1><strong>Demo Data ingested</strong></h1>
							</header>
							<p>Demo Data ingested into Database :api_calls</p>
                            <a href="/api_calls_dashboard" class="button small scrolly">Go to Dashboard for api_calls DB </a>
						</div>						
					</div>				
				</div>
			</article>
        <!-- Scripts -->
            <script src="../static/assets/js/jquery.min.js"></script>
            <script src="../static/assets/js/jquery.scrolly.min.js"></script>
            <script src="../static/assets/js/init.js"></script>
            <script src="../static/assets/js/browser.min.js"></script>
            <script src="../static/assets/js/breakpoints.min.js"></script>
            <script src="../static/assets/js/util.js"></script>
            <script src="../static/assets/js/main.js"></script>
    </body>
</html>
'''
        loguer(env.level+' route END OF api_calls_ingest_demo_data() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]    
        return html_output


#  def_api_calls_db_clear***
@app.route('/api_calls_db_clear', methods=['GET'])
def api_calls_db_clear():
    '''
    Flask Route for the api_calls_db_clear Database Clearing / reset function
    '''
    route="/api_calls_db_clear"
    env.level+='-'
    print('\n'+env.level,white('route api_calls_db_clear() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route api_calls_db_clear() in ***app.py*** : >')
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        with open('./sqlite_databases_code/api_calls/db_details.txt') as file:
            db_details_dict=json.loads(file.read())
        print('db_details_dict : \n',yellow(db_details_dict,bold=True))
        database = os.getcwd()+'/z_bases/api_calls.db'
        database=database.replace("\\","/")
        print('database is :',database)
        print('table is :', db_details_dict["table_name"])
        conn=create_connection(database) # open connection to database
        if conn:
            # connection to database is OK
            c=conn.cursor()
            print(f'- Deleting table : {db_details_dict["table_name"]} =>')
            sql_request="drop table "+db_details_dict["table_name"]
            c.execute(sql_request)
            conn.commit()
            print('-- OK DONE : Deleted table : '+db_details_dict["table_name"])
            create_db_and_table(db_details_dict["db_name"],db_details_dict["table_name"])
            print(f'-- OK table {db_details_dict["table_name"]} reseted')     

        html_output='''<!DOCTYPE HTML>
<!-- description-->
<html>
    <head>
        <title>FLASK APP GENERATOR</title>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no" />
        <link rel="stylesheet" href="../static/assets/css/main.css" />
    <script>
        function popup_window( url, id, width, height )
        {
            //extract the url parameters if any, and pass them to the called html
            var tempvar=document.location.toString(); // fetch the URL string
            var passedparams = tempvar.lastIndexOf("?");
            if(passedparams > -1)
                url += tempvar.substring(passedparams);
            popup = window.open( url, id, 'toolbar=no,scrollbars=yes,location=yes,statusbar=yes,menubar=no,resizable=yes,width=' + width + ',height=' + height + '' );
            popup.focus();
        }
    </script>
    </head>
    <body class="is-preload">
        <!-- Nav -->
            <nav id="nav">
                <ul>
                
                    <li><a href="/">Back to main page</a></li>
                    <li><a href="/logout">log Out</a></li>
                    <li><a href="javascript:popup_window('/page_info?page=route_def_api_calls_db_clear.py&route=/api_calls_db_clear','page_info',700,600);">:</a></li>
        
                </ul>
            </nav>
        <!-- Portfolio -->
			<article id="top" class="wrapper style1">
				<div class="container">
					<div class="row">
						<div class="col-4 col-5-large col-12-medium">
							<span class="image fit"><img src="../static/images/ok.png" alt="" /></span>
						</div>
						<div class="col-8 col-7-large col-12-medium">
							<header>
								<h1><strong>Database Content Deleted</strong></h1>
							</header>
							<p>Data in Database : api_calls had been cleaned</p>
                            <a href="/api_calls_dashboard" class="button small scrolly">Go to Dashboard for api_calls DB </a>
						</div>						
					</div>				
				</div>
			</article>
        <!-- Scripts -->
            <script src="../static/assets/js/jquery.min.js"></script>
            <script src="../static/assets/js/jquery.scrolly.min.js"></script>
            <script src="../static/assets/js/init.js"></script>
            <script src="../static/assets/js/browser.min.js"></script>
            <script src="../static/assets/js/breakpoints.min.js"></script>
            <script src="../static/assets/js/util.js"></script>
            <script src="../static/assets/js/main.js"></script>
    </body>
</html>
'''
        loguer(env.level+' route END OF api_calls_db_clear() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]    
        return html_output


#  def_api_calls_db_read***
@app.route('/api_calls_db_read', methods=['GET'])
def api_calls_db_read():
    '''
    Flask Route for the api_calls_db_read Database Read DB content function
    '''
    route="/api_calls_db_read"
    env.level+='-'
    print('\n'+env.level,white('route api_calls_db_read() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route api_calls_db_read() in ***app.py*** : >')
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        keyword=''
        keyword=request.args.get("keyword")
        print("\nkeyword : ",keyword)      
        with open('./sqlite_databases_code/api_calls/db_details.txt') as file:
            db_details_dict=json.loads(file.read())
        print('db_details_dict : \n',yellow(db_details_dict,bold=True))
        database = os.getcwd()+'/z_bases/api_calls.db'
        database=database.replace("\\","/")
        print('database is :',database)
        # sqlite:///:memory: (or, sqlite://)
        # sqlite:///relative/path/to/file.db
        # sqlite:////absolute/path/to/file.db
        db_name = "api_calls.db"
        table_name = db_details_dict["table_name"]
        engine = sqlalchemy.create_engine("sqlite:///z_bases/%s" % db_name, execution_options={"sqlite_raw_colnames": True})
        df = pd.read_sql_table(table_name, engine)
        out_df = df[['index','name','fqdn','relative_url','documentation','method','description','payload','header','body','query_params','custom_variables','authentication_profile','inputs_variables','output_variables']]
        #save result to csv file
        out_df.to_csv(r'./result/api_calls.csv')
        df = DataFrame(out_df)
        #print (df)
        select_options=''
        res = df.values.tolist()
        for item in res:
            if keyword:
                if keyword in item:
                    select_options=select_options+'<option value="'+str(item[0])+'">'+item[1]+'</option>'
            else:
                select_options=select_options+'<option value="'+str(item[0])+'">'+item[1]+'</option>'     
        print('=========================================')
        columns="name,fqdn,relative_url,documentation,method,description,payload,header,body,query_params,custom_variables,authentication_profile,inputs_variables,output_variables"                
        print('DONE')        
        html_output='''<!DOCTYPE HTML>
<!-- description-->
<html>
    <head>
        <title>FLASK APP GENERATOR</title>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no" />
        <link rel="stylesheet" href="../static/assets/css/main.css" />
    <script>
        function popup_window( url, id, width, height )
        {
            //extract the url parameters if any, and pass them to the called html
            var tempvar=document.location.toString(); // fetch the URL string
            var passedparams = tempvar.lastIndexOf("?");
            if(passedparams > -1)
                url += tempvar.substring(passedparams);
            popup = window.open( url, id, 'toolbar=no,scrollbars=yes,location=yes,statusbar=yes,menubar=no,resizable=yes,width=' + width + ',height=' + height + '' );
            popup.focus();
        }
    </script>
    </head>
    <body class="is-preload">
        <!-- Nav -->
            <nav id="nav">
                <ul>
                
                    <li><a href="/">Back to main page</a></li>
                    <li><a href="/api_calls_dashboard">Back to Database Page</a></li>
                    <li><a href="/logout">log Out</a></li>
                    <li><a href="javascript:popup_window('/page_info?page=route_def_api_calls_db_read.py&route=/api_calls_db_read','page_info',700,600);">:</a></li>
        
                </ul>
            </nav>
			<article id="indic_list" class="wrapper style4">
				<div class="container medium">
					<header>
						<h2>Database Content</h2>
                        <p>Select a Row</p>
						<p>Or refine Search by keyword (in any columns)</p>
					</header>
					<div class="row">
						<div class="col-12">
							<form method="get" action="/db_row_details">
                            	<input type="hidden" name="database" value="api_calls">
                            	<input type="hidden" name="table" value="api_calls"> 
                                <input type="hidden" name="columns" value="'''+columns+'''">                                
								<div class="row">
									<div class="col-12">
										<select id="row" name="row">
                                            '''+select_options+'''           
                                        </select>
									</div>      
									<div class="col-12">
										<ul class="actions">
                                            <li><input type="submit" value="Select this row" class="button small scrolly" /></li>
										</ul>
									</div>                                    
								</div>
							</form>
						</div>    
                        <form method="get" action="/api_calls_db_read">
                            <div class="row">                        
                                <div class="col-6 col-12-small">
                                    <h3>Search Keyword :</h3>
                                </div>                                
                                <div class="col-6 col-12-small">
                                    <input type="text"  id="keyword" name="keyword" placeholder="keyword" />
                               </div>  
                                <div class="col-12">      
                                    <ul class="actions">
                                        <input type="submit" value="Search" class="button small scrolly" />
                                    </ul>
                                </div> 
                        </form>
					</div>
					<footer>
						<ul id="copyright">
							
						</ul>
					</footer>
				</div>
			</article>
        <!-- Scripts -->
            <script src="../static/assets/js/jquery.min.js"></script>
            <script src="../static/assets/js/jquery.scrolly.min.js"></script>
            <script src="../static/assets/js/init.js"></script>
            <script src="../static/assets/js/browser.min.js"></script>
            <script src="../static/assets/js/breakpoints.min.js"></script>
            <script src="../static/assets/js/util.js"></script>
            <script src="../static/assets/js/main.js"></script>
    </body>
</html>
'''
        loguer(env.level+' route END OF api_calls_db_read() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]    
        return html_output


#  def_api_calls_db_update_entry***
@app.route('/api_calls_db_update_entry', methods=['GET'])
def api_calls_db_update_entry():
    '''
    Flask Route for the api_calls_db_update_entry Database Update an entry
    '''
    route="/api_calls_db_update_entry"
    env.level+='-'
    print('\n'+env.level,white('route api_calls_db_update_entry() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route api_calls_db_update_entry() in ***app.py*** : >')
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        row=request.args.get("row")
        print("\nrow : ",row)
        name=request.args.get('name')
        print('\nname : ',name)
        fqdn=request.args.get('fqdn')
        print('\nfqdn : ',fqdn)
        relative_url=request.args.get('relative_url')
        print('\nrelative_url : ',relative_url)
        documentation=request.args.get('documentation')
        print('\ndocumentation : ',documentation)
        method=request.args.get('method')
        print('\nmethod : ',method)
        description=request.args.get('description')
        print('\ndescription : ',description)
        payload=request.args.get('payload')
        print('\npayload : ',payload)
        header=request.args.get('header')
        print('\nheader : ',header)
        body=request.args.get('body')
        print('\nbody : ',body)
        query_params=request.args.get('query_params')
        print('\nquery_params : ',query_params)
        custom_variables=request.args.get('custom_variables')
        print('\ncustom_variables : ',custom_variables)
        authentication_profile=request.args.get('authentication_profile')
        print('\nauthentication_profile : ',authentication_profile)
        inputs_variables=request.args.get('inputs_variables')
        print('\ninputs_variables : ',inputs_variables)
        output_variables=request.args.get('output_variables')
        print('\noutput_variables : ',output_variables)
        with open('./sqlite_databases_code/api_calls/db_details.txt') as file:
            db_details_dict=json.loads(file.read())
        print('db_details_dict : \n',yellow(db_details_dict,bold=True))        
        db_name = "api_calls.db"
        table_name = db_details_dict["table_name"]
        where_clause='`index` = '+row
        sql_fields=['index','name','fqdn','relative_url','documentation','method','description','payload','header','body','query_params','custom_variables','authentication_profile','inputs_variables','output_variables']
        sql_data_list=[int(row),name,fqdn,relative_url,documentation,method,description,payload,header,body,query_params,custom_variables,authentication_profile,inputs_variables,output_variables]
        result=sqlite_db_update_entry(db_name,table_name,where_clause,sql_fields,sql_data_list)        
        message1="OK done"
        image="../static/images/ok.png" 
        message2="entry had been updated"
        message3="/api_calls_dashboard"
        message4="api_calls Dashboard"
        PAGE_DESTINATION="operation_done"
        page_name="operation_done.html"
        loguer(env.level+' route END OF example_name() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]
        return render_template('main_index.html',route=route,USERNAME=session['user'],PAGE_DESTINATION=PAGE_DESTINATION,message1=message1,message2=message2,message3=message3,message4=message4,image=image,page_name=page_name)
 


#  def_api_calls_db_delete_entry***
@app.route('/api_calls_db_delete_entry', methods=['GET'])
def api_calls_db_delete_entry():
    '''
    Flask Route for the api_calls_db_delete_entry Database delete entry
    '''
    route="/api_calls_db_delete_entry"
    env.level+='-'
    print('\n'+env.level,white('route api_calls_db_delete_entry() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route api_calls_db_delete_entry() in ***app.py*** : >')
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        row=request.args.get("row")
        print("\nrow : ",row)
        result=sqlite_db_delete_entry('api_calls',row)         
        message1="OK done - Entry DELETED"
        image="../static/images/ok.png" 
        message2="entry had been deleted"
        message3="/api_calls_dashboard"
        message4="api_calls Dashboard"
        PAGE_DESTINATION="operation_done"
        page_name="operation_done.html"
        loguer(env.level+' route END OF example_name() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]
        return render_template('main_index.html',route=route,USERNAME=session['user'],PAGE_DESTINATION=PAGE_DESTINATION,message1=message1,message2=message2,message3=message3,message4=message4,image=image,page_name=page_name)
 


#  def_api_calls_db_add_entry***
@app.route('/api_calls_db_add_entry', methods=['GET'])
def api_calls_db_add_entry():
    '''
    Flask Route for the api_calls_db_add_entry Database Update an entry
    '''
    route="/api_calls_db_add_entry"
    env.level+='-'
    print('\n'+env.level,white('route api_calls_db_add_entry() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route api_calls_db_add_entry() in ***app.py*** : >')
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        db_name = "api_calls.db"
        column_list=['name','fqdn','relative_url','documentation','method','description','payload','header','body','query_params','custom_variables','authentication_profile','inputs_variables','output_variables']
        print('\ncolumn_list :',cyan(column_list,bold=True))
        index=sqlite_db_get_last_index('api_calls')
        index+=1        
        print('index : ',index)
        PAGE_DESTINATION="z_sqlite_db_add_entry"
        page_name="z_sqlite_db_add_entry.html"
        db_name=db_name.split('.')[0]
        loguer(env.level+' route END OF example_name() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]
        return render_template('main_index.html',route=route,USERNAME=session['user'],PAGE_DESTINATION=PAGE_DESTINATION,page_name=page_name,column_list=column_list,index=index,db_name=db_name)
 


#  def_api_calls_db_add_entry_ok***
@app.route('/api_calls_db_add_entry_ok', methods=['GET'])
def api_calls_db_add_entry_ok():
    '''
    Flask Route for the api_calls_db_add_entry Database Update an entry
    '''
    route="/api_calls_db_add_entry_ok"
    env.level+='-'
    print('\n'+env.level,white('route api_calls_db_add_entry_ok() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route api_calls_db_add_entry_ok() in ***app.py*** : >')
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        name=request.args.get("name")
        print("\nname: ",name)
        fqdn=request.args.get("fqdn")
        print("\nfqdn: ",fqdn)
        relative_url=request.args.get("relative_url")
        print("\nrelative_url: ",relative_url)
        documentation=request.args.get("documentation")
        print("\ndocumentation: ",documentation)
        method=request.args.get("method")
        print("\nmethod: ",method)
        description=request.args.get("description")
        print("\ndescription: ",description)
        payload=request.args.get("payload")
        print("\npayload: ",payload)
        header=request.args.get("header")
        print("\nheader: ",header)
        body=request.args.get("body")
        print("\nbody: ",body)
        query_params=request.args.get("query_params")
        print("\nquery_params: ",query_params)
        custom_variables=request.args.get("custom_variables")
        print("\ncustom_variables: ",custom_variables)
        authentication_profile=request.args.get("authentication_profile")
        print("\nauthentication_profile: ",authentication_profile)
        inputs_variables=request.args.get("inputs_variables")
        print("\ninputs_variables: ",inputs_variables)
        output_variables=request.args.get("output_variables")
        print("\noutput_variables: ",output_variables)

        db_name=request.args.get("db_name")
        print('db_name :',db_name)     
        with open('./sqlite_databases_code/'+db_name+'/db_details.txt') as file:
            db_details_dict=json.loads(file.read())
        print('db_details_dict : \n',yellow(db_details_dict,bold=True)) 
        database = os.getcwd()+'/z_bases/'+db_name+'.db'
        database=database.replace("\\","/")
        table=db_details_dict['table_name']
        print('database is :',database) 
        print('table is :',table)          
        # Get last index value in SQLITE DB
        new_index=sqlite_db_get_last_index(db_name)+1        
        print('new_index is :',new_index)  
        sqlite_data=(new_index,name,fqdn,relative_url,documentation,method,description,payload,header,body,query_params,custom_variables,authentication_profile,inputs_variables,output_variables)
        sql_add=f"INSERT OR IGNORE into {table} (`index`,name,fqdn,relative_url,documentation,method,description,payload,header,body,query_params,custom_variables,authentication_profile,inputs_variables,output_variables) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
        print('sqlite_data :',sqlite_data)     
        print('sql_add :',sql_add)          
        con = sqlite3.connect(database)       
        try:
            cur = con.cursor()
            cur.execute(sql_add,sqlite_data)
            con.commit()
            print(green('OK DONE ENTRY DELETED',bold=True))
            image="../static/images/ok.png" 
            message1="Entry Added"
            message2="Entry was added to DB"
            message3=f"/{db_name}_dashboard"
            message4=f"{db_name}_dasbhoard"        
            PAGE_DESTINATION="operation_done"
            page_name="operation_done.html"            
            loguer(env.level+' route END OF machin_db_add_entry_ok() in ***app.py*** : >')    
            env.level=env.level[:-1]        
            return render_template('main_index.html',route=route,USERNAME=session['user'],PAGE_DESTINATION=PAGE_DESTINATION,message1=message1,message2=message2,message3=message3,message4=message4,image=image,page_name=page_name) 
        except:
            print(red('Error',bold=True))
            image="../static/images/nok.png" 
            message1="Error"
            message2="An error occured"
            message3=f"/{db_name}_dashboard"
            message4=f"{db_name}_dasbhoard"        
            PAGE_DESTINATION="operation_done"
            page_name="operation_done.html"            
            loguer(env.level+' route END OF machin_db_add_entry_ok() in ***app.py*** : >')    
            env.level=env.level[:-1]        
            return render_template('main_index.html',route=route,USERNAME=session['user'],PAGE_DESTINATION=PAGE_DESTINATION,message1=message1,message2=message2,message3=message3,message4=message4,image=image,page_name=page_name)



#  def_api_calls_db_ingest_csv***
@app.route('/api_calls_db_ingest_csv', methods=['GET'])
def api_calls_db_ingest_csv():
    '''
    Flask Route for the api_calls_db_ingest_csv Database Update an entry
    '''
    route="/api_calls_db_ingest_csv"
    env.level+='-'
    print('\n'+env.level,white('route api_calls_db_ingest_csv() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route api_calls_db_ingest_csv() in ***app.py*** : >')
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        db_name="api_calls"
        message1="Message 1 :"
        image="../static/images/toolbox.png"
        message2="Message 2 :"
        message3="/Message 3"
        message4="Message 4 in button"
        PAGE_DESTINATION="z_sqlite_ingest_csv"
        page_name="z_sqlite_ingest_csv.html"
        loguer(env.level+' route END OF api_calls_db_ingest_csv() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]
        return render_template('main_index.html',route=route,USERNAME=session['user'],PAGE_DESTINATION=PAGE_DESTINATION,message1=message1,message2=message2,message3=message3,message4=message4,image=image,page_name=page_name,db_name=db_name) 


#  def_api_calls_db_duplicate_entry***
@app.route('/api_calls_db_duplicate_entry', methods=['GET'])
def api_calls_db_duplicate_entry():
    '''
    Flask Route for the api_calls_db_duplicate_entry Database delete entry
    '''
    route="/api_calls_db_duplicate_entry"
    env.level+='-'
    print('\n'+env.level,white('route api_calls_db_duplicate_entry() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route api_calls_db_duplicate_entry() in ***app.py*** : >')
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        row=request.args.get("row")
        print("\nrow : ",row)
        result=sqlite_db_duplicate_entry('api_calls',row)         
        message1="OK done - Entry DUPLICATED"
        image="../static/images/ok.png" 
        message2="entry had been duplicated"
        message3="/api_calls_dashboard"
        message4="api_calls Dashboard"
        PAGE_DESTINATION="operation_done"
        page_name="operation_done.html"
        loguer(env.level+' route END OF example_name() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]
        return render_template('main_index.html',route=route,USERNAME=session['user'],PAGE_DESTINATION=PAGE_DESTINATION,message1=message1,message2=message2,message3=message3,message4=message4,image=image,page_name=page_name)
 


#  def_no_api_documentation***
@app.route('/no_api_documentation', methods=['GET'])
def no_api_documentation():
    '''
    Created : 2025-10-29T15:29:59.000Z

    description : display the NO API documentation available page
    '''
    route="/no_api_documentation"
    env.level+='-'
    print('\n'+env.level,white('route no_api_documentation() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route no_api_documentation() in ***app.py*** : >')
    global client_id
    global client_password
    global host
    global host_for_token
    global profil_name
    if not session.get('logged_in'):
        return render_template('login.html')
    else:       
        message1="NO API Documentation !"
        image="../static/images/nok.png" 
        message2="API Documentation is not public"
        message3="/"
        message4="Home"
        PAGE_DESTINATION="z_no_api_documentation for this product"
        page_name="z_no_api_documentation.html"
        loguer(env.level+' route END OF no_api_documentation() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]
        return render_template('main_index.html',route=route,USERNAME=session['user'],PAGE_DESTINATION=PAGE_DESTINATION,message1=message1,message2=message2,message3=message3,message4=message4,image=image,page_name=page_name)
        


#  def_variables_dashboard***
@app.route('/variables_dashboard', methods=['GET'])
def variables_dashboard():
    '''
    Flask Route for the variables_dashboard Database dashoard
    '''
    route="/variables_dashboard"
    env.level+='-'
    print('\n'+env.level,white('route variables_dashboard() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route variables_dashboard() in ***app.py*** : >')
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        html_output='''<!DOCTYPE HTML>
<!-- description-->
<html>
    <head>
        <title>FLASK APP GENERATOR</title>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no" />
        <link rel="stylesheet" href="../static/assets/css/main.css" />
    <script>
        function popup_window( url, id, width, height )
        {
            //extract the url parameters if any, and pass them to the called html
            var tempvar=document.location.toString(); // fetch the URL string
            var passedparams = tempvar.lastIndexOf("?");
            if(passedparams > -1)
                url += tempvar.substring(passedparams);
            popup = window.open( url, id, 'toolbar=no,scrollbars=yes,location=yes,statusbar=yes,menubar=no,resizable=yes,width=' + width + ',height=' + height + '' );
            popup.focus();
        }
    </script>
    </head>
    <body class="is-preload">
        <!-- Nav -->
            <nav id="nav">
                <ul>
                
                    <li><a href="/">Back to main page</a></li>
                    <li><a href="/logout">log Out</a></li>
                    <li><a href="javascript:popup_window('/page_info?page=route_def_variables_dashboard.py&route=/variables_dashboard','page_info',700,600);">:</a></li>
        
                </ul>
            </nav>
        <!-- Portfolio -->
            <article id="portfolio" class="wrapper style3">
                <div class="container">
                    <header>
                        <h2>variables Database</h2>
                    </header>
                    <div class="row">
                        <div class="col-4 col-6-medium col-12-small">
                            <article class="box style2">
                                <a href="/variables_create_db" class="image featured"><img src="../static/images/database0.png" alt="" /></a>
                                <h3><a href="/variables_create_db">Create Database</a></h3>
                                <p>Create the variables Database</p>
                            </article>
                        </div>
                        <div class="col-4 col-6-medium col-12-small">
                            <article class="box style2">
                                <a href="/variables_ingest_demo_data" class="image featured"><img src="../static/images/database0.png" alt="" /></a>
                                <h3><a href="/variables_ingest_demo_data">Ingest Demo Data</a></h3>
                                <p>Ingest Demo Data into DB</p>
                            </article>
                        </div>
                        <div class="col-4 col-6-medium col-12-small">
                            <article class="box style2">
                                <a href="/variables_db_read" class="image featured"><img src="../static/images/database0.png" alt="" /></a>
                                <h3><a href="/variables_db_read">Read Database content</a></h3>
                                <p>Read DB an Create a CSV result</p>
                            </article>
                        </div>
                        <div class="col-4 col-6-medium col-12-small">
                            <article class="box style2">
                                <a href="/variables_db_clear" class="image featured"><img src="../static/images/database0.png" alt="" /></a>
                                <h3><a href="/variables_db_clear">Clear Database</a></h3>
                                <p>Delete Database content</p>
                            </article>
                        </div>
                        <div class="col-4 col-6-medium col-12-small">
                            <article class="box style2">
                                <a href="/variables_db_ingest_csv" class="image featured"><img src="../static/images/database0.png" alt="" /></a>
                                <h3><a href="/variables_db_ingest_csv">Ingest a CSV file</a></h3>
                                <p>Ingest a CSV file</p>
                            </article>
                        </div>
                        <div class="col-4 col-6-medium col-12-small">
                            <article class="box style2">
                                <a href="/variables_db_add_entry" class="image featured"><img src="../static/images/database0.png" alt="" /></a>
                                <h3><a href="/variables_db_add_entry">Add Entry</a></h3>
                                <p>Add an Entry to Database</p>
                            </article>
                        </div>
            
                    </div>
                </div>
            </article>
        <!-- Scripts -->
            <script src="../static/assets/js/jquery.min.js"></script>
            <script src="../static/assets/js/jquery.scrolly.min.js"></script>
            <script src="../static/assets/js/init.js"></script>
            <script src="../static/assets/js/browser.min.js"></script>
            <script src="../static/assets/js/breakpoints.min.js"></script>
            <script src="../static/assets/js/util.js"></script>
            <script src="../static/assets/js/main.js"></script>
    </body>
</html>
'''
        loguer(env.level+' route END OF variables_dashboard() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]
        return html_output
        

#  def_variables_create_db***
@app.route('/variables_create_db', methods=['GET'])
def variables_create_db():
    '''
    Flask Route for the variables_create_db Database Create DB action
    '''
    route="/variables_create_db"
    env.level+='-'
    print('\n'+env.level,white('route variables_create_db() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route variables_create_db() in ***app.py*** : >')
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        with open('./sqlite_databases_code/variables/db_details.txt') as file:
            db_details_dict=json.loads(file.read())
        print('db_details_dict : \n',yellow(db_details_dict,bold=True))
        file=open('./sqlite_databases_code/variables/init/variables.csv','w')
        ligne_out=''
        len_columns=len(db_details_dict['columns'])-1
        i=0        
        for col in db_details_dict['columns']:
            if i<len_columns:
                ligne_out=ligne_out+col+','
            else:
                ligne_out=ligne_out+col
            i+=1
        file.write(ligne_out+'\n')
        for i in range (0,10):
            ligne_out='name'+str(i)+','+'environment_name'+str(i)+','+'value'+str(i)+','+'description'+str(i)+','+'comment'+str(i)+','+'used_by'+str(i)           
            file.write(ligne_out+'\n')
        file.close()  
        create_db_and_table(db_details_dict['db_name'],db_details_dict['table_name'])
        html_output='''<!DOCTYPE HTML>
<!-- description-->
<html>
    <head>
        <title>FLASK APP GENERATOR</title>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no" />
        <link rel="stylesheet" href="../static/assets/css/main.css" />
    <script>
        function popup_window( url, id, width, height )
        {
            //extract the url parameters if any, and pass them to the called html
            var tempvar=document.location.toString(); // fetch the URL string
            var passedparams = tempvar.lastIndexOf("?");
            if(passedparams > -1)
                url += tempvar.substring(passedparams);
            popup = window.open( url, id, 'toolbar=no,scrollbars=yes,location=yes,statusbar=yes,menubar=no,resizable=yes,width=' + width + ',height=' + height + '' );
            popup.focus();
        }
    </script>
    </head>
    <body class="is-preload">
        <!-- Nav -->
            <nav id="nav">
                <ul>
                
                    <li><a href="/">Back to main page</a></li>
                    <li><a href="/logout">log Out</a></li>
                    <li><a href="javascript:popup_window('/page_info?page=route_def_bases.py&route=/variables_create_db','page_info',700,600);">:</a></li>
        
                </ul>
            </nav>
        <!-- Portfolio -->
			<article id="top" class="wrapper style1">
				<div class="container">
					<div class="row">
						<div class="col-4 col-5-large col-12-medium">
							<span class="image fit"><img src="../static/images/ok.png" alt="" /></span>
						</div>
						<div class="col-8 col-7-large col-12-medium">
							<header>
								<h1><strong> Database :variables, was created</strong></h1>
							</header>
							<p>The SQLITE had been created in ./z_bases</p>
                            <a href="/variables_dashboard" class="button small scrolly">Go to Dashboard for variables DB </a>
						</div>						
					</div>				
				</div>
			</article>
        <!-- Scripts -->
            <script src="../static/assets/js/jquery.min.js"></script>
            <script src="../static/assets/js/jquery.scrolly.min.js"></script>
            <script src="../static/assets/js/init.js"></script>
            <script src="../static/assets/js/browser.min.js"></script>
            <script src="../static/assets/js/breakpoints.min.js"></script>
            <script src="../static/assets/js/util.js"></script>
            <script src="../static/assets/js/main.js"></script>
    </body>
</html>
'''
        loguer(env.level+' route END OF variables_create_db() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]    
        return html_output


#  def_variables_ingest_demo_data***
@app.route('/variables_ingest_demo_data', methods=['GET'])
def variables_ingest_demo_data():
    '''
    Flask Route for the variables_ingest_demo_data Database Ingest demo data
    '''
    route="/variables_ingest_demo_data"
    env.level+='-'
    print('\n'+env.level,white('route variables_ingest_demo_data() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route variables_ingest_demo_data() in ***app.py*** : >')
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        with open('./sqlite_databases_code/variables/db_details.txt') as file:
            db_details_dict=json.loads(file.read())
        print('db_details_dict : \n',yellow(db_details_dict,bold=True))
        database = os.getcwd()+'/z_bases/variables.db'
        database=database.replace("\\","/")
        print('database is :',database)
        lines=[]    
        file='./sqlite_databases_code/variables/init/variables.csv'
        with open (file) as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            lines = list(reader)
            indexA=0
            print('variables table =>\n')
            conn=create_connection(database) # open connection to database            
            for row in lines:
                if conn:
                    # connection to database is OK
                    c=conn.cursor()
                    # let's go to every lines one by one and let's extract url, targeted brand
                    sqlite_data=[indexA]
                    sqlite_data=(indexA,row[0] ,row[1] ,row[2] ,row[3] ,row[4] ,row[5])
                    sql_add="INSERT OR IGNORE into variables (`index`,name,environment_name,value,description,comment,used_by) VALUES (?,?,?,?,?,?,?)"
                    print('\nsql_add :',cyan(sql_add,bold=True))
                c.execute(sql_add, sqlite_data)
                print(green("==> OK Done : demo data ingested",bold=True))
                indexA+=1
                conn.commit()        

        html_output='''<!DOCTYPE HTML>
<!-- description-->
<html>
    <head>
        <title>FLASK APP GENERATOR</title>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no" />
        <link rel="stylesheet" href="../static/assets/css/main.css" />
    <script>
        function popup_window( url, id, width, height )
        {
            //extract the url parameters if any, and pass them to the called html
            var tempvar=document.location.toString(); // fetch the URL string
            var passedparams = tempvar.lastIndexOf("?");
            if(passedparams > -1)
                url += tempvar.substring(passedparams);
            popup = window.open( url, id, 'toolbar=no,scrollbars=yes,location=yes,statusbar=yes,menubar=no,resizable=yes,width=' + width + ',height=' + height + '' );
            popup.focus();
        }
    </script>
    </head>
    <body class="is-preload">
        <!-- Nav -->
            <nav id="nav">
                <ul>
                
                    <li><a href="/">Back to main page</a></li>
                    <li><a href="/logout">log Out</a></li>
                    <li><a href="javascript:popup_window('/page_info?page=route_def_variables.py&route=/variables_ingest_demo_data_ingest_demo_data','page_info',700,600);">:</a></li>
        
                </ul>
            </nav>
        <!-- Portfolio -->
			<article id="top" class="wrapper style1">
				<div class="container">
					<div class="row">
						<div class="col-4 col-5-large col-12-medium">
							<span class="image fit"><img src="../static/images/ok.png" alt="" /></span>
						</div>
						<div class="col-8 col-7-large col-12-medium">
							<header>
								<h1><strong>Demo Data ingested</strong></h1>
							</header>
							<p>Demo Data ingested into Database :variables</p>
                            <a href="/variables_dashboard" class="button small scrolly">Go to Dashboard for variables DB </a>
						</div>						
					</div>				
				</div>
			</article>
        <!-- Scripts -->
            <script src="../static/assets/js/jquery.min.js"></script>
            <script src="../static/assets/js/jquery.scrolly.min.js"></script>
            <script src="../static/assets/js/init.js"></script>
            <script src="../static/assets/js/browser.min.js"></script>
            <script src="../static/assets/js/breakpoints.min.js"></script>
            <script src="../static/assets/js/util.js"></script>
            <script src="../static/assets/js/main.js"></script>
    </body>
</html>
'''
        loguer(env.level+' route END OF variables_ingest_demo_data() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]    
        return html_output


#  def_variables_db_clear***
@app.route('/variables_db_clear', methods=['GET'])
def variables_db_clear():
    '''
    Flask Route for the variables_db_clear Database Clearing / reset function
    '''
    route="/variables_db_clear"
    env.level+='-'
    print('\n'+env.level,white('route variables_db_clear() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route variables_db_clear() in ***app.py*** : >')
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        with open('./sqlite_databases_code/variables/db_details.txt') as file:
            db_details_dict=json.loads(file.read())
        print('db_details_dict : \n',yellow(db_details_dict,bold=True))
        database = os.getcwd()+'/z_bases/variables.db'
        database=database.replace("\\","/")
        print('database is :',database)
        print('table is :', db_details_dict["table_name"])
        conn=create_connection(database) # open connection to database
        if conn:
            # connection to database is OK
            c=conn.cursor()
            print(f'- Deleting table : {db_details_dict["table_name"]} =>')
            sql_request="drop table "+db_details_dict["table_name"]
            c.execute(sql_request)
            conn.commit()
            print('-- OK DONE : Deleted table : '+db_details_dict["table_name"])
            create_db_and_table(db_details_dict["db_name"],db_details_dict["table_name"])
            print(f'-- OK table {db_details_dict["table_name"]} reseted')     

        html_output='''<!DOCTYPE HTML>
<!-- description-->
<html>
    <head>
        <title>FLASK APP GENERATOR</title>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no" />
        <link rel="stylesheet" href="../static/assets/css/main.css" />
    <script>
        function popup_window( url, id, width, height )
        {
            //extract the url parameters if any, and pass them to the called html
            var tempvar=document.location.toString(); // fetch the URL string
            var passedparams = tempvar.lastIndexOf("?");
            if(passedparams > -1)
                url += tempvar.substring(passedparams);
            popup = window.open( url, id, 'toolbar=no,scrollbars=yes,location=yes,statusbar=yes,menubar=no,resizable=yes,width=' + width + ',height=' + height + '' );
            popup.focus();
        }
    </script>
    </head>
    <body class="is-preload">
        <!-- Nav -->
            <nav id="nav">
                <ul>
                
                    <li><a href="/">Back to main page</a></li>
                    <li><a href="/logout">log Out</a></li>
                    <li><a href="javascript:popup_window('/page_info?page=route_def_variables_db_clear.py&route=/variables_db_clear','page_info',700,600);">:</a></li>
        
                </ul>
            </nav>
        <!-- Portfolio -->
			<article id="top" class="wrapper style1">
				<div class="container">
					<div class="row">
						<div class="col-4 col-5-large col-12-medium">
							<span class="image fit"><img src="../static/images/ok.png" alt="" /></span>
						</div>
						<div class="col-8 col-7-large col-12-medium">
							<header>
								<h1><strong>Database Content Deleted</strong></h1>
							</header>
							<p>Data in Database : variables had been cleaned</p>
                            <a href="/variables_dashboard" class="button small scrolly">Go to Dashboard for variables DB </a>
						</div>						
					</div>				
				</div>
			</article>
        <!-- Scripts -->
            <script src="../static/assets/js/jquery.min.js"></script>
            <script src="../static/assets/js/jquery.scrolly.min.js"></script>
            <script src="../static/assets/js/init.js"></script>
            <script src="../static/assets/js/browser.min.js"></script>
            <script src="../static/assets/js/breakpoints.min.js"></script>
            <script src="../static/assets/js/util.js"></script>
            <script src="../static/assets/js/main.js"></script>
    </body>
</html>
'''
        loguer(env.level+' route END OF variables_db_clear() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]    
        return html_output


#  def_variables_db_read***
@app.route('/variables_db_read', methods=['GET'])
def variables_db_read():
    '''
    Flask Route for the variables_db_read Database Read DB content function
    '''
    route="/variables_db_read"
    env.level+='-'
    print('\n'+env.level,white('route variables_db_read() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route variables_db_read() in ***app.py*** : >')
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        keyword=request.args.get("keyword")
        if keyword ==None:
            keyword=''
        keyword=keyword.lower()
        print("\nkeyword : ",keyword)      
        with open('./sqlite_databases_code/variables/db_details.txt') as file:
            db_details_dict=json.loads(file.read())
        print('db_details_dict : \n',yellow(db_details_dict,bold=True))
        database = os.getcwd()+'/z_bases/variables.db'
        database=database.replace("\\","/")
        print('database is :',database)
        # sqlite:///:memory: (or, sqlite://)
        # sqlite:///relative/path/to/file.db
        # sqlite:////absolute/path/to/file.db
        db_name = "variables.db"
        table_name = db_details_dict["table_name"]
        engine = sqlalchemy.create_engine("sqlite:///z_bases/%s" % db_name, execution_options={"sqlite_raw_colnames": True})
        df = pd.read_sql_table(table_name, engine)
        out_df = df[['index','name','environment_name','value','description','comment','used_by']]
        #save result to csv file
        out_df.to_csv(r'./result/variables.csv')
        df = DataFrame(out_df)
        #print (df)
        select_options=''
        res = df.values.tolist()
        element_index=1
        sorted_list=sorted(res, key=lambda x: x[element_index])                    
        for item in sorted_list:
            found=0
            if keyword!='':
                if keyword in item[1].lower():
                    found=1
                if keyword in item[3].lower():
                    found=1      
                if keyword in item[4].lower():
                    found=1     
                if keyword in item[5].lower():
                    found=1                
                if found:
                    select_options=select_options+'<option value="'+str(item[0])+'">'+item[1]+'</option>'
            else:
                select_options=select_options+'<option value="'+str(item[0])+'">'+item[1]+'</option>'     
        print('=========================================')
        columns="name,environment_name,value,description,comment,used_by"                
        print('DONE')        
        html_output='''<!DOCTYPE HTML>
<!-- description-->
<html>
    <head>
        <title>FLASK APP GENERATOR</title>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no" />
        <link rel="stylesheet" href="../static/assets/css/main.css" />
    <script>
        function popup_window( url, id, width, height )
        {
            //extract the url parameters if any, and pass them to the called html
            var tempvar=document.location.toString(); // fetch the URL string
            var passedparams = tempvar.lastIndexOf("?");
            if(passedparams > -1)
                url += tempvar.substring(passedparams);
            popup = window.open( url, id, 'toolbar=no,scrollbars=yes,location=yes,statusbar=yes,menubar=no,resizable=yes,width=' + width + ',height=' + height + '' );
            popup.focus();
        }
    </script>
    </head>
    <body class="is-preload">
        <!-- Nav -->
            <nav id="nav">
                <ul>
                
                    <li><a href="/">Back to main page</a></li>
                    <li><a href="/variables_dashboard">Back to Database Page</a></li>
                    <li><a href="/logout">log Out</a></li>
                    <li><a href="javascript:popup_window('/page_info?page=route_def_variables_db_read.py&route=/variables_db_read','page_info',700,600);">:</a></li>
        
                </ul>
            </nav>
			<article id="indic_list" class="wrapper style4">
				<div class="container medium">
					<header>
						<h2>Database Content</h2>
                        <p>Select a Row</p>
						<p>Or refine Search by keyword (in any columns)</p>
					</header>
					<div class="row">
						<div class="col-12">
							<form method="get" action="/db_row_details">
                            	<input type="hidden" name="database" value="variables">
                            	<input type="hidden" name="table" value="variables"> 
                                <input type="hidden" name="columns" value="'''+columns+'''">                                
								<div class="row">
									<div class="col-12">
										<select id="row" name="row">
                                            '''+select_options+'''           
                                        </select>
									</div>      
									<div class="col-12">
										<ul class="actions">
                                            <li><input type="submit" value="Select this row" class="button small scrolly" /></li>
										</ul>
									</div>                                    
								</div>
							</form>
						</div>    
                        <form method="get" action="/variables_db_read">
                            <div class="row">                        
                                <div class="col-6 col-12-small">
                                    <h3>Search Keyword :</h3>
                                </div>                                
                                <div class="col-6 col-12-small">
                                    <input type="text"  id="keyword" name="keyword" placeholder="keyword" />
                               </div>  
                                <div class="col-12">      
                                    <ul class="actions">
                                        <input type="submit" value="Search" class="button small scrolly" />
                                    </ul>
                                </div> 
                        </form>
					</div>
					<footer>
						<ul id="copyright">
							
						</ul>
					</footer>
				</div>
			</article>
        <!-- Scripts -->
            <script src="../static/assets/js/jquery.min.js"></script>
            <script src="../static/assets/js/jquery.scrolly.min.js"></script>
            <script src="../static/assets/js/init.js"></script>
            <script src="../static/assets/js/browser.min.js"></script>
            <script src="../static/assets/js/breakpoints.min.js"></script>
            <script src="../static/assets/js/util.js"></script>
            <script src="../static/assets/js/main.js"></script>
    </body>
</html>
'''
        loguer(env.level+' route END OF variables_db_read() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]    
        return html_output


#  def_variables_db_update_entry***
@app.route('/variables_db_update_entry', methods=['GET'])
def variables_db_update_entry():
    '''
    Flask Route for the variables_db_update_entry Database Update an entry
    '''
    route="/variables_db_update_entry"
    env.level+='-'
    print('\n'+env.level,white('route variables_db_update_entry() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route variables_db_update_entry() in ***app.py*** : >')
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        row=request.args.get("row")
        print("\nrow : ",row)
        name=request.args.get('name')
        print('\nname : ',name)
        environment_name=request.args.get('environment_name')
        print('\nenvironment_name : ',environment_name)
        value=request.args.get('value')
        print('\nvalue : ',value)
        description=request.args.get('description')
        print('\ndescription : ',description)
        comment=request.args.get('comment')
        print('\ncomment : ',comment)
        used_by=request.args.get('used_by')
        print('\nused_by : ',used_by)
        with open('./sqlite_databases_code/variables/db_details.txt') as file:
            db_details_dict=json.loads(file.read())
        print('db_details_dict : \n',yellow(db_details_dict,bold=True))        
        db_name = "variables.db"
        table_name = db_details_dict["table_name"]
        where_clause='`index` = '+row
        sql_fields=['index','name','environment_name','value','description','comment','used_by']
        sql_data_list=[int(row),name,environment_name,value,description,comment,used_by]
        result=sqlite_db_update_entry(db_name,table_name,where_clause,sql_fields,sql_data_list)        
        message1="OK done"
        image="../static/images/ok.png" 
        message2="entry had been updated"
        message3="/variables_dashboard"
        message4="variables Dashboard"
        PAGE_DESTINATION="operation_done"
        page_name="operation_done.html"
        loguer(env.level+' route END OF example_name() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]
        return render_template('main_index.html',route=route,USERNAME=session['user'],PAGE_DESTINATION=PAGE_DESTINATION,message1=message1,message2=message2,message3=message3,message4=message4,image=image,page_name=page_name)
 


#  def_variables_db_delete_entry***
@app.route('/variables_db_delete_entry', methods=['GET'])
def variables_db_delete_entry():
    '''
    Flask Route for the variables_db_delete_entry Database delete entry
    '''
    route="/variables_db_delete_entry"
    env.level+='-'
    print('\n'+env.level,white('route variables_db_delete_entry() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route variables_db_delete_entry() in ***app.py*** : >')
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        row=request.args.get("row")
        print("\nrow : ",row)
        result=sqlite_db_delete_entry('variables',row)         
        message1="OK done - Entry DELETED"
        image="../static/images/ok.png" 
        message2="entry had been deleted"
        message3="/variables_dashboard"
        message4="variables Dashboard"
        PAGE_DESTINATION="operation_done"
        page_name="operation_done.html"
        loguer(env.level+' route END OF example_name() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]
        return render_template('main_index.html',route=route,USERNAME=session['user'],PAGE_DESTINATION=PAGE_DESTINATION,message1=message1,message2=message2,message3=message3,message4=message4,image=image,page_name=page_name)
 


#  def_variables_db_add_entry***
@app.route('/variables_db_add_entry', methods=['GET'])
def variables_db_add_entry():
    '''
    Flask Route for the variables_db_add_entry Database Update an entry
    '''
    route="/variables_db_add_entry"
    env.level+='-'
    print('\n'+env.level,white('route variables_db_add_entry() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route variables_db_add_entry() in ***app.py*** : >')
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        db_name = "variables.db"
        column_list=['name','environment_name','value','description','comment','used_by']
        print('\ncolumn_list :',cyan(column_list,bold=True))
        index=sqlite_db_get_last_index('variables')
        index+=1        
        print('index : ',index)
        PAGE_DESTINATION="z_sqlite_db_add_entry"
        page_name="z_sqlite_db_add_entry.html"
        db_name=db_name.split('.')[0]
        loguer(env.level+' route END OF example_name() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]
        return render_template('main_index.html',route=route,USERNAME=session['user'],PAGE_DESTINATION=PAGE_DESTINATION,page_name=page_name,column_list=column_list,index=index,db_name=db_name)
 


#  def_variables_db_add_entry_ok***
@app.route('/variables_db_add_entry_ok', methods=['GET'])
def variables_db_add_entry_ok():
    '''
    Flask Route for the variables_db_add_entry Database Update an entry
    '''
    route="/variables_db_add_entry_ok"
    env.level+='-'
    print('\n'+env.level,white('route variables_db_add_entry_ok() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route variables_db_add_entry_ok() in ***app.py*** : >')
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        name=request.args.get("name")
        print("\nname: ",name)
        environment_name=request.args.get("environment_name")
        print("\nenvironment_name: ",environment_name)
        value=request.args.get("value")
        print("\nvalue: ",value)
        description=request.args.get("description")
        print("\ndescription: ",description)
        comment=request.args.get("comment")
        print("\ncomment: ",comment)
        used_by=request.args.get("used_by")
        print("\nused_by: ",used_by)

        db_name=request.args.get("db_name")
        print('db_name :',db_name)     
        with open('./sqlite_databases_code/'+db_name+'/db_details.txt') as file:
            db_details_dict=json.loads(file.read())
        print('db_details_dict : \n',yellow(db_details_dict,bold=True)) 
        database = os.getcwd()+'/z_bases/'+db_name+'.db'
        database=database.replace("\\","/")
        table=db_details_dict['table_name']
        print('database is :',database) 
        print('table is :',table)          
        # Get last index value in SQLITE DB
        new_index=sqlite_db_get_last_index(db_name)+1        
        print('new_index is :',new_index)  
        sqlite_data=(new_index,name,environment_name,value,description,comment,used_by)
        sql_add=f"INSERT OR IGNORE into {table} (`index`,name,environment_name,value,description,comment,used_by) VALUES (?,?,?,?,?,?,?)"
        print('sqlite_data :',sqlite_data)     
        print('sql_add :',sql_add)          
        con = sqlite3.connect(database)       
        try:
            cur = con.cursor()
            cur.execute(sql_add,sqlite_data)
            con.commit()
            print(green('OK DONE ENTRY DELETED',bold=True))
            image="../static/images/ok.png" 
            message1="Entry Added"
            message2="Entry was added to DB"
            message3=f"/{db_name}_dashboard"
            message4=f"{db_name}_dasbhoard"        
            PAGE_DESTINATION="operation_done"
            page_name="operation_done.html"            
            loguer(env.level+' route END OF machin_db_add_entry_ok() in ***app.py*** : >')    
            env.level=env.level[:-1]        
            return render_template('main_index.html',route=route,USERNAME=session['user'],PAGE_DESTINATION=PAGE_DESTINATION,message1=message1,message2=message2,message3=message3,message4=message4,image=image,page_name=page_name) 
        except:
            print(red('Error',bold=True))
            image="../static/images/nok.png" 
            message1="Error"
            message2="An error occured"
            message3=f"/{db_name}_dashboard"
            message4=f"{db_name}_dasbhoard"        
            PAGE_DESTINATION="operation_done"
            page_name="operation_done.html"            
            loguer(env.level+' route END OF machin_db_add_entry_ok() in ***app.py*** : >')    
            env.level=env.level[:-1]        
            return render_template('main_index.html',route=route,USERNAME=session['user'],PAGE_DESTINATION=PAGE_DESTINATION,message1=message1,message2=message2,message3=message3,message4=message4,image=image,page_name=page_name)



#  def_variables_db_ingest_csv***
@app.route('/variables_db_ingest_csv', methods=['GET'])
def variables_db_ingest_csv():
    '''
    Flask Route for the variables_db_ingest_csv Database Update an entry
    '''
    route="/variables_db_ingest_csv"
    env.level+='-'
    print('\n'+env.level,white('route variables_db_ingest_csv() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route variables_db_ingest_csv() in ***app.py*** : >')
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        db_name="variables"
        message1="Message 1 :"
        image="../static/images/toolbox.png"
        message2="Message 2 :"
        message3="/Message 3"
        message4="Message 4 in button"
        PAGE_DESTINATION="z_sqlite_ingest_csv"
        page_name="z_sqlite_ingest_csv.html"
        loguer(env.level+' route END OF variables_db_ingest_csv() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]
        return render_template('main_index.html',route=route,USERNAME=session['user'],PAGE_DESTINATION=PAGE_DESTINATION,message1=message1,message2=message2,message3=message3,message4=message4,image=image,page_name=page_name,db_name=db_name) 


#  def_variables_db_duplicate_entry***
@app.route('/variables_db_duplicate_entry', methods=['GET'])
def variables_db_duplicate_entry():
    '''
    Flask Route for the variables_db_duplicate_entry Database delete entry
    '''
    route="/variables_db_duplicate_entry"
    env.level+='-'
    print('\n'+env.level,white('route variables_db_duplicate_entry() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route variables_db_duplicate_entry() in ***app.py*** : >')
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        row=request.args.get("row")
        print("\nrow : ",row)
        result=sqlite_db_duplicate_entry('variables',row)         
        message1="OK done - Entry DUPLICATED"
        image="../static/images/ok.png" 
        message2="entry had been duplicated"
        message3="/variables_dashboard"
        message4="variables Dashboard"
        PAGE_DESTINATION="operation_done"
        page_name="operation_done.html"
        loguer(env.level+' route END OF example_name() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]
        return render_template('main_index.html',route=route,USERNAME=session['user'],PAGE_DESTINATION=PAGE_DESTINATION,message1=message1,message2=message2,message3=message3,message4=message4,image=image,page_name=page_name)
 


#  def_workflows***
@app.route('/workflows', methods=['GET'])
def workflows():
    '''
    Created : 2025-10-29T16:28:37.000Z

    description : display workflow creation dashboard
    '''
    route="/workflows"
    env.level+='-'
    print('\n'+env.level,white('route workflows() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route workflows() in ***app.py*** : >')
    global client_id
    global client_password
    global host
    global host_for_token
    global profil_name
    if not session.get('logged_in'):
        return render_template('login.html')
    else:     
        keyword='' # select every entries in DB
        with open('./sqlite_databases_code/workflows/db_details.txt') as file:
            db_details_dict=json.loads(file.read())
        print('db_details_dict : \n',yellow(db_details_dict,bold=True))
        database = os.getcwd()+'/z_bases/workflows.db'
        database=database.replace("\\","/")
        print('database is :',database)
        # sqlite:///:memory: (or, sqlite://)
        # sqlite:///relative/path/to/file.db
        # sqlite:////absolute/path/to/file.db
        db_name = "workflows.db"
        table_name = db_details_dict["table_name"]
        engine = sqlalchemy.create_engine("sqlite:///z_bases/%s" % db_name, execution_options={"sqlite_raw_colnames": True})
        df = pd.read_sql_table(table_name, engine)
        out_df = df[['index','workflow_name','step','step_name','input','output','comment']]
        #save result to csv file
        #out_df.to_csv(r'./result/workflows.csv')
        df = DataFrame(out_df)
        #print (df)
        select_options=''
        res = df.values.tolist()
        step_dict={}
        for item in res:
            print(item)    
            step_dict[item[2]]={
                'title':item[2],
                'description':item[3]
            }         
        print('step_dict : ' ,yellow(step_dict,bold=True))
        # sort detection by steps
        sorted_dict = {}
        step_list=[]
        for item,value in step_dict.items():
            print('item:\n',yellow(item,bold=True))   
            print('value:\n',yellow(value,bold=True))
            step_list.append([value['title'],item])
        sorted_step_list = sorted(step_list, key=operator.itemgetter(0),reverse=False)     
        print()
        print('sorted step_list:\n',cyan(sorted_step_list,bold=True))   
        print()     
        for step in sorted_step_list:
            for item,valeur in step_dict.items():
                if item==step[1] and valeur['title']== step[0]:
                    sorted_dict[item] = step_dict[item]
                    break    
        
        print('=========================================')
        columns="workflow_name,step,step_name,input,output,comment"    
        message1="Message 1 :"
        image="../static/images/toolbox.png" 
        message2="Message 2 :"
        message3="/Message 3"
        message4="Message 4 in button"
        PAGE_DESTINATION="z_workflows"
        page_name="z_workflows.html"
        loguer(env.level+' route END OF workflows() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]
        return render_template('main_index.html',route=route,USERNAME=session['user'],PAGE_DESTINATION=PAGE_DESTINATION,page_name=page_name,step_dict=sorted_dict)
        


#  def_workflows_db_read_custom***
@app.route('/workflows_db_read_custom', methods=['GET'])
def workflows_db_read_custom():
    '''
    Created : 2025-10-29T18:18:38.000Z

    description : Display the workflow read DB custom formular
    '''
    route="/workflows_db_read_custom"
    env.level+='-'
    print('\n'+env.level,white('route workflows_db_read_custom() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route workflows_db_read_custom() in ***app.py*** : >')
    global client_id
    global client_password
    global host
    global host_for_token
    global profil_name
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        keyword=''
        keyword=request.args.get("keyword")
        print("\nkeyword : ",keyword)
        with open('./sqlite_databases_code/workflows/db_details.txt') as file:
            db_details_dict=json.loads(file.read())
        print('db_details_dict : \n',yellow(db_details_dict,bold=True))
        database = os.getcwd()+'/z_bases/workflows.db'
        database=database.replace("\\","/")
        print('database is :',database)
        # sqlite:///:memory: (or, sqlite://)
        # sqlite:///relative/path/to/file.db
        # sqlite:////absolute/path/to/file.db
        db_name = "workflows.db"
        table_name = db_details_dict["table_name"]
        engine = sqlalchemy.create_engine("sqlite:///z_bases/%s" % db_name, execution_options={"sqlite_raw_colnames": True})
        df = pd.read_sql_table(table_name, engine)
        out_df = df[['index','workflow_name','step','step_name','input','output','comment']]
        #save result to csv file
        out_df.to_csv(r'./result/workflows.csv')
        df = DataFrame(out_df)
        #print (df)
        select_options=''
        res = df.values.tolist()
        element_index=2
        sorted_list=sorted(res, key=lambda x: x[element_index])
                    
        for item in sorted_list:
            if keyword:
                if keyword in item:
                    select_options=select_options+'<option value="'+str(item[2])+'">'+item[2]+'</option>'
            else:
                select_options=select_options+'<option value="'+str(item[2])+'">'+item[2]+'</option>'
        print('=========================================')
        columns="workflow_name,step,step_name,input,output,comment"
        print('DONE')
        html_output='''<!DOCTYPE HTML>
<!-- description-->
<html>
    <head>
        <title>FLASK APP GENERATOR</title>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no" />
        <link rel="stylesheet" href="../static/assets/css/main.css" />
    <script>
        function popup_window( url, id, width, height )
        {
            //extract the url parameters if any, and pass them to the called html
            var tempvar=document.location.toString(); // fetch the URL string
            var passedparams = tempvar.lastIndexOf("?");
            if(passedparams > -1)
                url += tempvar.substring(passedparams);
            popup = window.open( url, id, 'toolbar=no,scrollbars=yes,location=yes,statusbar=yes,menubar=no,resizable=yes,width=' + width + ',height=' + height + '' );
            popup.focus();
        }
    </script>
    </head>
    <body class="is-preload">
        <!-- Nav -->
            <nav id="nav">
                <ul>
                
                    <li><a href="/">Back to main page</a></li>
                    <li><a href="/workflows_dashboard">Back to Database Page</a></li>
                    <li><a href="/logout">log Out</a></li>
                    <li><a href="javascript:popup_window('/page_info?page=route_def_workflows_db_read.py&route=/workflows_db_read','page_info',700,600);">:</a></li>
        
                </ul>
            </nav>
            <article id="indic_list" class="wrapper style4">
                <div class="container medium">
                    <header>
                        <h2>Database Content</h2>
                        <p>Select a Row</p>
                        <p>Or refine Search by keyword (in any columns)</p>
                    </header>
                    <div class="row">
                        <div class="col-12">
                            <form method="get" action="/workflows_step_details">
                                <input type="hidden" name="database" value="workflows">
                                <input type="hidden" name="table" value="workflows">
                                <input type="hidden" name="columns" value="'''+columns+'''">
                                <div class="row">
                                    <div class="col-12">
                                        <select id="step" name="step">
                                        '''+select_options+'''
                                        </select>
                                    </div>
                                    <div class="col-12">
                                        <ul class="actions">
                                        <li><input type="submit" value="Select this row" class="button small scrolly" /></li>
                                        </ul>
                                    </div>
                                </div>
                            </form>
                        </div>
                        <form method="get" action="/workflows_db_read_custom">
                            <div class="row">
                                <div class="col-6 col-12-small">
                                    <h3>Search Keyword :</h3>
                                </div>
                                <div class="col-6 col-12-small">
                                    <input type="text"  id="keyword" name="keyword" placeholder="keyword" />
                                </div>
                                <div class="col-12">
                                    <ul class="actions">
                                        <input type="submit" value="Search" class="button small scrolly" />
                                    </ul>
                                </div>
                        </form>
                    </div>
                    <footer>
                        <ul id="copyright">
                            
                        </ul>
                    </footer>
                </div>
            </article>
        <!-- Scripts -->
            <script src="../static/assets/js/jquery.min.js"></script>
            <script src="../static/assets/js/jquery.scrolly.min.js"></script>
            <script src="../static/assets/js/init.js"></script>
            <script src="../static/assets/js/browser.min.js"></script>
            <script src="../static/assets/js/breakpoints.min.js"></script>
            <script src="../static/assets/js/util.js"></script>
            <script src="../static/assets/js/main.js"></script>
    </body>
</html>
'''
        loguer(env.level+' route END OF workflows_db_read() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]
        return html_output

#  def_db_row_details_workflows***
@app.route('/db_row_details_workflows', methods=['GET'])
def db_row_details_workflows():
    '''
    Created : 2025-10-26
    description : 
    '''
    route="/db_row_details_workflows"
    env.level+='-'
    print('\n'+env.level,white('route db_row_details_workflows() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route db_row_details_workflows() in ***app.py*** : >')
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        # GET variable from calling web page
        row=request.args.get("row")
        print("\nrow : ",row)
        database=request.args.get("database")
        print("\ndatabase : ",database)
        table=request.args.get("table")
        print("\ntable : ",table)
        columns=request.args.get("columns")
        print("\ncolumns : ",columns)
        column_list=columns.split(',')
        where_clause='where `index` = '+row
        entry_list=sqlite_db_select_entry(database,table,where_clause)
        print("\nentry_list : \n",entry_list)
        workflow_name=entry_list[0][1]
        step=entry_list[0][2]
        step_name=entry_list[0][3]
        input=entry_list[0][4]
        output=entry_list[0][5]
        comment=entry_list[0][6]
        PAGE_DESTINATION="z_db_display_entry_details_workflows"
        page_name="z_db_display_entry_details_workflows.html"
        loguer(env.level+' route END OF db_row_details_workflows() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]
        return render_template('main_index.html',route=route,USERNAME=session['user'],PAGE_DESTINATION=PAGE_DESTINATION,page_name=page_name,db_name=database,row=row,workflow_name=workflow_name,step=step,step_name=step_name,input=input,output=output,comment=comment)
        


#  def_new_step***
@app.route('/new_step', methods=['GET'])
def new_step():
    '''
    Created : 2025-10-29T22:20:51.000Z

    description : display the add a new step in workflows formular
    '''
    route="/new_step"
    env.level+='-'
    print('\n'+env.level,white('route new_step() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route new_step() in ***app.py*** : >')
    global client_id
    global client_password
    global host
    global host_for_token
    global profil_name
    if not session.get('logged_in'):
        return render_template('login.html')
    else:   
        workflow_name="Automation Challenge"
        PAGE_DESTINATION="z_new_step"
        page_name="z_new_step.html"
        loguer(env.level+' route END OF new_step() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]
        return render_template('main_index.html',route=route,USERNAME=session['user'],PAGE_DESTINATION=PAGE_DESTINATION,page_name=page_name,workflow_name=workflow_name)
        


#  def_workflows_step_details***
@app.route('/workflows_step_details', methods=['GET'])
def workflows_step_details():
    '''
    Created : 2025-11-03

    description : display formular for editing selected step details
    '''
    route="/workflows_step_details"
    env.level+='-'
    print('\n'+env.level,white('route workflows_step_details() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route workflows_step_details() in ***app.py*** : >')
    global client_id
    global client_password
    global host
    global host_for_token
    global profil_name
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        # GET variable from calling web page
        step=request.args.get("step")
        step0=step
        print("\nstep : ",step)
        with open('./result/step.txt','w') as file:
            file.write(step)        
        database="workflows"
        print("\ndatabase : ",database)
        table="workflows"
        print("\ntable : ",table)
        where_clause=f'where step = "{step}"'
        entry_list=sqlite_db_select_entry(database,table,where_clause)
        print("\nentry_list : \n",entry_list)
        row=entry_list[0][0]
        workflow_name=entry_list[0][1]
        #step=entry_list[0][2]
        step_name=entry_list[0][3]
        if ' <=> ' in step_name:
            step_name_list=step_name.split(' <=> ')
            step_prefix=step_name_list [0]
            step_name=step_name_list [1]
        else:
            step_prefix=""
            step_name=step_name           
        input=entry_list[0][4]
        if input=='':
            input='None'
        output=entry_list[0][5]
        if output=='':
            output='None'        
        comment=entry_list[0][6]
        # api calls
        db_name = "api_calls.db"
        table_name = "api_calls"
        engine = sqlalchemy.create_engine("sqlite:///z_bases/%s" % db_name, execution_options={"sqlite_raw_colnames": True})
        df = pd.read_sql_table(table_name, engine)
        out_df = df[['index','name','fqdn','relative_url','documentation','method','description','payload','header','body','query_params','custom_variables','authentication_profile','inputs_variables','output_variables']]
        #save result to csv file
        out_df.to_csv(r'./result/api_calls.csv')
        df = DataFrame(out_df)
        #print (df)
        #save result to csv file
        #out_df.to_csv(r'./result/workflows.csv')
        df = DataFrame(out_df)
        #print (df)
        select_options=''
        res = df.values.tolist()
        function_dict={}
        for item in res:
            print(item)    
            function_dict[item[1]]={
                'title':item[1],
            }     
        # functions
        # Functions
        db_name = "functions.db"
        table_name = "functions"
        engine = sqlalchemy.create_engine("sqlite:///z_bases/%s" % db_name, execution_options={"sqlite_raw_colnames": True})
        df = pd.read_sql_table(table_name, engine)
        out_df = df[['index','name','environment_name','description','called_function','input_variables','output_variables','comment']]
        df = DataFrame(out_df)
        #print (df)
        res = df.values.tolist()
        for item in res:
            print(item)    
            function_dict[item[1]]={
                'title':item[1],
            }         
        # variables        
        db_name = "variables.db"
        table_name = "variables"
        engine = sqlalchemy.create_engine("sqlite:///z_bases/%s" % db_name, execution_options={"sqlite_raw_colnames": True})
        df = pd.read_sql_table(table_name, engine)
        out_df = df[['index','name','environment_name','value','description','comment','used_by']]
        df = DataFrame(out_df)
        #print (df)
        res = df.values.tolist()
        variables_dict={}
        for item in res:
            print(item)    
            variables_dict[item[1]]={
                'title':item[1],
            }      
        sorted_variables_dict = {}
        variables_list=[]
        for item,value in variables_dict.items():
            print('item:\n',yellow(item,bold=True))   
            print('value:\n',yellow(value,bold=True))
            variables_list.append([value['title'],item])
        sorted_variables_list = sorted(variables_list, key=operator.itemgetter(0),reverse=False)     
        print()
        print('sorted_variables_list:\n',cyan(sorted_variables_list,bold=True))   
        print()     
        for step in sorted_variables_list:
            for item,valeur in variables_dict.items():
                if item==step[1] and valeur['title']== step[0]:
                    sorted_variables_dict[item] = variables_dict[item]
                    break            
        # STEPs
        db_name = "workflows.db"
        column_list=['workflow_name','step','step_name','input','output','comment']
        print('\ncolumn_list :',cyan(column_list,bold=True))
        index=sqlite_db_get_last_index('workflows')
        index+=1        
        print('index : ',index)
        # step list
        step_list_dict={}
        table_name = "workflows"
        engine = sqlalchemy.create_engine("sqlite:///z_bases/%s" % db_name, execution_options={"sqlite_raw_colnames": True})
        df = pd.read_sql_table(table_name, engine)
        out_df = df[['index','workflow_name','step','step_name','input','output','comment']]
        df = DataFrame(out_df)
        #print (df)
        res = df.values.tolist()
        steps_dict={}
        nb_step=0
        for item in res:
            print(item)    
            steps_dict[item[2]]={
                'title':item[2],
                'index':item[0]
            }  
            nb_step+=1
        print('steps_dict : ' ,yellow(steps_dict,bold=True))
        # sort detection by steps
        sorted_dict = {}
        step_list=[]
        for item,value in steps_dict.items():
            print('item:\n',yellow(item,bold=True))   
            print('value:\n',yellow(value,bold=True))
            step_list.append([value['title'],item])
        sorted_step_list = sorted(step_list, key=operator.itemgetter(0),reverse=False)     
        print()
        print('sorted step_list:\n',cyan(sorted_step_list,bold=True))   
        print()     
        for step in sorted_step_list:
            for item,valeur in steps_dict.items():
                if item==step[1] and valeur['title']== step[0]:
                    sorted_dict[item] = steps_dict[item]
                    break           
        
        # ######################################
        PAGE_DESTINATION="z_db_display_entry_details_workflows"
        page_name="z_db_display_entry_details_workflows.html"
        loguer(env.level+' route END OF db_row_details_workflows() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]
        return render_template('main_index.html',route=route,USERNAME=session['user'],PAGE_DESTINATION=PAGE_DESTINATION,row=row,page_name=page_name,db_name=database,workflow_name=workflow_name,step=step0,step_prefix=step_prefix,step_name=step_name,sorted_step_dict=sorted_dict,input=input,output=output,comment=comment,function_dict=function_dict,variables_dict=sorted_variables_dict)
        


#  def_run_workflow***
@app.route('/run_workflow', methods=['GET'])
def run_workflow():
    '''
    Created : 2025-10-31T13:52:25.000Z
    description : Go to run workflow
    '''
    route="/run_workflow"
    env.level+='-'
    print('\n'+env.level,white('route run_workflow() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route run_workflow() in ***app.py*** : >')
    global client_id
    global client_password
    global host
    global host_for_token
    global profil_name
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        with open('./result/step.txt','w') as file:
            file.write('Step 01')
        message1="Ready to run the workflow"
        image="../static/images/automation.png"
        message2="Run the workflow step by step"
        message3="/go_run_workflow"
        message4="GO Run Workflow"
        PAGE_DESTINATION="z_run_workflow"
        page_name="z_run_workflow.html"
        loguer(env.level+' route END OF run_workflow() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]
        return render_template('main_index.html',route=route,USERNAME=session['user'],PAGE_DESTINATION=PAGE_DESTINATION,message1=message1,message2=message2,message3=message3,message4=message4,image=image,page_name=page_name)
        


#  def_go_run_workflow***
@app.route('/go_run_workflow', methods=['GET'])
def go_run_workflow():
    '''
    Created : 2025-10-31T14:00:17.000Z

    description : go to step execution formular
    '''
    route="/go_run_workflow"
    env.level+='-'
    print('\n'+env.level,white('route go_run_workflow() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route go_run_workflow() in ***app.py*** : >')
    global client_id
    global client_password
    global host
    global host_for_token
    global profil_name
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        with open('./result/step.txt') as file:
            step=file.read()
        print("\nRead step  : ",step)            
        current_index=step.split(' ')[1]
        next_step=int(current_index)+1
        if next_step==1:
            str_next_step='Step 01'
        elif next_step==2:
            str_next_step='Step 02'    
        elif next_step==3:
            str_next_step='Step 03' 
        elif next_step==3:
            str_next_step='Step 03' 
        elif next_step==4:
            str_next_step='Step 04' 
        elif next_step==5:
            str_next_step='Step 05' 
        elif next_step==6:
            str_next_step='Step 06' 
        elif next_step==7:
            str_next_step='Step 07' 
        elif next_step==8:
            str_next_step='Step 08'     
        elif next_step==9:
            str_next_step='Step 09'             
        else:
            str_next_step='Step '+str(next_step)
        database="workflows"
        print("\ndatabase : ",database)
        table="workflows"
        print("\ntable : ",table)
        where_clause=f'where step = "{step}"'
        entry_list=sqlite_db_select_entry(database,table,where_clause)
        print("\nentry_list : \n",entry_list)        
        if entry_list!=[]:
            row=entry_list[0][0]
            workflow_name=entry_list[0][1]
            step=entry_list[0][2]
            step_name=entry_list[0][3]
            if ' <=> ' in step_name:
                step_name_list=step_name.split(' <=> ')
                step_prefix=step_name_list [0]
                step_name=step_name_list [1]
            else:
                step_prefix=""
                step_name=step_name           
            input=entry_list[0][4]
            output=entry_list[0][5]
            comment=entry_list[0][6]
       
            PAGE_DESTINATION="z_go_run_workflow_step"
            page_name="z_go_run_workflow_step.html"
            loguer(env.level+' route END OF db_row_details_workflows() in ***app.py*** : >')
            # ===================================================================
            env.level=env.level[:-1]
            return render_template('main_index.html',route=route,USERNAME=session['user'],PAGE_DESTINATION=PAGE_DESTINATION,row=row,page_name=page_name,db_name=database,workflow_name=workflow_name,step=step,step_prefix=step_prefix,step_name=step_name,input=input,output=output,comment=comment,next_step=str_next_step)
        else:
            image="../static/images/ok.png"
            message1="End Of workflow"
            message2="Workflow completed"
            message3="/challenge_result"
            message4="Check Results"
            PAGE_DESTINATION="operation_done"
            page_name="operation_done.html"
            env.level=env.level[:-1]
            return render_template('main_index.html',route=route,USERNAME=session['user'],PAGE_DESTINATION=PAGE_DESTINATION,message1=message1,message2=message2,message3=message3,message4=message4,image=image,page_name=page_name)
 

#  def_execute_this_step***
@app.route('/execute_this_step', methods=['GET'])
def execute_this_step():
    '''
    Created : 2025-11-03

    description : execute the step
    '''
    route="/execute_this_step"
    env.level+='-'
    print('\n'+env.level,white('route execute_this_step() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route execute_this_step() in ***app.py*** : >')
    global client_id
    global client_password
    global host
    global host_for_token
    global profil_name
    if not session.get('logged_in'):
        return render_template('login.html')
    else:          
        global use_simulator
        with open('./json_results/json_result.json','w') as file:  
            file.write('{}')
        with open('./result/step.txt') as file:
            step=file.read()
        current_index=step.split(' ')[1]
        next_step=int(current_index)+1
        if next_step==1:
            str_next_step='Step 01'
        elif next_step==2:
            str_next_step='Step 02'    
        elif next_step==3:
            str_next_step='Step 03' 
        elif next_step==3:
            str_next_step='Step 03' 
        elif next_step==4:
            str_next_step='Step 04' 
        elif next_step==5:
            str_next_step='Step 05' 
        elif next_step==6:
            str_next_step='Step 06' 
        elif next_step==7:
            str_next_step='Step 07' 
        elif next_step==8:
            str_next_step='Step 08'     
        elif next_step==9:
            str_next_step='Step 09'             
        else:
            str_next_step='Step '+str(next_step)
        database="workflows"
        print("\ndatabase : ",database)
        table="workflows"
        print("\ntable : ",table)
        where_clause=f'where step = "{step}"'
        entry_list=sqlite_db_select_entry(database,table,where_clause)
        print("\nentry_list : \n",entry_list)
        row=entry_list[0][0]
        workflow_name=entry_list[0][1]
        #step=entry_list[0][2]
        step_name=entry_list[0][3]         
        step_input=entry_list[0][4]
        step_input_list=step_input.split(',')
        '''
        if "{" in input or "[" in input:
            input
        '''
        step_output=entry_list[0][5]
        step_output_list=step_output.split(',')
        comment=entry_list[0][6]
        # ############################################
        # search for API calls
        use_function=1
        if use_function==1:
            db_name = "api_calls.db"
            table_name = "api_calls"
            engine = sqlalchemy.create_engine("sqlite:///z_bases/%s" % db_name, execution_options={"sqlite_raw_colnames": True})
            df = pd.read_sql_table(table_name, engine)
            out_df = df[['index','name','fqdn','relative_url','documentation','method','description','payload','header','body','query_params','custom_variables','authentication_profile','inputs_variables','output_variables']]
            df = DataFrame(out_df)
            #print (' df :',cyan(df,bold=True))
            res = df.values.tolist()
            authentication_profile=''
            found=0
            for item in res:
                api_call_name=item[1]
                print (' api call name :',cyan(api_call_name,bold=True))
                if ' <=> ' in step_name:
                    step_name=step_name.split(' <=> ')[1]                
                print (' step_name :',cyan(step_name,bold=True))
                if step_name==api_call_name:    
                    found=1
                    print('\n API Call found in Database :',cyan(item,bold=True))
                    api_call_name=item[1]        
                    result,response_txt=select_api_call_and_send_it(api_call_name)
            if found==0:
                # #################################################
                # #########  THEN SEARCH IN FUNCTIONS DATABASE
                response_txt=""
                keyword=step_name
                print("\nkeyword : ",keyword)      
                database = os.getcwd()+'/z_bases/functions.db'
                database=database.replace("\\","/")
                print('database is :',database)
                db_name = "functions.db"
                table_name = "functions"
                engine = sqlalchemy.create_engine("sqlite:///z_bases/%s" % db_name, execution_options={"sqlite_raw_colnames": True})
                df = pd.read_sql_table(table_name, engine)
                out_df = df[['index','name','environment_name','description','called_function','input_variables','output_variables','comment']]
                df = DataFrame(out_df)
                #print (df)
                select_options=''
                res = df.values.tolist()
                found=0
                for item in res:
                    if keyword in item:
                        found=1
                        print('FUNCTION FOUND THEN RUN IT')
                        print(item)
                        called_function=item[4]
                        print('called function : ',called_function)                   
                        print('input variables : ',item[5])
                        print('output variables : ',item[6])
                        print('Step input variables list : ',step_input_list)
                        print('Step output variables list : ',step_output_list)  
                        step_input_variable_list=[]
                        database="variables"
                        #database = os.getcwd()+'/z_bases/'+database+'.db'
                        #database=database.replace("\\","/")                    
                        print("\ndatabase : ",database)
                        table="variables"
                        print("\ntable : ",table)                    
                        for item in step_input_list:
                            where_clause=f'where name = "{item}"'
                            entry_list=sqlite_db_select_entry(database,table,where_clause)
                            #print("\nentry_list : \n",entry_list)
                            step_input_variable_list.append(entry_list[0][3])   
                        print('Step input variables list : ',yellow(step_input_variable_list,bold=True))
                        if called_function=='parse_result_of_cse_get_computers':
                            guid=parse_result_of_cse_get_computers(step_input_variable_list[0],step_input_variable_list[1])
                            if "xxxx" not in guid:
                                response_txt=guid
                                result=variables_sqlite_update_value(step_output,guid)
                                result=1
                                with open('./result/step.txt','w') as file:
                                    file.write(str_next_step)                               
                            else:
                                result=0
                        elif called_function=='cse_id_of_event_type_name':
                            event_type_id=cse_id_of_event_type_name(step_input_variable_list[0])
                            if "xxxx" not in event_type_id:
                                response_txt=event_type_id
                                result=variables_sqlite_update_value(step_output,event_type_id)
                                result=1
                                with open('./result/step.txt','w') as file:
                                    file.write(str_next_step)                               
                            else:
                                result=0    
                        elif called_function=='cse_check_for_events_in_host':
                            idlist=step_input_variable_list[2].split(',')     
                            host_events="xxxxxx"
                            host_events=cse_check_for_events_in_host(step_input_variable_list[0],step_input_variable_list[1],idlist)
                            host_events_txt=json.dumps(host_events)
                            with open('./json_results/json_result.json','w') as file:
                                file.write(host_events_txt)                        
                            #print('\nstep_output : ',red(step_output,bold=True))
                            #print()                              
                            if "xxxx" not in host_events:
                                response_txt=host_events
                                print('\nstep_output : ',red(step_output,bold=True))
                                print()                                
                                result=variables_sqlite_update_value(step_output,host_events_txt)
                                result=1
                                with open('./result/step.txt','w') as file:
                                    file.write(str_next_step)                               
                            else:
                                result=0      
                        elif called_function=='get_sha256_from_cse_event':
                            sha256="xxxxxx"
                            sha256,filename=get_sha256_from_cse_event(step_input_variable_list[0])
                            sha256_txt='{"sha256":"'+sha256+'"}'
                            with open('./json_results/json_result.json','w') as file:
                                file.write(sha256_txt)                        
                            #print('\nstep_output : ',red(step_output,bold=True))
                            #print()                              
                            if "xxxx" not in sha256:
                                response_txt=sha256_txt
                                #print('\nstep_output : ',red(step_output,bold=True))
                                #print()                                
                                variables_sqlite_update_value('CSE_malicious_file_sha256',sha256)
                                variables_sqlite_update_value('CSE_malicious_file_name',filename)
                                result=1
                                with open('./result/step.txt','w') as file:
                                    file.write(str_next_step)                               
                            else:
                                result=0         
                        elif called_function=='parse_result_of_ma_search_submission':
                            sample_id_txt="xxxxxx"
                            sample_id=parse_result_of_ma_search_submission(step_input_variable_list[0])
                            sample_id_txt='{"sample_id":"'+str(sample_id)+'"}'
                            with open('./json_results/json_result.json','w') as file:
                                file.write(sample_id_txt)                        
                            #print('\nstep_output : ',red(step_output,bold=True))
                            #print()                              
                            if "xxxx" not in sample_id_txt:
                                response_txt=sample_id_txt
                                #print('\nstep_output : ',red(step_output,bold=True))
                                #print()                                
                                variables_sqlite_update_value('Malware_Analytics_sample_ID',str(sample_id))
                                result=1
                                with open('./result/step.txt','w') as file:
                                    file.write(str_next_step)                               
                            else:
                                result=0     
                        elif called_function=='parse_umbrella_result_for_token':
                            token_txt="xxxxxx"
                            token_txt=parse_umbrella_result_for_token(step_input_variable_list[0])
                            with open('./json_results/json_result.json','w') as file:
                                file.write(token_txt)                        
                            #print('\nstep_output : ',red(step_output,bold=True))
                            #print()                              
                            if "xxxx" not in token_txt:
                                response_txt=token_txt
                                #print('\nstep_output : ',red(step_output,bold=True))
                                #print()                                
                                variables_sqlite_update_value('umbrella_v2_api_token',token_txt)
                                result=1
                                with open('./result/step.txt','w') as file:
                                    file.write(str_next_step)                               
                            else:
                                result=0            
                        elif called_function=='parse_result_of_ma_get_domains':
                            domain="xxxxxx"
                            domain,domain_ip=parse_result_of_ma_get_domains(step_input_variable_list[0])
                            result_txt="{'domain':'"+domain+"','domain_ip':'"+domain_ip+"'}"
                            with open('./json_results/json_result.json','w') as file:
                                file.write(result_txt)                        
                            #print('\nstep_output : ',red(step_output,bold=True))
                            #print()                              
                            if "xxxx" not in domain:
                                response_txt=result_txt
                                #print('\nstep_output : ',red(step_output,bold=True))
                                #print()                                
                                variables_sqlite_update_value('malicious_domain_ip',domain_ip)
                                variables_sqlite_update_value('domain',domain)
                                result=1
                                with open('./result/step.txt','w') as file:
                                    file.write(str_next_step)                               
                            else:
                                result=0      
                        elif called_function=='parse_result_of_dns_activity':
                            ip_list=["xxxxxx"]
                            ip_list=parse_result_of_dns_activity(step_input_variable_list[0],step_input_variable_list[1])
                            result_txt=json.dumps(ip_list)
                            with open('./json_results/json_result.json','w') as file:
                                file.write(result_txt)                        
                            #print('\nstep_output : ',red(step_output,bold=True))
                            #print()                              
                            if "xxxx" not in ip_list:
                                response_txt=result_txt
                                #print('\nstep_output : ',red(step_output,bold=True))
                                #print()                                
                                #variables_sqlite_update_value('malicious_domain_ip',domain_ip)
                                #variables_sqlite_update_value('domain',domain)
                                index=1
                                for ip_addr in ip_list:
                                    variable_name='internal_infected_ip_address_'+str(index)
                                    index+=1
                                    variables_sqlite_update_value(variable_name,ip_addr)
                                result=1
                                with open('./result/step.txt','w') as file:
                                    file.write(str_next_step)                               
                            else:
                                result=0              
                        elif called_function=='parse_xdr_result_for_token':
                            token_txt="xxxxxx"
                            token_txt=parse_xdr_result_for_token(step_input_variable_list[0])
                            with open('./json_results/json_result.json','w') as file:
                                file.write(token_txt)                        
                            #print('\nstep_output : ',red(step_output,bold=True))
                            #print()                              
                            if "xxxx" not in token_txt:
                                response_txt=token_txt
                                print('\nstep_output : ',red(step_output,bold=True))
                                print()                                
                                variables_sqlite_update_value(step_output,token_txt)
                                result=1
                                with open('./result/step.txt','w') as file:
                                    file.write(str_next_step)                               
                            else:
                                result=0           
                        elif called_function=='set_observable_type_to_domain':
                            response_txt="{'status':'success'}"
                            set_observable_type_to_domain()
                            with open('./json_results/json_result.json','w') as file:
                                file.write(response_txt)                        
                            result=1
                            with open('./result/step.txt','w') as file:
                                file.write(str_next_step)           
                        elif called_function=='update_variables_from_json_inputs':
                            response_txt="{'status':'success'}"
                            update_variables_from_json_inputs(step_input_variable_list[0])
                            with open('./json_results/json_result.json','w') as file:
                                file.write(response_txt)                        
                            result=1
                            with open('./result/step.txt','w') as file:
                                file.write(str_next_step)                                   
                        else:
                            result=0
                            image="../static/images/nok.png"
                            message1="Operation Failed"
                            message2="No Function to call was found"
                            message3="/"
                            message4="Home"
                            PAGE_DESTINATION="operation_done"
                            page_name="operation_done.html"
                            env.level=env.level[:-1]
                            return render_template('main_index.html',route=route,USERNAME=session['user'],PAGE_DESTINATION=PAGE_DESTINATION,message1=message1,message2=message2,message3=message3,message4=message4,image=image,page_name=page_name)
                                 
                if result==1:
                    image="../static/images/ok.png"
                    message1=response_txt
                    message2="Okay !"
                    message3="#portfolio"
                    message4="Button Message"
                    PAGE_DESTINATION="z_api_call_result"
                    page_name="z_api_call_result.html"
                    env.level=env.level[:-1]
                    return render_template('main_index.html',route=route,USERNAME=session['user'],PAGE_DESTINATION=PAGE_DESTINATION,message1=message1,message2=message2,message3=message3,message4=message4,image=image,page_name=page_name)
                else:
                    image="../static/images/nok.png"
                    message1="Operation Failed"
                    message2="An Error Occured"
                    message3="/"
                    message4="Home"
                    PAGE_DESTINATION="operation_done"
                    page_name="operation_done.html"
                    env.level=env.level[:-1]
                    return render_template('main_index.html',route=route,USERNAME=session['user'],PAGE_DESTINATION=PAGE_DESTINATION,message1=message1,message2=message2,message3=message3,message4=message4,image=image,page_name=page_name)
            
                # #################################################"
                if found==0:
                    image="../static/images/nok.png"
                    message1="Operation Failed"
                    message2="API call or Function not found"
                    message3="/"
                    message4="Home"
                    PAGE_DESTINATION="operation_done"
                    page_name="operation_done.html"
                    env.level=env.level[:-1]
                    return render_template('main_index.html',route=route,USERNAME=session['user'],PAGE_DESTINATION=PAGE_DESTINATION,message1=message1,message2=message2,message3=message3,message4=message4,image=image,page_name=page_name)
            else:
                with open('./json_results/json_result.json') as file:
                    call_result=file.read()
                variables_sqlite_update_value(step_output,call_result)    
                lines=call_result.split('\n')
                #print('  lines : \n',lines)
                print('\ncall_result : \n',green(call_result,bold=True)) 
                ii=0
                for line in lines:
                    response_txt=response_txt+line+'\n'
                    ii+=1
                    if ii>200:
                        response_txt=response_txt+'..... Rest of response is not shown... it was too long \n\n=> You can click on the [ Display in Tree Graph ] button  to see the entire content'
                        break
                # #########################################################
                if result==1:
                    with open('./result/step.txt','w') as file:
                        file.write(str_next_step)                   
                    image="../static/images/ok.png"
                    message1=response_txt
                    message2="Okay !"
                    message3="#"
                    message4=""
                    PAGE_DESTINATION="z_api_call_result"
                    page_name="z_api_call_result.html"
                    env.level=env.level[:-1]
                    return render_template('main_index.html',route=route,USERNAME=session['user'],PAGE_DESTINATION=PAGE_DESTINATION,message1=message1,message2=message2,message3=message3,message4=message4,image=image,page_name=page_name)           
        else:
            # DELETE THIS BRANCH IF IT WORKS
            db_name = "api_calls.db"
            table_name = "api_calls"
            engine = sqlalchemy.create_engine("sqlite:///z_bases/%s" % db_name, execution_options={"sqlite_raw_colnames": True})
            df = pd.read_sql_table(table_name, engine)
            out_df = df[['index','name','fqdn','relative_url','documentation','method','description','payload','header','body','query_params','custom_variables','authentication_profile','inputs_variables','output_variables']]
            df = DataFrame(out_df)
            #print (' df :',cyan(df,bold=True))
            res = df.values.tolist()
            authentication_profile=''
            found=0
            for item in res:
                api_call_name=item[1]
                print (' api call name :',cyan(api_call_name,bold=True))
                if ' <=> ' in step_name:
                    step_name=step_name.split(' <=> ')[1]                
                print (' step_name :',cyan(step_name,bold=True))
                if step_name==api_call_name:    
                    found=1
                    print('\n API Call found in Database :',cyan(item,bold=True))
                    name=item[1]
                    print('\nname : ',yellow(name,bold=True))
                    print()     
                    base_url=item[2]
                    print('\nbase_url : ',yellow(base_url,bold=True))
                    print()
                    relative_url=item[3]
                    print('relative_url : ',yellow(relative_url,bold=True))
                    api_documentation=item[4]
                    print()
                    print('api_documentation : ',yellow(api_documentation,bold=True))
                    method=item[5]
                    print()
                    print('method : ',yellow(method,bold=True))
                    short_description=item[6]
                    print()
                    print('short_description : ',yellow(short_description,bold=True))
                    payload=item[7]
                    payload=payload.replace('\n','')
                    payload=payload.replace('\r','')
                    payload=payload.replace('  ',' ')
                    payload=payload.replace('  ',' ')
                    payload=payload.replace('  ',' ')
                    payload=payload.replace('  ',' ')
                    print()
                    print('payload : ',yellow(payload,bold=True))
                    header=item[7]
                    header=header.replace('\n','')
                    header=header.replace('\r','')
                    header=header.replace('  ',' ')
                    header=header.replace('  ',' ')
                    header=header.replace('  ',' ')
                    header=header.replace('  ',' ')
                    print()
                    print('header : ',yellow(header,bold=True))
                    body=item[8]
                    body=body.replace('\n','')
                    body=body.replace('\r','')
                    body=body.replace('  ',' ')
                    body=body.replace('  ',' ')
                    body=body.replace('  ',' ')
                    body=body.replace('  ',' ')
                    print()
                    print('body : ',yellow(body,bold=True))
                    params=item[9]
                    params=params.replace('\n','***')
                    params=params.replace('\r','')
                    params=params.replace('  ',' ')
                    params=params.replace('  ',' ')
                    params=params.replace('  ',' ')
                    params=params.replace('  ',' ')
                    print()
                    print('params : ',yellow(params,bold=True))
                    custom_variables=item[10]
                    print('custom_variables : ',yellow(custom_variables,bold=True))                
                    parameters=item[11]
                    parameters=parameters.replace('\n','***')
                    parameters=parameters.replace('\r','')
                    parameters=parameters.replace('  ',' ')
                    parameters=parameters.replace('  ',' ')
                    parameters=parameters.replace('  ',' ')
                    parameters=parameters.replace('  ',' ')
                    print()
                    print('parameters : ',yellow(parameters,bold=True))
                    authentication_profile=item[12]
                    if authentication_profile==None:    
                        authentication_profile=''
                    print('authentication_profile : ',yellow(authentication_profile,bold=True))
                    input_variables=item[13]
                    print('input_variables : ',yellow(input_variables,bold=True))    
                    output_variables=item[10]
                    print('output_variables : ',yellow(output_variables,bold=True))   
            print('FOUND = ' ,found)
            if found==1:
                print('\nauthentication_profile : ',yellow(authentication_profile,bold=True))
                print()   
                '''
                filename='./api_calls_history/'+name+'_'+date_time_for_file_name()+'.txt'  # http://127.0.0.1:4000/code_edit?code=def_date_time_for_file_name.py&type=function
                with open(filename,'w') as file:
                    file.write('name=:'+name+'\n')
                    file.write('base_url=:'+base_url+'\n')
                    file.write('relative_url=:'+relative_url+'\n')
                    file.write('api_documentation=:'+api_documentation+'\n')
                    file.write('method=:'+method+'\n')
                    file.write('short_description=:'+short_description+'\n')
                    file.write('payload=:'+payload+'\n')
                    file.write('header=:'+header+'\n')
                    file.write('body=:'+body+'\n')
                    file.write('params=:'+params+'\n')
                    file.write('parameters=:'+parameters+'\n')
                    file.write('authentication_profile=:'+authentication_profile+'\n')
                with open('./result/last_api_call.txt','w') as file:
                    file.write(filename)
                '''
                # Select Authentication Profile
                
                if authentication_profile!="saved_token":
                    if authentication_profile!="":
                        username,password,api_key=select_profile_function(authentication_profile) 
                        
                        authentication_dict={
                            'username':username,
                            'password':password,
                            'api_key':api_key
                        }
                        print("\nauthentication_dict : ",yellow(authentication_dict,bold=True))  
                else:
                    with open('./profiles/saved_token.txt') as file:
                        api_key=file.read()
                if "@" in base_url:
                    chunks=base_url.split('@')
                    i=0
                    new_chunks=[]
                    for chunk in chunks:
                        if 'https' in chunk or 'HTTPS' in chunk:
                            chunk=chunk.replace('https://','')
                            chunk=chunk.replace('HTTPS://','')
                            protocol='https'
                        else:
                            chunk=chunk.replace('http://','')
                            chunk=chunk.replace('HTTP://','')      
                            protocol='http'                    
                        print(chunk)    
                        if i==0:
                            creds=chunk.split(':')
                            ii=0
                            new_cred_words=[]
                            for cred_word in creds:
                                if '$$' in cred_word:
                                    mot=cred_word.replace('$$','')
                                    mot=mot.replace('***','')                        
                                print(cyan(mot,bold=True))
                                new_cred_words.append(authentication_dict[mot])
                                ii+=1
                            print(yellow(new_cred_words,bold=True))
                            new_chunks.append(protocol+'://'+new_cred_words[0]+':'+new_cred_words[1]+'@')
                        elif i==1:
                           new_chunks.append(chunk)
                        i+=1
                    if use_simulator==1:
                        base_url=new_chunks[0].replace('https:','http:')+'localhost:4000'
                    else:
                        base_url=new_chunks[0]+new_chunks[1]
                else:
                    if use_simulator==1:
                        base_url='http://localhost:4000'

                print()
                print('final base_url to use : ',cyan(base_url,bold=True))                      
                additionnal_get_params='' # parameters at the end of the URL ?parm1=xxx?param2=yyy
                if body=='':
                    body_json={}
                else:
                    body_json=json.loads(body)
                if body_json == {"grant_type": "client_credentials"}:
                    header_json=json.loads(header)
                    result,response_txt=send_api_call_for_oauth_token(base_url,relative_url,client_id,client_password,header_json,body_json) # http://127.0.0.1:4000/code_edit?code=def_send_api_call_for_oauth_token.py&type=function
                elif payload == {"grant_type": "client_credentials"}:
                    header_json=json.loads(header)
                    result,response_txt=send_api_call_for_oauth_token(base_url,relative_url,client_id,client_password,header_json,body_json) # http://127.0.0.1:4000/code_edit?code=def_send_api_call_for_oauth_token.py&type=function
                else:
                    print("\nOK SEND CALL : ") 
                    result,response_txt=send_api_call_function(method,base_url,relative_url,additionnal_get_params,header,payload,body,parameters,api_key) # http://127.0.0.1:4000/code_edit?code=def_send_api_call_function.py&type=function

                # read the first 200 lines of the JSON result
                with open('./result/step.txt','w') as file:
                    file.write(str_next_step)   
                
                with open('./json_results/json_result.json') as file:
                    call_result=file.read()
                lines=call_result.split('\n')
                #print('  lines : \n',lines)
                print('\ncall_result : \n',cyan(call_result,bold=True))
                # update SQLite DB variables
                result=variables_sqlite_update_value(step_output,call_result)
                
                # ##################################
                response_txt=''
                ii=0
                for line in lines:
                    response_txt=response_txt+line+'\n'
                    ii+=1
                    if ii>200:
                        response_txt=response_txt+'..... Rest of response is not shown... it was too long \n\n=> You can click on the [ Display in Tree Graph ] button  to see the entire content'
                        break
                # #########################################################
                if result==1:
                    image="../static/images/ok.png"
                    message1=response_txt
                    message2="Connexion to XDR Tenant is Okay !"
                    message3="#portfolio"
                    message4="Button Message"
                    PAGE_DESTINATION="z_api_call_result"
                    page_name="z_api_call_result.html"
                    env.level=env.level[:-1]
                    return render_template('main_index.html',route=route,USERNAME=session['user'],PAGE_DESTINATION=PAGE_DESTINATION,message1=message1,message2=message2,message3=message3,message4=message4,image=image,page_name=page_name)
                else:
                    image="../static/images/nok.png"
                    message1="Operation Failed"
                    message2="An Error Occured"
                    message3="/"
                    message4="Home"
                    PAGE_DESTINATION="operation_done"
                    page_name="operation_done.html"
                    env.level=env.level[:-1]
                    return render_template('main_index.html',route=route,USERNAME=session['user'],PAGE_DESTINATION=PAGE_DESTINATION,message1=message1,message2=message2,message3=message3,message4=message4,image=image,page_name=page_name)

                                                                   

#  def_functions_dashboard***
@app.route('/functions_dashboard', methods=['GET'])
def functions_dashboard():
    '''
    Flask Route for the functions_dashboard Database dashoard
    '''
    route="/functions_dashboard"
    env.level+='-'
    print('\n'+env.level,white('route functions_dashboard() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route functions_dashboard() in ***app.py*** : >')
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        html_output='''<!DOCTYPE HTML>
<!-- description-->
<html>
    <head>
        <title>FLASK APP GENERATOR</title>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no" />
        <link rel="stylesheet" href="../static/assets/css/main.css" />
    <script>
        function popup_window( url, id, width, height )
        {
            //extract the url parameters if any, and pass them to the called html
            var tempvar=document.location.toString(); // fetch the URL string
            var passedparams = tempvar.lastIndexOf("?");
            if(passedparams > -1)
                url += tempvar.substring(passedparams);
            popup = window.open( url, id, 'toolbar=no,scrollbars=yes,location=yes,statusbar=yes,menubar=no,resizable=yes,width=' + width + ',height=' + height + '' );
            popup.focus();
        }
    </script>
    </head>
    <body class="is-preload">
        <!-- Nav -->
            <nav id="nav">
                <ul>
                
                    <li><a href="/">Back to main page</a></li>
                    <li><a href="/logout">log Out</a></li>
                    <li><a href="javascript:popup_window('/page_info?page=route_def_functions_dashboard.py&route=/functions_dashboard','page_info',700,600);">:</a></li>
        
                </ul>
            </nav>
        <!-- Portfolio -->
            <article id="portfolio" class="wrapper style3">
                <div class="container">
                    <header>
                        <h2>functions Database</h2>
                    </header>
                    <div class="row">
                        <div class="col-4 col-6-medium col-12-small">
                            <article class="box style2">
                                <a href="/functions_create_db" class="image featured"><img src="../static/images/database0.png" alt="" /></a>
                                <h3><a href="/functions_create_db">Create Database</a></h3>
                                <p>Create the functions Database</p>
                            </article>
                        </div>
                        <div class="col-4 col-6-medium col-12-small">
                            <article class="box style2">
                                <a href="/functions_ingest_demo_data" class="image featured"><img src="../static/images/database0.png" alt="" /></a>
                                <h3><a href="/functions_ingest_demo_data">Ingest Demo Data</a></h3>
                                <p>Ingest Demo Data into DB</p>
                            </article>
                        </div>
                        <div class="col-4 col-6-medium col-12-small">
                            <article class="box style2">
                                <a href="/functions_db_read" class="image featured"><img src="../static/images/database0.png" alt="" /></a>
                                <h3><a href="/functions_db_read">Read Database content</a></h3>
                                <p>Read DB an Create a CSV result</p>
                            </article>
                        </div>
                        <div class="col-4 col-6-medium col-12-small">
                            <article class="box style2">
                                <a href="/functions_db_clear" class="image featured"><img src="../static/images/database0.png" alt="" /></a>
                                <h3><a href="/functions_db_clear">Clear Database</a></h3>
                                <p>Delete Database content</p>
                            </article>
                        </div>
                        <div class="col-4 col-6-medium col-12-small">
                            <article class="box style2">
                                <a href="/functions_db_ingest_csv" class="image featured"><img src="../static/images/database0.png" alt="" /></a>
                                <h3><a href="/functions_db_ingest_csv">Ingest a CSV file</a></h3>
                                <p>Ingest a CSV file</p>
                            </article>
                        </div>
                        <div class="col-4 col-6-medium col-12-small">
                            <article class="box style2">
                                <a href="/functions_db_add_entry" class="image featured"><img src="../static/images/database0.png" alt="" /></a>
                                <h3><a href="/functions_db_add_entry">Add Entry</a></h3>
                                <p>Add an Entry to Database</p>
                            </article>
                        </div>
            
                    </div>
                </div>
            </article>
        <!-- Scripts -->
            <script src="../static/assets/js/jquery.min.js"></script>
            <script src="../static/assets/js/jquery.scrolly.min.js"></script>
            <script src="../static/assets/js/init.js"></script>
            <script src="../static/assets/js/browser.min.js"></script>
            <script src="../static/assets/js/breakpoints.min.js"></script>
            <script src="../static/assets/js/util.js"></script>
            <script src="../static/assets/js/main.js"></script>
    </body>
</html>
'''
        loguer(env.level+' route END OF functions_dashboard() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]
        return html_output
        

#  def_functions_create_db***
@app.route('/functions_create_db', methods=['GET'])
def functions_create_db():
    '''
    Flask Route for the functions_create_db Database Create DB action
    '''
    route="/functions_create_db"
    env.level+='-'
    print('\n'+env.level,white('route functions_create_db() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route functions_create_db() in ***app.py*** : >')
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        with open('./sqlite_databases_code/functions/db_details.txt') as file:
            db_details_dict=json.loads(file.read())
        print('db_details_dict : \n',yellow(db_details_dict,bold=True))
        file=open('./sqlite_databases_code/functions/init/functions.csv','w')
        ligne_out=''
        len_columns=len(db_details_dict['columns'])-1
        i=0        
        for col in db_details_dict['columns']:
            if i<len_columns:
                ligne_out=ligne_out+col+','
            else:
                ligne_out=ligne_out+col
            i+=1
        file.write(ligne_out+'\n')
        for i in range (0,10):
            ligne_out='name'+str(i)+','+'environment_name'+str(i)+','+'description'+str(i)+','+'called_function'+str(i)+','+'input_variables'+str(i)+','+'output_variables'+str(i)+','+'comment'+str(i)           
            file.write(ligne_out+'\n')
        file.close()  
        create_db_and_table(db_details_dict['db_name'],db_details_dict['table_name'])
        html_output='''<!DOCTYPE HTML>
<!-- description-->
<html>
    <head>
        <title>FLASK APP GENERATOR</title>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no" />
        <link rel="stylesheet" href="../static/assets/css/main.css" />
    <script>
        function popup_window( url, id, width, height )
        {
            //extract the url parameters if any, and pass them to the called html
            var tempvar=document.location.toString(); // fetch the URL string
            var passedparams = tempvar.lastIndexOf("?");
            if(passedparams > -1)
                url += tempvar.substring(passedparams);
            popup = window.open( url, id, 'toolbar=no,scrollbars=yes,location=yes,statusbar=yes,menubar=no,resizable=yes,width=' + width + ',height=' + height + '' );
            popup.focus();
        }
    </script>
    </head>
    <body class="is-preload">
        <!-- Nav -->
            <nav id="nav">
                <ul>
                
                    <li><a href="/">Back to main page</a></li>
                    <li><a href="/logout">log Out</a></li>
                    <li><a href="javascript:popup_window('/page_info?page=route_def_bases.py&route=/functions_create_db','page_info',700,600);">:</a></li>
        
                </ul>
            </nav>
        <!-- Portfolio -->
			<article id="top" class="wrapper style1">
				<div class="container">
					<div class="row">
						<div class="col-4 col-5-large col-12-medium">
							<span class="image fit"><img src="../static/images/ok.png" alt="" /></span>
						</div>
						<div class="col-8 col-7-large col-12-medium">
							<header>
								<h1><strong> Database :functions, was created</strong></h1>
							</header>
							<p>The SQLITE had been created in ./z_bases</p>
                            <a href="/functions_dashboard" class="button small scrolly">Go to Dashboard for functions DB </a>
						</div>						
					</div>				
				</div>
			</article>
        <!-- Scripts -->
            <script src="../static/assets/js/jquery.min.js"></script>
            <script src="../static/assets/js/jquery.scrolly.min.js"></script>
            <script src="../static/assets/js/init.js"></script>
            <script src="../static/assets/js/browser.min.js"></script>
            <script src="../static/assets/js/breakpoints.min.js"></script>
            <script src="../static/assets/js/util.js"></script>
            <script src="../static/assets/js/main.js"></script>
    </body>
</html>
'''
        loguer(env.level+' route END OF functions_create_db() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]    
        return html_output


#  def_functions_ingest_demo_data***
@app.route('/functions_ingest_demo_data', methods=['GET'])
def functions_ingest_demo_data():
    '''
    Flask Route for the functions_ingest_demo_data Database Ingest demo data
    '''
    route="/functions_ingest_demo_data"
    env.level+='-'
    print('\n'+env.level,white('route functions_ingest_demo_data() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route functions_ingest_demo_data() in ***app.py*** : >')
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        with open('./sqlite_databases_code/functions/db_details.txt') as file:
            db_details_dict=json.loads(file.read())
        print('db_details_dict : \n',yellow(db_details_dict,bold=True))
        database = os.getcwd()+'/z_bases/functions.db'
        database=database.replace("\\","/")
        print('database is :',database)
        lines=[]    
        file='./sqlite_databases_code/functions/init/functions.csv'
        with open (file) as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            lines = list(reader)
            indexA=0
            print('functions table =>\n')
            conn=create_connection(database) # open connection to database            
            for row in lines:
                if conn:
                    # connection to database is OK
                    c=conn.cursor()
                    # let's go to every lines one by one and let's extract url, targeted brand
                    sqlite_data=[indexA]
                    sqlite_data=(indexA,row[0] ,row[1] ,row[2] ,row[3] ,row[4] ,row[5] ,row[6])
                    sql_add="INSERT OR IGNORE into functions (`index`,name,environment_name,description,called_function,input_variables,output_variables,comment) VALUES (?,?,?,?,?,?,?,?)"
                    print('\nsql_add :',cyan(sql_add,bold=True))
                c.execute(sql_add, sqlite_data)
                print(green("==> OK Done : demo data ingested",bold=True))
                indexA+=1
                conn.commit()        

        html_output='''<!DOCTYPE HTML>
<!-- description-->
<html>
    <head>
        <title>FLASK APP GENERATOR</title>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no" />
        <link rel="stylesheet" href="../static/assets/css/main.css" />
    <script>
        function popup_window( url, id, width, height )
        {
            //extract the url parameters if any, and pass them to the called html
            var tempvar=document.location.toString(); // fetch the URL string
            var passedparams = tempvar.lastIndexOf("?");
            if(passedparams > -1)
                url += tempvar.substring(passedparams);
            popup = window.open( url, id, 'toolbar=no,scrollbars=yes,location=yes,statusbar=yes,menubar=no,resizable=yes,width=' + width + ',height=' + height + '' );
            popup.focus();
        }
    </script>
    </head>
    <body class="is-preload">
        <!-- Nav -->
            <nav id="nav">
                <ul>
                
                    <li><a href="/">Back to main page</a></li>
                    <li><a href="/logout">log Out</a></li>
                    <li><a href="javascript:popup_window('/page_info?page=route_def_functions.py&route=/functions_ingest_demo_data_ingest_demo_data','page_info',700,600);">:</a></li>
        
                </ul>
            </nav>
        <!-- Portfolio -->
			<article id="top" class="wrapper style1">
				<div class="container">
					<div class="row">
						<div class="col-4 col-5-large col-12-medium">
							<span class="image fit"><img src="../static/images/ok.png" alt="" /></span>
						</div>
						<div class="col-8 col-7-large col-12-medium">
							<header>
								<h1><strong>Demo Data ingested</strong></h1>
							</header>
							<p>Demo Data ingested into Database :functions</p>
                            <a href="/functions_dashboard" class="button small scrolly">Go to Dashboard for functions DB </a>
						</div>						
					</div>				
				</div>
			</article>
        <!-- Scripts -->
            <script src="../static/assets/js/jquery.min.js"></script>
            <script src="../static/assets/js/jquery.scrolly.min.js"></script>
            <script src="../static/assets/js/init.js"></script>
            <script src="../static/assets/js/browser.min.js"></script>
            <script src="../static/assets/js/breakpoints.min.js"></script>
            <script src="../static/assets/js/util.js"></script>
            <script src="../static/assets/js/main.js"></script>
    </body>
</html>
'''
        loguer(env.level+' route END OF functions_ingest_demo_data() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]    
        return html_output


#  def_functions_db_clear***
@app.route('/functions_db_clear', methods=['GET'])
def functions_db_clear():
    '''
    Flask Route for the functions_db_clear Database Clearing / reset function
    '''
    route="/functions_db_clear"
    env.level+='-'
    print('\n'+env.level,white('route functions_db_clear() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route functions_db_clear() in ***app.py*** : >')
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        with open('./sqlite_databases_code/functions/db_details.txt') as file:
            db_details_dict=json.loads(file.read())
        print('db_details_dict : \n',yellow(db_details_dict,bold=True))
        database = os.getcwd()+'/z_bases/functions.db'
        database=database.replace("\\","/")
        print('database is :',database)
        print('table is :', db_details_dict["table_name"])
        conn=create_connection(database) # open connection to database
        if conn:
            # connection to database is OK
            c=conn.cursor()
            print(f'- Deleting table : {db_details_dict["table_name"]} =>')
            sql_request="drop table "+db_details_dict["table_name"]
            c.execute(sql_request)
            conn.commit()
            print('-- OK DONE : Deleted table : '+db_details_dict["table_name"])
            create_db_and_table(db_details_dict["db_name"],db_details_dict["table_name"])
            print(f'-- OK table {db_details_dict["table_name"]} reseted')     

        html_output='''<!DOCTYPE HTML>
<!-- description-->
<html>
    <head>
        <title>FLASK APP GENERATOR</title>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no" />
        <link rel="stylesheet" href="../static/assets/css/main.css" />
    <script>
        function popup_window( url, id, width, height )
        {
            //extract the url parameters if any, and pass them to the called html
            var tempvar=document.location.toString(); // fetch the URL string
            var passedparams = tempvar.lastIndexOf("?");
            if(passedparams > -1)
                url += tempvar.substring(passedparams);
            popup = window.open( url, id, 'toolbar=no,scrollbars=yes,location=yes,statusbar=yes,menubar=no,resizable=yes,width=' + width + ',height=' + height + '' );
            popup.focus();
        }
    </script>
    </head>
    <body class="is-preload">
        <!-- Nav -->
            <nav id="nav">
                <ul>
                
                    <li><a href="/">Back to main page</a></li>
                    <li><a href="/logout">log Out</a></li>
                    <li><a href="javascript:popup_window('/page_info?page=route_def_functions_db_clear.py&route=/functions_db_clear','page_info',700,600);">:</a></li>
        
                </ul>
            </nav>
        <!-- Portfolio -->
			<article id="top" class="wrapper style1">
				<div class="container">
					<div class="row">
						<div class="col-4 col-5-large col-12-medium">
							<span class="image fit"><img src="../static/images/ok.png" alt="" /></span>
						</div>
						<div class="col-8 col-7-large col-12-medium">
							<header>
								<h1><strong>Database Content Deleted</strong></h1>
							</header>
							<p>Data in Database : functions had been cleaned</p>
                            <a href="/functions_dashboard" class="button small scrolly">Go to Dashboard for functions DB </a>
						</div>						
					</div>				
				</div>
			</article>
        <!-- Scripts -->
            <script src="../static/assets/js/jquery.min.js"></script>
            <script src="../static/assets/js/jquery.scrolly.min.js"></script>
            <script src="../static/assets/js/init.js"></script>
            <script src="../static/assets/js/browser.min.js"></script>
            <script src="../static/assets/js/breakpoints.min.js"></script>
            <script src="../static/assets/js/util.js"></script>
            <script src="../static/assets/js/main.js"></script>
    </body>
</html>
'''
        loguer(env.level+' route END OF functions_db_clear() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]    
        return html_output


#  def_functions_db_read***
@app.route('/functions_db_read', methods=['GET'])
def functions_db_read():
    '''
    Flask Route for the functions_db_read Database Read DB content function
    '''
    route="/functions_db_read"
    env.level+='-'
    print('\n'+env.level,white('route functions_db_read() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route functions_db_read() in ***app.py*** : >')
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        keyword=''
        keyword=request.args.get("keyword")
        print("\nkeyword : ",keyword)      
        with open('./sqlite_databases_code/functions/db_details.txt') as file:
            db_details_dict=json.loads(file.read())
        print('db_details_dict : \n',yellow(db_details_dict,bold=True))
        database = os.getcwd()+'/z_bases/functions.db'
        database=database.replace("\\","/")
        print('database is :',database)
        # sqlite:///:memory: (or, sqlite://)
        # sqlite:///relative/path/to/file.db
        # sqlite:////absolute/path/to/file.db
        db_name = "functions.db"
        table_name = db_details_dict["table_name"]
        engine = sqlalchemy.create_engine("sqlite:///z_bases/%s" % db_name, execution_options={"sqlite_raw_colnames": True})
        df = pd.read_sql_table(table_name, engine)
        out_df = df[['index','name','environment_name','description','called_function','input_variables','output_variables','comment']]
        #save result to csv file
        out_df.to_csv(r'./result/functions.csv')
        df = DataFrame(out_df)
        #print (df)
        select_options=''
        res = df.values.tolist()
        for item in res:
            if keyword:
                if keyword in item:
                    select_options=select_options+'<option value="'+str(item[0])+'">'+item[1]+'</option>'
            else:
                select_options=select_options+'<option value="'+str(item[0])+'">'+item[1]+'</option>'     
        print('=========================================')
        columns="name,environment_name,description,called_function,input_variables,output_variables,comment"                
        print('DONE')        
        html_output='''<!DOCTYPE HTML>
<!-- description-->
<html>
    <head>
        <title>FLASK APP GENERATOR</title>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no" />
        <link rel="stylesheet" href="../static/assets/css/main.css" />
    <script>
        function popup_window( url, id, width, height )
        {
            //extract the url parameters if any, and pass them to the called html
            var tempvar=document.location.toString(); // fetch the URL string
            var passedparams = tempvar.lastIndexOf("?");
            if(passedparams > -1)
                url += tempvar.substring(passedparams);
            popup = window.open( url, id, 'toolbar=no,scrollbars=yes,location=yes,statusbar=yes,menubar=no,resizable=yes,width=' + width + ',height=' + height + '' );
            popup.focus();
        }
    </script>
    </head>
    <body class="is-preload">
        <!-- Nav -->
            <nav id="nav">
                <ul>
                
                    <li><a href="/">Back to main page</a></li>
                    <li><a href="/functions_dashboard">Back to Database Page</a></li>
                    <li><a href="/logout">log Out</a></li>
                    <li><a href="javascript:popup_window('/page_info?page=route_def_functions_db_read.py&route=/functions_db_read','page_info',700,600);">:</a></li>
        
                </ul>
            </nav>
			<article id="indic_list" class="wrapper style4">
				<div class="container medium">
					<header>
						<h2>Database Content</h2>
                        <p>Select a Row</p>
						<p>Or refine Search by keyword (in any columns)</p>
					</header>
					<div class="row">
						<div class="col-12">
							<form method="get" action="/db_row_details">
                            	<input type="hidden" name="database" value="functions">
                            	<input type="hidden" name="table" value="functions"> 
                                <input type="hidden" name="columns" value="'''+columns+'''">                                
								<div class="row">
									<div class="col-12">
										<select id="row" name="row">
                                            '''+select_options+'''           
                                        </select>
									</div>      
									<div class="col-12">
										<ul class="actions">
                                            <li><input type="submit" value="Select this row" class="button small scrolly" /></li>
										</ul>
									</div>                                    
								</div>
							</form>
						</div>    
                        <form method="get" action="/functions_db_read">
                            <div class="row">                        
                                <div class="col-6 col-12-small">
                                    <h3>Search Keyword :</h3>
                                </div>                                
                                <div class="col-6 col-12-small">
                                    <input type="text"  id="keyword" name="keyword" placeholder="keyword" />
                               </div>  
                                <div class="col-12">      
                                    <ul class="actions">
                                        <input type="submit" value="Search" class="button small scrolly" />
                                    </ul>
                                </div> 
                        </form>
					</div>
					<footer>
						<ul id="copyright">
							
						</ul>
					</footer>
				</div>
			</article>
        <!-- Scripts -->
            <script src="../static/assets/js/jquery.min.js"></script>
            <script src="../static/assets/js/jquery.scrolly.min.js"></script>
            <script src="../static/assets/js/init.js"></script>
            <script src="../static/assets/js/browser.min.js"></script>
            <script src="../static/assets/js/breakpoints.min.js"></script>
            <script src="../static/assets/js/util.js"></script>
            <script src="../static/assets/js/main.js"></script>
    </body>
</html>
'''
        loguer(env.level+' route END OF functions_db_read() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]    
        return html_output


#  def_functions_db_update_entry***
@app.route('/functions_db_update_entry', methods=['GET'])
def functions_db_update_entry():
    '''
    Flask Route for the functions_db_update_entry Database Update an entry
    '''
    route="/functions_db_update_entry"
    env.level+='-'
    print('\n'+env.level,white('route functions_db_update_entry() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route functions_db_update_entry() in ***app.py*** : >')
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        row=request.args.get("row")
        print("\nrow : ",row)
        name=request.args.get('name')
        print('\nname : ',name)
        environment_name=request.args.get('environment_name')
        print('\nenvironment_name : ',environment_name)
        description=request.args.get('description')
        print('\ndescription : ',description)
        called_function=request.args.get('called_function')
        print('\ncalled_function : ',called_function)
        input_variables=request.args.get('input_variables')
        print('\ninput_variables : ',input_variables)
        output_variables=request.args.get('output_variables')
        print('\noutput_variables : ',output_variables)
        comment=request.args.get('comment')
        print('\ncomment : ',comment)
        with open('./sqlite_databases_code/functions/db_details.txt') as file:
            db_details_dict=json.loads(file.read())
        print('db_details_dict : \n',yellow(db_details_dict,bold=True))        
        db_name = "functions.db"
        table_name = db_details_dict["table_name"]
        where_clause='`index` = '+row
        sql_fields=['index','name','environment_name','description','called_function','input_variables','output_variables','comment']
        sql_data_list=[int(row),name,environment_name,description,called_function,input_variables,output_variables,comment]
        result=sqlite_db_update_entry(db_name,table_name,where_clause,sql_fields,sql_data_list)        
        message1="OK done"
        image="../static/images/ok.png" 
        message2="entry had been updated"
        message3="/functions_dashboard"
        message4="functions Dashboard"
        PAGE_DESTINATION="operation_done"
        page_name="operation_done.html"
        loguer(env.level+' route END OF example_name() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]
        return render_template('main_index.html',route=route,USERNAME=session['user'],PAGE_DESTINATION=PAGE_DESTINATION,message1=message1,message2=message2,message3=message3,message4=message4,image=image,page_name=page_name)
 


#  def_functions_db_delete_entry***
@app.route('/functions_db_delete_entry', methods=['GET'])
def functions_db_delete_entry():
    '''
    Flask Route for the functions_db_delete_entry Database delete entry
    '''
    route="/functions_db_delete_entry"
    env.level+='-'
    print('\n'+env.level,white('route functions_db_delete_entry() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route functions_db_delete_entry() in ***app.py*** : >')
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        row=request.args.get("row")
        print("\nrow : ",row)
        result=sqlite_db_delete_entry('functions',row)         
        message1="OK done - Entry DELETED"
        image="../static/images/ok.png" 
        message2="entry had been deleted"
        message3="/functions_dashboard"
        message4="functions Dashboard"
        PAGE_DESTINATION="operation_done"
        page_name="operation_done.html"
        loguer(env.level+' route END OF example_name() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]
        return render_template('main_index.html',route=route,USERNAME=session['user'],PAGE_DESTINATION=PAGE_DESTINATION,message1=message1,message2=message2,message3=message3,message4=message4,image=image,page_name=page_name)
 


#  def_functions_db_add_entry***
@app.route('/functions_db_add_entry', methods=['GET'])
def functions_db_add_entry():
    '''
    Flask Route for the functions_db_add_entry Database Update an entry
    '''
    route="/functions_db_add_entry"
    env.level+='-'
    print('\n'+env.level,white('route functions_db_add_entry() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route functions_db_add_entry() in ***app.py*** : >')
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        db_name = "functions.db"
        column_list=['name','environment_name','description','called_function','input_variables','output_variables','comment']
        print('\ncolumn_list :',cyan(column_list,bold=True))
        index=sqlite_db_get_last_index('functions')
        index+=1        
        print('index : ',index)
        PAGE_DESTINATION="z_sqlite_db_add_entry"
        page_name="z_sqlite_db_add_entry.html"
        db_name=db_name.split('.')[0]
        loguer(env.level+' route END OF example_name() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]
        return render_template('main_index.html',route=route,USERNAME=session['user'],PAGE_DESTINATION=PAGE_DESTINATION,page_name=page_name,column_list=column_list,index=index,db_name=db_name)
 


#  def_functions_db_add_entry_ok***
@app.route('/functions_db_add_entry_ok', methods=['GET'])
def functions_db_add_entry_ok():
    '''
    Flask Route for the functions_db_add_entry Database Update an entry
    '''
    route="/functions_db_add_entry_ok"
    env.level+='-'
    print('\n'+env.level,white('route functions_db_add_entry_ok() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route functions_db_add_entry_ok() in ***app.py*** : >')
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        name=request.args.get("name")
        print("\nname: ",name)
        environment_name=request.args.get("environment_name")
        print("\nenvironment_name: ",environment_name)
        description=request.args.get("description")
        print("\ndescription: ",description)
        called_function=request.args.get("called_function")
        print("\ncalled_function: ",called_function)
        input_variables=request.args.get("input_variables")
        print("\ninput_variables: ",input_variables)
        output_variables=request.args.get("output_variables")
        print("\noutput_variables: ",output_variables)
        comment=request.args.get("comment")
        print("\ncomment: ",comment)

        db_name=request.args.get("db_name")
        print('db_name :',db_name)     
        with open('./sqlite_databases_code/'+db_name+'/db_details.txt') as file:
            db_details_dict=json.loads(file.read())
        print('db_details_dict : \n',yellow(db_details_dict,bold=True)) 
        database = os.getcwd()+'/z_bases/'+db_name+'.db'
        database=database.replace("\\","/")
        table=db_details_dict['table_name']
        print('database is :',database) 
        print('table is :',table)          
        # Get last index value in SQLITE DB
        new_index=sqlite_db_get_last_index(db_name)+1        
        print('new_index is :',new_index)  
        sqlite_data=(new_index,name,environment_name,description,called_function,input_variables,output_variables,comment)
        sql_add=f"INSERT OR IGNORE into {table} (`index`,name,environment_name,description,called_function,input_variables,output_variables,comment) VALUES (?,?,?,?,?,?,?,?)"
        print('sqlite_data :',sqlite_data)     
        print('sql_add :',sql_add)          
        con = sqlite3.connect(database)       
        try:
            cur = con.cursor()
            cur.execute(sql_add,sqlite_data)
            con.commit()
            print(green('OK DONE ENTRY DELETED',bold=True))
            image="../static/images/ok.png" 
            message1="Entry Added"
            message2="Entry was added to DB"
            message3=f"/{db_name}_dashboard"
            message4=f"{db_name}_dasbhoard"        
            PAGE_DESTINATION="operation_done"
            page_name="operation_done.html"            
            loguer(env.level+' route END OF machin_db_add_entry_ok() in ***app.py*** : >')    
            env.level=env.level[:-1]        
            return render_template('main_index.html',route=route,USERNAME=session['user'],PAGE_DESTINATION=PAGE_DESTINATION,message1=message1,message2=message2,message3=message3,message4=message4,image=image,page_name=page_name) 
        except:
            print(red('Error',bold=True))
            image="../static/images/nok.png" 
            message1="Error"
            message2="An error occured"
            message3=f"/{db_name}_dashboard"
            message4=f"{db_name}_dasbhoard"        
            PAGE_DESTINATION="operation_done"
            page_name="operation_done.html"            
            loguer(env.level+' route END OF machin_db_add_entry_ok() in ***app.py*** : >')    
            env.level=env.level[:-1]        
            return render_template('main_index.html',route=route,USERNAME=session['user'],PAGE_DESTINATION=PAGE_DESTINATION,message1=message1,message2=message2,message3=message3,message4=message4,image=image,page_name=page_name)



#  def_functions_db_ingest_csv***
@app.route('/functions_db_ingest_csv', methods=['GET'])
def functions_db_ingest_csv():
    '''
    Flask Route for the functions_db_ingest_csv Database Update an entry
    '''
    route="/functions_db_ingest_csv"
    env.level+='-'
    print('\n'+env.level,white('route functions_db_ingest_csv() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route functions_db_ingest_csv() in ***app.py*** : >')
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        db_name="functions"
        message1="Message 1 :"
        image="../static/images/toolbox.png"
        message2="Message 2 :"
        message3="/Message 3"
        message4="Message 4 in button"
        PAGE_DESTINATION="z_sqlite_ingest_csv"
        page_name="z_sqlite_ingest_csv.html"
        loguer(env.level+' route END OF functions_db_ingest_csv() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]
        return render_template('main_index.html',route=route,USERNAME=session['user'],PAGE_DESTINATION=PAGE_DESTINATION,message1=message1,message2=message2,message3=message3,message4=message4,image=image,page_name=page_name,db_name=db_name) 


#  def_functions_db_duplicate_entry***
@app.route('/functions_db_duplicate_entry', methods=['GET'])
def functions_db_duplicate_entry():
    '''
    Flask Route for the functions_db_duplicate_entry Database delete entry
    '''
    route="/functions_db_duplicate_entry"
    env.level+='-'
    print('\n'+env.level,white('route functions_db_duplicate_entry() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route functions_db_duplicate_entry() in ***app.py*** : >')
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        row=request.args.get("row")
        print("\nrow : ",row)
        result=sqlite_db_duplicate_entry('functions',row)         
        message1="OK done - Entry DUPLICATED"
        image="../static/images/ok.png" 
        message2="entry had been duplicated"
        message3="/functions_dashboard"
        message4="functions Dashboard"
        PAGE_DESTINATION="operation_done"
        page_name="operation_done.html"
        loguer(env.level+' route END OF example_name() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]
        return render_template('main_index.html',route=route,USERNAME=session['user'],PAGE_DESTINATION=PAGE_DESTINATION,message1=message1,message2=message2,message3=message3,message4=message4,image=image,page_name=page_name)
 


#  def_select_api_call_and_send_it***
@app.route('/select_api_call_and_send_it', methods=['GET'])
def select_api_call_and_send_it(api_call_name):
    '''
    Created : 2025-11-03T10:27:03.000Z

    description : Select an API call in database by name, send it and save the result in ./result
    
    how to call it : result,response_txt=select_api_call_and_send_it(api_call_name)
    '''
    route="/select_api_call_and_send_it"
    env.level+='-'
    print('\n'+env.level,white('route select_api_call_and_send_it() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route select_api_call_and_send_it() in ***app.py*** : >')
    global use_simulator
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        database = "api_calls"
        '''
        database = os.getcwd()+'/z_bases/'+database
        database=database.replace("\\","/")   
        '''
        table = "api_calls"
        print("\ndatabase : ",database)
        table="api_calls"
        print("\ntable : ",table)
        where_clause=f'where name = "{api_call_name}"'
        entry_list=sqlite_db_select_entry(database,table,where_clause)
        print("\nentry_list : \n",entry_list)                    
        name=entry_list[0][1]
        print('\nname : ',yellow(name,bold=True))
        print()     
        base_url=entry_list[0][2]
        print('\nbase_url : ',yellow(base_url,bold=True))
        print()
        relative_url=entry_list[0][3]
        if '$' in relative_url:
            relative_url=replace_variable(relative_url)        
        print('relative_url : ',yellow(relative_url,bold=True))
        api_documentation=entry_list[0][4]
        print()
        print('api_documentation : ',yellow(api_documentation,bold=True))
        method=entry_list[0][5]
        print()
        print('method : ',yellow(method,bold=True))
        short_description=entry_list[0][6]
        print()
        print('short_description : ',yellow(short_description,bold=True))
        payload=entry_list[0][7]
        payload=payload.replace('\n','')
        payload=payload.replace('\r','')
        payload=payload.replace('  ',' ')
        payload=payload.replace('  ',' ')
        payload=payload.replace('  ',' ')
        payload=payload.replace('  ',' ')
        print()
        print('payload : ',yellow(payload,bold=True))
        header=entry_list[0][8]
        if '$' in header:
            header=replace_variable(header)        
        header=header.replace('\n','')
        header=header.replace('\r','')
        header=header.replace('  ',' ')
        header=header.replace('  ',' ')
        header=header.replace('  ',' ')
        header=header.replace('  ',' ')
        print()
        print('header : ',yellow(header,bold=True))
        body=entry_list[0][9]
        if '$' in body:
            body=replace_variable(body)          
        body=body.replace('\n','')
        body=body.replace('\r','')
        body=body.replace('  ',' ')
        body=body.replace('  ',' ')
        body=body.replace('  ',' ')
        body=body.replace('  ',' ')
        print()
        print('body : ',yellow(body,bold=True))
        params=entry_list[0][10]
        if '$' in params:
            params=replace_variable(params)             
        params=params.replace('\n','***')
        params=params.replace('\r','')
        params=params.replace('  ',' ')
        params=params.replace('  ',' ')
        params=params.replace('  ',' ')
        params=params.replace('  ',' ')
        print()
        print('params : ',yellow(params,bold=True))
        #custom_variables=entry_list[0][11]
        #print('custom_variables : ',yellow(custom_variables,bold=True))                
        parameters=entry_list[0][11]
        if '$' in parameters:
            parameters=replace_variable(parameters)            
        parameters=parameters.replace('\n','***')
        parameters=parameters.replace('\r','')
        parameters=parameters.replace('  ',' ')
        parameters=parameters.replace('  ',' ')
        parameters=parameters.replace('  ',' ')
        parameters=parameters.replace('  ',' ')
        print()
        print('parameters : ',yellow(parameters,bold=True))
        authentication_profile=entry_list[0][12]
        if authentication_profile==None:    
            authentication_profile=''
        print('authentication_profile : ',yellow(authentication_profile,bold=True))
        input_variables=entry_list[0][13]
        print('input_variables : ',yellow(input_variables,bold=True))    
        output_variables=entry_list[0][14]
        print('output_variables : ',yellow(output_variables,bold=True))   
    found=1
    print('\nFOUND (x114) = ' ,found)
    if found==1:
        print('\nauthentication_profile : ',yellow(authentication_profile,bold=True))
        print()   
        '''
        filename='./api_calls_history/'+name+'_'+date_time_for_file_name()+'.txt'  # http://127.0.0.1:4000/code_edit?code=def_date_time_for_file_name.py&type=function
        with open(filename,'w') as file:
            file.write('name=:'+name+'\n')
            file.write('base_url=:'+base_url+'\n')
            file.write('relative_url=:'+relative_url+'\n')
            file.write('api_documentation=:'+api_documentation+'\n')
            file.write('method=:'+method+'\n')
            file.write('short_description=:'+short_description+'\n')
            file.write('payload=:'+payload+'\n')
            file.write('header=:'+header+'\n')
            file.write('body=:'+body+'\n')
            file.write('params=:'+params+'\n')
            file.write('parameters=:'+parameters+'\n')
            file.write('authentication_profile=:'+authentication_profile+'\n')
        with open('./result/last_api_call.txt','w') as file:
            file.write(filename)
        '''
        # Select Authentication Profile
        api_key=""
        if authentication_profile!="saved_token":
            if authentication_profile!="":
                username,password,api_key=select_profile_function(authentication_profile) 
                
                authentication_dict={
                    'username':username,
                    'password':password,
                    'api_key':api_key
                }
                print("\nauthentication_dict : ",yellow(authentication_dict,bold=True))  
        else:
            with open('./profiles/saved_token.txt') as file:
                api_key=file.read()
        if "@" in base_url:
            chunks=base_url.split('@')
            i=0
            new_chunks=[]
            for chunk in chunks:
                if 'https' in chunk or 'HTTPS' in chunk:
                    chunk=chunk.replace('https://','')
                    chunk=chunk.replace('HTTPS://','')
                    protocol='https'
                else:
                    chunk=chunk.replace('http://','')
                    chunk=chunk.replace('HTTP://','')      
                    protocol='http'                    
                print(chunk)    
                if i==0:
                    creds=chunk.split(':')
                    ii=0
                    new_cred_words=[]
                    for cred_word in creds:
                        if '$$' in cred_word:
                            mot=cred_word.replace('$$','')
                            mot=mot.replace('***','')                        
                        print(cyan(mot,bold=True))
                        new_cred_words.append(authentication_dict[mot])
                        ii+=1
                    print(yellow(new_cred_words,bold=True))
                    new_chunks.append(protocol+'://'+new_cred_words[0]+':'+new_cred_words[1]+'@')
                elif i==1:
                   new_chunks.append(chunk)
                i+=1
            if use_simulator==1:
                base_url=new_chunks[0].replace('https:','http:')+'localhost:4000'
            else:
                base_url=new_chunks[0]+new_chunks[1]
        else:
            if use_simulator==1:
                base_url='http://localhost:4000'

        print()
        print('final base_url to use : ',cyan(base_url,bold=True))                      
        additionnal_get_params='' # parameters at the end of the URL ?parm1=xxx?param2=yyy
        if body=='':
            body_json={}
        else:
            body_json=json.loads(body)
        if body_json == {"grant_type": "client_credentials"}:
            header_json=json.loads(header)
            result,response_txt=send_api_call_for_oauth_token(base_url,relative_url,client_id,client_password,header_json,body_json) # http://127.0.0.1:4000/code_edit?code=def_send_api_call_for_oauth_token.py&type=function
        elif payload == {"grant_type": "client_credentials"}:
            header_json=json.loads(header)
            result,response_txt=send_api_call_for_oauth_token(base_url,relative_url,client_id,client_password,header_json,body_json) # http://127.0.0.1:4000/code_edit?code=def_send_api_call_for_oauth_token.py&type=function
        else:
            print(red("\nOK SEND CALL (203): ",bold=True)) 
            result,response_txt=send_api_call_function(method,base_url,relative_url,additionnal_get_params,header,payload,body,params,parameters,api_key) # http://127.0.0.1:4000/code_edit?code=def_send_api_call_function.py&type=function
            result=1
    return result,response_txt

#  def_challenge_result***
@app.route('/challenge_result', methods=['GET'])
def challenge_result():
    '''
    Created : 2025-11-05

    description : display the challenge result and discovery tables
    '''
    route="/challenge_result"
    env.level+='-'
    print('\n'+env.level,white('route challenge_result() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route challenge_result() in ***app.py*** : >')
    global client_id
    global client_password
    global host
    global host_for_token
    global profil_name
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        hostname=variable_value('victim_hostname')
        guid=variable_value('GUID')
        host_ip=variable_value('infected_machine_internal_ip_address')
        internal_ip_1=variable_value('internal_infected_ip_address_1')  
        internal_ip_2=variable_value('internal_infected_ip_address_2')
        internal_ip_3=variable_value('internal_infected_ip_address_3')
        sha256=variable_value('CSE_malicious_file_sha256')
        domain=variable_value('domain')
        executed_malware_id=variable_value('CSE_Executed_Malware_event_type_ID')
        threat_detected_id=variable_value('CSE_Threat_Detected_event_type_ID')
        sha256_submission=variable_value('Malware_Analytics_sample_ID')
        nb_events=variable_value('nb_of_events_on_victim_machine')
        filename=variable_value('CSE_malicious_file_name')
        malicious_domain_ip=variable_value('malicious_domain_ip')
        # ##
        internal_ip_1_isolation_status=variable_value('internal_ip_1_isolation_status')
        if 'NO' not in internal_ip_1_isolation_status:
            internal_ip_1_isolation_status='YES'        
        internal_ip_2_isolation_status=variable_value('internal_ip_2_isolation_status')
        if 'NO' not in internal_ip_2_isolation_status:
            internal_ip_2_isolation_status='YES'        
        internal_ip_3_isolation_status=variable_value('internal_ip_3_isolation_status')
        if 'NO' not in internal_ip_3_isolation_status:
            internal_ip_3_isolation_status='YES'
        host_ip_isolation_status=variable_value('host_ip_isolation_status')
        if internal_ip_3=="192.168.128.156" and host_ip=="192.168.128.156":  
            host_ip_isolation_status='YES'
        '''
        if 'NO' not in host_ip_isolation_status:
            host_ip_isolation_status='YES'   
        '''
        guid_isolation_status=variable_value('guid_isolation_status')
        if 'NO' not in guid_isolation_status:
            guid_isolation_status='YES'        
        hostname_isolation_status=variable_value('host_ip_isolation_status')
        if 'NO' not in hostname_isolation_status:
            hostname_isolation_status='YES'        
        sha256_isolation_status=variable_value('sha256_isolation_status')
        if 'NO' not in sha256_isolation_status:
            sha256_isolation_status='YES'        
        filename_isolation_status=variable_value('filename_isolation_status')
        if 'NO' not in filename_isolation_status:
            filename_isolation_status='YES'        
        malicious_domain_ip_isolation_status=variable_value('malicious_domain_ip_isolation_status')
        if 'NO' not in malicious_domain_ip_isolation_status:
            malicious_domain_ip_isolation_status='YES'        
        domain_isolation_status=variable_value('domain_isolation_status')
        if 'NO' not in domain_isolation_status:
            domain_isolation_status='YES'        
        victim_hostname_isolation_status=variable_value('victim_hostname_isolation_status')
        if 'NO' not in victim_hostname_isolation_status:
            victim_hostname_isolation_status='YES'        
        PAGE_DESTINATION="z_challenge_result"
        page_name="z_challenge_result.html"
        loguer(env.level+' route END OF challenge_result() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]
        return render_template('main_index.html',route=route,USERNAME=session['user'],PAGE_DESTINATION=PAGE_DESTINATION,page_name=page_name,hostname=hostname,
            host_ip=host_ip,internal_ip_1=internal_ip_1,internal_ip_2=internal_ip_2,internal_ip_3=internal_ip_3,sha256=sha256,domain=domain,executed_malware_id=executed_malware_id,
            threat_detected_id=threat_detected_id,sha256_submission=sha256_submission,guid=guid,nb_events=nb_events,filename=filename,malicious_domain_ip=malicious_domain_ip,
            internal_ip_1_isolation_status=internal_ip_1_isolation_status,internal_ip_2_isolation_status=internal_ip_2_isolation_status,internal_ip_3_isolation_status=internal_ip_3_isolation_status,
            host_ip_isolation_status=host_ip_isolation_status,guid_isolation_status=guid_isolation_status,hostname_isolation_status=hostname_isolation_status,sha256_isolation_status=sha256_isolation_status,
            filename_isolation_status=filename_isolation_status,malicious_domain_ip_isolation_status=malicious_domain_ip_isolation_status,domain_isolation_status=domain_isolation_status,
            victim_hostname_isolation_status=victim_hostname_isolation_status)
        


#  def_update_variable***
@app.route('/update_variable', methods=['GET'])
def update_variable():
    '''
    Created : 2025-11-04T17:31:37.000Z

    description : display selected variable details formular for update
    '''
    route="/update_variable"
    env.level+='-'
    print('\n'+env.level,white('route update_variable() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route update_variable() in ***app.py*** : >')
    global client_id
    global client_password
    global host
    global host_for_token
    global profil_name
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        # GET variable from calling web page
        name=request.args.get("name")
        print("\nname : ",name)
        database="variables"
        print("\ndatabase : ",database)
        table="variables"
        print("\ntable : ",table)
        where_clause=f'where name = "{name}"'
        entry_list=sqlite_db_select_entry(database,table,where_clause)
        print("\nentry_list : \n",entry_list)
        row=entry_list[0][0]
        print("\nrow : ",row)        
        name=entry_list[0][1]
        print("\nname : ",name)         
        environment_name=entry_list[0][2]
        print("\nenvironment_name : ",environment_name)
        value=entry_list[0][3]
        print("\nvalue : ",value)
        description=entry_list[0][4]
        print("\ndescription : ",description)
        comment=entry_list[0][5]
        print("\ncomment : ",comment)
        comment=entry_list[0][6]
        PAGE_DESTINATION="z_update_variable"
        page_name="z_update_variable.html"    
        loguer(env.level+' route END OF update_variable() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]
        return render_template('main_index.html',route=route,USERNAME=session['user'],PAGE_DESTINATION=PAGE_DESTINATION,
        page_name=page_name,row=row,name=name,environment_name=environment_name,value=value,description=description,comment=comment)
        


#  def_reset_results***
@app.route('/reset_results', methods=['GET'])
def reset_results():
    '''
    Created : 2025-11-09

    description : reset every challenge results
    '''
    route="/reset_results"
    env.level+='-'
    print('\n'+env.level,white('route reset_results() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route reset_results() in ***app.py*** : >')
    global client_id
    global client_password
    global host
    global host_for_token
    global profil_name
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        hostname=''
        variables_sqlite_update_value('victim_hostname',hostname)
        guid=''
        variables_sqlite_update_value('GUID',guid)
        host_ip=''
        variables_sqlite_update_value('infected_machine_internal_ip_address',host_ip)
        internal_ip_1=''
        variables_sqlite_update_value('internal_infected_ip_address_1',internal_ip_1)        
        internal_ip_2=''
        variables_sqlite_update_value('internal_infected_ip_address_2',internal_ip_2)
        internal_ip_3=''
        variables_sqlite_update_value('internal_infected_ip_address_3',internal_ip_3)
        sha256=''
        variables_sqlite_update_value('CSE_malicious_file_sha256',sha256)
        domain=''
        variables_sqlite_update_value('domain',domain)
        executed_malware_id=''
        variables_sqlite_update_value('CSE_Executed_Malware_event_type_ID',executed_malware_id)
        threat_detected_id=''
        variables_sqlite_update_value('CSE_Threat_Detected_event_type_ID',threat_detected_id)
        sha256_submission=''
        variables_sqlite_update_value('sha256_submission',sha256_submission)
        nb_events=''
        variables_sqlite_update_value('nb_of_events_on_victim_machine',nb_events)
        filename=''
        variables_sqlite_update_value('CSE_malicious_file_name',filename)
        CSE_Events=''
        variables_sqlite_update_value('CSE_Events',CSE_Events)        
        CSE_host_events=''
        variables_sqlite_update_value('CSE_host_events',CSE_host_events)         
        CSE_result_of_get_computers=''
        variables_sqlite_update_value('CSE_result_of_get_computers',CSE_result_of_get_computers)         
        Malware_Analytics_result_of_search_submission=''
        variables_sqlite_update_value('Malware_Analytics_result_of_search_submission',Malware_Analytics_result_of_search_submission)    
        umbrella_json_result_of_api_token_request=''
        variables_sqlite_update_value('umbrella_json_result_of_api_token_request',umbrella_json_result_of_api_token_request)
        umbrella_v2_api_token=''
        variables_sqlite_update_value('umbrella_v2_api_token',umbrella_v2_api_token)
        umbrella_result_of_get_dns_activity=''
        variables_sqlite_update_value('umbrella_result_of_get_dns_activity',umbrella_result_of_get_dns_activity)
        malicious_domain_ip=''
        variables_sqlite_update_value('malicious_domain_ip',malicious_domain_ip)
        XDR_Token=''        
        variables_sqlite_update_value('XDR_Token',XDR_Token)
        observable_payload_for_xdr_response_actions=''
        variables_sqlite_update_value('observable_payload_for_xdr_response_actions',observable_payload_for_xdr_response_actions)
        observable_value='192.168.128.156'
        variables_sqlite_update_value('observable_value',observable_value)
        observable_type='ip'
        variables_sqlite_update_value('observable_type',observable_type)       
        module_instance_id=''
        variables_sqlite_update_value('module_instance_id',module_instance_id)        
        action_id=''
        variables_sqlite_update_value('action_id',action_id)     

        internal_ip_1_isolation_status="NO"
        variables_sqlite_update_value('internal_ip_1_isolation_status',internal_ip_1_isolation_status)
        internal_ip_2_isolation_status="NO"
        variables_sqlite_update_value('internal_ip_2_isolation_status',internal_ip_2_isolation_status)
        internal_ip_3_isolation_status="NO"
        variables_sqlite_update_value('internal_ip_3_isolation_status',internal_ip_3_isolation_status)
        host_ip_isolation_status="NO"
        variables_sqlite_update_value('host_ip_isolation_status',host_ip_isolation_status)
        guid_isolation_status="NO"
        variables_sqlite_update_value('guid_isolation_status',guid_isolation_status)
        hostname_ip_isolation_status="NO"
        variables_sqlite_update_value('hostname_ip_isolation_status',hostname_ip_isolation_status)
        sha256_isolation_status="NO"
        variables_sqlite_update_value('sha256_isolation_status',sha256_isolation_status)
        filename_isolation_status="NO"
        variables_sqlite_update_value('filename_isolation_status',filename_isolation_status)
        malicious_domain_ip_isolation_status="NO"
        variables_sqlite_update_value('malicious_domain_ip_isolation_status',malicious_domain_ip_isolation_status)
        domain_isolation_status="NO"
        variables_sqlite_update_value('domain_isolation_status',domain_isolation_status)
        victim_hostname_isolation_status="NO"
        variables_sqlite_update_value('victim_hostname_isolation_status',victim_hostname_isolation_status)       
        variables_sqlite_update_value('domain','')  
        variables_sqlite_update_value('Malware_Analytics_sample_ID','')    
        variables_sqlite_update_value('Threat_Detected_Event_Type_ID','')     
        variables_sqlite_update_value('umbrella_investigate_api_key','')        
        variables_sqlite_update_value('malware_analytics_api_key','')
        variables_sqlite_update_value('Umbrella_client_id','')
        variables_sqlite_update_value('Umbrella_client_secret','')
        variables_sqlite_update_value('MA_result_of_get_domain','')
        variables_sqlite_update_value('temp','')
        variables_sqlite_update_value('XDR_client_id','')
        variables_sqlite_update_value('XDR_client_password','')
        variables_sqlite_update_value('observable_value','192.168.128.156')
        variables_sqlite_update_value('observable_type','ip')
        variables_sqlite_update_value('Threat_Detected_Event_Type_ID','')
        variables_sqlite_update_value('API_Call_Result','')          
        variables_sqlite_update_value('JSON_FOR_VARIABLE_RESPONSE_ACTION_FOR_CSE','{"module_instance_id":"","action_id":""}')
        variables_sqlite_update_value('JSON_FOR_VARIABLE_RESPONSE_ACTION_FOR_FIREWALLs','{"module_instance_id":"","action_id":""}')
        variables_sqlite_update_value('JSON_FOR_VARIABLE_RESPONSE_ACTION_FOR_HOSTNAME','{"module_instance_id":"","action_id":""}')
        variables_sqlite_update_value('JSON_FOR_VARIABLE_RESPONSE_ACTION_FOR_ISE','{"module_instance_id":"","action_id":""}')
        variables_sqlite_update_value('JSON_FOR_VARIABLE_RESPONSE_ACTION_FOR_UMBRELLA','{"module_instance_id":"","action_id":""}')
        
        with open('./templates/isolation_status.txt','w') as file2:
            file2.write('0')         
        PAGE_DESTINATION="z_challenge_result"
        page_name="z_challenge_result.html"
        loguer(env.level+' route END OF reset_results() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]
        return render_template('main_index.html',route=route,USERNAME=session['user'],PAGE_DESTINATION=PAGE_DESTINATION,page_name=page_name,hostname=hostname,
            host_ip=host_ip,internal_ip_2=internal_ip_2,internal_ip_3=internal_ip_3,sha256=sha256,domain=domain,executed_malware_id=executed_malware_id,
            threat_detected_id=threat_detected_id,sha256_submission=sha256_submission,guid=guid,nb_events=nb_events,internal_ip_1_isolation_status=internal_ip_1_isolation_status,
            internal_ip_2_isolation_status=internal_ip_2_isolation_status,internal_ip_3_isolation_status=internal_ip_3_isolation_status,host_ip_isolation_status=host_ip_isolation_status,
            sha256_isolation_status=sha256_isolation_status,malicious_domain_ip_isolation_status=malicious_domain_ip_isolation_status,domain_isolation_status=domain_isolation_status,
            filename_isolation_status=filename_isolation_status,victim_hostname_isolation_status=victim_hostname_isolation_status,guid_isolation_status=guid_isolation_status,
            malicious_domain_ip=malicious_domain_ip)
        

#  def_xdr_get_token***
@app.route('/xdr_get_token', methods=['GET'])
def xdr_get_token():
    '''
    Created : 2025-11-05T18:18:14.000Z

    description : display XDR Get token API information
    '''
    route="/xdr_get_token"
    env.level+='-'
    print('\n'+env.level,white('route xdr_get_token() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route xdr_get_token() in ***app.py*** : >')
    global client_id
    global client_password
    global host
    global host_for_token
    global profil_name
    if not session.get('logged_in'):
        return render_template('login.html')
    else:             
        message1="Message 1 :"
        image="../static/images/toolbox.png" 
        message2="Message 2 :"
        message3="/Message 3"
        message4="Message 4 in button"
        PAGE_DESTINATION="z_xdr_get_token"
        page_name="z_xdr_get_token.html"
        loguer(env.level+' route END OF xdr_get_token() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]
        return render_template('main_index.html',route=route,USERNAME=session['user'],PAGE_DESTINATION=PAGE_DESTINATION,message1=message1,message2=message2,message3=message3,message4=message4,image=image,page_name=page_name)
        


#  def_introduction***
@app.route('/introduction', methods=['GET'])
def introduction():
    '''
    Created : 2025-11-09T22:16:40.000Z

    description : challenge presentation
    '''
    route="/introduction"
    env.level+='-'
    print('\n'+env.level,white('route introduction() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route introduction() in ***app.py*** : >')
    global client_id
    global client_password
    global host
    global host_for_token
    global profil_name
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        # ===================================================================       
        '''
        # GET variable from calling web page
        profil_name='./profiles/'+request.args.get('profil_name')
        print()
        print('profil_name : ',profil_name)        
        # POST variable 
        keyword = request.form['keyword']
        print()
        print('keyword : ',keyword)
        
        # API TOKEN
        with open('ctr_token.txt','r') as file0:
            access_token=file0.read()
            
        action=request.args.get('action')
        print()
        print('action: ',action)
        print()
        if action=="copy":
            do something
            
        #CALL  A SUB FUNCTION
        print()   
        print(magenta('--> CALL  A SUB FUNCTION :',bold=True)) 
        '''        
        # Prepare the resulting Next Web Page
        result=1
        if result==1:        
            image="../static/images/ok.png" 
            message1="Title"
            message2="Connexion to XDR Tenant is Okay !"
            message3="#portfolio"
            message4="Button Message"            
        elif result==2:
            image="../static/images/ok.png" 
            message1="Title"
            message2="Connexion to XDR Tenant is Okay !"
            message3="#portfolio"
            message4="Button Message"              
        else:
            image="../static/images/ok.png" 
            message1="Title"
            message2="Connexion to XDR Tenant is Okay !"
            message3="#portfolio"
            message4="Button Message"              
        message1="Message 1 :"
        image="../static/images/toolbox.png" 
        message2="Message 2 :"
        message3="/Message 3"
        message4="Message 4 in button"
        PAGE_DESTINATION="z_introduction"
        page_name="z_introduction.html"
        loguer(env.level+' route END OF introduction() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]
        return render_template('main_index.html',route=route,USERNAME=session['user'],PAGE_DESTINATION=PAGE_DESTINATION,message1=message1,message2=message2,message3=message3,message4=message4,image=image,page_name=page_name)
        


#  def_workflows_solution***
@app.route('/workflows_solution', methods=['GET'])
def workflows_solution():
    '''
    Created : 2025-11-10T08:50:38.000Z

    description : install example of workflow solution
    '''
    route="/workflows_solution"
    env.level+='-'
    print('\n'+env.level,white('route workflows_solution() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route workflows_solution() in ***app.py*** : >')
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        action_type = 'replace'
        with open('./sqlite_databases_code/workflows/db_details.txt') as file:
            db_details_dict=json.loads(file.read())
        print('db_details_dict : \n',yellow(db_details_dict,bold=True))
        database = os.getcwd()+'/z_bases/workflows.db'
        database=database.replace("\\","/")
        print('database is :',database)
        print('table is :', db_details_dict["table_name"])
        conn=create_connection(database) # open connection to database
        if conn:
            # connection to database is OK
            c=conn.cursor()
            print(f'- Deleting table : {db_details_dict["table_name"]} =>')
            sql_request="drop table "+db_details_dict["table_name"]
            c.execute(sql_request)
            conn.commit()
            print('-- OK DONE : Deleted table : '+db_details_dict["table_name"])
            create_db_and_table(db_details_dict["db_name"],db_details_dict["table_name"])
            print(f'-- OK table {db_details_dict["table_name"]} reseted')     
        db_name='workflows'
        with open('./sqlite_databases_code/'+db_name+'/db_details.txt') as file:
            db_details_dict=json.loads(file.read())
        print('db_details_dict : \n',yellow(db_details_dict,bold=True))
        database = os.getcwd()+'/z_bases/'+db_name+'.db'
        database=database.replace("\\","/")
        print('database is :',database)
        print('table is :',db_details_dict['table_name'])
        lines=[]
        file='./DB_backups/workflows_full_solution_ok_20251109.csv'
        with open (file) as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            lines = list(reader)
            if action_type=="replace":
                conn=create_connection(database) # open connection to database
                if conn:
                    # connection to database is OK
                    c=conn.cursor()
                    print(f'- Deleting table : {db_details_dict["table_name"]} =>')
                    sql_request="drop table "+db_details_dict["table_name"]
                    c.execute(sql_request)
                    conn.commit()
                    print('-- OK DONE : Deleted table : '+db_details_dict["table_name"])
                    create_db_and_table(db_details_dict["db_name"],db_details_dict["table_name"])
                    print(f'-- OK table {db_details_dict["table_name"]} reseted')                  
                indexA=0
            else:
                indexA=sqlite_db_get_last_index(db_name)+1
            conn=create_connection(database) # open connection to database
            for row in lines:
                if conn:
                    # connection to database is OK
                    c=conn.cursor()
                    # let's go to every lines one by one and let's extract url, targeted brand
                    len_columns=len(db_details_dict['columns'])-1
                    sqlite_data=[indexA]
                    for cel in row:
                        sqlite_data.append(cel)
                    print('\nsqlite_data :',cyan(sqlite_data,bold=True))
                    sql_add=f"INSERT OR IGNORE into {db_details_dict['table_name']} (`index`,"
                    i=0
                    for col in db_details_dict['columns']:
                        print(col)
                        if i<len_columns:
                            sql_add=sql_add+col+","
                        else:
                            sql_add=sql_add+col+")"
                        i+=1
                    sql_add=sql_add+' VALUES (?,'
                    i=0
                    for col in db_details_dict['columns']:
                        print(col)
                        if i<len_columns:
                            sql_add=sql_add+"?,"
                        else:
                            sql_add=sql_add+'?)'
                        i+=1
                    #sql_add="INSERT OR IGNORE into truc (`index`,premier,deuxieme,troisieme,quatrieme) VALUES (?,?,?,?,?)"
                    print('\nsql_add :',cyan(sql_add,bold=True))
                c.execute(sql_add, sqlite_data)
                print(green("==> OK Done : demo data ingested",bold=True))
                indexA+=1
                conn.commit()
            
        message1="Ok Done"
        image="../static/images/ok.png" 
        message2="Example of workflow soluton installed"
        message3="/workflows"
        message4="Worflows"
        PAGE_DESTINATION="operation_done"
        page_name="operation_done.html"
        loguer(env.level+' route END OF workflows_solution() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]
        return render_template('main_index.html',route=route,USERNAME=session['user'],PAGE_DESTINATION=PAGE_DESTINATION,message1=message1,message2=message2,message3=message3,message4=message4,image=image,page_name=page_name)
        


#  def_reset_databases***
@app.route('/reset_databases', methods=['GET'])
def reset_databases():
    '''
    Created : 2025-11-11T08:02:29.000Z

    description : reset every databases
    '''
    route="/reset_databases"
    env.level+='-'
    print('\n'+env.level,white('route reset_databases() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route reset_databases() in ***app.py*** : >')
    global client_id
    global client_password
    global host
    global host_for_token
    global profil_name
    if not session.get('logged_in'):
        return render_template('login.html')
    else:    
        result=reset_every_databases()
        message1="Databases Reseted"
        image="../static/images/ok.png" 
        message2="Every databases have been reseted"
        message3="/"
        message4="Home"
        PAGE_DESTINATION="operation_done"
        page_name="operation_done.html"
        loguer(env.level+' route END OF reset_databases() in ***app.py*** : >')
        # ===================================================================
        env.level=env.level[:-1]
        return render_template('main_index.html',route=route,USERNAME=session['user'],PAGE_DESTINATION=PAGE_DESTINATION,message1=message1,message2=message2,message3=message3,message4=message4,image=image,page_name=page_name)
        


#  def_compiled_package***
@app.route('/compiled_package', methods=['GET'])
def compiled_package():
    '''
    Created : 2025-11-15T07:29:36.000Z

    description : create a compiled package
    '''
    route="/compiled_package"
    env.level+='-'
    print('\n'+env.level,white('route compiled_package() in ***app.py*** : >\n',bold=True))
    loguer(env.level+' route compiled_package() in ***app.py*** : >')
    global client_id
    global client_password
    global host
    global host_for_token
    global profil_name
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        os.system("python create_compiled_package.py 1")
        with open('./result/home_url.txt') as file:
            home_url=file.read()
        html_output='''<html><body><br><a href="'''+home_url+'''"><b><= back to home</b></a><br><br>
        <center><h3>PACKAGE CREATED check ./compiled_packagesp </h3></center>
        <center><h3>A directory structure PLUS a zip file had been created</h3></center>
        </body></html>
            ''';
    env.level=env.level[:-1]
    return html_output 
  


app.config['UPLOAD_FOLDER'] = './temp'

# a_core_main.py***
if __name__ == "__main__":    
    print()
    print(env.level,white('MAIN FUNCTION ( the application starts here ): >',bold=True))
    '''
    with open('./debug/log.txt','w') as file:
        pass
    '''
    loguer(env.level)
    loguer(env.level+' APPLICATION STARTS')
    loguer(env.level)
    print()
    host="127.0.0.1"
    with open('./port.txt') as file:    
        port=file.read()
    with open('./templates/isolation_status.txt','w') as file2:
        file2.write('0')         
    open_browser_tab(host,port)
    app.secret_key = os.urandom(12)
    #app.run(debug=False,host='0.0.0.0', port=port,ssl_context='adhoc')
    app.run(debug=False,host='0.0.0.0', port=port)
