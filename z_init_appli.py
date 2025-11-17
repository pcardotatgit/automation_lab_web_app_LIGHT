'''
    modification : 20251111
    
    description : initialize the application, create empty files  clean folder
'''
import glob
import os


ok_delete=1


def init_appli():
    with open('./venv/Scripts/activate.bat') as file:
        text_content=file.read()
    text_content=text_content.replace(':END','python app.py\n:END')
    with open('./venv/Scripts/activate.bat','w') as file:
        file.write(text_content)    
    os.remove("a.bat")
    os.remove("b.bat")
    os.remove("c.bat")
    os.remove("d.bat") 
    #os.remove("e.bat")
    with open('a.bat','w') as file:
        file.write('venv\\scripts\\activate')    
    with open('b.bat','w') as file:
        file.write('python app.py')        
    with open('port.txt','w') as file:
        file.write('4000')     
    with open('server_ip_address.txt','w') as file:
        file.write('localhost')           
                
if __name__=="__main__":
    init_appli()    
    print('OK DONE')