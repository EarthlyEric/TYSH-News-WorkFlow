# -*- coding: UTF-8 -*-
# Made By EarthlyEric
# For 楊凱鈞,學習歷程檔案
# V.0.4.hotfix1
#
import time, smtplib, keepalive, platform, sys, json

from datetime import datetime
from colored import fg, bg, attr
from urllib import request
from bs4 import BeautifulSoup
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from configobj import ConfigObj
from string import Template
from pathlib import Path

# 讀取Config
config=ConfigObj('./config.ini')

# 郵件設定
Mail = config['Mail']
fromac = Mail['from']
fromacpasswd = Mail['from_passwd']
toac = Mail['to']


# First Startup ?
string_is_first_startup=config['is_first_startup']['is_first_startup']

if string_is_first_startup == 'True':
    is_first_startup=True
elif string_is_first_startup == 'False':
    is_first_startup=False

# 系統資訊取用
def showinfo(tip, info):
    print("%s{}:{}%s".format(tip,info) % (fg(27), attr(0)))

#美化
def slowtype(text, speed, newLine=True):
        for i in text:
            print(i, end="", flush=True)
            time.sleep(speed)
        if newLine:
            print()


#Main Mail System
def main(msg,input_post_id):
    post_id=str(input_post_id)
    error_msg="The news is not existed!"

    if not msg==error_msg:
        try:
            url=f"http://www.tysh.tyc.edu.tw/ischool/public/news_view/show.php?nid={post_id}"
            #Using PC User Agent
            headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
            page=request.Request(url,headers=headers)
            page_info=request.urlopen(page).read().decode('utf-8')

            soup=BeautifulSoup(page_info, 'html.parser')


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
                with open('save_post_id.json', 'w') as jsonfile:
                    date=dict(save_post_id=post_id)
                    json.dump(date, jsonfile, indent=4)

            except:
                now_typec=datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
                print(f"[{now_typec}][ERROR] Error message: Write Error ")

            main(msg=title.string ,input_post_id=input_post_id+1)

        except Exception as e:
            try:
                with open('save_post_id.json', 'w') as jsonfile:
                    date=dict(save_post_id=post_id)
                    json.dump(date, jsonfile, indent=4)
            except:
                now_typec=datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
                print(f"[{now_typec}][ERROR] Error message: Write Error ")

            print(e)
            now_typed=datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
            print(f'[{now_typed}][INFO] 10 minutes later,Wait for Update')
            time.sleep(600)
            main(msg="",input_post_id=input_post_id)






def startup(load_post_id,input_is_first_up):
    print(f'\33]0;TYSH NEWS WORKFLOW by EarthlyEric6\a', end='', flush=True)

    #Status Serveice
    keepalive.keep_alive()

    #TYSH News Workflow LOGO
    time.sleep(5)
    #clear screen.
    #os.system('cls' if os.name == 'nt' else 'clear')
    logopath='./logo/logo.txt'
    f=open(logopath, 'r')

    time.sleep(1)


    print(f.read())
    f.close()
    #TYSH News Workflow CLI
    print('%s____________________________________________________________________________________________________________%s' % (fg(226), attr(0)))

    slowtype('\nWelcome !', .02, newLine = True)
    slowtype('\nChecking Config...', .02, newLine = True)

    if input_is_first_up==True:
        slowtype('\nThis is a first startup.', .02, newLine = True)

        first_setup_id=input("Please enter the first post id.\n")

        config_writer=ConfigObj('./config.ini')
        section=config_writer.get( 'First_setup_id' )
        section['first_setup_id']=f'{first_setup_id}'
        section2=config_writer.get( 'is_first_statup')
        section2['is_first_statup']='False'
        config_writer.write()
    elif input_is_first_up==False:
        pass



    #System Info Display
    print('%s____________________________________________________________________________________________________________%s' % (fg(226), attr(0)))
    print('                                                                                                            ')
    time.sleep(1)
    now_type0=datetime.now().strftime('%Y-%m-%d %I:%M:%S %p')
    showinfo('System',platform.platform())
    showinfo('64 bit or 32 bit', platform.architecture()[0])
    showinfo('CPU Architecture', platform.machine())
    showinfo('Computer Name', platform.node())
    showinfo('CPU', platform.processor())
    print(f'Time:{now_type0}')
    print('%s____________________________________________________________________________________________________________%s' % (fg(226), attr(0)))
    print('                                                                                                            ')
    time.sleep(1)

    if is_first_startup==True:
        with open('save_post_id.json', 'w') as jsonfile:
            date = dict(save_post_id=first_setup_id)
            json.dump(date, jsonfile, indent=4)
        slowtype('\nGood Bye ! Please Restart.', .02, newLine = True)
        sys.exit()

    elif is_first_startup==False:
        main(msg='',input_post_id=load_post_id)



if is_first_startup==True:
    startup(load_post_id=None,input_is_first_up=True)
elif is_first_startup == False:

    with open('./save_post_id.json') as save_id_json:
        save_id_json_array=json.load(save_id_json)
        save_id=save_id_json_array['save_post_id']

    startup(load_post_id=save_id,input_is_first_up=False)