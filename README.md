# Interface com o leitor de RFID RC522
## Cauã Veiga, Rafael Lobão
## Faculdade de Engenharia da Universidade do Porto

# 1. Introdução

Desenvolveu-se, no contexto da cadeira de Eletrónica Digital e Microprocessadores, uma interface que emprega um leitor de identificação por rádio frequência (RFID).

Neste projeto, idealizou-se uma situação em que uma empresa possui uma sala de acesso restrito. O acesso a esta sala é garantido sempre que o cartão de um funcionário autorizado é detetado pelo leitor.

Todos os acessos garantidos são registados num website e, no caso de um funcionário não autorizado tentar ter acesso à sala, algumas pessoas previamente definidas recebem um e-mail de notificação da ocorrência

# 2. Material

Neste projeto, usou-se o seguinte material: 

- placa de desenvolvimento;

- leitor de RFID RC522;

- Led vermelho e led verde;

## 2.1. RFID RC522 (fonte: https://www.electrofun.pt/comunicacao/leitor-rfid-arduino)

Especificações:

- Consumo: 13-26mA / DC 3.3V;

- Consumo em Stand-By: 10-13mA / 3.3V;

- Consumo em Sleep: - Pico de corrente: <30mA;

- Frequência da operação: 13,56MHz;

- Tipos de cartões suportados: Mifare1 S50, S70 Mifare1, Mifare UltraLight, Mifare Pro, Mifare Desfire;

- Temperatura operacional: -20ºC a 80ºC;

- Taxa de transferência: 10 Mbit/s;


# 3. Descrição

# 3.1. Tecnologia *Radio Frequency IDentification*

Um sistema RFID consiste basicamente em dois componentes principais, um objeto contendo uma *tag* (o qual será identificado), e um *leitor* que irá ler esta *tag*.

O *leitor* consiste em um módulo de rádiofrequência e uma antena que gera um campo eletromagnético de alta frequência. Já a *tag* é um microchip que guarda e processa informações, e possuí uma antena para receber e transmitir sinais. 

Quando a *tag* é aproximada ao *leitor*, o *leitor* gera um campo magnético e o chip responde transmitindo as suas informações para o leitor na forma de outro sinal de rádio, este processo é chamado *'retrodifusão'*. O *leitor* interpreta este sinal e manda os dados para o microcontrolador.
<figure>
<img src="images/RFID_leitor_tag.png"
     alt="RFID leitor_tag image"
     style="vertical-align:middle;margin:10px 115px" />

<figcaption align = "center"><b>Fig.1 - Funcionamento sistema RFID.
 <a href ='lastminuteengineers.com'>lastminuteengineers.com</a></b></figcaption>
</figure>

## 3.1. Cadastro Cartões

TO-DO

## 3.2. Descrição do funcionamento da interface

A interface tem 3 comportamentos distintos:

### 3.2.1. Se o cartão tiver autorização de acesso: 

Ao entrar: o led verde pisca uma vez (simbolizando o desbloqueio da porta), o ID do cartão, o nome do proprietário, a hora de acesso e a informação "Entrada Liberada" são registadas na página Web.

Ao sair: o led verde pisca duas vezes, o ID do cartão, o nome do proprietário, a hora de acesso e a informação "Saída Liberada" são registadas na página Web.

### 3.2.2. Se o cartão não tiver autorização de acesso: 

Uma notificação é enviada por e-mail a um grupo de pessoas pré-definidas com o ID do cartão, o nome do proprietário e a hora da tentativa de acesso. O mesmo é registado na página Web.

### 3.2.3. Se o ID do cartão não se encontrar registado:

Prosegue-se ao cadastro da pessoa: O nome é introduzido, juntamente com o estatuto de acesso à sala. A interface pede um PIN secreto. Este PIN é definido no ficheiro "mysecrets.py".

## 3.3. Montagem

(Inserir esquema do circuito)


## 3.4. Comuniação entre componentes
O RFID RC522 comunica com o ESP32 através do protocolo SPI tal e tal. A programação foi baseada em talv e tal código.

## 3.5. Notificação por e-mail

Para as notificações, usa-se uma API configurada pelo serviço/website IFTTT ("If This Then That").
Este serviço permite automatizar certas ações: as ações são executadas sempre que há um "trigger". Neste caso, o trigger é uma solicitação feita com recurso à biblioteca "urequests" e envia um ficheiro json com o ID do cartão e o nome do proprietário.

O código foi baseado no artigo: https://microcontrollerslab.com/micropython-esp32-esp8266-send-sensor-readings-via-email-ifttt/


## 3.6. Registro de acessos



# 4. Discussão/Conclusão/Coisas a melhorar/acrescentar

O objetivo proposto foi cumprido: implementou-se com sucesso uma interface com o leitor de RFID RC522o leitor de RFID RC522.

Como forma de complementar o projecto, empregou-se um sistema de notificações por e-mail e um sistema de registo de leituras.

Como forma de melhorar o projecto, podia-se ter implementado um "buzzer".

