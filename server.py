# first of all import the socket library
import socket
import pickle

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-m", help="Client")
parser.add_argument("-i", help="Host Name")
parser.add_argument("-p", help="Port", type=int)
args = parser.parse_args()


def xor(a, b):
    result = []

    for i in range(1, len(b)):
        if a[i] == b[i]:
            result.append('0')
        else:
            result.append('1')

    return ''.join(result)



def mod2div(divident, divisor):
    pick = len(divisor)

    tmp = divident[0: pick]

    while pick < len(divident):

        if tmp[0] == '1':

            tmp = xor(divisor, tmp) + divident[pick]

        else: 
            tmp = xor('0' * pick, tmp) + divident[pick]

        pick += 1

    if tmp[0] == '1':
        tmp = xor(divisor, tmp)
    else:
        tmp = xor('0' * pick, tmp)

    checkword = tmp
    return checkword


def decodeData(data, key):
    l_key = len(key)

    appended_data = data + '0' * (l_key - 1)
    remainder = mod2div(appended_data, key)

    # Return the remainder
    return remainder
    '''
    print("Remainder : ", remainder)
    print("Encoded Data (Data + Remainder) : ",
          codeword)
    '''

# Creating Socket
s = socket.socket()
print ("Socket successfully created")

# reserve a port on your computer in our
# case it is 12345 but it can be anything
port = args.p

s.bind((args.i, args.p))

print ("socket binded to %s" % (port))
# put the socket into listening mode
s.listen(5)
print ("socket is listening")

c, addr = s.accept()
while True:
    # Establish connection with client.
    print('Got connection from', addr)
    arr = ['hello', socket.gethostname()]

    data_string = pickle.dumps(arr)
    
    c.sendall(data_string)
    
    # Get data from client
    data = c.recv(1024)


    myData = pickle.loads(data)

    # if not data:
    #     break

    key = "1001"

    ans = decodeData(myData[4], key)
    print(myData)

    if myData[3] == "exit":
        print('----')

    # If remainder is all zeros then no error occured
    temp = "0" * (len(key) - 1)
    if ans == temp:
        c.sendall("Received No error FOUND")
    else:
        c.sendall("Error in data")

c.close()
