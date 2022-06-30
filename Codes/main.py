from mfrc522 import MFRC522
from machine import Pin, SPI
import socket
import time
import uasyncio
import urequests
import json
from mysecrets import api_key as apikey


# Definindo Led Pins
led_red = Pin(12, Pin.OUT)
led_green = Pin(15, Pin.OUT)


# Colocando os Leds para falso (desligado)
led_red.value(False)
led_green.value(False)

# Links APIs
link = 'https://timeapi.io/api/Time/current/zone?timeZone=Europe/Lisbon' # Horario
link_2 = 'https://maker.ifttt.com/trigger/cartao/with/key/' + apikey # Email

async def blink(output):
    '''Blink the desired led for 1.2 sec.'''
    if output.lower() == 'negado':
        led_off = led_green
        led_on = led_red
    else:
        led_off = led_red
        led_on = led_green

    led_off.value(False)
    led_on.value(True)
    await uasyncio.sleep_ms(1200)
    led_on.value(False)


def email(val1,val2):
    info = {"value1":val1, "value2":val2}
    request_headers = {"Content-Type": "application/json"}
    data = json.dumps(info)
    request = urequests.post(link_2,
        data = data)
    request.close()




spi = SPI(2, baudrate=5000000, polarity=0, phase=0,
            sck=Pin(18), mosi=Pin(23), miso=Pin(19))

spi.init()
rdr = MFRC522(spi=spi, gpioRst=25, gpioCs=5)

with open('registros.json') as json_file:
        ids = json.load(json_file)

async def main():
    global ids


    print(link_2)


    ENTRADA_SAIDA = 2

    print("Place card")

    html = """<!DOCTYPE html>
        <html>
            <head>
            <title>Registro Portaria</title>
            <meta http-equiv="refresh" content="1"/>
            <meta charset="utf-8"/>
            </head>
            <body> <h1>Registro Portaria</h1>
                <table border="1">

                <tr><th>Horário</th><th>Tipo</th><th>Nome</th><th>Estado</th></tr>
                %s

                </table>
            </body>
        </html>
        """


    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(1)

    print('listening on', addr)


    hist = []

    while True:

        (stat, tag_type) = rdr.request(rdr.REQIDL)

        if stat == rdr.OK:

            (stat, raw_uid) = rdr.anticoll()
            if stat == rdr.OK:

                card_id = "0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3])


                # Para caso o cartão ainda não estiver registrado:
                if card_id not in ids:
                    print('O cartão ainda não está registrado, por favor entre as informações a seguir: ')
                    ob = input('Objeto: ')
                    nm = input('Nome: ')
                    es = int(input('Estado (-1:Negado||0:Liberado): ')) # -1= negado, 0=liberado
                    ids[card_id] = [ob,nm,es]

                print(f'{ids[card_id][0]}: {ids[card_id][1]} --',end=' ')

                #Começamos com o caso negado, se for liberado mudamos o estado, caso contrário continua negado
                output = 'Negado'
                # Liberado, se estiver a entrar
                if int(ids[card_id][ENTRADA_SAIDA]) == 0:
                    #print(f'Entrada Liberada')
                    output = 'Entrada Liberada'
                    ids[card_id][ENTRADA_SAIDA] = 1
                # Liberado, se estiver a sair
                elif int(ids[card_id][ENTRADA_SAIDA]) == 1:
                    #print(f'Saída Liberada')
                    output = 'Saída Liberada'
                    ids[card_id][ENTRADA_SAIDA] = 0

                # Task para o LED
                uasyncio.create_task(blink(output))

                # Mandar email caso for negado
                if output.lower() == 'negado':
                    #info = {"value1":card_id, "value2":ids[card_id][1]}
                    #request_headers = {"Content-Type": "application/json"}
                    #request = urequests.post(link_2,
                    #    json = info, headers=request_headers)
                    #request.close()
                    #uasyncio.create_task(email(card_id,ids[card_id][1]))
                    email(card_id,ids[card_id][1])

                print(output)
                print('')

                x = json.loads(urequests.get(link).text)
                time_ = f"{x['day']}/{x['month']}/{x['year']}  {x['hour']}:{x['minute']}:{x['seconds']}"

                hist.append('<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (time_, ids[card_id][0], ids[card_id][1], output))


                cl, addr = s.accept()

                cl_file = cl.makefile('rwb', 0)
                while True:
                    line = cl_file.readline()
                    if not line or line == b'\r\n':
                        break
                await uasyncio.sleep_ms(5)

                response = html % '\n'.join(hist)
                cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
                cl.send(response)
                cl.close()

        await uasyncio.sleep_ms(5)

try:
    uasyncio.run(main())

except KeyboardInterrupt:
    print('Keyboard Interrupt')

finally:
    spi.deinit()

    led_green.value(False)
    led_red.value(False)
    # Directly from dictionary
    with open('registros.json', 'w') as outfile:
        json.dump(ids, outfile)

