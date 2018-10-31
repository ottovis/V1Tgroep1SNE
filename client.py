import socket
import time
import RPi.GPIO as GPIO


running = 1

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(27, GPIO.OUT)

host = '169.254.90.140'
port = 12346


def sendAlarm(i):
    try:
        f = socket.socket()
        print('Triggering alarm')
        f.connect((host, port))
        f.close()
    except ConnectionRefusedError:
        print('Server not running')
    except OSError:
        print('Server offline')
    except:
        print("Unknown failure")

    GPIO.output(27, GPIO.HIGH)
    time.sleep(.2) # geef conformatie dat knopje drukken werkte door een
    GPIO.output(27, GPIO.LOW)


GPIO.add_event_detect(17, GPIO.FALLING, callback=sendAlarm, bouncetime=500)

while running != 5:
    running = int(input())
    # houd het bestand running zodat de event trigger blijft werken zolang je niet 5 invoerd
