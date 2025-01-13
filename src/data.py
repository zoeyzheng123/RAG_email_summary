import base64


# Assuming creds is the authorized credentials object
def obtain_email_details(service, message_id):
    try:
        # Get the email message
        msg = service.users().messages().get(userId='me', id=message_id).execute()
        # Initialize email details
        email_details = {
            'subject': None,
            'sender': None,
            'recipient': None,
            'content': None,
            'date': None,
        }

        # Parse the message headers to get subject, sender, and recipient
        for header in msg['payload']['headers']:
            if header['name'] == 'Subject':
                email_details['subject'] = header['value']
            elif header['name'] == 'From':
                email_details['sender'] = header['value']
            elif header['name'] == 'To':
                email_details['recipient'] = header['value']

        # Check if there is the 'body' in the message payload
        if 'parts' in msg['payload']:
            for part in msg['payload']['parts']:
                if part['mimeType'] == 'text/plain':  # Extract plain text content
                    data = part['body'].get('data')
                    if data:
                        email_details['content'] = base64.urlsafe_b64decode(data).decode('utf-8')
                elif part['mimeType'] == 'text/html':  # If HTML content is available
                    data = part['body'].get('data')
                    if data:
                        email_details['content'] = base64.urlsafe_b64decode(data).decode('utf-8')

        # If no plain text or HTML, check for body in message
        elif 'body' in msg['payload']:
            data = msg['payload']['body'].get('data')
            if data:
                email_details['content'] = base64.urlsafe_b64decode(data).decode('utf-8')
        return email_details

    except Exception as error:
        print(f"An error occurred: {error}")
        return None


