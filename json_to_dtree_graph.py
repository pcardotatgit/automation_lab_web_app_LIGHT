# -*- coding: UTF-8 -*-
#!/usr/bin/env python
'''
    read a json file and parse it :
        Create a dtree.js graph with python path
    v_20240523
'''

from crayons import *
import sys
import time
from datetime import datetime, timedelta
import sqlite3
import json
import ijson
import os
import env as env

debug=0
bb=0
save_notes=0 # saving descriptions into notes or not.  0 = don't save note.  It is to avoid to store malicious parterns in description that could be detected by local antimalware
display_path=0

text_out_header='''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html>
<head>
    <title>Visual JSON Parser</title>
    <link rel="StyleSheet" href="../static/dtree.css" type="text/css" />
    <script type="text/javascript" src="../static/dtree.js"></script>
   <script language='javascript'>
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
<body>
<h1>JSON tree graph</h1>
<div class="dtree">
    <p><a href="javascript: d.openAll();">open all</a> | <a href="javascript: d.closeAll();">close all</a></p>
    <script type="text/javascript">
        <!--
        d = new dTree('d');
        d.add(0,-1,'JSON Tree');        
'''
#  def_read_json***
def read_json(filename):
    '''
    MODIFIED : 2025-05-24T10:21:17.000Z

    description : read json text file and convert it into json data
    '''
    route="/read_json"
    env.level+='-'
    print()
    print(green('def read_json() in incident_summary_json_to_dtree_graph.py : >',bold=True))
    print()   
    global client_id
    global client_password
    global host
    global host_for_token
    global profil_name 
    with open(filename,'r') as file:
        text_data=file.read()
    json_data=json.loads(text_data)
    return(json_data)
    # ===================================================================
    env.level=env.level[:-1]
    return result
    

#  def_parse_json_tree***
def parse_json_tree(json_data):
    '''
    MODIFIED : 2025-05-24T10:28:20.000Z

    description : Parse the JSON File
    '''
    route="/parse_json_tree"
    env.level+='-'
    print()
    print(env.level,white('def parse_json_tree() in incident_summary_json_to_dtree_graph.py : >',bold=True))
    print()
    i=1
    for itemL0 in json_data:
        if i==1:
            print (cyan(itemL0,bold=True))
            i=0
            i1=1
            for itemL1 in itemL0:
                if i1==1:
                    print (red(itemL1,bold=True))
                    i1=0
                else:
                    print (green(itemL1,bold=True))
                    i1=1            
        else:
            print (yellow(itemL0,bold=True))
            i=1 
            i1=1            
            for itemL1 in itemL0:
                if i1==1:
                    print (red(itemL1,bold=True))
                    i1=0
                else:
                    print (green(itemL1,bold=True))
                    i1=1 
    env.level=env.level[:-1]
    return result
    

#  def_sxo_path0***
def sxo_path0(path,list,index):
    '''
    MODIFIED : 2025-05-24T10:30:31.000Z

    description : get python path of keys
    '''
    route="/sxo_path0"
    env.level+='-'
    print()
    print(env.level,white('def sxo_path0() in json_to_dtree_graph.py : >',bold=True))
    print()
    word_list=path.split('.')
    ii=index
    result=''    
    #print()
    #print(list, index)
    #print()    
    for item in word_list:
        if item=='item':
            #result=result+'['+str(list[ii])+'].'
            result=result+'[xx].'
            ii+=1
            #print(yellow(item,bold=True))  
        else:
            result=result+item+'.'
            #print(white(item,bold=True))        
    #print()    
    result=result[:-1]
    #print(yellow(result,bold=True))
    goi=input('OK')
    # ===================================================================
    env.level=env.level[:-1]
    return result
    

