# Skrypt sluzy do zapytania api o reputacje sprzedawcy, zwraca one laczna liczbe opini (+ i -) oraz srednia z deliveryCost, service i description
import requests
import json


def get_http_response_sel(user_id,access_token): # zapytanie o sprzedajacego, jedyna zmiana, to podajemy jego id w main url
        MAIN_URL = 'https://api.allegro.pl/users/'+str(user_id)+'/ratings-summary'
        return requests.get(MAIN_URL,

                                    headers={
                                        'Authorization': 'Bearer ' + access_token,
                                        'Accept':
                                        'application/vnd.allegro.public.v1+json',
                                        'Content-Type':
                                        'application/vnd.allegro.public.v1+json'
                                    })


def get_seller_rates(user_id,access_token):   # zwraca srednia z ocen o sprzedajacym oraz laczna liczbe ocen
    response = get_http_response_sel(user_id,access_token)
    if response.status_code == 200:
        url_json_sel = json.loads(response.text)
        number = int(url_json_sel['recommended']['total']) + int(url_json_sel['notRecommended']['total'])
        rates = (float(url_json_sel['averageRates']['deliveryCost']) + float(url_json_sel['averageRates']['service']) + float(url_json_sel['averageRates']['description']))/3
        if rates is not None:
            return rates, number
    else:
            rates = 0
            number = 0
            return rates,number


