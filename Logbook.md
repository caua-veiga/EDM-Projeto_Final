# Interface com o leitor de RFID RC522 _ Aplicação segurança/banco

## 1. Propostas de interface
- 1.1 _ Bancos:
    Aplicação que registra/permite uma compra, com valor horário, cliente id, etc... 

- 1.2 _ Segurança:
    Aplicação que registra entrada e saída de pessoas numa portaria

## 2. Planeamento

### 2.1 - Comunicação RFID RC522 com esp32

Independentemente da interface escolhida na secção 1 (bancos ou segurança) a etapa mais importa é estabelecer corretamente a comunicação entre a esp32 e o módulo RFID. Para a primeira aula (06-06-2022) é um bom plano nos familiarizarmos com os equipamentos e estabelecer essa comunição corretamente, para que então possamos desenvolver aplicações mais complexas. Para isso, na próxima secção encontram-se algumas referências úteis.

### 2.1.1 - Referências Úteis

- 'µC-15 RFID en Micropython (SPI)' -- -- https://www.youtube.com/watch?v=rt8vbWKecqI

-  '026 - ESP32 MicroPython: MFRC522 RFID' -- --https://www.youtube.com/watch?v=KufRt3p9tCI

- 'RFID RC522 micropython sur ESP32' -- *vídeo em frances* -- https://www.youtube.com/watch?v=VSuAuU9Fngg 

- 'Curso ESP32 parte 12: RFID MFRC522 (MicroPython)' -- -- https://www.youtube.com/watch?v=BOgiGo0q_lo

- 'ESP32 com RFID: Controle de Acesso' -- *parece bom, mas código em C* -- https://www.youtube.com/watch?v=8NNyTiPXzdc

- 'ESP32: How to read RFID tags with a RFID Reader' -- *código em C* -- https://www.youtube.com/watch?v=pJLjFm4Ipro

- https://lastminuteengineers.com/how-rfid-works-rc522-arduino-tutorial/