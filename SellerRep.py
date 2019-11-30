# tutaj cos nie dziala, czemu ciagle 404? 
import requests
import json

access_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE1NzUxNzc2MjAsInVzZXJfbmFtZSI6IjQ4MDEzMjUzIiwianRpIjoiMGNlMTVhZDctZmJhNi00MjU4LTg1ZTktNjY0NGZkNjBhMDVlIiwiY2xpZW50X2lkIjoiYzNiYTNhYjJiN2FmNDE3NzllYzI5OWZlZmNhZjI0NTgiLCJzY29wZSI6WyJhbGxlZ3JvX2FwaSJdfQ.p5EVuu7HEXROTtGj5gXGKUYUVkxY1_5Dpwk1e2yfuxHUwl09UOpM3B-Fg3kTvBE5SFaI7uFDkh-rhJE3htb4LUQrxnqBlSajVpbPgqGzIsnsVpYecLps2FW2dlXiFXM6vXyf8dDvUgz99RTU7cHYk-ikJ5-HN2ajz7qKu-aJTFSHnis5lUpsIA0bTr9nkqDBAgHJSwGuayvQN9Abolo9b76m4_6rAc-Cq5uM00rY1tnZTY2GNFg3P338wlgWr-eU7o9SKJ_LMTi3sdUNPJ37zDXDmWY_dLlohQmUYgh9sP6yMuirbx8XDYWn7TxDhyB56VJOdniUqtb-mR7Z-QVEug"
MAIN_URL = 'https://api.allegro.pl/users/{userId}/ratings-summary'

user_id = "41846511"


def get_http_response(user_id):
        return requests.get(MAIN_URL,
                                    params={
                                        'userId': user_id
                                    },
                                    headers={
                                        'Authorization': 'Bearer ' +  access_token,
                                        'Accept':
                                        'application/vnd.allegro.public.v1+json',
                                        'Content-Type':
                                        'application/vnd.allegro.public.v1+json'
                                    })


resp = requests.get(MAIN_URL,
                            params={
                                    #'userId': '0'
                             },
                            headers={
                                    'Authorization': 'Bearer ' +  access_token,
                                    'Accept':
                                    'application/vnd.allegro.public.v1+json',
                                    'Content-Type':
                                    'application/vnd.allegro.public.v1+json'
                                })
#url_json = json.loads(resp.text)
print("X")
print(resp)
