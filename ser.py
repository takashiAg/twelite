# encoding:UTF-8

import serial
import urllib,urllib2
import threading
import sys

#POSTするURL
url="http://192.168.179.2/post.php"

#データの送信先
url_login="http://192.168.179.2/sensor.php"
username="ando"
password="ando"

#シリアルポートを指定
serport="/dev/ttyAMA0"

#idの集合(グローバル変数)
ids=[]

def  post(arg):
    try:
        #受信したデータを;でわける
        message=arg.split(";")
        
        #tweliteから情報が送られていないときは長さ３なので９を指定した時にえらーが発生
        error_checker=message[9]

        #tweliteから送られてきた情報が送信すべき情報であれば送信
        for id in ids:
            if id==message[5]:
                try:
                    params={'uart':arg}
                    data=urllib.urlencode(params)
                    req=urllib2.Request(url,data)
                    urllib2.urlopen(req)
                    print("I send a message to "+url+"\nmessage:"+arg)
                except:
                    print("I try to send a message but missed it")
    except IndexError:
        print("too short message")
    except:
        print("error")



#main program
#センサidを取得
try:
    data=urllib.urlencode({'user':username,'pass':password})
    req=urllib2.Request(url_login,data)
    res=urllib2.urlopen(req).read()
    ids=res.split(",")
except:
    print("センサidの取得に失敗")
    sys.exit()

#シリアル通信を開始
port = serial.Serial(serport, 115200)

while True:
    rcv = port.readline()
    resp=rcv.strip()
    print(resp)
    #データを送信する。送信中にシリアルからのアクセスが来て時間が遅れてしまうのを避けるため新しいスレッドを立てる
    threading.Thread(target=post,args=(resp,)).start()


