# -*- coding: UTF-8 -*-
#!/usr/bin/env python
'''
    description : analyse the log file in ./debug and format it for dtree view
'''
from crayons import *
import sys
import time
from datetime import datetime
import json
import ijson
import os
import env as env

title="debug"
book='log'
debug=0

text_out='''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html>
<head>
    <title>'''+title+'''</title>
    <link rel="StyleSheet" href="../static/dtree.css" type="text/css" />
    <script type="text/javascript" src="../static/dtree.js"></script>
</head>
<body>
<h1>'''+title+'''</h1>
<div class="dtree">
    <p><a href="javascript: d.openAll();">open all</a> | <a href="javascript: d.closeAll();">close all</a></p>
    <script type="text/javascript">
        <!--
        d = new dTree('d');
        d.add(0,-1,'Application Log Tree');        
'''

#  def_main***
def main():
    '''
    MODIFIED : 2025-07-19T14:01:36.000Z

    description : main function
    
    how to call it :
    '''
    route="/main"
    env.level+='-'
    print('\n'+env.level,white('def main() in analyse_application_logs.py : >\n',bold=True))
    #loguer(env.level+' def main() in analyse_application_logs.py : >')
    format_log()
    tree=parse_txt('./debug/parsed.txt',debug)
    footer='''
        document.write(d);
        //-->
    </script>
</div>
</body>
</html>
    '''
    global text_out
    text_out=text_out+tree+footer
    with open('./templates/log.html','w') as fich:
        fich.write(text_out)
    env.level=env.level[:-1]
    return 1
    

