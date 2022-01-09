import os,logging
from os import environ
from decouple import config
import telebot
import requests
import json
import csv


# TODO: 1.1 Add Request HTTP URL of the API
NUTRITIONIX_API_KEY = config('NUTRITIONIX_API_KEY')
NUTRITIONIX_APP_ID = config('NUTRITIONIX_APP_ID')
HTTP_API = config('http_api')



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
    global file
    file=open('nutrition_records.csv','a')
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
    usr_input = message.text[6:].split(',')
    # TODO: 2.1 Set user data
    try:
        global name,gender,weight,height,age
        name=usr_input[0]
        gender=usr_input[1]
        weight=int(usr_input[2])
        height=int(usr_input[3])
        age=int(usr_input[4])
        bot.reply_to(message, 'User set!')

    except (Exception) as e:
        bot.reply_to(message,"Error, Invalid format")
    reply = ''
    # TODO: 2.2 Display user details in the telegram chat
    reply="Name: "+name+"\nGender: "+gender+"\nWeight(Kg): "+str(weight)+"\nHeight(cm): "+str(height)+"\nAge: "+str(age)
    bot.send_message(message.chat.id, reply)


@bot.message_handler(func=lambda message: botRunning, commands=['nutrition'])
def getNutrition(message):
    bot.reply_to(message,'Getting nutrition info searching...')
    # TODO: 1.2 Get nutrition information from the API
    # TODO: 1.3 Display nutrition data in the telegram chat
    cont=message.text.split()
    # data=["Food Item ","Calories"," Total Fat","Carbohydrates","Protein"]
    if isinstance(cont[1], int):
        n=cont[1]
        r=requests.post("https://api.nutritionix.com/v1_1/search",json={"appId":NUTRITIONIX_APP_ID,"appKey":NUTRITIONIX_API_KEY,"fields": [
            "item_name",
            "item_description",
            "nf_calories",
            "nf_total_fat",
            "nf_total_carbohydrate",
            "nf_protein",
            "item_type",
            "nf_serving_size_qty",
        ],"query":cont[2]})
        data=r.json()
        row=(data['hits'][0]['fields'])
        rowcsv=[cont[2],row['nf_calories']*n,row['nf_total_fat']*n,_row['nf_total_carbohydrate']*n,row['nf_protein']*n]
        reply=("Food Item: "+f"{cont[2]}"+"\nCalories: "+str(row['nf_calories']*n)+"\nTotal Fat: "+str(row['nf_total_fat']*n)+"\nCarbohydrates: "+str(row['nf_total_carbohydrate']*n)+"\nProtein: "+str(row['nf_protein']*n))
        bot.reply_to(message,reply)
    elif type(cont[1])!=int:
        r=requests.post("https://api.nutritionix.com/v1_1/search",json={"appId":NUTRITIONIX_APP_ID,"appKey":NUTRITIONIX_API_KEY,"fields": [
            "item_name",
            "item_description",
            "nf_calories",
            "nf_total_fat",
            "nf_total_carbohydrate",
            "nf_protein",
            "item_type",
            "nf_serving_size_qty",
        ],"query":cont[1]})
        data=r.json()
        row=(data['hits'][0]['fields'])
        print(row)
        rowcsv=[str(cont[1]),str(row['nf_calories']),str(row['nf_total_fat']),str(row['nf_total_carbohydrate']),str(row['nf_protein'])]
        reply=("Food Item: "+f"{cont[1]}"+"\nCalories: "+str(row['nf_calories'])+"\nTotal Fat: "+str(row['nf_total_fat'])+"\nCarbohydrates: "+str(row['nf_total_carbohydrate'])+"\nProtein: "+str(row['nf_protein']))
        bot.reply_to(message,reply)


    # TODO: 3.2 Dump data in a CSV file
    writer=csv.writer(file)
    # writer.writerow(data)
    writer.writerows(rowcsv)


@bot.message_handler(func=lambda message: botRunning, commands=['exercise'])
def getCaloriesBurn(message):
    bot.reply_to(message, 'Estimating calories burned...')
    exercise=message.text[9:]
    url="https://trackapi.nutritionix.com/v2/natural/exercise"
    h={"x-app-id":NUTRITIONIX_APP_ID,"x-app-key":NUTRITIONIX_API_KEY}
    Headers = {'Content-Type': 'application/json',
           'x-app-id': NUTRITIONIX_APP_ID, 'x-app-key': NUTRITIONIX_API_KEY}

    data_json = {
        'query': exercise,
        'gender': gender,
        'weight_kg': weight,
        'height_cm': height,
        'age': age,
    }
    r=requests.post(url,json=data_json, headers=Headers )
    


    # TODO: 2.3 Get exercise data from the API
    # TODO: 2.4 Display exercise data in the telegram chat
    # TODO: 3.3 Dump data in a CSV file


@bot.message_handler(func=lambda message: botRunning, commands=['reports'])
def getCaloriesBurn(message):
    bot.reply_to(message, 'Generating report...')
    # TODO: 3.4 Send downlodable CSV file to telegram chat
    typr=message.text[9:]
    if typr=="nutrition":
        bot.send_document(message.chat.id,"nutrition_records.csv")
    elif typr=="exercise":
        bot.send_document(message.chat.id,"exercise_records.csv")


@bot.message_handler(func=lambda message: botRunning)
def default(message):
    bot.reply_to(message, 'I did not understand '+'\N{confused face}')


bot.infinity_polling()
