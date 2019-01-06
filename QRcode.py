from io import BytesIO
from time import sleep
from PIL import Image
from picamera import PiCamera
from zbarlight import scan_codes
import paho.mqtt.client as mqttClient
import time

def on_connect(client, userdata, flags, rc):
 
    if rc == 0:
 
        print("Connected to broker")
 
        global Connected                #Use global variable
        Connected = True                #Signal connection 
    else:
         print("Connection failed")
 
Connected = False   #global variable for the state of the connection
 
broker_address= "localhost"
port = 1883
user = "user"
password = "user"

client = mqttClient.Client("Python")               #create new instance
client.username_pw_set(user, password=password)    #set username and password
client.on_connect= on_connect                      #attach function to callback
client.connect(broker_address, port=port)          #connect to broker
 
client.loop_start()        #start the loop
 
while Connected != True:    #Wait for connection
    time.sleep(0.1)
 
try:
    while True:
      stream = BytesIO()
      codes = None


      with PiCamera() as camera:
        camera.start_preview()
        sleep(2)
        while codes is None:
          stream.seek(0)
          camera.capture(stream, 'jpeg')
          stream.seek(0)
          codes = scan_codes(['qrcode'], Image.open(stream))
          camera.stop_preview()
          print(codes)
        qr_code_re = [int(s) for s in codes[0].split() if s.isdigit()]

        
        values = ','.join(str(v) for v in qr_code_re)
        print(values)
        client.publish("QR_code_ref", values)

except KeyboardInterrupt:
 
    client.disconnect()
    client.loop_stop()






