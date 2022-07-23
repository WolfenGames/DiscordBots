from email import header
import requests
from dataclasses import dataclass, field

class BearerTokenFail(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class RequestFail(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

@dataclass
class TwitchClient():
    client_id: str
    client_secret: str
    last_auth_time: str

    def __post_init__(self):
        self.token = None

    def _set_headers(self, refresh=False):
        if refresh or not self.token:
            token = self._get_auth_token()

        self.headers = {
            'Authorization': f"Bearer {token}",
            'Client-Id': self.client_id
        }

    def get_users(self, list_of_users):
        users = '&login='.join(list_of_users)
        url = f"https://api.twitch.tv/helix/users?login={users}"
        return self._do_request(url)

    def get_is_streaming(self, user):
        url = f"https://api.twitch.tv/helix/streams?user_login={user}"
        return self._do_request(url)

    def _get_auth_token(self):
        url = f"https://id.twitch.tv/oauth2/token?client_id={self.client_id}&client_secret={self.client_secret}&grant_type=client_credentials"
        r = requests.post(url)

        if r.status_code == 200:
            res = r.json()
            return res["access_token"]
        raise BearerTokenFail(f"Oops: Client.auth: {r.status_code}, {r.headers}")

    def _test_call(self):
        self._set_headers()
        url = f"https://api.twitch.tv/helix/users?login=TheWolf_ZA"
        r = requests.get(url, headers=self.headers)
        if r.status_code != 200:
            self._set_headers(refresh=True)

    def _do_request(self, url):
        self._test_call()
        r = requests.get(url, headers=self.headers)
        if r.status_code == 200:
            return r.json()["data"]
        else:
            raise RequestFail(f"Oops: Client.request: {r.status}")