#  def_parse_txt***
def parse_txt(filename,debug):
    '''
    MODIFIED : 2025-07-19T14:08:15.000Z

    description : parse the input file and create the dtree html file
    
    how to call it :
    '''
    route="/parse_txt"
    env.level+='-'
    print('\n'+env.level,white('def parse_txt() in analyse_application_logs.py : >\n',bold=True))
    #loguer(env.level+' def parse_txt() in analyse_application_logs.py : >')
    # ===================================================================    
    lnumber=1
    level=0
    last_level=0
    tree=''
    back=0
    levels=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    level_index=0
    notes_index=0 
    fichier=open('result.txt','w')
    fichier2=open('tree.txt','w')    
    with open(filename) as file:
        all_text_content=file.read()
    lines=all_text_content.split('\n')
    parent_base=0
    str_parent=1
    for line in lines:
        nb_comma=line.count(';')
        nb_comma_to_add=4-nb_comma
        for i in range (0,nb_comma_to_add):
            line+=';'
        color=''         
        if ';cnk;' in line:
            color='red'     
        line_list=line.split(';')
        level=line_list[0].count('-')     
        description=line_list[1].replace("'","&lsquo;")
        liste_de_mots=description.split('<<:')
        if '<<col:' in liste_de_mots[0] and color=='':
            col_list=liste_de_mots[0].split('>>')
            color=col_list[0].replace('<<col:','')
            part1='<span style="color:'+color+';font-weight:bolder">'+col_list[1]+' </span>'          
        else:
            if color=='red':
                part1='<span style="color:red;font-weight:bolder"> '+liste_de_mots[0]+' </span>' 
            else:
                part1='<span style="color:blue;font-weight:bolder"> '+liste_de_mots[0]+' </span>'
        if len(liste_de_mots)>1:
            if '<<col:' in liste_de_mots[1]  and color=='':
                col_list=liste_de_mots[1].split('>>')
                color=col_list[0].replace('<<col:','')  
                part2='<span style="color:'+color+';font-weight:bolder">'+col_list[1]+'</span>' 
            else:
                part2='<span style="color:green;font-weight:bolder">'+liste_de_mots[1]+'</span>'
            description='('+str(lnumber)+')'+part1+part2
        else:
            description='('+str(lnumber)+')'+part1
        description='<b>'+description+'<b>'
        #icone=icon(line)
        icone=''
        if '<<url:' in line:
            lien_url=line_list[2].replace("<<url:","")
        elif '<<local_url:' in line:
            lien_url='notes/'+line_list[2].replace("<<local_url:","")            
        elif '<<note:' in line:
            lien_url='notes/'+line_list[2].replace("<<note:","")
        else:
            lien_url=''            
        # print(white(f"Parent -> last level:{last_level}",bold=True))          
        # print(white(f"Current-> level:{level}",bold=True))        
              
        if level==last_level+1:            #NEXT LEVEL
            str_parent=parent_base-1
            if debug:                        
                print(red(f"current level index ={level_index}",bold=True))                    
                print(red(f"parent level line number ={str_parent}",bold=True)) 
                print(red(f"levels before saving line",bold=True))
                print(yellow(levels,bold=True))              
            line_out2=f"        d.add({parent_base},{str_parent},'{description}','{lien_url}','','','{icone}','{icone}');" 
            # print()
            # print(cyan(line_out2,bold=True))  
            # print()
            if levels[level_index]==0:
                levels[level_index]=parent_base-1
            # print(green(f"set levels[{level_index}]to {parent_base}-1 and increment level_index",bold=True))                                  
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
            back=2 # next level
            if debug:
                print(red(f"after saving line",bold=True))       
                print(green(levels,bold=True))                 
                print(red(f"new level index ={level_index}",bold=True)) 
                print()
                gio=input(' -> NEW LEVEL and new key added:') 
                print('---------------------------------------------------next block >')                
        elif level<last_level:              # BACK TO PARENT LEVEL
            level_index=level-1
            str_parent=levels[level_index]
            for ii in range (level,26):
                levels[ii]=0
            if debug:                        
                print(yellow(f"BACK level index ={level_index}",bold=True))                    
                print(yellow(f"BACK parent level line number ={str_parent}",bold=True)) 
                print(yellow(levels,bold=True))              
            line_out2=f"        d.add({parent_base},{str_parent},'{description}','{lien_url}','','','{icone}','{icone}');"  
            # print()
            # print(cyan(line_out2,bold=True))  
            # print()         
            #levels[level_index]=parent_base            
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
            if debug:
                print(yellow(f"Newlevel index ={level_index}",bold=True))                    
                print(yellow(f"New parent level line number ={str_parent}",bold=True)) 
                print(yellow(levels,bold=True))              
                gio=input(' <- GET BACK AND NEW KEY ADDED:') 
                print('---------------------------------------------------next block >')  
            back=1
        elif level==last_level:       # SAME LEVEL - ADD NEW KEY
            # print('SAME LEVEL')
            if back==2:
                #str_parent=parent_base-1
                levels[level_index-1]=str_parent
                # print('back=2 =>  from new level')
            else:
                str_parent=levels[level_index-1]
                # print(f'back={back}')
            #str_parent=levels[level_index-1] 
            back=0
            if debug:                        
                print(red(f"level index ={level_index}",bold=True))                    
                print(red(f"parent level line number ={str_parent}",bold=True)) 
                print(yellow(levels,bold=True))              
            line_out2=f"        d.add({parent_base},{str_parent},'{description}','{lien_url}','','','{icone}','{icone}');" 
            # print()
            # print(cyan(line_out2,bold=True))     
            # print()           
            #levels[level_index]=parent_base   
            level_index=level
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
            if debug:
                print(red(f"level index ={level_index}",bold=True))                    
                print(red(f"parent level line number ={str_parent}",bold=True)) 
                print(red(f"after saving line",bold=True))
                print(yellow(levels,bold=True))             
                gio=input(' <-> SAME LEVEL NEW KEY ADDED:')   
                print('---------------------------------------------------next block >') 
        parent_base+=1                 
        last_level=level
        lnumber+=1
    fichier.close()
    fichier2.close()
    # ===================================================================
    env.level=env.level[:-1]
    return(tree)
    

