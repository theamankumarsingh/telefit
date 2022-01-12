import os
from os import environ
import telebot
import requests
import json
import csv
import io

NUTRITIONIX_API_KEY = 'd29b20ecd0b3b0248d067a90ce8e373e'
NUTRITIONIX_APP_ID = 'ee36d7b7'
HTTP_API = os.getenv('API_KEY')

HEADERS = {'Content-Type': 'application/json',
           'x-app-id': NUTRITIONIX_APP_ID, 'x-app-key': NUTRITIONIX_API_KEY,"x-remote-user-id": "0"}
user = {'name': None, 'gender': None,
        'weight': None, 'height': None, 'age': None}
bot = telebot.TeleBot('5014210290:AAGmfaDaQ-Tv6lnhAskJUl7UeX-GlNmvD4U')


@bot.message_handler(commands=['start', 'hello'])
def greet(message):
    global botRunning
    global nutrition
    global exercise
    global exercise_csv
    global nutrition_csv
    botRunning = True
    # TODO: 3.1 Add CSV file creation
    nutrition_csv = open("nutrition.csv","w")
    exercise_csv = open("exercise.csv","w")
    #exercise = io.StringIO()
    exercise=csv.writer(exercise_csv)
    nutrition=csv.writer(nutrition_csv)
    #exercise.seek(0)
    #nutrition = io.StringIO()
    #nutrition.seek(0)
    exercise.writerow(["Item Name","Quantity","Total weight(g)","Proteins","Carbohydrates","Calories","Cholestrols","Total Fat","Saturated Fat","Fibres","Potassium","Sodium","Sugars"])
    nutrition.writerow(['Bye'])
    exercise_csv.close()
    nutrition_csv.close()

    bot.reply_to(
        message, 'Hi,Hello,Namaste,Aadam! I am TeleFit. Use me to monitor your health'+'\N{grinning face with smiling eyes}'+'\nYou can use the command \"/help\" to know more about me.')


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
    try:
      user["name"]=usr_input[0].strip()
      user["gender"]=usr_input[1].strip()
      user["weight"]=usr_input[2].strip()
      user["height"]=usr_input[3].strip()
      user["age"]=usr_input[4].strip()
    except:
      bot.send_message(message.chat.id,"Error : ENTER THE CORRECT DETAILS\nUsage : /user <NAME>,<GENDER>,<WEIGHT(kg)>,<HEIGHT(cm)>,<AGE>\nExample : /user Prashanth,Male,80,192,17")
      return -1
    if(str(user['gender']).lower()!='male' and str(user['gender']).lower()!='female'):
      bot.send_message(message.chat.id,"Error!!\nGender should be male or female")
      return -1
    bot.reply_to(message, 'User set!')
    # TODO: 2.2 Display user details in the telegram chat
    bot.send_message(message.chat.id,"User Name : "+str(user['name'])+"\nGender : "+str(user['gender'])+"\nWeight : "+str(user['weight'])+"\nHeight : "+str(user['height'])+"\nAge : "+str(user['age']))


@bot.message_handler(func=lambda message: botRunning, commands=['nutrition'])
def getNutrition(message):
    #temp=str(message)
    #print(temp)
    #temp=list(temp.split(','))
    #for i in range(0,len(temp)):
      #if "'text': '" in temp[i]:
        #x=temp[i]
    #print(x)
    #x=x[9:]
    #x=x[1:-1]
    #x=x.split()
    y=message.text[11:]
    if(y==''):
      bot.send_message(message.chat.id,"Enter a food item \nUsage :/nutrition <QUERY>\nExample : /nutrition 1 piece pizza\nExample : /nutrition dosa 1 piece\nExample : /nutrition burger 2")
      return -1
    #print(x)
    #print("\n\n\n\n\n")
    bot.reply_to(message, 'Getting nutrition info...')
    # TODO: 1.2 Get nutrition information from the API
    #
    url="https://trackapi.nutritionix.com/v2/natural/nutrients"
    paramaters='{"query": "'+str(y)+'","locale": "en_US"}'
    n=1
    
    response = requests.post(url,paramaters,headers=HEADERS)
    #print(response)
    #bot.send_message(message.chat.id,response)
    data1 = json.loads(response.text)#response.content.decode('utf-8'))
    #print(data1)
    try:
      quantity=data1['foods'][0]['serving_qty']
      item_name=data1['foods'][0]['food_name']
      serv_wt=data1['foods'][0]['serving_weight_grams']
      totfat=data1['foods'][0]['nf_total_fat']
      satfat=data1['foods'][0]['nf_saturated_fat']
      chol=data1['foods'][0]['nf_cholesterol']
      cal=data1['foods'][0]['nf_calories']
      prot=data1['foods'][0]['nf_protein']
      carbs=data1['foods'][0]['nf_total_carbohydrate']
      fibr=data1['foods'][0]['nf_dietary_fiber']
      pota=data1['foods'][0]['nf_potassium']
      sod=data1['foods'][0]['nf_sodium']
      sug=data1['foods'][0]['nf_sugars']
    except:
      bot.send_message(message.chat.id,"Error!\nNo food item found"+'\N{confused face}')
      return -1
    bot.send_message(message.chat.id,"Item Name :"+str(item_name.upper())+"\nTotal Serving Weight(g) : "+str(serv_wt)+"\nQuantity : "+str(quantity)+"\n\nTotal Nutrition Values : "+"\n\nProteins : "+str(prot)+"\nCarbohydrates : "+str(carbs)+"\nCalories : "+str(cal)+"\nCholestrols : "+str(chol)+"\nTotal Fat : "+str(totfat)+"\nSaturated Fat : "+str(satfat)+"\nFibres : "+str(fibr)+"\nPotassium : "+str(pota)+"\nSodium : "+str(sod)+"\nSugars : "+str(sug))
    
    #if(int(x[2])>1):
      #bot.send_message(message.chat.id,"Item Name :"+str(item_name.upper())+"\nQuantity : "+str(n)+"\nTotal weight(g) : "+str(serv_wt*n)+"\n\nNutrition Values For Your Meal: "+"\n\nProteins : "+str(prot*n)+"\nCarbohydrates : "+str(carbs*n)+"\nCalories : "+str(cal*n)+"\nCholestrols : "+str(chol*n)+"\nTotal Fat : "+str(totfat*n)+"\nSaturated Fat : "+str(satfat*n)+"\nFibres : "+str(fibr*n)+"\nPotassium : "+str(pota*n)+"\nSodium : "+str(sod*n)+"\nSugars : "+str(sug*n))
    #
    # TODO: 1.3 Display nutrition data in the telegram chat
    # TODO: 3.2 Dump data in a CSV file
    nutrition_csv = open("nutrition.csv","w")
    nutrition=csv.writer(nutrition_csv)
    nutrition.writerow([str(item_name.upper()),str(quantity),str(serv_wt*n),str(prot*n),str(carbs*n),str(cal*n),str(chol*n),str(totfat*n),str(satfat*n),str(fibr*n),str(pota*n),str(sod*n),str(sug*n)])
    bot.send_message(message.chat.id,"Updated the csv file")


