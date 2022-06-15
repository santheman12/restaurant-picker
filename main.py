import os
import random

import PIL
import PySimpleGUI as sg
import requests
from urllib import request
from PIL import Image, ImageTk
import ssl

import glob

import yelp_api
import webbrowser
# ----------- Create the 3 layouts this Window will display -----------

# 1: intro
# 2: zip code
# 3: range
# 4: cusine
# 5: price
# 6: results



sg.change_look_and_feel("purple")

fontIntro = ("Franklin Gothic", "28", "bold")
fontText = ("Franklin Gothic", "15", "bold")
fontSubText = ("Franklin Gothic", "13")

# default price
price = "1,2,3,4"

keys_to_clear = ["-LOCATION-", "-RADIUS-", "-CUISINE-", "-PRICE1-", "-PRICE2-", "-PRICE3-", "-PRICE4-",
                 "-NAME-", "-RATING-", "-PRICE-", "-OPEN-", "-TYPE-", "-ADDRESS-"]

xSize = 500
ySize = 600


# image_url = "https://media.cntraveler.com/photos/60480c67ff9cba52f2a91899/16:9/w_2991,h_1682,c_limit/01-velo-header-seattle-needle.jpg"
# response = requests.get(image_url, stream=True)
# data = response.read()

def parse_folder():
    # images = glob.glob('/Users/sankalpvarshney/PycharmProjects/restaurantPicker/images/image1.jpg') + \
    #          glob.glob('/Users/sankalpvarshney/PycharmProjects/restaurantPicker/images/image2.jpg')+ \
    #          glob.glob('/Users/sankalpvarshney/PycharmProjects/restaurantPicker/images/image3.jpg')+ \
    #          glob.glob('/Users/sankalpvarshney/PycharmProjects/restaurantPicker/images/image4.jpg')+ \
    #          glob.glob('/Users/sankalpvarshney/PycharmProjects/restaurantPicker/images/image5.jpg')+ \
    #          glob.glob('/Users/sankalpvarshney/PycharmProjects/restaurantPicker/images/image6.jpg')+ \
    #          glob.glob('/Users/sankalpvarshney/PycharmProjects/restaurantPicker/images/image7.jpg')+ \
    #          glob.glob('/Users/sankalpvarshney/PycharmProjects/restaurantPicker/images/image8.jpg')+ \
    #          glob.glob('/Users/sankalpvarshney/PycharmProjects/restaurantPicker/images/image9.jpg')+ \
    #          glob.glob('/Users/sankalpvarshney/PycharmProjects/restaurantPicker/images/image10.jpg')

    imgs = []
    path = "/Users/sankalpvarshney/PycharmProjects/restaurantPicker/images"
    valid_images = [".jpg", ".gif", ".png", ".tga"]
    for f in os.listdir(path):
        ext = os.path.splitext(f)[1]
        if ext.lower() in valid_images:
            imgs.append(os.path.join(path, f))
        else:
            continue

    return imgs


def load_image(path, window, layout_number):
    try:
        image = Image.open(path)
        image.thumbnail((400, 400))
        photo_img = ImageTk.PhotoImage(image)
        window[f'image{layout_number}'].update(data=photo_img)
    except:
        print(f"Unable to open {path}!")


#1
intro_layout = [
                [sg.Text("Happy 3 Months Mahek!!!", justification='center', size=(100,1), font=fontIntro)],
                [sg.Text(justification='center')],
                [sg.Text("We both suck at choosing where to eat,", justification='center', size=(100,1), font=fontText)],
                [sg.Text("so I decided to make a little app that’ll help us decide!", justification='center', size=(100,1), font=fontText)],
                [sg.Text("I hope you like it!", justification='center', size=(100,1), font=fontText)],
                [sg.Text(justification='center')],
                [sg.Text("Love you", justification='center', size=(100,1), font=fontText)],
[sg.Text(justification='center')],
                [sg.Button("Let's Begin!", size=(200, 1))],
                [sg.Column([[sg.Image(key="image1", size=(400, 400))]], justification='center')],
            ]

