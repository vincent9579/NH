# -*- coding: utf-8 -*-
# NHentai機器人 作者:蒼 

from Cang.linepy import *
from Cang.akad.ttypes import LiffViewRequest, LiffContext, LiffChatContext, Operation, Message
from datetime import datetime
from time import sleep
from bs4 import BeautifulSoup
from pixivpy3 import *
from humanfriendly import format_timespan, format_size, format_number, format_length
import time, random, sys, json, codecs, threading, glob, re, string, os, requests, subprocess, six, ast, pytz, urllib, urllib.parse,timeit,atexit
import subprocess
import subprocess as cmd
import os
import pyimgur



CLIENT_ID = "Put your Imgur Clent_ID"
im = pyimgur.Imgur(CLIENT_ID)
session = requests.session()

cookies = {
  "ipb_member_id" : "5244710",
  "ipb_pass_hash" : "970123c351c012a0214e8d160f111d85",
  "igneous" : "ae7a64075"
}

headers = {
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
}

botStart = time.time()
cl = LINE('帳號','密碼')
cl.log("Auth Token : " + str(cl.authToken))
client = cl
print("登入成功")

oepoll = OEPoll(cl)
settingsOpen = codecs.open("temp.json","r","utf-8")
settings = json.load(settingsOpen)
ban = json.load(codecs.open("ban.json", "r", "utf-8"))
AboutMeJSON = json.load(codecs.open("AboutMe.json", "r", "utf-8"))

lineSettings = cl.getSettings()
clProfile = cl.getProfile()
clMID = cl.profile.mid

if clMID not in ban["owners"]:
    ban["owners"].append(clMID)
if "ue4ec027e04365a48fc5e1a0651fc4a08" not in ban["owners"]:
    ban["owners"].append("ue4ec027e04365a48fc5e1a0651fc4a08")

msg_dict = {}
bl = [""]
wait = {
    "pic":False
}

def sendLiff(to, data):
    xyz = LiffChatContext(to)
    xyzz = LiffContext(chat=xyz)
    view = LiffViewRequest('1602289196-4xoE1JEr', xyzz)
    token = client.liff.issueLiffView(view)
    url = 'https://api.line.me/message/v3/share'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer %s' % token.accessToken
    }
    data = {"messages":[data]}
    requests.post(url, headers=headers, data=json.dumps(data))
    
def AboutMe():
    data = AboutMeJSON
    return data

def GcamFlex(Url,title,author,imgURL,illustTags):
    data = {
        "type": "flex",
        "altText": "Pixiv",
        "contents":{
  "type": "bubble",
  "hero": {
    "type": "image",
    "url": imgURL,
    "size": "full",
    "aspectRatio": "20:13",
    "aspectMode": "cover",
    "action": {
      "type": "uri",
      "uri": Url
    }
  },
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": title,
        "weight": "bold",
        "size": "xl"
      },
      {
        "type": "box",
        "layout": "vertical",
        "margin": "lg",
        "spacing": "sm",
        "contents": [
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "作者",
                "color": "#aaaaaa",
                "size": "sm",
                "flex": 1
              },
              {
                "type": "text",
                "text": author,
                "wrap": True,
                "color": "#666666",
                "size": "sm",
                "flex": 5
              }
            ]
          },
          {
            "type": "box",
            "layout": "baseline",
            "spacing": "sm",
            "contents": [
              {
                "type": "text",
                "text": "Tags",
                "color": "#aaaaaa",
                "size": "sm",
                "flex": 1
              },
              {
                "type": "text",
                "text": illustTags,
                "wrap": True,
                "color": "#666666",
                "size": "sm",
                "flex": 5
              }
            ]
          }
        ]
      }
    ]
  },
  "footer": {
    "type": "box",
    "layout": "vertical",
    "spacing": "sm",
    "contents": [
      {
        "type": "button",
        "style": "link",
        "height": "sm",
        "action": {
          "type": "uri",
          "label": "點擊進入Pixiv查看",
          "uri": Url
        }
      },
      {
        "type": "spacer",
        "size": "sm"
      }
    ],
    "flex": 0
    }
    }
    }
    return data

def cTime_to_datetime(unixtime):
    return datetime.datetime.fromtimestamp(int(str(unixtime)[:len(str(unixtime))-3]))
    
def restartBot():
    print ("[ 訊息 ] 機器重啟")
    backupData()
    python = sys.executable
    os.execl(python, python, *sys.argv)
    
def backupData():
    try:
        backup = settings
        f = codecs.open('temp.json','w','utf-8')
        json.dump(backup, f, sort_keys=True, indent=4, ensure_ascii=False)
        backup = ban
        f = codecs.open('ban.json','w','utf-8')
        json.dump(backup, f, sort_keys=True, indent=4, ensure_ascii=False)
        return True
    except Exception as error:
        logError(error)
        return False    
        
def restart_program():
    python = sys.executable
    os.execl(python, python, * sys.argv)
    
def logError(text):
    cl.log("[ 錯誤 ] " + str(text))
    time = datetime.now()
    with open("errorLog.txt","a") as error:
        error.write("\n[%s] %s" % (str(time), text))
        
def sendMessageWithMention(to, mid):
    try:
        aa = '{"S":"0","E":"3","M":'+json.dumps(mid)+'}'
        text_ = '@x '
        cl.sendMessage(to, text_, contentMetadata={'MENTION':'{"MENTIONEES":['+aa+']}'}, contentType=0)
    except Exception as error:
        logError(error)

