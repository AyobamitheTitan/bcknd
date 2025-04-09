from datetime import datetime
from django.conf import settings
from dropbox import Dropbox, files, sharing


class DropboxService:
    def __init__(self):
        pass


    def store_file(self, file):
        dbx = Dropbox(settings.DROPBOX_ACCESS_TOKEN)
        
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