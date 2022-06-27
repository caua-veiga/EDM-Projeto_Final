# More details can be found in TechToTinker.blogspot.com
# George Bantique | tech.to.tinker@gmail.com

from mfrc522 import MFRC522
from machine import Pin, SPI
import socket
import time
import uasyncio


# Defining Led Pins
led_red = Pin(12, Pin.OUT)
led_green = Pin(15, Pin.OUT)


# Setting all leds to False
led_red.value(False)
led_green.value(False)

async def blink(output):
    '''Blink the desired led for 1.2 sec.'''
    if output.lower() == 'negado':
        led_off = led_green
        led_on = led_red
    else:
        led_off = led_red
        led_on = led_green

    led_off.off()
    led_on.on()
    await uasyncio.sleep_ms(1200)
    led_on.off()


spi = SPI(2, baudrate=5000000, polarity=0, phase=0,
            sck=Pin(18), mosi=Pin(23), miso=Pin(19))

spi.init()
rdr = MFRC522(spi=spi, gpioRst=25, gpioCs=5)
async def main():

    ENTRADA_SAIDA = 2

    # IDS: 'ID COMUNICAR COM OBJETO' : [OBJETO (CHAVEIRO OU CARTAO), NOME USUARIO (QLQR, APENAS INTERFACE), ESTADO (LIBERAR OU NN)
    # -- , CONTROLO ENTRADA OU SAIDA (0 OU 1)]
    ids = {'0x94006b1a': ['Chaveiro', 'Cauã Veiga',0],
        '0x9351e2ec': ['Cartão','Felipe Coutinho',-1]} # TROCAR ISSO PARA UM JSON

    #spi = SPI(2, baudrate=5000000, polarity=0, phase=0,
    #        sck=Pin(18), mosi=Pin(23), miso=Pin(19))

    #spi.init()
    #rdr = MFRC522(spi=spi, gpioRst=25, gpioCs=5)
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
            #print('TRUE')
            #cl, addr = s.accept()

            (stat, tag_type) = rdr.request(rdr.REQIDL)
            #print('resquest')
            if stat == rdr.OK:

                (stat, raw_uid) = rdr.anticoll()
                if stat == rdr.OK:
                    #print('K')
                    card_id = "0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3])
                    #ids[card_id] = ids.get(card_id, card_id)

                    # Para caso o cartão ainda não estiver registrado:
                    if card_id not in ids:
                        print('O cartão ainda não está registrado, por favor entre as informações a seguir: ')
                        ob = input('Objeto: ')
                        nm = input('Nome: ')
                        es = input('Estado: ')
                        cn = 0
                        ids[card_id] = [ob,nm,es,cn]

                    print(f'{ids[card_id][0]}: {ids[card_id][1]} --',end=' ')

                    #Para o caso em que é liberado
                    output = 'Negado'
                    # Se estiver a entrar
                    if ids[card_id][ENTRADA_SAIDA] == 0:
                        #print(f'Entrada Liberada')
                        output = 'Entrada Liberada'
                        ids[card_id][ENTRADA_SAIDA] = 1
                    # Se estiver a sair
                    elif ids[card_id][ENTRADA_SAIDA] == 1:
                        #print(f'Saída Liberada')
                        output = 'Saída Liberada'
                        ids[card_id][ENTRADA_SAIDA] = 0

                    # Para o caso em que foi negado (não terá como saber se está a entrar ou sair)
                    #else:
                        #print(f'Negado')
                    #    output = 'Negado'
                    uasyncio.create_task(blink(output))
                    print(output)
                    print('')

                    hist.append('<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % ('hora', ids[card_id][0], ids[card_id][1], output))

                    #print('antes cl')
                    cl, addr = s.accept()
                    #print('cl')
                    cl_file = cl.makefile('rwb', 0)
                    while True:
                        #print('To preso')
                        line = cl_file.readline()
                        if not line or line == b'\r\n':
                            break
                    await uasyncio.sleep_ms(5)
                    #rows = ['<tr><td>%s</td><td>%d</td></tr>' % (str(p), p.value()) for p in pins]
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
