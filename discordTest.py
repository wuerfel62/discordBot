import discord
import Wordle
import json

'''
richtig an der stelle -> bold (**letter**)
richtig an anderer stelle -> bold (*letter*)
'''

with open("token.sec", 'r') as tokenFile:
    token = tokenFile.read()

with open("bot.conf", "r") as confFile:
    botDict = json.load(confFile)

with open("roles.conf", "r") as confFile:
    rolesDict = json.load(confFile)

intents = discord.Intents.default()
intents.members = True
intents.reactions = True
client = discord.Client(intents=intents)


get_channel = lambda c: client.get_channel(c)
wordle = Wordle.wordle()
#msgs = []

bot_config_channel = botDict["configChannel"]
log_channel = botDict["logChannel"]
role_channel = botDict["rolesChannel"]
game_channel = botDict["gamesChannel"]

def get_msg_content(msg):
    word_list = msg.split(" ")
    return word_list[1]

@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))

    wordle.is_ingame = False

    await client.change_presence(activity=discord.Game(name="Solitaire"))


@client.event
async def on_message(message):
    role = discord.utils.find(lambda r: r.name == 'Admin', message.guild.roles)
    if message.channel.id == game_channel and message.author.roles[1] == role and message.author != client.user:
        #msgs.append(message)

        if message.content == "!clean":
            await message.channel.purge()
            await send_to_log(log_channel).send("**" + message.author.name + "**" + " cleaned channel " + "**" + message.channel.name + "**")

        if message.content == "!play":
            #await message.channel.send(wordle.guessedWords)
            await message.channel.send("Game Started")
            wordle.start_game()
            
        
        if message.content == "!stop":
            if wordle.is_ingame == True:
                wordle.is_ingame = False
                await message.channel.send("Game Stopped")
                print("Wordle game stopped")

        if message.content.startswith("!guess") and wordle.is_ingame:
            
            print("guessed word: " + (message.content).split("!guess ")[1])
            #wordle.guessedWords.append(get_msg_content(message.content))

            guest_words = wordle.check_word((message.content).split("!guess ")[1])

            #await message.channel.send(guest_words)
            
            for w in guest_words:
                await message.channel.send(w)
            if wordle.is_ingame == False:
                await message.channel.send("Game Ended")

    elif message.channel.id == bot_config_channel and message.author != client.user:
        msgContent = message.content.split()
        if msgContent[0] == "!role-add" and len(msgContent) == 3:
            rolesDict[msgContent[1]] = msgContent[2]
            save_roles()
            await send_to_log(message.author.name + " added role: " + msgContent[1] + "with emoji: " + msgContent[2])
        elif msgContent[0] == "!role-remove" and len(msgContent) == 2:
            rolesDict.pop(msgContent[1])
            save_roles()
            await send_to_log(message.author.name + " removed role: " + msgContent[1])
        elif msgContent[0] == "!regen-roles" and len(msgContent) == 1:
            await client.get_channel(role_channel).purge()

            rolesMessage = ""

            for r, e in rolesDict.items():
                rolesMessage += (e + " " + r + "\n")

            rolesMsg = await client.get_channel(role_channel).send(content=rolesMessage)

            for e in rolesDict:
                await rolesMsg.add_reaction(rolesDict[e])

            await send_to_log(message.author.name + " regenerated the roles message")
    else:
        ""

@client.event
async def on_raw_reaction_add(reaction):
    user = reaction.member

    if reaction.channel_id == role_channel and user != client.user:
        for name, emoji in rolesDict.items():
            if emoji == reaction.emoji.name:
                await user.add_roles(discord.utils.get(user.guild.roles, name=name), atomic = True)
                await send_to_log(log_channel).send("role **" + name + "** given to " + user.name)
            else:
                print("error" + reaction.emoji.name)

@client.event
async def on_raw_reaction_remove(reaction):
    user = ""
    if reaction.channel_id == role_channel and user != client.user:
        for member in client.get_all_members():
            if member.id == reaction.user_id:
                user = member
                for name, emoji in rolesDict.items():
                    if emoji == reaction.emoji.name:
                        await user.remove_roles(discord.utils.get(user.guild.roles, name=name), atomic = True)
                        await send_to_log("role **" + name + "** removed from " + user.name)
                    else:
                        print("error" + reaction.emoji.name)
    
async def send_to_log(message):
    print(message)
    await get_channel(log_channel).send(message)

def save_roles():
    with open("roles.conf", "w") as file:
        json.dump(rolesDict, file)


    #client.get_user(reaction.user_id)

client.run(token)
