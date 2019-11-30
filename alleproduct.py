import requests
import CheckRequirements
import json
import pyllegro

# token = pyllegro.get_token()  # do zdobycia tokena
# access_token = json.loads(token.text)["access_token"]
access_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE1NzUxNzc2MjAsInVzZXJfbmFtZSI6IjQ4MDEzMjUzIiwianRpIjoiMGNlMTVhZDctZmJhNi00MjU4LTg1ZTktNjY0NGZkNjBhMDVlIiwiY2xpZW50X2lkIjoiYzNiYTNhYjJiN2FmNDE3NzllYzI5OWZlZmNhZjI0NTgiLCJzY29wZSI6WyJhbGxlZ3JvX2FwaSJdfQ.p5EVuu7HEXROTtGj5gXGKUYUVkxY1_5Dpwk1e2yfuxHUwl09UOpM3B-Fg3kTvBE5SFaI7uFDkh-rhJE3htb4LUQrxnqBlSajVpbPgqGzIsnsVpYecLps2FW2dlXiFXM6vXyf8dDvUgz99RTU7cHYk-ikJ5-HN2ajz7qKu-aJTFSHnis5lUpsIA0bTr9nkqDBAgHJSwGuayvQN9Abolo9b76m4_6rAc-Cq5uM00rY1tnZTY2GNFg3P338wlgWr-eU7o9SKJ_LMTi3sdUNPJ37zDXDmWY_dLlohQmUYgh9sP6yMuirbx8XDYWn7TxDhyB56VJOdniUqtb-mR7Z-QVEug"
MAIN_URL = "https://api.allegro.pl/offers/listing"


# zapytanie o produkt
def get_http_response(name):
        return requests.get(MAIN_URL,
                                    params={
                                        'phrase': name
                                    },
                                    headers={
                                        'Authorization': 'Bearer ' +  access_token,
                                        'Accept':
                                        'application/vnd.allegro.public.v1+json',
                                        'Content-Type':
                                        'application/vnd.allegro.public.v1+json'
                                    })


# laduje odpowiedzi
def get_json(name):
    resp = get_http_response(name)
    if(resp.status_code == 200):
        return json.loads(resp.text)
    else:
        print("HTTP Error: " + str(resp))
        return 0


# zbiera dane od uzytkownika
def inputdata():
    print("Podaj nazwe produktu: ")
    name = input()
    print("Podaj ilosc sztuk (nie dotyczy, wpisz: nie): ")
    number = input()
    print("Podaj cene minimalna (nie dotyczy, wpisz: nie): ")
    minp = input()
    print("Podaj cene maksymalna (nie dotyczy, wpisz: nie): ")
    maxp = input()
    return name,number,minp,maxp


# data = inputdata()


set1 = []
set2 = []
set3 = []

for x in range(1):  # zmienic pozniej na 5
    set = []
    #data = inputdata()
    data = ["telewizor", 10, 1000, 1500]
    url_json = get_json(data[0])
    for j in url_json['items']:
        for k in url_json['items'][j]:
            if CheckRequirements.rates(3,5) is True:
                if CheckRequirements.count(data[1],k['stock']['available']) is True:
                    if CheckRequirements.productprice(data[2],data[3],k['sellingMode']['price']['amount']) is True:
                        # print(k['name'] + " cena = " + k['sellingMode']['price']['amount'] + " ilosc = " + str(k['stock']['available']) + " dostawa = " + k['delivery']['lowestPrice']['amount'])
                        set.append([k['sellingMode']['price']['amount'],k['name'],str(k['stock']['available']),k['delivery']['lowestPrice']['amount'],k['id']])    # cena,nazwa,ilosc, zeby latwiej posortowac
    # wersja 1 cena z dostawa
    for i in set[:]:
        i[0] = float(i[0]) + float(i[3])
    set.sort()
    set1.append(set[0])
    set2.append(set[1])
    set3.append(set[2])

print(set1)
print("-----------")
print(set2)
print("-----------")
print(set3)

# url to https://allegro.pl/oferta/ + set1[5]