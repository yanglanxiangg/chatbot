import requests
import datetime

def getData(c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,total):
    response = requests.get("https://opendata.arcgis.com/datasets/772f5cdbb99c4f6689ed1460c26f4b05_0/FeatureServer/0/query?outFields=*&where=1%3D1")
    # Handling response
    if response.status_code != 200:
        while response.status_code != 200:
            print("Connecting to API....")
            response = requests.get("https://opendata.arcgis.com/datasets/772f5cdbb99c4f6689ed1460c26f4b05_0/FeatureServer/0/query?outFields=*&where=1%3D1")
            if response.status_code == 200:
                break
    content = response.json()
    City1 = dict()
    count1 = 0
    total1 = 0
    City2 = dict()
    total2 = 0
    City3 = dict()
    total3 = 0
    City4 = dict()
    total4 = 0
    City5 = dict()
    total5 = 0
    City6 = dict()
    total6 = 0
    City7 = dict()
    total7 = 0
    City8 = dict()
    total8 = 0
    City9 = dict()
    total9 = 0
    City10 = dict()
    total10 = 0
    City11 = dict()
    total11 = 0

    date_map = dict()
    for i in content['features']:
        if i['attributes']['DateSpecCollect'] != 'Total':
            total1 += i['attributes'][c1]
            City1[count1] = total1

            total2 += i['attributes'][c2]
            City2[count1] = total2

            total3 += i['attributes'][c3]
            City3[count1] = total3

            total4 += i['attributes'][c4]
            City4[count1] = total4

            total5 += i['attributes'][c5]
            City5[count1] = total5

            total6 += i['attributes'][c6]
            City6[count1] = total6

            total7 += i['attributes'][c7]
            City7[count1] = total7

            total8 += i['attributes'][c8]
            City8[count1] = total8

            total9 += i['attributes'][c9]
            City9[count1] = total9

            total10 += i['attributes'][c10]
            City10[count1] = total10

            total11 += i['attributes'][total]
            City11[count1] = total11

            date_map[i['attributes']['DateSpecCollect']] = count1
            count1 += 1

    return date_map,City1,City2,City3,City4,City5,City6,City7,City8,City9,City10,City11