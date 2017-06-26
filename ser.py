import serial
import urllib,urllib2

port = serial.Serial("/dev/ttyAMA0", 115200)

while True:
    rcv = port.readline()
    resp=rcv.strip()
    print(resp)
    url="http://192.168.179.2/post.php"
    params={'uart':resp}
    data=urllib.urlencode(params)
    req=urllib2.Request(url,data)
    urllib2.urlopen(req)
