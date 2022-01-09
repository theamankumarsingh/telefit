import os,sys
from os import environ
import telebot
import requests
import json
import csv

def send_file(file,file_id):
    doc = open(file, 'rb')
    bot.send_document(chatid, doc)
    bot.send_document(chatid, file_id)
    doc.close()
    return(0)

# TODO: 1.1 Add Request HTTP URL of the API
os.environ['NUTRITIONIX_API_KEY'] = '90def6c337fde1172fe481c2741f3a79'
os.environ['NUTRITIONIX_APP_ID'] = 'cd43a2ba'
os.environ['http_api'] = '5024529250:AAEglZoPDW2MWyouwyHbfxXbkX9b7e9yLEY'

NUTRITIONIX_API_KEY = environ['NUTRITIONIX_API_KEY']
NUTRITIONIX_APP_ID = environ['NUTRITIONIX_APP_ID']
HTTP_API = environ['http_api']

urlnutrient='https://trackapi.nutritionix.com/v2/natural/nutrients'
urlexercise='https://trackapi.nutritionix.com/v2/natural/exercise'

headers = {'Content-Type': 'application/json',
           'x-app-id': NUTRITIONIX_APP_ID, 'x-app-key': NUTRITIONIX_API_KEY}

user = {'name': None, 'gender': None,
        'weight': None, 'height': None, 'age': None}

chatid='-687895137'

bot = telebot.TeleBot(HTTP_API)


@bot.message_handler(commands=['start', 'hello'])
def greet(message):
    global botRunning
    botRunning = True
    # TODO: 3.1 Add CSV file creation
    outputFile1 = open('nutrition_records.csv', 'w', newline='')
    outputWriter1 = csv.writer(outputFile1)
    outputWriter1.writerow(['Food Name','Quantity','Calories','Fat','Carbohydrates','Protein',])
    outputFile1.close()

    outputFile2 = open('exercise_records.csv', 'w', newline='')
    outputWriter2 = csv.writer(outputFile2)
    outputWriter2.writerow(['Exercise','Duration','Calories-Burned'])
    outputFile2.close()
    
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
    m=usr_input.split(',')
    # TODO: 2.1 Set user data
    user['name']=m[0]
    user['gender']=m[1]
    user['weight']=m[2]
    user['height']=m[3]
    user['age']=m[4]
    bot.reply_to(message, 'User set!')
    
    # TODO: 2.2 Display user details in the telegram chat
    reply = ''
    for i in user:
        reply+=i+': '+user[i]+'\n'
    bot.send_message(message.chat.id, reply)


@bot.message_handler(func=lambda message: botRunning, commands=['nutrition'])
def getNutrition(message):
    bot.reply_to(message, 'Getting nutrition info...')
    # TODO: 1.2 Get nutrition information from the API
    count=int(message.text[11:12])
    item=message.text[13:]
    body={"query":"message"}
    body["query"]=item
    response = requests.post(urlnutrient,headers=headers,json=body)
    response.raise_for_status()
    j=json.loads(response.text)['foods']
    
    # TODO: 1.3 Display nutrition data in the telegram chat
    l=[]
    l.append(j[0]['food_name'])
    l.append(str(count)+' '+j[0]['serving_unit'])
    l.append(str(round(count*float(j[0]['nf_calories']),2)))
    l.append(str(round(count*float(j[0]['nf_total_fat']),2)))
    l.append(str(round(count*float(j[0]['nf_total_carbohydrate']),2)))
    l.append(str(round(count*float(j[0]['nf_protein']),2)))
    s='Food Name: '+l[0]+'\n'
    s+='Quantity: '+l[1]+' '+'\n'
    s+='Calories: '+l[2]+'\n'
    s+='Fat: '+l[3]+'\n'
    s+='Carbohydrate: '+l[4]+'\n'
    s+='Protein: '+l[5]+'\n'
    bot.send_message(chatid,s)
    # TODO: 3.2 Dump data in a CSV file
    outputFile1 = open('nutrition_records.csv', 'a', newline='')
    outputWriter1 = csv.writer(outputFile1)
    outputWriter1.writerow(l)
    outputFile1.close()


@bot.message_handler(func=lambda message: botRunning, commands=['exercise'])
def getCaloriesBurn(message):
    bot.reply_to(message, 'Estimating calories burned...')
    # TODO: 2.3 Get exercise data from the API
    m=message.text[10:].split()
    time=int(m[0])
    unit=m[1]
    exercise=''
    l=[]
    for i in range(2,len(m)):
        exercise+=m[i]+' '
    body={"query":"message"}
    body["query"]=exercise
    response = requests.post(urlexercise,headers=headers,json=body)
    response.raise_for_status()
    j=json.loads(response.text)['exercises']
    totalmin=j[0]['duration_min']
    totalcal=j[0]['nf_calories']
    if unit.lower()[:3]=='sec':
        time=time/60
    elif unit.lower()[:4]=='hour':
        time=time*60
    time=round(time,2)
    calpermin=int(totalcal)/int(totalmin)
    totalcal=round(calpermin*time,2)
    l.append(j[0]['name'])
    l.append(str(time))
    l.append(str(totalcal))
    
    # TODO: 2.4 Display exercise data in the telegram chat
    
    s=''
    s+='Exercise Name :'+l[0]+'\n'
    s+='Duration :'+l[1]+' minutes'+'\n'
    s+='Calories burned :'+l[2]+'\n'
    bot.send_message(chatid,s)
    # TODO: 3.3 Dump data in a CSV file
    
    outputFile2 = open('exercise_records.csv', 'a', newline='')
    outputWriter2 = csv.writer(outputFile2)
    outputWriter2.writerow(l)
    outputFile2.close()


@bot.message_handler(func=lambda message: botRunning, commands=['reports'])
def getCaloriesBurn(message):
    bot.reply_to(message, 'Generating report...')
    # TODO: 3.4 Send downlodable CSV file to telegram chat
    m=message.text[9:].split(',')
    if len(m)==2:
        send_file('exercise_records.csv','Exercise1')
        send_file('nutrition_records.csv','Nutrition1')
        
    elif len(m)==1 and m[0].lower()=='exercise':
        send_file('exercise_records.csv','Exercise2')
        
    elif len(m)==1 and m[0].lower()=='nutrition':
        send_file('nutrition_records.csv','Nutrition2')
        
    else:
        bot.send_message(chatid,'Try again')


@bot.message_handler(func=lambda message: botRunning)
def default(message):
    bot.reply_to(message, 'I did not understand '+'\N{confused face}')


bot.infinity_polling()
