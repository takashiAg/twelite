import serial
import urllib,urllib2
import threading
import sys

#post suru url
url="http://192.168.179.2/post.php"

#kono gateway de sousinn suru id wo syutokusuru url
url_login="http://192.168.179.2/sensor.php"
username="ando"
password="ando"

serport="/dev/ttyAMA0"

ids=[]

def  post(arg):
    try:
        message=arg.split(";")
        error_checker=message[9]
        params={'uart':arg}
        for id in ids:
            if id==message[5]:
                try:
                    data=urllib.urlencode(params)
                    req=urllib2.Request(url,data)
                    urllib2.urlopen(req)
                    print("I send a message to "+url+"\nmessage:"+arg)
                except:
                    print("I try to send a message but missed it")
    except IndexError:
        print("too short")
    except:
        print("error")

#main program
try:
    data=urllib.urlencode({'user':username,'pass':password})
    req=urllib2.Request(url_login,data)
    res=urllib2.urlopen(req).read()
    ids=res.split(",")
except:
    print("sensor id no syutoku ni sippai")
    sys.exit()

#sensor
port = serial.Serial(serport, 115200)

while True:
    rcv = port.readline()
    resp=rcv.strip()
    print(resp)
    threading.Thread(target=post,args=(resp,)).start()