#2
zipCode_layout = [
                [sg.Text("Enter below the zipcode you're in right now!", justification='center', size=(100,1), font=fontText)],
                [sg.Text("(I have your current zipcode as 93405)", justification='center', size=(100,1), font=fontSubText)],
                [sg.Text(justification='center')],
                [sg.Input(key="-LOCATION-", size=(100, 10), justification='center')],
                [sg.Button("Next: How far do you want to go?", size=(200, 1))],
                [sg.Text(justification='center')],
                [sg.Column([[sg.Image(key="image2", size=(400, 400))]], justification='center')]
            ]

#3
range_layout = [
                [sg.Text("How far do you want to go? (miles)", justification='center', size=(100, 1), font=fontText)],
[sg.Text(justification='center')],
                [sg.Slider(key="-RADIUS-", range=(1, 20), orientation='h', size=(100, 20), default_value=10)],
                [sg.Button('Next: What type of food?', size=(200, 1))],
                [sg.Text(justification='center')],
                [sg.Column([[sg.Image(key="image3", size=(400, 400))]], justification='center')]
            ]

#4
cuisine_layout = [
                [sg.Text("What type of food do you want to eat?", justification='center', size=(100,1), font=fontText)],
                [sg.Text("(Leave it blank if no preference)", justification='center', size=(100,1), font=fontSubText)],
[sg.Text(justification='center')],
                [sg.Input(key="-CUISINE-", size=(100, 10), justification='center')],
                [sg.Button("Next: $$?", size=(200, 1))],
                [sg.Text(justification='center')],
                [sg.Column([[sg.Image(key="image4", size=(400, 400))]], justification='center')]
]

#5
price_layout = [
                [sg.Text("How much are we trying to spend?", justification='center', size=(100,1), font=fontText)],
                [sg.Text("(Leave it blank if no preference)", justification='center', size=(100,1), font=fontSubText)],
                [*[sg.T("     ") for i in range(5)], sg.Checkbox('$    ', key="-PRICE1-"),
                 sg.Checkbox('$$', default=False, key="-PRICE2-")],
                [*[sg.T("     ") for i in range(5)], sg.Checkbox('$$$', default=False, key="-PRICE3-"),
                 sg.Checkbox('$$$$', default=False, key="-PRICE4-")],
[sg.Text(justification='center')],
                [sg.Button("Alright, let's see where we're eating!", size=(200, 1))],
                [sg.Text(justification='center')],
                [sg.Column([[sg.Image(key="image5", size=(400, 400))]], justification='center')]
]

#6
results_layout = [
          [sg.Text('Name: ', size=(18, 1), font=fontText), sg.Text(size=(20, 1), justification='left', key='-NAME-', font = fontText)],
          [sg.Text('Rating: ', size=(20, 1), font = fontSubText), sg.Text(size=(20, 1), justification='left', key='-RATING-')],
          [sg.Text('Price: ', size=(20, 1), font = fontSubText), sg.Text(size=(20, 1), justification='left', key='-PRICE-')],
          [sg.Text('Open right now?: ', size=(20, 1), font = fontSubText), sg.Text(size=(20, 1), justification='left', key='-OPEN-')],
          [sg.Text('Type: ', size=(20, 1), font = fontSubText), sg.Text(size=(20, 1), justification='left', key='-TYPE-')],
          [sg.Text('Address: ', size=(20, 1), font = fontSubText), sg.Text(size=(20, 1), justification='left', key='-ADDRESS-')],
          [sg.Button("Let's go here!", enable_events=True, key='URL', size=(20, 1)), sg.Button("Next Option", size=(20, 1)), sg.Button("Restart", size=(20, 1))],
                [sg.Text(justification='center')],
                [sg.Column([[sg.Image(key="image6", size=(400, 400))]], justification='center')]
]

# ----------- Create actual layout using Columns and a row of Buttons

# 1: intro
# 2: zip code
# 3: range
# 4: cuisine
# 5: results

final_layout = [[sg.Column(intro_layout, key='-COL1-', justification='center'),
           sg.Column(zipCode_layout, key='-COL2-', visible=False, justification='center'),
           sg.Column(range_layout, visible=False, key='-COL3-', justification='center'),
           sg.Column(cuisine_layout, visible=False, key='-COL4-', justification='center'),
           sg.Column(price_layout, visible=False, key='-COL5-', justification='center'),
           sg.Column(results_layout, visible=False, key='-COL6-', justification='center')],
          ]

window = sg.Window('Where are we eating?', final_layout, size=(xSize, ySize), element_justification='c', resizable=True)


