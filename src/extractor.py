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

    new_file = [x.rstrip().decode(errors="ignore") for x in serial_txt if x not in [b'\x00', b'\r\n']]
    assert('BEGINNING' in new_file[0])
    memory_size = int(new_file[1])+1
    mem = np.zeros(memory_size, dtype=np.int16)
    i=0
    for line in new_file[2:]:
        elements = line.split(" ")
        for elem in elements:
            if 'How' in elements[0]:
                continue
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
    print(myports)
    for port in myports:
        if "Arduino Uno" in port[1]:
            myport = port[0]
            break
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

def sram_read_y(filename : str = "save", port : str = None, rounds : int = 250, y : float = 0.5) -> None:

    data = []
    if port is None:
        myport = get_serial_port()
    with Serial(port=myport, baudrate=57600, timeout=0.5, writeTimeout=1, ) as port_serie:
        if port_serie.isOpen():
            ligne = port_serie.readlines()
            print(ligne)
            ligne = port_serie.readlines()
            print(ligne)
            ligne = port_serie.readlines()
            print(ligne)
            ligne = port_serie.readlines()
            print(ligne)
            port_serie.write(str(rounds).encode())
            ligne = port_serie.readlines()
            while(not(ligne)):
                ligne = port_serie.readlines()
            print(ligne)
            port_serie.write(str(y).encode())

            for i in range(rounds): 
                ligne = port_serie.readlines()
                print(ligne)
                while(not ligne or (ligne[0] in [b'\x00', b'\r\n']) and len(ligne)<2):
                    ligne = port_serie.readlines()
                    print(ligne)
                data.append(ligne)

    np_data = np.array(data)
    np.save("./Sy_test/"+filename, np_data)


