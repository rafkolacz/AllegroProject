# Skrypt zawiera tylko funkcje do sprawdzenia, czy produkt spelnia okreslone warunki


def count(wanted,offered):  # wanted - ile sztuk chce kupic klient, offered - ile sprzedajacy ma
    wanted = int(wanted)
    offered = int(offered)
    if wanted > offered:
        return False
    else:
        return True    # jesli sprzedawca ma wystarczajaca ilosc przedmiotow, funkcja zwraca true


def rates(min, average,require,total): # min - wymagana ocena, av - srednia ocena, total - liczba wszystkich ocen, req - liczba wymaganych ocen
    if require <= total:
        if min > average:
            return False
        else:
            return True  # jesli sprzedawca ma wystarczajaca reputacje, funkcja zwraca true, pod warunkiem, ze ma odpowiednia ilosc ocen
    else:
        return False


def productprice(min,max,offered):  # min/max - namniejsza mozliwa cena i najwieksza dla klienta, offered - ile chce sprzedawca
    offered = float(offered)
    min = float(min)
    max = float(max)
    if min < offered:
        if offered <= max:
            return True
    else:
        return False    # zwraca true jak cena miesci sie w przedziale



