import requests
import json
import random

def requestRestaurantsNearby(location, radius, category, price):
    url = 'https://api.yelp.com/v3/businesses/search'
    key = "KjgSM553PkcBWOe1Hl-t3G4JT0QUC4Ok8xQMF2p76Jt2zEBJwa8yxS8HvnVT83Rmka071B3jXrEy6RZM3S6TbjATYccO-_KTlOIkTEaH6kUhb0CmTa3lQvPX6OjAYXYx"

    headers = {
        'Authorization' : 'Bearer %s' % key
    }
    # data = []
    # for offset in range(0, 200, 50):
    #     parameters = {
    #         'location': location,
    #         'term': category + " Restaurants", #----------add category to this
    #         'radius': radius,
    #         'categories': category,
    #         'price': price,
    #         'limit': 50
    #     }
    #     response = requests.get(url, headers=headers, params=parameters)
    #     if response.status_code == 200:
    #         data += response.json()
    #     elif response.status_code == 400:
    #         print('400 Bad Request')
    #         break

    data = []
    for offset in range(0, 150, 50):
        parameters = {
            'location': location,
            'term': category + " Restaurants",  # ----------add category to this
            'radius': radius,
            'categories': category,
            'price': price,
            'limit': 50
        }

        response = requests.get(url, headers=headers, params=parameters)
        if response.status_code == 200:
            data += response.json()['businesses']
        elif response.status_code == 400:
            print('400 Bad Request')
            break

    return process_response(data)
    #print(response)


def process_response(response):
    response_dict = {}
    random_place = 0
    # print(response)
    # print(len(response))
    if len(response) != 0:
        random_place = random.randint(0, len(response)-1)
    else:
        return None

    #print("total number of entries" + str(len(response)))
    #print("random number" + str(random_place))
    response_dict["name"] = response[random_place]["name"]
    response_dict["rating"] = response[random_place]["rating"]
    response_dict["price"] = response[random_place]["price"]
    response_dict["is_closed"] = response[random_place]["is_closed"]
    response_dict["type"] = response[random_place]["categories"][0]["title"]
    response_dict["url"] = response[random_place]["url"]
    response_dict["address"] = response[random_place]["location"]["address1"]

    #print(response_dict)

    return response_dict


