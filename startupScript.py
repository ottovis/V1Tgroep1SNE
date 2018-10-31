# testen van de commands uitvoeren in terminal
# dhcp uit op pi command: systemctl disable/stop isc-dhcp-server

import subprocess

# voor het testen van dit script, zorg dat het ip van de pi aangepast is naar het ip van je eigen pi
# om te voorkomen dat je wachtwoorden moet invoeren google even hoe je ssh-keygen gebruikt om private public key pair maakt
# normaal voer je commando's uit met os.command() maar die is niet goed meer ofzo, en dit is de vervanging
# al werkt deze vervanging veel verwarender en heb ik echt geen idee hoe het eigenlijk werkt
# het voordeel is dat je dit kan copy and pasten onder elkaar met meerdere commando's en die voert ie allemaal uit
# de top in het commando is een standaard linux commando, soort van taskmanager, deze kunnen we later vervangen
# met het uitvoeren een python script/home/otto/PycharmProjects/MiniprojectGerjan/CSN/client.py
# /home/otto/PycharmProjects/MiniprojectGerjan/CSN/gpio.py, om het alarm systeem te starten
# laat mij dit maar doen, want dit is gewoon kut anders :p

process = []


with open('serverip.txt', 'r') as file:
    for ip in file.read().split(';'):
        bashCommand = ['gnome-terminal', '--', 'ssh', ('pi@' + ip), '-X', '-t', 'python3 gpio.py'] # draai het gpio.py bestand op de server via ssh
        process.append(subprocess.Popen(bashCommand, stdout=subprocess.PIPE))
        output, error = process[-1].communicate()
        print(output)
        print(error)

with open('clientip.txt', 'r') as file:
    for ip in file.read().split(';'):
        bashCommand = ['gnome-terminal', '--', 'ssh', ('pi@' + ip), '-X', '-t', '-t', 'python3 client.py'] # draai het client.py bestand op de client via ssh
        process.append(subprocess.Popen(bashCommand, stdout=subprocess.PIPE))
        output, error = process[-1].communicate()
        print(output)
        print(error)