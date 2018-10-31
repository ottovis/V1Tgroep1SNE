#!/usr/bin/env bash

scp /home/otto/PycharmProjects/MiniprojectGerjan/CSN/gpio.py pi@169.254.90.140:/home/pi/
scp /home/otto/PycharmProjects/MiniprojectGerjan/CSN/client.py pi@169.254.90.140:/home/pi/

scp /home/otto/PycharmProjects/MiniprojectGerjan/CSN/gpio.py pi@169.254.177.151:/home/pi/
scp /home/otto/PycharmProjects/MiniprojectGerjan/CSN/client.py pi@169.254.177.151:/home/pi/

scp /home/otto/PycharmProjects/MiniprojectGerjan/CSN/gpio.py pi@169.254.193.169:/home/pi/
scp /home/otto/PycharmProjects/MiniprojectGerjan/CSN/client.py pi@169.254.193.169:/home/pi/

scp /home/otto/PycharmProjects/MiniprojectGerjan/CSN/gpio.py pi@169.254.3.86:/home/pi/
scp /home/otto/PycharmProjects/MiniprojectGerjan/CSN/client.py pi@169.254.3.86:/home/pi/

python3 ./startupScript.py