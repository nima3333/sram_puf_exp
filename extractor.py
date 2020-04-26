import numpy as np
from serial import *
import matplotlib.pyplot as plt

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

test = [b'BEGINNING\r\n', b'2047\r\n', b'0 0 0 0 6 1 66 0 93 0 53 1 C4 0 A2 0 \r\n', b'B6 0 D A 0 0 45 18 0 0 0 1C 0 0 0 4 \r\n', b'1 0 0 E8 3 0 0 0 0 0 0 C5 0 C4 0 C0 \r\n', b'0 C1 0 C2 0 C6 0 1 0 0 2D 2E 0 0 0 0 \r\n', b'0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 \r\n', b'0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 \r\n', b'0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 \r\n', b'0 0 0 0 0 0 0 0 0 0 0 0 47 49 4E 4E \r\n', b'49 4E 47 D A 32 30 34 37 D A 30 20 30 20 30 \r\n', b'20 30 20 20 20 20 20 20 D A 20 20 20 20 D A \r\n', b'20 20 20 20 D A 20 20 20 20 20 D A D A D \r\n', b'A D A 20 20 20 20 D A 20 20 20 0 0 0 0 \r\n', b'0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 \r\n', b'0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 \r\n', b'0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 \r\n', b'0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 \r\n', b'0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 \r\n', b'0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 \r\n', b'0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 \r\n', b'0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 \r\n', b'0 0 0 FD 7B AF DA 33 1C 24 1F FC 26 BF D4 8B \r\n', b'38 9F 58 E2 46 F2 CD F7 E5 AF 53 CB F7 A7 F1 D5 \r\n', b'33 41 E3 55 BC 68 CE C1 B9 B0 3E E0 9F 3B 73 D3 \r\n', b'BC 31 8A 43 5B DB 21 A5 DF EC E2 3F 40 55 7B 1B \r\n', b'A7 FC 7E A3 51 3D 17 F7 BB E0 19 8B 9B 34 9 6C \r\n', b'46 3B D6 88 D3 A5 7A 79 DE 7F 79 B3 59 47 A9 9E \r\n', b'8A 89 78 F9 20 0 23 FE 3F 43 A5 A1 1E 83 DE CE \r\n', b'6B 87 A1 B3 91 36 72 26 F6 9A 48 CF F7 2D 74 D9 \r\n', b'87 3B 62 F7 D3 EE 1F 7B 94 22 B3 BC E ED 8B E6 \r\n', b'F BF EE 71 A6 C7 C B9 BF 3A DB 89 E6 29 FF 8E \r\n', b'7A 16 9D D6 9C 69 E5 68 F6 45 DF EF 33 43 EA E6 \r\n', b'F5 27 7B E3 52 4A 32 EF 5E CE 6D 79 DB 8F 79 FC \r\n', b'74 8B 11 A3 17 44 27 B8 39 AE 93 9B 75 95 F9 2F \r\n', b'4B 59 DB 92 EF FD E2 34 75 19 CF F8 F3 B7 91 9F \r\n', b'69 1 89 2E 76 A6 FB EB 92 7D AB 1F C3 71 5E 1 \r\n', b'E2 1E 8C 61 CD FB 31 73 5F A7 92 C3 BC 71 40 F1 \r\n', b'8E BD EB DF 83 7A 28 8D 93 3F 1C F5 74 5B 49 E2 \r\n', b'ED CE 1D 10 EF 85 91 DE 61 9B DA 58 51 BC CF 17 \r\n', b'DB CC 3 1F F2 36 D8 71 8B 22 7F E2 C7 94 1F 7E \r\n', b'A9 6C BC 23 A9 FA 1D 57 DF EF FA AE C8 4E 6E BC \r\n', b'F BE E2 F4 F1 FF CF 77 C9 FB 8D E9 A6 D7 4F 92 \r\n', b'C9 AD 85 5D 4F F1 D3 AE 82 DE C9 BA CB 2B 9F F3 \r\n', b'17 1A 7D D0 2C 12 30 8F CE 6E 70 1E D3 6D E7 64 \r\n', b'83 37 14 2A 42 9F 71 86 B8 34 AE FC D6 8E BE EC \r\n', b'1C 64 BF 39 37 C4 56 E4 BE 48 34 EC CE FA DF B0 \r\n', b'DF 19 34 CE 3F 41 7A 1F 9B 6F FD 94 31 66 E 6F \r\n', b'FA 37 A7 60 5B 45 E6 6D 35 73 C3 B8 B5 3C 6E 7E \r\n', b'BF 79 32 D0 EE 59 84 1D C 66 2B BB F7 BE 67 79 \r\n', b'F3 27 7B 7B 59 D3 FB 6E C 7E 1F 8B B6 4F A5 7B \r\n', b'DB 47 C1 7E 3F AA 7E 5E AF 85 E8 97 2D D4 60 77 \r\n', b'D AA 78 55 4F 7A DA 4C AE 3E ED 5 EF B5 E9 97 \r\n', b'9 CA EA 91 FF C3 E5 BE B5 58 CC BB 24 AD BF FC \r\n', b'77 63 7F C1 C5 37 71 54 86 F2 16 6F 8B 37 9B CE \r\n', b'35 57 AA 72 32 AA 3F 4 A3 2A 8B D5 74 DA 97 D4 \r\n', b'7D CB 6D 93 FE F2 BF AD 7E EC 1C 1A 27 5F 76 3F \r\n', b'9B A7 3F C6 3B 69 B3 F2 5F 7F 3A B9 F3 D1 D8 40 \r\n', b'8F 34 3E 9C AF E9 5 FD FD 6D 15 A8 95 41 AB 6D \r\n', b'5D 15 FA 8A F3 3D B4 E1 D CD B4 F6 D5 7C BC E3 \r\n', b'52 7D 41 EB 46 22 2A EF 7B A 9F E8 DA DF 4B 4B \r\n', b'DB BF F6 DA E8 FD 13 CB 9A A1 E3 F5 19 C0 BB CC \r\n', b'D1 77 D4 C2 15 98 3F DB 2F 5 C6 CE C2 57 BE 6B \r\n', b'7D DF 5B AE C5 2F F5 E7 23 71 1 DC EC 58 1F 6E \r\n', b'DF C3 7 D7 EE EA E6 DF 27 50 46 41 11 2F 1 37 \r\n', b'57 FC 1E A7 F2 97 E6 17 2D CB AA F5 DA FD 3C 8C \r\n', b'2D DF 17 65 1F 56 68 DB C3 A7 4D 57 93 B4 FB C7 \r\n', b'6A 72 A9 B5 AD FD CE 48 1E 83 BF 7B C3 DA ED E5 \r\n', b'BF F7 9B 7C CE 6B 7B E8 5F 60 92 5 BF 5E B8 9C \r\n', b'69 E6 CC 8B F6 E8 D4 7F 4A 71 A8 20 79 A5 E3 BB \r\n', b'DB CD 34 AD 3A C F0 3E 95 37 6A F5 AD 81 B2 0 \r\n', b'7A B 2 65 69 7F E2 59 B7 3E C3 F5 99 CC F1 1D \r\n', b'99 B9 F2 E5 76 AF 8E B7 9D 5F FB 8B CD E8 92 F8 \r\n', b'F7 BF 5B B6 4F 7B E2 78 C8 E4 C6 F9 D0 93 75 47 \r\n', b'49 FC B8 FB 8E B4 E2 FF A B 3D B9 3F FC A3 2D \r\n', b'65 1B 3C 4B FF FE B E9 7B 8A 64 B9 3C F0 8F A2 \r\n', b'BB E9 35 2B 9C 9 C7 E7 77 AE 58 6 B9 EC FD 15 \r\n', b'F7 86 5F CB DD FC F1 4F 4F FE 63 84 1A 3E FB BF \r\n', b'9B D7 E8 B0 F4 36 E4 DD 98 DD A7 3B C2 6A D7 83 \r\n', b'7F AD F3 5B B6 DF DB BF CA 34 7F 8D 9F 50 A0 F9 \r\n', b'67 3F A5 AD 28 42 1F B3 AF F5 FA BA FA 73 2D D9 \r\n', b'8B 5D AA FC F3 CC 5A DC A9 E9 4F FE DB 6C F5 B1 \r\n', b'E E1 EA EB 78 71 FA A7 B4 2D 3F FF A2 4 2D AA \r\n', b'D6 AC 63 3C 1A 6D 63 D1 43 9F C4 6 F9 F8 55 D7 \r\n', b'1B FF DD A8 5C D1 D3 DB 51 E4 F4 FF 2B 87 1E 59 \r\n', b'22 ED 68 FC CB C1 93 D2 C7 81 83 9E F5 50 64 7B \r\n', b'42 FA 99 52 CB F9 EB A0 BD D9 78 A1 F6 23 F4 DB \r\n', b'2A 9 3D CC 41 47 C6 DD 3F 7E 62 4 CD B2 36 19 \r\n', b'FD 7C 5B 16 CF E5 FA 72 F4 BB 6C 5F EB 77 7D 76 \r\n', b'AE 67 1B 3F 2A 47 8F 24 B7 E9 28 A7 CE AD 38 CD \r\n', b'3F EF F3 96 72 B9 6F E 55 99 35 6F F7 CE 9B 97 \r\n', b'71 93 E9 3A AF A1 83 C5 33 6E 1E F6 F 89 69 E3 \r\n', b'72 CF 1A CE 3A 24 DF 8F FF C1 21 6F D7 80 6C E7 \r\n', b'3B 73 B5 F7 47 44 A7 A9 15 33 14 1F C6 5E EF 86 \r\n', b'9B 31 6B DE AD FF F3 ED 68 74 19 DF FA A1 A7 99 \r\n', b'1B F9 58 EF FA 77 E 7A 3B 52 7F CA 13 D5 DA 5A \r\n', b'6B EA 75 9A B1 57 B9 77 3A 85 DC C7 B7 C6 FE 3A \r\n', b'2B B6 13 EE B0 E3 73 EF 7B D5 9E F7 4F C1 F2 FE \r\n', b'13 C8 88 B4 9B 3D BA E5 42 FF 42 F4 8A 71 73 36 \r\n', b'DF 7C FE 93 6E 69 3A AA EB 24 48 FA 37 DF 78 E5 \r\n', b'93 6F E0 5A CB 3D 91 9D FB 8F EE BB C3 5 EF 69 \r\n', b'D6 D5 EC EF 5F 75 5E 89 C5 9 CD B3 36 A7 B6 8A \r\n', b'76 C9 AF 29 9D F8 86 E7 B7 5D 23 7A E8 C6 F6 33 \r\n', b'D2 DD 2F E1 AE F3 1C CC 5F DA 3B 51 59 68 95 CC \r\n', b'83 20 43 63 9F D2 7C 35 12 B6 A5 34 F7 16 E5 DE \r\n', b'C5 E9 9C FA 7B 8D 4E 7F 6B C7 FF A1 EB D5 D7 34 \r\n', b'61 BE BD 55 6F FD 45 69 BD B8 96 7C F 9C 81 43 \r\n', b'AB 7B 7C FF F0 7C FE 74 FE 3A 4D FC 2A 7E 5B 2D \r\n', b'8F 9A E3 B6 E6 BE DE C7 CB 6F D3 36 FB 5F 4C B8 \r\n', b'20 D6 E5 E1 D5 AD AF 36 DF C3 BB C3 49 F7 DC 4E \r\n', b'D7 F6 E6 BD C B9 6C 9F 5D 9F A1 72 A3 97 FB C1 \r\n', b'DD DF D4 D4 6E 55 BC 48 BE 63 AF F2 E5 5E F 6D \r\n', b'10 F7 8C 76 F3 DE DD 14 9F BC 35 7F BC 3C 97 5D \r\n', b'9B 3B FD 36 F8 3B 9F 71 BA F2 D6 96 81 E6 E6 29 \r\n', b'99 89 63 77 53 E5 1B 73 DB 3E 8 66 6B 9C 3D 1B \r\n', b'FE 4A 8E F8 FF 96 9F B2 71 6A B9 F9 DD C9 8B 2A \r\n', b'AF E5 E8 62 2C 6E AB CD 8 83 B1 F3 FA 8F 54 A3 \r\n', b'43 F9 36 76 AF EC F1 3F BE 58 73 F6 18 BD BB 5B \r\n', b'DD F1 F4 3E FB A5 75 48 72 2B 69 30 6B AB AC 51 \r\n', b'57 AC 65 73 31 5 EB C1 7A 49 E7 A7 19 17 7B 32 \r\n', b'F9 DA F4 F6 DE BB 77 CF E1 77 77 35 37 AB D6 4A \r\n', b'5B C6 A5 BF F3 AC 9E FF 6D 8E E6 2F FD 7E 52 2F \r\n', b'9E 60 F6 FC AE D5 D3 1C B7 52 D5 8 59 B5 ED 5B \r\n', b'55 9F EF DC B1 57 B9 78 8F 8A BF BE F8 DB A1 9C \r\n', b'6 B1 D1 CF 25 B1 EA B9 E3 3C AE E1 B6 C5 DA F8 \r\n', b'F7 E8 E7 CC 1 20 B5 1 0 0 1 20 0 1 0 8 \r\n', b'F3 8 F3 8 F2 0 85 8 D2 8 F2 0 21 7F 48 0 \r\n', b'0 1 F8 C6 FC EE CE 75 EF F7 D6 5D 55 80 A0 1 \r\n', b'1 20 0 1 1 20 1 1F 0 2 1E 0 C1 0 0 8 \r\n', b'86 FC 8 0 11 B5 FF 35 80 0 1 87 3 54 0 \r\n', b'\x00']

