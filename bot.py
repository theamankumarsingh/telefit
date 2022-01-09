import os
from os import environ
from dotenv import load_dotenv
import telebot
import requests
import json
import csv

load_dotenv()  # take environment variables from .env.

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
    foodFile = open('food.csv', 'w+', newline='')
    foodFileWrite = csv.writer(foodFile)
    foodFileWrite.writerow(
        ['Food-Name', 'Quantity', 'Calories', 'Fat', 'Carbohydrates', 'Protein'])
    foodFile.close()
    workoutFile = open('workout.csv', 'w+', newline='')
    workoutFileWrite = csv.writer(workoutFile)
    workoutFileWrite.writerow(['Exercise-Name', 'Duration', 'Calories-Burned'])
    workoutFile.close()
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
    global userwriterow
    # print(message)
    usr_input = message.text[6:].split()
    # TODO: 2.1 Set user data
    bot.reply_to(message, 'User set!')
    user['age'] = usr_input[4]
    user['gender'] = usr_input[1]
    user['height'] = usr_input[3]
    user['name'] = usr_input[0]
    user['weight'] = usr_input[2]
    reply = f"Name: {usr_input[0]} \nGender: {usr_input[1]} \nWeight: {usr_input[2]} \nHeight: {usr_input[3]} \nAge: {usr_input[4]}"
    # TODO: 2.2 Display user details in the telegram chat
    bot.send_message(message.chat.id, reply)


@bot.message_handler(func=lambda message: botRunning, commands=['nutrition'])
def getNutrition(message):
    bot.reply_to(message, 'Getting nutrition info...')
    msg = message.text[11:]
    url = "https://trackapi.nutritionix.com/v2/natural/nutrients"
    lst = []
    lst = []
    if 'and' in msg:
        lst = msg.split('and')
    if ',' in msg:
        lst = msg.split(',')
    else:
        lst.append(msg)
    for i in lst:
        payload = json.dumps({
            "query": i
        })
    # TODO: 1.2 Get nutrition information from the API
        response = requests.request("POST", url, headers=headers, data=payload)
        r = response.json()['foods'][0]
        foodDetails = {
            'foodName': r['food_name'],
            'quantity': str(str(r['serving_qty']) +
                            " " + r['serving_unit']),
            'calories': r['nf_calories'],
            'fat': r['nf_total_fat'],
            'carbohydrate': r['nf_total_carbohydrate'],
            'protein': r['nf_protein']
        }
    # TODO: 1.3 Display nutrition data in the telegram chat
        bot.reply_to(
            message, f"So.. Your Dietary values are out.. Check it out \nFood Name: {foodDetails['foodName']} \nQuantity: {foodDetails['quantity']} \nCalories: {foodDetails['calories']} \nFat: {foodDetails['fat']} \nCarbohydrate: {foodDetails['carbohydrate']} \nProtein: {foodDetails['protein']}")
    # TODO: 3.2 Dump data in a CSV file

        foodFile = open('food.csv', 'a')
        foodFileWrite = csv.writer(foodFile)
        foodFileWrite.writerow(
            [foodDetails['foodName'], foodDetails['quantity'], foodDetails['calories'], foodDetails['fat'], foodDetails['carbohydrate'], foodDetails['protein']])
        foodFile.close()


@bot.message_handler(func=lambda message: botRunning, commands=['exercise'])
def getCaloriesBurn(message):
    bot.reply_to(
        message, "Work Work Till You Sulk.. Here's your estimated calories burned...")
    msg = message.text[10:]
    url = "https://trackapi.nutritionix.com/v2/natural/exercise"
    lst = []
    if 'and' in msg:
        lst = msg.split('and')
    if ',' in msg:
        lst = msg.split(',')
    else:
        lst.append(msg)
    for i in lst:
        payload = json.dumps({
            "query": i,
            "gender": user['gender'],
            "weight_kg": int(user['weight']),
            "height_cm": int(user['height']),
            "age": int(user['age'])
        })
    # TODO: 2.3 Get exercise data from the API
        response = requests.request("POST", url, headers=headers, data=payload)
        r = response.json()['exercises'][0]
    # TODO: 2.4 Display exercise data in the telegram chat
        if len(r['exercises']) == 2:
            reply = 'Exercise Name: ' + str(r['exercises'][1]["name"]) + '\n' + 'Duration: ' + str(
                r['exercises'][1]["duration_min"]) + '\n' + 'Calories Burned: ' + str(r['exercises'][1]["nf_calories"])
        else:
            reply = 'Exercise Name: ' + str(r['exercises'][0]["name"]) + '\n' + 'Duration: ' + str(
                r['exercises'][0]["duration_min"]) + '\n' + 'Calories Burned: ' + str(r['exercises'][0]["nf_calories"])

        bot.reply_to(message, reply)
    # TODO: 3.3 Dump data in a CSV file

        workoutFile = open('workout.csv', 'a')
        workoutFileWrite = csv.writer(workoutFile)
        if len(r["exercises"]) == 2:
            string = [str(r['exercises'][1]["name"]), int(
                r['exercises'][1]["duration_min"]), int(r['exercises'][1]["nf_calories"])]
            workoutFileWrite.writerow(string)
        else:
            string = [str(r['exercises'][0]["name"]), int(
                r['exercises'][0]["duration_min"]), int(r['exercises'][0]["nf_calories"])]
            workoutFileWrite.writerow(string)
        workoutFile.close()


@ bot.message_handler(func=lambda message: botRunning, commands=['reports'])
def getCaloriesBurn(message):
    bot.reply_to(message, 'Generating report...')
    # TODO: 3.4 Send downlodable CSV file to telegram chat

    val = message.text[8:].split()
    if(len(val) == 1):
        if(val[0] == 'nutrition'):
            doc1 = open('food.csv', 'rb')
            bot.send_document(message.chat.id, doc1)
        elif(val[0] == 'exercise'):
            doc2 = open('workout.csv', 'rb')
            bot.send_document(message.chat.id, doc2)
    else:
        doc1 = open('food.csv', 'rb')
        bot.send_document(message.chat.id, doc1)
        doc2 = open('workout.csv', 'rb')
        bot.send_document(message.chat.id, doc2)


@ bot.message_handler(func=lambda message: botRunning)
def default(message):
    bot.reply_to(message, 'I did not understand '+'\N{confused face}')


bot.infinity_polling()