#  def_sxo_path***
def sxo_path(path,list,index):
    '''
    MODIFIED : 2025-05-24T10:31:51.000Z

    description : get path of keys in JSON data
    '''
    route="/sxo_path"
    env.level+='-'
    #print()
    #print(env.level,white('def sxo_path() in json_to_dtree_graph.py : >',bold=True))
    #print()
    word_list=path.split('.')
    ii=0
    result=''    
    #print()
    #print(cyan(list))
    #print()    
    for item in word_list:
        ii+=1
        if item=='item':
            result=result+'['+str(list[ii]-1)+']'
            #result=result+'[xx]'
            #print(yellow(f"ii:{ii} item={item} valeur:{list[ii]-1}",bold=True))                        
            #print(yellow(item,bold=True))  
        else:
            result=result+'["'+item+'"]'
            #print(white(item,bold=True))        
    #print()    
    #print(cyan(result,bold=True))
    #goi=input('OK')
    # ===================================================================
    env.level=env.level[:-1]
    return result
    

#  def_icon***
def icon(line,valeur):
    '''
    MODIFIED : 2025-05-24T10:33:10.000Z

    description : Figure out which icon must be displayed into the graph for this entry
    '''
    route="/icon"
    env.level+='-'
    print()
    print(env.level,white('def icon() in json_to_dtree_graph.py : >',bold=True))
    print()
    print(yellow(line))
    line=line.strip()
    #gio=input('OK:')
    if 'workflow'==line:
        icone='img/run.gif'  
        #gio=input('OK:')
    elif 'target_groups' in line:
        icone='img/target_group.gif'          
    elif 'target' in line:
        icone='img/target.gif'         
    elif 'actions'==line:
        icone='img/task.gif' 
    elif 'schedules' in line:
        icone='img/schedule.gif' 
    elif 'calendar' ==line:
        icone='img/schedule.gif'  
    elif 'variable_value_new' in line:
        icone='img/set_variable.gif' 
    elif 'variable' in line:
        icone='img/var_out.gif'         
    elif 'triggers' == line:
        icone='img/alarm.gif'  
    elif 'triggerschedule' in line:
        icone='img/schedule.gif'          
    elif 'subworkflows' in line:
        icone='img/subworkflow.gif' 
    elif 'dependent_workflows' in line:
        icone='img/subworkflow.gif'
    elif 'atomic' in line:
        icone='img/a_atomic.gif'        
    elif 'description' in line:
        icone='img/info.gif' 
    elif 'script' == line:
        icone='img/topic.png' 
    elif 'name' ==line:
        print(yellow(f'valeur : {valeur}',bold=True))
        #gio=input('OK:')
        if valeur=='<u>Execute Python Script</u>':
            icone='img/python.gif' 
        elif valeur=='<u>Condition Block</u>':
            icone='img/if_block.gif' 
        elif valeur=='<u>Set Variables</u>':
            icone='img/set_variable.gif'
        elif valeur=='<u>HTTP Request</u>':
            icone='img/globe.gif'    
        elif valeur=='<u>For Each</u>':
            icone='img/loop.gif'   
        elif valeur=='<u>Completed</u>':
            icone='img/checkbox_no_full.gif'  
        elif valeur=='<u>description</u>':
            icone='img/info.gif'
        elif valeur=='<u>Break</u>':
            icone='img/red_cross.gif'             
        elif valeur=='<u>Parallel Block</u>':
            icone='img/parallel_bloc.gif'    
        elif valeur=='<u>Parallel Branch</u>':
            icone='img/parallel_branch.gif'  
        elif valeur=='<u>While Loop</u>':
            icone='img/while_loop.gif'       
        else:
            icone='' 
    elif 'scope' ==line:
        print(yellow(f'valeur : {valeur}',bold=True))
        #gio=input('OK:')
        if valeur=='input':
            icone='img/input.gif' 
        elif valeur=='output':
            icone='img/output.gif'             
        else:
            icone=''             
    else:
        icone=''
    # ===================================================================
    env.level=env.level[:-1]
    return(icone)
    

