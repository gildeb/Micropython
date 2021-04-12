#
#   Copy the lines below in boot.py and restart
#
#   execfile('filename') : execute the script contained in 'filename'
#
def execfile(filename):
    try:
        f = open(filename, 'r')
    except:
        print('Error opening ', filename)
        return
    try:
        exec(f.read())
    except:
        print('Error executing ', filename)
#