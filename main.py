# -*- coding: UTF-8 -*-
# Made By EarthlyEric
# V.0.1
import urllib,time,sched,smtplib,keepalive
from urllib import request
from bs4 import BeautifulSoup
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from configobj import ConfigObj

config = ConfigObj('config.ini')

#Mail settings

mail=config['Mail']
fromac=mail['from']
fromacpasswd=mail['from_passwd']
toac=mail['to']

def main(msg,id):
    start_id=id
    errormsg="The news is not existed!"

    if not msg==errormsg:
        try:
           url = f"http://www.tysh.tyc.edu.tw/ischool/public/news_view/show.php?nid={start_id}"
           headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
           page = request.Request(url,headers=headers)
           page_info = request.urlopen(page).read().decode('utf-8')

           soup = BeautifulSoup(page_info, 'html.parser')
           # debug- >print(soup.prettify())
           title = soup.title
           print(title.string)

           content = MIMEMultipart()
           content["subject"] = f"【New】-{title.string}"
           content["from"] = f"{fromac}"
           content["to"] = f"{toac}"
           content.attach(MIMEText(f"News URL:{url}"))
           with smtplib.SMTP(host="smtp.gmail.com", port="587") as smtp:
               try:
                  smtp.ehlo()  # 驗證SMTP伺服器
                  smtp.starttls()  # 建立加密傳輸
                  smtp.login(f"{fromac}", f"{fromacpasswd}")  # 登入寄件者gmail
                  smtp.send_message(content)  # 寄送郵件
                  print(f"{title.string} Complete!")
               except Exception as e:
                  print("Error message: ", e)

           main(msg=title.string,id=id+1)
        except:
            time.sleep(600)
            print('10 minutes later,check for Update')
            main(msg="",id=id)
    
       


if __name__=="__main__":
    keepalive.keep_alive()
    main(msg="",id=6924)


