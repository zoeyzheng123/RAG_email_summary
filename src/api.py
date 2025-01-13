import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from langchain.schema import Document
from src.config import SCOPES, output_dir, cred_path
from src.transform import clean_content_with_ollama, parse_content
from src.data import obtain_email_details
from src.chroma import store_to_chroma

def download_creds(creds):
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            # your creds file here. Please create json file as here https://cloud.google.com/docs/authentication/getting-started
            "/Users/zeyi/Downloads/client_secret.json", SCOPES)
        creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(creds.to_json())


def fetch_and_store_emails(maxResults):
    creds = None
    emails = []
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        download_creds(creds)
    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)
        results = service.users().messages().list(userId='me', labelIds=['INBOX'],  maxResults=maxResults).execute()
        messages = results.get('messages',[])

        if not messages:
            print('No new messages.')
        else:
            for message in messages:
                email  = obtain_email_details(service, message['id'])
                content = email['content']

                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)

                if content:
                    content = parse_content(content)
                    file_name = os.path.join(output_dir, f"email_{message['id']}_original.txt")
                    # Save the email to a text file
                    with open(file_name, 'w', encoding='utf-8') as f:
                        f.write(content)
                    content = clean_content_with_ollama(content)

                subject = email['subject']
                sender = email['sender']

                # Format the text for the file
                email_text = f"Subject: {subject}\nSender: {sender}\nContent:\n{content}"
                metadata = {
                    'subject': email['subject'],
                    'sender': email['sender'],
                }
                doc = Document(page_content=email_text, metadata=metadata)
                emails.append(doc)
                # Define the file name
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                file_name = os.path.join(output_dir, f"email_{message['id']}.txt")

                # Save the email to a text file
                with open(file_name, 'w', encoding='utf-8') as f:
                    f.write(email_text)

        vectorstore = store_to_chroma(emails)
        return vectorstore
    except Exception as error:
        print(f'An error occurred: {error}')