@bot.message_handler(func=lambda message: botRunning, commands=['exercise'])
def getCaloriesBurn(message):
    bot.reply_to(message, 'Estimating calories burned...')
    # TODO: 2.3 Get exercise data from the API
    inp = message.text[10:].split()
    url="https://trackapi.nutritionix.com/v2/natural/exercise"
    
    parameters1={
      "query":str(inp),
      "gender":str(user['gender']),
      "weight_kg":user['weight'],
      "height_cm":user['height'],
      "age":user['age']
    }
    #print(user['gender'])
    if(str(user['gender'])=='None'):
      bot.send_message(message.chat.id,"You need to set user using /user to add your name")
    response1 = requests.post(url,json=parameters1,headers=HEADERS)
    #print(response1)
    data1 = json.loads(response1.text)
    #print(data1)
    try:
      bot.send_message(message.chat.id,"User Name : "+str(user['name'])+"\nTotal calories burnt : "+str(data1['exercises'][0]['nf_calories'])+" calories")
    except:
      bot.send_message(message.chat.id,"Error!!\nEnter correct data and correct exercise\nUsage : /exercise <NUMBER OF MINUTES> minutes <EXERCISE DONE>\nExample: /exercise 40 minutes push-ups \nMust include all special characters like '-' i.e. \npush-ups : correct\npushups  :wrong")
      return -1
    # TODO: 2.4 Display exercise data in the telegram chat
    # TODO: 3.3 Dump data in a CSV file
    #print(data1['exercises'][0]['nf_calories'])

    exercise.writerow(["User Name : "+str(user['name']),"Exercise Done : "+str(inp),"Total calories burnt : "+str(data1['exercises'][0]['nf_calories'])+" calories"])



@bot.message_handler(func=lambda message: botRunning, commands=['reports'])
def getCaloriesBurn(message):
    bot.reply_to(message, 'Generating report...')
    x=message.text[9:]
    if(x==''):
      bot.send_message(message.chat.id,"Usage : /reports <NAME OF REPORT>\nExample : /reports nutrition\nExample : /reports exercise")
      return -1
    
    x=x.split(',')
    for i in range(0,len(x)):
      if(str(x[i]).lower().strip()=='nutrition'):
        #buf = io.BytesIO()
        #buf.write(nutrition.getvalue().encode())
        #buf.seek(0)
        #buf.name = f'Nutrition_Report.csv'
        #try:
        nutrition_csv.close()
        #final_nut=open("nutrition.csv","rb")
        bot.send_document(message.chat.id,nutrition_csv)
        nutrition_csv.close()
        #except:
          #bot.send_message(message.chat.id,"Use the /nutrition command before requesting the nutrition report")
      elif(str(x[i]).lower().strip()=='exercise'):
        #buf = io.BytesIO()
        #buf.write(exercise.getvalue().encode())
        #buf.seek(0)
        #buf.name = f'Exercise_Report.csv'
        #try:
        
        #final_exe=open("exercise.csv","rb")
        bot.send_document(message.chat.id,exercise_csv)
        exercise_csv.close()
        #except:
          #bot.send_message(message.chat.id,"Use the /exercise command before requesting the nutrition report")
      else:
        bot.send_message(message.chat.id,"Error!!\nNo report found for "+str(x[i]))

      
    


@bot.message_handler(func=lambda message: botRunning)
def default(message):
    bot.reply_to(message, 'I did not understand '+'\N{confused face}')


bot.infinity_polling()
