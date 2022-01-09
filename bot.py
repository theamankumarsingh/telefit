import os
from os import environ
import telebot
import requests
import json
import csv
from dotenv import load_dotenv

load_dotenv()

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
    # TODO: 3.1 Add CSV file creation
    global outputFile
    outputFile = open('output.csv', 'w', newline='')
    
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
    usr_input = usr_input.split(',')
    user['name']=usr_input[0]
    user['gender']=usr_input[1]
    user['weight']=usr_input[2]
    user['height']=usr_input[3]
    user['age']=usr_input[4]
    bot.reply_to(message, 'User set!')
    reply = '''name: %s
gender: %s
weight: %s
height: %s
age: %s''' %(usr_input[0],usr_input[1],usr_input[2],usr_input[3],usr_input[4])
    # TODO: 2.2 Display user details in the telegram chat
    bot.send_message(message.chat.id, reply)


@bot.message_handler(func=lambda message: botRunning, commands=['nutrition'])
def getNutrition(message):
    bot.reply_to(message, 'Getting nutrition info...')
    # TODO: 1.2 Get nutrition information from the API

    data = {'query':message.text[11:]}
    result = requests.post('https://trackapi.nutritionix.com/v2/natural/nutrients',headers=headers,data=json.dumps(data))
    newData = json.loads(result.text)

    # TODO: 1.3 Display nutrition data in the telegram chat

    bot.send_message(message.chat.id,'''Food Name: %s
Quantity: %s
Calories: %s
Fat: %s
Carbohydrate: %s
Protein: %s'''%(newData['foods']['food_name'],newData['foods']['serving_qty'],newData['foods']['nf_calories'],newData['foods']['nf_total_fat'],newData['foods']['nf_total_carbohydrate'],newData['foods']['nf_protein'])
    )
    # TODO: 3.2 Dump data in a CSV file
    writer = csv.writer(outputFile)
    writer.writerow(newData['foods'])

@bot.message_handler(func=lambda message: botRunning, commands=['exercise'])
def getCaloriesBurn(message):
    bot.reply_to(message, 'Estimating calories burned...')
    # TODO: 2.3 Get exercise data from the API

    data = {'query':message.text[10:]}
    result = requests.post('https://trackapi.nutritionix.com/v2/natural/exercise',headers=headers,data=json.dumps(data))
    newData = json.loads(result.text)

    # TODO: 2.4 Display exercise data in the telegram chat

    bot.send_message(message.chat.id,'''Exercise Name: %s
Duration: %s
Calories Burned: %s''' %(newData['exercises']['user_input'],newData['exercises']['duration_min'],newData['exercises']['nf_calories'])
    )
    # TODO: 3.3 Dump data in a CSV file
    writer = csv.writer(outputFile)
    writer.writerow(newData['exercises'])

@bot.message_handler(func=lambda message: botRunning, commands=['reports'])
def getCaloriesBurn(message):
    bot.reply_to(message, 'Generating report...')
    # TODO: 3.4 Send downlodable CSV file to telegram chat
    bot.send_document(message.chat.id,outputFile,protect_content=False)

@bot.message_handler(func=lambda message: botRunning)
def default(message):
    bot.reply_to(message, 'I did not understand '+'\N{confused face}')


bot.infinity_polling()