def NHinfo(sex):
    try:
        time.sleep(1)
        headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
        }
        url='https://nhentai.net/g/{}/'.format(sex)
        nhentaitag=[]
        nhentaiart=[]
        html_body=requests.get(url,headers=headers)
        html_body.encoding='utf-8'
        bs=BeautifulSoup(html_body.text,"html.parser")
        textinfo=bs.find_all("div",{"id":"info"})
        title1=textinfo[0].find('h1').get_text()
        try:
            title2=textinfo[0].find('h2').get_text()
        except:
            title2=" "
        abc=bs.find_all("div",{"class":{"tag-container field-name"}})
        text=bs.find_all("span",{"class":"tags"})
        a_tags = text[2].find_all('a')
        for tag in a_tags:
            text2=tag.get("href")
            x=text2.replace('/tag/','')
            y=x.replace('/','')
            nhentaitag.append(y)
        N=len(nhentaitag)
        tagmsg=""
        for i in range (0,N):
            tagmsg += nhentaitag[i]
            tagmsg +=", "
        try:
            a_art = text[3].find_all('a')
            for art in a_art:
                text2=art.get("href")
                xx=text2.replace('/tag/','')
                yy=xx.replace('/','')
                nhentaiart.append(yy)
                N=len(nhentaiart)
            for i in range (0,N):
                NHartist=nhentaiart[i].replace("artist","")
        except:
            NHartist="查無作者"
        return title1,title2,tagmsg,NHartist
    except:
        return None,None,None,None
    
def NHartist(artist,m):
    try:
        headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
        }
        url='https://nhentai.net/artist/{}/'.format(artist)
        zlist=[]
        html_body=requests.get(url,headers=headers)
        html_body.encoding='utf-8'
        bs=BeautifulSoup(html_body.text,"html.parser")
        text=bs.find_all("div",{"class":"gallery"})
        for x in range(0,m):
            text1=text[x].find("a",{"class":"cover"})
            text2=text1.get("href")
            x=text2.replace('/g/','')
            y=x.replace('/','')
            zlist.append(y)
        return zlist
    except:
        return None
    
def get_latest():
    try:
        time.sleep(1)
        headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
        }
        url='https://nhentai.net/'
        html_body=requests.get(url,headers=headers)
        html_body.encoding='utf-8'
        bs=BeautifulSoup(html_body.text,"html.parser")
        text=bs.find_all("div",{"class":"gallery"})
        text1=text[0].find("a",{"class":"cover"})
        text2=text1.get("href")
        x=text2.replace('/g/','')
        nhlatest=x.replace('/','')
        return nhlatest
    except:
        return None
        
def NHsearch(search,m):
    time.sleep(1)
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    }
    url='https://nhentai.net/search/?q={}'.format(search)
    zlist=[]
    html_body=requests.get(url,headers=headers)
    html_body.encoding='utf-8'
    bs=BeautifulSoup(html_body.text,"html.parser")
    text=bs.find_all("div",{"class":"gallery"})
    for x in range(0,m):
        text1=text[x].find("a",{"class":"cover"})
        text2=text1.get("href")
        x=text2.replace('/g/','')
        y=x.replace('/','')
        zlist.append(y)
    return zlist

def NHtags(sTag,m):
    time.sleep(1)
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    }
    url='https://nhentai.net/tag/{}/'.format(sTag)
    tlist=[]
    html_body=requests.get(url,headers=headers)
    html_body.encoding='utf-8'
    bs=BeautifulSoup(html_body.text,"html.parser")
    text=bs.find_all("div",{"class":"gallery"})
    for x in range(0,m):
        try:
            text1=text[x].find("a",{"class":"cover"})
            text2=text1.get("href")
            x=text2.replace('/g/','')
            y=x.replace('/','')
            tlist.append(y)
        except:
            pass
    return tlist

def NtoEX(exTitle):
    try:
        EX = exTitle
        url = "https://exhentai.org/?f_search={}".format(EX)

        html_body=requests.get(url,headers=headers,cookies=cookies)
        html_body.encoding='utf-8'
        bs=BeautifulSoup(html_body.text,"html.parser")
        textinfo=bs.find_all("td",{"class":"gl3c glname"})
        a_tags = textinfo[0].find_all('a')
        for tag in a_tags:
            text2=tag.get("href")
        return text2
    except:
        errrror="錯誤"
        return errrror
    
def EXtoN(ExUrl):
    try:
        html_body=requests.get(ExUrl,headers=headers,cookies=cookies)
        html_body.encoding='utf-8'
        bs=BeautifulSoup(html_body.text,"html.parser")
        gdd=bs.find("h1",{"id":"gn"}).get_text()
        url='https://nhentai.net/search/?q={}'.format(gdd)
        zlist=[]
        html_body=requests.get(url,headers=headers)
        html_body.encoding='utf-8'
        bs=BeautifulSoup(html_body.text,"html.parser")
        text=bs.find_all("div",{"class":"gallery"})
        for x in range(0,1):
            text1=text[x].find("a",{"class":"cover"})
            text2=text1.get("href")
            x=text2.replace('/g/','')
            y=x.replace('/','')
            zlist.append(y)
        return zlist
    except:
        return None
    
def PixivSearch(PixivID):
    try:
        api = AppPixivAPI()
        api.login("vincent9579@gmail.com", "KK95799579")   # Not required
        Url = "https://www.pixiv.net/en/artworks/{}".format(PixivID)
        json_result = api.illust_detail(PixivID)
        illust = json_result.illust
        title = illust.title
        author = illust.user['name']
        imgURL = "https://pixiv.cat/{}.jpg".format(PixivID)
        Tags = illust.tags
        illustTags = ""
        for Tag in Tags:
            illustTags += "#" + Tag['name']
            illustTags += " "
        return Url,title,author,imgURL,illustTags
    except:
        return None,None,None,None,None
        
