# -*- coding: UTF-8 -*-
# Made By EarthlyEric
#For 楊凱鈞,學習歷程檔案
# V.0.3.fix5
#
import time,smtplib,keepalive,platform,os
from datetime import datetime
from colored import fg, bg, attr
from urllib import request
from bs4 import BeautifulSoup
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from configobj import ConfigObj
from string import Template
from pathlib import Path


config=ConfigObj('./config.ini')
#Mail settings
Mail=config['Mail']
fromac=Mail['from']
fromacpasswd=Mail['from_passwd']
toac=Mail['to']
st_id=config['id']['id']
temp_id=config['Temp']['Temp_id']








def main(msg,id):
    start_id=str(id)
    errormsg="The news is not existed!"

    if not msg==errormsg:
        try:
            url=f"http://www.tysh.tyc.edu.tw/ischool/public/news_view/show.php?nid={start_id}"
            headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
            page=request.Request(url,headers=headers)
            page_info=request.urlopen(page).read().decode('utf-8')

            soup=BeautifulSoup(page_info, 'html.parser')
            # debug- >print(soup.prettify())

            title=soup.title
            info_unit=soup.find(id='info_unit')
            info_person=soup.find(id='info_person')
            info_time=soup.find(id='info_time')
           
            now_typea=datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
            print(f'[{now_typea}][INFO] Get {title.string}')

            content=MIMEMultipart()
            content["subject"]=f"【New】-{title.string}"
            content["from"]=f"{fromac}"
            content["to"]=f"{toac}"

            template = Template(Path("./mail-templates/mail-template.html").read_text(encoding="utf-8"))
            body = template.substitute({"url": url,
            "info_unit":info_unit,
            "info_person":info_person,
            "info_time":info_time})
           
            content.attach(MIMEText(body,'html','utf-8'))

            with smtplib.SMTP(host="smtp.gmail.com", port="587") as smtp:
                try:
                    smtp.ehlo()  # 驗證SMTP伺服器
                    smtp.starttls()  # 建立加密傳輸
                    smtp.login(f"{fromac}", f"{fromacpasswd}")  # 登入寄件者gmail
                    smtp.send_message(content)  # 寄送郵件

                    now_typeb=datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
                    print(f"[{now_typeb}][INFO] Send to {toac}, Complete!")
                except Exception as e:
                    now_typec=datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
                    print(f"[{now_typec}][ERROR] Error message: ", e)
            try:
                config_writer=ConfigObj('./config.ini')
                section=config_writer.get( 'Temp' )
                section['Temp_id']=f"{id}"
                config_writer.write()
            except:
                now_typec=datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
                print(f"[{now_typec}][ERROR] Error message: Write Error ")

            main(msg=title.string,id=id+1)

        except Exception as e:
            try:
                config_writer=ConfigObj('./config.ini')
                section=config_writer.get( 'Temp' )
                section['Temp_id']=f"{id}"
                config_writer.write()
            except:
                now_typec=datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
                print(f"[{now_typec}][ERROR] Error message: Write Error ")
            print(e)
            now_typed=datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
            print(f'[{now_typed}][INFO] 10 minutes later,Check for Update')
            time.sleep(600)  
            main(msg="",id=id)



def showinfo(tip, info):
    print("%s{}:{}%s".format(tip,info) % (fg(27), attr(0)))

def slowtype(text, speed, newLine=True): 
        for i in text: 
            print(i, end="", flush=True) 
            time.sleep(speed) 
        if newLine: 
            print()


def setup(temp_id):
    print(f'\33]0;TYSH NEWS WORKFLOW by EarthlyEric6\a', end='', flush=True)
    keepalive.keep_alive()

    time.sleep(5)
    os.system('cls' if os.name == 'nt' else 'clear') #clear cli screen.
    logopath='./logo/logo.txt'
    f=open(logopath, 'r')

    time.sleep(1)

    
    print(f.read())
    print('%s____________________________________________________________________________________________________________%s' % (fg(226), attr(0)))
    slowtype('\nWelcome !', .02, newLine = True)


    print('%s____________________________________________________________________________________________________________%s' % (fg(226), attr(0)))
    print('                                                                                                            ')
    time.sleep(1)
    now_type0=datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
    showinfo("作業系統",platform.platform())
    showinfo('系統版本',platform.version())
    showinfo('作業系統名稱', platform.system())
    showinfo('系統位數', platform.architecture()[0])
    showinfo('CPU 架構', platform.machine())
    showinfo('系統名稱', platform.node())
    showinfo('處理器', platform.processor())
    print(f'Time:{now_type0}')
    print('%s____________________________________________________________________________________________________________%s' % (fg(226), attr(0)))
    print('                                                                                                            ')
    time.sleep(1)

    f.close()

    main(msg="",id=temp_id)

setup(temp_id=temp_id)