import requests
from dataclasses import dataclass

@dataclass
class TwitchClient():
    twitch_token: str
    client_id: str

    def set_headers(self):
        self.headers = {
            'Authorization': f"Bearer {self.twitch_token}",
            'Client-Id': self.client_id
        }

    def get_users(self, list_of_users):
        users = '&login='.join(list_of_users)
        url = f"https://api.twitch.tv/helix/users?login={users}"
        return self._do_request(url)

    def get_is_streaming(self, user):
        url = f"https://api.twitch.tv/helix/streams?user_login={user}"
        return self._do_request(url)


    def _do_request(self, url):
        r = requests.get(url, headers=self.headers)
        if r.status_code == 200:
            return r.json()["data"]
        else:
            raise f"Oops: Client.get_users: {r.status}"