#  def_format_description***
def format_description(description):
    '''
    MODIFIED : 2025-05-24T10:34:35.000Z

    description : Format the description field with html tags, string replacement and colors
    '''
    route="/format_description"
    env.level+='-'
    print()
    print(env.level,white('def format_description() in json_to_dtree_graph.py : >',bold=True))
    print()
    #print(description)
    #a=input('STOP 3: ')
    description=description.replace('\\','/')
    if 'generic . ' in description:
        description=description.split('generic . ')[1]
        #a=input('STOP 2: ')
    if 'base_type' in description or 'schema_id' in description or 'object_type' in description or 'is_required' in description or 'display_on_wizard' in description or 'is_invisible' in description or 'persist_output' in description or 'populate_columns' in description or 'skip_execution' in description or 'continue_on_failure' in description or 'basic . category' in description or 'category_type' in description or 'disable_certificate_validation' in description or 'delete_workflow_instance' in description or 'allow_auto_redirect' in description or 'allow_headers_redirect' in description or 'continue_on_error_status_code' in description or 'use_custom_format' in description or 'corejava' in description: 
        description="hidden..."
        #a=input('STOP : ')
    if 'datatype . ' in description:
        description=description.replace('datatype . ','')
    if 'core . ' in description:
        description=description.replace('core . ','')
    if 'logic . ' in description:
        description=description.replace('logic . ','')    
    if 'web-service . http_request' in description:
        description=description.replace('web-service . ','')       
    if '___( CLICK on this link to see object content )' in description:
        description=description.replace('<span style="color:black;font-weight:bolder">','<span style="color:red;font-weight:bolder">')
    if 'workflow . sub_workflow' in description:
        description=description.replace('<span style="color:black;font-weight:bolder">','<span style="color:DarkRed;font-weight:bolder">')
    if 'unique_name' in description:
        description=description.replace('<span style="color:black;font-weight:bolder">','<span style="color:LightBlue;font-weight:bolder">')
    if 'name' in description and '$' not in description:
        description=description.replace('<span style="color:black;font-weight:bolder">','<span style="color:black;background: #CAEFB1;font-weight:bolder">')
    if 'title' in description:
        description=description.replace('<span style="color:black;font-weight:bolder">','<span style="color:#008900;font-weight:bolder">')
    if 'script_arguments' in description:
        description=description.replace('script_arguments','variables sent from workflow to python script')
        description=description.replace('<span style="color:blue;font-weight:bolder">','<span style="color:green;font-weight:bolder">')
    if 'script_query' in description and '_name' in description:
        description=description.replace('script_query_name','Workflow variable')
    if 'script_query' in description and '_type' not in description:
        description=description.replace('script_query','python script variable')
    if 'script_queries' in description and 'activity' not in description:
        description=description.replace('script_queries','Results sent from  python script to workflow')
        description=description.replace('<span style="color:blue;font-weight:bolder">','<span style="color:DarkRed;font-weight:bolder">')
    if 'definition_workflow_' in description:
        string_token=description.split('definition_workflow_')[1]
        string_token=string_token.split('.')[0]
        string_token='definition_workflow_'+string_token
        string_token=string_token.replace('</span>','')
        string_token=string_token.strip()
        print('string_token : ',cyan(string_token,bold=True))
        #print('object_table : ',yellow(object_table['workflows'][string_token],bold=True))
        if string_token in object_table['workflows'].keys():
            print(' -> ',red(object_table['workflows'][string_token],bold=True))
            description=description.replace(string_token,'[ '+object_table['workflows'][string_token]+' ]')
            description=description.replace('$','')
    if 'definition_activity_' in description:
        description=description.replace('$','')
        string_token=description.split('definition_activity_')[1]
        string_token=string_token.split('.')[0]
        string_token='definition_activity_'+string_token
        string_token=string_token.replace('</span>','')
        string_token=string_token.strip()
        print('string_token : ',cyan(string_token,bold=True))        
        if string_token in object_table['activities'].keys():
            print(' -> ',red(object_table['activities'][string_token],bold=True))
            description=description.replace(string_token,'[ '+object_table['activities'][string_token]+' ]')            
    if 'variable_workflow_' in description:
        string_token=description.split('variable_workflow_')[1]
        string_token=string_token.split('.')[0]
        string_token='variable_workflow_'+string_token
        string_token=string_token.replace('</span>','')
        string_token=string_token.strip()
        print('string_token : ',cyan(string_token,bold=True))        
        if string_token in object_table['variables'].keys():
            print(' -> ',red(object_table['variables'][string_token],bold=True))
            description=description.replace(string_token,'[ '+object_table['variables'][string_token]['name']+' ]')
            description=description.replace('$','')
        #sys.exit()
        #a=input('STOP')
    # ===================================================================
    env.level=env.level[:-1]
    return(description)
    

