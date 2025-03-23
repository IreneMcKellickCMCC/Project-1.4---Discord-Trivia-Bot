#Importing necessary packages
import discord
from discord.ext import commands
import asyncio
import requests
import json

#Need the intents to initialize the bot
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

#Getting bot to collect a question from the API
def get_question():
    qs = ''
    id = 1
    answer = 0
    response = requests.get('http://127.0.0.1:8000/api/random/')
    json_data = json.loads(response.text)
    #Display question with numbered answers for people to type
    qs += "Question: \n"
    qs += json_data[0]['title'] + "\n"

    for item in json_data[0]['answer']:
        qs += str(id) + ". " + item['answer'] + "\n"

        if item['is_correct']:
            answer = id

        id += 1

    return(qs, answer)


#Preventing infinite loop and giving message condition to prompt bot
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('q!'):
        qs, answer = get_question()
        await message.channel.send(qs)

    def check(m):
        return m.author == message.author and m.content.isdigit()
    #Setting max response time to 5 seconds
    try:
        guess = await client.wait_for('message', check=check, timeout=5.0)
    except asyncio.TimeoutError:
        return await message.channel.send('Oops! You took too long to answer. Try again')
    #Setting feedback messages for correct and incorrect answers
    if int(guess.content) == answer:
        await message.channel.send('Correct! Good job')
    else: 
        await message.channel.send('Incorrect. Try again')
#Insert token here
client.run('TOKEN')