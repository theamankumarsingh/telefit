import os
from os import environ
from dotenv import load_dotenv
load_dotenv()
import telebot
import requests
import json
import csv
import re

# TODO: 1.1 Add Request HTTP URL of the API
nut_end_point_url = 'https://trackapi.nutritionix.com/v2/natural/nutrients'
exercise_end_point_url = 'https://trackapi.nutritionix.com/v2/natural/exercise'

NUTRITIONIX_API_KEY = environ['NUTRITIONIX_API_KEY']
NUTRITIONIX_APP_ID = environ['NUTRITIONIX_APP_ID']
HTTP_API = environ['http_api']

HEADERS = {'Content-Type': 'application/json',
           'x-app-id': NUTRITIONIX_APP_ID, 'x-app-key': NUTRITIONIX_API_KEY}
user = {'name': None, 'gender': None,
        'weight': None, 'height': None, 'age': None}
bot = telebot.TeleBot(HTTP_API)


@bot.message_handler(commands=['start', 'hello'])
def greet(message):
    global botRunning
    botRunning = True
    # TODO: 3.1 Add CSV file creation
    global nutrition_csv
    global exercise_csv
    nutrition_csv = open('nutrition.csv', 'w', newline='')
    exercise_csv = open('exercise.csv', 'w', newline='')
    global output_nutrition
    global output_exercise
    output_nutrition = csv.writer(nutrition_csv)
    output_exercise = csv.writer(exercise_csv)
    bot.reply_to(
        message,
        'Hello! I am TeleFit. Use me to monitor your health' + '\N{grinning face with smiling eyes}' + '\nYou can use the command \"/help\" to know more about me.')


@bot.message_handler(commands=['stop', 'bye'])
def goodbye(message):
    global botRunning
    botRunning = False
    bot.reply_to(message, 'Bye!\nStay Healthy' + '\N{flexed biceps}')

@bot.message_handler(func=lambda message: botRunning, commands=['help'])
def helpProvider(message):
    bot.reply_to(message,
                 '1.0 You can use \"/nutrition Units Quantity-Type Food-Name\" command to get the nutrients of a particular food. For eg: \"/nutrition 1 piece chapati\"\n\n2.1 For using the bot to get details about an exercise you need to first set the user data using the command \"/user Name, Gender, Weight(in Kg), Height (in cm), Age\". For eg: \"/user Akshat, Male, 70, 6, 19\n\n2.2 Then you can use the command \"/execise Duration-amount Duration-unit Exercise-name\" to get data about an exercise. For eg: \"/exercise 40 minutes push-ups\"\n\n3.0. You can use the command \"/reports Report-name\" to get the reports in CSV Format. For eg: \"/reports nutrition\" to get nutrition report and \"/reports exercise\" to get exercise reports or use the command \"/reports nutrition, exercise\" to get both nutrition and exercise reports\n\n4.0. You can use the command \"/stop\" or the command \"/bye\" to stop the bot.')


@bot.message_handler(func=lambda message: botRunning, commands=['user'])
def setUser(message):
    global user
    usr_input = message.text[6:]
    # TODO: 2.1 Set user data
    pattern = re.compile(r'(\w+),\s(\w+),\s(\d+),\s(\d+),\s(\d+)')
    userdata = pattern.search(usr_input)

    user['name'] = userdata[1]
    user['gender'] = userdata[2]
    user['weight'] = userdata[3]
    user['height'] = userdata[4]
    user['age'] = userdata[5]

    bot.reply_to(message, 'User set!')
    reply = ('name: ' + user['name'] + '\n' +
             'gender: ' + user['gender'] + '\n' +
             'weight: ' + str(user['weight']) + '\n' +
             'height: ' + str(user['height']) + '\n' +
             'age: ' + str(user['age']) + '\n')
    # TODO: 2.2 Display user details in the telegram chat
    bot.send_message(message.chat.id, reply)