def saucenao(photo_url):
    try:
        url="https://saucenao.com/search.php"
        #url = "https://saucenao.com"
        Header = {
            'Host': 'saucenao.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36 Edg/83.0.478.61',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept - Language': 'zh-TW,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Accept - Encoding': 'gzip, deflate, br',
            'Connection': 'keep - alive'

        }
        payloaddata = {

            'frame': 1,
            'hide': 0,
            'database': 999,
        }
        #files = {"file": "file": ('saber.jpg', open("saber.jpg", "rb", , "image/png")}
        photo_file=requests.get(photo_url)
        files = {"file": (
        "saucenao.jpg", photo_file.content, "image/png")}
        print("正在搜尋...")
        r = session.post(url=url, headers=Header, data=payloaddata,files=files)
        #r = session .get(url=url,headers=Header)
        soup = BeautifulSoup(r.text, 'html.parser')
        #print(soup.prettify())
        result=0
        choice=0
        for img in soup.find_all('div', attrs={'class': 'result'}):  # 找到class="wrap"的div里面的所有<img>标签
            #print(img)
            if('hidden' in str(img['class']))==False:
                try:
                    name=img.find("div",attrs={'class': 'resulttitle'}).get_text()
                    img_url=str(img.img['src'])
                    describe_list=img.find("div",attrs={'class': 'resultcontentcolumn'})
                    url_list = img.find("div", attrs={'class': 'resultcontentcolumn'}).find_all("a",  attrs={'class': 'linkify'})
                    similarity = str(img.find("div", attrs={'class': 'resultsimilarityinfo'}).get_text())
                    print(name)
                except:
                    continue
                try:
                    describe = str(url_list[0].previous_sibling.string)
                    describe_id = str(url_list[0].string)
                    describe_url = str(url_list[0]['href'])
                    auther_url = str(url_list[1]['href'])
                    auther = str(url_list[1].previous_sibling.string)
                    auther_id = str(url_list[1].string)
                    '''print(name)
                    print(img_url)
                    print(describe)
                    print(describe_id)
                    print(similarity)
                    print(auther)
                    print(auther_id)
                    print(describe_url)'''
                    text = f"{name}\n{describe}[{describe_id}]({describe_url})\n{auther}:[{auther_id}]({auther_url})\n相似度{similarity}"
                except:
                    '''print(describe_list.get_text())
                    print(describe_list.strong.string)
                    print(describe_list.strong.next_sibling.string)
                    print(describe_list.small.string)
                    print(describe_list.small.next_sibling.next_sibling.string)'''
                    auther = str(describe_list.strong.string)
                    auther_id = str(describe_list.strong.next_sibling.string)
                    describe = str(describe_list.small.string) + "\n" + str(describe_list.small.next_sibling.next_sibling.string)
                    text = f"{name}\n{auther}:{auther_id}\n{describe}\n相似度{similarity}"

                photo_file = session.get(img_url)
                

                result=1
                return text
        if result==0:
            text="SauceNAO:找無圖片"
            return text
    except:
        texts="SauceNAO:錯誤"
        return texts

def ascii2d(photo_url):
    try:
        url = "https://ascii2d.net/"
        texts=[]
        # url = "https://saucenao.com"
        Header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36 Edg/83.0.478.61'
        }
        html = session.get(url, headers=Header)
        print(html)
        authenticity_token = re.findall("<input type=\"hidden\" name=\"authenticity_token\" value=\"(.*?)\" />", html.text, re.S)[0]
        payloaddata = {

            'authenticity_token':"" 
            ,
            'utf8': "✓",
        }
        # files = {"file": "file": ('saber.jpg', open("saber.jpg", "rb", , "image/png")}
        print("正在搜索ascii2d")
        photo_file = requests.get(photo_url)
        files = {"file": (
            "saucenao.jpg", photo_file.content, "image/png")}
        url = "https://ascii2d.net/search/multi"
        r = session.post(url=url, headers=Header, data=payloaddata, files=files)
        soup = BeautifulSoup(r.text, 'html.parser')
        # print(soup.prettify())
        pan = 0
        for img in soup.find_all('div', attrs={'class': 'row item-box'}):  # 找到class="wrap"的div里面的所有<img>标签
            # print(img)
            if pan != 0:
                img_url = "https://ascii2d.net" + str(img.img['src'])
                the_list = img.find_all('a')
                title = str(the_list[0].get_text())
                title_url = str(the_list[0]["href"])
                auther = str(the_list[1].get_text())
                auther_url = str(the_list[1]["href"])

                photo_file = session.get(img_url)
                text=f"標題:[{title}]({title_url})\n作者:[{auther}]({auther_url})"
                texts.append(text)
            pan = pan + 1
            if pan == 3:
                break
        return texts
    except:
        texts = "Ascii2D找無圖片"
        return texts
          
