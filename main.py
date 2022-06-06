# More details can be found in TechToTinker.blogspot.com
# George Bantique | tech.to.tinker@gmail.com

from mfrc522 import MFRC522
from machine import Pin, SPI

ids = {'0x94006b1a': ['Chaveiro', 'Cauã Veiga'],
       '0x9351e2ec': ['Cartão','Rafael Lobão']}

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
                print(f'{ids[card_id][0]}: {ids[card_id][1]}')
                print('')
except KeyboardInterrupt:
    print('Keyboard Interrupt')

finally:
    spi.deinit()


