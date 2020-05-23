import requests
from bs4 import BeautifulSoup
import time
import smtplib
from email.mime.text import MIMEText
from email.header import Header

class newNotice(object):
    def __init__(self):
        self.url = 'http://www.cnic.cas.cn/yjsjy/tzgg/'
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"
        }
        self.notice=''

    def get_response(self, url):
        print(url)
        response = requests.get(url)
        data = response.content
        return data
    def data_save(self,data):
            with open('C.html','wb') as file:
                file.write(data)
    def parse_data(self,data):
        soup = BeautifulSoup(data, 'html.parser', from_encoding='gb18030')
        all = soup.find(id="content")
        new_url = self.url+all.a['href']
        print(all.a.text)
        self.notice = all.a.text
        #print(new_url)
        return new_url

    def get_content(self,new_url):
        data = requests.get(new_url).content
        soup = BeautifulSoup(data, 'html.parser', from_encoding='gb18030')
        tim = soup.find('div',class_="info-article").text[6:16]

        #print(tim)

        current_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        #print(current_time)

        if tim.strip() == current_time.strip():
            print("今日有新公告")
            self.notice = self.notice+"今日有新公告"
            self.send_email(self.notice)
        else:
            print("今日没有新公告")
            self.notice = "今日没有新公告"
            self.send_email(self.notice)

    def send_email(self,email_body):
        from_addr = 'XXX@qq.com'
        password = 'XXXX'#这里是QQ邮箱授权码

        # 收信方邮箱
        to_addr = 'XXX@qq.com'

        # 发信服务器
        smtp_server = 'smtp.qq.com'

        # 邮箱正文内容，第一个参数为内容，第二个参数为格式(plain 为纯文本)，第三个参数为编码
        msg = MIMEText(email_body, 'plain', 'utf-8')

        # 邮件头信息
        msg['From'] = Header(from_addr)
        msg['To'] = Header(to_addr)
        msg['Subject'] = Header('newest notice')

        # 开启发信服务，这里使用的是加密传输
        server = smtplib.SMTP_SSL(smtp_server)
        server.connect(smtp_server, 465)
        # 登录发信邮箱
        server.login(from_addr, password)
        # 发送邮件
        server.sendmail(from_addr, to_addr, msg.as_string())
        # 关闭服务器
        server.quit()
    def run(self):
        data = self.get_response(self.url)
        new_url = self.parse_data(data)
        self.get_content(new_url)
newNotice().run()


