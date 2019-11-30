

def count(wanted,offered):
    wanted = int(wanted)
    offered = int(offered)
    if wanted > offered:
        return False
    else:
        return True    # jesli sprzedawca ma wystarczajaca ilosc przedmiotow, funkcja zwraca true


def rates(min, average):

    if min > average:
        return False
    else:
        return True  # jesli sprzedawca ma wystarczajaca reputacje, funkcja zwraca true


def productprice(min,max,offered):
    offered = float(offered)
    min = float(min)
    max = float(max)
    if min < offered:
        if offered <= max:
            return True
    else:
        return False    # zwraca true jak cena miesci sie w przedziale



