from typing import Optional, Tuple

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build, Resource
from googleapiclient.http import MediaFileUpload

from azusauploadertoolbox.api.BaseApi import BaseApi
from azusauploadertoolbox.dir import CACHE_DIR


class YoutubeApi(BaseApi):
    API = 'https://www.googleapis.com'
    CLIENT_ID = '591454268704-82qdvtk5bs3i7bos6rpcmgqfal48cfmo.apps.googleusercontent.com'
    CLIENT_SECRET = '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'
    SCOPES = [
        f'{API}/auth/youtube',
        f'{API}/auth/youtube.readonly',
        f'{API}/auth/youtube.force-ssl',
        f'{API}/auth/youtube.upload',
        f'{API}/auth/youtube.channel-memberships.creator',
        f'{API}/auth/youtube.download',
    ]
    TOKEN_FILE = CACHE_DIR / 'youtube-credentials.json'

    def __init__(self):
        self.credentials: Optional[Credentials] = None
        self.youtube: Optional[Resource] = None

    def __del__(self):
        try:
            if self.youtube is not None:
                self.youtube.close()
        except:
            pass

    @property
    def has_credentials(self) -> bool:
        return self.TOKEN_FILE.exists()

    def run(self) -> Tuple[bool, str]:
        print(self.youtube.videos().insert(
            part="snippet,status",
            body={
                "snippet": {
                    "description": "Description of uploaded video.",
                    "title": "Test video upload."
                },
                "status": {
                    "privacyStatus": "private"
                }
            },
            media_body=MediaFileUpload("FILE", resumable=True)
        ).execute())
        return True, 'success'

    def load_credentials(self) -> None:
        if not self.TOKEN_FILE.exists():
            port = self.find_free_port()
            flow = InstalledAppFlow.from_client_config({
                'installed': {
                    'client_id': self.CLIENT_ID,
                    'client_secret': self.CLIENT_SECRET,
                    'redirect_uri': f'http://127.0.0.1:{port}',
                    'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
                    'token_uri': 'https://accounts.google.com/o/oauth2/token'
                }
            }, self.SCOPES)
            credentials: Credentials = flow.run_local_server(port=port)
            with self.TOKEN_FILE.open('w') as f:
                f.write(credentials.to_json())
                f.flush()
            self.credentials = credentials
        else:
            self.credentials = Credentials.from_authorized_user_file(self.TOKEN_FILE)
        self.youtube = build('youtube', 'v3', credentials=self.credentials)


if __name__ == '__main__':
    api = YoutubeApi()
    if api.has_credentials:
        api.load_credentials()
        api.run()
