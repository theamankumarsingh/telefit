import os
from os import environ
import telebot
import requests
import json
import csv
from webserver import keep_alive
from dotenv import load_dotenv
load_dotenv()


NUTRITIONIX_API_KEY = environ['NUTRITIONIX_API_KEY']
NUTRITIONIX_APP_ID = environ['NUTRITIONIX_APP_ID']
HTTP_API = environ['HTTP_API']

headers = {'Content-Type': 'application/json',
           'x-app-id': NUTRITIONIX_APP_ID, 'x-app-key': NUTRITIONIX_API_KEY}
user = {'name': None, 'gender': None,
        'weight': None, 'height': None, 'age': None}
bot = telebot.TeleBot(HTTP_API)

@bot.message_handler(commands=['start', 'hello'])
def greet(message):
    global botRunning
    botRunning = True
    file1 = open('nutrition_records.csv', 'w')
    file1.close()
    file2 = open('excerise_records.csv', 'w')
    file2.close()
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
    usr_input = (message.text[6:]).split()
    name = usr_input[0]
    gender = usr_input[1]
    weight = int(usr_input[2])
    height = int(usr_input[3])
    age = int(usr_input[4])
    bot.reply_to(message, 'User set!')
    reply = 'name: {}\ngender: {}\nweight: {}\nheight: {}\nage: {}'.format(name,gender,weight,height,age)
    bot.send_message(message.chat.id, reply)

@bot.message_handler(func=lambda message: botRunning, commands=['nutrition'])
def getNutrition(message):
    bot.reply_to(message, 'Getting nutrition info...')
    value = Resultnutrition(message.text)
    bot.reply_to(message, value)

def Resultnutrition(text):
    text = text[11:]
    payload = {"query" : text}
    file = open('nutrition_records.csv', 'w',newline="")
    writer = csv.writer(file)

    response = requests.post("https://trackapi.nutritionix.com/v2/natural/nutrients", headers=headers, data = json.dumps(payload))
    data = json.loads(response.text)
    x = 0
    response_message = ""
    for key,value in data["foods"][0].items():
        if(value==None) :
            continue
        response_message = response_message + key + ": " + str(value) + "\n"
        writer.writerow([key,value])
        x = x + 1
        if(x > 9):
            return response_message


@bot.message_handler(func=lambda message: botRunning, commands=['exercise'])
def getCaloriesBurn(message):
    bot.reply_to(message, 'Estimating calories burned...')
    response = ResultExcercise(message.text)
    bot.reply_to(message, response)

def ResultExcercise(text):
    text = text[9:]
    payload = {"query" : text}
    file = open('exercise_records.csv', 'w',newline="")
    writer = csv.writer(file)

    response = requests.post("https://trackapi.nutritionix.com/v2/natural/exercise", headers=headers, data = json.dumps(payload))
    data = json.loads(response.text)
    x = 0
    response_message = ""
    for key,value in data["exercises"][0].items():
        if(value==None) :
            continue
        response_message = response_message + key + ": " + str(value) + "\n"
        writer.writerow([key,value])
        x = x + 1
        if(x > 4):
            return response_message

@bot.message_handler(func=lambda message: botRunning, commands=['reports'])
def getCaloriesBurn(message):
    bot.reply_to(message, 'Generating report...')
    bot.send_document(chat_id=update.message.chat_id, document=file)
    usr_input = message.text[10:]
    reports = usr_input.split(', ')
    if("nutrition" in reports):
        bot.send_document(message.chat.id, data= open(nutrition_records,'rb'))
    if("exercise" in reports):
        bot.send_document(message.chat.id, data= open(exercise_records,'rb'))


@bot.message_handler(func=lambda message: botRunning)
def default(message):
    bot.reply_to(message, 'I did not understand '+'\N{confused face}')
keep_alive()

bot.infinity_polling()
