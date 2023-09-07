import socket, os

def getDataFileList():
    global connected
    s.send(b'1\n')
    resp, endresp = b'', b'endList\n'
    while len(resp) < len(endresp) and resp[-len(endresp):] != endresp:
        resp += s.recv(1000)
        if resp == b'':
            connected == False
            print('dataFileList : server socket closed')
            return
    fileList =  resp.decode().split('\n')
    return fileList[:-2]

def dataFileList():
    if not connected: return
    fileList = getDataFileList()
    for file in fileList:
        print(file)

def deleteDataFile():

    def removeFile(file):
        s.send(b'2\n')
        s.send(file.encode() + b'\n')
        resp = s.recv(1000)
        print(resp.decode())

    global connected

    while True:
        fileList = getDataFileList()
        try:
            while (filenb := int(input('file number (999=all, ctrl-C=back) : '))) not in range(1000):
                pass
            if filenb == 999:
                for file in fileList:
                    removeFile(file)
            elif (filename := 'MPU6050_{:03d}.dat'.format(filenb)) in fileList:
                removeFile(filename)
            else:
                print('{} does not exist'.format(filename))

        except KeyboardInterrupt:
            print('')
            return

def recordData():
    global connected

    try:
        while (filenb := int(input('new file number (ctrl-C = last+1) : '))) not in range(1000):
            pass
        filename = 'MPU6050_{:03d}.dat'.format(filenb)
        filename = filename.encode() + b'\n'
    except KeyboardInterrupt:
        print('')
        filename = b'new\n'
    s.send(b'3\n')
    s.send(filename)
    print(s.recv(100).decode())

def stop():
    global connected
    s.close()
    connected = False

def recvData():

    def getFile(filename):
        s.send(b'4\n')
        s.send(filename.encode() + b'\n')
        fd = open(filename, 'wb')
        buf = b''
        while len(buf) < 14 or (buf[-13:] != b'data file end' and buf[-14:] != b'sendFile error'):
            buf += s.recv(24)
        if buf[-13:] == b'data file end':
            fd.write(buf[:-13])
            print('file {} received, {} bytes'.format(filename, len(buf)-13))
            fd.close()
        else:
            print('server error, file {} not received'.format(filename))
            fd.close()
            os.remove(filename)

    fileList = getDataFileList()
    for file in fileList:
        print(file)

    while True:
        try:
            while (filenb := int(input('file number (ctrl-C = abort) : '))) not in range(1000):
                pass
            if (filename := 'MPU6050_{:03d}.dat'.format(filenb)) not in fileList:
                print('{} does not exist'.format(filename))
            else:
                getFile(filename)
                break
        except KeyboardInterrupt:
            break

# os.chdir('MyDir')
cmdList = {'1':dataFileList, '2':deleteDataFile, '3':recordData,  '4':recvData,  '5':stop}
host, port = '192.168.4.1', 18000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print('Connecting...')
s.connect((host, port))
print('Connected to server {}:{}'.format(host, port))
connected = True

while connected:
    cmd = input('command (1:file list  2:delete file  3:record  4:get file  5:stop  cmd:any repl command) : ')
    if cmd == 'stop':
        s.close()
        print('Disconnected from server')
        break
    if cmd in cmdList.keys():
        func = cmdList[cmd]
        func()
    else:
        s.send(cmd.encode() + b'\n')
        print(s.recv(1000).decode())

del s
