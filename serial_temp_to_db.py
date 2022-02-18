import serial
from pymongo import MongoClient
from datetime import datetime as dt
import time
import systemd.daemon

''' **************************************** '''

# Iniatilzation temperature. 0C looks better than a 'trash output'.
temp = 0

''' Constants '''
MAX_FERM_TEMP = 50
BAUD = 9600
PORT = "/dev/ttyUSB0"
READ_CMD = b'R'
MIN_FLOAT_LEN = 9
MAX_FLOAT_LEN = 11
IP_ADR = 27017
STARTUP_TESTS = 4

''' MongoDB '''
client = MongoClient('localhost', IP_ADR)
db = client.beertemp
collection = db.log
entry = db.entries

# Open serial connection to MCU
ser = serial.Serial(PORT, BAUD)

def get_temperature(temp):
    ser.write(bytes(READ_CMD))
    line = ser.readline().decode()
    if len(line) > MIN_FLOAT_LEN \
            and len(line)< MAX_FLOAT_LEN \
            and float(line.strip('\x00\n\r')) < MAX_FERM_TEMP:
        temp = (float(line.strip('\x00\n\r')))
    return temp

def temp_to_db(temp):
    temp_entry = {"temperature": get_temperature(temp),
            "time": dt.utcnow()} 
    entry.insert_one(temp_entry)

def init_script(temp):
    print('Running tests on port: ' + ser.portstr)
    print('using BAUD = ' + str(BAUD))
    for test in range(STARTUP_TESTS):
        try:
            time.sleep(0.5)
            ser.write(READ_CMD)
            line = ser.readline().decode()
            if len(line) > MIN_FLOAT_LEN \
                    and len(line)< MAX_FLOAT_LEN \
                    and float(line.strip('\x00\n\r')) < MAX_FERM_TEMP:
                print('OK Reading ' + str(test) + ': ' + line.strip('\x00\n\r'))
            else:
                print('Faulty reading ' + str(test) + ': ' + line)
        except Exception as e:
            raise e
    systemd.daemon.notify('READY=1')

def main():
    init_script(temp)
    while True:
        time.sleep(60)
        # time.sleep(60)
        # print('Hello Lennart!')
        try:
            temp_to_db(temp)
        except Exception as e:
            print(str(e))
''' **************************************** '''

if __name__ == "__main__":
    ''' Wait for DB and Serial init '''
    time.sleep(2)
    main()
