import os
from os import environ
import telebot
import requests
import json
import csv

# 1.1 Add Request HTTP URL of the API
Url= "https://trackapi.nutritionix.com/v2/"
NUTRITIONIX_API_KEY = environ.get('NUTRITIONIX_API_KEY')
NUTRITIONIX_APP_ID = environ.get('NUTRITIONIX_APP_ID')
HTTP_API = environ.get('http_api')


headers = {'x-app-id': NUTRITIONIX_APP_ID, 'x-app-key': NUTRITIONIX_API_KEY}
user = {'name': None, 'gender': None,
        'weight': None, 'height': None, 'age': None}
bot = telebot.TeleBot(HTTP_API)


@bot.message_handler(commands=['start', 'hello'])
def greet(message):
    global botRunning
    botRunning = True
    # 3.1 Add CSV file creation
    fileN = open("nutrition_records.csv","w",newline='')
    fileE = open("exercise_records.csv","w",newline='')
    Writer = csv.writer(fileE)
    Writer.writerow(["Exercise-Name", "Duration", "Calories-Burned"])
    Writer = csv.writer(fileN)
    Writer.writerow(["Food-Name", "Quantity", "Calories", "Fat", "Carbohydrates", "Protein"])
    fileN.close()
    fileE.close()
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
    usr_input = (message.text)[6:]
    # 2.1 Set user data
    usr_input = usr_input.split(",")
    user['name'] = usr_input[0] 
    user['gender'] = usr_input[1]
    user['weight'] = usr_input[2]
    user['height'] = usr_input[3]
    user['age'] = usr_input[4]
    bot.reply_to(message, 'User set!')
    reply = 'name: {}\ngender: {}\nweight: {}\nheight: {}\nage: {}'.format(user['name'],user['gender'],user['weight'],user['height'],user['age'])
    # 2.2 Display user details in the telegram chat
    bot.send_message(message.chat.id, reply)


@bot.message_handler(func=lambda message: botRunning, commands=['nutrition'])
def getNutrition(message):
    bot.reply_to(message, 'Getting nutrition info...')
    message_text = (message.text)[10:] 
    query={ "query": message_text }

    # 1.2 Get nutrition information from the API
    url= Url+"natural/nutrients"
    response = requests.request("POST", url, headers=headers, data=query)

    # 1.3 Display nutrition data in the telegram chat
    food = response.json()['foods'][0]
    foodname = str(food["food_name"])
    quantity = str(food["serving_qty"])+" "+str(food["serving_unit"])
    calories = str(food["nf_calories"])
    fat = str(food["nf_total_fat"])
    carbohydrates = str(food["nf_total_carbohydrate"])
    protein = str(food["nf_protein"])
    reply ="FoodName: {}\nQuantity: {}\nCalories: {}\nFat: {}\nCarbohydrates: {}\nProtein: {}".format(foodname,quantity,calories,fat,carbohydrates,protein)
    bot.reply_to(message, reply)

    # 3.2 Dump data in a CSV file
    file = open("nutrition_records.csv","a",newline='')
    Writer = csv.writer(file)
    Writer.writerow([foodname, quantity, calories, fat, carbohydrates, protein])
    file.close()


@bot.message_handler(func=lambda message: botRunning, commands=['exercise'])
def getCaloriesBurn(message):
    bot.reply_to(message, 'Estimating calories burned...')
    message_text = (message.text)[9:] 
    query={ "query": message_text }

    #2.3 Get exercise data from the API
    url = Url+"natural/exercise"
    response = requests.request("POST", url, headers=headers, data=query)
    exercise = response.json()['exercises'][0]
    # 2.4 Display exercise data in the telegram chat
    exercisename = exercise["user_input"]
    duration = exercise["duration_min"]
    caloriesburned  = exercise["nf_calories"]
    reply="Exercise Name: {}\nDuration: {}\nCalories Burned: {}".format(exercisename,duration,caloriesburned)
    bot.reply_to(message, reply)
    # 3.3 Dump data in a CSV file

    file = open("exercise_records.csv","a",newline='')
    Writer = csv.writer(file)
    Writer.writerow([exercisename, duration, caloriesburned])
    file.close()


@bot.message_handler(func=lambda message: botRunning, commands=['reports'])
def getCaloriesBurn(message):
    bot.reply_to(message, 'Generating report...')
    # 3.4 Send the downlodable CSV file to telegram chat
    usr_input = message.text[9:]
    chatid = message.chat.id
    fileN = open("nutrition_records.csv","rb")
    fileE = open("exercise_records.csv","rb")
    if  "nutrition, exercise" in usr_input:
        bot.send_document(chatid,fileE)
        bot.send_document(chatid,fileN)
    elif "exercise" in usr_input:
        bot.send_document(chatid,fileE)
    elif "nutrition" in usr_input:
        bot.send_document(chatid,fileN)
    fileE.close()
    fileN.close()

@bot.message_handler(func=lambda message: botRunning)
def default(message):
    bot.reply_to(message, 'I did not understand '+'\N{confused face}')
    

bot.infinity_polling()


