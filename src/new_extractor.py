import numpy as np
from serial import *
import matplotlib.pyplot as plt
from matplotlib import colors
import matplotlib as mlp
import serial.tools.list_ports
import time
from typing import Tuple, Iterable
from scipy.spatial import *
from PIL import Image
import io
import glob
import re

def get_serial_port() -> str:

    myports = [tuple(p) for p in list(serial.tools.list_ports.comports())]
    myport = ""
    print(myports)
    for port in myports:
        if "Arduino Uno" in port[1]:
            myport = port[0]
            break
    print(f"Port selectionné : {myport}")
    return myport

def sram_read_new(filename : str = "save", port : str = None, rounds : int = 250) -> None:

    data = []
    if port is None:
        myport = get_serial_port()
    with Serial(port=myport, baudrate=115200, timeout=0.2, writeTimeout=1, ) as port_serie:
        if port_serie.isOpen():
            ligne = port_serie.readlines()
            while(not(ligne) or not(any(b"How many rounds" in elem for elem in ligne))):
                ligne = port_serie.readlines()
            port_serie.write(str(rounds).encode())
            print("[P] Round success")       

            for i in range(rounds): 
                ligne = port_serie.readlines()
                while(not ligne or (ligne[0] in [b'\x00', b'\r\n']) and len(ligne)<2):
                    ligne = port_serie.readlines()
                print(f"[+] Reading {i} done, checking ... ", end='')
                lines = ligne[2:]
                if lines[0]==b'1024\r\n':
                    lines = lines[1:]
                temp_array = []
                for line in lines:
                    temps = line.decode(encoding="ascii", errors="ignore")
                    temps = temps.split(" ")
                    assert(len(temps)==17)
                    for elem in temps[:-1]:
                        if len(elem)==1:
                            temp_array += [0]*4
                            temp_array += list(map(lambda x: int(x), '{0:04b}'.format(int(elem[0], 16))))
                        else:
                            temp_array += list(map(lambda x: int(x), '{0:04b}'.format(int(elem[0], 16))))
                            temp_array += list(map(lambda x: int(x), '{0:04b}'.format(int(elem[1], 16))))
                data.append(temp_array)
                print("Done")

    np_data = np.array(data)
    print(np_data.shape)
    np.save(filename, np_data)

def sram_read_y(filename : str = "save", port : str = None, rounds : int = 250, y : int = 2048) -> None:

    data = []
    if port is None:
        myport = get_serial_port()
    with Serial(port=myport, baudrate=115200, timeout=0.2, writeTimeout=1, ) as port_serie:
        if port_serie.isOpen():
            ligne = port_serie.readlines()
            while(not(ligne) or not(any(b"How many rounds" in elem for elem in ligne))):
                ligne = port_serie.readlines()
            port_serie.write(str(rounds).encode())
            print("[P] Round success")       
                 
            ligne = port_serie.readlines()
            while(not(ligne) or not(any(b"Give y" in elem for elem in ligne))):
                ligne = port_serie.readlines()
            port_serie.write(str(y).encode())
            print("[P] sY success")       

            for i in range(rounds): 
                try:
                    ligne = port_serie.readlines()
                    while(not ligne or (ligne[0] in [b'\x00', b'\r\n']) and len(ligne)<2):
                        ligne = port_serie.readlines()
                    print(f"[+] Reading {i} done, checking ... ", end='')
                    lines = ligne[2:]
                    if lines[0]==b'1024\r\n':
                        lines = lines[1:]
                    temp_array = []
                    for line in lines:
                        temps = line.decode(encoding="ascii", errors="ignore")
                        temps = temps.split(" ")
                        if len(temps)!=17:
                            print(temps)
                            print(lines)
                            assert(len(temps)==17)
                        for elem in temps[:-1]:
                            if len(elem)==1:
                                temp_array += [0]*4
                                temp_array += list(map(lambda x: int(x), '{0:04b}'.format(int(elem[0], 16))))
                            else:
                                temp_array += list(map(lambda x: int(x), '{0:04b}'.format(int(elem[0], 16))))
                                temp_array += list(map(lambda x: int(x), '{0:04b}'.format(int(elem[1], 16))))
                    data.append(temp_array)
                    print("Done")
                except:
                    print("ERROR")

    np_data = np.array(data)
    print(np_data.shape)
    np.save(filename, np_data)



def find_square(index: int) -> int:
    """Find the bigger dimension to have a perfect square (for visualisation)

    :param index: array length
    :type index: int
    :return: new array length, smaller
    :rtype: int
    """

    return int(np.power(np.floor(np.sqrt(index)), 2))

def get_proba_array(x: np.ndarray) -> np.ndarray:
    """Given an array, compute the max probability of each element keeping the same value

    :param x: array of observations
    :type x: np.ndarray
    :return: array of probabilities
    :rtype: np.ndarray
    """
    length = find_square(x.shape[1])
    nbins = x.max() + 1
    ncols = length
    count = np.zeros((nbins, ncols), dtype=int)
    colidx = np.arange(ncols)[None, :]
    np.add.at(count, (x[:,:length], colidx), 1)
    return np.maximum(count[0], count[1])/(count[0] + count[1]), length

