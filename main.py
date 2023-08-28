from __future__ import print_function

import re

from helpers import *
from response_generation import respond

import os.path
import base64
import time
import email

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# email: offerslowincome@gmail.com

def authenticate():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return creds


def extract_html_payload(mime_msg):
    html = ""
    message_main_type = mime_msg.get_content_maintype()
    if message_main_type == 'multipart':
        for part in mime_msg.get_payload():
            if part.get_content_maintype() == 'text':
                html += part.get_payload()
    elif message_main_type == 'text':
        html += mime_msg.get_payload()

    return html


def get_job_category(html):
    if "Od 0 K=C4=8D, Zkr" in html:
        return "part_time"
    elif "Od 50 000 K=C4=8D, Pln=C3=BD =C3=BAvazek" in html:
        return "high_income"
    elif "Od 0 K=C4=8D, Pln=C3=BD =C3=BAvazek" in html:
        return "low_income"
    else:
        return "not_offer_email"

def get_unread_messages():
    try:
        # Call the Gmail API
        creds = authenticate()
        service = build('gmail', 'v1', credentials=creds)

        results = service.users().messages().list(userId='me',
                                                  labelIds=['INBOX'],
                                                  q="is:unread").execute()
        messages = results.get("messages", [])

        if messages:  # if some messages were found
            for i, message in enumerate(messages):  # go over all unread messages
                if i == 3: break

                msg = service.users().messages().get(userId='me',
                                                            id=message['id'],
                                                            format="raw").execute()

                mime_msg = email.message_from_bytes(base64.urlsafe_b64decode(msg['raw']))
                html = extract_html_payload(mime_msg)

                # extract relevant urls with job offerings
                pattern = r'"(http://tracking\.jobs\.cz[^"]*)"'
                job_urls = re.findall(pattern, html)
                job_urls = [url.strip().replace(" ", "")
                            .replace("=", "")
                            .replace("\r\n", "") for url in job_urls]

                category = get_job_category(html)

                if category == "not_offer_email":  # not an email from jobs cz
                    continue

                for url in job_urls:
                    respond(url, category)
                    print("DONE")

                time.sleep(1)
        else:
            print("no new messages")
            pass

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f'An error occurred: {error}')


if __name__ == '__main__':
    get_unread_messages()