layout = 1  # The currently visible layout
while True:
    event, values = window.read()
    # images = parse_folder()
    # if images:
    #     load_image(images[random.randint(0, len(images) - 1)], window, 1)

    #print(event, values)
    if event in (sg.WIN_CLOSED, 'Exit'):
        break

    if event == "Let's Begin!":
        window[f'-COL{layout}-'].update(visible=False)
        layout = 2
        window[f'-COL{layout}-'].update(visible=True)

        images = parse_folder()
        if images:
            load_image(images[random.randint(0, len(images)-1)], window, layout)

    if event.startswith("Next:"):
        window[f'-COL{layout}-'].update(visible=False)
        layout += 1
        window[f'-COL{layout}-'].update(visible=True)

        images = parse_folder()
        if images:
            load_image(images[random.randint(0, len(images)-1)], window, layout)
    if event == "Alright, let's see where we're eating!":
        window[f'-COL{layout}-'].update(visible=False)
        layout = 6
        window[f'-COL{layout}-'].update(visible=True)

        images = parse_folder()
        if images:
            load_image(images[random.randint(0, len(images) - 1)], window, layout)

        # formats prices-------------
        if values["-PRICE1-"] or values["-PRICE2-"] or values["-PRICE3-"] or values["-PRICE4-"]:
            price = ""
            for i in range(1, 5):
                if values[f'-PRICE{i}-']:
                    print(i)
                    price += str(i)
            price = ','.join(price)
        else:
            price = "1,2,3,4"

        # format location-------------
        if values["-LOCATION-"] == '':
            location = "93405"
        else:
            location = values["-LOCATION-"]

        # format radius---------------
        radius = int(values["-RADIUS-"])
        radius = int(radius * 1609.34)

        # get info on random restaurant
        place_info = yelp_api.requestRestaurantsNearby(location, radius, values["-CUISINE-"], price)
        print(place_info)
        if place_info is not None:
            place_url = place_info['url']
            place_info['is_closed'] = not place_info['is_closed']
            window['-NAME-'].Update(place_info['name'])
            window['-RATING-'].Update(place_info['rating'])
            window['-PRICE-'].Update(place_info['price'])
            window['-OPEN-'].Update(place_info['is_closed'])
            window['-TYPE-'].Update(place_info['type'])
            window['-ADDRESS-'].Update(place_info['address'])
        else:
            window['-NAME-'].Update("Something Went Wrong :(", font=fontSubText)
            window['-RATING-'].Update("Maybe a typo!", font=fontSubText)
            window['-PRICE-'].Update("Press Restart", font=fontSubText)

    if event == 'Next Option':

        images = parse_folder()
        if images:
            load_image(images[random.randint(0, len(images) - 1)], window, layout)

        if values["-PRICE1-"] or values["-PRICE2-"] or values["-PRICE3-"] or values["-PRICE4-"]:
            price = ""
            for i in range(1, 5):
                if values[f'-PRICE{i}-']:
                    print(i)
                    price += str(i)
            price = ','.join(price)
        else:
            price = "1,2,3,4"

        # format location-------------
        if values["-LOCATION-"] == '':
            location = "93405"
        else:
            location = values["-LOCATION-"]

        # format radius---------------
        radius = int(values["-RADIUS-"])
        radius = int(radius * 1609.34)

        place_info = yelp_api.requestRestaurantsNearby(location, radius, values["-CUISINE-"], price)
        if place_info is not None:
            place_url = place_info['url']
        else:
            window['-NAME-'].Update("Something Went Wrong (Typo Maybe) Press Restart")
        print(place_info)
        window['-NAME-'].Update(place_info['name'])
        window['-RATING-'].Update(place_info['rating'])
        window['-PRICE-'].Update(place_info['price'])
        window['-OPEN-'].Update(place_info['is_closed'])
        window['-TYPE-'].Update(place_info['type'])
        window['-ADDRESS-'].Update(place_info['address'])

    if event.startswith("URL"):
        print('button was pressed')
        #url = event.split(' ')[1]
        webbrowser.open(place_url)

    if event == "Restart":
        for key in keys_to_clear:
            window[key]('')
        window[f'-COL{layout}-'].update(visible=False)
        layout = 1
        window[f'-COL{layout}-'].update(visible=True)

window.close()
