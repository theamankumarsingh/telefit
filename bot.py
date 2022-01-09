import os,pprint
from os import environ, name

from requests.models import Response
import telebot
import requests
import json
import csv

# from flask import Flask, request
# server = Flask(__name__)


# TODO: 1.1 Add Request HTTP URL of the API


# os.environ['NUTRITIONIX_API_KEY'] = environ['NUTRITIONIX_API_KEY']
# os.environ['NUTRITIONIX_APP_ID'] = environ['NUTRITIONIX_API_KEY']
# os.environ['HTTP_API'] = environ['http_api']
NUTRITIONIX_API_KEY = environ['NUTRITIONIX_API_KEY']
NUTRITIONIX_APP_ID = environ['NUTRITIONIX_APP_ID']
HTTP_API = environ['TOKEN']

# NUTRITIONIX_API_KEY = environ['NUTRITIONIX_API_KEY']
# NUTRITIONIX_APP_ID = environ['NUTRITIONIX_APP_ID']
# HTTP_API = environ['http_api']

# headers = {'Content-Type': 'application/json',
#            'x-app-id': NUTRITIONIX_APP_ID, 'x-app-key': NUTRITIONIX_API_KEY}
# user = {'name': None, 'gender': None,
#         'weight': None, 'height': None, 'age': None}
# bot = telebot.TeleBot(HTTP_API)

headers = {'Content-Type': 'application/json',
           'x-app-id': NUTRITIONIX_APP_ID, 'x-app-key': NUTRITIONIX_API_KEY}
user = {'name': None, 'gender': None,
        'weight': None, 'height': None, 'age': None}
bot = telebot.TeleBot(HTTP_API)


@bot.message_handler(commands=['start', 'hello'])
def greet(message):
    global botRunning
    botRunning = True
    # TODO: 3.1 Add CSV file creation
    bot.reply_to(
        message, 'Hello! I am TeleFit. Use me to monitor your health'+'\N{grinning face with smiling eyes}'+'\nYou can use the command \"/help\" to know more about me.')
    fields=['Food-Name','Quantity','Calories','Fat',"Carbohydrates",'Protein']

    with open(r'nutrition_records.csv', 'w+') as f:
        writer = csv.writer(f)
        writer.writerow(fields)
    f.close()

    fields2=['Exercise-Name','Duration','Calories-Burned']
    
    with open(r'exercise_records.csv', 'w+') as f:
        writer = csv.writer(f)
        writer.writerow(fields2)

    f.close()


@bot.message_handler(commands=['stop', 'bye'])
def goodbye(message):
    global botRunning
    botRunning = False
    bot.reply_to(message, 'Bye!\nStay Healthy'+'\N{flexed biceps}')


@bot.message_handler(func=lambda message: botRunning, commands=['help'])
def helpProvider(message):
    bot.reply_to(message, '1.0 You can use \"/nutrition Units Quantity-Type Food-Name\" command to get the nutrients of a particular food. For eg: \"/nutrition 1 piece chapati\"\n\n2.1 For using the bot to get details about an exercise you need to first set the user data using the command \"/user Name, Gender, Weight(in Kg), Height (in cm), Age\". For eg: \"/user Akshat, Male, 70, 6, 19\n\n2.2 Then you can use the command \"/execise Duration-amount Duration-unit Exercise-name\" to get data about an exercise. For eg: \"/exercise 40 minutes push-ups\"\n\n3.0. You can use the command \"/reports Report-name\" to get the reports in CSV Format. For eg: \"/reports nutrition\" to get nutrition report and \"/reports exercise\" to get exercise reports or use the command \"/reports nutrition, exercise\" to get both nutrition and exercise reports\n\n4.0. You can use the command \"/stop\" or the command \"/bye\" to stop the bot.')


@bot.message_handler(func=lambda message: botRunning, commands=['user'])
def setUser(message):
    global user
    usr_input = message.text[6:]
    # TODO: 2.1 Set user data
    input_=usr_input.split(',')
    name= input_[0]
    gender= input_[1]
    weight= input_[2]
    height= input_[3]
    age= input_[4]
    user = input_
    bot.reply_to(message, 'User set!')
    reply = 'Name: '+ str(name) +'\n' + 'Gender : '+ str(gender) +'\n' + 'Weight: '+ str(weight) +'\n' + 'Height: '+ str(height) +'\n' + 'Age: '+ str(age)
    # TODO: 2.2 Display user details in the telegram chat
    bot.send_message(message.chat.id, reply)
    


