"""
Original: Shelley Pham
New Author: Shubham Naik
"""

from __future__ import print_function
import httplib2
import os
import re
import time
import base64

from apiclient import discovery
from apiclient import errors
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText




# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-python-quickstart.json
SCOPES = 'https://mail.google.com/'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Gmail API Python Quickstart'


def get_credentials():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'gmail-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        print('Your credentials are invalid, please run "python ./src/auth.py!")
    return credentials

def create_message(sender, to, subject, message_text):
  message = MIMEText(message_text, 'html')
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject
  return {'raw': base64.urlsafe_b64encode(message.as_string())}

def send_message(service, user_id, message):
  try:
    message = (service.users().messages().send(userId=user_id, body=message)
               .execute())
    print ('Message Id: %s' % message['id'])
    return message
  except errors.HttpError, error:
    print ('An error occurred: %s' % error)


def main():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)

    email_list = sys.argv[1];
    email_template = open('message.txt', 'r').read()

    email_subject = "Greetings! Quick Question?";

    email_contents = email_template;
    encoded_message = create_message('Shubham Naik <shubham.naik10@gmail.com>', email_list, email_subject, email_contents)
    send_message(service, 'me', encoded_message)

    print ("Email sent to ", email_list)


if __name__ == '__main__':
    main()
