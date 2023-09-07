import os
import network, socket
from machine import Pin, SoftI2C
from time import ticks_us, sleep_ms
from struct import pack, unpack
from MPU6050dmp20 import *

def getMessage():
    ''' read message from server '''
    return conn.readline()  # blocking

def listDataFiles():
    fileList = []
    for file in os.listdir():
        if file[:8] == 'MPU6050_' and file[-4:] == '.dat':
            fileList.append(file)
    return fileList

def sendDataFileList():
    fileList = listDataFiles()
    for file in fileList:
        conn.send(file.encode() + b'\n' )
    conn.send(b'endList\n')

def deleteDataFile():
    file = getMessage().strip()
    file = file.decode()
    fileList = listDataFiles()
    if file in fileList:
        os.remove(file)
        print('file {} removed'.format(file))
        conn.send(b'file {} removed'.format(file))
    else:
        print('error, file {} not removed'.format(file))
        conn.send(b'error, file {} not removed'.format(file))

def getNewDataFileName():
    newnum = 0
    for file in os.listdir():
        if file[:8] == 'MPU6050_' and file[-4:] == '.dat':
            if (num := int(file[8:-4])) >= newnum:
                newnum = num + 1
    return 'MPU6050_{:03d}.dat'.format(newnum)

def recordData():
    global wait, full
    # create new data file
    file = getMessage().decode().strip()
    if file == 'new': file = getNewDataFileName()
    fd = open(file, 'wb')
    # start dmp
    mpu.resetFIFO()
    start_time = ticks_us()
    # record data
    count = 0
    while count < npts:
        if (nb := mpu.getFIFOCount()) > 42:
            if nb == 1024:
                full += 1
            buf = mpu.getFIFOBytes(42)
            data = buf[0:2] + buf[4:6] + buf[8:10] + buf[12:14] # quaternion
            data += buf[16:18] + buf[20:22] + buf[24:26]        # gyro
            data += buf[28:30] + buf[32:34] + buf[36:38]        # accel
            data += pack('I', ticks_us()-start_time)            # time
            fd.write(data)
            count += 1
        else:
            wait += 1
    #  
    fd.close()
    conn.send('file {} created'.format(file).encode())

def sendFile():
    file = getMessage().decode().strip()
    print('sending file {}'.format(file))
    try:
        fd = open(file, 'rb')
        n = 0
        while buf := fd.read(24):
            conn.sendall(buf)
            n += 24
        fd.close()
        conn.send(b'data file end')
        print('file {} sent successfully, {} bytes'.format(file, n))
    except:
        print('sendFile error')
        conn.send(b'sendFile error')
#
i2c = SoftI2C(scl=Pin(2),sda=Pin(0),freq=400_000)
mpu = MPU6050dmp(i2c, axOff=-914, ayOff=683, azOff=1173, gxOff=530, gyOff=-31, gzOff=45)
mpu.dmpInitialize()
mpu.setDMPEnabled(True)
mpu.getIntStatus()
#
npts, count, wait, full = 1000, 0, 0, 0
#
messDict = {b'1\n':sendDataFileList , b'2\n':deleteDataFile , b'3\n':recordData, b'4\n':sendFile }
# activate access point
ap = network.WLAN(network.AP_IF)
ap.active(True)
# activate server
host, port = '192.168.4.1', 18000
soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.bind((host, port))
soc.listen(1)
#
while True:
    
    conn, addr = soc.accept()
    print('Client {} connected'.format(addr))
    connected = True

    while connected:
        try:
            mess = getMessage()   # blocking
            if mess == b'':
                print('Client socket closed, Client {} disconnected'.format(addr))
                connected = False
        except:
            print('getMessage error')
            conn.close()
            connected = False
        if mess in messDict.keys():
            func = messDict[mess]
            func()
        else:
            try:
                exec(mess)       # repl command received
                conn.send('{} exec ok\n'.format(mess).encode())
            except:
                conn.send('{} exec error\n'.format(mess).encode())