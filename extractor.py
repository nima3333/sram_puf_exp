import numpy as np
from serial import *

def get_mem_matrix(file):
    mem = np.zeros(2048)
    with open(file) as f:
        content = f.read().splitlines()

    i=0
    for line in content:
        elements = line.split(" ")
        for elem in elements[:-1]:
            mem[i] = int(elem, 16)
            i+=1
    return mem

mem1 = get_mem_matrix("/Users/nima/Desktop/1")
print(mem1)

import serial.tools.list_ports
myports = [tuple(p) for p in list(serial.tools.list_ports.comports())]
print(myports)

with Serial(port="/dev/cu.usbmodem142201", baudrate=57600, timeout=1, writeTimeout=1, ) as port_serie:
    if port_serie.isOpen():
        ligne = port_serie.readlines()
        ligne = port_serie.readlines()
        print(ligne[0].rstrip().decode())
        port_serie.write(b'3')

        for i in range(3): 
            ligne = port_serie.readlines()
            while(not ligne or ligne[0] == b'\x00'):
                ligne = port_serie.readlines()
            print(ligne)

