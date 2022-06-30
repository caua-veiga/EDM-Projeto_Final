# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()

from mysecrets import enderecos, api_key
import time
import network
import urequests


ssid, password = enderecos['iphone_caua']

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
print(wlan.scan())
if not wlan.isconnected():
    print('Connecting to network...')
    wlan.connect(ssid, password)   #'HUAWEI', 'vouchorar'
    while not wlan.isconnected():
        print('.', end='')
        time.sleep(0.1)
    print(' Connected!')
print('network config:', wlan.ifconfig())