def get_serial_matrix(serial_txt):
    new_file = [x.rstrip().decode() for x in serial_txt if x != b'\x00']
    assert(new_file[0] == 'BEGINNING')
    memory_size = int(new_file[1])+1
    mem = np.zeros(memory_size, dtype=np.int16)
    i=0
    for line in new_file[2:]:
        elements = line.split(" ")
        for elem in elements[:-1]:
            mem[i] = int(elem, 16)
            i+=1
    return mem

mem1 = get_mem_matrix("1")
print(mem1.shape)

mem2 = get_serial_matrix(test)
print(mem2.shape)

'''
import serial.tools.list_ports
myports = [tuple(p) for p in list(serial.tools.list_ports.comports())]
print(myports)

data = []
with Serial(port="/dev/cu.usbmodem142201", baudrate=57600, timeout=1, writeTimeout=1, ) as port_serie:
    if port_serie.isOpen():
        ligne = port_serie.readlines()
        ligne = port_serie.readlines()
        print(ligne[0].rstrip().decode())
        port_serie.write(b'10')

        for i in range(10): 
            ligne = port_serie.readlines()
            while(not ligne or ligne[0] in [b'\x00', b'\r\n']):
                ligne = port_serie.readlines()
            data.append(ligne)

np_data = np.array(data)
np.save("save", np_data)
'''

a = np.load("save.npy", allow_pickle=True)
print(a)


new = []
for elem in a:
    new.append(get_serial_matrix(elem))

proba_list = []
for i in range(2048):
    a = np.array(new)[:,i]
    counts = np.bincount(a)
    proba_list.append(np.max(counts)/np.sum(counts))

plt.hist(proba_list)
plt.show()

