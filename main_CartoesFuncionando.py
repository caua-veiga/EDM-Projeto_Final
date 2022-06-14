# More details can be found in TechToTinker.blogspot.com
# George Bantique | tech.to.tinker@gmail.com

from mfrc522 import MFRC522
from machine import Pin, SPI


# IDS: 'ID COMUNICAR COM OBJETO' : [OBJETO (CHAVEIRO OU CARTAO), NOME USUARIO (QLQR, APENAS INTERFACE), ESTADO (LIBERAR OU NN)
# -- , CONTROLO ENTRADA OU SAIDA (0 OU 1)]
ids = {'0x94006b1a': ['Chaveiro', 'Cauã Veiga','Liberado',0],
       '0x9351e2ec': ['Cartão','Felipe Coutinho','Negado',0]}

spi = SPI(2, baudrate=5000000, polarity=0, phase=0,
          sck=Pin(18), mosi=Pin(23), miso=Pin(19))

spi.init()
rdr = MFRC522(spi=spi, gpioRst=25, gpioCs=5)
print("Place card")

try:
    while True:

        (stat, tag_type) = rdr.request(rdr.REQIDL)
        if stat == rdr.OK:
            (stat, raw_uid) = rdr.anticoll()
            if stat == rdr.OK:
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
                if ids[card_id][2].lower() == 'liberado':
                    # Se estiver a entrar
                    if ids[card_id][3] == 0:
                        print(f'Entrada {ids[card_id][2]}')
                        ids[card_id][3] = 1
                    # Se estiver a sair
                    elif ids[card_id][3] == 1:
                        print(f'Saída {ids[card_id][2]}')
                        ids[card_id][3] = 0
                # Para o caso em que foi negado (não terá como saber se está a entrar ou sair)
                else:
                    print(f'{ids[card_id][2]}')
                print('')
except KeyboardInterrupt:
    print('Keyboard Interrupt')

finally:
    spi.deinit()


