import os
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = [
    'https://www.googleapis.com/auth/youtube.readonly'
    ]


def get_authenticated_service(service, version, client_secrets_file='client_secret.json', **scopes):
    # OAuth 2.0 인증 흐름 초기화
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                client_secrets_file, SCOPES)
            creds = flow.run_local_server(port=0)
        # 증명서 토큰 저장
        with open('token.json', 'w') as token:
            token.write(creds.to_json())


    # 인증된 서비스 반환
    return build(service, version, credentials=creds, )

if __name__ == "__main__":
    get_authenticated_service('youtube', 'v3', SCOPES)