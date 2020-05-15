import numpy as np
from serial import *
import matplotlib.pyplot as plt
from matplotlib import colors
import serial.tools.list_ports
import time
from typing import Tuple

def get_mem_matrix(file: str) -> np.ndarray:
    """[Depreciated] Convert a serial transmission log into a matrix of bytes

    :param file: path of the file
    :type file: str
    :return: flat array of bytes 
    :rtype: np.ndarray
    """

    #FIXME: size
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

def get_serial_matrix(serial_txt: np.ndarray) -> np.ndarray:
    """Convert a serial transmission (array of string) into a matrix of bytes

    :param serial_txt: array of strings representing the serial transmission
    :type serial_txt: np.ndarray
    :return: array of bytes
    :rtype: np.ndarray
    """

    new_file = [x.rstrip().decode() for x in serial_txt if x not in [b'\x00', b'\r\n']]
    assert('BEGINNING' in new_file[0])
    memory_size = int(new_file[1])+1
    mem = np.zeros(memory_size, dtype=np.int16)
    i=0
    for line in new_file[2:]:
        elements = line.split(" ")
        for elem in elements[:-1]:
            mem[i] = int(elem, 16)
            i+=1
    return mem

def get_serial_port() -> str:
    """Get the serial port associated to the Arduino Uno (to adapt if not an uno)

    :return: port name
    :rtype: str
    """
    myports = [tuple(p) for p in list(serial.tools.list_ports.comports())]
    myport = ""
    for port in myports:
        if "Arduino Uno" in port[1]:
            myport = port[0]
            break
    assert(myport)
    print(f"Port selectionné : {myport}")
    return myport

def sram_read(filename : str = "save", port : str = None, rounds : int = 250) -> None:
    """Get [rounds] dump of a part of the SRAM of the arduino

    :param filename: name of the save, defaults to "save"
    :type filename: str, optional
    :param port: serial port, defaults to None
    :type port: str, optional
    :param rounds: number of sram dump, defaults to 250
    :type rounds: int, optional
    """

    data = []
    if port is None:
        myport = get_serial_port()
    with Serial(port=myport, baudrate=57600, timeout=0.5, writeTimeout=1, ) as port_serie:
        if port_serie.isOpen():
            ligne = port_serie.readlines()
            ligne = port_serie.readlines()
            ligne = port_serie.readlines()
            ligne = port_serie.readlines()
            port_serie.write(str(rounds).encode())

            for i in range(rounds): 
                ligne = port_serie.readlines()
                while(not ligne or (ligne[0] in [b'\x00', b'\r\n']) and len(ligne)<2):
                    ligne = port_serie.readlines()
                    print(ligne)
                data.append(ligne)

    np_data = np.array(data)
    np.save(filename, np_data)


def get_arrays_from_save(a : np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """Transform the saved npy file, already loaded, to 2 arrays of the dump sram values
    The hexa array is a int array with values of bytes
    The binary array, 8 times bigger, is a int array with the bit values

    :param a: already loaded npy file
    :type a: np.ndarray
    :return: "hexa" and binary array
    :rtype: Tuple[np.ndarray, np.ndarray]
    """

    new = []
    for elem in a:
        new.append(get_serial_matrix(elem))
    hexa_array = np.array(elem)
    binary_array = []
    for elem in new:
        to_add = []
        for item in elem:
            to_add += list(map(lambda x: int(x), '{0:08b}'.format(item)))
        binary_array.append(to_add)
    binary_array = np.array(binary_array)
    return hexa_array, binary_array


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

def display_array(display_array: np.ndarray) -> None:
    """Nice display

    :param display_array: display array previously generated
    :type display_array: np.ndarray
    """

    #Custom colormap
    cmap = colors.ListedColormap(['green', 'yellow', "white"])
    bounds=[0,0.5,1.5,3]
    norm = colors.BoundaryNorm(bounds, cmap.N)

    """Old version
    plt.matshow(arr.reshape((90,90)), cmap=cmap, norm=norm)
    ax = plt.gca()
    ax.grid(color='b', linestyle='-', linewidth=1)
    plt.show()"""

    plt.rcParams["figure.figsize"] = (10,10)
    plt.pcolormesh(display_array.reshape((90,90)), edgecolors='k', linewidth=1, cmap=cmap, norm=norm)
    plt.axis('off')
    ax = plt.gca()
    ax.invert_yaxis()
    ax.set_aspect('equal')
    plt.box(False)
    plt.savefig('save.png')
    plt.show()

if __name__ == "__main__":

    a = np.load("save.npy", allow_pickle=True)
    _, binary_array = get_arrays_from_save(a)
    prob, length = get_proba_array(binary_array)
    disp_array = get_displayed_array(prob, binary_array, length)
    display_array(disp_array)
