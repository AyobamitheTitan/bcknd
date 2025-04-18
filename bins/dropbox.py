from datetime import datetime
from django.conf import settings
from dropbox import Dropbox, files, sharing
import requests


class DropboxService:
    def __init__(self):
        self.ACCESS_TOKEN = settings.DROPBOX_ACCESS_TOKEN
        self.AUTH_CODE = settings.DROPBOX_AUTH_CODE
        self.REFRESH_TOKEN = settings.DROPBOX_REFRESH_TOKEN
        self.APP_KEY = settings.DROPBOX_APP_KEY
        self.APP_SECRET = settings.DROPBOX_APP_SECRET

    def get_new_access_token(self):
        response = requests.post(
            'https://api.dropbox.com/oauth2/token',
            data={
                'grant_type': 'refresh_token',
                'refresh_token': self.REFRESH_TOKEN,
            },
            auth=(self.APP_KEY, self.APP_SECRET)
        )
        
        if response.status_code == 200:
            return response.json()['access_token']
        else:
            raise Exception(f"Token refresh failed: {response.text}")

    def initialize_dropbox_auth(self):
        auth_code = self.AUTH_CODE
        
        response = requests.post(
            'https://api.dropbox.com/oauth2/token',
            data={
                'code': auth_code,
                'grant_type': 'authorization_code',
                'client_id': self.APP_KEY,
                'client_secret': self.APP_SECRET,
                'redirect_uri': None
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            print("Access Token:", data['access_token'])
            print("Refresh Token:", data['refresh_token'])
        else:
            raise Exception(f"Auth failed: {response.text}")

    def store_file(self, file):
        dbx = self.get_dropbox_client()
        
        file_ext = file.name.split(".")[-1]
        file_name = f"/bins/{datetime.now().strftime('%Y%m%d_%H%M%S')}.{file_ext}"

        dbx.files_upload(file.read(), file_name, mode=files.WriteMode.overwrite)

        shared_link_metadata = dbx.sharing_create_shared_link_with_settings(
            file_name,
            settings=sharing.SharedLinkSettings(requested_visibility=sharing.RequestedVisibility.public)
        )

        raw_url = shared_link_metadata.url
        direct_url = raw_url.replace("www.dropbox.com", "dl.dropboxusercontent.com").replace("?dl=0", "")

        return direct_url
    
    def get_dropbox_client(self):
        try:
            dbx = Dropbox(self.ACCESS_TOKEN)
            dbx.users_get_current_account()
            return dbx
        except:
            # Refresh if token is invalid
            new_token = self.get_new_access_token()
            settings.DROPBOX_ACCESS_TOKEN = new_token
            return Dropbox(new_token)