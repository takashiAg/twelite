import serial
import urllib,urllib2
import threading

url="http://192.168.179.2/post.php"

def  post(arg):
    try:
        uart=arg.split(";")[9]
        params={'uart':arg}
        data=urllib.urlencode(params)
        req=urllib2.Request(url,data)
        urllib2.urlopen(req)
    except IndexError:
        print("too short")
    except:
        print("error")

port = serial.Serial("/dev/ttyAMA0", 115200)

while True:
    rcv = port.readline()
    resp=rcv.strip()
    print(resp)
    threading.Thread(target=post,args=(resp,)).start()
