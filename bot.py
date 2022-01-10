import os
from os import environ
import telebot
import requests
import json
import csv
from dotenv import load_dotenv
load_dotenv()


# TODO: 1.1 Add Request HTTP URL of the API-Done
NUTRITIONIX_API_KEY = environ.get('NUTRITIONIX_API_KEY')
NUTRITIONIX_APP_ID = environ.get('NUTRITIONIX_APP_ID')
HTTP_API = environ.get('http_api')

headers = {'Content-Type': 'application/json',
           'x-app-id': NUTRITIONIX_APP_ID, 'x-app-key': NUTRITIONIX_API_KEY}
user = {'name': None, 'gender': None,
        'weight': None, 'height': None, 'age': None}
bot = telebot.TeleBot(HTTP_API)


@bot.message_handler(commands=['start', 'hello'])
def greet(message):
    global botRunning
    botRunning = True
    header_excer = ['Excercise-Name','Duration','Calories-Burned']
    header_nutri = ['Food-Name','Quantity','Calories','Fat','Carbohydrates','Protein']
    f = open('nutrition_details.csv', 'w')
    csvwriterf = csv.writer(f)
    csvwriterf.writerow(header_nutri)
    f.close()
    b = open('exercies_details.csv', 'w')
    csvwriterb = csv.writer(b)
    csvwriterb.writerow(header_excer)
    b.close()
    # TODO: 3.1 Add CSV file creation-Done
    bot.reply_to(
        message, 'Hello! I am TeleFit. Use me to monitor your health'+'\N{grinning face with smiling eyes}'+'\nYou can use the command \"/help\" to know more about me.')


@bot.message_handler(commands=['stop', 'bye'])
def goodbye(message):
    global botRunning
    botRunning = False
    bot.reply_to(message, 'Bye!\nStay Healthy'+'\N{flexed biceps}')


@bot.message_handler(func=lambda message: botRunning, commands=['help'])
def helpProvider(message):
    bot.reply_to(message, '1.0 You can use \"/nutrition Units Quantity-Type Food-Name\" command to get the nutrients of a particular food. For eg: \"/nutrition 1 piece chapati\"\n\n2.1 For using the bot to get details about an exercise you need to first set the user data using the command \"/user Name, Gender, Weight(in Kg), Height (in cm), Age\". For eg: \"/user Manoj, Male, 78, 6, 17\n\n2.2 Then you can use the command \"/execise Duration-amount Duration-unit Exercise-name\" to get data about an exercise. For eg: \"/exercise 40 minutes push-ups\"\n\n3.0. You can use the command \"/reports Report-name\" to get the reports in CSV Format. For eg: \"/reports nutrition\" to get nutrition report and \"/reports exercise\" to get exercise reports or use the command \"/reports nutrition, exercise\" to get both nutrition and exercise reports\n\n4.0. You can use the command \"/stop\" or the command \"/bye\" to stop the bot.')


@bot.message_handler(func=lambda message: botRunning, commands=['user'])
def setUser(message):
    global user
    usr_input = message.text[6:]
    Name, Gender, Weight, Height, Age = usr_input.split(', ')
    # TODO: 2.1 Set user data-Done
    bot.reply_to(message, 'User set!')
    reply = 'Name: '+str(Name)+'\n'+'Gender: '+str(Gender)+'\n'+'Weight: '+str(Weight)+'\n'+'Height: '+str(Height)+'\n'+'Age: '+str(Age)
    # TODO: 2.2 Display user details in the telegram chat-Done
    bot.send_message(message.chat.id, reply)


@bot.message_handler(func=lambda message: botRunning, commands=['nutrition'])
def getNutrition(message):
    bot.reply_to(message, 'Getting nutrition info...')
    data = message.text[11:]
    url = "https://trackapi.nutritionix.com/v2/natural/nutrients"
    x = requests.request("POST", url, headers=headers, json={"query":data})
    for i in x.json():
        for j in ((x.json())[i]):
            jsonNutri = j
    foodname = str(jsonNutri['food_name'])
    foodquantity = str(jsonNutri['serving_qty'])+' '+str(jsonNutri['serving_unit'])
    foodcalories = str(jsonNutri['nf_calories'])
    foodfat = str(jsonNutri['nf_total_fat'])
    foodcarbo = str(jsonNutri['nf_total_carbohydrate'])
    foodpro = str(jsonNutri['nf_protein'])
    messageNutri = "Food Name: " + foodname + '\n' + "Quantity: " + foodquantity + '\n' + "Calories: " + foodcalories + '\n' + "Fat: " + foodfat + '\n' + "Carbohydrate: " + foodcarbo + '\n' + "Protein: " + foodpro
    bot.send_message(message.chat.id, messageNutri)
    # TODO: 1.2 Get nutrition information from the API-Done
    # TODO: 1.3 Display nutrition data in the telegram chat-Done
    # TODO: 3.2 Dump data in a CSV file-Done
    d = []
    for i in [foodname,foodquantity,foodcalories,foodfat,foodcarbo,foodpro]:
        d.append(i)
    with open('nutrition_details.csv','a') as fn:
        csvwriter = csv.writer(fn)
        csvwriter.writerow(d)


@bot.message_handler(func=lambda message: botRunning, commands=['exercise'])
def getCaloriesBurn(message):
    bot.reply_to(message, 'Estimating calories burned...')
    data = message.text[10:]
    url = "https://trackapi.nutritionix.com/v2/natural/exercise"
    x = requests.request("POST", url, headers=headers, json={"query":data})
    for i in x.json():
        for j in (x.json())[i]:
            jsonExc = j
    excerciseName = str(jsonExc['user_input'])
    excerciseTime = str(jsonExc['duration_min'])+' minutes'
    excerciseCal = str(jsonExc['nf_calories'])
    messageExc = 'Exercise Name: '+excerciseName+'\n'+'Duration: '+excerciseTime+'\n'+'Calories Burned: '+excerciseCal
    bot.send_message(message.chat.id, messageExc)
    # TODO: 2.3 Get exercise data from the API-Done
    # TODO: 2.4 Display exercise data in the telegram chat-Done
    # TODO: 3.3 Dump data in a CSV file-Done
    d = []
    for i in [excerciseName,excerciseTime,excerciseCal]:
        d.append(i)
    with open('exercies_details.csv','a') as fe:
        csvwriter = csv.writer(fe)
        csvwriter.writerow(d)


@bot.message_handler(func=lambda message: botRunning, commands=['reports'])
def getCaloriesBurn(message):
    #bot.reply_to(message, 'Generating report...')
    # TODO: 3.4 Send downlodable CSV file to telegram chat
    greport = (message.text[9:]).split(',')
    if 'nutrition' in greport:
        bot.reply_to(message, 'Generating Nutritions report...')
        fileN=open('nutrition_details.csv','rb')
        bot.send_document(message.chat.id,fileN)
    if 'exercise' in greport:
        bot.reply_to(message, 'Generating Exercise report...')
        fileE=open('exercies_details.csv','rb')
        bot.send_document(message.chat.id,fileE)
        
    


@bot.message_handler(func=lambda message: botRunning)
def default(message):
    bot.reply_to(message, 'I did not understand '+'\N{confused face}')


bot.infinity_polling()