@bot.message_handler(func=lambda message: botRunning, commands=['nutrition'])
def getNutrition(message):
    bot.reply_to(message, 'Getting nutrition info...')
    # TODO: 1.2 Get nutrition information from the API
    text = message.text
    text2= text.replace('/nutrition ', '')
    print(text2)
    url = "https://trackapi.nutritionix.com/v2/natural/nutrients"
    lst=[]
    if 'and' in text2:
        lst = text2.split('and')
    if ',' in text2:
        lst = text2.split(',')
    else:
        lst.append(text2)
        

    global headers
    for i in lst:
        payload = json.dumps({
        "query": i
        })
        
        response = requests.request("POST", url, headers=headers, data=payload)
        d = json.loads(response.text)
        
        # TODO: 1.3 Display nutrition data in the telegram chat
        reply = 'Food Name: ' + str(d['foods'][0]["food_name"]) + '\n' + 'Quantity: ' + str(d['foods'][0]["serving_qty"]) +' ' +str(d['foods'][0]["serving_unit"]) + '\n' + 'Calories: ' + str(d['foods'][0]["nf_calories"])+ '\n' + 'Fat: ' + str(d['foods'][0]["nf_total_fat"])+ '\n' + 'Carbohydrate: ' +str(d['foods'][0]["nf_total_carbohydrate"])+ '\n' + 'Protein: ' + str(d['foods'][0]["nf_protein"])
        bot.send_message(message.chat.id, reply)
        fields = [str(d['foods'][0]["food_name"]),str(d['foods'][0]["serving_qty"]) +' ' +str(d['foods'][0]["serving_unit"]),d['foods'][0]["nf_calories"],d['foods'][0]["nf_total_fat"],d['foods'][0]["nf_total_carbohydrate"],d['foods'][0]["nf_protein"]]
    # TODO: 3.2 Dump data in a CSV file
        

        
        with open(r'nutrition_records.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow(fields)
        f.close()
    
   

@bot.message_handler(func=lambda message: botRunning, commands=['exercise'])
def getCaloriesBurn(message):
    bot.reply_to(message, 'Estimating calories burned...')
    # TODO: 2.3 Get exercise data from the API
    url = "https://trackapi.nutritionix.com/v2/natural/exercise"
    text = message.text
    text2= text.replace('/excercise ', '')
    print(text2)
    lst=[]
    if 'and' in text2:
        lst = text2.split('and')
    if ',' in text2:
        lst = text2.split(',')
    else:
        lst.append(text2)
    global headers
    for i in lst:

        payload = json.dumps({
        "query":i,
        "gender":user[1],
        "weight_kg":int(user[2]),
        "height_cm":int(user[3]),
        "age":int(user[4])
        })
        response = requests.request("POST", url, headers=headers, data=payload)
        d = json.loads(response.text)

    # TODO: 2.4 Display exercise data in the telegram chat   
        
        if len(d["exercises"]) ==2:

            reply = 'Exercise Name: ' + str(d['exercises'][1]["name"]) + '\n' + 'Duration: ' + str(d['exercises'][1]["duration_min"]) + '\n' +'Calories Burned: ' + str(d['exercises'][1]["nf_calories"])
        else:
            reply = 'Exercise Name: ' + str(d['exercises'][0]["name"]) + '\n' + 'Duration: ' + str(d['exercises'][0]["duration_min"]) + '\n' +'Calories Burned: ' + str(d['exercises'][0]["nf_calories"])

        bot.send_message(message.chat.id, reply)
    
    
    # TODO: 3.3 Dump data in a CSV file
        
        
        with open(r'exercise_records.csv', 'a') as f:
            writer = csv.writer(f)
            if len(d["exercises"]) ==2:
                fields1=[str(d['exercises'][1]["name"]),int(d['exercises'][1]["duration_min"]),int(d['exercises'][1]["nf_calories"])]
                writer.writerow(fields1)
            else:
                fields2=[str(d['exercises'][0]["name"]),int(d['exercises'][0]["duration_min"]),int(d['exercises'][0]["nf_calories"])]
                writer.writerow(fields2)
        f.close()

@bot.message_handler(func=lambda message: botRunning, commands=['reports'])
def getCaloriesBurn(message):
    bot.reply_to(message, 'Generating report...')
    # TODO: 3.4 Send downlodable CSV file to telegram chat
    text = message.text
    text2= text.replace('/reports ', '')
    if text2=='nutrition':
        doc = open('nutrition_records.csv', 'rb')
        bot.send_document(message.chat.id, doc)
    elif text2=='exercise':
        doc = open('exercise_records.csv', 'rb')
        bot.send_document(message.chat.id, doc)
    else:
        doc = open('nutrition_records.csv', 'rb')
        doc2 = open('exercise_records.csv', 'rb')
        bot.send_document(message.chat.id, doc)
        bot.send_document(message.chat.id, doc2)

    
@bot.message_handler(func=lambda message: botRunning)
def default(message):
    bot.reply_to(message, 'I did not understand '+'\N{confused face}')
    

bot.infinity_polling()
