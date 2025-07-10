# -*- coding: utf-8 -*-
"""
更新时间：2023/5/1
修改内容：
- 增加 Bark 推送支持（含 icon 图标）
- 改为类静态方法进行推送
- 修复 msgs 拼接逻辑错误
"""

import requests
import os
import re
import json
from time import sleep

requests.urllib3.disable_warnings()

# 初始化环境变量
cs = 0    # 如非青龙运行或不需要变量请改为2
cxt = 10  # 重试等待时间（秒）
ttoken = ""
tuserid = ""
push_token = ""
SKey = ""
QKey = ""
ktkey = ""
bark_key = ""
bark_icon = ""
msgs = ""
datas = ""

if cs == 1:
    if "cs_ssp" in os.environ:
        datas = os.environ.get("cs_ssp")
    else:
        print('您没有输入任何信息')
        exit()
elif cs == 2:
    datas = ""  # 直接运行请填写
else:
    if "fs" in os.environ:
        fs = os.environ.get('fs')
        fss = fs.split("&")
        if "tel" in fss and "ssp_telkey" in os.environ:
            telekeys = os.environ.get("ssp_telkey").split('\n')
            ttoken = telekeys[0]
            tuserid = telekeys[1]
        if "qm" in fss and "ssp_qkey" in os.environ:
            QKey = os.environ.get("ssp_qkey")
        if "stb" in fss and "ssp_skey" in os.environ:
            SKey = os.environ.get("ssp_skey")
        if "push" in fss and "ssp_push" in os.environ:
            push_token = os.environ.get("ssp_push")
        if "kt" in fss and "ssp_ktkey" in os.environ:
            ktkey = os.environ.get("ssp_ktkey")
        if "bark" in fss and "ssp_barkkey" in os.environ:
            bark_key = os.environ.get("ssp_barkkey")
            if "ssp_barkicon" in os.environ:
                bark_icon = os.environ.get("ssp_barkicon")

    if "ssp" in os.environ:
        datas = os.environ.get("ssp")
        if datas == "":
            print('您没有输入任何信息')
            exit()
    else:
        print('您没有输入任何信息')
        exit()

groups = datas.split('\n')

class SspanelQd(object):
    def __init__(self, name, site, username, psw):
        self.name = name
        self.base_url = site
        self.email = username
        self.password = psw
        self.tele_api_url = 'https://api.telegram.org'
        self.tele_bot_token = ttoken
        self.tele_user_id = tuserid

    def checkin(self):
        email = self.email.replace('@', '%40')
        password = self.password
        try:
            session = requests.session()
            session.get(self.base_url, verify=False)

            login_url = self.base_url + '/auth/login'
            headers = {
                'User-Agent': 'Mozilla/5.0',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            }

            post_data = f'email={email}&passwd={password}&code='
            session.post(login_url, post_data.encode(), headers=headers, verify=False)

            headers['Referer'] = self.base_url + '/user'
            response = session.post(self.base_url + '/user/checkin', headers=headers, verify=False)
            msg = response.json().get('msg')
        except:
            return False

        try:
            info_url = self.base_url + '/user'
            response = session.get(info_url, verify=False)
            level = re.findall(r'\["class", "(.*?)"],', response.text)[0]
            day = re.findall(r'\["class_expire", "(.*)"],', response.text)[0]
            rest = re.findall(r'\["unused_traffic", "(.*?)"]', response.text)[0]
            msg = f"- 今日签到信息：{msg}\n- 用户等级：{level}\n- 到期时间：{day}\n- 剩余流量：{rest}"
        except:
            try:
                level = re.findall(r'\["VIP", "(.*?)"],', response.text)[0]
                day = re.findall(r'\["VIP_Time", "(.*)"],', response.text)[0]
                rest = re.findall(r'\["Traffic", \'(.*?)\'],', response.text)[0]
                msg = f"- 今日签到信息：{msg}\n- 用户等级：{level}\n- 到期时间：{day}\n- 剩余流量：{rest}"
            except:
                pass
        return msg

    def main(self):
        global msgs
        msg = self.checkin()
        for i in range(1, 6):
            if msg is False:
                print(f"等待 {cxt} 秒后重试，第 {i}/5 次")
                sleep(cxt)
                msg = self.checkin()
            else:
                break

        if msg is False:
            msg = f"{self.name} 签到失败，可能是网站错误或账号密码问题"
        msgs += f"\n\n✈️ 站点：{self.name}\n👤 用户：{self.email}\n{msg}"
        print(msg)

    # 推送函数们
    @staticmethod
    def kt_send(msg):
        if ktkey == '':
            return
        url = f'https://push.xuthus.cc/send/{ktkey}'
        data = ('签到完成，点击查看详细信息~\n' + str(msg)).encode("utf-8")
        requests.post(url, data=data)

    @staticmethod
    def pushplus_send(msg):
        if push_token == '':
            return
        url = 'http://www.pushplus.plus/send'
        data = {
            "token": push_token,
            "title": "机场签到通知",
            "content": msg
        }
        headers = {'Content-Type': 'application/json'}
        body = json.dumps(data).encode('utf-8')
        requests.post(url, data=body, headers=headers)

    @staticmethod
    def Qmsg_send(msg):
        if QKey == '':
            return
        url = f'https://qmsg.zendee.cn/send/{QKey}'
        data = {'msg': msg}
        requests.post(url, data=data)

    def server_send(self, msg):
        if SKey == '':
            return
        url = f"https://sctapi.ftqq.com/{SKey}.send"
        data = {'text': self.name + "签到通知", 'desp': msg}
        requests.post(url, data=data)

    def tele_send(self, msg: str):
        if self.tele_bot_token == '':
            return
        url = f"{self.tele_api_url}/bot{self.tele_bot_token}/sendMessage"
        data = {
            'chat_id': self.tele_user_id,
            'parse_mode': "Markdown",
            'text': msg
        }
        requests.post(url, data=data)

    @staticmethod
    def bark_send(msg):
        if bark_key == '':
            return
        title = "机场签到通知"
        url = f"https://api.day.app/{bark_key}/{title}/{msg}?icon={bark_icon}"
        try:
            requests.get(url)
        except Exception as e:
            print("Bark 推送失败:", e)


# 主执行流程
i = 0
print("已设置不显示账号密码等信息")
while i < len(groups):
    group = groups[i]
    i += 1
    try:
        site_name, web_site, prof = group.split('|')
    except:
        print("签到信息格式错误")
        continue

    for idx, profile in enumerate(prof.split(';'), start=1):
        try:
            username, pswd = profile.split(',')
        except:
            print(f"账号信息格式错误：{profile}")
            continue

        print(f"✅ 开始签到 - 站点：{site_name}，账号 {idx}")
        run = SspanelQd(site_name, web_site, username, pswd)
        run.main()

# 推送通知
SspanelQd.kt_send(msgs)
SspanelQd.pushplus_send(msgs)
SspanelQd.bark_send(msgs)