#  def_parse_json***
def parse_json(json_filename,debug):
    '''
    MODIFIED : 2025-05-24T10:36:02.000Z

    description : Main function that parses the JSON file and create the HTML Result
    '''
    route="/parse_json"
    env.level+='-'
    print()
    print(env.level,white('def parse_json() in json_to_dtree_graph.py : >',bold=True))
    print()
    tree=''
    parent_base=0
    parent=1
    child=0
    prefix_lenght=0
    levels=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    level_index=0
    notes_index=0
    nb_levels_items_list=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    levels_items_name_list=["","","","","","","","","","","","","","","","","","","","","","","","","","","",""]
    upper_level=''
    list_of_keywords=["empty list"]
    with open(json_filename, 'rb') as input_file:
        # load json iteratively
        parser = ijson.parse(input_file)
        fichier=open('result.txt','w')
        fichier2=open('tree.txt','w')
        last_dot_count=0
        back=0
        word_list=['end_map','map_key','end_array','start_array','start_map']
        for prefix, event, value in parser:
            print('{},-> {} = {}'.format(prefix, event, value))
            if event not in word_list:
                key_list=prefix.split('.')
                key=key_list[len(key_list)-1]
                if debug:
                    print(red(type(value),bold=True))      
                link=''
                if type(value) is str:
                    if debug:
                        print(red('value count:',bold=True))
                        print(red(value.count('\n'),bold=True))
                    if len(value)<1000 and value.count('\n')==0 and value.count('\r')==0:
                        valeur=value.replace("'","")
                    else:
                        if debug:
                            print(cyan(valeur,bold=True))
                        note_name='./templates/note_'+str(notes_index)+'.html'
                        with open(note_name,'w') as note:
                            note.write('<!DOCTYPE html><html><head><meta charset="utf-8"><title>python script</title><link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/9.2.0/styles/vs.min.css"></head><body><pre class="with-hljs"><code class="lang-py"><b>')
                            note.write(value)
                            note.write('\n\n</b></code></pre><script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/9.2.0/highlight.min.js"></script><script>hljs.initHighlightingOnLoad();</script></body></html>')
                        link='./note_'+str(notes_index)+'.html'
                        link='javascript:popup_window(\'./open_incident_note?description=note_'+str(notes_index)+'.html\', \'note\', 700, 500);'
                        notes_index+=1                        
                        valeur='___( CLICK on this link to see object content )'
                else:
                    valeur=value                      
                    if debug:
                        print('not a string')
                if debug:                        
                    print(yellow(valeur,bold=True))
                line_out='{},-> {} = {}'.format(prefix, key, valeur)                           
                fichier.write(line_out)
                fichier.write("\r")  
                if link=='':
                    #link='no_link1.html'
                    link=''
                parent=levels[level_index]
                str_parent=str(parent)
                if debug:
                    print(red(f"level index ={level_index}",bold=True))
                    print(red(f"parent level line number ={str_parent}",bold=True))
                    print(yellow(levels,bold=True))
                if key=='item':
                    item_index=str(nb_levels_items_list[level_index])
                    nb_levels_items_list[level_index]+=1
                    prefix_nb_items=prefix.count('.')
                    chemin_list=prefix.split('.')
                    if chemin_list[prefix_nb_items-1]=='variables' and chemin_list[prefix_nb_items]=='item':
                        key='variable'
                    if chemin_list[prefix_nb_items-1]=='actions' and chemin_list[prefix_nb_items]=='item':
                        key='action'  
                    if chemin_list[prefix_nb_items-1]=='blocks' and chemin_list[prefix_nb_items]=='item':
                        key='block'                           
                    key=key+item_index                
                if display_path:
                    prefix2='|--------------->'+sxo_path(prefix,nb_levels_items_list,level_index)
                else:
                    prefix2='' 
                if type(valeur)==bool:
                    if valeur:
                        color2='green'
                    else:
                        color2='red'
                else:
                    if valeur=='input':
                        color2='green'
                    elif valeur=='None':
                        color2='grey'
                    elif valeur=='output':
                        color2='red'                           
                    else:
                        color2='black'  
                if key=='name' or key=='display_name':
                    valeur='<u>'+valeur+'</u>'                  
                if type(valeur)==str:              
                    if valeur=='None':
                        valeur=''
                    else:
                        valeur=valeur.replace('.',' . ') 
                        if "secure_string" in valeur:
                            color2='orange'
                        elif "subworkflow" in valeur:
                            color2='red'                                
                if valeur is None:                     
                        valeur=''
                check_key_list=['variable_value_new','variable_to_update']
                if key in check_key_list and valeur=='':
                    color2='red'
                    valeur='Is empty... Is it Realy Missing ?  Check This...'                                    
                if ( key in list_of_keywords or 'item' in key) and valeur: 
                    color2='maroon' 
                else:
                    #color2='grey'
                    color2='maroon'
                icone=icon(key,valeur)
                icone_open=icone  
                if key in list_of_keywords:
                    description='<span style="color:blue;font-weight:bolder"> {}</span> : <span style="color:{};font-weight:bolder">{}</span> {} '.format( key,color2, valeur, prefix2) 
                else:
                    description='<span style="color:grey;font-weight:bolder"> {}</span> : <span style="color:{};font-weight:bolder">{}</span> {} '.format( key,color2, valeur, prefix2)                
                #description='<span style="color:blue;font-weight:bolder"> {}</span> : <span style="color:{};font-weight:bolder">{}</span> {} '.format( key,color2, valeur, prefix2) 
                title='dtree'
                target=''
                if parent==-1:
                    description='JSON Tree'
                description=format_description(description)                    
                line_out2=f"        d.add({parent_base},{str_parent},'{description}',\"{link}\",'{title}','{target}','{icone}','{icone_open}');"
                print(cyan(line_out2,bold=True))
                if debug:
                    gio=input('-- NEW KEY ADDED :')                
                if parent_base!=0:
                    tree=tree+line_out2+'\n'
                    fichier2.write(line_out2)
                    fichier2.write("\r") 
                    print(green('saved *')) 
                else:
                    print(red('dont save'))                    
                parent_base+=1
            else:
                if event == 'start_array' or event == 'start_map':
                    if debug:
                        print(yellow('go to next level ->',bold=True))
                    key_list=prefix.split('.')
                    key=key_list[len(key_list)-1]
                    valeur=value
                    line_out='{},-> {} = {}'.format(prefix, key, valeur)                           
                    fichier.write(line_out)
                    fichier.write("\r")  
                    link='no_link2.html'
                    mota='Levels : '
                    for a in range (0,level_index):
                        mota+=str(levels[a])+' - '
                    print(white(mota,bold=True))
                    the_parent=levels[level_index]
                    str_parent=str(the_parent)
                    if debug:                        
                        print(red(f"level index ={level_index}",bold=True))                    
                        print(red(f"parent level line number ={str_parent}",bold=True)) 
                        print(yellow(levels,bold=True))
                        print(yellow(levels_items_name_list,bold=True))
                    upper_level=prefix   
                    prefix2=prefix
                    if level_index>=len(levels_items_name_list): 
                        print(level_index)
                        print(levels_items_name_list)
                        gio=input('STOP')                    
                    print(levels_items_name_list[level_index])
                    print(key)
                    if levels_items_name_list[level_index]!=key:
                        levels_items_name_list[level_index]=key
                        nb_levels_items_list[level_index]=0                        
                    if key=='item':
                        item_index=str(nb_levels_items_list[level_index])
                        nb_levels_items_list[level_index]+=1  
                        prefix_nb_items=prefix.count('.')                        
                        chemin_list=prefix.split('.')
                        if chemin_list[prefix_nb_items-1]=='variables' and chemin_list[prefix_nb_items]=='item':
                            key='variable'  
                        if chemin_list[prefix_nb_items-1]=='actions' and chemin_list[prefix_nb_items]=='item':
                            key='action' 
                        if chemin_list[prefix_nb_items-1]=='blocks' and chemin_list[prefix_nb_items]=='item':
                            key='block'                             
                        key=key+item_index        
                        prefix2=sxo_path(prefix,nb_levels_items_list,level_index)
                    icone=icon(key,valeur)
                    icone_open=icone                          
                    if parent==-1:
                        description='JSON Tree';  
                    else:                    
                        if display_path:
                            prefix2='|--------------->'+sxo_path(prefix,nb_levels_items_list,level_index)
                        else:
                            prefix2=''
                        if type(valeur)==bool:
                            if valeur:
                                color2='green'
                            else:
                                color2='red'
                        else:
                            if valeur=='input':
                                color2='green'
                            elif valeur=='None':
                                color2='grey'
                            elif valeur=='output':
                                color2='red'                           
                            else:
                                color2='black'
                        if key=='name' or key=='display_name':
                            valeur='<u>'+valeur+'</u>'
                        if type(valeur)==str:
                            if valeur=='None':
                                color2='red'
                                valeur='MISSING ?'
                            else:
                                valeur=valeur.replace('.','  .  ')                                  
                        if valeur is None:
                            valeur=''
                        if key in list_of_keywords:
                            description='<span style="color:blue;font-weight:bolder"> {}</span> : <span style="color:{};font-weight:bolder">{}</span> {} '.format( key,color2, valeur, prefix2) 
                        else:
                            description='<span style="color:grey;font-weight:bolder"> {}</span> : <span style="color:{};font-weight:bolder">{}</span> {} '.format( key,color2, valeur, prefix2)
                    title='dtree'
                    target='' 
                    description=format_description(description)                    
                    line_out2=f"        d.add({parent_base},{str_parent},'{description}','{link}','{title}','{target}','{icone}','{icone_open}');"
                    print(cyan(line_out2,bold=True))
                    if debug:
                        gio=input(' -> NEW CHILD KEY ARRAY ADDED:')
                    if parent_base!=0:
                        tree=tree+line_out2+'\n'
                        fichier2.write(line_out2)
                        fichier2.write("\r")
                        #levels[level_index]+=1
                        if debug:
                            print(green('saved to file',bold=True)) 
                    else:
                        if debug:
                            print(red('dont save'))          
                        else:
                            pass 
                    level_index+=1
                    levels[level_index]=parent_base                     
                    parent_base+=1                    
                    if debug:
                        print(yellow(levels,bold=True))
                        print(yellow(f"new level_index = {level_index}  and value set to {levels[level_index]}",bold=True))                      
                        gio=input('en avant NEXT done >>:')
                if event == 'end_array' or event == 'end_map':
                    back=1
                    nb_levels_items_list[level_index]=0                         
                    if debug:
                        print(yellow(levels,bold=True))
                    if upper_level==prefix:                        
                        level_index-=1
                        if debug:
                            print('level_index equal -1')
                    else:
                        level_index=prefix.count('.')+1
                        if debug:
                            print('count number of dots')                        
                    if debug:
                        print(cyan(f"{prefix} (prefix)",bold=True))
                        print(cyan(f"{upper_level} (upper_level)",bold=True))
                        print(red(levels,bold=True))
                        print(red(f"level_index = {level_index}",bold=True))
                        print(red(f"next parent line = {levels[level_index]}",bold=True))                     
                        gio=input('en arriere BACK done<<:')
        fichier.close()
        fichier2.close()
    # ===================================================================
    env.level=env.level[:-1]
    return(tree)
    

