import os
from time import time
import urllib.request
import telebot
import requests
import json
import csv
import telepot

# TODO: 1.1 Add Request HTTP URL of the API

NUTRITIONIX_API_KEY = os.getenv('nutrionix_api_key')
NUTRITIONIX_APP_ID = os.getenv('NUTRITIONIX_APP_ID')
HTTP_API = os.getenv('api_key')
BASE_URL = 'https://trackapi.nutritionix.com/v2/'
#url= 'https://trackapi.nutritionix.com/v2/search/instant'

headers = {'Content-Type': 'application/json',
           'x-app-id': NUTRITIONIX_APP_ID, 'x-app-key': NUTRITIONIX_API_KEY}
user = {'name': None, 'gender': None,
        'weight': None, 'height': None, 'age': None}
bot = telebot.TeleBot('5092698710:AAF_Tn7PszopBAjpeTIf0Y88vhR2tDUqJgI')


@bot.message_handler(commands=['start', 'hello'])
def greet(message):
    global botRunning
    botRunning = True
    # TODO: 3.1 Add CSV file creation
    global outputFile
    outputFile = open('nutriton.csv', 'w', newline='')
    outputDictWriter = csv.DictWriter(outputFile,["Food-Name","Quantity","Calories","Fat","Carbohydrates","Protein"])
    outputDictWriter.writeheader() 
    global ExerciseFile
    ExerciseFile = open('Exercise.csv', 'w', newline='')
    outputDictWriterExe = csv.DictWriter(ExerciseFile,["Exercise-Name","Duration","Calories-Burned"])
    outputDictWriterExe.writeheader()
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
    l=usr_input.split(",")
    name=l[0]
    global gender
    gender=l[1]
    global weight
    weight=l[2]
    global height
    height=l[3]
    global age
    age=l[4]
    bot.reply_to(message, 'User set!')
    reply = 'name:{}\n gender:{}\n weight:{}\n height:{}\n age:{}'.format(name,gender,weight,height,age)
    # TODO: 2.2 Display user details in the telegram chat
    bot.send_message(message.chat.id, reply)


@bot.message_handler(func=lambda message: botRunning, commands=['nutrition'])
def getNutrition(message):
    url = "{0}natural/nutrients".format(BASE_URL)
    bot.reply_to(message, 'Getting nutrition info...')
    req=message.text.split()
    #food_name=" ".join(req[1:])
    food_name = req[-1]
    qua=req[1]
    print("food name ", food_name)
    body={
        "query":"{}".format(food_name)
    }
    response = requests.post(url, headers=headers, json=body, allow_redirects=False, timeout=30)
    data=response.json()    
    i=data["foods"][0]
    msg='Food Name: {}\nQuantity: {} {}\nCalories: {}\nFat:{}\nCarbohydrate:{}\nProtein:{}'.format(i['food_name'],qua,i["serving_unit"],i["nf_calories"],i["nf_total_fat"],i["nf_total_carbohydrate"],i["nf_protein"])
    bot.send_message(message.chat.id, msg)
    outputFile = open('nutrition.csv', 'a', newline='')
    outputDictWriter = csv.DictWriter(outputFile,["Food-Name","Quantity","Calories","Fat","Carbohydrates","Protein"])
    if outputFile.tell() == 0:
        outputDictWriter.writeheader()   
    outputDictWriter.writerow({"Food-Name":'{}'.format(i['food_name']),"Quantity":'{}'.format(qua),"Calories":'{}'.format(i['nf_calories']),"Fat":'{}'.format(i['nf_total_fat']),"Carbohydrates":'{}'.format(i["nf_total_carbohydrate"]),"Protein":'{}'.format(i["nf_protein"])})
    
    # TODO: 1.2 Get nutrition information from the API
    # TODO: 1.3 Display nutrition data in the telegram chat
    # TODO: 3.2 Dump data in a CSV file


@bot.message_handler(func=lambda message: botRunning, commands=['exercise'])
def getCaloriesBurn(message):
    url = "{0}natural/exercise".format(BASE_URL)
    bot.reply_to(message, 'Estimating calories burned...')
    req=message.text.split()
    exer =req[1]+" "+req[2]+" "+req[-1]
    time=req[1]+" "+req[2]
    body={
        "query":"{}".format(exer),
        "gender":"{}".format(gender),
        "weight_kg":"{}".format(weight),
        "height_cm":"{}".format(height),
        "age":"{}".format(age)
    }
    response = requests.post(url, headers=headers, json=body, allow_redirects=False, timeout=30)
    data=response.json()
    i=data["exercises"][0]
    msg="Exercise Name: {}\n Duration: {}\n Calories Burned: {}".format(req[-1],time,i["nf_calories"])
    bot.send_message(message.chat.id, msg)
    ExerciseFile = open('Exercise.csv', 'a', newline='')
    outputDictWriterExe = csv.DictWriter(ExerciseFile,["Exercise-Name","Duration","Calories-Burned"])
    if ExerciseFile.tell() == 0:
        outputDictWriterExe.writeheader()   
    outputDictWriterExe.writerow({"Exercise-Name":'{}'.format(req[-1]),"Duration":'{}'.format(time),"Calories-Burned":'{}'.format(i['nf_calories'])})
    # TODO: 2.3 Get exercise data from the API
    # TODO: 2.4 Display exercise data in the telegram chat
    # TODO: 3.3 Dump data in a CSV file


@bot.message_handler(func=lambda message: botRunning, commands=['reports'])
def getCaloriesBurn(message):
    bot.reply_to(message, 'Generating report...')
    # TODO: 3.4 Send downlodable CSV file to telegram chat
    req=message.text.split()
    if(req[1]=="exercise"):
        file=open("Exercise.csv",'r')
        bot.send_document(message.chat.id,data=file,caption="Exercise.csv")
    elif(req[1]=="nutrition"):
        file=open("nutrition.csv",'r')
        bot.send_document(message.chat.id,data=file,caption="Exercise.csv")
    elif(req[1]=="exercise,nutrition" or req[1]=="nutrition,exercise"):
        file1=open("Exercise.csv",'r')
        bot.send_document(message.chat.id,data=file1,caption="Exercise.csv")
        file=open("nutrition.csv",'r')
        bot.send_document(message.chat.id,data=file,caption="Exercise.csv")


@bot.message_handler(func=lambda message: botRunning)
def default(message):
    bot.reply_to(message, 'I did not understand '+'\N{confused face}')


bot.polling()
