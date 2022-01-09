import os
from os import environ
import telebot
import requests
import json
import csv
import re

# TODO: 1.1 Add Request HTTP URL of the API
NUTRITIONIX_API_KEY = environ['NUTRITIONIX_API_KEY']
NUTRITIONIX_APP_ID = environ['NUTRITIONIX_APP_ID']
HTTP_API = environ['http_api']
HTTP_URL_NUTRITION = "https://trackapi.nutritionix.com/v2/natural/nutrients"
HTTP_URL_EXERCISE = "https://trackapi.nutritionix.com/v2/natural/exercise"

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
    user_data = usr_input.split(', ')
    print(user_data)
    user["name"] = user_data[0]
    user["gender"] = user_data[1]
    user["weight"] = user_data[2]
    user["height"] = user_data[3]
    user["age"] = user_data[4]
    bot.reply_to(message, 'User set!')
    # TODO: 2.2 Display user details in the telegram chat
    reply = "Name: " + user["name"] + "\nGender: " + user["gender"] + "\nWeight: " + str(user["weight"]) + "\nHeight: " + str(user["height"]) + "\nAge: " + str(user["age"]) 
    bot.send_message(message.chat.id, reply)


@bot.message_handler(func=lambda message: botRunning, commands=['nutrition'])
def getNutrition(message):
    bot.reply_to(message, 'Getting nutrition info...')
    # TODO: 1.2 Get nutrition information from the API
    text = message.text[11:] 
    print(text)
    body = {
        "query": text,
        "timezone": "IN/Kolkata"
    }
    res = requests.post(HTTP_URL_NUTRITION,headers= headers, json= body)
    if(res.status_code != 200):
        print("Response Error!")
        print(res.status_code)
    
    # TODO: 1.3 Display nutrition data in the telegram chat
    nutrient_list = ["food_name",
            "serving_qty",
            "nf_calories",
            "nf_total_fat",
            "nf_total_carbohydrate",
            "nf_protein"]

    nutrient_dict = {"serving_weight_grams":"Serving weight(gms)",
            "food_name":"Food Name",
            "serving_qty":"Quantity",
            "nf_calories":"Calories",
            "nf_total_fat":"Total Fat",
            "nf_saturated_fat":"Saturated Fat",
            "nf_cholesterol":"Cholestrol",
            "nf_sodium":"Sodium",
            "nf_total_carbohydrate":"Total Carbohydrate",
            "nf_dietary_fiber":"Dietary Fibre",
            "nf_sugars":"Sugars",
            "nf_protein":"Protein",
            "nf_potassium":"Potassium"}

    res = res.json()
    reply = ''
    nutrient_values = res["foods"][0]
    for nutrient in nutrient_list:
        reply += nutrient_dict[nutrient] + ": " + str(nutrient_values[nutrient]) + "\n"
    
    print(reply)
    bot.send_message(message.chat.id, reply)
    # TODO: 3.2 Dump data in a CSV file


@bot.message_handler(func=lambda message: botRunning, commands=['exercise'])
def getCaloriesBurn(message):
    bot.reply_to(message, 'Estimating calories burned...')
    # TODO: 2.3 Get exercise data from the API
    body = {
    "query": message.text[10:],
    "gender": user["gender"],
    "weight_kg": user["weight"],
    "height_cm": user["height"],
    "age": user["age"]
    }
    res = requests.post(HTTP_URL_EXERCISE,headers= headers, json= body)
    if(res.status_code != 200):
        print("Response Error!")
        print(res.status_code)
    res = res.json()
    # TODO: 2.4 Display exercise data in the telegram chat
    Exname = str(res["exercises"][0]["name"])
    ExDuration = str(res["exercises"][0]["duration_min"])
    ExCalories = str(res["exercises"][0]["nf_calories"])
    reply = "Exercise Name: " + Exname
    reply += "\nDuration: " + ExDuration
    reply += "\nCalories Burned: " + ExCalories
    print(reply)
    bot.send_message(message.chat.id, reply)
    # TODO: 3.3 Dump data in a CSV file


@bot.message_handler(func=lambda message: botRunning, commands=['reports'])
def getCaloriesBurn(message):
    bot.reply_to(message, 'Generating report...')
    # TODO: 3.4 Send downlodable CSV file to telegram chat


@bot.message_handler(func=lambda message: botRunning)
def default(message):
    bot.reply_to(message, 'I did not understand '+'\N{confused face}')


bot.infinity_polling()
