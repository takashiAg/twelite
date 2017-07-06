# encoding:UTF-8

import serial
import urllib
import threading
import sys
import os
import time

#POSTするURL
url="http://192.168.179.10:8081/post.php"

#データの送信先
url_login="http://192.168.179.10:8081/sensor.php"
username="ando"
password="ando"

#シリアルポートを指定
serport="/dev/ttyAMA0"

#idの集合(グローバル変数)
ids=[]

# logファイルの場所
log=os.path.join(os.path.dirname(__file__),"log.txt")

def  post(arg):
    try:
        '''
        f=open(log,"a")
        f.write(arg+"\n")
        f.close()
        '''
        #受信したデータを;でわける
        message=arg.split(";")
        
        #tweliteから情報が送られていないときは長さ３なので９を指定した時にえらーが発生
        error_checker=message[9]
        #tweliteから送られてきた情報が送信すべき情報であれば送信
        
        flag_id=0;
        for id in ids:
            if id==message[5]:
                flag_id=1
                try:
                    params={'uart':arg}
                    data=urllib.urlencode(params)
                    urllib.urlopen(url,data)
                    print("I send a message to "+url+"\nmessage:"+arg)
                except:
                    print("I try to send a message but missed it")
        if flag_id==0:
            print("I try to send a message but but the sensor id is not yours")
    except IndexError:
        print("too short message")
    except:
        print("error")



#main program
#センサidを取得
while ids==[]:
    try:
        data=urllib.urlencode({'user':username,'pass':password})
        res=urllib.urlopen(url_login,data).read()
        ids=res.split(",")
    except:
        print("センサidの取得に失敗")
        f=open(log,"w")
        f.write("センサidの取得に失敗\n")
        f.close()
        time.sleep(1.0)
print(ids)
#シリアル通信を開始
port = serial.Serial(serport, 115200)

while True:
    rcv = port.readline()
    resp=rcv.strip()
    print(resp)
    #データを送信する。送信中にシリアルからのアクセスが来て時間が遅れてしまうのを避けるため新しいスレッドを立てる
    threading.Thread(target=post,args=(resp,)).start()


