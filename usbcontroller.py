import serial
import time

""" arduino = serial.Serial(port='COM4', baudrate=115200, timeout=.1) #initilise arduino object

def write_read(x):
    arduino.write(bytes(x, 'utf-8')) #send byte array to arduino
    time.sleep(0.05)
    data = arduino.readline() #read response
    return data
 """


def sendtaxelcount(taxelarray, debug=False):
    taxelcount = 0
    for row in taxelarray:
        for taxel in row:
            if str(taxel) == '1':
                taxelcount += 1
    taxelcount = '/v'+str(taxelcount)+'\n' #add identifiers to message
    print('Sent taxelcount: ',bytes(taxelcount, 'utf-8')) #print message sent to arduino

    if debug: 
        print('Sent taxelcount: ',bytes(taxelcount, 'utf-8')) #print message sent to arduino
        return 
"""     else:
        write_read(taxelcount) #return arduino response """
 
def sendtaxeldata(taxelarray, debug=False):
    newtaxelgroup = True
    taxelmessage = ''
    for row in taxelarray:
        for taxel in row:        
            if newtaxelgroup:
                taxelgroup = ''
            taxelgroup += str(taxel) #add taxel to binary taxel group of 4
            if len(taxelgroup) == 4:
                newtaxelgroup = True
            elif len(taxelgroup) != 4:
                newtaxelgroup = False
            if newtaxelgroup:
                taxelgroup = hex(int(taxelgroup, 2))[2:] #convert 4 taxels to single hex
                taxelmessage += taxelgroup
    taxelmessage = '/v'+str(taxelmessage)+'\n' #add identifiers to message
    print('Sent taxeldata: ',bytes(taxelmessage, 'utf-8')) #print message sent to arduino
 
    if debug: 
        print('Sent taxeldata: ',bytes(taxelmessage, 'utf-8')) #print message sent to arduino
        return 
"""     else:
        write_read(taxelmessage) #return the arduino repsonse     """