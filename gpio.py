import RPi.GPIO as GPIO
import threading
import time
from functools import partial
import socket

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(13, GPIO.OUT)  # rood lampje en piep
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # systeem actief
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # alarm uit
GPIO.setup(18, GPIO.OUT)   # groen lampje
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # deactiveerd
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Alarm af

idle = True
active = False
running = True
speed_idle = .25  # snelheid van knipperen bij idle in computer-seconden
speed_active = .1  # snelheid van knipperen bij alarm activatie in c-s
code = '0000'


def nieuw_code():
    global code
    try:
        new = int(input('Geef uw nieuwe code van minimaal 4 cijfers: '))
        if len(str(new)) >= 4:
            code = str(new)
            return True
    except:
        print('De code moet uit cijfers bestaan')
        nieuw_code()


def check_code():
    if input('\nVoer uw code in: ') == code:
        return True
    print('Dit is niet de correcte code\n')
    return False


def leds():
    while running:
        while active:  # als active True is, gooi het lampje in knippermodus
            GPIO.output(18, GPIO.LOW)
            GPIO.output(13, GPIO.HIGH)
            time.sleep(speed_active)
            GPIO.output(13, GPIO.LOW)
            time.sleep(speed_active)
        while idle:  # als idle True is, gooi het lampje in knippermodus
            GPIO.output(13, GPIO.LOW)
            GPIO.output(18, GPIO.HIGH)
            time.sleep(speed_idle)
            GPIO.output(18, GPIO.LOW)
            time.sleep(speed_idle)
        GPIO.output(13, GPIO.LOW)
        GPIO.output(18, GPIO.LOW)


def check_console():
    while running:  # vraag aan gebruiker wat hij wil doen
        try:
            x = int(input('\n1 Voor alarm actief\n'
                          '2 Voor alarm de-actief\n'
                          '3 Om het alarm af te zetten\n'
                          '4 Om alarm te testen\n'
                          '5 Om een nieuwe code in te voeren\n'
                          '6 Om programma stop te zetten\n'
                          '  Ik kies optie: '))
            if x == 2 or x == 3:
                if check_code():
                    actions(x)
            else:
                actions(x)
        except:  # meld dit als het ingevoerde geen 1 - 6 is
            print('Dit is geen 1, 2, 3, 4, 5 of 6')


def actions(x):
    global idle, active
    x = int(x)
    # print('\n')
    if x == 1:  # zet opties aan of uit aan de hand van wat de gebruiker ingevoerd heeft
        idle = True
        # print('Alarm staat nu op scherp')
    elif x == 2:
        # if check_code():
            idle = False
            # print('Alarm staat nu op onscherp')
    elif x == 3:
        if active:
            # if check_code():
                active = False
                idle = True
                # print('Alarm is nu uitgeschakeld')
        # else:
            # print('Het alarm gaat niet af, u hoeft het niet uit te zetten')
    elif x == 4:
        if idle:
            active = True
            idle = False
            # print('Alarm gaat af!!!')
         # print('Het systeem staat niet op scherp')
    elif x == 5:
        if check_code():
            if nieuw_code():
                print('U heeft nu een nieuwe code')
    elif x == 6:
        shutdown()
        print('Shutting down... \nSee you next time!')
    time.sleep(.25)


def button_action(x, i):
    i = 0
    actions(x)


def shutdown():
    global idle, active, running
    running, active, idle = False, False, False
    GPIO.output(18, GPIO.HIGH)
    GPIO.output(13, GPIO.HIGH)
    time.sleep(3)
    GPIO.output(18, GPIO.LOW)
    GPIO.output(13, GPIO.LOW)


def listenNetwork():
    while running:
        c, addr = s.accept()  # Establish connection with client.
        button_action(4, 0)
        print('test')
        c.close()


GPIO.add_event_detect(17, GPIO.RISING, callback=partial(button_action, 1), bouncetime=500)
GPIO.add_event_detect(23, GPIO.RISING, callback=partial(button_action, 2), bouncetime=500)
GPIO.add_event_detect(27, GPIO.RISING, callback=partial(button_action, 3), bouncetime=500)
GPIO.add_event_detect(19, GPIO.RISING, callback=partial(button_action, 4), bouncetime=500)

s = socket.socket()  # Create a socket object
host = '169.254.90.140'  # Get local machine name
port = 12346  # Reserve a port for your service.
s.bind((host, port))  # Bind to the port
s.listen(5)  # Now wait for client connection.

# laat deze functies altijd en tegelijk draaien zolang het programma runt
t1 = threading.Thread(target=leds, name='leds')
t2 = threading.Thread(target=check_console, name='check_console')
t3 = threading.Thread(target=listenNetwork)

t1.start()
t2.start()
t3.start()

t1.join()
t2.join()
t3.join()
