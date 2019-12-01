import requests
import CheckRequirements
import SellerRep
import json
import pyllegro

token = pyllegro.get_token()  # do zdobycia tokena
access_token = json.loads(token.text)["access_token"]
#print(access_token)

#access_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE1NzUyNTI2MjgsInVzZXJfbmFtZSI6IjQ4MDEzMjUzIiwianRpIjoiOTc3ODAzZDctNDk1NS00NjUxLWI2Y2EtZTNlMjgzODBhYWFjIiwiY2xpZW50X2lkIjoiYzNiYTNhYjJiN2FmNDE3NzllYzI5OWZlZmNhZjI0NTgiLCJzY29wZSI6WyJhbGxlZ3JvX2FwaSJdfQ.7UbdbgOTraexomScv0Scgq5La2Tk1C1lTaa6p_2QTNhzHXsAiES9PdO-hxlm7u0P4O6JD8So_PL_0xdGOWQkYO_oaWiJIcfn_D-vGE7pgWvC1XfAC1OXcEk2UwTnjei3tO3BQu6wiP7_FJQ-yyqhRuGwTDHLulc8syj_F91ygE0nPFoW7SUQmMqraAx9weXrscGvLM_b3HeSF_BWHYodzY3g0o8sf7w5Bpk_TIYMi6PwgnzVxMNOiQQSctTPOFNqRy-RZdefXWhs7kakCt69lBtWxnymtOD7r8y743uqh4UNeseKs-69zN885ck4ZovgG6psjSrvMTqlVxKmz042mA"
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
    print("Podaj minimalna reputacje (nie dotyczy, wpisz: nie): ")
    reputation = input()
    print("Podaj minimalna liczbe ocen (nie dotyczy, wpisz: nie): ")
    number = input()
    return name,number,minp,maxp,reputation,number


# data = inputdata()


set1 = []
set2 = []
set3 = []

# data = inputdata()
# data = ["telewizor", 10, 1000, 1500, 5, 1000] # do testowania jednego zapytania
data = [["telewizor", 10, 1000, 1500, 5, 1000],["xbox one x", 5, 1300, 1700, 4.5, 1000],["ps4", 15, 1000, 1500, 4, 2000],["mustang", 1, 1000, 170000, 0, 1],["Red Dead Redemption", 1, 100, 200, 5, 3000]]

# petla pyta o wybrany produkt
x = 0   # tutaj jako count
for product_parameter in data:  # a tutaj x leci po data, czyli jak poda 3 produkty, to petla sie wykona 3 razy
    set = []
    url_json = get_json(data[x][0])
    for j in url_json['items']:
        for k in url_json['items'][j]:
            if CheckRequirements.count(data[x][1],k['stock']['available']) is True:    # liczba sztuk
                    if CheckRequirements.productprice(data[x][2],data[x][3],k['sellingMode']['price']['amount']) is True: # czy cena miesci sie w granicach
                        seller = SellerRep.get_seller_rates(int(k['seller']['id']),access_token)
                        if CheckRequirements.rates(data[x][4], seller[0], data[x][5], seller[1]) is True:  # oceny, przydaloby sie, zeby najpierw bylo sortowanie, a pozniej sprawdzal oceny
                            #print(k['name'] + " cena = " + k['sellingMode']['price']['amount'] + " ilosc = " + str(k['stock']['available']) + " dostawa = " + k['delivery']['lowestPrice']['amount'])
                            #print(" " + str(seller[0]))    # do testow
                            set.append([k['sellingMode']['price']['amount'],k['name'],str(k['stock']['available']),k['delivery']['lowestPrice']['amount'],k['id']])    # cena,nazwa,ilosc, zeby latwiej posortowac
    # wersja 1 cena z dostawa
    for i in set[:]:
        i[0] = float(i[0]) + float(i[3])
    set.sort()
    if len(set) > 0:
        set1.append(set[0])
    else:
        set1.append("Nie ma produku spelniajacego wymagania")   # tutaj fajnie by bylo ogarnac wlasny blad
    if len(set) > 1:
        set2.append(set[1])
    else:
        set1.append("Nie ma produku spelniajacego wymagania")
    if len(set) > 2:
        set3.append(set[2])
    else:
        set3.append("Nie ma produku spelniajacego wymagania")
    x += 1


#print(set1)
#print("-----------")
#print(set2)
#print("-----------")
#print(set3)




# do wyswietlania w konsoli
count = 0
print("Zestaw 1: ")
for i in data:
    if set1[count][1] != "i":
        print(str(count+1) + ". " + str(set1[count][1]) + " https://allegro.pl/oferta/" + str(set1[count][4]))
    else:
        print("Nie ma produku nr " + str(count+1)  + " spelniajacego wymagania")
    count += 1
count = 0
print("Zestaw 2: ")
for i in data:
    try:
        if set2[count][1] != "i":
            print(str(count+1) + ". " + str(set2[count][1]) + " https://allegro.pl/oferta/" + str(set2[count][4]))
        else:
            print("Nie ma produku nr " + str(count + 1) + " spelniajacego wymagania")
    except IndexError:
        print("Nie ma produku nr " + str(count + 1) + " spelniajacego wymagania")
    count += 1
count = 0
print("Zestaw 3: ")
for i in data:
    if set3[count][1] != "i":
        print(str(count+1) + ". " + str(set3[count][1]) + " https://allegro.pl/oferta/" + str(set3[count][4]))
    else:
        print("Nie ma produku nr " + str(count + 1) + " spelniajacego wymagania")
    count += 1
