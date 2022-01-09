
import os
from os import environ
import telebot
import requests
import json
import csv
from dotenv import load_dotenv
load_dotenv('/home/adithya-rxdrn/telefit/.env')

#  TODO: 1.1 Add Request HTTP URL of the API
url1 = "https://trackapi.nutritionix.com/v2/natural/nutrients"
url2= "https://trackapi.nutritionix.com/v2/natural/exercise"
NUTRITIONIX_API_KEY = environ['NUTRITIONIX_API_KEY']
NUTRITIONIX_APP_ID = environ['NUTRITIONIX_APP_ID']
HTTP_API = environ['http_api']

Headers = {'Content-Type': 'application/json',
           'x-app-id': NUTRITIONIX_APP_ID, 'x-app-key': NUTRITIONIX_API_KEY}
user = {'name': None, 'gender': None,
        'weight': None, 'height': None, 'age': None}
bot = telebot.TeleBot(HTTP_API)



@bot.message_handler(commands=['start', 'hello'])
def greet(message):
    global botRunning
    botRunning = True
    # TODO: 3.1 Add CSV file creation
    with open('nutrition.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Food Name', 'Quantity', 'Calories', 'Fat', 'Carbohydrates', 'Protein'])

    with open('exercise.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Exercise Name', 'Duration', 'Calories Burned'])
    
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
    usr_data=usr_input.split(",")
    # TODO: 2.1 Set user data
    user['name'] = usr_data[0]
    user['gender'] = usr_data[1]
    user['weight'] = usr_data[2]
    user['height'] = usr_data[3]
    user['age'] = usr_data[4]
    bot.reply_to(message, 'User set!')
    reply = 'name: ' + str(usr_data[0]) + ' gender: ' + str(usr_data[1]) + ' weight: ' + str(usr_data[2]) + ' height: ' + str(usr_data[3]) + ' age: ' + str(usr_data[4])
    # TODO: 2.2 Display user details in the telegram chat
    bot.send_message(message.chat.id, reply)


@bot.message_handler(func=lambda message: botRunning, commands=['nutrition'])
def getNutrition(message):
    bot.reply_to(message, 'Getting nutrition info...')
    # TODO: 1.2 Get nutrition information from the API
    response = requests.post(url1, headers=Headers, json={'query':message.text[11:]})
    res = response.json()
    # TODO: 1.3
    bot.send_message(message.chat.id, 'Food Name: ' + str(res['foods'][0]['food_name']) + '\nQuantity: ' + str(res['foods'][0]['serving_qty']) +'\nCalories: ' + str(res['foods'][0]['nf_calories']) +'\nFat: ' + str(res['foods'][0]['nf_total_fat']) +'\nCarbohydrates: ' + str(res['foods'][0]['nf_total_carbohydrate']) +'\nProtein: ' + str(res['foods'][0]['nf_protein']))
    # TODO: 3.2
    with open('nutrition.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([str(res['foods'][0]['food_name']), str(res['foods'][0]['serving_qty']), str(res['foods'][0]['nf_calories']), str(res['foods'][0]['nf_calories']), str(res['foods'][0]['nf_total_carbohydrate']), str(res['foods'][0]['nf_protein'])])

@bot.message_handler(func=lambda message: botRunning, commands=['exercise'])
def getCaloriesBurn(message):
    query=message.text
    bot.reply_to(message, 'Estimating calories burned...')
    # TODO: 2.3 Get exercise data from the API
    response = requests.post(url2, headers=Headers, json={'query':message.text[10:], 'gender':user['gender'], 'weight_kg':user['weight'], 'height_cm':user['height'], 'age':user['age']})
    res = response.json()
    # TODO: 2.4 Display exercise data in the telegram chat
    bot.send_message(message.chat.id,'Exercise Name: ' + str(res['exercises'][0]['user_input']) + '\nDuration: ' + str(res['exercises'][0]['duration_min']) + '\nCalories Burned: ' + str(res['exercises'][0]['nf_calories']))
    # TODO: 3.3 Dump data in a CSV file
    with open('exercise.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([str(res['exercises'][0]['user_input']), str(res['exercises'][0]['duration_min']), str(res['exercises'][0]['nf_calories'])])

@bot.message_handler(func=lambda message: botRunning, commands=['reports'])
def getCaloriesBurn(message):
    y=message.text
    bot.reply_to(message, 'Generating report...')
    # TODO: 3.4 Send downlodable CSV file to telegram chat
    if 'nutrition' in y:
        doc = open('./nutrition.csv', 'rb')
        bot.send_document(message.chat.id, doc)
    if 'exercise' in y:
        doc = open('./exercise.csv', 'rb')
        bot.send_document(message.chat.id, doc)

@bot.message_handler(func=lambda message: botRunning)
def default(message):
    bot.reply_to(message, 'I did not understand '+'\N{confused face}')


bot.infinity_polling()