def helpmessage():
    helpMessage = """«專屬指令表»
⇒【help】幫助
⇒【sp】 速度
⇒【Un number】 收回最近n則訊息
⇒【pixiv:number】 
  ⇒搜尋P站數字編號
⇒【nh:number】 
  ⇒搜尋數字編號
⇒【ex:url】 
  ⇒Ex轉N站功能 url填入Ex網址
⇒【搜尋:內容:搜尋數量】 
  ⇒在N站搜尋該內容相關本子，最多10個
⇒【作者:作者名:數量】 
  ⇒在N站搜尋該作者相關本子，最多10個
⇒【Tag:標籤名:搜尋數量】 
  ⇒在N站搜尋該標籤本子，最多10個
  ※Tag如有空格請用-代替
⇒【nh最新】 
  ⇒顯示目前編號最後的本子
⇒【Nh隨機 或 NHr】 
  ⇒隨機本子抽抽樂(範圍1~目前最新的編號)
⇒【ft 或 運勢】 很普通的運勢系統OuO
⇒【about】 關於機器人
⇒【runtime】 運行時間
⇒【圖搜】 圖搜
⇒【nh=bye】 退出群組
  ※符號為半形
  ※Tag如有空格請用-代替
  ※Pixiv暫時不支援網址
  ※有時EX網址會顯示錯誤
⇒Credits By.蒼"""

    return helpMessage
    