#  def_go_analyse_json***
def go_analyse_json(filename):
    '''
    MODIFIED : 2025-06-02T17:10:40.000Z

    description : analyse json file located in json result and create the tree graph
    '''
    route="/go_analyse_json"
    env.level+='-'
    print()
    print(env.level,white('def go_analyse_json() in json_to_dtree_graph.py : >',bold=True))
    print()
    global text_out_header
    fichier='./json_results/'+filename
    #print(fichier) 
    #tree=parse_json(fichier,debug)
    tree=parse_json_with_path(fichier,debug)
    footer='''
        document.write(d);
        //-->
    </script>
</div>
</body>
</html>
    '''
    
    text_out=text_out_header+tree+footer
    with open('./templates/dtree.html','w') as fich:
        fich.write(text_out)
    # ===================================================================
    env.level=env.level[:-1]
    return text_out
    

#  def_parse_json_with_path***
def parse_json_with_path(json_filename,debug):
    '''
    MODIFIED : 2025-06-03T08:09:54.000Z

    description : read json file , parse it and create dtree, and include key path into the graph
    '''
    route="/parse_json_with_path"
    env.level+='-'
    print('\n'+env.level,white('def parse_json_with_path() in json_to_dtree_graph.py : >',bold=True))
    tree=''
    parent_base=0
    parent=1
    child=0
    prefix_lenght=0
    levels=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    level_index=0
    notes_index=0
    nb_levels_items_list=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    levels_items_name_list=["","","","","","","","","","","","","","","","","","","","","","",]
    upper_level=''
    with open(json_filename, 'rb') as input_file:
        # load json iteratively
        parser = ijson.parse(input_file)
        fichier=open('result.txt','w')
        fichier2=open('tree.txt','w')
        last_dot_count=0
        back=0
        word_list=['end_map','map_key','end_array','start_array','start_map']
        for prefix, event, value in parser:
            # print('{},-> {} = {}'.format(prefix, event, value))
            if event not in word_list:
                key_list=prefix.split('.')
                key=key_list[len(key_list)-1]
                if debug:
                    print(red(type(value),bold=True))      
                link=''
                if type(value) is str:
                    if debug:
                        print(red('value count:',bold=True))
                        print(red(value.count('\n'),bold=True))
                    if len(value)<1000 and value.count('\n')==0 and value.count('\r')==0:
                        valeur=value.replace("'","")
                    else:
                        if debug:
                            print(cyan(valeur,bold=True))
                        note_name='./result/note_'+str(notes_index)+'.txt'
                        notes_index+=1
                        with open(note_name,'w') as note:
                            note.write(value)
                        link='./note_'+str(notes_index)+'.txt'
                        valeur='...( LONG TEXT CONTENT- CLICK ON THIS LINK TO SEE IT )'
                else:
                    valeur=value
                    if debug:
                        print('not a string')
                if debug:                        
                    print(yellow(valeur,bold=True))
                line_out='{},-> {} = {}'.format(prefix, key, valeur)                           
                fichier.write(line_out)
                fichier.write("\r")  
                if link=='':
                    link='link.html'
                parent=levels[level_index]
                str_parent=str(parent)
                if debug:
                    print(red(f"level index ={level_index}",bold=True))
                    print(red(f"parent level line number ={str_parent}",bold=True))
                    print(yellow(levels,bold=True))
                if key=='item':
                    item_index=str(nb_levels_items_list[level_index])
                    nb_levels_items_list[level_index]+=1
                    key=key+item_index
                prefix2=sxo_path(prefix,nb_levels_items_list,level_index)
                description='<span style="color:green;font-weight:bolder">{}</span> = <span style="color:blue;font-weight:bolder">{}</span>  |---------------> {} '.format( key, valeur, prefix2) 
                if parent==-1:
                    description='JSON Tree';                 
                line_out2=f"        d.add({parent_base},{str_parent},'{description}','{link}');"
                # print(cyan(line_out2,bold=True))
                if debug:
                    gio=input('-- NEW KEY ADDED :')                
                if line_out2!="        d.add(0,0,'<span style=\"color:black;font-weight:bolder\"></span> |--------------->  ','');":
                    tree=tree+line_out2+'\n'
                    fichier2.write(line_out2)
                    fichier2.write("\r") 
                    # print(green('saved *')) 
                else:
                    # print(red('dont save'))                    
                    pass
                parent_base+=1
            else:
                if event == 'start_array' or event == 'start_map':
                    if debug:
                        print(yellow('go to next level ->',bold=True))
                    key_list=prefix.split('.')
                    key=key_list[len(key_list)-1]
                    valeur=value
                    line_out='{},-> {} = {}'.format(prefix, key, valeur)                           
                    fichier.write(line_out)
                    fichier.write("\r")  
                    link='link.html'
                    mota='Levels : '
                    for a in range (0,level_index):
                        mota+=str(levels[a])+' - '
                    # print(white(mota,bold=True))
                    the_parent=levels[level_index]
                    str_parent=str(the_parent)
                    if debug:                        
                        print(red(f"level index ={level_index}",bold=True))                    
                        print(red(f"parent level line number ={str_parent}",bold=True)) 
                        print(yellow(levels,bold=True))
                        print(yellow(levels_items_name_list,bold=True))
                    upper_level=prefix   
                    prefix2=prefix
                    # print(levels_items_name_list[level_index])
                    # print(key)
                    #gio=input('STOP')
                    if levels_items_name_list[level_index]!=key:
                        levels_items_name_list[level_index]=key
                        nb_levels_items_list[level_index]=0                        
                    if key=='item':
                        item_index=str(nb_levels_items_list[level_index])
                        nb_levels_items_list[level_index]+=1                        
                        key=key+item_index        
                        prefix2=sxo_path(prefix,nb_levels_items_list,level_index)
                    if parent==-1:
                        description='JSON Tree';  
                    else:
                        description='<span style="color:black;font-weight:bolder">{}</span> |---------------> {} '.format( key, prefix2 ) 
                    line_out2=f"        d.add({parent_base},{str_parent},'{description}','');"
                    # print(cyan(line_out2,bold=True))
                    if debug:
                        gio=input(' -> NEW CHILD KEY ARRAY ADDED:')
                    if line_out2!="        d.add(0,0,'<span style=\"color:black;font-weight:bolder\"></span> |--------------->  ','');":
                        tree=tree+line_out2+'\n'
                        fichier2.write(line_out2)
                        fichier2.write("\r")
                        #levels[level_index]+=1
                        if debug:
                            print(green('saved to file',bold=True)) 
                    else:
                        if debug:
                            print(red('dont save'))          
                        else:
                            pass 
                    level_index+=1
                    levels[level_index]=parent_base                     
                    parent_base+=1                    
                    if debug:
                        print(yellow(levels,bold=True))
                        print(yellow(f"new level_index = {level_index}  and value set to {levels[level_index]}",bold=True))                      
                        gio=input('en avant NEXT done >>:')
                if event == 'end_array' or event == 'end_map':
                    back=1
                    nb_levels_items_list[level_index]=0                         
                    if debug:
                        print(yellow(levels,bold=True))
                    if upper_level==prefix:                        
                        level_index-=1
                        if debug:
                            print('level_index equal -1')
                    else:
                        level_index=prefix.count('.')+1
                        if debug:
                            print('count number of dots')                        
                    if debug:
                        print(cyan(f"{prefix} (prefix)",bold=True))
                        print(cyan(f"{upper_level} (upper_level)",bold=True))
                        print(red(levels,bold=True))
                        print(red(f"level_index = {level_index}",bold=True))
                        print(red(f"next parent line = {levels[level_index]}",bold=True))                     
                        gio=input('en arriere BACK done<<:')
        fichier.close()
        fichier2.close()
        return(tree)
      


