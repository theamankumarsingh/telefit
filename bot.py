import os
from os import environ, name
import telebot
import requests
import json
import csv

from telebot.types import Document

os.environ['NUTRITIONIX_APP_ID'] = 'ec8dd5a9'
os.environ['http_api'] = '5030645700:AAEiF3t7OZbLMi0uN7qXqWhBE_QK9fu8XjQ'
os.environ['NUTRITIONIX_API_KEY'] = 'de0c2dd842eec373963e73f21ff601c1'


# TODO: 1.1 Add Request HTTP URL of the API
NUTRITIONIX_API_KEY = environ.get('NUTRITIONIX_API_KEY')
NUTRITIONIX_APP_ID = environ.get('NUTRITIONIX_APP_ID')
HTTP_API = environ.get('http_api')

headers = {'Content-Type': 'application/json',
           'x-app-id': NUTRITIONIX_APP_ID, 'x-app-key': NUTRITIONIX_API_KEY}
user = {'name': None, 'gender': None,
        'weight': None, 'height': None, 'age': None}
bot = telebot.TeleBot(HTTP_API)


@bot.message_handler(commands=['greet'])
def greet(message):
    bot.reply_to(message, "Hey!, how's it going?... seems like the trial is running just fine")

@bot.message_handler(commands=['reply'])
def reply(message):
    bot.send_message(message.chat.id, "what reply?")
    bot.send_message(message.chat.id, "2nd reply")
    bot.send_message(message.chat.id, "3rd reply")
    bot.reply_to(message, "does this also send?")


@bot.message_handler(commands=['start', 'hello'])
def greet(message):
    global botRunning
    botRunning = True
    # TODO: 3.1 Add CSV file creation
    fieldnames1 = ['Food Name','Quantity','Calories','Fat','Carbohydrate','Protein']
    fieldnames2 = ['Exercise Name','Duration','Calories Burned']
    with open('nutrition.csv', 'w', encoding='UTF8', newline='') as n:
        writer = csv.DictWriter(n, fieldnames=fieldnames1)
        writer.writeheader()
        n.close()
    with open('exercise.csv', 'w', encoding= 'UTF8', newline= '') as e:
        writer = csv.DictWriter(e, fieldnames=fieldnames2)
        writer.writeheader()
        e.close()
    bot.reply_to(
        message, 'Hello! I am TeleFit. Use me to monitor your health'+'\N{grinning face with smiling eyes}'+'\nYou can use the command \"/help\" to know more about me.')
    

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
    user_data = [usr_input.split(',')]
    if len(user_data[0]) == 5:
        bot.reply_to(message, 'User set!')
        # TODO: 2.2 Display user details in the telegram chat
        name = user_data[0][0]
        gender = user_data[0][1]
        weight = user_data[0][2]
        height = user_data[0][3]
        age = user_data[0][4]
        reply = f'Name: {name}\nGender:{gender}\nWeight:{weight}\nHeight:{height}\nAge:{age}'
        bot.send_message(message.chat.id, reply)
    else:
        error_m = f'Error! wrong format for /user.... try /help to find the correct format'
        bot.send_message(message.chat.id, error_m)


@bot.message_handler(func=lambda message: botRunning, commands=['nutrition'])
def getNutrition(message):
    bot.reply_to(message, 'Getting nutrition info...')
    # TODO: 1.2 Get nutrition information from the API
    model = {}
    model["query"] = message.text[11:]
    url = 'https://trackapi.nutritionix.com/v2/natural/nutrients'
    r= requests.post(url, headers=headers, json=model)
    data = json.loads(r.content.decode('utf-8'))
    # TODO: 1.3 Display nutrition data in the telegram chat
    name = data['foods'][0]['food_name']
    serv = data['foods'][0]['serving_qty']
    servunit = data['foods'][0]['serving_unit']
    cal = data['foods'][0]['nf_calories']
    fat = data['foods'][0]['nf_total_fat']
    carbs = data['foods'][0]['nf_total_carbohydrate']
    protein = data['foods'][0]['nf_protein']
    s = f'Food Name: {name}\nQuantity: {serv} {servunit}\nCalories: {cal}\nFat: {fat}\nCarbohydrate: {carbs}\nProtein: {protein}'
    bot.send_message(message.chat.id, s)
####################
    # TODO: 3.2 Dump data in a CSV file
    row1 = [name, serv, cal, fat, carbs, protein]
    with open('nutrition.csv', 'a') as f_object:
        writer_object = csv.writer(f_object)
        writer_object.writerow(row1)
        f_object.close()


@bot.message_handler(func=lambda message: botRunning, commands=['exercise'])
def getCaloriesBurn(message):
    bot.reply_to(message, 'Estimating calories burned...')
    # TODO: 2.3 Get exercise data from the API
    req = {}
    req["query"] = message.text[10:]
    l = 'https://trackapi.nutritionix.com/v2/natural/exercise'
    rq = requests.post(l, headers=headers, json=req)
    info = json.loads(rq.content.decode('utf-8'))
    # TODO: 2.4 Display exercise data in the telegram chat
    ex_name = info['exercises'][0]['name']
    ex_time = info['exercises'][0]['duration_min']
    calories = info['exercises'][0]['nf_calories']
    texercise = f'Exercise Name: {ex_name}\nDuration: {ex_time} minutes\nCalories Burned: {calories}'
    bot.send_message(message.chat.id, texercise)
    # TODO: 3.3 Dump data in a CSV file
    row1 = [ex_name, ex_time, calories]
    with open('exercise.csv', 'a') as f_object:
        writer_object = csv.writer(f_object)
        writer_object.writerow(row1)
        f_object.close()


@bot.message_handler(func=lambda message: botRunning, commands=['reports'])
def getCaloriesBurn(message):
    bot.reply_to(message, 'Generating Report...')
    # TODO: 3.4 Send downlodable CSV file to telegram chat
    r = message.text.split()
    if r[1] == 'exercise':
        document = open('exercise.csv', 'rb')
        bot.send_document(message.chat.id, document)
    elif r[1] == 'nutrition':
        document = open('nutrition.csv','rb')
        bot.send_document(message.chat.id, document)
    else:
        bot.send_message(message.chat.id, f'Wrong input kingly choose "nutrition" or "exercise" for /reports command')



@bot.message_handler(func=lambda message: botRunning)
def default(message):
    bot.reply_to(message, 'I did not understand '+'\N{confused face}')


bot.infinity_polling()
