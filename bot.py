import os
from os import environ
from dotenv import load_dotenv
from requests.models import Response
import telebot
import requests
import json
import csv

# TODO: 1.1 Add Request HTTP URL of the API
load_dotenv
NUTRITIONIX_API_KEY= environ['NUTRITIONIX_API_KEY']
NUTRITIONIX_APP_ID= environ['NUTRITIONIX_APP_ID']
HTTP_API = environ['http_api']

headers = {'Content-Type': 'application/json',
           'x-app-id': NUTRITIONIX_APP_ID, 'x-app-key': NUTRITIONIX_API_KEY}
user = {'name': None, 'gender': None,
        'weight': None, 'height': None, 'age': None}
bot = telebot.TeleBot(HTTP_API)


@bot.message_handler(commands=['start', 'hello'])
def greet(message):
    global botRunning
    global csv_nutrition, csv_exercise, nutrition, exercise
    botRunning = True
    # TODO: 3.1 Add CSV file creation
    csv_nutrition = open('nutrition.csv', 'w')
    nutrition = csv.writer(csv_nutrition)
    csv_exercise = open('exercise.csv','w')
    exercise = csv.writer(csv_exercise)
    bot.reply_to(message, 'Hello! I am TeleFit. Use me to monitor your health'+'\N{grinning face with smiling eyes}'+'\nYou can use the command \"/help\" to know more about me.')


@bot.message_handler(commands=['stop', 'bye'])
def goodbye(message):
    global botRunning
    botRunning = False
    csv_exercise.close()
    csv_nutrition.close()
    bot.reply_to(message, 'Bye!\nStay Healthy'+'\N{flexed biceps}')


@bot.message_handler(func=lambda message: botRunning, commands=['help'])
def helpProvider(message):
    bot.reply_to(message, '1.0 You can use \"/nutrition Units Quantity-Type Food-Name\" command to get the nutrients of a particular food. For eg: \"/nutrition 1 piece chapati\"\n\n2.1 For using the bot to get details about an exercise you need to first set the user data using the command \"/user Name, Gender, Weight(in Kg), Height (in cm), Age\". For eg: \"/user Akshat, Male, 70, 6, 19\n\n2.2 Then you can use the command \"/execise Duration-amount Duration-unit Exercise-name\" to get data about an exercise. For eg: \"/exercise 40 minutes push-ups\"\n\n3.0. You can use the command \"/reports Report-name\" to get the reports in CSV Format. For eg: \"/reports nutrition\" to get nutrition report and \"/reports exercise\" to get exercise reports or use the command \"/reports nutrition, exercise\" to get both nutrition and exercise reports\n\n4.0. You can use the command \"/stop\" or the command \"/bye\" to stop the bot.')


@bot.message_handler(func=lambda message: botRunning, commands=['user'])
def setUser(message):
    global user
    usr_input = message.text[6:]
    # TODO: 2.1 Set user data
    user['name'], user['gender'], user['weight'], user['height'], user['age'] = map(str, usr_input.split(', '))
    bot.reply_to(message, 'User set!')
    # TODO: 2.2 Display user details in the telegram chat
    reply = ''
    for key, value in user.items():
        reply+='{} is {}\n'.format(key,value)
    bot.send_message(message.chat.id, reply)


@bot.message_handler(func=lambda message: botRunning, commands=['nutrition'])
def getNutrition(message):
    bot.reply_to(message, 'Getting nutrition info...')
    # TODO: 1.2 Get nutrition information from the API
    r=requests.post('https://trackapi.nutritionix.com/v2/natural/nutrients', json={"query":message.text[11:]}, headers=headers)
    r.raise_for_status()
    jsondata = json.loads(r.text)
    # TODO: 1.3 Display nutrition data in the telegram chat
    nutrientdata = jsondata['foods'][0]
    reply = "Calories: {} \nCholesterol: {} \nDietary Fiber: {} \nPotassium: {} \nProtein: {} \nSaturated Fat: {} \nSodium: {} \nSugars: {} \nTotal Carbohydrate: {} \nTotal fat: {}".format(nutrientdata['nf_calories'],nutrientdata['nf_cholesterol'],nutrientdata['nf_dietary_fiber'],nutrientdata['nf_potassium'],nutrientdata['nf_protein'],nutrientdata['nf_saturated_fat'],nutrientdata['nf_sodium'],nutrientdata['nf_sugars'],nutrientdata['nf_total_carbohydrate'],nutrientdata['nf_total_fat'])
    bot.send_message(message.chat.id, reply)
    # TODO: 3.2 Dump data in a CSV file
    count = 0
    for emp in jsondata['foods']:
        if count == 0:
            header = emp.keys()
            nutrition.writerow(header)
            count += 1
    nutrition.writerow(emp.values())
    
@bot.message_handler(func=lambda message: botRunning, commands=['exercise'])
def getCaloriesBurn(message):
    bot.reply_to(message, 'Estimating calories burned...')
    # TODO: 2.3 Get exercise data from the API
    r=requests.post('https://trackapi.nutritionix.com/v2/natural/exercise', json={
        "query":message.text[10:], 
        "gender":user['gender'], 
        "weight_kg":user['weight'], 
        "height_cm":user['height'],
        "age":user['age']
        }, headers=headers)
    r.raise_for_status()
    jsondata = json.loads(r.text)
    # TODO: 2.4 Display exercise data in the telegram chat
    exercisedata = jsondata['exercises'][0]
    reply= "Exercise: {} \nMinutes Spent: {} \nMET: {} \nCalories Burnt: {}".format(exercisedata['name'], exercisedata['duration_min'] ,exercisedata['met'],exercisedata['nf_calories'])
    bot.send_message(message.chat.id, reply)
    # TODO: 3.3 Dump data in a CSV file
    count = 0
    for e in jsondata['exercises']:
        if count == 0:
            header = e.keys()
            exercise.writerow(header)
            count += 1
    exercise.writerow(e.values())

@bot.message_handler(func=lambda message: botRunning, commands=['reports'])
def getCaloriesBurn(message):
    bot.reply_to(message, 'Generating report...')
    # TODO: 3.4 Send downlodable CSV file to telegram chat
    if message.text[9:].strip()=='nutrition':
        bot.send_document(5042333374, csv_nutrition)
    elif message.text[9:].strip()=='exercise':
        bot.send_document(5042333374, csv_exercise)
    elif message.text[9:].strip()=='nutrition, exercise':
        bot.send_document(5042333374, csv_nutrition)
        bot.send_document(5042333374, csv_exercise)
    else:
        print("Incorrect Syntax. Try again.")

@bot.message_handler(func=lambda message: botRunning)
def default(message):
    bot.reply_to(message, 'I did not understand '+'\N{confused face}')


bot.infinity_polling()