#  def_icon***
def icon(line):
    '''
    MODIFIED : 2025-07-19T14:16:41.000Z

    description : select the icon at the begining of the line
    
    how to call it :
    '''
    route="/icon"
    env.level+='-'
    print('\n'+env.level,white('def icon() in analyse_application_logs.py : >\n',bold=True))
    loguer(env.level+' def icon() in analyse_application_logs.py : >')
    # ===================================================================    
    if ';!;' in line:
        icone='img/warning2.gif'  
    elif ';q;' in line:
        icone='img/icon_question.gif'  
    elif ';t;' in line:
        icone='img/icon_todo.gif'  
    elif ';error;' in line:
        icone='img/icon_not_active.png'   
    elif ';checknok;' in line:
        icone='img/check_no.gif' 
    elif ';cnk;' in line:
        icone='img/checkbox_no_full.gif'         
    elif ';checkok;' in line:
        icone='img/checkbox_ok.gif' 
    elif ';checkokfull;' in line:
        icone='img/checkbox_ok_full.gif'       
    elif ';checknokfull;' in line:
        icone='img/checkbox_no_full.gif' 
    elif ';cok;' in line:
        icone='img/checkbox_ok_full.gif'         
    elif ';infected;' in line:
        icone='img/trojan.gif'     
    elif ';block;' in line:
        icone='img/red_cross.gif'     
    elif ';allow;' in line:
        icone='img/check_ok_green.gif'  
    elif ';alert;' in line:
        icone='img/alarm.gif'  
    elif ';task;' in line:
        icone='img/task.gif' 
    elif ';connected;' in line:
        icone='img/icon_connected.png'    
    elif ';disconnected;' in line:
        icone='img/icon_disconnected.png'  
    elif ';off;' in line:
        icone='img/icon_unavailable.png'  
    elif ';eth;' in line:
        icone='img/icon_wired.png'   
    elif ';wifi;' in line:
        icone='img/icon_wireless.png'  
    elif ';book;' in line:
        icone='img/book.png' 
    elif ';cmd;' in line:
        icone='img/cmd.png' 
    elif ';python;' in line:
        icone='img/python.gif'   
    elif ';py;' in line:
        icone='img/python.gif' 
    elif ';firefox;' in line:
        icone='img/firefox.gif'   
    elif ';protect;' in line:
        icone='img/protect.gif'
    elif ';if;' in line:
        icone='img/if_block.gif'   
    elif ';loop;' in line:
        icone='img/loop.gif'  
    elif ';http_target;' in line:
        icone='img/http_target.gif'  
    elif ';http;' in line:
        icone='img/http_target.gif'      
    elif ';stop;' in line:
        icone='img/stop.gif' 
    elif ';info;' in line:
        icone='img/info.gif' 
    elif ';del;' in line:
        icone='img/trash.gif'   
    elif ';read;' in line:
        icone='img/topic.png'    
    elif ';start;' in line:
        icone='img/start.gif'     
    elif ';root;' in line:
        icone='img/base.gif'   
    elif ';folder;' in line:
        icone='img/folder.gif'   
    elif ';folderopen;' in line:
        icone='img/folderopen.gif'   
    elif ';node;' in line:
        icone='img/node.gif'    
    elif ';endpoint;' in line:
        icone='img/base.gif'       
    elif ';video;' in line:
        icone='img/youtube.jpg'     
    elif ';globe;' in line:
        icone='img/globe.gif'  
    elif ';vpn;' in line:
        icone='img/anyconnect.jpg'   
    elif ';anyconnect;' in line:
        icone='img/anyconnect.jpg'         
    else:
        icone=''
    # ===================================================================
    env.level=env.level[:-1]
    return(icone)
    

#  def_sxo_path***
def sxo_path():
    '''
    MODIFIED : 2025-07-19T14:20:04.000Z

    description : add JSON path in the resulting line
    
    how to call it :
    '''
    route="/sxo_path"
    env.level+='-'
    print('\n'+env.level,white('def sxo_path() in analyse_application_logs.py : >\n',bold=True))
    loguer(env.level+' def sxo_path() in analyse_application_logs.py : >')
    # ===================================================================    
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
    

#  def_loguer***
def loguer(log):
    '''
    MODIFIED : 2025-07-19T14:38:03.000Z

    description : log when a function or a route is called with start date
    
    how to call it :
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
    MODIFIED : 2025-08-01

    description : read log file and create a formated file
    
    how to call it :
    '''
    route="/format_log"
    env.level+='-'
    print('\n'+env.level,white('def format_log() in analyse_application_logs.py : >\n',bold=True))
    #loguer(env.level+' def format_log() in analyse_application_logs.py : >')
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
                    line=line.replace(': > at','<<: at')
                    if 'route' in line:
                        url=f";<<url:http://localhost:{port}/code_edit?code=route_def_{script}.py&type=route"
                    else:
                        url=f";<<url:http://localhost:{port}/code_edit?code=def_{script}.py&type=function"
                    # print('\n url :',green(url+'\n',bold=True))
                elif '???' in line:
                    line=line.replace('- var','-;')
                    line=line.split(' ???')[0]
                    line.replace(' : ','<<:')
                    line.replace(' = ','<<:')
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
                    line=line.replace(': > at','<<: at')
                    if 'route' in line:
                        url=f";<<url:http://localhost:{port}/code_edit_B?code=route_{script}.py&subdir={subdir}"
                    else:
                        url=f";<<url:http://localhost:{port}/code_edit_B?code=def_{script}.py&subdir={subdir}"       
                    # print('\n url :',green(url+'\n',bold=True))
                file.write('-'+line+url+';;;\n')
    # ===================================================================
    env.level=env.level[:-1]
    return 1
    

if __name__=="__main__":
    print(white("\nstart here : analyse_application_log.py",bold=True))
    main()
    print(cyan('\n================ DONE ==================\n\nEnd of script : analyse_application_log.py',bold=True))    
