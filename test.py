import os,logging,pprint
from os import environ
from decouple import config
# from requests.sessions import _Data
import telebot
import requests
import json
import csv

NUTRITIONIX_API_KEY = config('NUTRITIONIX_API_KEY')
NUTRITIONIX_APP_ID = config('NUTRITIONIX_APP_ID')
HTTP_API = config('http_api')
NUTRITIONIX_API_ID= '8326234b'
NUTRITIONIX_APP_KEY ='14c63015febf267b23c05604706bc2ee'	

# food=input("Enter food: ").lower()


# r=requests.post("https://api.nutritionix.com/v1_1/search",json={"appId":"8326234b","appKey":str(config('NUTRITIONIX_API_KEY')),"fields": [
#     "item_name",
#     "item_description",
#     "nf_calories",
#     "nf_total_fat",
#     "nf_total_carbohydrate",
#     "nf_protein",
#     "item_type"
#   ],"query":food,"filters": {
#     "not": {
#       "item_type": 1
#     }}})



# r=requests.post("https://trackapi.nutritionix.com/v2/natural/nutrients",json={"x-app-id":"8326234b","x-app-key":str(config('NUTRITIONIX_API_KEY')),"query": "string",
#   "num_servings": 2,"nf_calories",
#     "nf_total_fat",
#     "nf_total_carbohydrate",
#     "nf_protein"})

# data=r.json()
# row=(data['hits'][0]['fields'])
# # print(data["hits"][0].keys())
# # print(data["type"])
# print(data,"\n\n")
# print(data['hits'][0]['fields'])
# print(row['item_name'].split()[0])

# print("good boy")
# print("food Item :",food)
# print("Calories :",row['nf_calories'])
# print("Total Fat: ",row['nf_total_fat'])
# print("Carbohydrates: ",row['nf_total_carbohydrate'])
# print("protein: ",row['nf_protein'])

# print(type(4)!=str)

# a="234,234,2342,  33  ,33,  2,23,234".split(',')
# for s in a:
#   print(int(s))
NUTRITIONIX_API_KEY= '03b15a8fe4985d8ad01e234a078596fc'
NUTRITIONIX_APP_ID = '8326234b'	

exercise= "30 minutes push-ups"
gender="male"
height=173
weight=67
age=18


# r=requests.post("https://trackapi.nutritionix.com/v2/natural/exercise",json={"x-app-id":NUTRITIONIX_APP_ID,"x-app-key":NUTRITIONIX_API_KEY,"query":exercise,
#  "gender":gender,
#  "weight_kg":weight,
#  "height_cm":height,
#  "age":age})

# datado=r.json()
url="https://trackapi.nutritionix.com/v2/natural/exercise"
h={"x-app-id":NUTRITIONIX_APP_ID,"x-app-key":NUTRITIONIX_API_KEY}

Headers = {'Content-Type': 'application/json',
           'x-app-id': NUTRITIONIX_APP_ID, 'x-app-key': NUTRITIONIX_API_KEY}
# data={'query,':exercise,
#  'gender':gender,
#  'weight_kg':weight,
#  'height_cm':height,
#  'age':age}
data_json = {
        'query': exercise,
        'gender': gender,
        'weight_kg': weight,
        'height_cm': height,
        'age': age,
    }
r=requests.post(url,json=data_json, headers=Headers )

f=r.json()
print(f)

# print(datado)

# import csv

# with open('names.csv', 'w') as csvfile:
#     fieldnames = ['first_name', 'last_name']
#     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

#     writer.writeheader()
#     writer.writerow({'first_name': 'Baked', 'last_name': 'Beans'})
#     writer.writerow({'first_name': 'Lovely', 'last_name': 'Spam'})
#     writer.writerow({'first_name': 'Wonderful', 'last_name': 'Spam'})
