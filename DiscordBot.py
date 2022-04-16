import discord
import json
from discord.ext import commands

try:
    with open("token.sec", 'r') as tokenFile:
        token = tokenFile.read()
except:
    open("token.sec", 'x')
    print("Token file empty")
try:
    with open("channel.conf", "r") as confFile:
        botDict = json.load(confFile)
except:
    open("channel.conf", "x")
    botDict = {"rolesChannel": 0, "logChannel": 0, "configChannel": 0}
try:
    with open("roles.conf", "r") as confFile:
        rolesDict = json.load(confFile)
except:
    open("roles.conf", "x")
    rolesDict = {}

bot = commands.Bot(command_prefix="$")

get_channel = lambda c: bot.get_channel(c)

bot_config_channel = botDict["configChannel"]
log_channel = botDict["logChannel"]
role_channel = botDict["rolesChannel"]

@bot.event
async def on_ready():
    print("We have logged in as {0.user}".format(bot))

    await bot.change_presence(activity=discord.Game(name="Tetris"))

@bot.command()
async def test(ctx, arg):
    await ctx.send(arg)
    await send_to_log("message sent")

@bot.command()
async def clean(ctx):
    if is_admin(ctx):
        await ctx.channel.purge()
        await send_to_log("**" + ctx.author.name + "**" + " cleaned channel " + "**" + ctx.channel.name + "**")
    else:
        await send_to_log("something went wrong")


@bot.command()
async def addRole(ctx, name, emoji):
    if ctx.channel.id == bot_config_channel and ctx.author != bot.user and is_admin(ctx):
        rolesDict[name] = emoji
        save_roles()
        await send_to_log(ctx.author.name + " added role: " + name + " with emoji: " + emoji + " to role management")

@bot.command()
async def removeRole(ctx, name):
    if ctx.channel.id == bot_config_channel and ctx.author != bot.user and is_admin(ctx):
        rolesDict.pop(name)
        save_roles()
        await send_to_log(ctx.author.name + " removed role: " + name + " from role management")

@bot.command()
async def regenRoles(ctx):
    if ctx.channel.id == bot_config_channel and ctx.author != bot.user and is_admin(ctx):
        await bot.get_channel(role_channel).purge()

        rolesMessage = ""

        for r, e in rolesDict.items():
            rolesMessage += (e + " " + r + "\n")

        rolesMsg = await bot.get_channel(role_channel).send(content=rolesMessage)

        for e in rolesDict:
            await rolesMsg.add_reaction(rolesDict[e])

        await send_to_log(ctx.author.name + " regenerated the roles message in the roles channel")

@bot.command()
async def setLogChannel(ctx):
    if is_admin(ctx):
        botDict["logChannel"] = ctx.channel.id
        save_channels()
        log_channel = ctx.channel.id
        await send_to_log(ctx.author.name + " changed log-channel to: " + ctx.channel.name)

@bot.command()
async def setConfigChannel(ctx):
    if is_admin(ctx):
        botDict["configChannel"] = ctx.channel.id
        save_channels()
        await send_to_log(ctx.author.name + " changed config-channel to: " + ctx.channel.name)

@bot.command()
async def setRoleChannel(ctx):
    if is_admin(ctx):
        botDict["rolesChannel"] = ctx.channel.id
        save_channels()
        await send_to_log(ctx.author.name + " changed role-channel to: " + ctx.channel.name)


@bot.event
async def on_raw_reaction_add(reaction):
    user = reaction.member

    if reaction.channel_id == role_channel and user != bot.user:
        for name, emoji in rolesDict.items():
            if emoji == reaction.emoji.name:
                await user.add_roles(discord.utils.get(user.guild.roles, name=name), atomic = True)
                await send_to_log("role **" + name + "** given to " + user.name)
            #else:
            #    print("error" + reaction.emoji.name)

@bot.event
async def on_raw_reaction_remove(reaction):
    user = ""
    if reaction.channel_id == role_channel and user != bot.user:
        for member in bot.get_all_members():
            if member.id == reaction.user_id:
                user = member
                for name, emoji in rolesDict.items():
                    if emoji == reaction.emoji.name:
                        await user.remove_roles(discord.utils.get(user.guild.roles, name=name), atomic = True)
                        await send_to_log("role **" + name + "** removed from " + user.name)
                        continue
                    #else:
                    #    print("error" + reaction.emoji.name)

    
async def send_to_log(message):
    print(message)
    await get_channel(log_channel).send(message)

def save_roles():
    with open("roles.conf", "w") as file:
        json.dump(rolesDict, file)

def save_channels():
    with open("channel.conf", "w") as file:
        json.dump(botDict, file)

def is_admin(ctx):
    return discord.utils.find(lambda r: r.name == 'Admin', ctx.guild.roles) in ctx.author.guild.roles


    #client.get_user(reaction.user_id)

bot.run(token)
