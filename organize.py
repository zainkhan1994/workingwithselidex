from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os.path

# If modifying these SCOPES, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

def main():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)

    # Call the Drive v3 API
    results = service.files().list(
        pageSize=10, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))

if __name__ == '__main__':
    main()

from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

# Assuming you already have the 'credentials.json' file and token.pickle for authentication
creds = None
# Load the credentials from token.pickle
with open('token.pickle', 'rb') as token:
    creds = pickle.load(token)

# Build the service
service = build('drive', 'v3', credentials=creds)

# Get the About resource for the drive to access storage information
about = service.about().get(fields='storageQuota').execute()

# Retrieve storage quota information
storage_quota = about.get('storageQuota')
used_storage = storage_quota.get('usage')
total_storage = storage_quota.get('limit')

# Calculate the percentage usage (used storage is in bytes, convert to GB for readability)
used_gb = float(used_storage) / (1024*1024*1024)
total_gb = float(total_storage) / (1024*1024*1024)
percent_used = (used_gb / total_gb) * 100

# Print the storage usage details
print(f'You are currently using {used_gb:.2f} GB of {total_gb:.2f} GB.')
print(f'Percentage of storage used: {percent_used:.2f}%')
