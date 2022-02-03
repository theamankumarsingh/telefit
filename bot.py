import os
from os import environ
#import telebot
import requests
import json
import csv
#import pyTelegramBotAPI

# TODO: 1.1 Add Request HTTP URL of the API

a= requests.get("https://api.nutritionix.com/v1_1/search/mcdonalds?results=0:20&fields=item_name,brand_name,item_id,nf_calories&appId=5d935adf&appKey=e0053975dfc4542a712d1afffb7c7671")
os.environ['NUTRITIONIX_API_KEY'] = 'e0053975dfc4542a712d1afffb7c7671'
os.environ['NUTRITIONIX_APP_ID'] = '5d935adf'
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
    bot.reply_to(message, 'User set!')
    reply = ''
    # TODO: 2.2 Display user details in the telegram chat
    bot.send_message(message.chat.id, reply)


@bot.message_handler(func=lambda message: botRunning, commands=['nutrition'])
def getNutrition(message):
    bot.reply_to(message, 'Getting nutrition info...')
    # TODO: 1.2 Get nutrition information from the API
    b=json.load('{"total_hits":207,"max_score":3.6226628,"hits":[{"_index":"f762ef22-e660-434f-9071-a10ea6691c27","_type":"item","_id":"152152206994a479c9298d37","_score":3.6226628,"fields":{"item_id":"152152206994a479c9298d37","item_name":"Quarter Pounder with Cheese Bacon","brand_name":"McDonald"s","nf_calories":630,"nf_serving_size_qty":1,"nf_serving_size_unit":"serving"}},{"_index":"f762ef22-e660-434f-9071-a10ea6691c27","_type":"item","_id":"513fc9e73fe3ffd40300108e","_score":3.6226628,"fields":{"item_id":"513fc9e73fe3ffd40300108e","item_name":"1% Low Fat Milk Jug","brand_name":"McDonald"s","nf_calories":100,"nf_serving_size_qty":1,"nf_serving_size_unit":"serving"}},{"_index":"f762ef22-e660-434f-9071-a10ea6691c27","_type":"item","_id":"513fc9e73fe3ffd4030010ab","_score":3.6226628,"fields":{"item_id":"513fc9e73fe3ffd4030010ab","item_name":"Chicken McNuggets, 6 Piece","brand_name":"McDonald"s","nf_calories":250,"nf_serving_size_qty":1,"nf_serving_size_unit":"serving"}},{"_index":"f762ef22-e660-434f-9071-a10ea6691c27","_type":"item","_id":"513fc9e73fe3ffd4030010b2","_score":3.6226628,"fields":{"item_id":"513fc9e73fe3ffd4030010b2","item_name":"Chocolate Shake, Small","brand_name":"McDonald"s","nf_calories":530,"nf_serving_size_qty":1,"nf_serving_size_unit":"serving"}},{"_index":"f762ef22-e660-434f-9071-a10ea6691c27","_type":"item","_id":"513fc9e73fe3ffd4030010c9","_score":3.6226628,"fields":{"item_id":"513fc9e73fe3ffd4030010c9","item_name":"Dr Pepper, Medium","brand_name":"McDonald"s","nf_calories":200,"nf_serving_size_qty":1,"nf_serving_size_unit":"serving"}},{"_index":"f762ef22-e660-434f-9071-a10ea6691c27","_type":"item","_id":"513fc9e73fe3ffd4030010ca","_score":3.6226628,"fields":{"item_id":"513fc9e73fe3ffd4030010ca","item_name":"Dr Pepper, Small","brand_name":"McDonald"s","nf_calories":140,"nf_serving_size_qty":1,"nf_serving_size_unit":"serving"}},{"_index":"f762ef22-e660-434f-9071-a10ea6691c27","_type":"item","_id":"513fc9e73fe3ffd4030010cf","_score":3.6226628,"fields":{"item_id":"513fc9e73fe3ffd4030010cf","item_name":"Filet-O-Fish Sandwich","brand_name":"McDonald"s","nf_calories":380,"nf_serving_size_qty":1,"nf_serving_size_unit":"serving"}},{"_index":"f762ef22-e660-434f-9071-a10ea6691c27","_type":"item","_id":"513fc9e73fe3ffd4030010f5","_score":3.6226628,"fields":{"item_id":"513fc9e73fe3ffd4030010f5","item_name":"Hot Chocolate, Small","brand_name":"McDonald"s","nf_calories":370,"nf_serving_size_qty":1,"nf_serving_size_unit":"serving"}},{"_index":"f762ef22-e660-434f-9071-a10ea6691c27","_type":"item","_id":"513fc9e73fe3ffd40300110e","_score":3.6226628,"fields":{"item_id":"513fc9e73fe3ffd40300110e","item_name":"Iced Coffee, Large","brand_name":"McDonald"s","nf_calories":260,"nf_serving_size_qty":1,"nf_serving_size_unit":"serving"}},{"_index":"f762ef22-e660-434f-9071-a10ea6691c27","_type":"item","_id":"513fc9e73fe3ffd403001110","_score":3.6226628,"fields":{"item_id":"513fc9e73fe3ffd403001110","item_name":"Iced Coffee, Small","brand_name":"McDonald"s","nf_calories":140,"nf_serving_size_qty":1,"nf_serving_size_unit":"s-erving"}},{"_index":"f762ef22-e660-434f-9071-a10ea6691c27","_type":"item","_id":"513fc9e73fe3ffd40300111b","_score":3.6226628,"fields":{"item_id":"513fc9e73fe3ffd40300111b","item_name":"Iced Tea, Large","brand_name":"McDonald"s","nf_calories":0,"nf_serving_size_qty":1,"nf_serving_size_unit":"serving"}},{"_index":"f762ef22-e660-434f-9071-a10ea6691c27","_type":"item","_id":"513fc9e73fe3ffd403001139","_score":3.6226628,"fields":{"item_id":"513fc9e73fe3ffd403001139","item_name":"World Famous Fries, Medium","brand_name":"McDonald"s","nf_calories":320,"nf_serving_size_qty":1,"nf_serving_size_unit":"serving"}},{"_index":"f762ef22-e660-434f-9071-a10ea6691c27","_type":"item","_id":"513fc9e73fe3ffd40300113a","_score":3.6226628,"fields":{"item_id":"513fc9e73fe3ffd40300113a","item_name":"Honest Kids Appley Ever After Organic Juice Drink","brand_name":"McDonald"s","nf_calories":35,"nf_serving_size_qty":1,"nf_serving_size_unit":"serving"}},{"_index":"f762ef22-e660-434f-9071-a10ea6691c27","_type":"item","_id":"513fc9e73fe3ffd40300117d","_score":3.6226628,"fields":{"item_id":"513fc9e73fe3ffd40300117d","item_name":"Sausage, Egg & Cheese McGriddles","brand_name":"McDonald"s","nf_calories":550,"nf_serving_size_qty":1,"nf_serving_size_unit":"serving"}},{"_index":"f762ef22-e660-434f-9071-a10ea6691c27","_type":"item","_id":"513fc9e73fe3ffd403001184","_score":3.6226628,"fields":{"item_id":"513fc9e73fe3ffd403001184","item_name":"McFlurry with OREO Cookies, Snack Size","brand_name":"McDonald"s","nf_calories":340,"nf_serving_size_qty":1,"nf_serving_size_unit":"serving"}},{"_index":"f762ef22-e660-434f-9071-a10ea6691c27","_type":"item","_id":"513fc9e73fe3ffd40300118f","_score":3.6226628,"fields":{"item_id":"513fc9e73fe3ffd40300118f","item_name":"Sprite, Medium","brand_name":"McDonald"s","nf_calories":170,"nf_serving_size_qty":1,"nf_serving_size_unit":"serving"}},{"_index":"f762ef22-e660-434f-9071-a10ea6691c27","_type":"item","_id":"513fc9e73fe3ffd403001191","_score":3.6226628,"fields":{"item_id":"513fc9e73fe3ffd403001191","item_name":"Strawberry Banana Smoothie, Large","brand_name":"McDonald"s","nf_calories":330,"nf_serving_size_qty":1,"nf_serving_size_unit":"serving"}},{"_index":"f762ef22-e660-434f-9071-a10ea6691c27","_type":"item","_id":"513fc9e73fe3ffd403001196","_score":3.6226628,"fields":{"item_id":"513fc9e73fe3ffd403001196","item_name":"Strawberry Shake, Large","brand_name":"McDonald"s","nf_calories":800,"nf_serving_size_qty":1,"nf_serving_size_unit":"serving"}},{"_index":"f762ef22-e660-434f-9071-a10ea6691c27","_type":"item","_id":"ae495051f4042f9fabd0857a","_score":3.6226628,"fields":{"item_id":"ae495051f4042f9fabd0857a","item_name":"Chicken McNuggets, 40 Piece","brand_name":"McDonald"s","nf_calories":1660,"nf_serving_size_qty":1,"nf_serving_size_unit":"serving"}},{"_index":"f762ef22-e660-434f-9071-a10ea6691c27","_type":"item","_id":"c6408349fd55c0abb61fe946","_score":3.6226628,"fields":{"item_id":"c6408349fd55c0abb61fe946","item_name":"Blueberry Muffin","brand_name":"McDonald"s","nf_calories":470,"nf_serving_size_qty":1,"nf_serving_size_unit":"serving"}}]}')
    # TODO: 1.3 Display nutrition data in the telegram chat
    
    # TODO: 3.2 Dump data in a CSV file


@bot.message_handler(func=lambda message: botRunning, commands=['exercise'])
def getCaloriesBurn(message):
    bot.reply_to(message, 'Estimating calories burned...')
    # TODO: 2.3 Get exercise data from the API
    
    # TODO: 2.4 Display exercise data in the telegram chat
    # TODO: 3.3 Dump data in a CSV file


@bot.message_handler(func=lambda message: botRunning, commands=['reports'])
def getCaloriesBurn(message):
    bot.reply_to(message, 'Generating report...')
    # TODO: 3.4 Send downlodable CSV file to telegram chat


@bot.message_handler(func=lambda message: botRunning)
def default(message):
    bot.reply_to(message, 'I did not understand '+'\N{confused face}')


bot.infinity_polling()
