import os
from os import environ
import re
import telebot
import requests
import json
import csv

nutirents_url = "https://trackapi.nutritionix.com/v2/natural/nutrients"
exercise_url = "https://trackapi.nutritionix.com/v2/natural/exercise"
# TODO: 1.1 Add Request HTTP URL of the API
NUTRITIONIX_API_KEY = environ['NUTRITIONIX_API_KEY']
NUTRITIONIX_APP_ID = environ['NUTRITIONIX_APP_ID']
HTTP_API = environ['http_api']

headers = {'Content-Type': 'application/json',
           'x-app-id': NUTRITIONIX_APP_ID, 'x-app-key': NUTRITIONIX_API_KEY}
user = {'name': None, 'gender': None,
        'weight': None, 'height': None, 'age': None}
bot = telebot.TeleBot(HTTP_API)


@bot.message_handler(commands=['start', 'hello'])
def greet(message):
    global botRunning
    botRunning = True
    file = open('exercise.csv', 'w')
    file.close()
    file = open('nutrition.csv', 'w')
    file.close()
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
    usr_data = usr_input.split(",")
    user['name'] = usr_data[0]
    user['gender'] = usr_data[1]
    user['weight'] = usr_data[2]
    user['height'] = usr_data[3]
    user['age'] = usr_data[4]
    bot.reply_to(message, 'User set!')
    reply = 'name: ' + str(usr_data[0]) + ' gender: ' + str(usr_data[1]) + ' weight: ' + str(usr_data[2]) + ' height: ' + str(usr_data[3]) + ' age: ' + str(usr_data[4])
    bot.send_message(message.chat.id, reply)


@bot.message_handler(func=lambda message: botRunning, commands=['nutrition'])
def getNutrition(message):
    bot.reply_to(message, 'Getting nutrition info...')
    text = get_nutrition_data(message.text)
    bot.reply_to(message, text)


@bot.message_handler(func=lambda message: botRunning, commands=['exercise'])
def getCaloriesBurn(message):
    bot.reply_to(message, 'Estimating calories burned...')
    response = get_exercise_data(message.text)
    bot.reply_to(message, response)


@bot.message_handler(func=lambda message: botRunning, commands=['reports'])
def getCaloriesBurn(message):
    bot.reply_to(message, 'Generating report...')
    # TODO: 3.4 Send downlodable CSV file to telegram chat
  


@bot.message_handler(func=lambda message: botRunning)
def default(message):
    bot.reply_to(message, 'I did not understand '+'\N{confused face}')

######################### DEFINED BY ME ##########################################################
######################## GET ALL NUTRITION VALUE #################################################
def get_nutrition_data(text):
    text = text[11:]
    payload = {"query" : text}
    file = open('nutrition.csv', 'w',newline="")
    writer = csv.writer(file)

    response = requests.post(nutirents_url, headers=headers, data = json.dumps(payload))
    data = json.loads(response.text)
    i = 0
    response_message = ""
    for key,value in data["foods"][0].items():
        if(value==None) :
            continue
        response_message = response_message + key + ": " + str(value) + "\n"
        writer.writerow([key,value])
        i = i + 1
        if(i > 10):
            return response_message

#########################FOR GETTING EXERCISE DATA############################################################
def get_exercise_data(text):
    text = text[9:]
    payload = {"query" : text}
    file = open('exercise.csv', 'w',newline="")
    writer = csv.writer(file)

    response = requests.post(exercise_url, headers=headers, data = json.dumps(payload))
    data = json.loads(response.text)
    i = 0
    response_message = ""
    for key,value in data["exercises"][0].items():
        if(value==None) :
            continue
        response_message = response_message + key + ": " + str(value) + "\n"
        writer.writerow([key,value])
        i = i + 1
        if(i > 4):
            return response_message


bot.infinity_polling()