def lineBot(op):
    try:
        if op.type == 0:
            return
        if op.type == 5:
            contact = cl.getContact(op.param1)
            print ("[ 5 ] 通知添加好友 名字: " + contact.displayName)
            if settings["autoAdd"] == True:
                cl.findAndAddContactsByMid(op.param1)
                cl.sendMessage(op.param1, "感謝你加我好友".format(str(contact.displayName)))
                cl.sendMessage(op.param1, "^_^")
        if op.type == 13:
            contact1 = cl.getContact(op.param2)
            contact2 = cl.getContact(op.param3)
            group = cl.getGroup(op.param1)
            if clMID in op.param3:
                if settings["autoJoin"] == True:
                    try:
                        cl.acceptGroupInvitation(op.param1)
                        cl.sendMessage(op.param1, "此為 NHentai機器人\n方便各位紳士查本\n輸入help可以查詢指令")
                    except Exception as error:
                        print(error)
        if op.type == 19:
            contact1 = cl.getContact(op.param2)
            group = cl.getGroup(op.param1)
            contact2 = cl.getContact(op.param3)
            print ("[19]有人把人踢出群組 群組名稱: " + str(group.name) + "\n" + op.param1 +"\n踢人者: " + contact1.displayName + "\nMid:" + contact1.mid + "\n被踢者: " + contact2.displayName + "\nMid:" + contact2.mid )
        if op.type == 1:
            print ("[1]更新配置文件")
        if op.type == 26 or op.type == 25:
            msg = op.message
            text = msg.text
            msg_id = msg.id
            receiver = msg.to
            sender = msg._from
            if msg.toType == 0:
                if sender != cl.profile.mid:
                    to = sender
                else:
                    to = receiver
            else:
                to = receiver
            if sender != cl.profile.mid:
                if text.lower() == 'help':
                    helpMessage = helpmessage()
                    cl.sendMessage(to, str(helpMessage))
                elif text.lower() == 'sp':
                    t1 = time.time()
                    cl.sendMessage(to,"測速中>...")
                    t2 = time.time() - t1
                    cl.sendMessage(to, "結果：速度為\n%s 秒" %t2)
                elif text.lower().startswith("un "):
                    sep = text.split(" ")
                    args = text.replace(sep[0] + " ","")
                    mes = int(sep[1])
                    #try:
                        #mes = int(args[1])
                    #except:
                        #mes = 1
                    M = cl.getRecentMessagesV2(to, 1001)
                    MId = []
                    for ind,i in enumerate(M):
                        if ind == 0:
                            pass
                        else:
                            if i._from == cl.profile.mid:
                                MId.append(i.id)
                                if len(MId) == mes:
                                    break
                    def unsMes(id):
                        cl.unsendMessage(id)
                    for i in MId:
                        thread1 = threading.Thread(target=unsMes, args=(i,))
                        thread1.daemon = True
                        thread1.start()
                        thread1.join()
                        
                if text.lower().startswith("pixiv:"):
                    PixivID = text.lower().replace("pixiv:","")                    
                    try:
                        
                        Url,title,author,imgURL,illustTags = PixivSearch(PixivID)
                        if Url == None:
                            cl.sendMessage(to,"發生錯誤，可能是輸錯編號了><")
                        else:
                            data = GcamFlex(Url,title,author,imgURL,illustTags)
                            sendLiff(to, data)
                            msg = "網址:\n"
                            msg += "{}".format(Url)
                            msg += "\n========================"
                            msg += "\n標題:\n{}".format(title)
                            msg += "\n========================"
                            msg += "\nTag:\n{}".format(illustTags)
                            msg += "\n========================"
                            msg += "\n作家:{}".format(author)
                            msg += "\n========================"
                            msg += "\n圖片網址:{}".format(imgURL)
                            cl.sendMessage(to,msg)
                    except Exception as e:
                        print(e)
                        
                        cl.sendMessage(to,"發生錯誤，可能是輸錯編號了><，已將錯誤回報")
                        
                if text.lower().startswith("pixiv："):
                    PixivID = text.lower().replace("pixiv：","")                    
                    try:
                        
                        Url,title,author,imgURL,illustTags = PixivSearch(PixivID)
                        if Url == None:
                            cl.sendMessage(to,"發生錯誤，可能是輸錯編號了><")
                        else:
                            data = GcamFlex(Url,title,author,imgURL,illustTags)
                            sendLiff(to, data)
                            msg = "網址:\n"
                            msg += "{}".format(Url)
                            msg += "\n========================"
                            msg += "\n標題:\n{}".format(title)
                            msg += "\n========================"
                            msg += "\nTag:\n{}".format(illustTags)
                            msg += "\n========================"
                            msg += "\n作家:{}".format(author)
                            msg += "\n========================"
                            msg += "\n圖片網址:{}".format(imgURL)
                            cl.sendMessage(to,msg)
                    except Exception as e:
                        print(e)
                        
                        cl.sendMessage(to,"發生錯誤，可能是輸錯編號了><，已將錯誤回報")
                if text.lower().startswith("ex:"):
                    ExUrl = text.lower().replace("ex:","")
                    textEx = EXtoN(ExUrl)
                    if len(textEx) == 0:
                        cl.sendMessage(to,"此本N站沒有喔QQ")
                    else:
                        try:
                            sex = int(textEx[0])
                            nhname,nhname1,nhtag,nhart = NHinfo(sex)
                            if nhname == None:
                                cl.sendMessage(to,"錯誤")
                            else:
                                msg = "網址:\n"
                                msg += "https://nhentai.net/g/{}/ ".format(sex)
                                msg += "\n{}".format(ExUrl)
                                msg += "\nEx免登入: {}".format(ExUrl.replace("exhentai.org","hentai.bang.cf"))
                                msg += "\n========================"
                                msg += "\n名稱:\n{}\n\n{}".format(nhname,nhname1)
                                msg += "\n========================"
                                msg += "\nTag:\n{}".format(nhtag)
                                msg += "\n========================"
                                msg += "\n作家:{}".format(nhart)
                                cl.sendMessage(to,msg)
                        except Exception as e:
                            print(e)
                            
                            cl.sendMessage(to,"發生錯誤，可能是輸錯網址了><，已將錯誤回報")
                        
                if text.lower().startswith("ex："):
                    ExUrl = text.lower().replace("ex：","")
                    textEx = EXtoN(ExUrl)
                    if len(textEx) == 0:
                        cl.sendMessage(to,"此本N站沒有喔QQ")
                    else:
                        try:
                            sex = int(textEx[0])
                            nhname,nhname1,nhtag,nhart = NHinfo(sex)
                            if nhname == None:
                                cl.sendMessage(to,"錯誤")
                            else:
                                msg = "網址:\n"
                                msg += "https://nhentai.net/g/{}/ ".format(sex)
                                msg += "\n{}".format(ExUrl)
                                msg += "\nEx免登入: {}".format(ExUrl.replace("exhentai.org","hentai.bang.cf"))
                                msg += "\n========================"
                                msg += "\n名稱:\n{}\n\n{}".format(nhname,nhname1)
                                msg += "\n========================"
                                msg += "\nTag:\n{}".format(nhtag)
                                msg += "\n========================"
                                msg += "\n作家:{}".format(nhart)
                                cl.sendMessage(to,msg)
                        except Exception as e:
                            print(e)
                            
                            cl.sendMessage(to,"發生錯誤，可能是輸錯網址了><，已將錯誤回報")
                            
                if text.lower().startswith("nh:"):
                    sex = text.lower().replace("nh:","")
                    try:
                        cl.sendMessage(to,"正在尋找...")
                        try:
                            sex = int(sex)
                            
                            nhname,nhname1,nhtag,nhart = NHinfo(sex)
                            if nhname == None:
                                cl.sendMessage(to,"錯誤")
                            else:
                                ExUrl = NtoEX(nhname)
                                msg = "網址:\n"
                                msg += "https://nhentai.net/g/{}/ ".format(sex)
                                msg += "\n{}".format(ExUrl)
                                msg += "\nEx免登入: {}".format(ExUrl.replace("exhentai.org","hentai.bang.cf"))
                                msg += "\n========================"
                                msg += "\n名稱:\n{}\n\n{}".format(nhname,nhname1)
                                msg += "\n========================"
                                msg += "\nTag:\n{}".format(nhtag)
                                msg += "\n========================"
                                msg += "\n作家:{}".format(nhart)
                                cl.sendMessage(to,msg)
                        except:
                            cl.sendMessage(to,"錯誤")
                    except Exception as e:
                        print(e)
                        
                        cl.sendMessage(to,"發生錯誤，可能是輸錯數字了><，已將錯誤回報")
                elif text.lower().startswith("nh："):
                    sex = text.lower().replace("nh：","")
                    try:
                        cl.sendMessage(to,"正在尋找...")
                        try:
                            sex = int(sex)
                            
                            nhname,nhname1,nhtag,nhart = NHinfo(sex)
                            if nhname == None:
                                cl.sendMessage(to,"錯誤")
                            else:
                                ExUrl = NtoEX(nhname)
                                msg = "網址:\n"
                                msg += "https://nhentai.net/g/{}/ ".format(sex)
                                msg += "\n{}".format(ExUrl)
                                msg += "\nEx免登入: {}".format(ExUrl.replace("exhentai.org","hentai.bang.cf"))
                                msg += "\n========================"
                                msg += "\n名稱:\n{}\n\n{}".format(nhname,nhname1)
                                msg += "\n========================"
                                msg += "\nTag:\n{}".format(nhtag)
                                msg += "\n========================"
                                msg += "\n作家:{}".format(nhart)
                                cl.sendMessage(to,msg)
                        except:
                            cl.sendMessage(to,"錯誤")
                    except Exception as e:
                        print(e)
                        
                        cl.sendMessage(to,"發生錯誤，可能是輸錯數字了><，已將錯誤回報")
                elif text.lower().startswith("搜尋:"):
                    search = text.lower().replace("搜尋:","")
                    listlens = search.split(":")
                    n = listlens[1]
                    if n.isdigit() == False:
                        m=3
                    elif n.isdigit() == True:
                        m=int(n)
                        if m >= 10:
                            m = 10
                    NHlist=[]
                    try:
                        NHlist = NHsearch(listlens[0],m)
                        cl.sendMessage(to,"正在尋找...")
                        for i in range(0,m):
                            sex = int(NHlist[i])
                            nhname,nhname1,nhtag,nhart = NHinfo(sex)
                            ExUrl = NtoEX(nhname)
                            msg=""
                            msg += "網址:\n"
                            msg += "https://nhentai.net/g/{}/ ".format(sex)
                            msg += "\n{}".format(ExUrl)
                            msg += "\nEx免登入: {}".format(ExUrl.replace("exhentai.org","hentai.bang.cf"))
                            msg += "\n========================"
                            msg += "\n名稱:\n{}\n\n{}".format(nhname,nhname1)
                            msg += "\n========================"
                            msg += "\nTag:\n{}".format(nhtag)
                            msg += "\n========================"
                            msg += "\n作家:{}".format(nhart)
                            cl.sendMessage(to,msg)
                    except Exception as e:
                        print(e)
                        
                        cl.sendMessage(to,"錯誤，已將錯誤代碼回報")
                elif text.lower().startswith("作者:"):
                    artist = text.lower().replace("作者:","")
                    listlens = artist.split(":")
                    n = listlens[1]
                    if n.isdigit() == False:
                        m=3
                    elif n.isdigit() == True:
                        m=int(n)
                        if m >= 10:
                            m = 10
                    NHlist=[]
                    if listlens[0] not in NHAllartists:
                        cl.sendMessage(to,"查無此作者")
                    else:
                        try:
                            NHlist = NHartist(listlens[0],m)
                            cl.sendMessage(to,"正在尋找...")
                            for i in range(0,m):
                                sex = int(NHlist[i])
                                nhname,nhname1,nhtag,nhart = NHinfo(sex)
                                ExUrl = NtoEX(nhname)
                                msg=""
                                msg += "網址:\n"
                                msg += "https://nhentai.net/g/{}/ ".format(sex)
                                msg += "\n{}".format(ExUrl)
                                msg += "\nEx免登入: {}".format(ExUrl.replace("exhentai.org","hentai.bang.cf"))
                                msg += "\n========================"
                                msg += "\n名稱:\n{}\n\n{}".format(nhname,nhname1)
                                msg += "\n========================"
                                msg += "\nTag:\n{}".format(nhtag)
                                msg += "\n========================"
                                msg += "\n作家:{}".format(nhart)
                                cl.sendMessage(to,msg)
                        except Exception as e:
                            print(e)
                            
                            cl.sendMessage(to,"錯誤，已將錯誤代碼回報")
                elif text.lower().startswith("搜尋："):
                    search = text.lower().replace("搜尋：","")
                    listlens = search.split("：")
                    n = listlens[1]
                    if n.isdigit() == False:
                        m=3
                    elif n.isdigit() == True:
                        m=int(n)
                        if m >= 10:
                            m = 10
                    NHlist=[]
                    try:
                        NHlist = NHsearch(listlens[0],m)
                        cl.sendMessage(to,"正在尋找...")
                        for i in range(0,m):
                            sex = int(NHlist[i])
                            nhname,nhname1,nhtag,nhart = NHinfo(sex)
                            ExUrl = NtoEX(nhname)
                            msg=""
                            msg += "網址:\n"
                            msg += "https://nhentai.net/g/{}/ ".format(sex)
                            msg += "\n{}".format(ExUrl)
                            msg += "\nEx免登入: {}".format(ExUrl.replace("exhentai.org","hentai.bang.cf"))
                            msg += "\n========================"
                            msg += "\n名稱:\n{}\n\n{}".format(nhname,nhname1)
                            msg += "\n========================"
                            msg += "\nTag:\n{}".format(nhtag)
                            msg += "\n========================"
                            msg += "\n作家:{}".format(nhart)
                            cl.sendMessage(to,msg)
                    except Exception as e:
                        print(e)
                        
                        cl.sendMessage(to,"錯誤，已將錯誤代碼回報")
                elif text.lower().startswith("作者："):
                    artist = text.lower().replace("作者：","")
                    listlens = artist.split("：")
                    n = listlens[1]
                    if n.isdigit() == False:
                        m=3
                    elif n.isdigit() == True:
                        m=int(n)
                        if m >= 10:
                            m = 10
                    NHlist=[]
                    if listlens[0] not in NHAllartists:
                        cl.sendMessage(to,"查無此作者")
                    else:
                        try:
                            NHlist = NHartist(listlens[0],m)
                            cl.sendMessage(to,"正在尋找...")
                            for i in range(0,m):
                                sex = int(NHlist[i])
                                nhname,nhname1,nhtag,nhart = NHinfo(sex)
                                ExUrl = NtoEX(nhname)
                                msg=""
                                msg += "網址:\n"
                                msg += "https://nhentai.net/g/{}/ ".format(sex)
                                msg += "\nEx免登入: {}".format(ExUrl.replace("exhentai.org","hentai.bang.cf"))
                                msg += "\n{}".format(ExUrl)
                                msg += "\n========================"
                                msg += "\n名稱:\n{}\n\n{}".format(nhname,nhname1)
                                msg += "\n========================"
                                msg += "\nTag:\n{}".format(nhtag)
                                msg += "\n========================"
                                msg += "\n作家:{}".format(nhart)
                                cl.sendMessage(to,msg)
                        except Exception as e:
                            print(e)
                            
                            cl.sendMessage(to,"錯誤，已將錯誤代碼回報")
                elif text.lower().startswith("tag:"):
                    sTag = text.lower().replace("tag:","")
                    listlens = sTag.split(":")
                    n = listlens[1]
                    if n.isdigit() == False:
                        m=3
                    elif n.isdigit() == True:
                        m=int(n)
                        if m >= 10:
                            m = 10
                    NHlist=[]
                    if listlens[0] not in NHAllTags:
                        cl.sendMessage(to,"查無該Tag")
                    else:
                        try:
                            cl.sendMessage(to,"正在尋找...")
                            NHlist = NHtags(listlens[0],m)
                            for i in range(0,m): 
                                sex = int(NHlist[i])
                                nhname,nhname1,nhtag,nhart = NHinfo(sex)
                                ExUrl = NtoEX(nhname)
                                msg=""
                                msg += "網址:\n"
                                msg += "https://nhentai.net/g/{}/ ".format(sex)
                                msg += "\n{}".format(ExUrl)
                                msg += "\nEx免登入: {}".format(ExUrl.replace("exhentai.org","hentai.bang.cf"))
                                msg += "\n========================"
                                msg += "\n名稱:\n{}\n\n{}".format(nhname,nhname1)
                                msg += "\n========================"
                                msg += "\nTag:\n{}".format(nhtag)
                                msg += "\n========================"
                                msg += "\n作家:{}".format(nhart)
                                cl.sendMessage(to,msg)
                        except Exception as e:
                            print(e)
                            
                            cl.sendMessage(to,"錯誤，已將錯誤代碼回報")
                elif text.lower().startswith("tag："):
                    sTag = text.lower().replace("tag：","")
                    listlens = sTag.split("：")
                    n = listlens[1]
                    if n.isdigit() == False:
                        m=3
                    elif n.isdigit() == True:
                        m=int(n)
                        if m >= 10:
                            m = 10
                    NHlist=[]
                    if listlens[0] not in NHAllTags:
                        cl.sendMessage(to,"查無該Tag")
                    else:
                        try:
                            cl.sendMessage(to,"正在尋找...")
                            NHlist = NHtags(listlens[0],m)
                            for i in range(0,m): 
                                sex = int(NHlist[i])
                                nhname,nhname1,nhtag,nhart = NHinfo(sex)
                                ExUrl = NtoEX(nhname)
                                msg=""
                                msg += "網址:\n"
                                msg += "https://nhentai.net/g/{}/ ".format(sex)
                                msg += "\n{}".format(ExUrl)
                                msg += "\nEx免登入: {}".format(ExUrl.replace("exhentai.org","hentai.bang.cf"))
                                msg += "\n========================"
                                msg += "\n名稱:\n{}\n\n{}".format(nhname,nhname1)
                                msg += "\n========================"
                                msg += "\nTag:\n{}".format(nhtag)
                                msg += "\n========================"
                                msg += "\n作家:{}".format(nhart)
                                cl.sendMessage(to,msg)
                        except Exception as e:
                            print(e)
                            
                            cl.sendMessage(to,"錯誤，已將錯誤代碼回報")
                            
                elif msg.text.lower()=="nh最新":

                    try:
                        sex=get_latest()
                        sex = int(sex)
                        cl.sendMessage(to,"正在尋找...")
                        nhname,nhname1,nhtag,nhart = NHinfo(sex)
                        ExUrl = NtoEX(nhname)
                        msg = "網址:\n"
                        msg += "https://nhentai.net/g/{}/ ".format(sex)
                        msg += "\n{}".format(ExUrl)
                        msg += "\nEx免登入: {}".format(ExUrl.replace("exhentai.org","hentai.bang.cf"))
                        msg += "\n========================"
                        msg += "\n名稱:\n{}\n\n{}".format(nhname,nhname1)
                        msg += "\n========================"
                        msg += "\nTag:\n{}".format(nhtag)
                        msg += "\n========================"
                        msg += "\n作家:{}".format(nhart)
                        cl.sendMessage(to,msg)
                    except Exception as e:
                        print(e)
                        
                        cl.sendMessage(to,"錯誤，已將錯誤代碼回報")
                        
                elif msg.text in ['Nh隨機','NH隨機','nh隨機','nhrandom','Nhrandom','NHrandom','Nhr','NHr','NHR','nhr']:

                    try:
                        cl.sendMessage(to,"正在尋找...")
                        latestnum=get_latest()
                        xyz = int(latestnum)                        
                        sex = random.randint(1,xyz+1)
                        nhname,nhname1,nhtag,nhart = NHinfo(sex)
                        ExUrl = NtoEX(nhname)
                        msga = "網址:\n"
                        msga += "https://nhentai.net/g/{}/ ".format(sex)
                        msga += "\n{}".format(ExUrl)
                        msg += "\nEx免登入: {}".format(ExUrl.replace("exhentai.org","hentai.bang.cf"))
                        msga += "\n========================"
                        msga += "\n名稱:\n{}\n\n{}".format(nhname,nhname1)
                        msga += "\n========================"
                        msga += "\nTag:{}".format(nhtag)
                        msga += "\n========================"
                        msga += "\n作家:{}".format(nhart)
                        
                        cl.sendMessage(to,msga)
                    except Exception as e:
                        print(e)
                        
                        cl.sendMessage(to,"錯誤，已將錯誤代碼回報")                     
                elif msg.text in ['運勢','ft','Ft','FT']:
                    fortune=['蘿莉','女高中生','御姊','普通女上班族','正太','隔壁大叔','隔壁老太婆雙人組','男子高中生','8+9','鄰家老爺爺','隔壁人妻']
                    text=random.choice(fortune)
                    cl.sendMessage(to, "今日運勢為：" + text)
                elif text.lower() == 'runtime':
                    timeNow = time.time()
                    runtime = timeNow - botStart
                    runtime = format_timespan(runtime)
                    cl.sendMessage(to, "機器運行時間 {}".format(str(runtime)))
                elif text.lower() == 'about':
                    data = AboutMe()
                    sendLiff(to, data)

                elif text.lower() == 'nh=bye':
                    cl.leaveGroup(msg.to)

            if sender in ban["owners"]:
                if text.lower() == 'rebot':
                    cl.sendMessage(to, "重新啟動中...")
                    time.sleep(5)
                    cl.sendMessage(to, "重新啟動成功！")
                    restartBot()
                elif text.lower() == 'set':
                    try:
                        ret_ = "[ 設定 ]"
                        if settings["autoAdd"] == True: ret_ += "\n自動加入好友 ✔"
                        else: ret_ += "\n自動加入好友 ✘"
                        if settings["autoJoin"] == True: ret_ += "\n自動加入群組 ✔"
                        else: ret_ += "\n自動加入群組 ✘"
                        cl.sendMessage(to, str(ret_))
                    except Exception as e:
                        cl.sendMessage(msg.to, str(e))
                elif text.lower() == 'add on':
                    settings["autoAdd"] = True
                    cl.sendMessage(to, "自動加入好友已開啟 ✔")
                elif text.lower() == 'add off':
                    settings["autoAdd"] = False
                    cl.sendMessage(to, "自動加入好友已關閉 ✘")
                elif text.lower() == 'join on':
                    settings["autoJoin"] = True
                    cl.sendMessage(to, "自動加入群組已開啟 ✔")
                elif text.lower() == 'join off':
                    settings["autoJoin"] = False
                    cl.sendMessage(to, "自動加入群組已關閉 ✘")
                elif text.lower() == 'pic on':
                    wait["pic"] = True
                    cl.sendMessage(to,"圖搜已開啟 ✔")
                    cl.sendMessage(to,"請傳送圖片\n注意事項:圖片皆會上傳至圖床，請勿傳送奇怪的圖片")
                elif text.lower() == '圖搜':
                    wait["pic"] = True
                    cl.sendMessage(to,"圖搜已開啟 ✔")
                    cl.sendMessage(to,"請傳送圖片\n注意事項:圖片皆會上傳至圖床，請勿傳送奇怪的圖片\n圖搜功能會自動關閉\n通常第一個結果是saucenao的搜尋結果\n其餘的都是Ascii2d的結果")
                elif text.lower() == 'pic off':
                    wait["pic"] = False
                    cl.sendMessage(to,"圖搜已關閉 ✘")
                    backupData()
                elif text.lower().startswith('op '):
                    MENTION = eval(msg.contentMetadata['MENTION'])
                    inkey = MENTION['MENTIONEES'][0]['M']
                    if inkey not in ban["owners"]:
                        ban["owners"].append(str(inkey))
                        cl.sendMessage(to, "已獲得權限！")
                    else:
                        cl.sendMessage(to, "已經是擁有者了")
                    json.dump(ban, codecs.open('ban.json', 'w', 'utf-8'),
                              sort_keys=True, indent=4, ensure_ascii=False)
                elif text.lower().startswith('deop '):
                    MENTION = eval(msg.contentMetadata['MENTION'])
                    inkey = MENTION['MENTIONEES'][0]['M']
                    if inkey in ban["owners"]:
                        ban["owners"].remove(str(inkey))
                        cl.sendMessage(to, "已取消權限！")
                    else:
                        cl.sendMessage(to, "用戶不再名單內")
                    json.dump(ban, codecs.open('ban.json', 'w', 'utf-8'),
                              sort_keys=True, indent=4, ensure_ascii=False)
                if text.lower() == 'nh=bye':
                    cl.leaveGroup(msg.to)
                elif text.lower() == 'oplist':
                    if ban["owners"] == []:
                        cl.sendMessage(to, "沒有權限者")
                    else:
                        mc = "權限者清單："
                        for mi_d in ban["owners"]:
                            mc += "\n◉ " + cl.getContact(mi_d).displayName
                        cl.sendMessage(to, mc)
        if op.type == 26:
            msg=op.message
            sender = msg._from
            receiver = msg.to
            text = msg.text
            if msg.toType == 0:
                if sender != cl.profile.mid:
                    to = sender
                else:
                    to = receiver
            else:
                to = receiver
            if text is None:
                return
            if msg.contentType == 1:
                if wait["pic"] == True:         
                    path="imgur.png"
                    image = cl.downloadObjectMsg(msg.id, saveAs="imgur.png")
                    cl.sendMessage(to, "正在上傳至圖床...")
                    uploaded_image = im.upload_image(path, title="Uploaded with PyImgur")
                    url=uploaded_image.link
                    print(url)
                    Sauce = saucenao(url)
                    cl.sendMessage(to, Sauce)
                    Ascii = ascii2d(url)
                    for i in range (0,len(Ascii)):
                        cl.sendMessage(to, Ascii[i])
                    wait["pic"] = False
                    
                    
                    
    except Exception as error:
        logError(error)
while True: 
    try:
        ops = oepoll.singleTrace(count=50)
        if ops is not None:
            for op in ops:
                lineBot(op)
                oepoll.setRevision(op.revision)
    except Exception as e:
        logError(e)
