import discord
import os
import requests
import json
import random
from replit import db
from live import live

client = discord.Client()

fun_words = ["funny", "fun", "meme", "anime", "laugh", "joke", "amusing", "hilarious", "comic"]

fun_encouragements = [
  """ 
  “I’m sick of following my dreams, man. I’m just going to ask where they’re going and hook up with ’em later. 🥶” —Mitch Hedberg 
  """,

  """ 
  “Gentlemen, you can’t fight in here. This is the war room. 👻 ” 
  —President Merkin Muffley
  """,

  """
  “My mother always used to say: The older you get, the better you get, unless you’re a banana. 👾” —Rose (Betty White), The Golden Girls
  """,

  """ 
  “Halloween is the beginning of the holiday shopping season. That’s for women. The beginning of the holiday shopping season for men is Christmas Eve. 👽” -David Letterman
  """,

  """
  “Before you criticize someone, you should walk a mile in their shoes. That way when you criticize them, you are a mile away from them and you have their shoes. 🤖” —Jack Handey
  """,

  """
  Bob: “Looks like you’ve been missing a lot of work lately.”
Peter: “I wouldn’t say I’ve been missing it, Bob. 🤡”
—Bob (Paul Wilson) and Peter (Ron Livingston), Office Space
""",

"""
“Clothes make the man. Naked people have little or no influence in society. 🎃”
—Mark Twain
""",
"""
“Before you marry a person, you should first make them use a computer with slow Internet to see who they really are. 🤯” —Will Ferrell
""",

"""
“I love being married. It’s so great to find that one special person you want to annoy for the rest of your life. 🕵️‍♂️” —Rita Rudner
""",

"""
“I want my children to have all the things I couldn’t afford. Then I want to move in with them. 👨‍🔬” —Phyllis Diller
"""
]

workout_words = ["gym", "hard", "bench", "squat" "cardio", "diet", "pump", "bulk", "cut", "pr"]

workout_motivation = [
  """ “Of course it’s hard. It’s supposed to be hard. If it were easy, everybody would do it. Hard is what makes it great. 🦾”
  """,

  """
  “Your body can stand almost anything. It’s your mind that you have to convince. 🧠”
  """,

  """
  “Success isn’t always about greatness. It’s about consistency. Consistent hard work gains success. Greatness will come. 👨‍🎓”
  """,

  """
  “Train insane or remain the same. 👩‍🏫”
  """,

  """
  “Definition of a really good workout: when you hate doing it, but you love finishing it. 👨‍🎨”
  """,
  """
  “Push yourself because no one else is going to do it for you. 👨‍⚖️”
  """,
  """
  “Success starts with self-discipline. 🤵”
  """
]

if "responding" not in db.keys():
  db["responding"] = True


def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouraging_message]

def delete_encouragment(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
  db["encouragements"] = encouragements

@client.event
async def on_ready():
  print('Vibey user is logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  msg = message.content
  
  if msg.startswith('!motivation'):
    quote = get_quote()
    await message.channel.send(quote + " 🤟")

  if db["responding"]:
    options = fun_encouragements
    if "encouragements" in db.keys():
      options = options + db["encouragements"]

    if any(word in msg for word in fun_words):
      await message.channel.send(random.choice(options))

    elif any(word in msg for word in workout_words):
      await message.channel.send(random.choice(workout_motivation))


  if msg.startswith("!new"):
    encouraging_message = msg.split("!new ", 1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New vibey memo added 👨‍🚀")
  
  if msg.startswith("!del"):
    encouragements = []
    if "encouragements" in db.keys():
      index = int(msg.split("!del", 1)[1])
      delete_encouragment(index)
      encouragements = db["encouragements"]
      await message.channel.send(encouragements)
  
  if msg.startswith("!list"):
    encouragements = []
    if "encouragements" in db.keys():
      encouragements = db["encouragements"]
    await message.channel.send(encouragements)

  if msg.startswith("!responding"):
    value = msg.split("!responding ",1)[1]
    
    if value.lower() == "on":
      db["responding"] = True
      await message.channel.send("Responding is on 🧙")
    elif value.lower() == "off":
      db["responding"] = False
      await message.channel.send("Responding is off 🧛") 


live()
client.run(os.getenv('TOKEN'))