def compare_arrays_flipping_bytes(display_array1: np.ndarray, display_array2: np.ndarray, name: str) -> None:
    """Display a comparaison graph

    :param display_array1: display array previously generated
    :type display_array1: np.ndarray
    :param display_array2: display array previously generated
    :type display_array2: np.ndarray
    :param name: name of the file (without extension)
    :type name: str
    """

    #count noisy bits flipped 
    diff = np.where(display_array1!=display_array2)
    counter = 0
    for ind in diff[0]:
        if display_array1[ind]==2 or display_array2[ind]==2:
            counter += 1
    print(f"Noisy bits flipped : {counter}\nTotal flipped bits : {len(diff[0])}")

    display_array1[np.where(display_array1!=display_array2)]=3
    display_array(display_array1, name, True)

def display_array(display_array: np.ndarray, name: str, display : bool = False) -> None:
    """Nice display

    :param display_array: display array previously generated
    :type display_array: np.ndarray
    """

    #Custom colormap
    cmap = colors.ListedColormap(['green', 'yellow', "white", "red"])
    bounds=[0,0.5,1.5,2.5,3.5]
    norm = colors.BoundaryNorm(bounds, cmap.N)

    """Old version
    plt.matshow(arr.reshape((90,90)), cmap=cmap, norm=norm)
    ax = plt.gca()
    ax.grid(color='b', linestyle='-', linewidth=1)
    plt.show()"""
    fig = plt.figure(figsize=(10,10))
    plt.pcolormesh(display_array.reshape((90,90)), edgecolors='k', linewidth=1, cmap=cmap, norm=norm)
    plt.axis('off')
    ax = plt.gca()
    ax.invert_yaxis()
    ax.set_aspect('equal')
    plt.box(False)
    plt.title(name)
    plt.savefig(name, dpi=plt.gcf().dpi, bbox_inches = 'tight', pad_inches=0.4)
    if display:
        plt.show()

def get_displayed_array(prob: np.ndarray, binary: np.ndarray, length: int) -> np.ndarray:
    """Transform the probabilities array into an array suited for visualization with fixed values for constant values of bits

    :param prob: probability array
    :type prob: np.ndarray
    :param binary: binary array
    :type binary: np.ndarray
    :param length: length given by find_square
    :type length: int
    :return: display suited array
    :rtype: np.ndarray
    """
    
    array = []
    binary_transpose = binary.T
    for proba, value in zip(prob, binary_transpose):
        if proba == 1.0 and value[0] == 0:
            array.append(0)
        elif proba == 1.0 and value[0] == 1:
            array.append(1)
        else:
            array.append(2)
    return np.array(array)

if __name__ == "__main__":
    """a = np.load("./new_nano_1.npy", allow_pickle=True)[1:]
    prob1, length1 = get_proba_array(a)
    display_array1 = get_displayed_array(prob1, a, length1)

    b = np.load("./new_nano_2.npy", allow_pickle=True)[1:]
    prob2, length2 = get_proba_array(b)
    display_array2 = get_displayed_array(prob2, b, length2)
    compare_arrays_flipping_bytes(display_array1, display_array2, "new_nano_flipping_1_2")
    """

    """    y_list = list(range(0,150)) + list(range(150, 250, 2)) + [1000]
    y_list = list(set(y_list))
    y_list.sort()

    for i in y_list:
        sram_read_y(filename=f"./Sy_test/test_y_{i}", rounds=25, y=i)"""
    sram_read_y(filename=f"./Sy_test/test_y_{4095}", rounds=25, y=4095)
    """#Get flipping bits
    a = np.load("./Sy_test/test_y_0.npy", allow_pickle=True)[1:]
    b = np.load("./Sy_test/test_y_230.npy", allow_pickle=True)[1:]
    prob1, length1 = get_proba_array(a)
    display_array1 = get_displayed_array(prob1, a, length1)

    prob2, length2 = get_proba_array(b)
    display_array2 = get_displayed_array(prob2, b, length2)

    #compare_arrays_flipping_bytes(display_array1, display_array2, "new_nano_flipping_1_2")
    
    diff = np.where(display_array1!=display_array2)[0]
    new_diff = []    
    for ind in diff:
        if display_array1[ind]!=2 and display_array2[ind]!=2:
            new_diff.append(ind)
    diff = np.array(new_diff)
    
    nb_flip = len(diff)

    #go through files
    files = glob.glob(".\\Sy_test/*.npy")
    max_n = len(files)

    matrix = np.zeros((nb_flip, max_n), dtype=int)
    new_y_list = []
    for measure in files:
        number = (int(re.findall(r'\.\\Sy_test\\test_y_([0-9]+)\.npy', measure)[0]))
        new_y_list.append(number)
    new_y_list.sort()
    print(new_y_list)

    for measure in files:
        try:
            number = new_y_list.index(int(re.findall(r'\.\\Sy_test\\test_y_([0-9]+)\.npy', measure)[0]))
            a = np.load(measure, allow_pickle=True)[1:]
            prob, length = get_proba_array(a)
            disp_array = get_displayed_array(prob, a, length)
            matrix[:,number] = disp_array[diff]
        except Exception as e:
            print(measure)
            print(e)

    #Custom colormap
    cmap = colors.ListedColormap(['green', 'yellow', "white", "red"])
    bounds=[0,0.5,1.5,2.5,3.5]
    norm = colors.BoundaryNorm(bounds, cmap.N)

    fig = plt.figure(figsize=(20,20))
    plt.pcolormesh(matrix[:,:], edgecolors='k', linewidth=0, cmap=cmap, norm=norm)
    plt.axis('off')
    ax = plt.gca()
    ax.invert_yaxis()
    ax.set_aspect('equal')
    plt.box(False)
    plt.show()"""
    