# -*- coding: UTF-8 -*-
# Made By EarthlyEric
# V.0.2.fix1
import urllib,time,sched,smtplib,keepalive,platform,logging
from datetime import datetime
from urllib import request
from bs4 import BeautifulSoup
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from configobj import ConfigObj



config=ConfigObj('./config.ini')
#Mail settings
Mail=config['Mail']

fromac=Mail['from']
fromacpasswd=Mail['from_passwd']
toac=Mail['to']
bst_id=config['id']['id']
st_id=int(bst_id)



def main(msg,id):
    start_id=id
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

           body=f"""
           News URL:{url}
           發布單位:{info_unit.get_text()}
           發布人:{info_person.get_text()}
           發布時間:{info_time.get_text()}
           TYSH News WorkFlow @ReLoad Dev
           """
           
           content.attach(MIMEText(body))

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

           main(msg=title.string,id=id+1)

        except:
            now_typed=datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
            print(f'[{now_typed}][INFO] 10 minutes later,Check for Update')
            time.sleep(600)  
            main(msg="",id=id)



def showinfo(tip, info):
    print("{}:{}".format(tip,info))  



keepalive.keep_alive()

time.sleep(5)

logopath='./logo/logo.txt'
f=open(logopath, 'r')



time.sleep(1)

print('____________________________________________________________________________________________________________')

print(f.read())

print('____________________________________________________________________________________________________________')
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
print('____________________________________________________________________________________________________________')
print('                                                                                                            ')
time.sleep(1)

f.close()

main(msg="",id=6923)
    
    


