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
#def inputdata():
#    print("Podaj nazwe produktu: ")
#    name = input()
#    print("Podaj ilosc sztuk (nie dotyczy, wpisz: nie): ")
#    number = input()
#    print("Podaj cene minimalna (nie dotyczy, wpisz: nie): ")
#    minp = input()
#    print("Podaj cene maksymalna (nie dotyczy, wpisz: nie): ")
#    maxp = input()
#    print("Podaj minimalna reputacje (nie dotyczy, wpisz: nie): ")
#    reputation = input()
#    print("Podaj minimalna liczbe ocen (nie dotyczy, wpisz: nie): ")
#    number = input()
#    return name,number,minp,maxp,reputation,number


# data = inputdata()




# data = inputdata()
# data = ["telewizor", 10, 1000, 1500, 5, 1000] # do testowania jednego zapytania
#data = [["telewizor", 10, 1000, 1500, 5, 1000],["xbox one x", 5, 1300, 1700, 4.5, 1000],["ps4", 15, 1000, 1500, 4, 2000],["mustang", 1, 1000, 170000, 0, 1],["Red Dead Redemption", 1, 100, 200, 5, 3000]]

# petla pyta o wybrany produkt

class AllegroAPI():
    x = 0

    def __init__(self, data):
        self.data=data
        self.set1 = []
        self.set2 = []
        self.set3 = []

    def search(self):
        for product in self.data:  # a tutaj x leci po data, czyli jak poda 3 produkty, to petla sie wykona 3 razy
            set = []
            url_json = get_json(self.data[self.x][0])
            for j in url_json['items']:
                for k in url_json['items'][j]:
                    if CheckRequirements.count(self.data[self.x][1], k['stock']['available']) is True:  # liczba sztuk
                        if CheckRequirements.productprice(self.data[self.x][2], self.data[self.x][3], k['sellingMode']['price'][
                            'amount']) is True:  # czy cena miesci sie w granicach
                            # print(k['name'] + " cena = " + k['sellingMode']['price']['amount'] + " ilosc = " + str(k['stock']['available']) + " dostawa = " + k['delivery']['lowestPrice']['amount'])
                            # print(" " + str(seller[0]))    # do testow
                            set.append([k['sellingMode']['price']['amount'], k['name'], str(k['stock']['available']),
                                        k['delivery']['lowestPrice']['amount'], k['id'],
                                        int(k['seller']['id'])])  # cena,nazwa,ilosc, zeby latwiej posortowac
            # wersja 1 cena z dostawa
            for i in set[:]:
                i[0] = float(i[0]) + float(i[3])  # dodajemy do ceny koszt dostawy
            set.sort(reverse=True)

            if self.x > 0:  # sprawdza czy w poprzednich zestawach sa ci sami sprzedawcy, jesli tak to ich faworyzuje
                j = 0
                for i in set[:]:
                    for k in self.set1:
                        if i[5] == k[5]:
                            seller = SellerRep.get_seller_rates(i[5], access_token)
                            if CheckRequirements.rates(self.data[self.x][4], seller[0], self.data[self.x][5], seller[1]) is True:
                                i[0] = float(i[0]) - float(i[3])
                                self.set1.append(i)
                                break
                            j += 1
            if self.x > 0:
                j = 0
                for i in set[:]:
                    for k in self.set2:
                        if i[5] == k[5]:
                            seller = SellerRep.get_seller_rates(i[5], access_token)
                            if CheckRequirements.rates(self.data[self.x][4], seller[0], self.data[self.x][5], seller[1]) is True:
                                i[0] = float(i[0]) - float(i[3])
                                self.set2.append(i)
                                break
                            j += 1
            if self.x > 0:
                j = 0
                for i in set[:]:
                    for k in self.set2:
                        if i[5] == k[5]:
                            seller = SellerRep.get_seller_rates(i[5], access_token)
                            if CheckRequirements.rates(self.data[self.x][4], seller[0], self.data[self.x][5], seller[1]) is True:
                                i[0] = float(i[0]) - float(i[3])
                                self.set3.append(i)
                                break
                        j += 1
            set.sort()

            # formujemy zestawy
            if len(set) > 0:
                for k in set[:]:
                    if len(self.set1) < self.x + 1:
                        seller = SellerRep.get_seller_rates(int(k[5]), access_token)
                        if CheckRequirements.rates(self.data[self.x][4], seller[0], self.data[self.x][5], seller[1]) is True:
                            self.set1.append(set[0])
                            break
            else:
                self.set1.append("Nie ma produku spelniajacego wymagania")

            if len(set) > 1:
                for k in set[:]:
                    if len(self.set2) < self.x + 1:
                        seller = SellerRep.get_seller_rates(int(k[5]), access_token)
                        if CheckRequirements.rates(self.data[self.x][4], seller[0], self.data[self.x][5], seller[1]) is True:
                            self.set2.append(set[1])
                            break
            else:
                self.set1.append("Nie ma produku spelniajacego wymagania")

            if len(set) > 2:
                for k in set[:]:
                    if len(self.set3) < self.x + 1:
                        seller = SellerRep.get_seller_rates(int(k[5]), access_token)
                        if CheckRequirements.rates(self.data[self.x][4], seller[0], self.data[self.x][5], seller[1]) is True:
                            self.set3.append(set[2])
                            break
            else:
                self.set3.append("Nie ma produku spelniajacego wymagania")
            self.x += 1



        print(self.set1)
        print("-----------")
        print(self.set2)
        print("-----------")
        print(self.set3)




        # do wyswietlania w konsoli
        price1 = 0
        price2 = 0
        price3 = 0
        count = 0
        print("Zestaw 1: ")
        for i in self.data:
            try:
                if self.set1[count][1] != "i":
                    print(str(count + 1) + ". " + str(self.set1[count][1]) + " Cena: " + str(
                        self.set1[count][0]) + " https://allegro.pl/oferta/" + str(self.set1[count][4]))
                    price1 += self.set1[count][0]
                else:
                    print("Nie ma produku nr " + str(count + 1) + " spelniajacego wymagania")
            except IndexError:
                print("Nie ma produku nr " + str(count + 1) + " spelniajacego wymagania")
            count += 1
        count = 0
        print("Zestaw 2: ")
        for i in self.data:
            try:
                if self.set2[count][1] != "i":
                    print(str(count + 1) + ". " + str(self.set2[count][1]) + " Cena: " + str(
                        self.set2[count][0]) + " https://allegro.pl/oferta/" + str(self.set2[count][4]))
                    price2 += self.set2[count][0]
                else:
                    print("Nie ma produku nr " + str(count + 1) + " spelniajacego wymagania")
            except IndexError:
                print("Nie ma produku nr " + str(count + 1) + " spelniajacego wymagania")
            count += 1
        count = 0
        print("Zestaw 3: ")
        for i in self.data:
            try:
                if self.set3[count][1] != "i":
                    print(str(count + 1) + ". " + str(self.set3[count][1]) + " Cena: " + str(
                        self.set3[count][0]) + " https://allegro.pl/oferta/" + str(self.set3[count][4]))
                    price3 += self.set3[count][0]
                else:
                    print("Nie ma produku nr " + str(count + 1) + " spelniajacego wymagania")
            except IndexError:
                print("Nie ma produku nr " + str(count + 1) + " spelniajacego wymagania")
            count += 1

#a = AllegroAPI(data)
#a.search()
