import uasyncio
import urequests
import json
from mysecrets import api_key as apikey







link_2 = 'https://maker.ifttt.com/trigger/cartao/with/key/' + apikey
print(link_2)

print('')
print('AAAAAA')
for i in range(5):
    # Mandar email caso for negado

    info = {"value1":0001, "value2":9990}
    data = json.dumps(info)
    request_headers = {"Content-Type": "application/json"}
    request = urequests.post(link_2,
        json = info, headers=request_headers)
    request.close()
    print(i)
