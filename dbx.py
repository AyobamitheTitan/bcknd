import os
from dropbox import DropboxOAuth2FlowNoRedirect

auth_flow = DropboxOAuth2FlowNoRedirect(os.getenv("DROPBOX_APP_KEY"), os.getenv("DROPBOX_APP_SECRET"), token_access_type='offline')
authorize_url = auth_flow.start()
print("1. Go to:", authorize_url)
print('2. Click "Allow" (you might have to log in first).')
print('3. Copy the authorization code.')
auth_code = input("Enter the authorization code here: ").strip()