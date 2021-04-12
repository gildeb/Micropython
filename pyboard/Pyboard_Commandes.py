import sys, serial
from serial.tools.list_ports import comports
from time import sleep

def initUSB(port=None):
    ''' Initialisation du port série'''
    for p in comports():
        if port == None or port == p.device:
            try:
                s = serial.Serial(p.device,115200, write_timeout=2.)
                sleep(0.1)
                while s.in_waiting:
                    s.flushInput()
                    sleep(1)
                # print('s.in_waiting',s.in_waiting)
                s.write(b'\x03')
                sleep(0.1)
                ans = b''
                while s.in_waiting:
                    ans += s.read(s.in_waiting)
                    sleep(3)
                # print('s.in_waiting',s.in_waiting)
                # print('prompt',ans)
                if len(ans) >= 6 and ans[-6:] == b'\r\n>>> ':
                    replCmd(s,b'import os')
                    sleep(0.1)
                    s.flushInput()
                    ans, = replCmd(s,b'os.uname().machine', return_ans=True)
                    board = ans.decode().strip('"')
                    print(board + ' found on port', p.device)
                    return s
                else:
                    s.close()
            except:
                pass
    print('No Micropython board found!')
    return None

def replCmd(s,cmd, return_ans=False):
    ''' Envoi d'une commande à l'interface REPL de la pyboard

    Arguments:
        s = decsripteur du port serie renvoyé par initUSB

        cmd = commande pyboard, de la forme b'commande'

    Renvoie la liste des lignes de la reponse console'''
    # on verifie que le buffer d'entrée est vide
    if s.in_waiting != 0:
        s.read(s.in_waiting)   # on vide le buffer d'entrée
    # execution de la commande
    s.write(cmd+b'\r')
    ans = b''
    ans = ans.strip(cmd)
    while b'>>> ' not in ans:
        ans += s.read(s.inWaiting())
    ans = ans.strip(cmd+b'\r\n')
    ans = ans.strip(b'\r\n>>> ')
    # return ans.split(b'\r\n')
    ans =  ans.split(b'\r\n')
    if return_ans:
        return ans
    else:
        for line in ans:
            print(line.decode())

def reset(s):
    ''' Reset de la pyboard'''
    s.write(b'pyb.hard_reset()\r')

def pybRestart(s):
    ''' Reset de la Pyboard avec réinitialisation du port série
        Renvoie l'identifiant serial s

        Fonctionne sur MacOs uniquement
        '''
    reset(s)
    sleep(5)
    s.close()
    return initUSB()