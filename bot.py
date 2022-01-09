import os
from os import environ
import telebot
import requests
import json
import csv,io

from telebot.types import Message

# TODO: 1.1 Add Request HTTP URL of the API
os.environ['NUTRITIONIX_API_KEY'] 
os.environ['NUTRITIONIX_APP_ID'] 
os.environ['http_api'] 
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

    global nutritionFile 
    nutritionFile= open('nutrition_records.csv','w',newline='')
    global exerciseFile 
    exerciseFile = open('exercise_records.csv','w',newline='')

    global nutrition_File_writter 
    nutrition_File_writter= csv.DictWriter(nutritionFile,['Food-Name','Quantity','Calories','Fat','Carbohydrate','Protien'])
    global exercise_File_writter 
    exercise_File_writter= csv.DictWriter(exerciseFile,['Exercise-Name','Duration','Calories-Burnd'])

    nutrition_File_writter.writeheader()
    exercise_File_writter.writeheader()

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

    lis = usr_input.split(', ')
    user['name'] = lis[0] 
    user['gender'] = lis[1]
    user['weight'] = lis[2]
    user['height'] = lis[3]
    user['age'] = lis[4]

    bot.reply_to(message, 'User set!')
    
    # TODO: 2.2 Display user details in the telegram chat

    reply = 'name: '+ user['name'] +'\ngender: '+user['gender'] +'\nweight: '+user['weight']+'\nheight: '+user['height']+'\nage: '+user['age']
    bot.send_message(message.chat.id, reply)


@bot.message_handler(func=lambda message: botRunning, commands=['nutrition'])
def getNutrition(message):
    bot.reply_to(message, 'Getting nutrition info...')
    # TODO: 1.2 Get nutrition information from the API

    url = 'https://trackapi.nutritionix.com/v2/natural/nutrients'
    query = {'query': message.text[11:]}
    response = requests.post(url, headers=headers,json=query)
    data = json.loads(response.text)
    
    # TODO: 1.3 Display nutrition data in the telegram chat
    bot.reply_to(message,'Food name: '+ data['foods'][0]['food_name']+'\n Quantity: '+ str(message.text[11:18])  + '\n Calories: ' + str(data['foods'][0]['nf_calories']) + '\n Fat: ' + str(data['foods'][0]['nf_total_fat']) + '\n Carbohydrates: ' + str(data['foods'][0]['nf_total_carbohydrate']) + '\n Protien: '+ str(data['foods'][0]['nf_protein']))
    
    # TODO: 3.2 Dump data in a CSV file
    
    nutrition_File_writter.writerow({'Food-Name':data['foods'][0]['food_name'],'Quantity':str(message.text[11:18]),'Calories':str(data['foods'][0]['nf_calories']),'Fat':str(data['foods'][0]['nf_total_fat']),'Carbohydrate':str(data['foods'][0]['nf_total_carbohydrate']),'Protien':str(data['foods'][0]['nf_protein'])})
    

@bot.message_handler(func=lambda message: botRunning, commands=['exercise'])
def getCaloriesBurn(message):
    bot.reply_to(message, 'Estimating calories burned...')
    # TODO: 2.3 Get exercise data from the API

    url = 'https://trackapi.nutritionix.com/v2/natural/exercise'
    query={'query':message.text[10:]}
    response = requests.post(url,headers=headers,json=query)
    data = json.loads(response.text)


    Exercise_data = {
        'Exercise Name':data['exercises'][0]['name'],
        'Duration':message.text[10:20],
        'Calories Burned':data['exercises'][0]['nf_calories']
    }

    # TODO: 2.4 Display exercise data in the telegram chat
    reply = 'Exercise Name: '+Exercise_data['Exercise Name'] + '\nDuration: '+str(Exercise_data['Duration'])+ '\nCalories Burned: '+str(Exercise_data['Calories Burned'])
    bot.send_message(message.chat.id, reply)
    # TODO: 3.3 Dump data in a CSV file

    exercise_File_writter.writerow({'Exercise-Name':Exercise_data['Exercise Name'],'Duration':str(Exercise_data['Duration']),'Calories-Burnd':str(Exercise_data['Calories Burned'])})

@bot.message_handler(func=lambda message: botRunning, commands=['reports'])
def getCaloriesBurn(message):
    bot.reply_to(message, 'Generating report...\n')
    # TODO: 3.4 Send downlodable CSV file to telegram chat

    if message.text[9:] == 'nutrition':
      
      f = open('nutrition_records.csv','rb')
      bot.send_document(message.chat.id,f)
      f.close()
    elif message.text[9:] == 'exercise':
        
        f = open('exercise_records.csv','rb')
        bot.send_document(message.chat.id,f)
        f.close()
    elif message.text[9:] == 'nutrition, exercise':
        
        exerciseFile.close()
        f = open('nutrition_records.csv','rb')
        bot.send_document(message.chat.id,f)
        f.close()
        file = open('exercise_records.csv','rb')
        bot.send_document(message.chat.id,file)
        file.close()


@bot.message_handler(func=lambda message: botRunning)
def default(message):
    bot.reply_to(message, 'I did not understand '+'\N{confused face}')


bot.infinity_polling()
