import serial
from pymongo import MongoClient
from datetime import datetime as dt
import time
import systemd.daemon
import os.path
import base64
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

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
CORRECT_TESTS = 3

''' MongoDB '''
client = MongoClient('localhost', IP_ADR)
db = client.beertemp
entry = db.entries
settings = db.settings

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
    print('Baud rate = ' + str(BAUD))
    correct_count = 0
    faulty_count = 0
    while correct_count != CORRECT_TESTS:
        try:
            time.sleep(0.5)
            ser.write(READ_CMD)
            line = ser.readline().decode()
            if len(line) > MIN_FLOAT_LEN \
                    and len(line)< MAX_FLOAT_LEN \
                    and float(line.strip('\x00\n\r')) < MAX_FERM_TEMP:
                print('Correct reading: ' + line.strip('\x00\n\r'))
                correct_count+=1
            else:
                print('Faulty reading: ' + line.strip('\x00\n\r'))
                faulty_count+=1
        except Exception as e:
            raise e
    print('Passed init tests on ' + str(correct_count) + \
            ' correct readings and ' + str(faulty_count) + ' faulty readings')
    systemd.daemon.notify('READY=1')

def detect_temp_drop():
    # Return list of the two latest temperatures using natural ordering
    diff_entries = list(entry.find().sort('$natural',-1).limit(2))

    temp_1 = diff_entries[0]['temperature']
    temp_2 = diff_entries[1]['temperature']

    date_1 = diff_entries[0]['time'].date()
    date_2 = diff_entries[1]['time'].date()
   
    # Return temp drop tolerance
    drop_tol = int(settings.find_one({"_id": "settings"})['drop'])

    # Check temp drop tolerance only if the two entries has same date
    if date_1 == date_2:
        temp_drop = temp_2 - temp_1
        if temp_drop > drop_tol:
            send_warning(drop_tol, temp_drop, date_1)

def create_message(sender, to, subject, message_text):
  message = MIMEText(message_text)
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject
  return {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}

def send_warning(drop_tol, temp_drop, date_1):
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('/home/alarm/token.json'):
        creds = Credentials.from_authorized_user_file('/home/alarm/token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '/home/alarm/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)
        to = "forsman.august@gmail.com"
        sender = "beermail2022@gmail.com"
        user_id = "me"
        subject = "Beer Temperature Warning"
        message_text = "WARNING, AUGUST!\nTemperature has dropped: " + str(temp_drop) + "C\nbetween the last two readings."
        message = create_message(sender, to, subject, message_text)
        # send_message(service, user_id, message)

    except HttpError as error:
        print(error)

def send_message(service, user_id, message):
  try:
    message = (service.users().messages().send(userId=user_id, body=message)
               .execute())
    print('Warning message sent')
    print(message['id'])
    return message
  except HttpError as error:
    print(error)

def main():
    init_script(temp)
    while True:
        time.sleep(10)
        try:
            temp_to_db(temp)
            detect_temp_drop()
            print("Current temp drop parameter: ")
            print(int(settings.find_one({"_id": "settings"})['drop']))
        except Exception as e:
            print(str(e))

''' **************************************** '''

if __name__ == "__main__":
    ''' Wait for DB and Serial init '''
    time.sleep(2)
    main()
