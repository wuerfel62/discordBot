import discord
from discord.ext import commands
import Wordle


'''
richtig an der stelle -> bold (**letter**)
richtig an anderer stelle -> bold (*letter*)
'''
token = ""

intents = discord.Intents.default()
intents.members = True
intents.reactions = True
client = discord.Client(intents=intents)

#bot = commands.bot(command_prefix='!')

get_channel = lambda c: client.get_channel(c)
wordle = Wordle.wordle()
#msgs = []

log_channel = 962787056445161502
role_channel = 962431123319824434

def get_msg_content(msg):
    word_list = msg.split(" ")
    return word_list[1]

@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))

    wordle.is_ingame = False

    await client.change_presence(activity=discord.Game(name="Wordle"))


@client.event
async def on_message(message):
    role = discord.utils.find(lambda r: r.name == 'Admin', message.guild.roles)
    if message.channel.name == "bot_testing" and message.author.roles[1] == role and message.author != client.user:
        #msgs.append(message)

        #if message.author == client.user:
        #    return
        
        #if message.content.startswith("!hello"):
        #    await message.channel.send("Hello!")

        if message.content == "!clean":
            await message.channel.purge()
            await get_channel(log_channel).send("**" + message.author.name + "**" + " cleaned channel " + "**" + message.channel.name + "**")

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
    else:
        ""

@client.event
async def on_raw_reaction_add(reaction):
    user = reaction.member

    if reaction.channel_id == role_channel:
        if str(reaction.emoji) == "🔴":
            await user.add_roles(discord.utils.get(user.guild.roles, name="Member"), atomic = True)
            print("role Member given to " + user.name)
            await get_channel(log_channel).send("role **Member** given to " + user.name)
        elif str(reaction.emoji) == "🔵":
            await user.add_roles(discord.utils.get(user.guild.roles, name="Member"), atomic = True)
            print("role Member given to " + user.name)
            await get_channel(log_channel).send("role **Member** given to " + user.name)
        else:
            print("error")

@client.event
async def on_raw_reaction_remove(reaction):
    user = ""
    for member in client.get_all_members():
        if member.id == reaction.user_id:
            user = member
            
    #client.get_user(reaction.user_id)

    if reaction.channel_id == role_channel:
        if str(reaction.emoji) == "🔴":
            await user.remove_roles(discord.utils.get(user.guild.roles, name="Member"), atomic = True)
            print("role Member removed from " + user.name)
            await get_channel(log_channel).send("role **Member** removed from " + user.name)
        elif str(reaction.emoji) == "🔵":
            await user.remove_roles(discord.utils.get(user.guild.roles, name="Member"), atomic = True)
            print("role test removed from " + user.name)
            await get_channel(log_channel).send("role **Member** removed from " + user.name)
        else:
            print("error")

#bot.run("OTQ3MTU4NTkzOTIzMzQ2NDUz.YhpMLg.ovRz6LNWow5UPtvVgBNdXFrQ8TQ")


client.run(token)