def get_arrays_from_save(a : np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """Transform the saved npy file, already loaded, to 2 arrays of the dump sram values
    The hexa array is a int array with values of bytes
    The binary array, 8 times bigger, is a int array with the bit values
    //TODO: hexa array not implemented

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

def compare_arrays(display_array1: np.ndarray, display_array2: np.ndarray, name: str) -> None:
    """Display a comparaison graph

    :param display_array1: display array previously generated
    :type display_array1: np.ndarray
    :param display_array2: display array previously generated
    :type display_array2: np.ndarray
    :param name: name of the file (without extension)
    :type name: str
    """
    
    buf1 = io.BytesIO()
    buf2 = io.BytesIO()
    buf3 = io.BytesIO()

    display_array(display_array1, buf1, False)
    display_array(display_array2, buf2, False)

    a = np.count_nonzero(display_array1==display_array2)
    b = len(display_array1) - a
    fig = plt.figure(figsize=(10,10))
    patches, texts, _ = plt.pie([a, b], autopct="%1.1f%%", wedgeprops=dict(width=0.5), textprops={'fontsize': 18})
    plt.legend(patches, ('Same bit', 'Different bit'), loc="best", prop={'size': 20})
    plt.savefig(buf3, dpi=plt.gcf().dpi, bbox_inches = 'tight', pad_inches=0.4)

    buf1.seek(0)
    buf2.seek(0)
    buf3.seek(0)
    im1 = Image.open(buf1)
    im2 = Image.open(buf2)
    im3 = Image.open(buf3)

    dst = Image.new('RGB', (im1.width + im2.width + im2.width, im1.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))
    dst.paste(im3, (im1.width + im2.width, 0))
    dst.save(f'{name}.png')
    buf1.close()
    buf2.close()
    buf3.close()

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


def proba_test(serial_txt: np.ndarray) -> np.ndarray:
    """TODO

    :param serial_txt: array of strings representing the serial transmission
    :type serial_txt: np.ndarray
    :return: TODO
    :rtype: np.ndarray
    """

    array = np.zeros(16)
    new_file = [x.rstrip().decode(errors="ignore") for x in serial_txt if x not in [b'\x00', b'\r\n']]
    print(new_file[0])
    assert('BEGINNING' in new_file[0])
    memory_size = int(new_file[1])+1
    mem = np.zeros(memory_size, dtype=np.int16)
    i=0
    for line in new_file[2:]:
        elements = line.split(" ")
        for elem in elements:
            if len(elem)==1:
                print(elem)
                array[int(elem[0],16)] += 1
                array[0] += 1
            else:
                array[int(elem[0],16)] += 1
                array[int(elem[1],16)] += 1
            i+=1
    return array

def autocorr(x):
    result = np.correlate(x, x, mode='full')
    return result[result.size//2:]


def aaafft(cor):
    N = len(cor)
    Y    = np.fft.fft(cor)
    freq = np.fft.fftfreq(len(cor), 1)

    plt.bar( freq, np.abs(Y), 1/N)
    plt.title("FFT autocorellation nano 2")
    plt.show()


if __name__ == "__main__":
    
    for i in range(0, 500, 2):
        sram_read_y(filename=f"test_y_{i}", rounds=20, y=i/4096)

    """#Get flipping bits
    a = np.load("./new_test_flipping_fac2.npy", allow_pickle=True)[1:]
    b = np.load("./new_test_flipping_fac5.npy", allow_pickle=True)[1:]

    _, binary_array = get_arrays_from_save(a)
    prob, length = get_proba_array(binary_array)
    display_array1 = get_displayed_array(prob, binary_array, length)

    _, binary_array2 = get_arrays_from_save(b)
    prob2, length = get_proba_array(binary_array2)
    display_array2 = get_displayed_array(prob2, binary_array2, length)

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
    for measure in files:
        number = int(re.findall(r'\.\\Sy_test\\test_y_([0-9]+)\.npy', measure)[0])//2
        a = np.load(measure, allow_pickle=True)[1:-1]
        _, binary_array = get_arrays_from_save(a)
        prob, length = get_proba_array(binary_array)
        disp_array = get_displayed_array(prob, binary_array, length)
        matrix[:,number] = disp_array[diff]

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

    """a = np.load("./new_test_flipping_fac2.npy", allow_pickle=True)[1:]
    b = np.load("./new_test_flipping_fac5.npy", allow_pickle=True)[1:]

    _, binary_array = get_arrays_from_save(a)
    prob, length = get_proba_array(binary_array)
    disp_array = get_displayed_array(prob, binary_array, length)

    _, binary_array2 = get_arrays_from_save(b)
    prob2, length = get_proba_array(binary_array2)
    disp_array2 = get_displayed_array(prob2, binary_array2, length)

    compare_arrays_flipping_bytes(disp_array, disp_array2, "nanoNew_flipping_2_5")"""
    """a = binary_array[5].copy()
    a[np.where(a==0)] = -1
    print(np.mean(a))
    auto = autocorr(a) / autocorr(a)[0]
    plt.plot(range(len(auto)), auto)
    plt.title("Autocorellation Nano 2")
    plt.show()
    aaafft(auto)"""
    """b= proba_test(a[0])

    plt.bar( [hex(i) for i in range(16)] , b)
    plt.title("Distribution des nibbles sur uno2")
    plt.show()"""
        
    """    prob, length = get_proba_array(binary_array)
        disp_array = get_displayed_array(prob, binary_array, length)
        print(100 * np.count_nonzero(disp_array==0) / disp_array.shape[0])
        print(100 * np.count_nonzero(disp_array==1) / disp_array.shape[0])
        print(np.count_nonzero(disp_array==2))
        display_array(disp_array, "test", True)
        _, binary_array2 = get_arrays_from_save(b)
        prob2, length = get_proba_array(binary_array2)
        disp_array2 = get_displayed_array(prob2, binary_array2, length)
        print(100 * np.count_nonzero(disp_array2==0) / disp_array2.shape[0])
        print(100 * np.count_nonzero(disp_array2==1) / disp_array2.shape[0])
        print(100 * np.count_nonzero(disp_array2==2) / disp_array2.shape[0])
        compare_arrays(disp_array, disp_array2, "concat")
    """