@bot.message_handler(func=lambda message: botRunning, commands=['nutrition'])
def getNutrition(message):
    bot.reply_to(message, 'Getting nutrition info...')
    # TODO: 1.2 Get nutrition information from the API

    query = {
        'query': message.text[11:]
    }
    r_nut = requests.post(nut_end_point_url, headers=HEADERS, json=query)
    nut_data = json.loads(r_nut.text)

    # TODO: 1.3 Display nutrition data in the telegram chat
    reply_data = ('Food Name: ' + nut_data['foods'][0]['food_name'] + '\n' +
                  'Quantity: ' + str(nut_data['foods'][0]['serving_qty']) + '\n' +
                  'Calories: ' + str(nut_data['foods'][0]['nf_calories']) + '\n' +
                  'Fat: ' + str(nut_data['foods'][0]['nf_total_fat']) + '\n' +
                  'Carbohydrate: ' + str(nut_data['foods'][0]['nf_total_carbohydrate']) + '\n' +
                  'Protein: ' + str(nut_data['foods'][0]['nf_protein']))
    bot.send_message(message.chat.id, reply_data)
    # TODO: 3.2 Dump data in a CSV file
    output_nutrition.writerow(['Food Name', 'Quantity', 'Calories', 'Fat', 'Carbohydrate', 'Protein'])
    output_nutrition.writerow(
        [nut_data['foods'][0]['food_name'], nut_data['foods'][0]['serving_qty'], nut_data['foods'][0]['nf_calories'],
        nut_data['foods'][0]['nf_total_fat'], nut_data['foods'][0]['nf_total_carbohydrate'],
                             nut_data['foods'][0]['nf_protein']])


@bot.message_handler(func=lambda message: botRunning, commands=['exercise'])
def getCaloriesBurn(message):
    bot.reply_to(message, 'Estimating calories burned...')
    # TODO: 2.3 Get exercise data from the API
    query = {
        'query': message.text[10:],
        'gender': user['gender'],
        'weight_kg': user['weight'],
        'height_cm': user['height'],
        'age': user['age']
    }
    r_exer = requests.post(exercise_end_point_url, headers=HEADERS, json=query)
    exercise_data = json.loads(r_exer.text)
    # TODO: 2.4 Display exercise data in the telegram chat
    reply_exercise = ('Exercise Name: ' + exercise_data['exercises'][0]['name'] + '\n' +
                      'Duration: ' + str(exercise_data['exercises'][0]['duration_min']) + '\n' +
                      'Calories Burned: ' + str(exercise_data['exercises'][0]['nf_calories']) + '\n')
    bot.send_message(message.chat.id, reply_exercise)
    # TODO: 3.3 Dump data in a CSV file
    output_exercise.writerow(['Exercise Name', 'Duration', 'Calories Burned'])
    output_exercise.writerow([exercise_data['exercises'][0]['name'], exercise_data['exercises'][0]['duration_min'],
                              exercise_data['exercises'][0]['nf_calories']])

@bot.message_handler(func=lambda message: botRunning, commands=['reports'])
def getCaloriesBurn(message):
    bot.reply_to(message, 'Generating report...')
    # TODO: 3.4 Send downlodable CSV file to telegram chat
    nutrition_csv.close()
    exercise_csv.close()
    nutrition = open('nutrition.csv', 'rb')
    exercise = open('exercise.csv', 'rb')
    if message.text[9:] == 'nutrition':
        bot.send_document(message.chat.id, nutrition, protect_content=False)
    if message.text[9:] == 'exercise':
        bot.send_document(message.chat.id, exercise, protect_content=False)
    if message.text[9:] == 'nutrition, exercise':
        bot.send_document(message.chat.id, nutrition, protect_content=False)
        bot.send_document(message.chat.id, exercise, protect_content=False)
    else:
        default(message)

@bot.message_handler(func=lambda message: botRunning)
def default(message):
    bot.reply_to(message, 'I did not understand ' + '\N{confused face}')


bot.infinity_polling()
