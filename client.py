# Import socket module
import socket               
import sys
import argparse
import pickle


def xor(a, b):
 
    # initialize result
    result = []
 
    # Traverse all bits, if bits are
    # same, then XOR is 0, else 1
    for i in range(1, len(b)):
        if a[i] == b[i]:
            result.append('0')
        else:
            result.append('1')
 
    return ''.join(result)
 
 
# Performs Modulo-2 division
def mod2div(divident, divisor):
 
    # Number of bits to be XORed at a time.
    pick = len(divisor)
 
    # Slicing the divident to appropriate
    # length for particular step
    tmp = divident[0 : pick]
 
    while pick < len(divident):
 
        if tmp[0] == '1':
 
            # replace the divident by the result
            # of XOR and pull 1 bit down
            tmp = xor(divisor, tmp) + divident[pick]
 
        else:   # If leftmost bit is '0'
            # If the leftmost bit of the dividend (or the
            # part used in each step) is 0, the step cannot
            # use the regular divisor; we need to use an
            # all-0s divisor.
            tmp = xor('0'*pick, tmp) + divident[pick]
 
        # increment pick to move further
        pick += 1
 
    # For the last n bits, we have to carry it out
    # normally as increased value of pick will cause
    # Index Out of Bounds.
    if tmp[0] == '1':
        tmp = xor(divisor, tmp)
    else:
        tmp = xor('0'*pick, tmp)
 
    checkword = tmp
    return checkword
 
# Function used at the sender side to encode
# data by appending remainder of modular divison
# at the end of data.
def encodeData(data, key):
 
    l_key = len(key)
 
    # Appends n-1 zeroes at end of data
    appended_data = data + '0'*(l_key-1)
    remainder = mod2div(appended_data, key)
 
    # Append remainder in the original data
    codeword = data + remainder
    return codeword    
    '''
    print("Remainder : ", remainder)
    print("Encoded Data (Data + Remainder) : ",
          codeword)
    '''





# Create a socket object
s = socket.socket()         
 
# Define the port on which you want to connect
port = 12345               
 
# connect to the server on local computer
s.connect(('localhost', port))
s.settimeout(10)

# Send data to server 'Hello world'

## s.sendall('Hello World')
x = pickle.loads(s.recv(64))
print(x[0])


while True:
    input_string = raw_input("Enter data you want to send->")
    if input_string == "exit":
        s.close
        break
    #s.sendall(input_string)
    data =(''.join(format(ord(x), 'b') for x in input_string))
    print (data)
    key = "1001"

    ans = encodeData(data,key)
    #s.sendall(ans)

    ip = socket.gethostname() 
    print("host : ",ip)

    length  = 1024
    destination_address = x[1]
    source_address = ip
    payload = input_string 
    crc = ans

    #Buffer size
    BUFFER_SIZE = 1024

    packet = [BUFFER_SIZE,destination_address,source_address,payload,crc]

    data_string = pickle.dumps(packet)

    s.sendall(data_string)

    # receive data from the server
    print (s.recv(1024))

    # close the connection
s.close()
